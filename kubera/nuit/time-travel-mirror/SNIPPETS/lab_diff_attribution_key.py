# SOURCE: bugatti_cockpit/lab_diff.py — canon-vs-rehearsal round-turn matching key.
# REDACTED: none needed — this is pure matching/indexing logic over generic record fields
# (instrument, leg, tag, timestamps); no strategy parameters, no account or P&L data.
#
# The point: matching keys collision-check themselves and escalate to a wider key rather than
# silently overwriting one round-turn's record with another's when two rows share a key.

def _key(r, with_exit_ts=False):
    k = (r["instrument"], r["leg"], r.get("exit_name") or "", r["entry_ts_ns"])
    return k + (r["exit_ts_ns"],) if with_exit_ts else k


def _index(rows):
    idx, collisions = {}, 0
    for r in rows:
        if r.get("exit_name") == "EndOfData":
            continue
        k = _key(r)
        if k in idx:
            collisions += 1
        idx[k] = r
    if collisions:  # disambiguate with exit_ts_ns and re-check
        idx, collisions = {}, 0
        for r in rows:
            if r.get("exit_name") == "EndOfData":
                continue
            k = _key(r, with_exit_ts=True)
            if k in idx:
                collisions += 1
            idx[k] = r
    return idx, collisions

# Caller contract (from the module docstring): "A key collision makes the diff INVALID rather
# than silently corrupting it." — if disambiguation still collides, the diff run is expected to
# refuse rather than publish a mismatched attribution.
