<!-- WHAT: a status summary synthesized from the source repo's protocol document and sealing-close
     summary. REDACTED: nothing — dates, phase counts, and gap descriptions only. -->

# Honest status: BUILT+DORMANT, and what's really missing

## What ran, for real

- 8 phases sealed (0, 1, 2, 3, 3.5, 4, 4-rebind, 4.5), each with a signed git tag, a signed
  detached-GPG envelope, and a hand-run verification ritual at the opening of the next phase.
- The chain never broke. Every "opening ritual" transcript on disk (`gpg_verification_transcript.md`)
  shows exit 0 / "Good signature" for every check, every phase, including the largest — 11
  checks at Phase 4's open.
- One real integrity finding surfaced and was handled *through* the protocol rather than around it:
  the Phase 4 activation-window truncation bug (LOCK-19 class), disposed of via a companion seal
  rather than an erasing re-sign (`hash_chain_provenance.md`).
- The mortal-architect protocol produced at least one real, on-record mid-cycle stand-down
  (Architect XI → XII, 2026-04-29) with a clean written handback, not a silent context switch.

## What was designed but never built

`HANDOFF_CRYPTO_PROTOCOL.md §9` is a full specification for `ledger/handoff_verifier.py` — module
layout, function signatures for every layer (CJS-v1 primitives, lock hashing, file hashing, git
checks, GPG checks, composed verification, a CLI entry point), a dependency list, a performance
budget, defined error semantics, and a 7-part test suite spec (§12: lock hashing, file hashing,
git, GPG, integration tests for `verify_handoff`, halt-protocol tests, and a CJS-v1 test-vector
file). The section header marks it explicitly: **"SPEC ONLY."** It was never implemented as code
in this project. Every verification event that actually happened in the real phase transitions was
a human running the equivalent `gpg --verify` / `git tag -v` / hash-recompute commands by hand and
reading the terminal output — proven in `gpg_verification_transcript.md`, not merely claimed.

The `LEDGER_HALT.txt` sentinel and halt-manifest format (§10) are likewise fully specified as the
*output* of that automated verifier, but since the verifier never ran as code, the halt gate that
actually operated in practice was the ritual's own "If any fails, HALT" instruction to the AI
session performing the manual check — enforced by discipline and by a git commit hook (blocking a
commit that deletes `LEDGER_HALT.txt` without a human co-sign), not by the mechanical pipeline the
spec describes.

## Single key, not the multi-key design

`signed_by_fingerprint` is identical — Leo's — across all 8 sealed envelopes. `src/governance/`
contains a `rotate_keys.py` module, meaning key rotation was designed for, but no rotation, and no
second signer (e.g. Mariele, mentioned as a possible co-root in §13's bootstrap ceremony spec), was
ever actually exercised on this chain. One key, one operator, the whole way through.

## Why it's parked, not abandoned

The project this protocol protected (NUIT Spectral Minesweeper's design-and-build cycle) reached
Phase 4.5's design-cycle close on 2026-04-28 and the cycle wound down naturally — there was nothing
further to seal. The method is not "retired" in the sense of superseded or broken; it is dormant in
the sense that its next use is a future project resuming AI-session-boundary work at the same
rigor. The method also lives on in a documentary sense inside this very showcase repo: every build
session that produced these showcase docs itself leaves a receipt (see the top-level `receipts/`
directory and `METHOD.md`) — the discipline of "handoffs as artifacts" continues even where the
cryptographic sealing does not.

## What "convergent-validated, not novel" means here

Every primitive used — SHA-256, GPG detached signatures, signed git tags, append-only hash chains —
is stock and cited to a standard in the protocol document's own §16 references. Tooling that
audits AI-agent action trails already exists elsewhere (broadly, "ai-audit-trail"-shaped prior
art). What is not generic off-the-shelf is the specific combination: gating admission *across the
AI dev-session boundary itself* (a fresh session may not trust what it inherits until a human-run
chain-verification says so) plus the mortal-architect succession convention riding on top of the
same sealed record. The claim made here is the existence proof — this combination ran, for real,
eight times in a row — not a claim of cryptographic novelty.
