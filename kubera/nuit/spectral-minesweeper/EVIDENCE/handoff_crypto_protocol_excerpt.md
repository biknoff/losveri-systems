# EVIDENCE — handoff crypto protocol (head excerpt, cross-link)

**What this is:** the frontmatter and opening framing of
`HANDOFF_CRYPTO_PROTOCOL.md` (5th-house-kubera, branch `cocktail-v3`) — shown
only to establish that the cryptographic handoff-trust layer this project's
`receipts/` and `seals/` sit under is a real, specified protocol, not an
informal convention. **The full protocol (GPG verification, hash-chain
mechanics, the `LEDGER_HALT` gate) belongs to and is evidenced in the separate
`kubera/nuit/build-method-governance/` project** — do not duplicate it here;
follow that project's own README/EVIDENCE for the verified transcript.

## Frontmatter

```yaml
file: HANDOFF_CRYPTO_PROTOCOL.md
authored: 2026-04-24 (Claude Opus 4.7 follow-up session with Leo)
purpose: specify the three-layer cryptographic trust protocol governing every phase handoff
status: LOCK-HEAVY · load-bearing · once signed, modifications require Leo+Mariele + versioned supersession
version: v1 (bootstrap)
pairs_with:
  - NUIT_SPECTRAL_BLUEPRINT_v2_20260424.md (ur-source of the architecture this protocol guards)
  - HANDOFF_design_to_phase0_build.md (original Phase 0 brief; establishes LOCK-20 mongoose idempotency that this protocol extends)
  - PHASE_0_AMENDMENTS_20260424.md (extends original brief; provenance_hash_dict includes this file)
governance: Leo + Mariele are sole signing roots; no other party's GPG signature is accepted
supersedes: none (this is v1)
implementation_target: ledger/handoff_verifier.py (SPEC ONLY inside this file; Builder implements in Phase 0)
```

## Opening framing (verbatim, one paragraph)

> **Reader discipline.** This document specifies the cryptographic substrate for
> every handoff between phases. It is not a PKI project. It is not a research
> contribution. It is a three-layer application of standard tools (SHA-256, GPG,
> git) that makes the sentence *"Phase N says X"* mechanically verifiable by
> Phase N+1, rather than taking it on faith. The protocol inherits the
> architectural grain of LOCK-20 (mongoose idempotency: `run_id + output_hash +
> source_code_hash`) and lifts it one level up, from numeric mongoose outputs to
> phase-handoff documents.

The connective tissue worth naming: LOCK-20 (mongoose idempotency — see
`SNIPPETS/idempotency_check.py`) is the *numeric* discipline; this protocol is
the same discipline lifted to the *document* layer. Same instinct, two altitudes.
