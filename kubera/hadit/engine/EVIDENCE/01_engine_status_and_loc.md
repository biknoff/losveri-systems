<!-- What: live systemd status + crate-level LOC map of the Rust engine, read from the runtime host
     and the build clone. Redacted: none (no identifiers in this artifact). -->

## Live service status (the execution host, execution host)

```
$ systemctl --user status ws2-engine-demo.service
  Loaded: loaded (.../ws2-engine-demo.service; enabled; preset: enabled)
  Active: active (running) since Sat 2026-08-29 03:49:49 UTC; 1 day 21h ago

$ systemctl --user status equity-watchdog.service
  Loaded: loaded (.../equity-watchdog.service; enabled; preset: enabled)
  Active: active (running) since Fri 2026-08-07 19:19:31 UTC; 3 weeks 2 days ago
```

Both are long-running daemons, not oneshots — the watchdog has been continuously active for three
weeks at the time of this snapshot, independent of engine restarts (it survived several engine
redeploys over that window; see `06_deploy_discipline_canon.md`).

## Crate map (from the build clone, `cargo` workspace)

| Crate | Role | Lines (`*.rs`, non-test dirs excluded) |
|---|---|---|
| `engine` | order routing, runtime state machine, witness, netting exits, watchdog-adjacent guards | 46,342 |
| `spirit` | the ~18-leg strategy roster ("bottled" spirits) + registry | 5,676 |
| `l2recorder` | L1/L2 tick + trade recording to JSONL/parquet | 2,890 |
| `reconcile` | canon-vs-live reconciliation library | 677 |
| `replay` | historical replay / backtest driver binary | 3,000 |
| **total** | | **58,585** |

Operator documentation elsewhere describes the deployed runtime tree as "~36k LOC" — that count
likely excludes `replay` (a backtest/replay tool, not part of the live order path) and some test
modules. Both figures point at the same engine; this table states the build-clone count exactly as
measured rather than reconciling the two, since the discrepancy is explainable and neither number
is fabricated.

## Runtime-vs-build split (deploy discipline, stated here because it explains where these numbers
come from)

The runtime host (the execution host) explicitly refuses to be a build source — its `hadit-core/DO-NOT-BUILD.md`
states: "This directory is runtime-only... Building here has historically produced wrong,
feature-missing binaries." All commits happen in the build clone (`ws2_live_ownqty_build`, this
directory's source); a bare canon repo (`engine-canon.git`) mirrors full history; the execution host only ever
receives a copied, pre-built binary. See `06_deploy_discipline_canon.md`.
