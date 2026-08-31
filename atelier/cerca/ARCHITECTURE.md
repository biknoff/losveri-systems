# CERCA — Architecture

## 1. The four bodies + the Faraday-reference floor

Four participants stand on a performance floor wired as a Faraday
reference plane. That reference is what lets the instrument treat every
reading as conductance *between two specific bodies* rather than picking
up capacitive noise from the room, the building's wiring, or nearby
electronics — the floor is the instrument's ground truth. Each
participant wears or holds a pair of custom conductive headphones. The
headphones are wired to do two jobs at once: they are the electrode that
makes skin contact for sensing, and they are the audio-return path that
carries the generated sound back to that same participant. (Evidence:
`EVIDENCE/cerca_photo_1.jpg`, `EVIDENCE/cerca_photo_2.jpg`.)

## 2. Beacon coding

Each of the 4 participants has one analog sensing pin and one digital
"beacon" emitter pin on the Arduino (`aPin[0..3]`, `dPin[0..3]` in
`CercaV7.0.ino`). The emitters take turns: `driveLOW → driveHIGH (8µs) →
driveLOW → hi-Z`, inside a fixed 300µs window (`BEACON_US`), followed by a
400µs settle before the next emitter's turn. While one body's pin beacons,
all 4 sensing channels listen — so a single scan cycle produces a full 4×4
matrix of readings (each emitter against each listener), not just one
number per body. This turn-taking, prime-number-coded pulse pattern is
what disambiguates *which* pair of bodies is actually in electrical
contact when more than one pair touches at once — see
[DECISIONS.md](DECISIONS.md).

## 3. Cleaning the signal

Each of the 16 raw per-cycle readings goes through the same chain:

1. **FIR** (order 4) — a short moving-average to knock down sample-level
   noise.
2. **IIR** (`ALPHA = 0.6`) — a slower low-pass to smooth the FIR output.
3. **Adaptive notch filter** (diagonal/self channels only) — an FFT
   (16-point) runs every 20 cycles, finds the dominant frequency in each
   self-channel if it stands well above the noise floor (`peak > 3 ×
   median`), and tunes a biquad notch onto it. This is how the instrument
   rejects mains hum or other periodic environmental noise without a fixed
   notch frequency.
4. **Attack/release smoothing** — asymmetric coefficients (`ATTACK =
   0.50`, `RELEASE = 0.75`) so a touch registers quickly but a release
   decays more gradually, avoiding visual/audio flicker at the threshold.
5. **Dynamic baseline** — while a self-channel reads quiet (below
   `QUIET_THRESHOLD`), its baseline drifts slowly toward the current value
   (`BASE_IIR_COEF = 0.005`), so the instrument re-centers on room/skin
   drift between performances without a manual re-cal.

Firmware also auto-calibrates each channel's raw offset over its first 50
loops, blending the window's max and average (`RAW_CAL_TILT`) — a rough
per-session leveling before the show starts. (Full excerpt:
`EVIDENCE/firmware_excerpt_CercaV7.0.ino.txt`.)

## 4. The 6-pair + 4-self conductance matrix

From the cleaned 4×4 grid, the firmware folds the readings down using a
fixed pair map (`Pmap = {0,1} {0,2} {0,3} {1,2} {1,3} {2,3}`) — the 6
unique unordered pairs among 4 people. Each pair's value is the average of
its two directions (emitter-A→listener-B and emitter-B→listener-A) minus
the relevant baseline, gain-scaled per pair, and glitch-guarded (a jump
bigger than `GLITCH_STEP` in one cycle is rejected as noise, not motion).
The 4 self/diagonal channels (each body against itself, via the
adaptive-notch path) are read alongside the 6 pairs. Together that is the
"exactly 10 columns" the firmware header documents — 6 pairs + 4 selves —
streamed out over serial every cycle.

## 5. Gesture grammar and output

The 10-channel stream (6 pair-conductances + 4 self-conductances) is the
input alphabet to a 49-form confidence-scored gesture grammar: each
recognized touch configuration among the 4 bodies — who's touching whom,
how strongly, how many pairs at once — maps to one of 49 gesture forms,
each carried with a confidence score rather than a hard binary
classification. That grammar output drives the generative music and
lighting engine (visual layer implemented in Processing —
`Cerca_Visuals.pde` — reading the same serial stream).

## 6. Why this design

See [DECISIONS.md](DECISIONS.md) for the specific rejected alternatives
(single-pulse beaconing, separate electrode straps, keeping the patent
"pending" indefinitely, and others).
