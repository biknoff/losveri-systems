# CERCA — Decisions

Format: choice made — rejected alternative and why.

## 1. Prime-number-coded beacon pulses — rejected: assuming only one pair touches at a time

A performance with 4 people rarely has exactly one pair in contact.
Turn-taking, distinctly-coded emitter pulses let the firmware attribute
each reading to a specific emitter/listener pair even when several pairs
are touching simultaneously, instead of collapsing to "someone is
touching someone" and guessing which pair from a single combined signal.

## 2. Conductive headphones as dual electrode + audio-return — rejected: separate electrode straps

An earlier approach would have put a dedicated conductive strap or pad on
each participant purely for sensing, plus separate headphones for audio.
Building the electrode into the headphones themselves means the contact
point participants need for sound is the same contact point the
instrument senses through — one object to wear, not two, and no seam
where a strap could lose contact while the headphones stayed on.

## 3. Faraday-reference floor — rejected: relying on a fixed capacitive baseline per venue

Every venue has different wiring, nearby electronics, and audience size,
which shifts a fixed capacitive baseline enough to break sensing between
installs. Wiring the floor itself as the reference plane makes every
reading relative to a stable in-room ground, rather than a baseline that
has to be re-tuned by hand at each venue.

## 4. Adaptive (FFT-tuned) notch filter — rejected: a fixed 50/60Hz notch

A fixed mains-hum notch assumes the dominant noise source and its
frequency are known and constant. Running a 16-point FFT every 20 cycles
and only engaging a notch when a peak clearly dominates (`> 3× median`)
lets the firmware reject whatever periodic noise is actually present at a
given venue, and turn the notch off cleanly when there isn't one.

## 5. Asymmetric attack/release smoothing — rejected: a single symmetric smoothing coefficient

A single smoothing constant makes touch-onset feel laggy if tuned for
clean release, or makes release feel twitchy if tuned for fast onset.
Splitting attack (0.50) from release (0.75) lets a touch register quickly
while a release decays more gradually, matching how the piece is meant to
feel to a participant.

## 6. Let the filing lapse, state it — rejected: "patent-pending" forever

A provisional patent was filed; USPTO requested additional information to
proceed; the filing was allowed to lapse rather than pursued further.
This repo states that history exactly, rather than describing the piece
as "patented" or leaving a stale "patent-pending" label that would misrepresent
its current legal status.
