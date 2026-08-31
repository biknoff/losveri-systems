# Evidence: detector — deterministic feature extraction + within-person baseline design

**What this is:** verbatim excerpts from the openSMILE/eGeMAPS extraction call and the
within-person baseline builder (`emotion_calibrated.py`, `dysregulation_baseline_v2.py`,
`1st House - Fred Beta/`), read-only via SSH. This shows the *design shape* only — the feature
*names* eGeMAPS defines, and the *statistical procedure* used to build a personal reference. It
never shows a computed value, threshold, or baseline number belonging to any person.

**Redactions:** every absolute filesystem path containing an operator's home directory or a
corpus location has been replaced with a generic placeholder (`<corpus root>`); no such path,
real or placeholder-filled, points at an audio file. No numeric feature value is reproduced from
this codebase anywhere in this repository.

## The extractor is deterministic openSMILE, not a hosted affect model

```python
def _get_smile():
    """Lazy-load openSMILE eGeMAPSv02 extractor."""
    global _smile
    if _smile is not None:
        return _smile
    import opensmile
    _smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    return _smile
```

The production Fred pipeline (`1st House - Fred/audio_analysis.py`) loads two extractor
instances side by side — eGeMAPSv02 and ComParE_2016 — both at `Functionals` level (i.e.
per-segment statistical summaries of the low-level descriptors, not raw frame-by-frame series).
openSMILE is a local, open-source, deterministic DSP toolkit: the same audio in always produces
the same feature vector out. No network call, no hosted-model version drift, no probabilistic
sampling — the property the within-person-baseline design (below) depends on.

## The curated feature subset (names only — this is a public, standard eGeMAPS vocabulary)

```python
RAW_FEATURES = [
    "F0semitoneFrom27.5Hz_sma3nz_amean",
    "F0semitoneFrom27.5Hz_sma3nz_stddevNorm",
    "F0semitoneFrom27.5Hz_sma3nz_percentile20.0",
    "F0semitoneFrom27.5Hz_sma3nz_percentile80.0",
    "jitterLocal_sma3nz_amean",
    "jitterLocal_sma3nz_stddevNorm",
    "shimmerLocaldB_sma3nz_amean",
    "shimmerLocaldB_sma3nz_stddevNorm",
    "HNRdBACF_sma3nz_amean",
    "spectralFlux_sma3_amean",
    "spectralFlux_sma3_stddevNorm",
    "slopeV0-500_sma3nz_amean",
    "slopeV500-1500_sma3nz_amean",
    "loudness_sma3_amean",
    "loudness_sma3_stddevNorm",
    "mfcc1_sma3_amean", "mfcc2_sma3_amean", "mfcc3_sma3_amean", "mfcc4_sma3_amean",
]
```

19 of the eGeMAPSv02 standard's 88 functionals — pitch (F0 in semitones, mean/variability/
percentile spread), voice-quality (jitter, shimmer, harmonics-to-noise ratio), spectral (flux,
slope in two bands), loudness, and low-order MFCCs. These are the published eGeMAPS feature
names (Eyben et al. 2016), not anything proprietary or personal — the curation choice (why these
19 of 88) is the design artifact, not the names themselves.

## Within-person baseline: robust statistics, hour-of-day conditioned

```python
def robust_stats(values: np.ndarray) -> dict:
    """Median, MAD (scaled to sigma-equivalent), percentiles, min/max."""
    med = float(np.median(values))
    mad_raw = float(np.median(np.abs(values - med)))
    mad_sigma = mad_raw * 1.4826
    p25, p50, p75, p90, p95 = np.percentile(values, [25, 50, 75, 90, 95]).tolist()
    return {"n": int(values.size), "mean": ..., "std": ..., "median": med,
            "mad": mad_raw, "mad_sigma": mad_sigma,
            "p25": p25, "p50": p50, "p75": p75, "p90": p90, "p95": p95,
            "min": ..., "max": ...}

def build_baseline(records: list[dict]) -> dict:
    overall = {feat: _stats_for_feature(records, feat) for feat in RAW_FEATURES}
    by_hour: dict[str, dict] = {}
    buckets = defaultdict(list)
    for r in records:
        if r["hour"] is not None:
            buckets[r["hour"]].append(r)
    for hour, recs in sorted(buckets.items()):
        if len(recs) < 20:          # minimum-support gate — no baseline from a thin hour bucket
            continue
        by_hour[str(hour)] = {"n_turns": len(recs),
                               "features": {f: _stats_for_feature(recs, f) for f in RAW_FEATURES}}
    return {"overall": overall, "by_hour_of_day": by_hour}
```

Design shape: median + MAD (median absolute deviation, scaled by 1.4826 to a sigma-equivalent) is
used instead of mean/stddev — the standard robust-statistics choice when a distribution may
contain real outlier turns (a raised voice, a laugh) that a mean-based baseline would let distort
the reference itself. The baseline is computed **overall** and **separately per hour-of-day
bucket**, with a hard floor of 20 turns before an hour bucket is trusted enough to report — thin
buckets are silently excluded rather than baselined on weak support. Turns under 0.35s duration
and turns missing ≥25% of the curated feature set are filtered out before baseline construction
(`collect_leo_turns`, same file). No baseline number, percentile value, or threshold appears here
or anywhere in this repository.

## Reference documentation (existence only)

A technical reference document, `Vocal_Dysregulation_Detection_Technical_Reference.docx`, exists
in the operator's files describing this pipeline in full. Its content is not reproduced here
(binary format, not fetched for this evidence set); its existence is noted as corroboration that
the detector has written technical documentation beyond the code itself.
