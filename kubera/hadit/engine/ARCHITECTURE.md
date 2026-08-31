# ARCHITECTURE

Part of HADIT — see [STORY.md](../../../STORY.md).

## Components

| Component | Host | What it is |
|---|---|---|
| `ws2-engine-demo.service` (crate `engine`) | the execution host (execution) | order routing, runtime state machine, netting/exit management, witness writer |
| `spirit` crate | build clone, linked into `engine` | the ~18-leg strategy roster ("bottled" spirits); no dependency on `engine` (structural isolation used in certification audits) |
| `reconcile` crate + `rust-recon-daily.timer` | the research host (research) | canon-vs-live nightly reconciliation |
| `l2recorder` | the execution host | independent L1/L2 tick + trade recording |
| `replay` | build clone | historical replay / backtest driver, not part of the live order path |
| `equity_watchdog.py` | the execution host, own systemd unit | independent account protector — flatten/halt/latch |
| `hadit-mt5-gateway` (`mt5_zmq_gateway.py` under Wine) | the execution host, containerized | the only venue adapter; golden-image MT5 terminal, ZMQ interface |
| `engine-canon.git` | the execution host, bare repo | canonical build history, mirrored from the build clone |
| Time Travel Mirror | the research host | byte-linked deploy rehearsal environment — see `../../nuit/time-travel-mirror/` |

## Data flow

```
strategy decision (spirit crate)
        |
        v
engine runtime  --place/cancel-->  mt5_zmq_gateway (golden-image MT5 terminal)  --> venue (broker)
        |                                          |
        | witness event (every transition)         | history_deals (venue truth)
        v                                          v
witness/{date}/{leg}.jsonl  <---------- exit enrichment reads venue deals, never engine memory
        |
        v
rust-recon-daily (nightly, 22:12 UTC) --venue-truth-wins--> verdict digest (unpriced rows stated)

equity_watchdog.py  --independent poll of the SAME gateway-->  flatten/halt/latch (human clears)

engine-canon.git (bare) --> Time Travel Mirror (rehearse) --> PLANNED_RESTART marker --> live swap
```

## Boundaries

- **Build vs runtime.** All commits happen in the build clone (the research host); the execution host's runtime
  tree explicitly refuses to be a build source (`DO-NOT-BUILD.md`) — it only receives a pre-built
  binary copied in at deploy time.
- **Engine vs watchdog.** The watchdog is a separate process and systemd unit with "zero shared
  code with the engine," reading the same venue truth independently. A bug in the engine's judgment
  cannot also disable its own supervisor.
- **Engine vs gateway.** The order/tick interface to the broker is a separate ZMQ process
  (`mt5_zmq_gateway.py`) running against a golden-image MT5 terminal; the engine never drives MT5's
  UI directly.
- **spirit vs engine.** The strategy-decision crate has no dependency on the order-routing crate —
  used directly in certification audits to prove a bottle-only change cannot have caused an
  engine-side regression.

## Failure modes and how they're handled

| Failure | Handling |
|---|---|
| Witness write fails (disk full, permissions) | Loud counted failure, trading continues (observability degrades visibly, never silently) |
| Venue deal history ambiguous (merged/netted position) | Exit price/profit fields left `null` rather than estimated |
| Account breaches day/week/margin risk limits | Watchdog flattens + halts + latches; only a human clears the latch |
| Engine crashes or is killed | Relaunch script checks the watchdog latch before restarting — a latched account will not silently resume trading |
| Deploy binary regresses | Pre-recorded rollback marker (previous binary hash + backup path + rollback commands) written before the swap |
| A certify run finds a mismatch | Filed and root-caused (see the 2026-08-10 stale-oracle example), not silently rerun until green |
| Config staged but never armed | `check` reports `global_dry` and `live_enable` state explicitly so a reviewer sees whether a run is live before it runs |

## Human gates

- **Arming live trading** is a human's hand on an env var (`HADIT_WS2_LIVE_ENABLE`) — never set by
  a unit file or a script.
- **Clearing a watchdog latch** is a human deleting a file and restarting the engine — no
  auto-clear, no timed cooldown.
- **Deploys** happen in a flat window, rehearsed first in the Time Travel Mirror, with the rollback
  marker written and reviewed before the binary swap — not after something goes wrong.
- **Certification reds** are triaged by a human/auditor before being accepted as pre-existing or
  filed as new defects — a red does not get silently reclassified as noise.
