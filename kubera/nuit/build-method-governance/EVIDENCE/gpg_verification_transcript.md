<!-- WHAT: real terminal-output excerpts from the source repo's HANDOFF_phase_N.md files —
     the "opening ritual" verification commands each session ran, and one full sealing-ceremony
     record. REDACTED: nothing removed from the shown commands/output; the GPG fingerprint shown
     is Leo's PUBLIC key fingerprint (safe to publish, it's how anyone verifies a signature, not
     a secret) and is quoted verbatim because the protocol itself treats it as a citable trust
     anchor. No private key material appears anywhere in this file. -->

# Manual verification, phase after phase — real transcripts

This is the evidence for "verification ran" without an automated `handoff_verifier.py` (which was
never built — see `honest_status_and_gaps.md`). Each phase's `HANDOFF_phase_N.md` opens with an
"opening ritual" instructing the next session to run these commands, in order, before reading
anything else, and to HALT if any fails. The count of required checks grows every phase because
each new seal adds one more tag and one more envelope signature to the chain that must all still
verify:

| Phase transition | Required checks | Source |
|---|---|---|
| → Phase 0 | ALL THREE must exit 0 | `HANDOFF_phase_0.md:1054` |
| → Phase 1 | ALL FIVE must exit 0 | `HANDOFF_phase_1.md:913` |
| → Phase 2 | ALL SEVEN must exit 0 | `HANDOFF_phase_2.md:1016` |
| → Phase 3.5 | All **NINE** must exit 0 | `HANDOFF_phase_3.md:472` |
| → Phase 4 | ALL ELEVEN must exit 0 | `HANDOFF_phase_3_5.md:979` (5 tags + 5 envelope sigs + trailing check) |

Verbatim (Phase 3 opening, `HANDOFF_phase_3.md`):

```
git tag -v design-phase-sealed-2026-04-24
git tag -v phase-0-sealed
git tag -v phase-1-sealed
git tag -v phase-2-sealed
git tag -v phase-3-sealed
gpg --verify seals/phase_0_envelope.json.sig seals/phase_0_envelope.json
gpg --verify seals/phase_1_envelope.json.sig seals/phase_1_envelope.json
gpg --verify seals/phase_2_envelope.json.sig seals/phase_2_envelope.json
gpg --verify seals/phase_3_envelope.json.sig seals/phase_3_envelope.json

All NINE must exit 0. If any fails, HALT.
```

## A full sealing-ceremony record (real output, Phase 4 close, 2026-04-27)

From `HANDOFF_phase_4.md §F`, captured by the Phase 4 Builder — this is the actual terminal output
of one real ceremony, not a template:

```text
=== Phase 4 seal verification ===
Date: 2026-04-27T17:17:31Z
Branch: main
HEAD: defa1bb1019ef46a4dd882c9c09bf2147b26b730

--- envelope detached signature ---
gpg: Signature made Mon Apr 27 12:45:00 2026 AST
gpg:                using EDDSA key 2CDEE63DDA2B1D57F25EADE381A4D221CAA55FF1
gpg: Good signature from "leo <redacted>" [ultimate]
exit=0

--- tag signature (git verify-tag) ---
gpg: Signature made Mon Apr 27 13:13:13 2026 AST
gpg:                using EDDSA key 2CDEE63DDA2B1D57F25EADE381A4D221CAA55FF1
gpg: Good signature from "leo <redacted>" [ultimate]
exit=0

--- envelope hash recompute ---
404746d66b96cfae9de0e9205d116b6f318d0cc1ddba7499d3372e49c402d9f3  seals/phase_4_envelope.json
Expected: 404746d66b96cfae9de0e9205d116b6f318d0cc1ddba7499d3372e49c402d9f3

--- predecessor chain check ---
recorded predecessor_envelope_sha256: bfda152318f0fae169ec5a796c161e8d83ac0c7e1166b6c30e479bd7e685fff1
computed sha256(seals/phase_3_5_envelope.json): bfda152318f0fae169ec5a796c161e8d83ac0c7e1166b6c30e479bd7e685fff1
CHAIN: OK

--- full trust chain end-to-end ---
design-phase-sealed-2026-04-24    OK
phase-0-sealed                    OK
phase-1-sealed                    OK
phase-2-sealed                    OK
phase-3-sealed                    OK
phase-3-5-design-sealed-2026-04-25 OK
```

Every check that a hypothetical `handoff_verifier.py` would perform mechanically — signature
validity, hash recomputation, chain-continuity comparison — is present here, run by hand, with the
raw `gpg`/`sha256sum`/`git` output kept rather than summarized.

## On "9/9"

The operator's own record (Atlas, dated 2026-07-20) states plainly: **"9/9 GPG sigs re-verified
live today."** The Phase-3-opening ritual above shows the mechanical origin of that count (5 tag
verifications + 4 envelope signature verifications = 9 GPG operations, all must exit 0 with "Good
signature"). A dedicated, dated 2026-07-20 terminal transcript matching that specific re-verification
run was not found on disk during this write-up's research pass; what's shown above is the closest
real, on-disk equivalent — the Phase 4 ceremony record and the phase-by-phase ritual definitions
that establish exactly what "9" refers to and what passing it looks like. Stated as pending rather
than fabricated.
