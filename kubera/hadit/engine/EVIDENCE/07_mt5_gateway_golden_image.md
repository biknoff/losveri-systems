<!-- What: design excerpt from hadit-mt5-gateway/start.sh (the execution host), the boot script for the containerized
     MT5 terminal gateway. Redacted: none needed — no hostnames, IPs, or account values appear in the
     excerpted lines; internal container paths (/hadit_mt5, /opt/wineprefix) are generic, not
     topology-revealing. -->

```bash
#!/bin/bash
# Hadit MT5 — GOLDEN IMAGE runtime boot.
# MT5 + servers.dat + ZMQ EA + chart are already baked into the image
# (see build_install_mt5.sh). This script does NOT install or compile anything —
# it only: writes the per-container auto-login + governor config from env,
# launches the terminal, and keeps it authorized.
#
# GOVERNOR (Algo Trading) is DECLARATIVE, not toggled. The [Experts] Enabled=1 /
# AllowDllImport=1 block in mt5cfg.ini IS the master switch: a fresh terminal
# launched with /config:mt5cfg.ini boots with the governor already ON. This is
# the idempotent Linux-native mechanism — rewriting the same config every boot
# cannot invert the state. There is NO ctrl+e, NO xdotool, NO accounts.dat seed,
# NO window focus. Governor health is observed over ZMQ (EA heartbeat), never via
# the bridge. Cold boot is therefore instant. Deterministic, headless, no LLM in
# the loop.
```

```bash
# --- re-assert broker directory + PURGE the legacy EA (idempotent; cheap) -------
# No EA, no chart: the tick/order interface is the wine-python ZMQ gateway, not an
# Expert Advisor. We only need servers.dat so a fresh terminal can resolve the broker.
rm -f "$MQ/Profiles/Charts/"*/chart*.chr 2>/dev/null
rm -f "$MQ/Experts/HaditZmqEA.ex5" "$MQ/Indicators/HaditZmqTicks.ex5" 2>/dev/null
```

**What this proves:**
- **No GUI automation.** The terminal's algo-trading state is set by a config file baked into the
  image and rewritten declaratively on every boot — not by simulated keypresses or window-focus
  tricks (the comment names the specific anti-pattern it replaced: an "edge-triggered ctrl+e
  toggle" that had previously flipped a different account's governor OFF by accident).
- **Idempotent, deterministic boot.** The script also disables Wine's auto-update mechanism with a
  one-line sentinel file, because the update was measured to rewrite ~1,678 files (~1.6 GB) into the
  container's writable layer on every cold start otherwise — a concrete, measured justification for
  the idempotency rule, not a guess.
- **No EA, no chart.** The order/tick interface is a separate ZMQ gateway process, not an Expert
  Advisor running inside the terminal — the legacy EA and chart are actively purged on every boot so
  they can never silently re-bind the gateway's own socket.
