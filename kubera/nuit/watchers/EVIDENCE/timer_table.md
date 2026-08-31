# EVIDENCE: 9 watcher timers, live today

What: `systemctl --user list-timers --all` on the research host, captured 2026-08-31.
Redacted: nothing sensitive in unit names; other timers on the same host (unrelated projects —
time-travel registry, a telegram poller, nightly recon/regime/parity jobs) are left out of this
excerpt since they aren't part of this fleet. No hostnames shown (systemd's own output doesn't
carry them).

## The 9 watcher timers (~60s cadence) + the watchdog-of-watchers

```
NEXT                            LEFT LAST                              PASSED UNIT                            ACTIVATES
Mon 2026-08-31 01:38:30 UTC       7s Mon 2026-08-31 01:37:33 UTC      49s ago nuit-reject-watcher.timer       nuit-reject-watcher.service
Mon 2026-08-31 01:38:35 UTC      12s Mon 2026-08-31 01:37:39 UTC      43s ago nuit-naked-orphan-watcher.timer nuit-naked-orphan-watcher.service
Mon 2026-08-31 01:38:40 UTC      17s Mon 2026-08-31 01:37:40 UTC      42s ago nuit-identity-watcher.timer     nuit-identity-watcher.service
Mon 2026-08-31 01:38:50 UTC      27s Mon 2026-08-31 01:37:53 UTC      29s ago consolidation-watcher.timer     consolidation-watcher.service
Mon 2026-08-31 01:38:55 UTC      32s Mon 2026-08-31 01:37:59 UTC      23s ago nuit-watchdog.timer             nuit-watchdog.service
Mon 2026-08-31 01:39:00 UTC      37s Mon 2026-08-31 01:38:03 UTC      19s ago nuit-health-supervisor.timer    nuit-health-supervisor.service
Mon 2026-08-31 01:39:05 UTC      42s Mon 2026-08-31 01:38:05 UTC      17s ago net-out-watcher.timer           net-out-watcher.service
Mon 2026-08-31 01:39:10 UTC      47s Mon 2026-08-31 01:38:10 UTC      12s ago nuit-phantom-watcher.timer      nuit-phantom-watcher.service
Mon 2026-08-31 01:39:20 UTC      57s Mon 2026-08-31 01:38:20 UTC       2s ago engine-liveness-watcher.timer   engine-liveness-watcher.service
Mon 2026-08-31 01:39:20 UTC      57s Mon 2026-08-31 01:38:20 UTC       2s ago nuit-oversize-watcher.timer     nuit-oversize-watcher.service
```

Count: 9 failure-class watcher timers (reject, naked-orphan, identity, consolidation, net-out,
phantom, engine-liveness, oversize, and the watchdog-of-watchers rounding out the family) plus
`nuit-health-supervisor.timer`, the tenth same-cadence unit that watches host/gateway health
rather than one specific failure class (see ARCHITECTURE.md). Every `LAST ... PASSED` column
reads under a minute at capture time — the fleet is firing, not stalled.
