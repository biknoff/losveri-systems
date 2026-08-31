# Architecture

## Three layers

**1. The timer fleet (9 systemd `--user` timers, ~60s cadence).** Each unit runs one Python
script once per cycle, reads a snapshot or tails an event stream from the execution host over a
read-only channel, computes a verdict, and either stays silent or telegrams. State is
transition-driven, not a heartbeat: a watcher pages on a healthy→bad transition, re-pages on a
cooldown while the condition persists, and sends one RECOVERED note when it clears. A tenth
timer (`nuit-health-supervisor`) runs at the same cadence but is not itself one of the 9 — it
probes host-level and gateway-level health (heartbeat age, systemd unit restarts, per-terminal
account identity, disk/mem/load) and pushes a verdict *into* the execution host's own cockpit,
deliberately computed outside it so a self-hang on that host shows up as a missing push, never a
self-reported green.

**2. The cron durable layer.** Three per-minute cron jobs plus one 3-hourly job, chosen
specifically because they run under the OS scheduler rather than inside any interactive or
agent session — they survive a session dying, which a systemd `--user` timer tied to a login
session historically has not. This layer targets narrower, higher-consequence failure classes
that the general timer fleet does not cover: a managed stop silently reverting instead of only
ratcheting tighter, a zeroed leg placing an order through an unpark bypass, and a durable
event-driven trade tail. The crontab's own header states the operating philosophy directly:
"Silent when flat" — it only speaks when there is something to say.

**3. The 3-hour backstop.** A shell script invoked by cron that runs a full state snapshot
headlessly, archives the output, and telegrams the operators *only* on two conditions: the live
binary's sha has drifted from the last known/authorized baseline, or the snapshot script itself
crashed or hung. Every other run is silent by design — the archive itself is the record; the
telegram is reserved for the two things a human actually needs to see between backstop cycles.

## Failure-class coverage (defense-in-depth)

Each of the 9 timers owns exactly one failure class — a deliberate choice over one monolithic
monitor (see [DECISIONS.md](DECISIONS.md)):

| Watcher | Failure class it catches |
|---|---|
| `engine_liveness_watcher` | The engine process or its status heartbeat going stale/silent while the market is open — engine-independent, so a hung engine can't hide behind its own quiet log. |
| `nuit_oversize_watcher` | A leg carrying more live contracts at the venue than its governed per-trade size — the counter-leak class, with severity split by whether the excess is filled or just resting. |
| `nuit_reject_watcher` | Venue-level order rejects and abandoned-session events surfaced from the witness log — broker truth, not engine self-report. |
| `nuit_naked_orphan_watcher` | A specific, audited gap left after other watchers: resting orders that carry a live leg's own comment tag (so the generic phantom check exempts them) but whose registry/park record was independently lost. |
| `nuit_identity_watcher` | Demo-vs-live account mismatch across four independent identity sources (gateway truth, config expectation, cockpit display, engine log) — any disagreement is paged as CRITICAL, and an unreadable source pages too (unprovable is not treated as green). |
| `consolidation_watcher` | Netting consolidation leaving a leg's intended stop orphaned, naked positions (SL absent), the separate equity-watchdog's own heartbeat/latch state, and an orphan-position guard for venue positions belonging to no engine leg. |
| `net_out_watcher` | Net-out/flip events on netting symbols, tailed from a durable engine-appended event stream — quiet when the feature flag that produces the stream is off. |
| `nuit_phantom_watcher` | Unattributed orders/positions at the venue that were placed by nothing the engine's own registry recognizes — the "shadow executor" class. |
| `nuit_watchdog` | The watchers watching the watchers: every program's own state-file freshness, so a dead health supervisor doesn't die silently. Also the sole pusher of the cockpit's Monitoring tab (research host is pull-only otherwise). |

Cron durable layer, narrower and higher-consequence:

| Detector | Failure class |
|---|---|
| `managed_stop_watch.py` | A managed trailing/breakeven stop silently reverting or widening instead of only ever ratcheting tighter — log-only on the execution host, so this grep is the only observer of it. |
| `zeroed_leg_watch.py` | A leg zeroed to size 0 still placing an order through an audited unpark-path bypass — the "zeroing disables the leg" guarantee, independently enforced. |
| `trade_watch.py` | Event-driven trade-lifecycle tailing that wakes the supervising process on real activity rather than polling on a fixed interval. |
| `backstop_run.sh` (3h) | Binary-sha drift from the authorized baseline, or a crash/hang in the snapshot pipeline itself. |

## The boundary: alert and halt, never author

Structural, not just stated. Every read path in the fleet goes through one of: a read-only exec
channel to the execution host (grep the family's source — the shared helper issues shell
commands over SSH and every caller passes read/query commands; no watcher constructs an
order-placement, modification, or cancellation call), witness-log tailing (append-only, engine
writes it, watchers only read it), or local state-file reads. The only actions available back
out are: append to a local alert log, send a Telegram message, and — for the separate
equity-watchdog process that `consolidation_watcher` meta-watches but does not replace — flatten
and latch, with the latch cleared only by a human. No watcher script in this fleet imports or
calls anything resembling an order-send/order-cancel API.

## Failure modes of the watchers themselves

- **A single watcher dies or stalls.** `nuit_watchdog` reads every other program's state-file
  `last_cycle_ts` each cycle and pages if any program goes stale beyond a threshold generous
  enough to absorb a couple of missed cycles but tight enough to catch a real hang.
- **The whole systemd `--user` manager dies.** The cockpit's Monitoring tab is fed by
  `nuit_watchdog`'s push; if the pusher itself is gone, the cockpit ages the feed server-side and
  shows it as stale rather than continuing to display a frozen "last known good" as if it were
  current.
- **The research host loses its channel to the execution host.** `nuit_health_supervisor`
  telegrams after two consecutive failed probes — a research-host-down or execution-host-down
  condition still reaches the operators from the side that's still up.
- **A session-scoped watcher dies with the session.** This is exactly why the durable cron layer
  exists as a second, independent scheduling mechanism outside systemd `--user` — see
  [DECISIONS.md](DECISIONS.md).
- **The backstop pipeline itself hangs or crashes.** `backstop_run.sh` treats its own timeout
  and non-zero exit as first-class alertable conditions, not silent failures.

## Adjacent, not part of the fleet

`ramp_watcher.py` runs nightly (not on the ~60s cadence) and is explicitly a **recon consumer**,
not a watcher: it reads verdicts already produced by the nightly reconciliation pipeline (owned
by the [Time Travel Mirror](../time-travel-mirror/)) and turns them into a per-leg promote
*recommendation* for a human to act on in the cockpit. Zero account writes, by its own stated
doctrine.
