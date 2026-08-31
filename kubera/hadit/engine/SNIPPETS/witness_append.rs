// Source: crates/engine/src/witness.rs (build clone). Redacted: nothing — this is the append
// function itself, not a data sample (see EVIDENCE/04_witness_spine_sample.md for a real,
// redacted event).
//
// WHAT THIS PROVES: append-only, create-if-missing, one file per spirit per ET trading day; a
// write failure is counted and logged loudly rather than silently dropped — the 2026-07-25 fix
// noted in the comment closed exactly the failure mode a witness spine cannot afford: losing an
// event with no trace that it was lost.

/// Append one witness event. Best-effort: a missing `witness_dir` is the caller's decision to
/// no-op, not this function's — call sites that hold `Option<PathBuf>` should skip calling this
/// when `None`.
pub fn append_event(
    witness_dir: &Path,
    ts_utc_ns: u128,
    spirit: &str,
    instrument: &str,
    account_id: &str,
    state: &str,       // ORDER_PLACED | ORDER_BLOCKED | CANCELLED | FILLED | EXIT | SIT_OUT
    detail: Value,
    ticket: Option<&str>,
    source: &str,
    dry_run: bool,
) {
    let session_date = crate::registry::et_session_date(ts_utc_ns as i64);
    let path = witness_path(witness_dir, &session_date, spirit);
    if let Some(dir) = path.parent() {
        if let Err(e) = std::fs::create_dir_all(dir) {
            witness_failed(&path, &format!("create_dir_all: {e}"));
        }
    }
    let record = serde_json::json!({
        "ts_utc_ns": ts_utc_ns.to_string(), "schema": SCHEMA, "spirit": spirit,
        "instrument": instrument, "account_id": account_id, "state": state,
        "detail": detail, "ticket": ticket, "source": source, "dry_run": dry_run,
    });
    use std::io::Write;
    // LOUD FAILURE (2026-07-25). This was `if let Ok(..) { let _ = writeln!(..) }`: an open or
    // write failure discarded the whole event with no log line and no counter — the
    // observability spine failing invisibly, which is the worst possible failure mode for a
    // spine. Still best-effort (a witness failure must never block trading), but never silent
    // again.
    match std::fs::OpenOptions::new().create(true).append(true).open(&path) {
        Err(e) => witness_failed(&path, &format!("open: {e}")),
        Ok(mut f) => {
            if let Err(e) = writeln!(f, "{record}") {
                witness_failed(&path, &format!("write: {e}"));
            }
        }
    }
}
