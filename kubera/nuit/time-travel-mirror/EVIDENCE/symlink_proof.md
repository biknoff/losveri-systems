<!-- WHAT: excerpt of the mirror's own README + honesty doc describing the symlink/patch mechanism
     and its verifier. REDACTED: local filesystem paths and hostnames replaced with generic
     role names (live-host / mirror-host); nothing else — this section is architecture
     description, no P&L, no account data, no strategy logic. -->

# The byte-identity claim, mechanically proven

From the mirror's build record (2026-07-25):

> The backtest links live-host's actual engine-tree crates — **372 of 373 engine-tree files are
> symlinks into a pristine, chmod-a-w copy of live-host's bytes**, and the one remaining file
> differs from live-host by **six `pub ` tokens and nothing else**, mechanically proven on every
> build.

## The verifier — three checks, exit 0 or exit 2, no third outcome

| | check | catches |
|---|---|---|
| **A** | every file in the pristine snapshot still matches the recorded manifest hash | anything on the mirror host editing the pristine copy (incl. a build tool writing through a symlink) |
| **B** | the build tree, with every declared patch **mechanically reversed**, is hash-identical to the snapshot; every non-patched file is still a **symlink** | an undeclared edit inside an engine module; a symlink swapped for a copy; a patch that does more than it claims |
| **C** | a fresh re-hash of the live host's working tree still matches the manifest | the live tree changing under the mirror — i.e., staleness |

**Negative controls, actually run** (all exit 2 — the verifier does not just pass when everything
is fine, it was proven to fail when things are not):

- appended one comment line to the one patched file → check B failed: "does NOT reduce to live
  bytes when patches are reversed — there is an UNDECLARED edit"
- replaced a symlink with an identical byte-for-byte copy → check B failed: "is a real file but no
  patch declares it"
- corrupted one manifest hash → check A failed ("snapshot MODIFIED") **and** check C failed
  ("live host CHANGED — mirror is stale, re-pull and re-prove")

## Enforced in three places, so it cannot be skipped

1. The build itself runs checks A+B at compile time and refuses to produce a binary if either
   fails (a deliberate, visible env-var escape hatch exists for debugging only).
2. The rehearsal runner re-checks before launching any run and refuses on failure.
3. Every output binary and every result artifact is **stamped** with the source git head, the
   pull timestamp, and a hash rollup of the whole snapshot — a result file alone tells you which
   engine version produced it.

## The patch itself — visibility-only, by construction

Six edits, each of the exact form `fn X(` → `pub fn X(`, applied to one governance/sizing module.
The functions being exposed are the live module's own clock-and-path-injected variants; they are
private in production only because the sole callers there are the module's own two-line wall-clock
wrappers. Rust visibility carries no runtime semantics — the verifier's check B proves this
mechanically (patch reversed ⇒ byte-identical) rather than asking anyone to take it on faith.
