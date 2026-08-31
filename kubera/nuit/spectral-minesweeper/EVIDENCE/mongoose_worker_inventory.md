# EVIDENCE — mongoose worker inventory (determinism contract)

**What this is:** the full list of worker modules in `mongooses/` (5th-house-kubera,
branch `cocktail-v3`) — the deterministic pipeline stages that do the actual
in-sample/out-of-sample/stress computation, deduplication, normalization, and
report assembly. Filenames only; no math internals.

**Why this is evidence, not decoration:** every mongoose that dispatches the
pricing/backtest engine does so under LOCK-20 — the engine is invoked twice per
candidate and the two output hashes must match exactly, or the candidate is
marked `IDEMPOTENCY_MISMATCH` and excluded. See `SNIPPETS/idempotency_check.py`
for the actual dispatch-twice-and-compare code.

## Count

`mongooses/` holds 22 directory entries: 20 deterministic worker modules
(19 `mongoose_*.py` files + `regime_classifier.py`), plus `__init__.py` and a
`sandbox/` scratch subdirectory (not workers, excluded from the "~21-22
deterministic workers" count in `VERIFICATION.md`).

## Inventory (the 20 worker modules)

```
mongoose_candidate_audit.py
mongoose_combined_window_enrichment.py
mongoose_daily_pass.py
mongoose_day_level_v5.py
mongoose_dd_budget_model_DEPRECATED_v2.py
mongoose_dedup_2_5.py
mongoose_feasibility_ablation.py
mongoose_ledger_compaction.py
mongoose_nautilus_backtest.py
mongoose_per_year_normalization.py
mongoose_strategion_gate.py
mongoose_v_deploy_report.py
mongoose_v_is_from_anvil.py
mongoose_v_is_parallel.py
mongoose_v_is.py
mongoose_v_manifest.py
mongoose_v_oos.py
mongoose_v_stress.py
mongoose_v_stress_retail_v5.py
regime_classifier.py
```

`mongoose_v_is.py` + `mongoose_v_is_parallel.py` + `mongoose_v_is_from_anvil.py`
are three variants of the same gate, kept side by side rather than silently
overwritten — another instance of the "state the wrong turn, don't erase it"
discipline seen in `LINEAGE.md`. Likewise `mongoose_dd_budget_model_DEPRECATED_v2.py`
is retired in its own filename, not deleted.

## The contract, in one sentence

Idempotent by construction: identical inputs must produce byte-identical outputs
on a second run, verified per-candidate, or the pipeline halts that candidate
rather than silently accepting drift.
