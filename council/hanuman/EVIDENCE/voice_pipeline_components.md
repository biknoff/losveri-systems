# Voice pipeline — what's on disk, verified component by component

**What this is:** a direct, file-by-file check of the claimed voice-pipeline components (CoreAudio AEC, VAD, WhisperKit large-v3-turbo, echo handling, speaker ID), so the README's claims are traceable to what's actually in the repo rather than restated from the operator's own notes.

**Redactions:** transcript **text** fields from `logs/sessions/*.jsonl` are withheld (spoken content); timestamps, speaker labels, confidence scores, and language fields are kept as they are not personal content.

---

### WhisperKit `large-v3-turbo` — confirmed
`ear/Package.swift` declares a dependency on `argmaxinc/WhisperKit` (`from: "0.9.0"`). `ear/Sources/HanumanEar/main.swift` instantiates it by name:

```swift
var model: String = "large-v3-turbo"
...
let whisperKit = try await WhisperKit(model: model, verbose: debug, prewarm: true)
```

`config/hanuman.yaml`'s `ear.model` setting agrees (`"large-v3-turbo"`). This is a real, on-device CoreML model dependency, not a description of an aspiration.

### Voice-activity detection — RMS gate, not Silero
The code implements an energy-threshold gate:

```swift
static let rmsThreshold: Float = 0.008
...
let rms = Self.computeRMS(audio)
if rms < Self.rmsThreshold { return }  // skip near-silent chunk
```

No reference to Silero (or any learned VAD model) appears anywhere in `ear/`, `brain/`, or `config/` outside this repo's `main.swift.bak` (an older revision, same RMS-based approach). Stated plainly: the current build's VAD is a simple RMS energy gate, not a Silero model — the operator's own atlas describes the intended/marketed stack; this repo's code implements a simpler version of the "VAD" piece today.

### CoreAudio AEC — configured, signaling implemented, hardware layer not independently verified from Swift alone
`config/hanuman.yaml`:
```yaml
echo:
  tail_ms: 200
  embedding_exclusion: true
  system_aec: true
```
`brain/voice.py` implements the coordination half of this explicitly — it sends `ECHO_GATE_ON` before TTS playback and `ECHO_GATE_OFF` (after a buffer) when done, over a Unix control socket the `ear` daemon listens on (`--control-socket` flag in `main.swift`). What is confirmed: the echo-gate signaling protocol between TTS and the transcription daemon is real and implemented on both sides. What is not independently confirmed from `main.swift`: whether the audio tap itself (`AVAudioEngine.inputNode`) is configured for full hardware voice-processing AEC, versus relying on the gate/exclusion logic alone during TTS playback.

### Speaker identification — a real, separate, working pipeline
`brain/speaker_id.py` loads `speechbrain/spkrec-ecapa-voxceleb` (ECAPA-TDNN) and compares against `enrollment/embeddings.json`. Two real enrollment recordings exist on disk (`enrollment/leo.wav`, 8.9MB; `enrollment/mariele.wav`, 10.7MB). A real session log (`logs/sessions/2026-04-15_153833.jsonl`) shows the pipeline producing structured output:

```json
{"ts": 1776281913.6, "ts_end": 1776281915.6, "speaker": "leo", "speaker_confidence": 0.99999988, "language": "es", ...}
```
(message text withheld)

`main.swift` itself still marks per-utterance diarization as `"speaker": "unknown", // TODO: SpeakerKit diarization (Phase 1.5)` — meaning the Swift daemon's own inline field is a placeholder, while the separate Python `speaker_id.py` module is the pipeline that's actually verified doing real speaker identification against real enrollment data.

### Session-log volume, as evidence of real (not staged) runs
Six session-log files under `logs/sessions/`, ranging 0–153 lines each, spanning a single day (2026-04-15) — consistent with iterative real testing during active development, not a single scripted demo run.
