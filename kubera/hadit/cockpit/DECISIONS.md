# Decisions — HADIT Cockpit

## 1. No web framework
**Chosen:** Python stdlib `ThreadingHTTPServer`, hand-registered routes.
**Rejected:** Flask/FastAPI/Django. For a single-operator internal tool with no need for templating engines, ORMs, or a plugin ecosystem, a framework adds a dependency surface and an upgrade-treadmill for a process that renders live-money data — the stdlib server is enough, auditable in full, and has no supply-chain surface beyond Python itself.

## 2. One generator, one data domain, no cross-talk
**Chosen:** 27 independent generator services, each owning exactly one panel's data, each writing its own state file, none reading another's.
**Rejected:** one monolithic data-aggregation service feeding all panels. A single aggregator becomes a single point of failure for the whole cockpit and a coordination bottleneck for 27 independently-evolving data domains; independent generators mean a margin-watcher bug never takes down the live-candles panel.

## 3. Watchers and watchdog PUSH; everything else is PULLED
**Chosen:** a dedicated ingest endpoint for real-time safety state (health, per-watcher alerts), while ordinary panel data is pulled by the server from generator-written state files.
**Rejected:** polling the watcher fleet for status. Safety-relevant state (is something currently critical, is the engine alive) needs to reach the display the instant it changes, not on the next poll cycle — the push path exists specifically for that class of data, and only that class.

## 4. Explicit, dated, human-signed route annotations for money-path vs. display-only
**Chosen:** every route that could plausibly be mistaken for an order path carries an in-source comment stating it is not, with the date and the operator who authorized that classification.
**Rejected:** relying on function naming or file organization alone to communicate which routes can move money. A comment that has to be renewed with a name and a date is a much higher bar to silently violate than an implicit convention — anyone reading the code six months later gets the same clarity the original author had.

## 5. Two independent chart implementations, not one shared component
**Chosen:** `chart.html` and `hadit_chart.html` exist as separate, ~4,000-line pages rather than one parameterized chart component.
**Rejected:** unifying them behind a shared abstraction. (Recorded honestly as a real design tradeoff, not necessarily an endorsed one — duplication here trades maintenance cost for the ability to evolve two chart use-cases independently without one change risking the other; this repo states it plainly rather than presenting it as an unqualified best practice.)
