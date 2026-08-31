# Architecture

Fred is two systems. They share a name, a household, and a lineage moment (the Hume→openSMILE
migration described below), but they are different codebases, at different points on the
build/run spectrum, doing different jobs. This document describes each, then the one place they
are designed to meet.

## System A — the voice-note bot line (RUNNING)

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

**Hosting.** Two live deployment modes for the same bot, by design: a Cloud Run service
(`python:3.11-slim`, `ffmpeg`/`libsndfile1` for audio, `FRED_ENABLE_HUME_FALLBACK` and
`FRED_GEMINI_TRANSCRIPTION_MODEL` as runtime-selectable env vars — provider choice is a deploy-time
knob, not a hard dependency baked into the code) that runs the Flask webhook, and a local
long-running polling copy (`poll_runner.py`, launchd `KeepAlive`) for when the webhook is
deliberately torn down — the runner's own docstring names the handoff "Path W protocol" so the two
are never live against Telegram at the same time.

**Status: RUNNING, event-driven.** Four launchd jobs on the household Mac keep the bot line active
day to day: a `WatchPaths` agent wired directly into the real macOS Voice Memos recordings folder
(fires a one-shot processing pass on every new recording — its log shows real, clean-completing
fires through 2026-08-24), the local Telegram poller itself (`KeepAlive`-restarted, log active
through 2026-08-30), a 30s sync job, and a 60s inbox-bridge job. This is not inferred from a
changelog — it is a live PID (`launchctl list`) and dated log output observed directly. See
[`EVIDENCE/launchd_automation_and_live_activity.md`](EVIDENCE/launchd_automation_and_live_activity.md)
for the full plist contents, the currently-loaded job table, and an honest read of what the logs do
and don't show (the poller's most recent log lines are a recurring unhandled-exception error, not a
clean success — reported as such, not smoothed over).

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

**Status: BUILT+DORMANT.** Scoring code untouched since the 2026-04-10 validation event. The
`Source Material` corpus directory backing that event holds 391 dated files spanning
2026-03-17–2026-04-15 — a one-month batch gathered around the validation, not a continuously
updated feed; no evidence of detector-specific activity was found past that window. (The bot
line's own voice-note ingestion is separately, currently live — see System A above and
[`EVIDENCE/launchd_automation_and_live_activity.md`](EVIDENCE/launchd_automation_and_live_activity.md)
— but that liveness belongs to the bot, not to this detector's scoring pipeline; the two are not
conflated here.) Proven once, deliberately parked, not decayed.

## Where the two systems are designed to meet

Nothing in the current code path wires the detector's floor-check output into the bot's replies,
or into Abraxas. The intended integration — voice note → both flows run → detector output becomes
somatic context Abraxas can reason over when the family is deciding something — is **designed, not
built**. The root [`STORY.md`](../../STORY.md) diagram and this project's own README mark that
edge with a dashed line for exactly that reason: it is the honest state of the connection, not an
aspiration dressed as a fact.

## Running vs. dormant — why two different words

- **RUNNING** (the bot): four always-on launchd jobs, a live PID on the local poller, and dated log
  activity through 2026-08-24 (watcher, clean completions) and 2026-08-30 (poller, still logging,
  though its most recent lines are errors rather than clean success — see the evidence file).
- **BUILT+DORMANT** (the detector): a validated pipeline, deliberately not re-run since its
  2026-04-10 validation event; no detector-specific activity found past its April corpus window.

Both are honest states, and neither is "broken" or "abandoned" — the distinction is worth keeping
precisely because the two systems' liveness is now genuinely different, not because one status word
would be more flattering than the other. Collapsing them into one status would either overstate the
detector's current activity or understate that the bot line is live, unglamorous errors and all.
