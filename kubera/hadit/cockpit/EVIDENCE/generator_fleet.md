<!-- What: the real, named list of systemd services feeding cockpit panels, read directly from the
     live execution host's unit list. Redacted: none — unit names only, no state/content. -->

## 27 named generator services (of the engine project's 47-unit automation total)

```
alarms · alarm-watcher · banked · bartender · check-narration · cockpit ·
dayleg-cap · decay-alerts · decay-state · deck-descriptor · deck-health ·
edges-live · eod-report · gold-weather · law-state · ledger-emitter ·
live-candles · liveness · margin-watcher · mes-decay · positions · radial ·
readiness · recon-daily · spirits-geometry · spirit-stats · thoughtbubble ·
weather · weather-arm · weather-terroir · witness-edp-backfill · witness-rollup
```

Each name maps to exactly one panel or data domain on the front end — `live-candles` feeds the
chart pages, `spirit-stats`/`spirits-geometry` feed the per-leg strategy cards, `margin-watcher`/
`decay-alerts`/`mes-decay` feed the risk-monitoring panels, `weather`/`weather-arm`/
`weather-terroir` feed the regime-awareness banner, `eod-report`/`ledger-emitter`/`banked` feed
the end-of-day and ledger views, `witness-rollup`/`witness-edp-backfill` keep the witness-derived
displays current. `recon-daily` is the same nightly reconciliation documented in the
[Time Travel Mirror](../../nuit/time-travel-mirror/) project — surfaced here, not re-implemented.
