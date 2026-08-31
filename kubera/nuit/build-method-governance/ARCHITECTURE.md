# Architecture

Source of truth: `HANDOFF_CRYPTO_PROTOCOL.md` (76KB, authored 2026-05-01, itself the bootstrap
root of the hash chain it defines). This document summarizes it; §-references below point into
the original spec.

## 1. Three stacked layers

**Layer 1 — content hashing.**
- `lock_hash_dict` (§3): every design "lock" (a locked decision — 22 of them by Phase 0, e.g.
  "the system is simulation-based inference, not predictive-model fitting") is serialized to a
  canonical record and SHA-256'd. Reword the prose, even faithfully, and the hash changes — this
  is what catches silent drift between phases.
- `provenance_hash_dict` (§4): every input file the phase depends on (blueprints, OCS configs,
  contracts, prior handoffs) gets a file-content SHA-256 entry.

**Layer 2 — git-commit provenance** (§6): a signed git tag (`phase-N-sealed`) anchors the envelope
to one specific commit. Tag message states the predecessor tag and a one-line summary; verification
checks the tag exists, is GPG-signed by a trusted fingerprint, names the expected envelope hash,
and points at a commit that actually contains the envelope file.

**Layer 3 — GPG signature** (§7): a detached signature (`seals/phase_N_envelope.json.sig`) over
the envelope's raw bytes. Trust root: Leo's public key (`seals/leo_public_key.asc`), fingerprint
`2CDEE63DDA2B1D57F25EADE381A4D221CAA55FF1`, EDDSA, referenced unchanged across every phase (0
through 4, plus the 4-rebind companion) — the "single signing key" honest gap below is this
fingerprint used end to end, never rotated or joined by a second signer in practice, though the
protocol's design (`rotate_keys.py` exists in `src/governance/`) allows for more than one.

## 2. Envelope format (§5.1)

One JSON file per phase close, `seals/phase_{N}_envelope.json`:

```
envelope_version, phase_n, phase_from, phase_to, authored_utc,
lock_hash_dict{ LOCK-01..LOCK-22: sha256 },
provenance_hash_dict{ <every dependency file>: sha256 },
predecessor_envelope_sha256,      # the chain link — see §3 below
git_commit_sha,
handoff_md_ref, handoff_md_sha256,
signed_by_fingerprint,
notes                              # free text, CJS-v1-safe
```

All fields required except `notes`. See `SNIPPETS/envelope_schema_excerpt.json` for a real
(redacted-of-nothing — these are hashes and metadata, not secrets) example: the actual Phase 0
envelope.

A real operational wrinkle, preserved rather than smoothed over: `handoff_md_sha256` cannot be
known until the narrative `.md` is *written*, which happens *after* the sealing ceremony verifies
structurally — so it starts as the literal string `"<PENDING_HANDOFF_WRITE>"`, and the envelope is
re-signed once the real hash is injected. Two-step, not fabricated.

## 3. The hash chain (§5.2)

`predecessor_envelope_sha256` is the SHA-256 of the *previous* envelope's raw file bytes. Phase 0's
predecessor is `HANDOFF_CRYPTO_PROTOCOL.md` itself — the bootstrap root. This produces an
append-only chain:

```
HANDOFF_CRYPTO_PROTOCOL.md
  → phase_0_envelope.json → phase_1_envelope.json → phase_2_envelope.json
  → phase_3_envelope.json → phase_3_5_envelope.json → phase_4_envelope.json
  → phase_4_envelope_rebind.json  (companion tag, see DECISIONS.md #5)
```

8 envelopes, 8 links. Tampering with any envelope midstream breaks the chain from that point
forward — a verifier walking backward from the tip hits the first broken link and stops. No LLM
session acting alone can forge a chain-valid envelope: it doesn't hold Leo's private key and can't
retroactively update every downstream predecessor reference. Full provenance detail, including the
actual recorded hashes: `EVIDENCE/hash_chain_provenance.md`.

## 4. Canonicalization — CJS-v1 (§2)

A from-scratch, byte-deterministic JSON serialization (sorted ASCII keys, no inter-token
whitespace, UTF-8, `ensure_ascii=False`) — deliberately **not** full RFC 8785 JCS (§2.4): no
UTF-16 key-sort, no ECMAScript number formatting, no NFC normalization, because every hashed field
in this protocol is ASCII-keyed, float-free, and human-curated. The protocol names exactly what
would force a CJS-v2 (floats, non-ASCII keys, a cross-language verifier) rather than silently
under-specifying the boundary. Spec excerpt: `SNIPPETS/cjs_v1_spec.py`.

## 5. The halt gate — `LEDGER_HALT.txt` (§10)

On any verification failure: a halt manifest is written
(`ledger/verification_failures/phase_N_<timestamp>.json`, naming which layer failed and why), a
sentinel file `LEDGER_HALT.txt` is created at repo root, and every downstream pipeline entry point
checks for that sentinel *first* and refuses to proceed while it exists. Clearing it is a human-only
action — "LLMs and scripts are forbidden from removing this file." The protocol is explicit that
this is not itself cryptographically enforced (an LLM with filesystem write access could
technically delete the sentinel); the actual enforcement is a git commit hook that refuses any
commit deleting `LEDGER_HALT.txt` without a co-signed commit from Leo or Mariele, plus operational
file-permission hygiene. §10.4 states the rule directly: an LLM may read the failure manifest and
narrate it, may suggest hypotheses, and must not act on them without operator confirmation in chat.

## 6. Architect succession (mortal-architect protocol)

Not a cryptographic layer — a governance convention layered on top of the same sealed substrate.
No single AI context is trusted to run the whole multi-month build:

- Architects are numbered and sequential (Master Architect I, II, … XIII observed in the record).
  Each is a fresh chat session, told explicitly what it is not ("You are NOT a Phase Builder…
  you are the design-and-oversight role") and what its predecessors did, sourced only from written
  artifacts.
- **Stand-down rule.** An architect that senses its own context is degrading ("bandwidth signal")
  hands off *mid-cycle* rather than pushing through — e.g. Architect XI stood down 2026-04-29
  mid-cycle; Architect XII took the handback for the remaining checkpoint and cycle close.
- **No architect-to-architect talk.** Successors never converse with predecessors directly — there
  is no shared context to converse in. The channel is exclusively the written handoff packet
  (a spawn prompt citing prior artifacts by filename, a continuity document, and the sealed
  envelope chain underneath it). This is the same discipline as the crypto layer, applied to
  human-AI governance instead of file integrity: trust only what's written down and checkable, not
  what's remembered.
- Full transcript excerpt of a real succession: `EVIDENCE/mortal_architect_succession.md`.

## 7. The named gap: `handoff_verifier.py` was never built

§9 of the protocol document is a full module specification — function signatures, a CLI entry
point, dependencies, a performance budget, error semantics, and a 7-part test suite spec (§12) —
for a single automated tool that would run all three layers end to end and emit the halt manifest
mechanically. It is marked **"SPEC ONLY"** in the source heading. It was never implemented as code.
Every verification that actually happened in this project's real phase transitions happened by a
human (or an AI session, instructed to and audited) running the equivalent `git tag -v` / `gpg
--verify` / hash-recompute commands **by hand**, phase by phase, and reading "Good signature" /
`exit=0` off the terminal — documented in `EVIDENCE/gpg_verification_transcript.md`. The design is
complete; the automation is not. Stated here rather than implied, because a system that claims
automated verification it doesn't have is worse than one that admits it doesn't have it.
