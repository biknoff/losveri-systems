# Architecture

## Orchestrator, not monolith

Chris runs as a **Vertex AI Agent Engine** deployment built on Google's Agent Development Kit (ADK). The root agent (`agent.py`) is deliberately thin: it does not parse transactions or do arithmetic itself. It holds an LLM-driven routing prompt that reads the request and hands off to one of eleven sub-agents, each scoped to one domain:

- `expense_agent`, `income_agent`, `loan_borrowing_agent` — the money-math specialists (schedule calculation, recurrence, persistence)
- `household_query_agent` — reads the Life Tracker spreadsheet, MD Balances, and the bank feed; answers "what's unlogged," "what did I spend," "can we afford X"
- `calendar_agent`, `chris_viz_agent`, `stats_site_agent`, `venture_intelligence_agent`, `distribution_reconciliation_agent`, `knowledge_library_agent`, `research_agent` — surrounding capabilities

Persistence — writing to the Sheet-of-record and creating Calendar events — is centralized rather than duplicated per sub-agent, so every write goes through the same idempotency and locking discipline regardless of which sub-agent produced it.

The runtime carries its own defensive layer for the Vertex managed environment: it sanitizes environment variables that would otherwise let API-key auth leak into a managed-runtime Vertex session, and hydrates non-secret runtime defaults (sheet ID, calendar ID, GCP project number — none of which are credentials) when it detects it's running under Cloud Run/Vertex markers rather than locally.

## The expense flow (voice note → ledger)

A voice note is transcribed upstream by **Hanuman**, the Council's comms gate (`../hanuman/`) — Chris does not do speech-to-text itself. The resulting text arrives as an intent. An earlier, still-live layer of the same codebase (`command_engine.py` / `meta_layer.py`) classifies the intent — `NEW_TRANSACTION`, `CORRECTION_OF_PREVIOUS`, `FEEDBACK_ON_SYSTEM_BEHAVIOR`, `ARCHITECTURAL_INSTRUCTION`, `CONVERSATIONAL`, or `AMBIGUOUS` — using both regex hints (amount patterns, date patterns, correction language) and LLM judgment, then confidence-scores the result.

For a new expense, the `expense_agent` sub-agent computes the schedule (one-time or recurring subscription, negative cashflow convention) via a shared `FinancialEngine`, then calls persistence tools that write the schedule to the spreadsheet and create the matching Calendar event(s) in the same pass. Every mutating write carries an idempotency key derived from a stable hash of the normalized payload plus the source event, so a retried webhook or a duplicated voice note doesn't create a duplicate ledger line.

## SimpleFIN bank feed — built and wired

A `simplefin_client.py` module in Chris's own `tools/` package talks to the SimpleFIN Bridge API directly (read-only account/transaction fetch, 90-day request window). The access URL is resolved through a layered lookup — a bundled file for the deployed Vertex runtime, a local dev file, an environment variable, or GCP Secret Manager as a last resort — and is never logged.

This client is called from `household_query_tools.py`, which is imported by `household_query_agent` and wired into the root agent's routing table. Two tools sit on top of it:

- `get_recent_bank_transactions` — raw pull of transactions + balances for a lookback window
- `find_unlogged_transactions` — the primary tool: pulls bank expenses, reads the Life Tracker for the same period, and buckets each bank transaction as already-logged (amount-and-day match), an ATM cash withdrawal (flagged separately, with a prompt back to the user), an internal transfer or bridge fee (filtered out), or genuinely unlogged (returned with a category guess, sorted card-priority-first).

This is real, running code exercised against the live account, not a stub — it is "wired" in the sense that a household query actually invokes it end-to-end and gets real transactions back.

## Reconciliation — the designed half

`find_unlogged_transactions` is a **diff, surfaced to a human** — it never writes back to the ledger. The match it performs (same day, same rounded amount) is a heuristic gap-finder, not a reconciliation engine: no persisted match state, no confidence score attached to a specific ledger row, no automatic write-back that marks a Sheet entry "reconciled" or resolves an amount mismatch. A separate, earlier module in the codebase (`reconcile.py`) defines a `RECONCILE` event type and the event-sourcing plumbing (idempotency keys, event store) that a real reconciliation engine would build on — but nothing currently drives it against the SimpleFIN feed.

Stated plainly: the design for closing this loop — bank transaction → confidence-matched ledger entry → automatic reconciliation write — exists in shape (the event type, the client, the diff tool are all in place as building blocks) but the matching-and-write-back engine itself has not been built. Today a human reads what `find_unlogged_transactions` surfaces and decides what to log. That is the honest boundary of what runs versus what is designed.

## Meta-cognitive review layer

See [EVIDENCE/04-meta-cognitive-layer.md](EVIDENCE/04-meta-cognitive-layer.md) for the design excerpt and what it reviews.
