# Decisions

## 1. Symlink the live bytes into the build tree
**Rejected: a copied tree.** A copy drifts silently — that is exactly the failure this mirror
replaced (a fork taken at an unrecorded moment, 11 of 75 files different by the time anyone
looked, and nothing in the old system could notice). A symlink cannot drift without the target
changing, and the target changing is exactly what the verifier's check A/C watch for.

## 2. Prove the one unavoidable diff mechanically, every build
**Rejected: trust a code review that the patch is visibility-only.** A human reviewing a diff and
attesting "this is just `pub`" is a claim, not a proof, and it does not survive the diff changing
later. Reversing the declared patch and hash-comparing to the pristine snapshot is a check that
runs every time, at build time, and fails the build if it's ever wrong — not a one-time sign-off.

## 3. A real shim broker with venue-matching + broker-personality netting
**Rejected: idealized fills** (a hand-rolled fill model with no netting, no ticket consolidation,
no broker-side margin arithmetic). The whole point of era-exact acceptance is to find out what the
live engine's own recon race conditions and netting-merge edges actually do under realistic
matching — an idealized fill model would have hidden the one real defect the acceptance found
(a market-order under-fill on a no-spread tape) rather than surfacing it.

## 4. Era-exact segmented replay for acceptance, not "current binary over history"
**Rejected: replay the whole window under today's code and call the delta noise.** That conflates
two different questions — "does the mirror reproduce what live actually did" and "what would
today's code have done differently." The acceptance keeps them separate: segmented, era-exact runs
answer the first; one separate current-binary run answers the second as an explicit counterfactual.

## 5. Every diff row gets a named cause class, or it's red
**Rejected: an aggregate match-rate score.** A percentage match rate can hide a systematic,
explainable gap behind a merely-adequate-looking number, and it can also hide one real bug inside
a mass of tolerable timing noise. Row-by-row attribution to a fixed, named class list means an
unclassifiable row cannot be averaged away — it stays visibly red.

## 6. The nightly digest states unpriced rows explicitly
**Rejected: silent partial sums.** A digest that quietly sums only the rows it could price will
understate the day's live total whenever pricing fails for reasons unrelated to trading — and
nobody reading a lower-than-real number would know to ask why. This was a real bug (2026-08-29,
see `EVIDENCE/unpriced_rows_honesty.md`), fixed by threading an explicit unpriced-row count and
note through every rollup level rather than fixing only the top-line total.

## 7. The nightly reconciler consumes the witness spine, not engine memory
**Rejected: querying the live engine's live state directly.** The witness spine is an append-only,
already-committed record of what happened; querying live state risks racing an in-flight order or
reading a value that changes between the query and the write. It also keeps the reconciler
structurally read-only with respect to the live engine — the same "watcher cannot author"
boundary applied elsewhere in this repo's supervision layer.

## 8. Deploys still route through a human reading the rehearsal verdict
**Rejected: auto-deploy on a passing mirror run.** The mirror's job is to make the rehearsal
trustworthy, not to make the deploy decision. A passing verdict is necessary evidence for a human
deploy decision; it is deliberately not wired to trigger one on its own.
