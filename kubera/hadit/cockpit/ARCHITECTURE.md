# Architecture — HADIT Cockpit

## Components

- **`server.py`** (~3,800 lines): a single Python process using the stdlib `ThreadingHTTPServer` — no Flask/FastAPI/Django. Every route is a hand-registered path handler. This is a deliberate minimalism: no framework dependency for the process that renders the family's live trading surface.
- **27 generator services** (systemd, most on short timers or persistent daemons — see [engine/EVIDENCE](../engine/EVIDENCE/09_verification_harness_fleet_and_automation_scale.md) for the full 47-unit automation count on this host): each owns exactly one data domain (candles, spirit geometry, margin, decay, weather/regime, ledger, EOD) and writes to a state file the server reads. No generator talks to another generator directly — the server is the only consumer, and generators never write to each other's state files (a discipline that keeps 27 independent processes from needing to coordinate).
- **15 front-end pages**: not a single-page app — `index.html` (the main dashboard), two independent chart implementations (`chart.html`, `hadit_chart.html`), a `backtest.html`, a `mirror_timetravel.html` / `mirror_runs.html` pair (Time Travel Mirror visibility), `monitoring.html` (the watcher/watchdog ingest display), `hardware.html`, `edge.html`, `gold_recon.html`, `weather_terroir.html`, and smaller utility pages.

## Data flow

Two distinct feed types reach the server, and the codebase treats them differently:

1. **Pull, generator-fed**: the 27 generators write state files on their own schedule; the server reads them on request. Stale-tolerant by design — a generator outage degrades one panel, not the whole cockpit.
2. **Push, watcher-fed**: the NUIT watcher fleet and the equity watchdog actively POST their verdicts to two dedicated ingest endpoints (`_handle_health_ingest`, `_handle_monitor_ingest`) — these are real-time, not polled, and use atomic writes (`tmp` file + `os.replace`) so a crash mid-write never corrupts the state the Monitoring tab reads. See `SNIPPETS/health_ingest_handler.py`.

## Boundaries

- **Display vs. order path, annotated in source.** Routes that only surface data carry an explicit comment and an operator authorization note (e.g. "NOT a money-path / order route — health monitoring only. (Leo-authorized 2026-07-05.)"). This repo's redaction policy keeps the money-path routes' specifics out of evidence text, but the *pattern* — explicit, dated, human-signed annotation of which routes can and cannot move money — is itself real design discipline worth showing.
- **The cockpit does not compute strategy or risk logic.** It renders what the engine, the generators, and the watchers already decided; the generators themselves are read-only consumers of engine/witness state (see [engine/ARCHITECTURE.md](../engine/ARCHITECTURE.md)).
- **The 38 cockpit-feeding services are a subset of the engine project's 47-unit automation total** — cross-referenced there, not double-counted here.

## Failure modes

- A dead generator degrades its one panel (stale data, visibly time-stamped) rather than crashing the server — each panel reads independently.
- A dead watcher/watchdog stops pushing to the ingest endpoints; the Monitoring tab shows the last-received verdict with its timestamp rather than silently going blank, so staleness itself is visible.
