<!-- What: (1) what the verification harness fleet checks and why it's structured as many small
     crates rather than one; the real Rust scale is included as supporting detail, not the
     headline. (2) the real automation-unit count on each host. Redacted: none — structural counts
     and behavior, not strategy content. -->

## One purpose-built check per live scenario, not one big test suite

Beyond the core engine (`01_engine_status_and_loc.md`), a separate fleet of **11 hash-distinct
verification harness crates** exists — each its own real Cargo project, each independently built
to check exactly one reconciliation or canon-consistency question against live venue data:
per-account money-movement reconciliation, per-symbol quantity-map verification, duplicate-guard
checks, queue-position canon checks. The design choice worth naming is *why eleven crates and not
one*: each harness fails independently and says precisely which live scenario it caught, rather
than one shared test binary where a failure requires triage to find the actual scenario at fault.
One of the eleven is the [Time Travel Mirror](../../nuit/time-travel-mirror/) (`bugatti_wave3_wt`),
already documented as its own project; the other ten do the same category of work and had not
previously been surfaced in this repo.

*A note on withheld names:* individual crate names encode which live account/scenario each
harness checks — naming them precisely would describe live account topology, which this repo's
redaction policy keeps out. What each harness checks and why the fleet is shaped this way is the
evidence; the per-crate identity is not needed to prove it.

For reference, not as the point: this fleet is 124,206 lines, and the same variance discipline
that separates the deployed runtime tree from the canonical build-source tree (`06_deploy_discipline_canon.md`)
means the core engine's own crate-level count differs by a few thousand lines depending which tree
you measure — quoting one number as *the* number would imply a precision the multi-tree deploy
design doesn't have. Total real, non-duplicated Rust across both hosts lands around 215-220k
lines if a single figure is wanted; ~9 further directories are full snapshots of the core engine
at different points in time and are deliberately excluded from that count, not summed into it.

## Automation units — also undercounted

The engine project previously named only the equity watchdog and the L1 recorder as independent
automation. A direct count of every systemd unit + timer + cron line on the execution host finds
**47 distinct automation units**: 29 services + 8 non-overlapping timers + 2 cron jobs (roll-day
automation) + the watchdog and recorder already documented, with the balance being ~30
purpose-built cockpit data generators (weather/decay/positions/radial/banked-$/EOD-report/
law-state/witness-rollup/margin-watcher, each its own small always-on or timer-fired process) —
not one monolithic "cockpit," a fleet of small, independently-restartable services. See
[the watchers project](../../nuit/watchers/) for the equivalent count on the research host (20
units: 16 timers + 4 cron lines) — the two hosts' automation is deliberately not shared, per the
hygiene-as-architecture split documented in `STORY.md`.
