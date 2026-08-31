<!-- WHAT: a file-listing (names, sizes, dates) of the private source repo's seals/ directory.
     REDACTED: nothing — these are file names and byte sizes only, never envelope contents or
     signature bytes. Per the commissioning instruction, seal file CONTENTS were never read for
     this write-up beyond the metadata fields (hashes, phase numbers) needed to describe the
     chain mechanism, reproduced in hash_chain_provenance.md. -->

# Seal inventory — file listing only

From the private source repo's `seals/` directory, `ls -la` (2026-05, unchanged since):

```
leo_public_key.asc             725 bytes   # Leo's public GPG key — only public material published
phase_0_envelope.json         4823 bytes
phase_0_envelope.json.sig      147 bytes
phase_1_envelope.json         6366 bytes
phase_1_envelope.json.sig      265 bytes
phase_2_envelope.json         8366 bytes
phase_2_envelope.json.sig      265 bytes
phase_3_envelope.json        13821 bytes
phase_3_envelope.json.sig      265 bytes
phase_3_5_envelope.json      15336 bytes
phase_3_5_envelope.json.sig    265 bytes
phase_4_envelope.json        21367 bytes
phase_4_envelope.json.sig      265 bytes
phase_4_envelope_rebind.json 15182 bytes
phase_4_envelope_rebind.json.sig 265 bytes
phase_4_5_envelope.json      10763 bytes
phase_4_5_envelope.json.sig    265 bytes
```

**17 files total: 8 envelope/signature pairs (16 files) + 1 public key.** Phases sealed: 0, 1, 2,
3, 3.5, 4, 4-rebind (a deliberate companion tag, not an overwrite — see DECISIONS.md #5), 4.5.

Each `.sig` is a detached GPG signature over the corresponding `.json`'s raw bytes (§7.3 of
`HANDOFF_CRYPTO_PROTOCOL.md`). The `.sig` files are small (147–265 bytes) because a detached
Ed25519/EDDSA signature is small regardless of the signed payload's size — the `.json` files range
from 4.8KB (Phase 0, a bootstrap envelope with few dependency files) to 21.4KB (Phase 4, the
largest phase's V_is binding evidence and dependency set).

## Adjacent: 50 receipt files — one folder in a much larger corpus

The build-discipline receipts folder (`receipts/`, a separate but related practice — every
commissioned agent produces a receipt before its work is considered complete, per
`BUILDER_GOVERNANCE §7`) holds 50 files as of the last count: handoffs, audits, dispatch records,
and one `README.md` documenting the naming convention
(`HANDOFF_<commission-name>_to_operator_<YYYY-MM-DD>.md`) and the reconstruction-caveat rule (a
receipt written retroactively for un-receipted prior work is banner-marked
`RECONSTRUCTED FROM SELF-BRIEF`, never passed off as contemporaneous).

That 50 is one directory, not the whole corpus. A direct re-count across both machines that hosted
this build (the research host and a separate, only-partially-overlapping Mac-side cache) finds on the order of
150-220 distinct handoff/audit/dispatch documents total, spread across several mirrored directory
trees that don't fully sync with each other. Full accounting, including three additional real
integrity catches drawn from this same `receipts/` folder: `corpus_scale_and_more_catches.md`.
