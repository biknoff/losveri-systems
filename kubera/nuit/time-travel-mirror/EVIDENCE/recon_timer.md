<!-- WHAT: the nightly reconciliation systemd timer, verbatim, plus the pipeline it triggers.
     REDACTED: nothing in the timer unit itself needed redaction (no hostnames, paths, or
     credentials in the [Timer] stanza); the description comment naming an internal chain step
     ("mes-glbx-sync") is left as-is since it names a pipeline stage, not a credential or
     account. -->

# Nightly reconciliation — trigger

`~/.config/systemd/user/rust-recon-daily.timer` (user systemd unit, host: the research/recon
host), verbatim:

```ini
[Unit]
Description=Nightly Rust recon (gold+MES) at 22:12 UTC (after the EOD chain + mes-glbx-sync 21:30, off-minute)

[Timer]
OnCalendar=*-*-* 22:12:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
```

`Persistent=true` means a missed run (host down at 22:12) fires as soon as the timer unit is next
active, rather than being silently skipped until the next scheduled slot.

## What it triggers

`OnCalendar` fires the paired `.service` unit, which runs `run_daily.sh`. That script:

1. pulls the day's tick and bar data for the instruments the engine trades,
2. regenerates a governed replay — the same law-in-loop engine code the mirror links, run over the
   week-to-date data, not an independently-modeled backtest,
3. hands the live witness spine and the governed replay to the verdict builder
   (`build_verdict.py`), which matches, classifies, and rolls up every row (see
   [`../SNIPPETS/`](../SNIPPETS/) for the classifier legend and the unpriced-rows logic),
4. writes the verdict/digest feed files and pushes the nightly digest.

Chosen deliberately at :12 past the hour, after the day's end-of-day settlement chain and a
separate data-sync job at :30 the hour before — the timer's own description states why, rather
than leaving the off-minute unexplained.
