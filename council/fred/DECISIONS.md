# Decisions

## 1. Within-person baseline, not population norms
**Rejected: scoring every voice note against population-wide affect norms.** A population
reference answers "how unusual is this voice relative to other people" — a different, weaker
question than "is this person at their own baseline." Once the operating question changed to the
latter, the whole downstream design (feature choice, statistical procedure, validation plan) had
to be re-anchored on one person's own longitudinal history rather than a population distribution.
See [`LINEAGE.md`](../../LINEAGE.md) thread 3 and [`EVIDENCE/study1_design_excerpt.md`](EVIDENCE/study1_design_excerpt.md).

## 2. Deterministic openSMILE/eGeMAPS features, not a hosted affect API, for a floor decision
**Rejected: continuing to route the floor-check itself through Hume.** A hosted, versioned,
probabilistic affect model can drift under the hood between calls — acceptable for population-
relative scoring, disqualifying for a personal reference that must be reproducible call to call.
The migration moved extraction to openSMILE (local, deterministic, open-source DSP) precisely
because the same audio must always produce the same feature vector, or "personal baseline" is not
a well-defined concept. See [`EVIDENCE/detector_feature_extraction_and_baseline_design.md`](EVIDENCE/detector_feature_extraction_and_baseline_design.md).

## 3. Two systems, stated as two
**Rejected: blurring the bot and the detector into one pitch.** The bot (a Telegram voice-note
assistant, PAUSED) and the detector (a deterministic prosody-baseline pipeline, BUILT+DORMANT) are
different codebases with different status, different validation, and different failure modes.
Presenting them as one "Fred product" would let the bot's liveliness (or the detector's rigor)
launder the other's actual status. Stated separately here — separate badges, separate evidence,
separate architecture sections — on the same principle the rest of this repo holds to: honesty is
the aesthetic.

## 4. No clinical claims, ever
**Rejected: describing the detector as diagnosing, screening, or flagging a clinical condition.**
The detector's own design document explicitly avoids the term "dysregulation" as its scientific
claim, coining "time-conditioned acoustic deviation" instead, and states directly that "a future
observation may be acoustically out-of-reference without assigning a latent emotional,
physiological, or diagnostic cause." This repo's ceiling matches that discipline: "dysregulation
detection relative to a personal baseline," never a medical or diagnostic claim, regardless of how
compelling the one real validation event was.

## 5. Frozen in-sample reference + chronological out-of-sample test, not adaptive-only
**Rejected: a purely walk-forward/adaptive baseline from the start.** The primary validation rule
fits the time-conditioned reference entirely in-sample, freezes it, and forbids updating it during
the primary OOS test — only after that frozen result is established does an adaptive walk-forward
variant get evaluated, and only as a secondary operational analysis. This is the same discipline
named in the root `VERIFICATION.md` as shared with the trading pipeline: prove the frozen model
generalizes before you let it adapt.

## 6. Hour-of-day-conditioned baseline, not one flat personal average
**Rejected: a single time-invariant personal baseline.** "Expected acoustic state" varies
systematically with time of day for a given person; averaging across all hours would blur that
structure into noise and make a night-time voice look artificially "off" against a daytime mean.
The baseline is built per-hour-bucket (with a 20-turn minimum-support floor before a bucket is
trusted) as well as overall, so a deviation is measured against "expected self at this time," not
"expected self on average."

## 7. Pre-declared stress tests over a single held-out check
**Rejected: validating with one train/test split and calling it done.** The design pre-declares
six falsification tests before running the primary analysis (temporal shuffle/null,
high-comparability audio subset, session-balancing, alternative time binning, feature-family
leave-out, boundary/clock stress) — the same "try to break your own result before you trust it"
ethic that governs the trading pipeline's own OOS discipline, applied here to a within-person
acoustic model instead of a strategy edge.
