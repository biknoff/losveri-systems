# Source: 1st House - Fred/fred_bot_cloud_integration.py (top of file, verbatim)
# Real production entry point for the Telegram voice-note bot line.
# Shown here: the version header, changelog, and the timing-target constants
# that encode the progressive two-phase response design. No handler bodies,
# no chat IDs, no audio paths.

# Fred Bot v6.3.8 - Progressive Response Architecture (Sheets)
# CHANGELOG v6.3.8:
# - Phase 0: ACK inmediato (<1s) before any heavy processing
# - Phase 1: Transcribe + Parse + Execute expenses in parallel
# - Phase 2: Hume runs in background, only awaited for conversational
# - Expense confirmation sent BEFORE Fred's emotional response

# ============ TIMING TARGETS ============
PHASE0_TARGET_MS = 1000   # ACK should be sent within 1s
PHASE1_TARGET_MS = 5000   # Expense confirmation within 5s
PHASE2_TARGET_MS = 15000  # Emotional response within 15s
HUME_TIMEOUT_SECONDS = 30 # Max wait for Hume before continuing

# Reading: Phase 0 acknowledges the voice note fast. Phase 1 runs the
# deterministic, fast path (transcribe + parse + execute an expense) and
# returns before the affective pass is even awaited. Phase 2 is the
# (then-Hume, later-migrated) prosody/affect pass, backgrounded and only
# blocked on when the reply is conversational rather than transactional.
# The user's fast confirmation never waits on the slow, probabilistic call.
