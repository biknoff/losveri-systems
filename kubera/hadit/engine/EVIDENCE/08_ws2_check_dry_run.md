<!-- What: the `check` subcommand's real output-line format from ws2_live_engine.rs (build clone) — a
     smoke test that verifies config, lane identity, and connectivity WITHOUT ever placing an order,
     and the fail-closed identity rule it enforces before any account may go live. Redacted: none —
     this is format strings and a doc comment, no runtime values were captured. -->

## `check` subcommand — every line it can print (`crates/engine/src/bin/ws2_live_engine.rs`)

```
WS2_CHECK accounts_config=<path>
WS2_CHECK account=<id> enabled=<bool> money=<bool> dry_run=<bool> endpoint=<...> \
          sizing=<...> legs_sized=<n>/18 total_contracts=<n>
WS2_CHECK deck_built legs=<n>
WS2_CHECK deck_manifest_written=<path>
WS2_CHECK warmup_bars=<n> span_utc=[<t0>..<t1>] days=<n>
WS2_CHECK lane_identity=OK | WS2_CHECK lane_identity=FAIL <err>
WS2_CHECK lane=<account_id> ping_ok=<bool> reply=<...>
WS2_CHECK global_dry=<bool> live_enable=<env-value-or-none>
```

`check` builds the real deck, loads the real warmup spine, and pings every configured lane — it
exercises the full boot path except order placement — then reports `global_dry` and whether
`HADIT_WS2_LIVE_ENABLE` is set, so a reviewer can see in one command whether the invocation they are
about to run is dry by default.

## The fail-closed rule `check` verifies (`verify_lane_identity`, same file)

> Verificator hard condition (2026-07-05 ruling): before any account can PLACE, its lane must PROVE
> the expected MT5 login, and no money lane may share a login with a non-money lane. Fail-closed:
> unreachable lane / missing pin / mismatch on a placing account = abort.

**Dry-run-by-default in practice:** the `a6859b8` rollback marker (`06_deploy_discipline_canon.md`)
records `check smoke test clean (AMP_LIVE ping fail expected — account disabled)` as a *passing*
result — a disabled account failing its live ping is the expected, correct outcome, not swallowed as
a false green. Arming a lane to place real orders is a separate, explicit config/env state; `check`
never flips it.
