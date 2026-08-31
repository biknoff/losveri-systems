# Decisions

## 1. Seal across the AI-session boundary, not just the code commit
**Rejected: sealing only code commits.** A signed commit or tag proves a snapshot of *code* is
authentic; it says nothing about whether the *reasoning and design substrate* a fresh AI session
is about to inherit is intact. The threat model here is specifically a new chat session with no
memory, told to trust a pile of prior handoff documents and locked decisions — so the envelope
hashes lock text, decision records, and dependency files, not just source code, and the seal gate
sits at the boundary between one session's work and the next session reading it.

## 2. Human-clear `LEDGER_HALT.txt`, no auto-resume
**Rejected: an automated retry or auto-resume on the next clean check.** The halt protocol (§10)
exists precisely because the thing this protocol distrusts is LLM judgment under pressure to keep
moving. An automatic resume would recreate exactly that pressure one level up — "the pipeline
decided the failure was transient." Clearing the sentinel is deliberately a human-only action
(enforced by a commit hook requiring Leo/Mariele co-sign), and an LLM is explicitly forbidden from
even attempting it.

## 3. Mortal architects with a stand-down rule
**Rejected: one immortal architect context running the whole multi-month build.** A single
long-running context accumulates undocumented state — decisions made under context pressure that
nobody outside the session can audit, because they were never forced into writing. Bounding each
architect's tenure, and giving it explicit permission to *stand down mid-cycle* on its own
bandwidth signal (real instance: Architect XI, 2026-04-29) rather than push through degraded
reasoning, forces every architectural decision through a written, dated, filename-citable handoff.
No architect-to-architect conversation exists because none is needed — the sealed record is the
channel.

## 4. Manual verification over claiming unbuilt automation
**Rejected: describing `handoff_verifier.py` as running, or quietly skipping verification because
the tool wasn't built.** The full spec for an automated verifier exists (§9) and was never coded.
Rather than either fabricate an automation claim or drop verification altogether, every real phase
transition ran the equivalent checks by hand — `git tag -v`, `gpg --verify`, hash recomputation —
with the terminal output kept as the evidence. Slower, and honestly labeled as manual; not skipped,
and not oversold.

## 5. Companion-tag rebinding over in-place re-signing
**Rejected: re-signing the same envelope in place to fix a found bug.** When Phase 4's original
seal was found to rest on a truncated data window (LOCK-19 class), the project sealed a *second*,
companion envelope (`phase-4-rebinding-sealed`) chaining from the first, rather than overwriting
`phase_4_envelope.json` and re-signing. In-place correction would have erased the original sealed
state — and with it, the record that a real bug was caught and how it was found. The chain has a
deliberate branch instead of a silently corrected single line, on the stated principle
"provenance-preservation-over-erasure."

## 6. One signing key, exercised honestly rather than a rotation story
**Rejected: pretending multi-key signing or rotation was exercised.** `rotate_keys.py` exists in
`src/governance/` and the bootstrap ceremony spec (§13) explicitly allows for Mariele as a co-root.
In practice, every one of the 8 sealed envelopes carries the identical fingerprint —
`2CDEE63DDA2B1D57F25EADE381A4D221CAA55FF1`, Leo's key, unrotated. The design supports more; the
record states what actually ran, which is one key the whole way through.

## 7. A deliberately incomplete canonicalization (CJS-v1), not full RFC 8785 JCS
**Rejected: adopting a stock JCS library wholesale.** Full JCS (RFC 8785) specifies UTF-16
key-sorting, ECMAScript number formatting, and NFC normalization — machinery this protocol's actual
hashed fields (ASCII keys, no floats, human-curated text) never exercise. Rather than pull in a
general-purpose canonicalizer whose extra guarantees are untested against this data, the protocol
defines the narrower CJS-v1 and names exactly what would force a versioned CJS-v2 supersession —
scope-matched to the real input domain instead of generically "safe."

## 8. A two-step handoff-hash injection instead of a hash of a file that doesn't exist yet
**Rejected: computing `handoff_md_sha256` before `HANDOFF_phase_N.md` is written, or omitting the
field.** The envelope is sealed *before* the narrative markdown exists (the ceremony verifies the
structural substrate first), so the field starts as the literal string `"<PENDING_HANDOFF_WRITE>"`
rather than a fabricated placeholder hash, and the envelope is re-signed once the real file and its
real hash exist. A small operational wrinkle, kept visible in the schema rather than smoothed over
with a fake value.
