# Boot-time fleet reconciliation — source docstring

**What this is:** the module docstring of `reconcile_boot_fleet.py`, the script that reconciles the declared per-account MT5 container fleet after a host or Docker restart. This is the architecture headline for Miami: the fleet does not just start on boot, it is *reconciled to a declared state*, one container at a time, with memory headroom checked before each start.

**Redactions:** none needed — the source contains no hostnames, IPs, or account identifiers by design (see the docstring itself: "It never embeds users, accounts, or credentials").

---

```
Reconcile the declarative Hadit MT5 fleet after Docker/host startup.

The cockpit owns account configuration; this helper owns only boot recovery.  It never embeds
users, accounts, or credentials.  Desired containers come from fleet_registry.json, and missing
or stopped shells are brought up one at a time to avoid a 25-prefix Wine startup spike.
```

**Behavior, read from the source:**
- Desired state: a JSON registry of accounts, each mapped to a container name.
- For each declared account: check container state (`absent` / `running` / other) via `docker inspect`.
- `absent` → wait for memory headroom, then `docker compose up -d --no-deps <service>`.
- Every declared container (regardless of prior state): repair its restart policy to `unless-stopped` and its memory/memory-swap caps — this heals containers whose settings drifted, or that predate the current generated compose file.
- Not `running` → wait for headroom, `docker start`, then stagger before moving to the next account (default 8 seconds) — the fleet comes up in a controlled trickle, not a stampede.
- The whole pass runs under a file lock (`flock`) so a concurrent boot invocation cannot race itself.

This is boot-time self-healing for a fleet of per-account containers, deliberately scoped to *never* touch credentials or account configuration — that stays in the cockpit's domain.
