# file: SNIPPETS/idempotency_check.py
# source: mongooses/mongoose_v_is.py (5th-house-kubera, branch cocktail-v3), ~lines 1299-1376
# excerpted read-only; math/thresholds elsewhere in the file are NOT reproduced here.
#
# What this shows: LOCK-20's idempotency contract as actually implemented — the
# engine is dispatched TWICE per candidate and the two output hashes must match
# exactly, or the candidate is marked IDEMPOTENCY_MISMATCH and excluded from the
# pass set. There is no retry-and-average, no "close enough." Hash-identical or halt.

# f. dispatch engine twice (LOCK-20 idempotency_proof)
cand_run_dir = run_dir / cid
cand_run_dir.mkdir(parents=True, exist_ok=True)
cand_path = cand_run_dir / "candidate_payload.yaml"
cand_path.write_text(
    yaml.safe_dump(payload, sort_keys=True, default_flow_style=False),
    encoding="utf-8",
)
engine_brief = {
    "candidate_path": str(cand_path),
    "ocs_path": str(ocs_path),
    "data_path": brief["data_path"],
    "is_start": brief["is_start"],
    "is_end": brief["is_end"],
    "seed": int(brief["seed"]),
    "costs_spec": brief["costs_spec"],
}
brief_path = cand_run_dir / "brief.json"
brief_path.write_bytes(_cjs_v1(engine_brief))

timeout_seconds = int(brief.get("engine_timeout_seconds", DEFAULT_ENGINE_TIMEOUT_SECONDS))
try:
    output_run1, hash_run1 = _dispatch_engine_subprocess(brief_path, timeout_seconds=timeout_seconds)
    output_run2, hash_run2 = _dispatch_engine_subprocess(brief_path, timeout_seconds=timeout_seconds)
except EngineTimeout as exc:
    # R10a per Leo decision 2026-04-26: TIMEOUT disposition;
    # candidate is v2-valid, engine couldn't complete within budget.
    per_candidate.append({
        "candidate_id": cid,
        "declared": declared,
        "feasibility_filter_disposition": disposition,
        "engine_disposition": "TIMEOUT",
        "engine_disposition_detail": str(exc),
        "engine_invoked": True,
        "idempotency_proof": None,
        "is_pass": False,
        "albedo_metrics": None,
        "per_trade_summary": None,
        "engine_run_dir": str(cand_run_dir),
    })
    n_engine_error += 1
    continue
except Exception as exc:
    ...  # ERROR disposition, same shape, omitted here

idem_match = (hash_run1 == hash_run2)
if not idem_match:
    per_candidate.append({
        "candidate_id": cid,
        "declared": declared,
        "feasibility_filter_disposition": disposition,
        "engine_disposition": "IDEMPOTENCY_MISMATCH",
        "engine_disposition_detail": (
            f"LOCK-20 violation: run1={hash_run1} run2={hash_run2}"
        ),
        "engine_invoked": True,
        "idempotency_proof": None,
        "is_pass": False,
        "albedo_metrics": None,
        "per_trade_summary": None,
        "engine_run_dir": str(cand_run_dir),
    })
    n_engine_error += 1
    continue

# Persist run1 output only after the two hashes agree.
(cand_run_dir / "engine_output_run1.json").write_bytes(_cjs_v1(output_run1))
(cand_run_dir / "engine_output_run2_hash.txt").write_text(hash_run2 + "\n", encoding="utf-8")
