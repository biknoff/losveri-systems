<!-- WHAT: the predecessor_envelope_sha256 chain, reconstructed from the real seal envelope JSON
     files on disk (metadata fields only — phase numbers, hashes, notes; never strategy content,
     lock text, or file contents beyond their hash). REDACTED: nothing removed; every hash shown
     is a hash, not a secret. -->

# The 8-link predecessor hash chain, root to tip

Each envelope's `predecessor_envelope_sha256` field is the SHA-256 of the *previous* envelope's
raw file bytes (or, for Phase 0, of `HANDOFF_CRYPTO_PROTOCOL.md` itself — the bootstrap root).
Walking the chain as recorded in the actual seal files:

```
HANDOFF_CRYPTO_PROTOCOL.md
    sha256 = 965bc0ff994671c6db84b4fdde78640d63090c6bf951cb8742cd436129ce12dd
        │
        ▼
phase_0_envelope.json      predecessor = 965bc0ff...  (protocol doc)
        │  sha256(this file)
        ▼
phase_1_envelope.json      predecessor = sha256(phase_0_envelope.json)
        │
        ▼
phase_2_envelope.json      predecessor = sha256(phase_1_envelope.json)
        │
        ▼
phase_3_envelope.json      predecessor = sha256(phase_2_envelope.json)
        │
        ▼
phase_3_5_envelope.json    predecessor = sha256(phase_3_envelope.json)
        │
        ▼
phase_4_envelope.json      predecessor = bfda152318f0fae169ec5a796c161e8d83ac0c7e1166b6c30e479bd7e685fff1
                                        = sha256(phase_3_5_envelope.json)  [confirmed at Phase 4 close, see gpg_verification_transcript.md]
        │
        ▼
phase_4_envelope_rebind.json   predecessor = 7a8b07a70f254ae24874daf4bb51de5724b3559bd4a5c9bb1b89f9a2fe9021a9
                                            = sha256(phase_4_envelope.json, post-handoff-hash-injection state)
        │
        ▼
phase_4_5_envelope.json    (Phase 4.5 design-cycle close; chains forward from the rebind)
```

**8 links, 8 envelopes, unbroken.** Each hash above is the file-bytes SHA-256 of the actual sealed
JSON on disk, taken directly from the envelope fields (not recomputed independently for this
write-up — recomputation is exactly what the never-built `handoff_verifier.py` would automate, and
what the manual ritual in `gpg_verification_transcript.md` did do, by hand, at each real phase
transition).

## The one deliberate branch: `phase_4_envelope_rebind.json`

Phase 4's original sealed evidence used a truncated activation window (a silent 17-month data-slice
truncation bug, LOCK-19 class). Rather than re-signing `phase_4_envelope.json` in place to fix it —
which would have erased the original sealed state and the discovery itself from the record — the
project sealed a **companion tag**: `phase-4-rebinding-sealed`, chaining from `phase-4-sealed`,
preserving both as independently valid trust-chain members. The envelope's own notes field states
the rationale directly:

> "Re-bind delta is material (4 IS-pass lost, 2 gained, 1 cluster eliminated, 1 confirmed false
> positive at PF=8.86 → 0.95). Path A (companion tag phase-4-rebinding-sealed) preserves the
> original phase-4-sealed state as historical evidence of the truncation finding... Path B
> (in-place re-sign overwriting phase-4-sealed) would erase the historical record and the case
> study with it. Provenance-preservation-over-erasure pattern."

This is the real-world instance behind DECISIONS.md #5 — the chain has a branch precisely because
erasing evidence of a caught bug was rejected as an option.

## Signing key, unchanged across the whole chain

`signed_by_fingerprint`: `2CDEE63DDA2B1D57F25EADE381A4D221CAA55FF1` (Leo, ed25519, ultimate trust)
— present, identical, in every one of the 8 envelopes, from Phase 0 through Phase 4.5. No second
signer or key rotation was exercised in practice, even though the design supports it (see
`SNIPPETS/` and `honest_status_and_gaps.md`).
