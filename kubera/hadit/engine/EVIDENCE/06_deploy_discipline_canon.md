<!-- What: bare-canon branch cadence (engine-canon.git, the execution host), the runtime-tree DO-NOT-BUILD rule,
     and one redacted PLANNED_RESTART rollback marker. Redacted: nothing removed except noting hashes
     are kept per the brief ("strip hashes ok to keep, strip any account/env values" — no account/env
     values were present in the source marker). -->

## Deploy-branch cadence (`engine-canon.git`, bare repo, the execution host — branch names are feature slugs, no
strategy logic in the names themselves)

```
k2-package-20260810
candlegs-livebase-20260809
n9log-livebase-20260809
wattr-livebase-20260809
ghostfix-gapAB-livebase-20260809
c08-perseq-lock-livebase-20260809
wedshort-gate-livebase-20260808
codex/rfd-g3d-dedup-livebase-20260806
d1-missedfill-20260804
witness-survivor-attribution-20260803
combined-deploy-20260803
netting-exit-fix-20260803
final-batch-integration-20260803
tp-limit-solo-fix-21
ghost-fold-20260803
batch-integration-20260803
adopt-order-20260803
```
17 of the tail-most branches shown; the visible window alone spans 2026-08-03 -> 2026-08-10 — a
dense, near-daily deploy-branch cadence, each branch a single scoped change.

## Build/runtime separation (`hadit-core/DO-NOT-BUILD.md`, the execution host)

> This directory is **runtime-only**... Building here has historically produced wrong,
> feature-missing binaries... **Build tree:** `ws2_live_ownqty_build` on the build host. All engine
> commits happen there, or are pushed there and mirrored into `engine-canon.git`, before any build.
> **Deploy:** build on the build host -> copy the built binary to the execution host -> restart the service. the execution host
> never runs `cargo build`.

## Rollback marker (`PLANNED_RESTART_a6859b8_20260826T025440Z.md`, the execution host, verbatim minus nothing sensitive)

```
Change: engine: prox-park CANCEL/force-flat trade-end gap (...) + cross-account scoping
        (commit a6859b8, branch k2-package-20260810)

binary 21fb88f2d39be74c5c4b8df3f08dc81be99bf37baefb4e492b2396c5000992d6 <-> commit a6859b8
prev   178525f0b3d4025e39b18e5b02845730e1f147b5085c9cb6d3ff2140a9ba354e (commit b7ec868)
       backup=.../ws2_live_engine.pre_a6859b8_20260826T025440Z

Audit status: fresh-reviewer audit PASS (cargo test -p engine --release: 549/549). strings-diff
vs running binary: all known feature markers match old vs new except drop_prox_parks
(old=0, new=1, expected new feature). check smoke test clean.

No persisted state files edited (this fix touches only cancel/force-flat routing).

Rollback:
  systemctl --user stop ws2-engine-demo.service
  cp .../ws2_live_engine.pre_a6859b8_20260826T025440Z .../ws2_live_engine
  systemctl --user start ws2-engine-demo.service
```

Note the shape: the binary hash is recorded *before* the swap, the previous binary is preserved on
disk under a versioned filename, and the rollback command is written down as part of the same
document that authorizes the deploy — not reconstructed after the fact.

## Deploy rehearsal

Every one of these branches is exercised in the Time Travel Mirror — a byte-identical copy of the
live engine tree — before touching the live binary. See
`../../nuit/time-travel-mirror/` for the mirror's own evidence (372/373 files symlink-identical,
the one divergent file mechanically proven to differ by six `pub` tokens).
