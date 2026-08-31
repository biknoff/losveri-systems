# SOURCE: src/governance/receipt_builder.py — the receipt-log chain-link mechanism, real code,
# unedited except for the surrounding docstring/comment trim. This is the append-only chain
# discipline applied to the Logia receipt log (a sibling mechanism to the phase-envelope chain
# described in ARCHITECTURE.md / EVIDENCE/hash_chain_provenance.md — same idea, one layer down:
# every receipt links to the canonical hash of the one before it).
# REDACTED: nothing — no secrets, no strategy content, pure chain-linking logic.

import hashlib
import json
import pathlib
from typing import Any

EMPTY_CHAIN = hashlib.sha256(b"").hexdigest()


def _canonical(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _compute_prev_hash(log_path: pathlib.Path) -> str:
    """Read last line of the log and hash its canonical JSON.

    Returns EMPTY_CHAIN if the file does not exist or is empty.
    """
    if not log_path.exists():
        return EMPTY_CHAIN
    content = log_path.read_text(encoding="utf-8").strip()
    if not content:
        return EMPTY_CHAIN
    last_line = content.rsplit("\n", 1)[-1]
    last_entry = json.loads(last_line)
    return hashlib.sha256(_canonical(last_entry)).hexdigest()


# Every new receipt written to the append-only JSONL log carries this value as its own
# `prev_hash` field — the same "walk backward, first broken link stops you" property as the
# phase-envelope chain, applied at receipt granularity instead of phase granularity.
