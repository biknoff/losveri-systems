# Architecture

Fred is two systems. They share a name, a household, and a lineage moment (the Hume→openSMILE
migration described below), but they are different codebases, at different points on the
build/run spectrum, doing different jobs. This document describes each, then the one place they
are designed to meet.

## System A — the voice-note bot line (PAUSED, verified)

**What it does.** A Telegram bot that receives a voice note, transcribes it, and responds —
including parsing and executing expense entries (the same expense-to-ledger function Chris now
owns; Fred's bot line predates and originally carried that logic).

**Two-phase response design.** The production entry point (`fred_bot_cloud_integration.py`,
v6.3.8, "Progressive Response Architecture") is built around timing targets, not a single
synchronous handler:

- **Phase 0** — acknowledge receipt in under 1s.
- **Phase 1** — transcribe, parse, and execute the fast deterministic path (e.g. an expense
  entry) in parallel, target 5s. The user's confirmation is sent here.
- **Phase 2** — the affective/prosody pass (originally Hume) runs in the background and is only
  *awaited* — blocking the reply — when the response is conversational rather than transactional.

The point of the split: a slow, probabilistic affective call never blocks a fast, deterministic
one. See [`EVIDENCE/bot_v6_3_8_header_and_two_phase_design.md`](EVIDENCE/bot_v6_3_8_header_and_two_phase_design.md)
for the verbatim header and constants.

**Lineage: Hume era → later Gemini migration.** The bot's affect pass began on Hume (a hosted
affect API); its transcription/generation stack separately went through a documented sequence of
model swaps over roughly five months — a transcription-model change, a Gemini 3.5 migration, a
lighter-weight model swap, a local-Whisper evaluation, a Gemini 3.7 Flash canonicalization, and a
thinking-budget tuning pass — each preserved as a dated backup file rather than overwritten. See
[`EVIDENCE/migration_trail_and_cloud_hosting.md`](EVIDENCE/migration_trail_and_cloud_hosting.md).

**Hosting.** Runs as a Cloud Run service (`python:3.11-slim`, `ffmpeg`/`libsndfile1` for audio,
`FRED_ENABLE_HUME_FALLBACK` and `FRED_GEMINI_TRANSCRIPTION_MODEL` as runtime-selectable env vars —
provider choice is a deploy-time knob, not a hard dependency baked into the code).

**Status: PAUSED, verified working.** The bot is not currently receiving traffic in production,
but its most recent state is a working, self-consistent codebase (its own startup log and
Telegram greeting both self-report v6.3.8, matching the operator's record) — paused by choice, not
abandoned mid-build.

## System B — the deterministic prosody/dysregulation detector (BUILT+DORMANT)

**What it does.** Extracts acoustic features from a voice note using openSMILE (a local,
deterministic DSP toolkit — not a hosted, versioned, probabilistic model) at the eGeMAPSv02
functional level, and compares them against a personal, hour-of-day-conditioned baseline built
from that same person's longitudinal voice notes. Ceiling claim: **dysregulation detection
relative to a personal baseline.** Never a diagnosis. Never a medical claim.

**Why deterministic extraction, specifically.** A personal baseline is only a well-defined concept
if the same audio always produces the same feature vector — a hosted affect model can drift
between calls under an SDK or model-version change in ways that would silently corrupt a "this is
your normal" reference. See [`DECISIONS.md`](DECISIONS.md) #2.

**Baseline / floor concept.** The baseline builder pulls a curated ~19-feature subset of the
88-dim eGeMAPSv02 output (pitch, jitter, shimmer, harmonics-to-noise ratio, spectral flux/slope,
loudness, low-order MFCCs — published, standard feature names) per speech turn, filters out very
short turns and turns with too much missing data, then computes **median + MAD-based robust
statistics** (deliberately not mean/stddev, to resist a single loud or unusual turn distorting the
reference) — both **overall** and **separately per hour-of-day bucket**, with a 20-turn minimum
before a bucket is trusted. A later observation is checked against "expected self at this time,"
not "expected self on average" or "expected person in general." See
[`EVIDENCE/detector_feature_extraction_and_baseline_design.md`](EVIDENCE/detector_feature_extraction_and_baseline_design.md)
and [`SNIPPETS/feature_extraction_and_baseline_shape.py`](SNIPPETS/feature_extraction_and_baseline_shape.py).

**Validation.** Design discipline documented in `Study 1 Design v2` (a locked research roadmap):
fit the time-conditioned reference entirely in-sample, freeze it, test chronological out-of-sample
— no peeking, no adaptive updates during the primary test — then run six pre-declared
falsification/stress tests before trusting the result (temporal shuffle, high-comparability audio
subset, session-balancing, alternative time binning, feature-family leave-out, boundary/clock
stress). Same OOS ethic as the trading pipeline, applied to prosody. See
[`EVIDENCE/study1_design_excerpt.md`](EVIDENCE/study1_design_excerpt.md).

A real cross-validation event (2026-04-10) is the strongest single proof point: the detector's
acoustic-deviation signal and an independent household observation of the same person landed on
the same day, without either side seeing the other's signal. Single event, not clinically
replicated — proof-of-concept, stated as exactly that. See
[`EVIDENCE/validation_event_summary.md`](EVIDENCE/validation_event_summary.md).

**Hosting.** A GPU-backed Cloud Run service (`diarize + identify + prosody + transcribe`,
`nvidia-l4`, `min-instances=0`) exists for the fuller pipeline this detector sits inside — scales
to zero between invocations, which is the literal, technical meaning of "dormant" here: nothing is
running or billing until it is deliberately invoked again.

**Status: BUILT+DORMANT.** Scoring code untouched since the 2026-04-10 validation event; the
voice-note ingestion feeding its corpus kept running independently for months afterward. Proven
once, deliberately parked, not decayed.

## Where the two systems are designed to meet

Nothing in the current code path wires the detector's floor-check output into the bot's replies,
or into Abraxas. The intended integration — voice note → both flows run → detector output becomes
somatic context Abraxas can reason over when the family is deciding something — is **designed, not
built**. The root [`STORY.md`](../../STORY.md) diagram and this project's own README mark that
edge with a dashed line for exactly that reason: it is the honest state of the connection, not an
aspiration dressed as a fact.

## Paused vs. dormant — why two different words

- **PAUSED** (the bot): a working, previously-live service, currently not receiving traffic, that
  could be turned back on largely as-is.
- **BUILT+DORMANT** (the detector): a validated pipeline, deliberately not re-run since its
  validation event, its ingestion/corpus side still alive independently of its scoring side.

Both are honest states, and neither is "broken" or "abandoned" — the distinction is worth keeping
because collapsing them into one status word would either overstate the bot's current activity or
understate how proven the detector already is.
