# EVIDENCE: defense-in-depth by failure class

What: one-line synthesis of each watcher's own module docstring, read directly from source on
the research host. Redacted: internal strategy/leg names replaced with generic terms
("a leg", "a symbol"); no account, broker, or P&L detail was present in any docstring to begin
with.

| Watcher | Failure class | Can | Cannot |
|---|---|---|---|
| `engine_liveness_watcher.py` | Engine process/heartbeat going stale or silent while the market is open, independent of the engine's own log | page CRITICAL, then re-page on a cooldown | restart the engine, touch an order |
| `nuit_oversize_watcher.py` | A leg carrying more live contracts than its governed size (counter-leak class) | page by severity (filled excess = CRITICAL, resting-only = log) | resize or cancel anything |
| `nuit_reject_watcher.py` | Venue-level order rejects and abandoned-session events, from the witness log | batch + page, deduped | retry the order |
| `nuit_naked_orphan_watcher.py` | Orphan resting orders whose registry/park record was independently lost, despite carrying a valid leg tag | page CRITICAL | repair the record itself (human or the equity watchdog only) |
| `nuit_identity_watcher.py` | Demo-vs-live account mismatch across 4 independent identity sources | page CRITICAL immediately, incl. on an unreadable/unprovable source | change which account is live |
| `consolidation_watcher.py` | Netting consolidation leaving a leg's stop orphaned; naked positions; the separate equity-watchdog's heartbeat/latch; orphan venue positions | page CRITICAL, report a watchdog latch reason | clear a latch (human only) |
| `net_out_watcher.py` | Net-out/flip events on netting symbols, tailed from a durable engine-appended stream | page within ~1 minute of a new event | author or reverse the net-out |
| `nuit_phantom_watcher.py` | Unattributed orders/positions placed by nothing the engine's registry recognizes | page CRITICAL, RECOVERED on clear | cancel the phantom order |
| `nuit_watchdog.py` | Any other watcher program going stale (watchdog-of-watchers) + pushes the cockpit Monitoring feed | page, push status | restart a dead watcher |
| `nuit_health_supervisor.py` | Host/gateway-level health: heartbeat age, unit restarts, per-terminal account identity, disk/mem/load | probe, judge, push verdict, alert | modify a unit or account setting |
| `managed_stop_watch.py` (cron) | A managed trailing/breakeven stop silently reverting instead of only ratcheting tighter | page on a stop regression | fix the stop itself |
| `zeroed_leg_watch.py` (cron) | A zeroed (size-0) leg still placing an order via an audited unpark bypass | page on the bypass or its precondition | block the order |
| `trade_watch.py` (cron) | Event-driven trade-lifecycle tailing | wake the supervising process, log | send anything to the operators itself for routine events |
| `backstop_run.sh` (cron, 3h) | Binary-sha drift from baseline; snapshot pipeline crash/hang | page only on those two conditions | anything else |

The shape is deliberate: nine narrow, single-purpose timers plus a smaller, higher-consequence
cron set, rather than one general monitor — see `DECISIONS.md`.
