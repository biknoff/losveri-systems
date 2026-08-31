# EVIDENCE: running archives (backstop + wake reports)

What: directory listings only (file counts + date-range sample) of the backstop and wake-report
archive directories on the research host, captured 2026-08-31. Redacted: report *contents* are
never shown here — these directories hold trade data, so only existence and filenames (which
carry timestamps, nothing else) are cited, per the task's redaction rule.

## `backstop_runs/` — one archive per 3h backstop cycle

192 files present, including `latest.md` (a rolling pointer) and 191 dated `wake_<UTC
timestamp>.md` archives. Earliest sampled: `wake_20260808T175315Z.md`. The archive is
self-pruned to the most recent 200 runs by the backstop script itself (visible in
`backstop_run.sh`'s own source, not re-quoted here). 192 archived runs at roughly one every 3
hours is consistent with continuous operation since the 2026-08-08 re-arm date in the crontab
header.

## `WAKE_REPORTS/` — dated wake-report snapshots

258 files present, filenames of the form `wake_<date>_<time>ET.md`. Earliest sampled:
`wake_20260802_1818ET.md`. This directory is described in the source project inventory as
"still being written" as of the capture date — an actively growing record, not a stale or
one-time artifact.

Neither directory's contents (trade detail, report bodies) are excerpted anywhere in this
project.
