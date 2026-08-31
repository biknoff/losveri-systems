<!-- WHAT: excerpt of build_verdict.py showing the 2026-08-29 fix that makes the nightly digest
     state unpriced matched rows explicitly instead of silently excluding them from the total.
     REDACTED: the specific dollar figures that triggered the fix (a live-vs-real total
     discrepancy example in the original code comment) and specific leg/time identifiers in the
     f-string are generalized to opaque tokens — the logic and the honesty property are the
     evidence, not the numbers that motivated it. -->

# The digest states unpriced rows, rather than a silent partial sum

Real bug, real fix, dated in the code: a nightly digest under-reported the day's live total
because two matched live exits could not be priced, and the summation silently dropped them
instead of surfacing that fact.

```python
# HONESTY FIX (2026-08-29, operator — a prior digest showed a live total that silently excluded
# unpriced rows: net_live silently summed only the priced rows, no signal that some matched exits
# had pnl_live=None).
# A row is "matched but unpriced" when it actually traded live (cls matched/qty_clamp_known)
# but resolve couldn't price it — net_live then EXCLUDES it, which must be stated, not implied.
unpriced_rows = [r for r in rows if r.get("cls") in ("matched", "qty_clamp_known")
                 and r.get("pnl_live") is None]
if unpriced_rows:
    notes.append(f"{len(unpriced_rows)} matched live exit(s) could not be priced (pnl_live=None) — "
                 f"net_live ${net_live:,.2f} EXCLUDES them: "
                 + ", ".join(f"{r['leg']}@{r['entry_et'][-5:]}" for r in unpriced_rows))
```

The row count (`n_unpriced`) is threaded through the per-instrument, combined, and digest-text
rollups so the caveat cannot be dropped silently at any later aggregation step — it appears as an
explicit `(N unpriced)` suffix wherever a net total is rendered.

This is the same design property named in [VERIFICATION.md](../../../VERIFICATION.md) and
[METHOD.md](../../../METHOD.md) for the whole repo — *"fail open to null, never fabricate"* —
applied to a reporting rollup rather than an engine decision: a row that cannot be honestly priced
is named as missing from the total, not folded into it.
