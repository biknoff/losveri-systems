# Decisions — HADIT Miami

Each entry: the choice made, and the alternative considered and rejected.

## 1. External users on a separate, dedicated server
**Chosen:** Miami runs on its own box, entirely apart from the family's own execution engine.
**Rejected:** shared infrastructure with the family's own accounts. External users' credentials, containers, and failure domain would then sit next to live family capital — one compromised or misbehaving external account could reach the family's own trading. The cost of a second box was accepted specifically to make that impossible structurally, not by policy.

## 2. Per-account containers
**Chosen:** one MT5 terminal + one gateway process per account, each in its own container.
**Rejected:** one shared terminal serving multiple accounts. MT5 is one-login-per-terminal by design, so a shared terminal would mean either constant re-login (breaking live positions/state) or building account-switching logic MT5 was never built for. Per-container isolation also means one account's crash or corrupted state cannot touch another's.

## 3. Reconcile the fleet at boot
**Chosen:** an explicit reconciler that checks every declared account's container state after every host/Docker restart and repairs what's missing, stopped, or drifted.
**Rejected:** assuming containers came back up correctly on their own (relying on Docker restart policies alone). Restart policies drift, get overwritten by manual debugging, or don't cover every failure path (a stopped container with a healthy restart policy still doesn't come back on host reboot without a compose-level reconcile). The reconciler makes "the declared fleet exists and runs" an actively-checked invariant, not an assumption.

## 4. Declarative terminal configuration
**Chosen:** login and governor (algo-trading) state written into `mt5cfg.ini` before every boot; the terminal launches already configured.
**Rejected:** GUI automation (`ctrl+e` toggling, xdotool, clicking through the login wizard). GUI automation is edge-triggered and non-idempotent — proven in production, where a governor toggle silently flipped an account's trading off. A declarative config that's rewritten identically every boot cannot end up in the wrong state by construction.

## 5. Official MetaTrader5 API over ZeroMQ, not an Expert Advisor
**Chosen:** the gateway uses the official MT5 Python API locally inside the Wine process, with no chart, no EA, no candle subscription.
**Rejected:** an EA-based bridge (chart-attached Expert Advisor talking out via a custom protocol). EAs gate on chart-symbol synchronization, which turned out to be a real, costly failure mode — a broker/account-type symbol-suffix mismatch (e.g. a standard vs. pro account naming the same instrument differently) meant a chart could never sync, and that failure was originally misdiagnosed as an architecture problem rather than a naming one. Removing the EA removed the entire failure class.

## 6. One shared tick feed per broker, not per account
**Chosen:** a single `data`-role gateway per broker publishes ticks; every account on that broker subscribes to the same feed.
**Rejected:** each account's gateway pulling its own tick feed. Prices are identical across accounts on the same broker — pulling per-account would multiply load by the account count for no informational gain, and would not scale past a handful of accounts.

## 7. Auto-resolve the traded symbol per account, never hardcode it
**Chosen:** each account resolves its own tradable symbol name at connect time.
**Rejected:** hardcoding a symbol string across the fleet. The same instrument (e.g. gold) can carry different suffixes depending on broker and account type; a hardcoded symbol works for some accounts and silently fails for others.

## 8. Derived (delta) Docker images, not full rebuilds, on a disk-constrained host
**Chosen:** a thin image layer adding just the ZMQ gateway on top of a proven, already-built MT5 base image.
**Rejected:** rebuilding the full multi-gigabyte MT5+Wine image on every change. On a disk-constrained box, a full rebuild risked (and once caused) running out of disk mid-build, which silently corrupted a file transfer. A derived image keeps changes small and the base reusable across the fleet.
