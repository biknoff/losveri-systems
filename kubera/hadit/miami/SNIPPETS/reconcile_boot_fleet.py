# Source: deploy/reconcile_boot_fleet.py — the fleet reconciler (near-verbatim, no redactions
# needed: the source deliberately embeds no hostnames, IPs, or account identifiers).
#
# What this shows: boot-time self-healing of a fleet of per-account containers. The
# reconciler owns bringing declared containers up to their declared state; it never
# owns account configuration (that stays in the cockpit).

"""Reconcile the declarative Hadit MT5 fleet after Docker/host startup.

The cockpit owns account configuration; this helper owns only boot recovery. It never
embeds users, accounts, or credentials. Desired containers come from fleet_registry.json,
and missing or stopped shells are brought up one at a time to avoid a Wine startup spike.
"""
import fcntl
import json
import time
from pathlib import Path

MIN_AVAILABLE_MB = 1536
STAGGER_SECONDS = 8.0


def available_mb() -> int:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) // 1024
    return 0


def wait_for_headroom() -> None:
    while available_mb() < MIN_AVAILABLE_MB:
        print(f"fleet boot: waiting for memory headroom ({available_mb()} MiB available)")
        time.sleep(10)


def main(registry_path: Path, lock_path: Path) -> int:
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)  # a concurrent boot pass cannot race itself
        payload = json.loads(registry_path.read_text())
        accounts = payload.get("accounts") or {}
        for login, spec in accounts.items():
            name = f"mt5_{login}"
            state = container_state(name)          # docker inspect -f '{{.State.Status}}'
            if state == "absent":
                wait_for_headroom()
                compose_up(name)                    # docker compose up -d --no-deps <service>
                state = container_state(name)
            # Repair legacy containers whose policy drifted, or that predate the
            # generated compose file's resource stanza — every pass, not just on create.
            repair_restart_policy_and_memory_caps(name, spec)
            if state != "running":
                wait_for_headroom()
                docker_start(name)
                time.sleep(STAGGER_SECONDS)         # controlled trickle, not a stampede
        return 0
