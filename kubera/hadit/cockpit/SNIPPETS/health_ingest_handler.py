# Verbatim excerpt from server.py (~3,800-line stdlib HTTP server backing the HADIT cockpit).
# No identifiers, secrets, or account-specific data in this handler — it operates entirely on
# operational status strings pushed by the watcher fleet and equity watchdog.

    # ── NUIT health ingest (PUSH from the Nuit checker) ──────────────────────
    # Stores the latest {overall, targets{cockpit,engine,recorder,gateway}, ts} verdict atomically.
    # NOT a money-path / order route — health monitoring only. (Operator-authorized 2026-07-05.)
    def _handle_health_ingest(self):
        b = self._read_json_body()
        overall = str(b.get("overall") or "").strip().lower()
        if overall not in ("live", "degraded", "system_down"):
            return self._json(400, {"ok": False, "error": "overall must be live|degraded|system_down"})
        targets = b.get("targets") or {}
        if not isinstance(targets, dict):
            return self._json(400, {"ok": False, "error": "targets must be an object"})
        _now = int(time.time())
        verdict = {"overall": overall, "targets": {str(k): str(v) for k, v in targets.items()},
                   "ts": int(b.get("ts") or _now), "received_ts": _now, "wired": True}
        try:
            os.makedirs(os.path.dirname(NUIT_HEALTH_PATH), exist_ok=True)
            tmp = NUIT_HEALTH_PATH + ".tmp"
            with open(tmp, "w") as f:
                json.dump(verdict, f, separators=(",", ":"))
            os.replace(tmp, NUIT_HEALTH_PATH)
        except Exception as e:
            return self._json(500, {"ok": False, "error": "write failed: %s" % e})
        log.info("health_ingest: overall=%s targets=%s", overall, list(verdict["targets"].keys()))
        return self._json(200, {"ok": True, **verdict})

    # ── MONITOR status ingest (PUSH from the Nuit watchdog) ──────────────────
    # Stores the latest per-watcher live state + recent-alerts feed for the
    # Monitoring tab. Not a money/order route — display only. (Operator-authorized 2026-07-12.)
    def _handle_monitor_ingest(self):
        b = self._read_json_body()
        watchers = b.get("watchers")
        if not isinstance(watchers, dict):
            return self._json(400, {"ok": False, "error": "watchers must be an object"})
        _now = int(time.time())
        doc = {"watchers": watchers,
               "recent_alerts": b.get("recent_alerts") if isinstance(b.get("recent_alerts"), list) else [],
               "pushed_ts": float(b.get("pushed_ts") or _now), "received_ts": _now, "wired": True}
        # ... (atomic write to state file, same pattern as _handle_health_ingest above)
