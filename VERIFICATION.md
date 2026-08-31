# VERIFICATION — the culture, cross-cutting

The answer to "how do you know it works?" — asked of every system here, answered differently by layer, but always answered. Evidence excerpts live in each project's `EVIDENCE/`; this page is the map.

## At the engine (execution truth)

- **Byte-parity certification.** The Rust engine was certified against its Python/Nautilus oracle bar-for-bar: 112,439/112,439 and 193,019/193,019 matched decisions; 26/28 certification checks green — and the 2 honest reds are documented with what they were, because a certification with no reds found is a certification that wasn't looking. (`kubera/hadit/engine/EVIDENCE/`)
- **Witness logs.** The engine emits append-only, per-session JSONL witness events for every order-lifecycle transition. Downstream systems treat the witness spine — not the engine's memory — as what happened.
- **Venue truth beats engine belief.** Exit prices and P&L are enriched from the broker's own deal history; where a merged position makes per-leg attribution ambiguous, fields are nulled rather than estimated ("fail open to null, never fabricate").

## Above the engine (independent supervision)

- **The equity watchdog** — a separate process, engine-independent, that can flatten, halt, and latch on breach; only a human clears the latch.
- **The NUIT watcher fleet** — nine systemd timers plus a cron "durable layer" that survives session death, on a different server than the engine, each watching one failure class (liveness, oversize, phantom orders, naked orphans, identity drift…). Watchers alert and halt; they cannot author.
- **Nightly reconciliation** — canon (what should have traded) vs live (what did), priced from venue records, with divergences classified and the digest stating plainly when a row could not be priced rather than hiding it in a total.

## Around every deploy

- **The Time Travel Mirror** — backtests compile against the live engine's actual bytes: 372 of 373 engine-tree files are symlinks into a read-only copy of the live tree, and the one divergent file is mechanically proven each build to differ by six `pub` tokens only. Deploy doctrine: rehearse in the mirror, observe, then live.
- **Flat-window swaps with rollback markers** — binary hashes recorded before/after, previous binary preserved, one-command rollback written down *before* the swap.
- **Fresh-reviewer audit before anything live.** A real example from this repo's own build period: an enrichment change passed its tests, then an independent audit found it could blend two distinct netting events into one attribution in a rare multi-fill window — a bounded but real misattribution. It was fixed, differentially re-verified, and only then deployed. The audit exists to catch exactly the bug the author's tests didn't imagine.

## In the research layer (epistemic integrity)

- **The V-chain** — candidate strategies pass staged validation gates (in-sample → out-of-sample → stress → manifest), each gate with pre-declared criteria; verdict files are on disk, dated.
- **Mongoose determinism** — 20 deterministic research workers, idempotent by contract: re-run must be hash-identical or the pipeline halts.
- **Six-state contract classifier** — every research claim carries an explicit state; an interpreter never fabricates a number.
- **Cryptographic sealing** (at its fullest) — 9/9 GPG signatures verify over the sealed record; an 8-link predecessor hash chain binds the sequence; a human-clear `LEDGER_HALT` gate stops the line on integrity doubt. Stated honestly: the automated verifier was never built (verification was run manually), and a single signing key was used. (`kubera/nuit/build-method-governance/`)

## In the somatic layer

- **Fred's detector** was validated within-person, on longitudinal data, with chronological out-of-sample splits and pre-declared stress tests (Study 1 design) — the same OOS discipline as the trading pipeline, applied to prosody. The Hume→openSMILE migration happened precisely when benchmarking moved from population to within-person: personal baselines demand deterministic, personally-anchored measurement.

**The pattern:** at every layer, the system that produces a result is never the only system that vouches for it.
