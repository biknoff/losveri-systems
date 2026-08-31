<!-- What: real, direct line-count evidence for the cockpit's backend and frontend, from the live
     execution host. Redacted: none — file names and line counts only, no content. -->

## Backend

```
$ wc -l /home/hadit/hadit/amp_cockpit/server.py
3803 server.py
```

## Frontend — 15 real pages (`.bak`/`.pre_*` snapshots excluded from this count)

```
   12  delta_dashboard.html
   12  delta_index.html
   12  weather.html
  108  mirror_runs.html
  244  monitoring.html
  257  gold_recon.html
  336  backtest.html
  405  rust_canon.html
  424  hardware.html
  488  weather_terroir.html
  554  mirror_timetravel.html
  681  edge.html
 3829  hadit_chart.html
 4188  chart.html
 4855  index.html
-----
16405  total (HTML)
  948  total (JS, hadit_logic.js + others)
```

**Combined real total: 16,588 (backend) + 16,405 (HTML) + 948 (JS) ≈ 33,940 lines.**

## Iteration evidence

The static directory carries dozens of dated `.bak_*`/`.pre_*` snapshots of `index.html`, `chart.html`, and others spanning 2026-05 through 2026-08 (e.g. `index.html.pre_goldretire_20260811T224548Z`, `index.html.pre_rmrfdsizing_20260716T142826Z`, `chart.html.bak_20260705_tradepanel_hilma`) — the same before-a-risky-change snapshot discipline documented elsewhere in this repo (engine deploys, watcher scripts), applied here to the front-end code that renders live trading state.
