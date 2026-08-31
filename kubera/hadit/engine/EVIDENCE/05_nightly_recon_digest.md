<!-- What: real source excerpt from the nightly reconciler (the research host, rust_recon_daily/build_verdict.py)
     showing the explicit unpriced-row classification, plus the top-level shape of a real verdict.json
     (keys only — all dollar/qty values are excluded, not just redacted, since this file's whole
     purpose is to avoid ever presenting P&L). Redacted: all monetary values, all row-level detail. -->

## The rule, in the reconciler's own comment (`build_verdict.py`)

```python
# A row is "matched but unpriced" when it actually traded live (cls matched/qty_clamp_known)
unpriced_rows = [r for r in rows if r.get("cls") in ("matched", "qty_clamp_known")
                 and r.get("pnl_live") is None]
if unpriced_rows:
    notes.append(f"{len(unpriced_rows)} matched live exit(s) could not be priced (pnl_live=None) — "
                  ...)
```

This runs for the gold book, the MES book, and the combined book independently — each carries its
own `n_unpriced` count into the digest text:

```python
unpriced_bit = f" ({mt['n_unpriced']} unpriced)" if mt.get("n_unpriced") else ""
lines.append(f"Day: live ${'<redacted>'}{unpriced_bit} (...) ...")
```

The digest line format always states the unpriced count *inline with the total*, not as a footnote
— a reader cannot see "Day: live $X" without also seeing "(N unpriced)" in the same clause when N is
nonzero. This is the "digests state unpriced rows explicitly" claim, verified against the actual
formatting code rather than a description of it.

## Real verdict.json shape (the research host, `rust_recon_daily/work/verdict.json`, top-level keys only)

```json
{
  "gold": { "...": "per-book verdict object" },
  "mes": { "...": "per-book verdict object" },
  "combined": { "...": "merged verdict object, n_matched / n_unpriced / net_live / notes[]" }
}
```

**Schedule:** `rust-recon-daily.timer` (the research host user systemd), fires nightly at 22:12 UTC — confirmed
independently against the running systemd unit, not just the script's existence.

**Venue-truth-wins:** the reconciler prices canon (what should have traded) against live (what did)
using the broker's own deal/trade records as ground truth; where a canon trade only has a low-
confidence synthetic price (before the venue's tick database starts), the digest states that
explicitly too (`"canon trade(s) priced on the ... LOW-CONFIDENCE"` note path in the same file) —
the same "state it, don't hide it in a total" discipline applied twice in one script.
