# Excerpt from backstop_run.sh — the 3h backstop's alert gate. Telegrams
# fire on exactly two conditions (timeout, crash) or a third computed one
# (sha drift, deduped so a standing/authorized change doesn't re-page every
# cycle); every other run of this script is silent by design — the archive
# file is the record, the telegram is reserved.
# Redacted: the live-sha-matching regex and dedup file paths are shown
# structurally; no actual sha values appear (see EVIDENCE/cron_durable_layer.md
# for why: <sha> replaces the real baseline value throughout this project).

timeout 150 python3 /home/nuit/wake_report.py > "$OUT" 2>&1
rc=$?
cp "$OUT" "$LEDGER/latest.md" 2>/dev/null

# prune archive to last 200 runs
ls -1t "$LEDGER"/wake_*.md 2>/dev/null | tail -n +201 | xargs -r rm -f

LIVE_SHA=$(grep -oE 'sha `[0-9a-f]{16}`' "$OUT" | head -1 | grep -oE '[0-9a-f]{16}' | head -1)
LAST=/home/nuit/for_the_record/.backstop_last_alerted_sha

alert=""
if [ $rc -eq 124 ]; then
  alert="BACKSTOP: wake_report TIMED OUT (>150s) at ${TS} — execution-host read may be hung"
elif [ $rc -ne 0 ]; then
  alert="BACKSTOP: wake_report CRASHED rc=${rc} at ${TS} (see ${OUT})"
elif grep -qi "CHANGED\*\* from last known baseline" "$OUT"; then
  # sha drift. dedup on the drifted sha so a standing/authorized change does
  # not re-page every 3h cycle.
  if [ -n "${LIVE_SHA}" ] && [ "${LIVE_SHA}" != "$(cat "$LAST" 2>/dev/null)" ]; then
    alert="BACKSTOP: live sha drifted to ${LIVE_SHA}"
  fi
fi
# alert="" (the default / healthy path) sends nothing at all.
