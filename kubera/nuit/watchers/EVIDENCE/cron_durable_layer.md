# EVIDENCE: cron durable layer + 3h backstop

What: `crontab -l` on the research host, captured 2026-08-31.
Redacted: the baseline commit sha replaced with `<sha>`; the operator names in the original
comment generalized to "the operators" per the repo's redaction rule (recipient identities are
never shown, even in a comment).

```
# Los Verí LIVE supervision — DURABLE layer (survives session death). Re-armed 2026-08-08 (Sat). UTC.
# Baseline: live sha <sha> (authorized deploy). Silent when flat; telegram the operators.
# --- event-driven safety detectors (every 60s) ---
* * * * * /usr/bin/python3 /home/nuit/managed_stop_watch.py >/dev/null 2>>/home/nuit/for_the_record/.managed_stop.cronerr
* * * * * /usr/bin/python3 /home/nuit/zeroed_leg_watch.py >/dev/null 2>>/home/nuit/for_the_record/.zeroed_leg.cronerr
# --- 2h backstop: runs wake_report, archives -> backstop_runs/latest.md, telegrams ONLY on sha-drift/crash ---
# Fires :05 past even UTC hours. Self-silent when flat + sha-matched.
* * * * * /usr/bin/python3 /home/nuit/trade_watch.py >/dev/null 2>>/home/nuit/for_the_record/.trade_watch.cronerr
5 */3 * * * /home/nuit/backstop_run.sh >/dev/null 2>>/home/nuit/for_the_record/.backstop.cronerr
```

Two things this proves:

1. **"Re-armed 2026-08-08"** in the header is the layer's own maintenance record — this is not a
   set-and-forgotten cron entry; someone came back and re-confirmed it against a baseline after
   the fact.
2. **The backstop cadence changed** from 2h to 3h (visible in the `backstop_run.sh` comment,
   `EVIDENCE`d separately) — evidence this layer is tuned under operational pressure ("conserving
   tokens" per the source comment), not installed once and left alone.

`backstop_run.sh`'s own header states the alert contract precisely: it telegrams only on
(a) live-sha drift from the authorized baseline, or (b) the snapshot script crashing/hanging.
Every other 3-hour cycle is silent by design — see `SNIPPETS/silent_when_healthy_gate.py` /
`silent_when_healthy_gate.sh` excerpt for the mechanism.
