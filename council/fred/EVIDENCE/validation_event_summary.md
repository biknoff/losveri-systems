# Evidence: the validation event (2026-04-10)

**What this is:** a summary, stated at the abstraction level this repo requires, of the event the
operator's own documentation calls the detector's strongest proof point — sourced from a bounded
search of operator-authored markdown for an April-10 reference. The underlying record contains a
personal quote and a session-level acute/non-acute label; **neither is reproduced here**. This
file states only the *design property* the event demonstrates.

**Redactions:** no verbatim quote, no health/clinical label, no per-turn score, no participant
identity beyond "the operator" and "a household member" (both already nameable per this repo's
redaction rules as operators/subjects-by-choice, in the abstract only).

## What happened, abstractly

On 2026-04-10, the detector scored a same-day voice note and flagged a subset of the operator's
turns as outside their personal acoustic reference. Independently — without access to the
detector's output — a household member raised a wellbeing check-in with the operator that same
afternoon, prompted by nothing but ordinary observation. The two observations (instrument-in-
machine, instrument-in-household) landed on the same day, about the same person, without either
side having seen the other's signal.

## Why this counts as validation, and what it does not prove

- **What it demonstrates:** the detector's within-person acoustic-deviation signal correlated,
  same-day, with an independent human observation of the same person — a real cross-validation
  against a signal the detector had no access to and could not have been tuned against.
- **What it does not demonstrate:** this is a single event (n=1), same-day, not clinically
  replicated, not independently adjudicated, and not a controlled trial. It is strong
  proof-of-concept for the architecture — a deterministic, personally-baselined acoustic signal
  landing on the same day as an independent human read — not a clinical validation, and it is
  never described as one anywhere in this repository.
- The detector's own design (see [`study1_design_excerpt.md`](study1_design_excerpt.md)) is
  explicit that this class of signal is "acoustically out-of-reference," not a diagnosis — this
  event is consistent with, not an exception to, that framing.

## Operational note

The detector's scoring code has been untouched since this event (2026-04-10); the voice-note
ingestion pipeline that feeds its corpus kept running independently afterward, into at least
mid-2026. This is the shape of "BUILT+DORMANT (validated)" used throughout this directory: proven
once, deliberately not re-run since, not decayed or abandoned mid-build.
