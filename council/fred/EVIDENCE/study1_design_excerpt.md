# Evidence: Study 1 design — chronological OOS + pre-declared stress tests

**What this is:** excerpts from `Study_1_Design_v2_Time_Conditioned_Acoustic_Reference.docx`
(locked design roadmap, version 2, dated 2026-08-30), extracted locally from the docx XML (a
`.docx` is a zip of XML parts; `word/document.xml` was unzipped and text-stripped, bounded to the
relevant sections). This is the design document referenced by the root [`VERIFICATION.md`](../../../VERIFICATION.md)
somatic-layer claim and [`LINEAGE.md`](../../../LINEAGE.md) thread 3.

**Redactions:** none required — this document is already written at the abstraction level this
repo requires (it explicitly avoids the clinical term "dysregulation" as its scientific claim; see
below). No personal acoustic values appear in the source document itself.

## The core architectural idea (verbatim)

> Population reference asks: "How unusual is this voice relative to other people?"
> Person-only reference asks: "How unusual is this voice relative to this person overall?"
> Time-conditioned personal reference asks: "How unusual is this voice relative to what is
> expected from this person at this time of day?"

## The scientific framing deliberately avoids clinical language (verbatim)

> Scientific term: time-conditioned acoustic deviation (T-CAD). The study does not require the
> psychological or clinical term "dysregulation." A future observation may be acoustically
> out-of-reference without assigning a latent emotional, physiological, or diagnostic cause.

## Primary validation rule — frozen in-sample reference, chronological OOS (verbatim)

> Primary validation rule: fit the time-conditioned reference entirely in-sample; freeze it; do
> not update it during the primary OOS test. Only after the frozen-reference result is established
> may an adaptive walk-forward version be evaluated as a secondary operational analysis.

Same discipline named explicitly in the root `VERIFICATION.md`: "chronological out-of-sample
splits and pre-declared stress tests... the same OOS discipline as the trading pipeline, applied
to prosody."

## Pre-declared falsification and stress tests (verbatim table, §14)

| Stress test | Question it answers |
|---|---|
| Temporal shuffle/null | Break the relationship between observations and clock time within appropriate temporal blocks. The reference model's advantage should collapse or materially weaken if real time structure drives the result. |
| High-comparability audio subset | Repeat on recordings with the strongest audio-domain comparability. Tests whether the temporal reference is an artifact of difficult source transformations. |
| Session-balanced analysis | Prevent days/conversations with many turns from dominating the reference or OOS score. |
| Alternative time binning | Run one or two predeclared reasonable neighboring time representations as sensitivity analyses, without re-optimizing after OOS. |
| Feature-family leave-out | Remove one major feature family at a time to see whether the core hypotheses depend entirely on a single fragile measurement family. |
| Boundary/clock stress | Test modest shifts in bin boundaries (e.g., ±30 min where predeclared) to ensure results are not an arbitrary artifact of exact hour cutoffs. |

## Explicit honesty about sample size (verbatim, §16)

> The effective human sample is two intensively observed people. Thousands of repeated
> observations increase information about within-person temporal structure; they do not turn N=2
> into a population cohort... The paper's claim should be architectural and within-person: whether
> expected self-at-time can be recovered and forward-validated in these two naturalistic
> longitudinal cases.

This is the same "state the honest gap, don't oversell" ethic the rest of this portfolio holds to
— the study design itself refuses to claim more than the evidence supports, which is why this
project's own claims are capped at "dysregulation detection relative to a personal baseline,"
never a clinical or diagnostic claim.
