# Ecological (Bronfenbrenner-tiered) memory — structure on disk

**What this is:** the top-level layout of `memory/` and the contents of each tier directory, verifying the operator's own documentation of a Bronfenbrenner-style "ecological" memory model against what actually exists on disk. Filenames only — no file contents opened for the entries below beyond the one contract file already excerpted in `council_topology.md`.

**Redactions:** none needed — directory/file names carry no personal content by themselves (dates, schema files, index files).

---

```
$ ls memory/
chronosystem/    claude_memory_export.json   exosystem/
family_update_ledger.jsonl   macrosystem/   MANIFEST.json
mesosystem/   procedural/   semantic/
```

Six tiers exist as real directories, each populated:

| Tier | Contents (filenames) | What it's for (per the model design) |
|---|---|---|
| `macrosystem/` | `current_phase.json` | The broadest frame — current life/system phase |
| `chronosystem/` | `family_arc.json` | Time-extended narrative arc |
| `exosystem/` | `2026-W14.json`, `2026-W16.json` | Weekly-indexed outer-context snapshots |
| `mesosystem/` | 12 daily files, `2026-03-31.json` → `2026-05-08.json` | Day-indexed interaction context |
| `semantic/` | `contacts.json`, `household_state.json`, `principles_gap.json`, `sacred_rules.json`, `trading_rules.json` | Durable facts/rules, not episodes |
| `procedural/` | `agent_contracts.json`, `abraxas_dispatch_rules.json`, `kubera_contract.json`, `trading_protocols.json`, `corrective_patterns.json`, `three_role_agent_topology.json`, `dispatch_brief_discipline.json`, `family_updates.json` | How-to / contract / protocol definitions |

`MANIFEST.json` is a top-level index over the tiers. The CLI wrapper (`tools/abraxas`) reads `memory/MANIFEST.json` as one of its required-at-boot files (see `EVIDENCE/boot_hard_fail.md`) and injects a "nested-system context protocol" into every prompt instructing the model to escalate through mesosystem → exosystem → macrosystem → chronosystem only on demand, not preload all of it — the stated discipline is to keep the always-loaded context small (an explicit echo of Principle I applied to the agent's own context window, per the vessel file).

This confirms the tiered structure is real and populated, not just named in documentation — with the caveat that tier population is uneven (`mesosystem` has 12 daily entries vs. `exosystem`'s 2 weekly entries), consistent with a system still being actively developed rather than a finished, uniformly-maintained pipeline.
