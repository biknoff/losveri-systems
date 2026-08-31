<!-- What: (a) redacted excerpt of the actual 2026-07-08 certification sweep record
     (CERT_SUITE_GREEN_SWEEP_20260708_HANDOFF.md, execution host) — the "26/28 green, 2 honest reds"
     document; (b) real certification-harness output showing the methodology; (c) a second real
     "honest red" from a 2026-08-10 independent audit. Redacted in (a): strategy identifiers
     (→ opaque tokens), the locked risk-cap value and stop-distance figures (strategy parameters),
     source-box names. Structural counts, dates, and the divergence characterizations are verbatim. -->

## The certification sweep record (2026-07-08, redacted excerpt)

> **Mandate:** get the entire `cargo test -p spirit --release --no-fail-fast -- --ignored` suite
> green. Baseline: 20/28 green, 8 failing on missing oracle-trace files, one leg's risk cap
> disabled, one leg uncertified.
>
> **Result: 26/28 green. 2 genuine divergences (STOP+report per mandate, not forced).** The
> uncertified leg precisely reported (no harness exists).

- **Leg-A** (risk-cap re-certification): oracle trace regenerated *with* the newly-enabled ex-ante
  risk gate at the exact point the Rust port has it — the first attempt at the reference
  implementation got a subtle lifecycle detail wrong and was fixed *before* certifying. Result:
  **PASS, 112,439/112,439 byte-parity**; all 10 embedded white-box unit tests still pass. The
  running binary was backed up from `/proc/<pid>/exe` and hash-verified byte-identical to the live
  process before the rebuilt binary was deployed.
- **Honest red #1 (Leg-B):** a pre-existing, read-only, dated oracle ledger already on the host
  disagrees with the Rust port's emitted entry price on 5 real trading days inside the overlap
  window. Cross-validated as a genuine divergence between two references — stopped and reported,
  not forced green.
- **Honest red #2 (Leg-C):** 718/35,999 bars mismatch on one field (`armed`) on exactly the two
  days the window's derivation makes reachable — and the Rust port's own docstring *already
  flagged this exact area* as an uncertain gate, "Transpiled 1:1 — NOT 'fixed'". The divergence
  was characterized (Rust arms; oracle stays un-armed) and left standing as documented
  uncertainty.
- **The uncertified leg:** "no cert harness exists (precisely, not fabricated)" — its 8 embedded
  white-box unit tests all pass, and the record names the real behavioral cert it still needs
  (against a 250-fill realized-outcome ledger) rather than claiming trace-level certification it
  doesn't have.

## The certification method (real harness output, `_certify.log`, build clone)

Per-spirit decision-layer certification replays a recorded oracle trace and diffs the engine's
computed decision state bar-for-bar:

```
════════ spirit_mgc_c08 DECISION-LAYER CERTIFICATION ════════
trace span (ET date): 2026-05-31 -> 2026-06-19
bars compared       : 11614 / 11614
decision parity      : PASS (byte-parity)  (mismatched bars: 0)
emit bars (bracket)  : 56
signals matched      : 57/57
═══════════════════════════════════════════════════════════
CLOSED: 11614/11614 bars decision-state byte-parity, 57/57 signals matched.
```

A behavioral (scenario-based) certification layer runs alongside it:

```
CLOSED: 20 scenarios / 55 steps byte-exact; 20 arm geometries, 4 give-up paths, 2 concurrency skips.
```

## A real "honest red" caught by this harness (independent audit, 2026-08-10, `K2_PACKAGE_BUILD_20260810.md`)

The same certify family failed on a different bottle (`certify_mgc_rfd_g3`) during a build package's
own pre-deploy audit. The independent reviewer did not wave it through — they reproduced it, then
traced the root cause: the oracle trace file predated a legitimate signal-dedupe change to the
bottle, so the trace itself was stale, not the engine:

```
decision parity: PASS (byte-parity), mismatched bars: 0   <- decision layer is intact
                                                             (only emit/signal-count check fails)
Three independent lines of evidence this branch cannot be the cause:
1. Structural isolation: crates/spirit has no dependency on engine.
2. Stale oracle confirmed: oracle mtime predates the bottle's last legitimate change.
3. git merge-base --is-ancestor <bottle-change-sha> <baseline-sha> -> true (the trace is older).
```

Verdict recorded: `CONFIRMED PRE-EXISTING, root cause identified` — filed as a separate ticket
(regenerate the oracle), not silently patched over. The same audit's summary table lists one
BLOCKING finding elsewhere in the package (a cockpit threshold basis, unrelated to parity) and
several CONFIRMED-OK / CONCERN items — a certification with only-green rows is not what this
process produces; this is what "26/28 green with 2 honest reds" looks like in practice on this
codebase, even though the specific July record could not be located this pass.
