# Decisions

Choices made building and later retiring the Chicago pipeline, with the rejected
alternative stated for each.

## 1. Bridge Python strategy logic into NT8 via a C# layer

**Chosen:** write/author strategy logic on the Python side, transpile/port it into
NinjaScript C# to run inside NinjaTrader 8's native execution model.
**Rejected: write strategies natively in C# from the start.** NT8's own language is
NinjaScript C#. Staying Python-side kept strategy authoring in the same language as the
rest of the research stack (the NUIT discovery pipeline), at the cost of needing a bridge
and, later, a parity problem between the two languages.

## 2. Prove two-language agreement, don't trust the port

**Chosen:** treat "does the C# side actually do what the Python side specified" as a
question requiring verification, not an assumption.
**Rejected: trust the port.** This is the decision that mattered most in hindsight — it
is the direct ancestor of the parity discipline that now governs the Rust engine (see
`../engine/`'s Time Travel Mirror, byte-identical build certification against the
Nautilus oracle). The habit of demanding proof that two implementations of the same logic
agree was born here, where the two languages were Python and C#, not Python and Rust.

## 3. Supervised auto-relaunch of the runner, not manual restarts

**Chosen:** a supervisor process watches the live runner and relaunches it automatically
(~5-8s) on failure, with a mandatory post-restart verification step
(`transport=WIRED armed=True`) before trusting the new process.
**Rejected: manual restarts.** A human noticing and manually restarting a crashed runner
is both slower and skips the verification ritual under pressure. Building the supervisor
in from early on is what let the team run this on a platform (consumer NT8/Windows) that
crashes and needs restarting in the first place.

## 4. A restart-safety window rule around armed positions

**Chosen:** explicitly forbid restarting the runner during an armed funded-leg window
unless the trigger is far out-of-the-money.
**Rejected: restart whenever convenient.** Restarting mid-position risk is exactly the
kind of operational hazard that GUI-automated, single-process trading platforms create;
writing the rule down and enforcing it by hand was the precursor to the engine's later,
formal force-flat/armed-window guards.

## 5. Record live ticks even though nothing downstream consumed them yet

**Chosen:** add an additive, env-gated tick recorder that tees the live tape to a local
Parquet catalog (added mid-pipeline, 2026‑06‑09, once the team noticed the tape was being
discarded).
**Rejected: only capture the data once there was an explicit user for it.** Recording
first, finding the use later, meant the record exists at all — the daily tape files and
the `backfill_*` file in `EVIDENCE/production-tree-counts.md` are the direct result.

## 6. Retire the platform, don't keep patching it

**Chosen:** deliberately move off NT8/Windows once the C# bridge, GUI automation
fragility, and single-box crash/restart risk stopped being worth managing, and rebuild
the execution layer on an open, scriptable stack (Nautilus/Python, then the Rust engine).
**Rejected: keep patching consumer-grade infrastructure.** More supervision, more restart
rules, and more careful ritual could have kept NT8 limping along further. The team's own
framing — "we evolved out of consumer-grade NT8/Windows" — is a statement that the
platform's ceiling had been reached, not that the approach had failed. Both the original
Chicago VM and the successor Windows box (HaditFugue) are gone; nothing was left running
on them to maintain.

## 7. Preserve the artifacts instead of letting the retired boxes take them

**Chosen:** before decommissioning, pull the strategy trees, ATM templates, analyzer
logs, and tick tapes off the Chicago box and keep independent copies (one on the current
build host, one mirrored to a second machine).
**Rejected: let the exported/backup copies be the only record, or let the box's demise
delete the history.** The counts and date ranges in `EVIDENCE/` exist only because this
decision was made — a retired platform whose evidence had been deleted with it would be
unprovable, not just unavailable.
