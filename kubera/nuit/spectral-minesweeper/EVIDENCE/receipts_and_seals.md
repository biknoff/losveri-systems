# EVIDENCE — handoffs and seals (the discipline layer)

**What this is:** counts and representative filenames from `receipts/` and a
count-only note on `seals/` (5th-house-kubera, branch `cocktail-v3`) — the
paper trail underneath the V-chain.

## Receipts: 50

`receipts/` holds 50 files — handoffs, audits, and dispatch specs, each named
for the pipeline stage and dated. Representative filenames (not an exhaustive
list; chosen to show the naming convention, not cherry-picked for content):

```
AUDIT_v_deploy_report_round2_2026-05-06.md
AUDIT_v_manifest_round2_2026-05-06.md
AUDIT_v_stress_round2_2026-05-06.md
EXTERNAL_AUDIT_DIGEST_2026-05-05.md
HANDOFF_agitated_combined_window_to_operator_2026-05-06.md
HANDOFF_all_candidates_audit_to_operator_2026-05-06.md
HANDOFF_cf1_pivot_to_operator_2026-05-05.md
HANDOFF_cf2_dedup_sizer_to_operator_2026-05-06.md
HANDOFF_cf3_cycle1_daughter_generation_to_operator_2026-05-06.md
HANDOFF_cibation_rerun_to_operator_2026-05-07.md
dispatch_v5_focused_fib_rth_2026-05-08.json
```

Two things the naming convention itself proves: (1) every handoff is addressed
`_to_operator` — the human is always the receiving end, not a bystander; (2)
handoffs are dated and stage-scoped, not a single monolithic log — each pipeline
move gets its own receipt.

## Seals: 17 (count only)

`seals/` holds 17 entries. Per the sourcing constraint for this reconstruction,
seal contents are never opened — the cryptographic sealing mechanism itself
(GPG signatures, hash chains, the `LEDGER_HALT` human-clear gate) is documented
and evidenced in the separate **Build Method + crypto governance** project
(`kubera/nuit/build-method-governance/`), which this project links to rather
than duplicates. See `SNIPPETS/` there for the verified transcript, and
`EVIDENCE/handoff_crypto_protocol_excerpt.md` here for the protocol's own
framing of why sealing exists.
