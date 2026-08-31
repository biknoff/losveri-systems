# Excerpt from nuit_common.py — the ONE channel every watcher uses to reach
# the execution host. Every caller passes a read/query script; nothing in
# the fleet constructs an order-placement, modification, or cancellation
# call through this function (verified by grep — see
# ../EVIDENCE/readonly_boundary.md). Redacted: host constant names only
# (become generic placeholders below); the real constants never named a
# hostname in the source itself either — they were already opaque config
# values.

def exec_read_only(script: str, timeout: int = 60) -> str:
    """Run a read-only bash script on the execution host (b64-wrapped, no
    quoting issues). Returns stdout. Raises on any channel failure.
    stderr is ignored unless stdout is empty."""
    import paramiko  # local import: keeps module importable without paramiko for tests

    pw = open(EXEC_HOST_PW_FILE).read().strip()
    b64 = base64.b64encode(script.encode()).decode()
    cmd = "printf %s " + b64 + " | base64 -d | bash"
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # key-first, password kept as in-call fallback only
        c.connect(EXEC_HOST, username=EXEC_USER, password=pw, timeout=20,
                  key_filename="~/.ssh/id_ed25519",
                  allow_agent=True, look_for_keys=True, banner_timeout=20)
        _, o, e = c.exec_command(cmd, timeout=timeout)
        out = o.read().decode()
        err = e.read().decode()
    except Exception as exc:
        raise ExecHostError(f"{type(exc).__name__}: {exc}") from exc
    finally:
        c.close()
    if not out.strip() and err.strip():
        raise ExecHostError(f"remote stderr, empty stdout: {err.strip()[:400]}")
    return out

# Every watcher calls this with a query/read script only — e.g. "cat
# state/engine_status.json", a positions/orders READ verb against the
# exec-gateway, or a witness-log grep. The channel itself has no concept of
# a write; the boundary is enforced by what callers choose to send, and an
# audit of every caller in this codebase found zero order verbs (see
# EVIDENCE/readonly_boundary.md).
