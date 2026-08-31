# ARCHITECTURE — Spectral Minesweeper

Part of NUIT — see [../../../STORY.md](../../../STORY.md) § "NUIT began as a
discovery system." For the canonical statement of what the apparatus *is*
(discipline-agnostic), see the reference blueprint quoted in `README.md` §
"The general form"; this page covers what was actually built.

## Two layers

1. **What ran (BUILT):** the Cold-Firing candidate-generation and V-chain
   validation pipeline — chunk substrate, mongoose workers, ledger, receipts,
   seals. Concrete, exercised, verdicts on disk.
2. **What was specified but not built (DESIGNED):** SEER (terrain discovery,
   Rung 2) and PROBE (directed candidate search within fertile terrain) — the
   general `(ΦT, ΦM, G)` apparatus described in Blueprint v4. The mid-build
   honesty is the point: Cold-Firing is what "PROBE without SEER" — blind
   search — looks like in practice, per the blueprint's own § 3.1.

## 1. Chunk substrate (`engine/spectral/`)

The engine components were built and contracted in numbered "chunks," 0
through 7 (with sub-versions at 6.5 and 7 v2/v3). Every chunk carries a
`*_contract.json` (what it promises), a `*_manifest.json` (what it produced),
and a `*_tests.json` (what was checked) — see
`EVIDENCE/chunk_stage_substrate.md` for the full stage list. Chunk names only;
kernel math, PDE derivations, and corpus-generator internals are withheld.

## 2. Mongoose workers (`mongooses/`) — the determinism contract

22 directory entries; 20 are deterministic worker modules (19 `mongoose_*.py`
+ `regime_classifier.py`), covering candidate audit, dedup, per-year
normalization, feasibility filtering, and the V-gate mongooses themselves
(`mongoose_v_is.py`, `mongoose_v_oos.py`, `mongoose_v_stress.py`).

**The contract (LOCK-20):** any mongoose that dispatches the pricing/backtest
engine does so *twice* per candidate. The two runs' output hashes must match
exactly (`hash_run1 == hash_run2`); a mismatch is recorded as
`IDEMPOTENCY_MISMATCH` and the candidate is excluded rather than accepted on a
best-of-two basis. See `SNIPPETS/idempotency_check.py`. This is enforced per
candidate, not sampled — every candidate that reaches the engine gets the
double-dispatch check.

## 3. The V-chain gates (names, not thresholds)

Three sequential gates, each with pre-declared pass/fail criteria fixed before
the run, not chosen after seeing results:

- **V_is** — in-sample: does the candidate clear a profitability bar with
  acceptable year-to-year health, across the in-sample window?
- **V_oos** — out-of-sample: does the in-sample survivor's edge persist on
  held-out data, within a declared in-sample/out-of-sample parity band?
- **V_stress** — stress: do V_oos survivors hold up under declared stress
  conditions (only reached if something survives V_oos)?

Each gate writes a `*_verdicts.jsonl` file — one row per candidate, every row
carrying its `verdict` and, on failure, the specific `fail_reasons` that fired.
See `EVIDENCE/v_chain_verdicts_structure.md` for the real field names and row
counts from one cohort (`cf11`, dated 2026-05-11) with all numeric values
redacted, and `SNIPPETS/verdict_row_structure.jsonl` for the shape.

## 4. Ledger — the six-state contract classifier

`ledger/contract_state.py` is a pure function: given per-component runtime
results and the declared contract, it returns one of six states, ranked worst
to best:

```
BROKEN → CONTRACT_MISMATCH → SCAFFOLD_ONLY → SEARCH_INFEASIBLE
       → PARTIAL_SPEC_ACTIVE → FULL_SPEC_ACTIVE
```

`PARTIAL_SPEC_ACTIVE` (a component running on a declared fallback rather than
its primary implementation) is explicitly marked not eligible for "funded"
status under LOCK-22 — a partially-substituted pipeline cannot claim full
credibility even if it happens to produce a plausible-looking output. See
`SNIPPETS/contract_state_classifier.py`.

## 5. Discipline layer: receipts, seals, alchemical stages

- **50 receipts** in `receipts/` — every handoff addressed `_to_operator`,
  dated, stage-scoped. See `EVIDENCE/receipts_and_seals.md`.
- **17 seals** in `seals/` — counted only, contents never opened per this
  project's sourcing constraint; the sealing mechanism itself is documented in
  `kubera/nuit/build-method-governance/`.
- **Alchemical stage vocabulary** (Calcination, Sublimation, Cibation,
  Conjunction, Fermentation, Projection...) — an ordered, fixed naming
  convention across the Minesweeper v3/v4/v5 working trees, so any artifact's
  build phase is legible from its directory name. Vocabulary discipline, not
  a claim about mechanism — the apparatus's own blueprint (§ 1.4) explicitly
  refuses to let any single metaphor become foundational. See
  `EVIDENCE/alchemical_stage_vocabulary.md`.

## 6. What's withheld, and why

| Withheld | Why |
|---|---|
| `FORMULA_LIBRARY/` | Never opened, never listed. A formula library exists and is withheld — trade secret. |
| Gate thresholds (PF cutoffs, parity bounds, stress conditions) | Trade secret — these are the pipeline's actual edge-discrimination power. |
| `config` blocks in verdict rows (entry/exit windows, stop sizing, symbol+rule combos) | Trade secret strategy parameters. |
| Chunk 3/4 math (log-likelihood, PDE derivation, kernel implementation) | Trade secret model internals. |
| Corpus-grammar / candidate-generation internals | Trade secret. |
| Candidate/leg names | Replaced with opaque tokens throughout. |
| Seal contents | Sourcing constraint for this project; see governance project instead. |
| P&L figures | Never shown, here or anywhere in this repo. |

## What SEER/PROBE would add (DESIGNED, not built)

Per Blueprint v4: SEER would discover the terrain representation ΦT — the
latent coordinate that predicts *which regions of terrain are generatively
fertile* — from a constructed residual field (§ 7 of the blueprint). PROBE
would then search within fertile terrain for surviving manifestations. Neither
exists yet; Cold-Firing's Sobol-style candidate sweep is explicitly named in
the blueprint itself as "blind search... expensive, undirected" — what PROBE
looks like *without* SEER. The honest framing: the build that happened (Cold-
Firing) was good, disciplined work; it is also, by the apparatus's own later
self-correction, not yet the apparatus it was reaching for.
