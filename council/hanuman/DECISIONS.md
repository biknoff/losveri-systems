# Decisions — Hanuman

Each entry: the choice made, and the alternative considered and rejected.

## 1. One comms gate all agents share
**Chosen:** a single MCP server (`whatsapp-mcp`) and a single Gmail SMTP skill, both mounted or invoked by every agent that needs to send a message — Fred, Chris, Fay, Abraxas.
**Rejected:** every agent owning its own WhatsApp session or SMTP credential. That multiplies the number of live sessions to protect and re-pair, multiplies the code that has to get JID handling and rate limits right, and turns "is WhatsApp working" into an N-agent question instead of a one-server question. Two independent SKILL.md files encode this as policy, not just convenience: agents are told explicitly not to build a second transport even when the MCP tool isn't mounted in their current session — fall back to Hanuman's own repo, not a new implementation.

## 2. Baileys (unofficial protocol library) over the official WhatsApp Business API
**Chosen:** `@whiskeysockets/baileys`, a reverse-engineered WhatsApp Web client.
**Rejected:** the official WhatsApp Business Cloud API. The official path requires a Meta Business/App Review process and a phone number provisioned specifically for the integration — friction disproportionate to a personal/family messaging need. Baileys pairs like a second linked device via QR scan, no approval process. The honest cost, stated plainly rather than hidden: it's an unofficial library riding WhatsApp's undocumented protocol, which can break on WhatsApp's end without notice.

## 3. Domain-agnostic tool surface
**Chosen:** MCP tools that take a JID and text/file — no concept of "household staff," "contacts I'm allowed to message," or message categories inside the tool implementations.
**Rejected:** baking per-agent authorization or content rules into the transport layer. That would mean the gate has to be re-taught every time a new consumer (a new house) is added, and it blurs the one line this repo depends on: Hanuman moves messages, callers decide what and to whom.

## 4. RMS energy gate before a heavier VAD model
**Chosen:** a simple `rmsThreshold` computed per audio chunk, run in Swift before the chunk ever reaches WhisperKit.
**Rejected (so far):** a learned VAD model (e.g., Silero) in the hot path. The energy gate is cheap, has zero model-loading cost, and — combined with the post-transcription hallucination blacklist — catches the two failure modes that matter most (silence triggering a Whisper hallucination, and Whisper's well-known short-utterance artifacts). A learned VAD is a plausible next step, not yet what's built.

## 5. Split the voice pipeline across two languages/processes
**Chosen:** Swift/CoreML (`ear/`) for the ML-inference hot path (WhisperKit on the Neural Engine), Python (`brain/`) for orchestration, speaker-ID, and dispatch.
**Rejected:** one process in one language. WhisperKit's ANE acceleration is a Swift/CoreML capability; the dispatch and speaker-ID tooling (speechbrain, Claude Code CLI invocation) is far more natural in Python. Splitting cleanly at the Unix-socket boundary keeps each half small and lets either be replaced without touching the other.

## 6. Config declares the AEC/echo design explicitly, even before it's fully proven out
**Chosen:** `config/hanuman.yaml` states the intended echo-cancellation behavior (`system_aec`, `embedding_exclusion`, `tail_ms`) as first-class, named settings, and `brain/voice.py` implements the echo-gate signaling contract around every TTS turn.
**Rejected:** leaving AEC as an implicit assumption or an ad hoc sleep-and-hope around playback. Naming the mechanism in config, even where the underlying hardware-AEC guarantee isn't independently verified from the Swift code alone, keeps the intended architecture legible and auditable rather than folklore.
