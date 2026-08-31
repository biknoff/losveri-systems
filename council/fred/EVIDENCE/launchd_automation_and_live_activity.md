# Evidence: launchd automation + live-activity trail (bot line is RUNNING)

**What this is:** read-only SSH inspection (`launchctl list`, `cat` on plist files — OS config, not
personal data — and log-file `tail`/`stat`) of the four launchd jobs that make up the bot line's
always-on automation, plus the operational evidence that they are actually firing, not just
installed.

**Redactions:** log lines shown are operational metadata only — timestamps and `N processed`/error
counts. No transcript content, no audio, no message text, no names beyond "Leo"/"Mariele" (already
named elsewhere in this repo) appear below.

## Four jobs, four different triggers

| Label | Trigger | What it runs |
|---|---|---|
| `com.losveri.fred-voicememo-watcher` | `WatchPaths` on the real macOS Voice Memos recordings folder | `tools/fred_voicememo_oneshot.py` — one-shot processing pass per new recording |
| `com.losveri.fred-kubera-bot` | `RunAtLoad` + `KeepAlive` (restarts on crash, not on clean exit) | `poll_runner.py` — the **local polling copy** of the Telegram bot itself |
| `com.leo.fredsync` | `StartInterval` = 30s | a sync script |
| `com.losveri.fred-colossus-bridge-temp` | `StartInterval` = 60s | an inbox-bridge script, `--limit 5` |

`com.losveri.fred-voicememo-watcher` (verbatim plist, paths already public elsewhere in this repo):

```xml
<key>ProgramArguments</key>
<array>
    <string>/Users/leo/Los Veri/1st House - Fred Beta/venv/bin/python</string>
    <string>-u</string>
    <string>/Users/leo/Los Veri/tools/fred_voicememo_oneshot.py</string>
</array>
<key>WatchPaths</key>
<array>
    <string>/Users/leo/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>ThrottleInterval</key>
<integer>5</integer>
```

`WatchPaths` on the *actual* OS-level Voice Memos recordings directory (not a custom drop folder)
means this agent is wired directly into the same folder the Voice Memos app itself writes to —
event-driven, not polled, and with a 5s throttle to coalesce filesystem-event bursts from a single
recording.

`com.losveri.fred-kubera-bot`'s own docstring (verbatim) states its role precisely:

```
poll_runner.py — Local polling runner for Fred + Kubera handler.
...
This is the LaunchAgent entry point. It does NOT start Flask.
Cloud Run runs the Flask webhook; this runs the local polling copy.
The webhook must be deleted before this is started (Path W protocol).
```

So there are, by design, two live deployment modes for the same bot (a Cloud Run webhook and a
local long-running poller under `KeepAlive`), with an explicit protocol for not running both
against Telegram at once.

## Currently loaded, right now (`launchctl list`)

```
PID    LastExitStatus  Label
80574  1               com.losveri.fred-colossus-bridge-temp
582    0               com.losveri.fred-kubera-bot
-      78              com.leo.fredsync
-      0                com.losveri.fred-voicememo-watcher
```

A live PID for `fred-kubera-bot` (the local bot poller) means the process is running at the moment
of this check, not just registered. `fred-voicememo-watcher` shows no PID because it is
event-driven (`WatchPaths`) — no PID between triggers is the expected, correct resting state for
that job, not evidence of inactivity.

## The watcher log shows real, recent fires

`fred_v2_watcher_stdout.log` (2.5MB) — tail, dated entries through **2026-08-24**:

```
[2026-08-24 15:24:37] Voice memo one-shot triggered
[2026-08-24 15:24:38] One-shot complete: 0 processed
[2026-08-24 15:26:05] Voice memo one-shot triggered
[2026-08-24 15:26:05] One-shot complete: 0 processed
```

Stated plainly, not spun: the watcher fired and completed cleanly. Most recent entries in this log
report `0 processed` — the trigger fired (the OS event reached the script and the script ran to
completion) but found nothing new to process at that moment. That is a live, armed watcher, not
constant fresh output; both things are true at once and neither should be inferred from the other.

## The local bot poller's own log is more recent than the watcher's

`~/Library/Logs/fred_kubera_bot.out.log` — 3.3MB, **last modified 2026-08-30 21:12** (the day
before this evidence was gathered):

```
2026-08-29 21:11:58 - ERROR - No error handlers are registered, logging exception.
2026-08-30 20:18:32 - ERROR - No error handlers are registered, logging exception.
2026-08-30 21:12:04 - ERROR - No error handlers are registered, logging exception.
2026-08-30 21:12:13 - ERROR - No error handlers are registered, logging exception.
```

Stated as-is: the local poller is alive and actively logging as of the day before this check, but
its most recent activity in this log is a recurring, unhandled exception (its own `python-telegram-
bot` `Application` has no error handler registered) rather than a clean success line — the
`err.log` in the same directory also shows a `telegram.error.NetworkError: Bad Gateway` from
`get_updates`. This is presented as what it is: the process is running and reaching Telegram's API
often enough to hit network errors, not proof that user-facing replies are currently succeeding.
It is additional evidence of liveness, held to a lower confidence bar than the watcher's clean
completions above — treat the watcher log as the primary RUNNING evidence and this as corroborating
context.
