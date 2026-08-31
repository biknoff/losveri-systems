# Decisions

## Voice as the input for an expense
**Chosen:** speak the expense, Hanuman transcribes, Chris parses and writes it.
**Rejected: a form to fill in.** A structured expense-entry app is easier to build and easier to validate, but it adds friction at the exact moment (mid-errand, hands full) an expense actually happens. The whole point of the household finance layer is that logging an expense costs nothing more than saying it.

## Multi-agent orchestrator, not a monolith with tools
**Chosen:** a thin ADK root agent that routes to eleven scoped sub-agents (expense, income, loans, household query, calendar, viz, ...).
**Rejected: one big agent with every tool attached.** A single agent holding twenty-plus tools has to reason about all of them on every turn, and a bad tool choice on one domain (say, miscategorizing a bank transaction) has no natural boundary stopping it from also touching Calendar or another domain's data. Splitting by domain keeps each sub-agent's prompt small and its blast radius contained to what it actually owns.

## SimpleFIN — read-only aggregation
**Chosen:** SimpleFIN Bridge, a read-only account/transaction API with a Basic-Auth access URL scoped to read.
**Rejected: screen-scraping bank logins.** Screen-scraping needs the actual bank credentials, breaks on every UI change the bank ships, and grants far more access than "read my transactions" requires. SimpleFIN's model — a dedicated read-only bridge, no write capability, no stored bank password — is the smaller trust surface for the same data.

## Reconciliation stated DESIGNED, not built
**Chosen:** ship `find_unlogged_transactions` as a human-facing diff tool, and say plainly that automatic reconciliation (confidence-matched, auto-written-back) does not exist yet.
**Rejected: implying it exists because the pieces are all present.** The event type, the client, and the diff logic are all in the codebase, and it would be easy to describe this as "reconciliation" — but nothing currently matches a bank transaction to a specific ledger row with a confidence score and writes that match back unattended. Calling that "designed, not built" is the accurate claim; calling it "built" because the adjacent pieces exist is exactly the kind of overclaim this archive is built to avoid.

## Idempotency keys on every mutating write
**Chosen:** every write (Sheet row, Calendar event) is guarded by an idempotency key derived from a stable hash of the normalized payload plus the source event id.
**Rejected: trusting the caller not to retry.** Webhooks retry, voice pipelines occasionally double-fire, and a household ledger duplicating a transaction is a real, if minor, form of data corruption. The idempotency layer costs a hash computation and a lookup; the alternative costs a hand-audit of the ledger.

## A meta-cognitive review pass before anything is trusted
**Chosen:** classify intent, score confidence, and thread related messages together before letting a message become a ledger mutation.
**Rejected: trust the first-pass parse.** A single LLM parse of "fix that, it should be $40 not $140" needs to know which prior transaction "that" refers to, or it either does nothing or corrupts the wrong row. The review layer's job is specifically to catch the case where the naive first read would be wrong — corrections, feedback, and architectural instructions all need to be told apart from a genuinely new expense before anything gets written.
