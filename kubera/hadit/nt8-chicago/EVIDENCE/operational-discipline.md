# Evidence: supervised runner discipline (successor deployment)

**What this is:** an excerpt from a private operational memory document describing the
live-runner behavior of the *successor* NT8-era deployment (internally called
HaditFugue), a supervised Windows-hosted runner that came after the Chicago install
described in the rest of this directory. It is included here because it documents the
operational maturity the Chicago-era work fed into, on the same NT8/Windows platform
lineage, before that lineage was retired outright.

**Redactions applied:** host/path details generalized (no hostnames, no account
identifiers); component and mechanism descriptions kept.

## Excerpt (redacted)

> Restart = python node only (never the trading platform): kill the runner process by
> commandline match, supervisor script relaunches it in ~5-8s via a launch batch file.
> Verify after restart: `transport=WIRED armed=True` in the live log. Config (state,
> cushions, leg bases) is cached at startup — config edits need a restart to take effect.
> Don't restart during an armed funded-leg window unless the trigger is far
> out-of-the-money. [path/host details redacted]
>
> Tick recording (added 2026‑06‑09): the live tape was being discarded; an additive actor
> (`tick_recorder.py`, env-gated, default ON) now tees trade ticks to a local Parquet
> catalog, flushing every 5000 ticks / 60s, with a health JSON file. Verified writing.
>
> Also mentioned: a `multi_account_router.py` component (noted as safe to sync from the
> Mac source, unlike the runner file itself, which had diverged/been hand-patched live).

## Why this matters for the retirement narrative

Four disciplines are visible in this one paragraph, all of which read forward into the
Rust engine running today:

1. **Supervised auto-relaunch** — the runner is not trusted to stay up; a supervisor
   process watches and restarts it.
2. **Post-restart verification as a ritual, not an assumption** — `transport=WIRED
   armed=True` is checked in the log after every restart, not inferred.
3. **A restart-safety window rule** — restarts are deliberately withheld during an armed
   position window unless the risk is negligible. This is a hand-written version of the
   force-flat/armed-window guard logic that exists formally in the current engine.
4. **Config-cache awareness** — the team knew and documented that config changes require
   a restart to take effect, rather than discovering it live.

None of this eliminated the underlying fragility of a GUI-automated Windows platform —
it made that fragility *manageable* until it wasn't worth managing further.

**Source:** local memory document, read directly (no remote-host access needed for this
file).
