# Architecture — Hanuman

## Scope

Two independent subsystems live under one house: the **comms gate** (MCP server for WhatsApp + a Gmail SMTP skill) and the **voice pipeline** (local speech-to-text + speaker ID). They share nothing at runtime — the gate is I/O-bound and network-facing, the voice pipeline is on-device and audio-facing — but both exist for the same reason: give every other agent a channel to the world without each one re-implementing it.

## The comms gate

`whatsapp-mcp` (`whatsapp-baileys-ts`) is a single Node/TypeScript MCP server (`@modelcontextprotocol/sdk`) wrapping `@whiskeysockets/baileys`, an unofficial WhatsApp Web protocol library, plus a local SQLite cache of chats/contacts/messages (`data/whatsapp.db`) for fast search. It exposes eight tools over MCP — `search_contacts`, `list_messages`, `list_chats`, `get_chat`, `get_message_context`, `send_message`, `send_document`, `search_messages` — each a thin, domain-agnostic wrapper: JID/text/file in, WhatsApp API call out. No tool encodes who a contact is or why a message is being sent.

Any agent whose session mounts Hanuman's `.mcp.json` entry inherits all eight tools automatically — that's the "one server, many consumers" design (see `README.md`'s diagram: Fred, Chris, Fay, Abraxas all call the same `send_message`). When an agent session doesn't have the MCP tool mounted, the fallback is still Hanuman's own repo — `npx tsx send_whatsapp_once.ts` inside `whatsapp-mcp/` — never a second implementation. Two separate SKILL.md files (one in `whatsapp-mcp/`, one in `skills/send-whatsapp-via-hanuman/`) both encode this as a hard rule.

Gmail works the same way at a smaller scale: `skills/send-gmail/send_gmail.py` is a single SMTP-TLS sender any agent can shell out to, credential resolved from one canonical file rather than per-agent secrets.

Session authentication (`whatsapp-mcp/auth_info/`) is a single WhatsApp Web pairing, scanned once; every consumer rides that one session. This is the same tradeoff as any shared-credential gate: one thing to protect, one thing that can go down for everyone.

## The voice pipeline

Two processes, split by language for the right reason: Swift/CoreML for on-Neural-Engine ML inference (`ear/`), Python for orchestration and lighter models (`brain/`).

- **`ear/` (Swift, `HanumanEar`)** — `AVAudioEngine` taps the mic, converts to 16kHz mono Float32, buffers into ~2s chunks, and runs each chunk through **WhisperKit** at the **`large-v3-turbo`** model (confirmed in `Package.swift`'s dependency on `argmaxinc/WhisperKit` and instantiated by name in `main.swift`). Before a chunk reaches Whisper it passes an RMS energy gate (`rmsThreshold: 0.008`) that skips near-silent audio — this is the pipeline's actual voice-activity gate today, implemented as a simple energy threshold, not (per the files on disk) a Silero VAD model. After transcription, a hallucination filter drops known Whisper artifacts (`"thanks for watching."`, bare punctuation, sub-3-character output) — a real, non-trivial cleanup step Whisper users generally need and this pipeline implements.
- **Echo/AEC**: `config/hanuman.yaml` declares `system_aec: true` (CoreAudio-level echo cancellation) and `embedding_exclusion: true` (drop transcript segments matching the system's own enrolled voice), plus a `tail_ms` gate after TTS playback. `brain/voice.py`'s TTS layer explicitly signals an "echo gate ON/OFF" over a control socket around every spoken response — the coordination contract these config flags describe is implemented at the signaling level; whether `AVAudioEngine`'s tap alone yields full hardware AEC (vs. requiring `AVAudioSession`'s voice-processing I/O) is not something the current `main.swift` demonstrates directly.
- **Speaker identification** is a separate, working pipeline: `brain/speaker_id.py` loads an ECAPA-TDNN model (`speechbrain/spkrec-ecapa-voxceleb`) and compares embeddings against `enrollment/embeddings.json`, built from two real enrolled voice samples (`operator_a.wav`, `operator_b.wav`). Real session logs (`logs/sessions/*.jsonl`) show this running end-to-end: timestamped, per-segment records carrying `speaker`, `speaker_confidence`, and `language` fields (message text withheld here — see EVIDENCE for the redaction note).
- **`brain/daemon.py` + `brain/router.py`** consume the `ear` daemon's Unix-socket JSON-lines output and dispatch qualifying transcripts to Claude Code sub-agents, capped at `max_concurrent_agents`.

## Why this split holds

The comms gate is a thin, stateless-per-call protocol wrapper — its entire job is to *not* know anything domain-specific, so that many callers can share it safely. The voice pipeline is the opposite: it's allowed to be stateful and specific (it knows two enrolled speakers by name) because it serves one purpose — turning speech in this house into text and identity, for whichever downstream agent the brain's router decides should see it.
