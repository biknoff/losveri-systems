# Evidence: bot v6.3.8 header + two-phase design

**What this is:** the literal top-of-file header and changelog from the production Telegram bot
entry point (`fred_bot_cloud_integration.py`), plus the timing-target constants that encode its
two-phase response architecture. Read via read-only SSH against the source machine, quoted
verbatim except where noted.

**Redactions:** none needed in this excerpt — no audio paths, no personal values, no credentials.
A Telegram bot-token/greeting line further down the file (not shown) was excluded because it
formats a chat ID; nothing about it is quoted here.

## Header + changelog (verbatim, top of file)

```python
# Fred Bot v6.3.8 - Progressive Response Architecture (Sheets)
# CHANGELOG v6.3.8:
# - Phase 0: ACK inmediato (<1s) before any heavy processing
# - Phase 1: Transcribe + Parse + Execute expenses in parallel
# - Phase 2: Hume runs in background, only awaited for conversational
# - Expense confirmation sent BEFORE Fred's emotional response
```

## Phase timing targets (verbatim, top of file)

```python
# ============ TIMING TARGETS ============
PHASE0_TARGET_MS = 1000   # ACK should be sent within 1s
PHASE1_TARGET_MS = 5000   # Expense confirmation within 5s
PHASE2_TARGET_MS = 15000  # Emotional response within 15s
HUME_TIMEOUT_SECONDS = 30 # Max wait for Hume before continuing
```

## Reading

The changelog *is* the architecture statement: Phase 0 acknowledges receipt of a voice note in
under a second; Phase 1 transcribes and executes the fast, deterministic path (expense parsing)
in parallel, target 5s; Phase 2 runs the (then-Hume) affective pass in the background and is only
awaited when the response is conversational — the user gets their fast confirmation before Fred's
"emotional" reply arrives. This is the "voice-note bot line" referenced throughout this directory:
lineage-tagged v6.3.8, Hume-era, later migrated (see
[`migration_trail_and_cloud_hosting.md`](migration_trail_and_cloud_hosting.md)).

`config.py` in the same directory still carries `HUME_TIMEOUT_SECONDS` and imports consistent
with the Hume SDK (`from hume import HumeClient`, `# Note: Prosody/Models classes removed in SDK
v0.9+` — a comment documenting a real SDK-version adaptation, left in place as lineage evidence
rather than scrubbed).

**Status confirmed by this file:** the bot's own startup log line and Telegram greeting both
self-report `v6.3.8`, matching the operator's stated version — this is the bot code as it stands
today, RUNNING (see [`launchd_automation_and_live_activity.md`](launchd_automation_and_live_activity.md)
for the live-process evidence), not a stale artifact.
