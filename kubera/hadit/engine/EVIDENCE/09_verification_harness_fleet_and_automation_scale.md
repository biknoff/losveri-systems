<!-- What: (1) the real total Rust surface across every distinct project on the execution+research
     hosts, verified by direct `find`+`wc -l` (excluding target/ and duplicate worktree snapshots);
     (2) the real automation-unit count on each host. Corrects an earlier undersell. Redacted:
     none — these are structural counts, not strategy content. -->

## The Rust surface is bigger than one crate map — and smaller than a naive sum

`01_engine_status_and_loc.md` gives the core engine's crate-level LOC from one build clone
(58,585). That number is real but incomplete in two ways worth stating precisely rather than
rounding away:

1. **The same 5 crates exist at slightly different sizes across several trees** — the deployed
   runtime tree, the canonical build-source tree, and this repo's own build clone all differ by a
   few thousand lines at any given moment, because they're deliberately not always in lockstep
   (see `06_deploy_discipline_canon.md`'s canon-vs-runtime separation). That variance is a feature
   of the deploy discipline, not measurement error — quoting one tree's number as *the* number
   would imply a precision the multi-tree design doesn't have.
2. **A second, genuinely separate body of Rust exists**, never previously counted: **11
   hash-distinct per-scenario/per-account verification harness crates**, each its own real Cargo
   project, each independently built to check one specific reconciliation or canon-consistency
   question against live venue data — not copies of the core engine, and not test fixtures.
   Verified directly (`find <root> -name '*.rs' | xargs wc -l`, `target/` excluded, each root
   confirmed to have a distinct git/file hash from its siblings):

   | Harness | Lines |
   |---|---|
   | (the largest 7, names withheld here as internal scenario labels — see note below) | — |
   | **Total, 11 distinct crates** | **124,206** |

   One of these eleven is the [Time Travel Mirror](../../nuit/time-travel-mirror/)
   (`bugatti_wave3_wt`) already documented as its own project. The other ten are siblings doing the
   same category of work — per-account money-movement reconciliation, per-symbol quantity-map
   verification, duplicate-guard checks, queue-position canon checks — that this repo had not
   previously surfaced at all.

   *A note on the withheld names:* the individual crate names encode which live account/scenario
   each harness checks (e.g. a specific multi-account money-sweep case, a specific symbol's
   quantity-map edge case) — naming them precisely would describe live account topology, which
   this repo's redaction policy keeps out. The count, the aggregate LOC, and the category of work
   are the evidence; the per-crate identity is not needed to prove the claim.

**Combined, verified, non-duplicated Rust total across both hosts: roughly 215,000–220,000
lines** — core engine + spirit roster + the verification harness fleet + the mirror's shim broker.
This excludes ~9 further directories that are simply full snapshots of the core engine at
different points in time (deliberately not summed — that would double-count, not add new code).

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
