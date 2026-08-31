<!-- What: header docstring of equity_watchdog.py (the execution host), the independent account-protector process.
     Redacted: the two personal Telegram chat-id constants (replaced with <redacted>); everything
     else (thresholds, file paths, logic description) is design documentation, not a secret. -->

```
EQUITY WATCHDOG — engine-independent last-resort account protector.

Runs on the execution host as its own systemd user unit. Polls the exec gateway (the SAME live truth the
engine trades through, but zero shared code with the engine) every POLL_S seconds and trips —
cancel_all + flatten_all + stop ws2-engine-demo + LATCH + Telegram — when the account breaches:

  DAY  : loss since the trading-day anchor >= DAY_TRIP_FRAC x R_day  (malfunction detector:
         R_day = the book's WORST BY-DESIGN day = sum over legs trading today of
         mixer_qty x leg_1R. Losing more than every leg's full stop means stops are not being
         honored / engine rogue / disorderly market. Scales AUTOMATICALLY with the mixer.)
  WEEK : REALIZED week P&L <= (1 - WEEK_TRIP_PCT/100) x Monday anchor, enforced by an
         INDEPENDENT process that actually FLATTENS; the engine's own halt only blocks new
         entries and dies with it. REALIZED BASIS: the week floor is evaluated on settled
         account BALANCE, not floating equity (floating-basis stress study showed 44-61% false
         halts, zero ruin benefit). Balance moves only at position close -> deterministic.
  MARGIN: margin_level < MARGIN_TRIP_PCT with positions open (beat broker auto-liquidation).

Fail-safety: a stale/dead gateway feed NEVER trips (it could not flatten anyway) — it alerts.
A missing/garbage calibration file falls back to PCT_FALLBACK of week-anchor equity.
DRY mode (WATCHDOG_DRY=1): full decision pipeline + Telegram tagged [DRY], NO actions.
After a trip the LATCH file blocks re-trip loops AND blocks engine relaunch (relaunch script
checks it). Clearing the latch is a HUMAN act: delete the file, restart the engine.
```

```python
GATEWAY = os.environ.get("WATCHDOG_GATEWAY", "tcp://127.0.0.1:7101")
POLL_S = int(os.environ.get("WATCHDOG_POLL_S", "5"))
STATE_DIR = "/home/hadit/hadit-ws2/state"
LATCH_PATH = os.path.join(STATE_DIR, "equity_watchdog_latch.json")
HEARTBEAT_PATH = os.path.join(STATE_DIR, "equity_watchdog_heartbeat.json")
TG_CHATS = ["<redacted>", "<redacted>"]  # every alert to both operators

DAY_ALERT_FRAC = 0.50   # of R_day -> Telegram alert
DAY_TRIP_FRAC = 1.10    # of R_day (+ slippage headroom) -> FLATTEN + HALT + LATCH
DAY_TRIP_MIN_USD = 400.0  # absolute floor so a tiny/missing R_day can't hair-trigger
```

**What this proves:** the watchdog is a *separate process* (own systemd unit, own poll loop, "zero
shared code with the engine"), reads the same venue truth the engine reads (not the engine's own
belief about its state), and its only recovery path out of a trip is a human deleting a file and
restarting the engine — no auto-clear.
