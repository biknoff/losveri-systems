# Excerpt from nuit_identity_watcher.py — the fleet's shared transition-driven
# alert pattern (verbatim structure, symbols renamed only where they named
# an internal field; no strategy/account identifiers were present in this
# excerpt to begin with).
#
# Shape: page on a bad transition, re-page on a cooldown while it persists,
# send exactly one RECOVERED note when it clears. Never a heartbeat, never
# silent-fails a page (a raised exception here returns non-zero so the
# process supervisor's own liveness check notices).

prev_level = state.get("level", "match")
last_page = state.get("last_page_ts", 0)

send_msg = None
if level in ("mismatch", "unprovable"):
    if level != prev_level or now - last_page >= REPAGE_S:
        head = ("CRITICAL — ACCOUNT IDENTITY MISMATCH" if level == "mismatch"
                else "CRITICAL — ACCOUNT IDENTITY UNPROVABLE")
        send_msg = (f"[NUIT IDENTITY] {head}\n{stamp} · market {market}\n"
                    + "\n".join(lines)
                    + "\nDo NOT trust the cockpit header until this recovers.")
        state["last_page_ts"] = now
elif prev_level in ("mismatch", "unprovable"):
    send_msg = (f"[NUIT IDENTITY] RECOVERED — all identity sources agree\n"
                f"{stamp} · market {market}\n" + "\n".join(lines))

if send_msg:
    _kind = "RECOVERED" if level == "match" else "FIRING"
    send_msg = sev_prefix("RECOVERED" if _kind == "RECOVERED" else "CRITICAL",
                          "NUIT IDENTITY") + "\n" + send_msg
    resp = tg_send(send_msg)
    append_alert(SELF_KEY, "CRITICAL", _kind,
                 f"account identity {level}: " + " · ".join(lines[:4]))

state.update({"level": level, "sources": sources, "last_cycle_ts": now})
save_json(args.state_path, state)
