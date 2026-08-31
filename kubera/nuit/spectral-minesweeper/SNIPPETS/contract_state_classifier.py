# file: SNIPPETS/contract_state_classifier.py
# source: ledger/contract_state.py (5th-house-kubera, branch cocktail-v3), lines 1-95
# excerpted read-only, in full for this module's header + state enum + role matcher.
# The classify() body (component composition logic) is not reproduced — this excerpt
# is enough to show the six-state contract and that the classifier is pure/deterministic.

"""contract_state.py — LEDGER six-state classifier (Phase 1 deliverable 2/5).

Source of truth for the LEDGER state enum:
    blueprint § 3       — original five states
    amendments § 4      — sixth state SEARCH_INFEASIBLE
    test_six_states.md  — fixture spec each test exercises

Pure logic. No filesystem reads, no subprocess, no network. Given:
    - per-component runtime results (from verify_runtime.py)
    - contract.yaml's components dict (parsed by caller)
    - optional search_infeasible_signal from PROBE post-flight (Phase 11+)

Returns: (state, reasons_dict). Caller writes the manifest.

State precedence (highest priority wins; halt states beat proceed states):
    BROKEN              — runtime exception or timeout (machinery itself failed)
    CONTRACT_MISMATCH   — fingerprint doesn't match primary OR any declared fallback
    SCAFFOLD_ONLY       — fingerprint matches a declared scaffold_probe
    SEARCH_INFEASIBLE   — N>=N_min trials clean, margin vectors uniformly negative on >=1 rule (PROBE-fed)
    PARTIAL_SPEC_ACTIVE — at least one component on a declared fallback (LOCK-22: not eligible for funded)
    FULL_SPEC_ACTIVE    — every component matches its primary, no fallbacks engaged

The classifier is independent of WHICH component is in which state; it composes
boolean predicates and returns the worst-priority verdict with reasons cited per
component.
"""

from __future__ import annotations
from typing import Any

# Canonical state enum — must match contract.yaml::components.ledger_preflight.output_contract.state_enum
# Order matters: precedence priority for multi-state composition (highest = worst).
STATES = (
    "BROKEN",
    "CONTRACT_MISMATCH",
    "SCAFFOLD_ONLY",
    "SEARCH_INFEASIBLE",
    "PARTIAL_SPEC_ACTIVE",
    "FULL_SPEC_ACTIVE",
)

# Per-component runtime result schema (produced by verify_runtime.py per component):
#   {
#     "component_id": str,                   # contract.yaml key, e.g. "celerite2d_backend"
#     "fingerprint": str | None,             # "<id>@<version>" if OK; None on EXCEPTION/MISSING
#     "status": "OK" | "EXCEPTION" | "TIMEOUT" | "MISSING",
#     "exception": str | None,               # exception text if EXCEPTION, else None
#     "evidence": dict,                      # discovery details (path, hash, etc.); free-form
#   }


def _matched_role(component_result: dict[str, Any], component_spec: dict[str, Any]) -> str:
    """Return one of {'primary', 'fallback', 'scaffold', 'unmatched', 'missing'}.

    Reads the runtime fingerprint from component_result and compares to:
      - component_spec['primary']                  exact string match -> 'primary'
      - component_spec.get('allowed_fallbacks',[]) any exact match    -> 'fallback'
      - component_spec.get('scaffold_probes',[])   probe_id match     -> 'scaffold'
      - else                                                          -> 'unmatched'

    If component_result['status'] != 'OK', returns 'missing' (no fingerprint to compare).
    """
    if component_result.get("status") != "OK":
        return "missing"
    fp = component_result.get("fingerprint")
    if fp is None:
        return "missing"
    if fp == component_spec.get("primary"):
        return "primary"
    if fp in (component_spec.get("allowed_fallbacks") or []):
        return "fallback"
    for probe in component_spec.get("scaffold_probes") or []:
        if isinstance(probe, dict) and fp == probe.get("probe_id"):
            return "scaffold"
        if isinstance(probe, str) and fp == probe:
            return "scaffold"
    return "unmatched"

# classify(component_results, contract_components, ...) -> (state, reasons_dict)
# composes _matched_role() across all declared components and returns the
# worst-priority state per the STATES ordering above. Body omitted here.
