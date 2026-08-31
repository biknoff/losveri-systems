# Evidence: the NT8 production user-data tree

**What this is:** directory-level counts and mtime ranges from a genuine NinjaTrader 8
user-data tree (`References from Chicago/`), preserved on the current build host, plus
confirmation that an independent mirror of the analyzer-log export exists on a second
machine. This is the artifact-level proof that the system was a real, exercised NT8
production install — not a template or a demo.

**Redactions applied:** no file names are given for `templates_Strategy/` or
`strategyanalyzerlogs/` — those file names encode strategy/system identity. Only counts
and date ranges are reported. No account IDs, hostnames, symbols, or P&L appear anywhere
in the source tree inspected.

## Directory counts (NT8 user-data tree, host copy)

| Directory | File count | Mtime range |
|---|---|---|
| `AtmStrategy/` | 42 | 2026‑05‑17 → 2026‑05‑29 |
| `Custom_Strategies/` | 21 | 2026‑05‑28 20:47 → 2026‑05‑29 00:50 |
| `Custom_Indicators/` | 143 | 2026‑05‑28 20:47 → 20:48 |
| `Custom_AddOns/` | 8 | 2026‑05‑28 20:48 → 2026‑05‑29 18:26 |
| `templates_Strategy/` | 54 | 2026‑05‑28 20:48:32 → :51 |
| `templates_Indicator/` | 1 | 2026‑05‑28 20:48:56 |
| `strategyanalyzerlogs/` | 563 | 2026‑05‑15 09:34 → 2026‑05‑16 16:07 |

That is a strategy/indicator/AddOn/template inventory in the hundreds of files, with ATM
(Advanced Trade Management) order templates present — the shape of an NT8 install that
was actually configured and run, not a fresh checkout.

## Independent mirror (second machine)

A second copy of `References from Chicago/strategyanalyzerlogs/` exists on a separate
machine (a Mac used as the team's file mirror). File count (563) and mtime range
(2026‑05‑15 09:34 → 2026‑05‑16 16:07) are identical to the host copy — i.e., this is a
verified mirror of the same analyzer-export batch, not a second unrelated dataset.

## Live tick tapes

`nt8_tapes/` (daily CSV recordings, separate backup location): 27 files. First (sorted):
`2026-06-05.csv`; last: `backfill_2026-06-04.csv` — early-to-mid June 2026. The presence
of a `backfill_*` file alongside daily files is itself evidence of an operational
recording pipeline (something that needed to catch up a gap), not a one-off export.

**Source commands (read-only, run via the build host and an ssh mirror host):** directory
listings and `find`/`stat`-style mtime queries against the paths above. No file contents
from `Custom_Strategies/`, `Custom_Indicators/`, `AtmStrategy/`, `templates_Strategy/`, or
`strategyanalyzerlogs/` were read or reproduced.
