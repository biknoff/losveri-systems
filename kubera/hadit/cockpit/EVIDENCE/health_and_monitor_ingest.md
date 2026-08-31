<!-- What: description + evidence that the NUIT watcher fleet and equity watchdog actively PUSH
     their state into the cockpit over dedicated endpoints, rather than the cockpit polling for it.
     Redacted: none in this description; see SNIPPETS/health_ingest_handler.py for the actual code
     (also unredacted — no identifiers/secrets in this handler). -->

Two endpoints exist specifically for real-time safety state, distinct from the 27 pull-based
generator panels:

- **`_handle_health_ingest`** — receives `{overall, targets{cockpit,engine,recorder,gateway}, ts}`
  from the NUIT health checker; validates `overall` is one of `live|degraded|system_down`, writes
  atomically (temp file + `os.replace`), and logs the ingest.
- **`_handle_monitor_ingest`** — receives `{watchers: {...}, recent_alerts: [...], pushed_ts}` from
  the equity watchdog / watcher fleet; feeds the Monitoring tab directly.

Both handlers carry an explicit in-source note that they are display-only, not order-path, each
with a date and the authorizing operator's name — see `SNIPPETS/health_ingest_handler.py` for the
verbatim comment. This is the concrete integration point between the
[watchers project](../../nuit/watchers/) and this cockpit: the same processes documented there are
what the Monitoring tab actually displays, not a parallel or re-implemented status check.
