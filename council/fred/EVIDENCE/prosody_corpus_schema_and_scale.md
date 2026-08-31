# Evidence: the prosody corpus — real schema depth, redacted values

**What this is:** structural inspection (file counts, field names, one full-schema example with
every value replaced by a placeholder) of `Fred's Corpus/Source Material/`, the directory the bot
line's Phase 2 affective pass writes into. This is corpus *output* evidence — the bot's per-note
affect artifact — distinct from the detector's own within-person baseline computation (already
covered in [`detector_feature_extraction_and_baseline_design.md`](detector_feature_extraction_and_baseline_design.md)
and [`../SNIPPETS/feature_extraction_and_baseline_shape.py`](../SNIPPETS/feature_extraction_and_baseline_shape.py)).
Stated precisely so the two are not conflated, per this repo's own rule.

**Redaction discipline:** every `score`, every `emotion`/date pairing, and every acoustic
measurement below is a placeholder (`0.NN`, `N`). Nothing in this file is a real value from a real
recording of a real person on a real date. Field *names* are schema, not content, and are shown
verbatim because a schema is not personal data.

## Scale

- **391** `prosody_summary.json` files under `Fred's Corpus/Source Material/`, confirmed by direct
  count (`find ... -name prosody_summary.json | wc -l`).
- **57** dated batch folders (e.g. `fred_20260415_095505_mariele_evening_20260413`,
  `critical_20260320_234622_truly_difficult_conversation`) — batch-folder naming embeds both a
  processing timestamp and a source-date label.
- File `mtime` range across the corpus: **2026-03-17 to 2026-04-15** — a one-month window, not the
  full operating span of the bot line. This is corroborating, not contradicting, evidence for the
  existing repo claim that the detector's *scoring* side has been dormant since its 2026-04-10
  validation event; this corpus is the batch of source material gathered around that event, not a
  continuously updated feed. (No file with this name was found dated after mid-April in this
  directory — a live *ingestion* channel, if one still runs, was not located under this path in
  this pass.)

## Real schema, placeholder values

Every `prosody_summary.json` file inspected shares this shape (confirmed across multiple files
from different dates):

```json
{
  "segment_count": 1,
  "top_average_emotions": [
    {"emotion": "Boredom", "score": 0.NN},
    {"emotion": "Sadness", "score": 0.NN},
    {"emotion": "Tiredness", "score": 0.NN},
    {"emotion": "Fear", "score": 0.NN},
    {"emotion": "Anxiety", "score": 0.NN},
    {"emotion": "Distress", "score": 0.NN},
    {"emotion": "Calmness", "score": 0.NN},
    {"emotion": "Anger", "score": 0.NN},
    {"emotion": "Surprise", "score": 0.NN},
    {"emotion": "Excitement", "score": 0.NN}
  ],
  "peak_moments": [
    {
      "begin": 0.0,
      "end": 0.0,
      "text": "",
      "emotions": [
        {"emotion": "Boredom", "score": 0.NN},
        {"emotion": "Sadness", "score": 0.NN}
      ]
    }
  ],
  "features": {
    "sample_rate": 16000,
    "sample_count": 0,
    "duration_seconds": 0.0,
    "voiced_ratio": 0.0,
    "average_rms": 0.0,
    "rms_stdev": 0.0,
    "average_zcr": 0.0,
    "average_peak": 0.0,
    "pitch_stdev_hz": 0.0,
    "silence_threshold": 0.0,
    "overall_peak": 0.0,
    "estimated_pitch_hz": null,
    "average_voiced_span_seconds": 0.0,
    "max_voiced_span_seconds": 0.0,
    "long_voiced_span_ratio": 0.0,
    "voiced_spans": [],
    "windows": [
      {"window_index": 0, "begin_seconds": 0.0, "end_seconds": 0.0,
       "rms": 0.0, "peak": 0.0, "zcr": 0.0, "pitch_hz": null, "voiced": false}
    ],
    "vocal_mode": "",
    "vocal_mode_confidence": 0.0,
    "vocal_mode_reasons": []
  }
}
```

## What this schema actually shows

Two distinct measurement layers live in the same file, and they are worth naming precisely rather
than folding into one "prosody" claim:

1. **`top_average_emotions` / `peak_moments`** — a ten-dimension named-emotion vector (Hume-
   lineage schema: population-model emotion labels with continuous scores) plus time-localized
   `peak_moments`, each with `begin`/`end` timestamps and its own top-emotion sublist. This is a
   *segment-and-peak* structure, not a single scalar score per note — it is built to answer "when,
   within this note, did the signal peak" as well as "what was the note's average."
2. **`features`** — a lower-level, self-contained acoustic layer computed per note: RMS/peak/ZCR
   energy statistics, a windowed time series (`windows`, one entry per sub-segment with its own
   RMS/peak/ZCR/pitch), a `voiced_ratio` and voiced-span structure, and a classified `vocal_mode`
   with a confidence and reason list. This is a simpler, purpose-built acoustic layer distinct from
   the openSMILE eGeMAPSv02 functional set the *detector's own* baseline builder consumes (see the
   evidence and snippet cited above) — same household, same audio pipeline, but not the same
   feature set, and this file does not claim otherwise.

The corpus is real, dated, structurally rich per-file output, at real scale (391 files); the
redaction rule above holds regardless of how impressive the shape is.
