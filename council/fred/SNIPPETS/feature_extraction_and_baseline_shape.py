# Source: 1st House - Fred Beta/emotion_calibrated.py + dysregulation_baseline_v2.py
# (excerpted, lightly reformatted for one file; logic and identifiers verbatim).
# Shows the DESIGN SHAPE only: deterministic feature extraction + a within-person,
# hour-of-day-conditioned robust baseline. No computed values, thresholds, or
# baselines belonging to any person appear anywhere in this file.

import numpy as np
from collections import defaultdict


# --- Deterministic extraction: local DSP, not a hosted affect model ---

def _get_smile():
    """Lazy-load openSMILE eGeMAPSv02 extractor."""
    import opensmile
    return opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )


# Curated subset of the 88-dim eGeMAPSv02 functional set (published, standard
# feature names — Eyben et al. 2016 — not proprietary or personal):
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


# --- Within-person baseline: robust stats, hour-of-day conditioned ---

def robust_stats(values: np.ndarray) -> dict:
    """Median, MAD (scaled to sigma-equivalent), percentiles, min/max.

    Median/MAD chosen over mean/stddev deliberately: a raised-voice or
    laughing turn should not drag the personal reference itself off center.
    """
    med = float(np.median(values))
    mad_sigma = float(np.median(np.abs(values - med))) * 1.4826
    p25, p50, p75, p90, p95 = np.percentile(values, [25, 50, 75, 90, 95]).tolist()
    return {
        "n": int(values.size), "median": med, "mad_sigma": mad_sigma,
        "p25": p25, "p50": p50, "p75": p75, "p90": p90, "p95": p95,
    }


def build_baseline(records: list[dict]) -> dict:
    """Overall baseline + a separate baseline per hour-of-day bucket.

    Buckets under 20 turns are dropped rather than trusted on thin support —
    the personal reference is only as good as the support behind each hour.
    """
    overall = {feat: robust_stats(np.array([r[feat] for r in records])) for feat in RAW_FEATURES}

    buckets = defaultdict(list)
    for r in records:
        if r["hour"] is not None:
            buckets[r["hour"]].append(r)

    by_hour = {}
    for hour, recs in sorted(buckets.items()):
        if len(recs) < 20:
            continue
        by_hour[str(hour)] = {
            "n_turns": len(recs),
            "features": {f: robust_stats(np.array([r[f] for r in recs])) for f in RAW_FEATURES},
        }

    return {"overall": overall, "by_hour_of_day": by_hour}
