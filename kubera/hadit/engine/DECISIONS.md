# DECISIONS

Part of HADIT — see [STORY.md](../../../STORY.md). Each decision states the nearest-wrong
alternative that was rejected, not just what was chosen.

1. **Venue deal-history truth over engine-computed P&L.** Exit price and profit are read from the
   broker's own `history_deals` records (`summarize_exit_deals`, `SNIPPETS/venue_truth_gate.rs`).
   *Rejected:* trusting the engine's own fill/exit bookkeeping — it would agree with itself even
   when a netted sibling position corrupted the attribution.

2. **Fail open to null, never fabricate.** When a merged position's per-leg exit can't be cleanly
   attributed, the field is left `None` (`SNIPPETS/fail_open_to_null.rs`, three independent call
   sites). *Rejected:* a best-effort estimate (e.g. splitting profit proportionally) — it would
   look like data and hide exactly the cases that need a human's attention.

3. **Separate watchdog process, not in-engine risk checks.** `equity_watchdog.py` runs as its own
   systemd unit, polls the same gateway the engine trades through, and can flatten/halt/latch with
   "zero shared code with the engine" (`EVIDENCE/03`). *Rejected:* risk checks living inside the
   engine's own event loop — a bug that breaks the engine's judgment breaks its self-check at the
   same time.

4. **Byte-parity certification before cutover, not test-suite-only equivalence.** Each strategy
   bottle is certified bar-for-bar against a recorded oracle trace (`EVIDENCE/02`), and a
   certification run that finds nothing wrong is treated with suspicion, not relief — the 2026-08-10
   audit that caught a stale oracle is the evidence trail for that stance. *Rejected:* a green unit
   test suite as sufficient proof of behavioral equivalence — unit tests exercise what the author
   thought to test; a byte-parity replay exercises what actually happened.

5. **Witness spine as source of truth, not engine state dumps.** Downstream systems (recon,
   attribution, audits) read the append-only JSONL witness log, never the engine's in-memory state.
   *Rejected:* periodic state snapshots — a snapshot only shows the last state, not the sequence of
   decisions that produced it, and a snapshot taken after a bug has already run silently through
   memory tells you nothing about when it started.

6. **Rehearse in a byte-linked mirror before deploying, not a staging environment with drifting
   deps.** Every deploy branch is exercised in the Time Travel Mirror — a tree where 372/373 files
   are literal symlinks into the live engine's own bytes (`../../nuit/time-travel-mirror/`).
   *Rejected:* a conventional staging server with its own checkout and its own dependency
   versions — it can pass while the live tree, months later, has silently drifted from it.

7. **Human-only latch clear, never an automatic cooldown.** The watchdog's trip latch blocks both
   re-tripping and engine relaunch until a human deletes the latch file
   (`EVIDENCE/03`). *Rejected:* a timed cooldown that auto-clears — it would relaunch into whatever
   condition caused the trip in the first place, with nobody having looked at it.

8. **Loud failure for the witness writer, but never a trading-blocking one.** A witness write
   failure increments a counter and logs (`SNIPPETS/witness_append.rs`) instead of either silently
   dropping the event or halting the order path. *Rejected (both directions):* silent drop (an
   observability spine that can fail invisibly is worse than no spine) and hard-block-on-write-
   failure (a full disk on the logging path should not be able to stop live risk management).

9. **Bare canon repo plus a runtime tree that refuses to build.** `engine-canon.git` on the
   execution host holds full mirrored history; the runtime tree carries a `DO-NOT-BUILD.md` stating
   it has "historically produced wrong, feature-missing binaries" when built in place
   (`EVIDENCE/06`). *Rejected:* building directly on the execution host — convenient, and the exact
   mechanism that produced wrong binaries before the rule existed.

10. **Declarative golden-image MT5 boot, not GUI automation.** The algo-trading governor is a config
    file baked into the image and rewritten idempotently on every boot (`EVIDENCE/07`).
    *Rejected:* the prior `ctrl+e` edge-triggered toggle approach — the source comment records that
    it once flipped a different account's governor off by accident, which a declarative boot cannot
    do because there is no toggle to mis-time.
