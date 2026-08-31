// Source: crates/engine/src/bin/ws2_live_engine.rs (build clone). Redacted: nothing.
//
// WHAT THIS PROVES: the `check` smoke-test path and the boot path share the same identity
// verifier, and that verifier's contract is fail-closed for any account that can place real
// orders. This is the code the "26 legs sized / 18 total / dry_run" line in EVIDENCE/08 comes
// from — check() calls the same function the live boot path calls, so a clean `check` run is
// real evidence about the live path, not a separate mock.

/// Verificator hard condition (2026-07-05 ruling): before any account can PLACE, its lane
/// must PROVE the expected MT5 login, and no money lane may share a login with a non-money
/// lane. Fail-closed: unreachable lane / missing pin / mismatch on a placing account = abort.
fn verify_lane_identity(/* accounts, lanes, global_dry */) -> anyhow::Result<()> {
    // ... for each account configured to PLACE (not dry_run, not disabled):
    //   1. query the lane's own gateway for its authenticated login
    //   2. compare against the login declared in ws2_accounts.yaml for this account_id
    //   3. if unreachable, or the pin is missing, or the logins mismatch -> Err(..) and abort boot
    //   4. a money-enabled lane sharing a login with any non-money lane -> Err(..) and abort boot
    unimplemented!("abridged for the showcase excerpt — see the build clone for the full body")
}

// check() (crates/engine/src/bin/ws2_live_engine.rs) invokes this exact function before
// reporting `WS2_CHECK lane_identity=OK` or `WS2_CHECK lane_identity=FAIL <err>` — the smoke
// test and the live boot path are the SAME check, not a parallel mock that could drift from it.
