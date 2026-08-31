# Council topology — vessel files + contract structure

**What this is:** a directory listing of `Agents/vessels/` (per-agent persona/constitution files, one per house agent) and the top-level structure of `memory/procedural/agent_contracts.json` (the machine-readable contract each agent operates under). Filenames and schema keys only.

**Redactions:** vessel file contents not reproduced beyond the design-showing excerpt in SNIPPETS/ (with a chat-id line removed — see that file's own header). Contract *values* shown below (identity/scope/allowed/forbidden actions) are role descriptions, not personal data, and are reproduced verbatim as evidence of the design.

---

## Vessel files on disk

```
$ ls Agents/vessels/
abraxas_vessel.md
chris_vessel.md
fay_vessel.md
fred_vessel.md
kubera_vessel.md
scribe_vessel.md
thoth_vessel.md
```

Seven vessels exist for seven agents (Abraxas, Chris, Fay, Fred, Kubera, Scribe, Thoth) — direct evidence the twelve-house Council (see `STORY.md`) is a real, partially-built architecture: multiple houses have working, versioned constitution files (each carries `.bak_*` revision history, e.g. `.bak_20260614_nudge_policy_removal` on every vessel — a policy change applied uniformly across all seven agents on the same day), not just Abraxas alone.

## agent_contracts.json — structure

```
$ python3 -c "import json; d=json.load(open('memory/procedural/agent_contracts.json')); print(list(d.keys()))"
['schema_version', 'layer', 'type', 'author', 'generated_at', 'sources', 'agents', 'routing_rules', 'hierarchy']

$ python3 -c "...print(list(d['agents'].keys()))"
['ABRAXAS', 'GARUDA', 'MUSHAKA', 'FRED', 'CHRIS', 'KUBERA', 'FAY', 'THOTH', 'SCRIBE']
```

Nine registered agent contracts, each with the same fixed shape (see `SNIPPETS/agent_contract_shape.json` for the ABRAXAS entry in full): `emoji`, `identity`, `house`, `model`, `scope`, `cognitive_posture`, `allowed_actions`, `forbidden_actions`, `working_dirs`, `response_format`, `mode_marker`.

## hierarchy block

```json
{
  "sovereign": "ANIMA (World Soul, above all houses)",
  "meta_layer": "ABRAXAS (supervisory oracle, pattern reader)",
  "planning_layer": "GARUDA (architect, planner)",
  "execution_layer": "MUSHAKA (code shipper, file operator)",
  "domain_agents": ["FRED (1st)", "CHRIS (2nd)", "KUBERA (5th, quant/risk/recon, under Chris)", "FAY (6th)"],
  "knowledge_agents": ["THOTH (corpus)", "SCRIBE (academic, isolated)"],
  "echo_layer": "Per-agent lightweight self-check. Silent if correct. Escalates to ANIMA if not."
}
```

Abraxas sits at the `meta_layer`, above the planning/execution pipeline (GARUDA/MUSHAKA) and above the domain house-agents it consults (FRED, CHRIS, KUBERA, FAY) — matching the "lord of lords, consults not merges" design stated in `STORY.md` and this project's README.

## routing_rules keys

```
['voice_notes', 'financial_logic', 'backtest_verification', 'knowledge_extraction',
 'university_work', 'architecture_planning', 'code_execution', 'household_coordination',
 'trading_biometrics', 'abraxas_request']
```

A named routing table — evidence dispatch to house agents is a declared, table-driven decision, not ad hoc improvisation by whichever agent happens to be talking.
