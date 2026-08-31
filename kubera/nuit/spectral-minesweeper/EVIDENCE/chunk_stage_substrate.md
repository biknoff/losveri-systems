# EVIDENCE — chunk substrate as named stages

**What this is:** the stage names of the `engine/spectral/` build substrate
(5th-house-kubera, branch `cocktail-v3`) — the numbered "chunks" each engine
component was built and contracted in. **Names and file kinds only.** No math,
no kernel internals, no PDE content — `chunk_4_physics_pde.md` and
`chunk_4_derivation.md` exist and are not opened here beyond their filenames.

## The stages (build order)

| Chunk | Present artifacts (by kind) |
|---|---|
| 0 | loader, assumptions, contract, manifest, tests |
| 1 | PSD module, kernel spec, assumptions, contract, manifest, tests, export manifest |
| 2 | contract, manifest, tests |
| 3 | log-likelihood module, assumptions, contract, manifest, tests |
| 4 | derivation doc, physics/PDE doc, assumptions, contract, manifest, tests |
| 5 | assumptions, contract, manifest, tests |
| 6 | assumptions, contract, manifest, tests |
| 6.5 (+ v2, v3) | corpus generator(s), bridge module, candidate jsonl, assumptions, contract, manifest, tests, corpus config |
| 7 (+ v2, v3) | harness, assumptions, contract, manifest, tests |

Every chunk carries the same triple discipline: `*_contract.json` (what the
chunk promises), `*_manifest.json` (what it actually produced), `*_tests.json`
(what was checked) — a per-stage version of the same contract-first posture
that shows up again in the ledger's six-state classifier
(`SNIPPETS/contract_state_classifier.py`) and the handoff crypto protocol.

## What's deliberately not shown

`celerite2d.py` / `celerite2d_kernels.c` (the spectral kernel implementation),
`chunk_3_loglike.py`, `chunk_4_derivation.md`, `chunk_4_physics_pde.md`, and the
corpus-generator internals are real files on disk, named here for structure
only — their contents are the trade-secret math substrate and are not excerpted.
