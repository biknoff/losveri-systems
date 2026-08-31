# Architecture — HADIT Miami

## Scope

This document covers the backend (data + execution plane) and the fleet/boot model. The frontend is a manual-trading web cockpit reusing the family's existing HADIT cockpit design (see [HADIT engine](../engine/)), repointed at this backend's ZMQ surface.

## Fleet model: one image, N containers

MT5 is a one-login-per-terminal platform — there is no multi-account mode inside a single terminal process. Miami's answer is horizontal: **one MT5 image on disk, shared copy-on-write**, and **one container per external account**, each running its own Wine-hosted MT5 terminal plus a thin writable layer. A per-account gateway process (`mt5_zmq_gateway.py`) sits inside each container, using the *official* MetaTrader5 Python API locally (no chart, no Expert Advisor, no GUI automation) and fans that account's data and execution surface out over ZeroMQ.

Two gateway roles, selected by an environment variable (`MT5_ROLE`):

- **`data`** — one per broker, not per account. Publishes the shared tick stream (`ZMQ PUB`) that every account on that broker subscribes to, plus historic-tick service. Ticks are not pulled per-account; that would multiply the load by N accounts for identical broker prices.
- **`exec`** — one per account. A `ZMQ REP` socket serving account/order commands only (snapshot, place, modify, cancel, flatten). Cheap, because it carries no tick traffic.

Isolation between accounts is enforced at three layers simultaneously: container, OS thread/process, and socket. A fault or credential in one account's container cannot reach another's.

## Declarative config, not GUI automation

Each terminal's auto-login (`Login`/`Password`/`Server`) and governor state (`[Experts] Enabled=1` — MT5's "Algo Trading" master switch) are written into an `mt5cfg.ini` before the terminal ever launches, from a per-account secret. Launched with `terminal64.exe /portable /config:mt5cfg.ini`, the terminal auto-connects headlessly; the "Open an account" wizard modal never appears, so nothing downstream (IPC handshake, the exec gateway) blocks on it. Rewriting the same declarative config on every boot cannot flip the governor into the wrong state — earlier iterations tried the reverse (`ctrl+e`/xdotool toggling, an edge-triggered UI action) and it silently flipped an account's trading off. See `SNIPPETS/gen_mt5_config_declarative.py`.

## Reconcile the fleet at boot

A registry (`fleet_registry.json`) declares the desired containers — which accounts should exist and running. On host or Docker restart, `reconcile_boot_fleet.py` walks that registry and, for each declared account:

1. Checks live container state via `docker inspect`.
2. Brings up anything `absent` via `docker compose up -d --no-deps`.
3. Repairs restart policy and memory caps on any container whose settings drifted (including containers that predate the current generated compose file).
4. Starts anything `stopped`.
5. Staggers each start (default 8s) and waits for memory headroom before starting the next, to avoid a startup spike across a fleet of Wine prefixes.

This runs under a file lock so a concurrent boot pass can't race itself. The reconciler deliberately owns *only* boot recovery — it never embeds account credentials; the cockpit owns account configuration, the reconciler owns making the declared containers actually exist and run.

## Command surface

Every account's exec gateway exposes the same small JSON command set over `ZMQ REQ/REP`: `ping`, `snapshot`, `account`/`positions`/`orders`, `place` (bracket order — LIMIT entry with atomic server-side SL/TP), `modify` (drag entry/SL/TP), `cancel` (one working order), `flatten_all` (close all positions — priority #1), `cancel_all` (cancel all pending + detach SL/TP — priority #2), `history_ticks`, `history_rates`. See `SNIPPETS/gateway_command_surface.py` for the exact shape.

Multi-account and copy-trading both reduce to the same primitive: the cockpit fans one user action out to every subscribed account's `REQ` socket in parallel. Measured fan-out (7 accounts, 2 brokers): wall-clock for `place`/`cancel_all` across all accounts is bounded by the *slowest single account*, not the sum — genuinely parallel, not serialized.

## Boundary: family infrastructure vs. external-user infrastructure

The family's own execution engine ([HADIT engine](../engine/)) and its manual-trading cockpit run on a separate server from Miami. Miami is a complete, self-contained stack — fleet, gateways, cockpit, and the external users' credentials — on its own dedicated box. The two stacks share lineage (the cockpit UI design, the ZMQ-fan-out pattern) but not infrastructure, credentials, or failure domain. When the family later ported a cockpit panel into their own the family's futures venue setup, they ported it *from* Miami's canonical panel — evidence that the design flowed outward and then partly back, never that the infrastructure merged (see `EVIDENCE/cross_pollination_family_cockpit.md`).

## Known scaling limit

Terminal RAM is the wall: N accounts = N Wine/MT5 terminals at roughly 400MB each (one terminal per login, no way around it on this platform). The ZMQ/data layer itself scales cheaply — ticks are one shared PUB per broker regardless of account count. Roughly ten accounts fit comfortably on a modest box; larger fleets need more RAM, not architectural changes.
