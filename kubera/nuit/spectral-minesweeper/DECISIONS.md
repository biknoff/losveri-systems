# DECISIONS — Spectral Minesweeper

Choices made in the research pipeline itself, each with the alternative that
was considered and rejected. Ordered roughly by where each decision sits in
the pipeline, terrain-discipline decisions last.

## 1. Hash-identical or halt (LOCK-20 idempotency)

Every candidate that reaches the pricing engine is dispatched twice; the two
output hashes must match exactly or the candidate is excluded as
`IDEMPOTENCY_MISMATCH`.

**Rejected: tolerate flaky reruns / retry-and-average.** A pipeline that
averages away nondeterminism can no longer tell the difference between "this
candidate's edge is real" and "this candidate's edge is an artifact of
whichever run happened to land." Treating any mismatch as a hard failure keeps
the pipeline's numeric claims trustworthy at the cost of throwing away
candidates that might have been fine — the correct trade for a research
pipeline whose output feeds real capital decisions.

## 2. Pre-declared gates, not judged-after-the-fact

V_is/V_oos/V_stress criteria are fixed before a cohort runs; verdict rows cite
the specific `fail_reasons` that fired against the pre-declared thresholds.

**Rejected: judge results after seeing them.** Post-hoc threshold-setting is
how overfitting hides — pick the bar the candidate happens to clear, in
retrospect, and call it a criterion. Fixing the bar first, and letting most
candidates fail it (as cf11 shows — 360 in, 2 to V_oos, 0 to V_stress), is
what makes a pass mean something.

## 3. Six-state contract classification, with a partial-spec state that disqualifies

The ledger's classifier can mark a run `PARTIAL_SPEC_ACTIVE` when a component
is running on a declared fallback rather than its primary implementation —
and LOCK-22 makes that state explicitly ineligible for "funded" status.

**Rejected: treat fallback and primary as equivalent if the output looks
plausible.** A fallback component might produce a numerically reasonable
result while silently changing what's actually being measured. Refusing to
call a fallback-run result "fully specified" prevents a substituted pipeline
from quietly earning the same trust as the real one.

## 4. Sealed, receipted handoffs over ambient conversational memory

50 receipts, 17 GPG-sealed entries, each phase handoff addressed
`_to_operator` and dated — the crypto protocol lifts the same
hash-identical-or-halt instinct from numeric mongoose outputs up to
handoff *documents*.

**Rejected: trust the next session's summary of the last one.** An LLM
regenerating "what phase N concluded" from memory is indistinguishable, in
prose, from a faithful handoff — and is exactly how heuristic drift enters a
long AI-assisted build. Making "Phase N says X" mechanically checkable removes
that failure mode structurally rather than relying on discipline alone.

## 5. Alchemical stage names as a fixed vocabulary, not a metaphor to build around

Calcination → Sublimation → Cibation → Conjunction → Fermentation →
Projection order stage directories across the v3/v4/v5 working trees.

**Rejected: let the metaphor become the mechanism.** The apparatus's own
blueprint (§ 1.4) explicitly forbids any single explanatory metaphor
(chemotaxis, spectral decomposition, or — by the same logic — alchemy) from
becoming foundational. The vocabulary is used for exactly what a numbered
stage list would do: legible provenance by directory name. It is retained
*as* discipline precisely because it is not asked to explain anything.

## 6. Trading as proving ground, deliberately, with an explicit ethics boundary

The general `(ΦT, ΦM, G)` apparatus is discipline-agnostic; trading was chosen
as the first domain because manifestations are manufacturable and outcomes are
cheap and fast to evaluate.

**Rejected: point an immature apparatus at human domains first.** Blueprint v4
§ 6.1 states this directly — a false generative-analogy claim in a domain
involving people is borne by people, not by a P&L, and demands far more
adversarial scrutiny before anyone acts on it. The discipline is to let
trading validate the tool before the tool is ever pointed at higher-stakes
domains: "failures cost money, not people."

## 7. Name the unbuilt as DESIGNED, plainly

SEER and PROBE are stated as specified-but-not-built in this project's own
status badges, not folded into "BUILT" by implication.

**Rejected: demo-ware vocabulary.** Calling a designed-only component "built"
because its name appears in working code (Cold-Firing *is*, per the
blueprint's own framing, primitive PROBE-without-SEER) would blur exactly the
distinction this whole repo's honesty posture depends on. The correction is
part of the record: v3 mistook a vocabulary shadow (SBI-proper) for the
substance; v4's correction is written down, not quietly absorbed. Cold-Firing
is real, exercised work — being honest that it's not yet the full apparatus
does not diminish it.

## 8. Baseline-first factor extraction, sequencing over shortcutting

Blueprint v4 § 7 insists the residual field (Step 0: baseline model, subtract,
get `R_t`) must exist *before* factor extraction is attempted — a
well-posedness argument, not a scheduling preference.

**Rejected: search for the latent factor directly in raw outcomes.** Without a
baseline to subtract, "find the coordinate that explains this" is ill-posed —
there is no defined remainder to explain. This decision is recorded here
because it governs what any future SEER build must do first; it has not yet
been executed (see README status).

## 9. Fractal-φ slicing over multi-instrument infrastructure, for the first
   generative-analogy tests

`∼_G` (generative analogy between terrains) is testable within a single data
stream by context-slicing (ES-1h-at-London-open vs. ES-5m-at-NY-open, etc.)
rather than requiring multiple instruments up front.

**Rejected: build multi-instrument data infrastructure before testing whether
the core `∼_G` claim is even findable.** Slicing one stream fractally answers
the load-bearing question — can the apparatus find generative analogy at all —
cheaply, using data already on disk, before committing to the larger
infrastructure lift.
