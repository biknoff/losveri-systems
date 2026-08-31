<!-- WHAT: redacted summary of the formal acceptance record (2026-07-23/24 live window,
     8 runs). REDACTED: all P&L dollar figures, the account balance walk, specific strategy leg
     names (replaced with opaque tokens), symbol+timeframe+rule combinations, and any figure that
     would let a reader reconstruct position sizing. What remains: the run structure, the
     diff-attribution method, the class census (counts only), and the isolation/write-safety
     result — the parts that prove the acceptance was rigorous, not what it earned. -->

# Formal acceptance — summary

**Status:** FINAL, assembled 2026-07-26. 8 runs, all ledgers extracted, all diffs attributed, all
run directories kept intact for audit.

## What was run

The real shim broker (venue-matching library + broker-personality netting) replaced the mock in
the harness. Integration smoke went green first: engine boot → order placement → simulated fill
→ engine poll-diff observed the fill → witness log carried matching deal identifiers. Isolation
PASS, zero unscoped writes outside the run's own directory.

The acceptance itself replayed a real historical live trading window **under the exact binaries
and environment that traded it**, not the current code:

- The window was segmented at the live engine's actual restarts (6 segments), each run under the
  binary fetched and hash-verified from the corresponding rollback copy, seeded from live ground
  truth at each boundary (balances reconstructed backward from a statement anchor; open-book state
  cross-checked against venue deal history).
- A separate full-window run under the *current* binary, same seed, isolates what recent code
  changes altered — a counterfactual, not a second ground truth.
- A deep-start variant reboots at the live engine's actual last restart before the window
  (rather than a synthetic boot at window-start) to separate "the mirror is wrong" from
  "the mirror was never given the multi-day warm state live had."

## The attributed diff

Every live order-lifecycle event in the window was matched to a rehearsal event by leg identity
and nearest placement time (18 rows in the primary run). Every row — matched or not — was assigned
exactly one cause class:

- **exact match** — same decision, same second (typically within ~2s, a replay-pacing artifact),
  same price to the tick, same outcome.
- **(b) tape/clock resolution limit** — a known, bounded difference from replaying without the
  original bid/ask spread, or from timing compression amplifying a genuine live race condition.
- **(c) seed/input limit** — an input the acceptance could not recover from any existing record
  (e.g., a live governance-module snapshot at an arbitrary non-restart instant), stated as
  unrecoverable rather than guessed at.
- **(d) shim defect** — a real bug in the rehearsal broker itself.

Class census, primary run (18 matched rows + day-level P&L reconciled to the last cent, figures
redacted): **0 class-(a)** unexplained deltas by construction; **6 class-(b)**; **8 class-(c)**;
**0 class-(d) outstanding**. One class-(d) defect *was* found during acceptance (a market-order
under-fill edge on the no-spread tape), root-caused, fixed three ways, covered by a new regression
test, and every affected run was re-run clean before the census above was taken — isolation PASS
and zero contamination flags across all final runs.

**Every dollar of both exchange-day P&L deltas was accounted for by named rows** — the acceptance
record states this explicitly and shows the per-row decomposition; the figures themselves are
redacted here.

## Verdict (as recorded)

> The mirror reproduces the live engine's trading up to the known delta and the named limits
> above — with era-exact binaries and environment, every live order decision the mirror also took
> was reproduced at the same second, the same price to the tick, and — where quantities agreed —
> the same P&L to the cent.

What the acceptance states it could **not** close, plainly: the live governance module's
instantaneous state at an arbitrary non-restart instant (not recoverable from any existing
record); sub-tick spread behavior (no quote-level data exists for the dates in question); and
live's exact in-memory state between restarts (bounded, not eliminated, by the deep-start
variant — the signal stream converges to live's within a session once booted at a real restart).
