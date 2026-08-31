# Backend validation debrief (excerpt)

**What this is:** excerpt of a phase debrief documenting the Miami MT5 backend's validation across multiple accounts and brokers, on native Linux Docker.

**Redactions:** server hostname/IP, account logins, and the specific host port table have been removed. Broker names generalized to "Broker A" / "Broker B". Dates are the debrief's own internal dates, kept for lineage context.

---

> **Status:** Backend validated end-to-end across **7 accounts / 2 brokers**. Frontend (cockpit) not yet wired at this point in the project — that was the next layer (now built; see `../README.md`).
>
> Migrated the platform off Mac/emulated Docker onto **native Linux Docker**, and replaced the entire interface paradigm with a clean **official-API → ZeroMQ** backend — no Expert Advisor, no chart, no bridge.
>
> **Hard results (measured, not asserted):**
> - Deterministic cold-boot of 7 terminals (2 brokers): **~31 seconds** to all-gateways-up + both tick feeds streaming (was ~5 minutes + a stuck account before the fixes below).
> - Snapshot carries the full trading/margin section: balance, equity, margin, margin_free, margin_level, profit, leverage.
> - **Parallel order fan-out:** `place` 7/7 and `cancel_all` 7/7, **wall-clock ≈ slowest single account, not the sum** — genuinely parallel, isolated per account, across both brokers.
> - **Replicable + broker-agnostic:** new accounts, including a different broker, cold-boot on the *identical* image, auto-login, auto-resolve the traded symbol, stream + serve — zero code change.
>
> **Hurdles overcome (root causes, not symptoms):**
> 1. Governor (Algo Trading) flakiness — an edge-triggered UI toggle silently flipped an account's trading off. Fixed by making the governor state **declarative** (written into the terminal config every boot; no GUI, no toggle).
> 2. A costly misdiagnosed symbol-sync timeout — the real cause was a per-account, per-broker symbol-name mismatch (e.g. a broker's standard-account suffix vs. its pro-account symbol). Fixed by auto-resolving the traded symbol per account rather than hardcoding it.
> 3. A prior cross-platform bridge workaround, needed only when the host and the Wine/MT5 process were on different CPU architectures, was removed entirely once running on native Linux — the official API talks to ZeroMQ directly, no bridge layer.
> 4. Disk-constrained host — solved with derived (delta) images instead of full rebuilds, and file-integrity checks before baking or syncing any container image.

**Don'ts, stated explicitly in the source debrief:** no Expert Advisors/charts for the tick/order interface; no GUI-toggle governor control; never hardcode a trading symbol (varies by account type and broker); never assume a copy under a full disk succeeded without an integrity check.
