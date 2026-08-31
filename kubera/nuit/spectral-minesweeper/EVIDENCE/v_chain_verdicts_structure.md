# EVIDENCE — V-chain verdicts on disk (structure, not values)

**What this is:** field-name and row-count evidence that the Cold-Firing V-chain
(V_is → V_oos → V_stress) actually ran, taken from one cold-firing cohort, `cf11`,
in `5th-house-kubera` (branch `cocktail-v3`).

**Why redacted:** the `config` block per candidate encodes strategy parameters
(entry/exit windows, stop sizing, symbol/rule combinations) — trade secret. All
gate thresholds (PF cutoffs, parity bounds) are trade secret. Only field names,
row counts, verdict enums, and file dates are shown. See `SNIPPETS/verdict_row_structure.jsonl`
for the field-level shape with values stripped.

## Source paths (read-only, not copied verbatim)

```
cold_firing_cf11_v_is/v_is_verdicts.jsonl
cold_firing_cf11_v_oos/v_oos_verdicts.jsonl
cold_firing_cf11_v_stress/v_stress_verdicts.jsonl
```

## Row counts and dates

| Gate | File | Rows | mtime (UTC) |
|---|---|---|---|
| V_is (in-sample) | `v_is_verdicts.jsonl` | 360 | 2026-05-11 17:34:10 |
| V_oos (out-of-sample) | `v_oos_verdicts.jsonl` | 2 | 2026-05-11 17:34:10 |
| V_stress (stress) | `v_stress_verdicts.jsonl` | 0 | 2026-05-11 17:34:10 |

All three files share one mtime — the chain ran through in one pass, gate to gate,
not hand-assembled after the fact.

## What the counts mean

- 360 candidates entered V_is (in-sample profitability + year-health check).
- 2 of those 360 passed V_is and were carried into V_oos.
- Both of the 2 **failed** V_oos — `"verdict": "FAIL"` with cited `fail_reasons`
  (e.g. `PF_oos<threshold`, `parity>threshold`, `grade=WEAK`) — pre-declared gate
  names, not post-hoc rationalization.
- 0 candidates reached V_stress for this cohort, because nothing survived V_oos.
  The empty file is itself evidence: a chain that produces an empty downstream
  file when nothing qualifies, rather than fabricating a row, is doing what a
  non-cherry-picking pipeline should do.

`cf11` was chosen for this excerpt precisely because it is not a success story —
it shows the gates actually killing candidates, which is stronger evidence of a
real (not decorative) validation chain than a cohort that passed everything.

## Other cohorts on disk

`cf11` is one of ~180 `cold_firing_*` run directories under this branch (dated
2026-05 across ~cf1 through cf39 plus URR/basket/retro variants); most session
directories also carry a `passers.json`. Only `cf11`'s three verdict files are
excerpted here; the rest are read-only sources not reproduced.
