# Decisions

**Watchers cannot author — rejected: a self-healing engine.** A watcher that could place,
modify, or cancel an order to "fix" what it finds would need its own correctness guarantees at
the same bar as the engine it watches — and a bug in the watcher would now be a bug with order
access. Every watcher in this fleet is read-only against the execution host by construction (one
shared channel, no write verb ever passed through it); the only interventions available are a
Telegram page and, for the one process authorized to act, the separate equity watchdog's
flatten-and-latch — with the latch cleared only by a human.

**A durable cron layer that survives session death — rejected: watchers living inside an
interactive/agent session only.** The systemd `--user` timer fleet is tied to a login-scoped
manager; a session ending has historically been able to take watchers down with it. The three
per-minute cron detectors plus the 3h backstop run under the OS scheduler specifically so the
highest-consequence checks (a stop silently reverting, a zeroed leg placing an order anyway,
binary-sha drift) do not depend on any session staying alive.

**Silent when flat — rejected: a heartbeat/status ping on every cycle.** The crontab's own header
states it directly: "Silent when flat." A watcher that pings on every healthy cycle trains the
operators to stop reading pings — alarm fatigue is a designed-against failure mode here, not an
oversight. Every watcher in the fleet is transition-driven (fires once on bad, re-pages on a
bounded cooldown while it persists, fires once on RECOVERED) rather than periodic.

**Per-failure-class watchers — rejected: one monolithic monitor.** Nine narrow scripts, each
reading a specific signal and understanding one failure shape (a stale heartbeat, an oversized
leg, a phantom order, an identity mismatch, a lost orphan record...) rather than one general
health check trying to reason about all of them at once. The tradeoff bought is legibility per
alert (a page names its exact failure class) at the cost of more processes to keep alive — which
is why `nuit_watchdog` exists as the tenth-ish process: a small, dedicated watcher of the
watchers, rather than folding that responsibility into every individual script.

**Four independent identity sources, not one — rejected: trusting the cockpit's own display.**
`nuit_identity_watcher` cross-checks gateway truth, config expectation, cockpit display, and the
engine's own log line against each other, and treats an unreadable source as unprovable
(paged), not green. A single source of truth for demo-vs-live account identity was rejected
specifically because the cockpit display is exactly the thing that could be lying.

**Reuse before build — rejected: a second independent naked-position detector.** When asked for
an orphan/naked-order watcher, the team audited what already existed first and found naked
positions were already covered by `consolidation_watcher`; `nuit_naked_orphan_watcher` was
scoped narrowly to the one real, audited gap (orphan resting orders with a valid leg tag but a
lost registry record) rather than re-implementing detection that already paged loudly elsewhere
— avoiding a second pipeline that would double every real page forever.

**Meta-watching the equity watchdog, not replacing it — rejected: folding flatten/halt authority
into the supervision fleet.** `consolidation_watcher` reports the separate equity-watchdog
process's heartbeat and latch state (and reports a latch reason, never restarts anything on its
own), keeping the one component with actual intervention authority as a single, separately
audited process rather than distributing halt authority across nine scripts.

**Dated `.pre_*` snapshots before every live change — rejected: relying on version control alone
as the rollback point.** Every watcher script keeps a timestamped, change-tagged copy of itself
immediately before a fix lands (46 such snapshots across the fleet as of this writing), giving a
one-command rollback target for a script that runs against real money every 60 seconds, without
waiting on a separate deploy/rollback tool to be reachable.
