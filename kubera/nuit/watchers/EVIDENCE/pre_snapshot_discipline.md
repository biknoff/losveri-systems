# EVIDENCE: iteration-under-fire, the `.pre_<fix>_<timestamp>` discipline

What: a file listing (`ls`/`find`) of the watcher fleet's source directory on the research
host, captured 2026-08-31, counting the `.pre_*` snapshot files each script leaves behind
before a change is applied. Redacted: nothing — filenames only, no content shown; the tags
inside the filenames are the operators' own short change-labels, already generic (e.g.
`nakedguard`, `emojisev`, `netxaware`) with no leg/strategy names in any of them.

## Count

**46 dated pre-change snapshots** across the fleet's source and its manifest, spanning
2026-07-12 through 2026-08-14 (roughly five weeks of the visible history):

| File | Snapshot count |
|---|---|
| `nuit_oversize_watcher.py` | 7 |
| `ramp_watcher.py` | 7 (+ 1 `.deployed_` marker) |
| `consolidation_watcher.py` | 6 |
| `nuit_watchdog.py` | 5 |
| `monitor_manifest.json` | 5 |
| `nuit_health_supervisor.py` | 4 |
| `nuit_common.py` | 3 |
| `nuit_phantom_watcher.py` | 3 |
| `engine_liveness_watcher.py`, `net_out_watcher.py`, `nuit_identity_watcher.py`, `nuit_reject_watcher.py`, `stress_test.py` | 1 each |

Every snapshot is taken **before** a change lands — the convention is
`<script>.pre_<change-tag>_<UTC-timestamp>Z`, e.g.
`nuit_oversize_watcher.py.pre_concurrency_20260727`. This is a live rollback point captured at
the moment of highest risk (right before a running watcher's logic changes), not a periodic
backup — the count is a direct proxy for how many times this fleet has been safely modified
while live. `nuit_oversize_watcher.py` alone shows 7 tagged revisions (size-threshold fixes, a
concurrency fix, a race fix, an alert-cleanup pass, a k2 deploy) — the watcher with the most
edit pressure is also the one carrying the most snapshots, which is the expected shape for a
discipline that is actually followed rather than performed once.
