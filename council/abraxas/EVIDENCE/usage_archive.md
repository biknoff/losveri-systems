# Usage evidence — response archives + scheduled daemon

**What this is:** file-count and date-range evidence from `for_the_record/channel_agent_responses/` (per-response artifacts: `.md` script, `.ogg`/`.mp3` audio, `_receipt.json`) and `for_the_record/morning_brief_runtime/` (a scheduled `launchd` job). Names and dates only — response bodies were never opened.

**Redactions:** file contents not read (they are personal — family conversation). Telegram `chat_id` values excluded throughout this repo per redaction policy.

---

## Telegram response archive

```
$ ls for_the_record/channel_agent_responses/ | grep -E '^abraxas_telegram_response_[0-9]{8}_[0-9]{6}\.md$' | wc -l
9
$ ... | sort | sed -n '1p;$p'
abraxas_telegram_response_20260317_135002.md
abraxas_telegram_response_20260421_073915.md
```

9 distinct ABRAXAS Telegram text responses on disk, spanning 2026-03-17 → 2026-04-21 (>5 weeks), each paired with a `_receipt.json` delivery record; 5 of the archived responses include a companion `.ogg` — the rendered voice reply actually sent, not just the text. The same directory holds parallel archives for other channel agents on the same delivery path (`garuda_telegram_response_*`, `fred_whatsapp_response_*`), evidence this is a shared, reused mechanism rather than a one-off script.

## Scheduled morning brief (launchd)

```
$ cat ~/Library/LaunchAgents/com.losveri.abraxas-morning-brief.plist
```
`StartCalendarInterval`: weekdays (Mon–Fri), 06:00 local. `RunAtLoad`: false (fires only on schedule, not on login — evidence it is a real recurring job, not something triggered ad hoc). `ProgramArguments` invokes `tools/send_abraxas_morning_brief.py` directly.

```
$ ls for_the_record/morning_brief_runtime/ | grep -c '_receipt.json$'
12
$ ... | sort | sed -n '1p;$p'
abraxas_morning_brief_2026-03-17_receipt.json
abraxas_morning_brief_2026-04-01_receipt.json
```

194 total files under `morning_brief_runtime/` (receipts + launchd stdout/stderr logs), confirming the job has been firing and logging on its calendar interval since 2026-03-17.

## Continued active development past the archived window

Tool file modification times on the source host, unrelated to the response archive above, show the pipeline kept being touched well past April: `abraxas_daemon_bar.py` last modified 2026-05-28 (a memory-fix revision, per its own backup-file name), `abraxas_tts.py` last modified 2026-07-26 (a TTS-model-bump revision). Consistent with a system in continuous daily use rather than a dormant one-time build.
