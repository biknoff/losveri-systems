// Excerpt from ear/Sources/HanumanEar/main.swift — the real-time energy
// gate (the pipeline's actual VAD today) and the post-transcription
// Whisper-hallucination filter. Verbatim from source.

static let rmsThreshold: Float = 0.008
static let hallucinationBlacklist: Set<String> = [
    "", ".", "-", "?", "!", "♪", "♫",
    "okay.", "okay", "ok.", "ok",
    "you.", "you",
    "thanks for watching.", "thanks for watching!",
    "thank you.", "thank you",
    "bye.", "bye", "bye-bye.",
    "yeah.", "yeah", "yes.", "yes",
    "right.", "right", "all right.",
    "oh.", "oh", "oh my goodness.",
    "whoa.", "whoa", "hmm.", "hmm",
    "mm-hmm.", "mm.", "uh-huh.",
    "that's right.", "transmits.",
    ".."
]

static func isHallucination(_ text: String) -> Bool {
    let lower = text.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
    if lower.isEmpty { return true }
    if hallucinationBlacklist.contains(lower) { return true }
    let stripped = lower.unicodeScalars.filter { CharacterSet.alphanumerics.contains($0) }
    if stripped.count < 3 { return true }
    return false
}

static func computeRMS(_ samples: [Float]) -> Float {
    guard !samples.isEmpty else { return 0 }
    var sumSq: Float = 0
    for s in samples { sumSq += s * s }
    return (sumSq / Float(samples.count)).squareRoot()
}

// Call site, inside processAudioChunk(_:whisperKit:socketManager:audioDirectory:debug:):
//
//   let rms = Self.computeRMS(audio)
//   if rms < Self.rmsThreshold {
//       if debug { print("[vad] skip (rms=\(String(format: "%.4f", rms)))") }
//       return
//   }
