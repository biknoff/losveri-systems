# Architecture

## 1. The symlink / byte-identity mechanism

The mirror's build tree is generated, never hand-edited:

- **A pristine snapshot** — the live engine's working tree (not `git HEAD`; the working tree is
  what is actually deployed) pulled read-only over one `tar` stream, unpacked, and `chmod -R a-w`.
  Recorded in a manifest: an md5 per file, the live tree's git head, and the pull timestamp.
- **The build tree** — mostly (**372 of 373 files**) symlinks straight into the pristine snapshot,
  so the compiler reads the live engine's actual bytes. A small number of files are real copies
  only where the toolchain itself must write through them (lockfiles, generated manifests) — a
  symlink there would write back into the pristine snapshot, which must never happen.
- **One patch layer** — a single file (a governance/sizing module) is produced by mechanically
  applying a small, declared patch: six edits, each of the exact shape `fn X(` → `pub fn X(`.
  Nothing else changes. The functions being exposed are the live module's own clock-and-path
  injected variants — private in production only because the sole callers there are the module's
  two-line wall-clock wrappers. Rust visibility has no runtime semantics; the patch does not touch
  behavior.
- **A three-check verifier**, run at every build and before every rehearsal run, exit 0 or exit 2
  (no silent-warning path):
  - **Check A** — every file in the pristine snapshot still matches its recorded manifest hash
    (catches anything writing into the snapshot, including a build tool through a symlink).
  - **Check B** — the one patched file, with the declared patch mechanically *reversed*, reduces
    to byte-identity with the snapshot; every other file in the build tree is still a symlink, not
    a copy (catches an undeclared edit, a symlink silently swapped for a copy, or a patch that does
    more than it claims).
  - **Check C** — a fresh re-hash of the live host's working tree still matches the manifest
    (catches the live tree moving out from under the mirror).
  - Enforced in three independent places so it cannot be skipped by forgetting: at compile time
    (a tampered tree fails to produce a binary), before every rehearsal run, and baked into every
    output artifact as a provenance stamp (source git head, pull timestamp, and a hash rollup of
    the whole snapshot) — so a result file alone tells you which engine produced it.

Patch edits are anchored by unique surrounding text, not line number, so a change that moves the
patched functions around in the file does not silently break the mirror — a rename or removal
fails loudly instead, because that is a real seam change that needs a human.

## 2. The shim broker

The rehearsal harness routes the **unmodified** live engine's broker calls to a shim process that
impersonates the live gateway protocol, backed by a real venue-matching library rather than a
hand-rolled fill model:

- **Matching + simulated account** come from a genuine backtest matching engine (native, no
  scripting-language bindings in the dependency graph) — real order types, a real fill model, a
  real simulated exchange.
- **Broker-personality state** is layered on top and is authoritative for anything the wire
  protocol exposes: ticket table, netting-consolidated positions (merge / reduce / flip, surviving
  ticket id), deal history, balance/equity/margin arithmetic in the broker's own convention (fixed
  per-contract margin, not a leverage model) — because that is what a live gateway would answer,
  and it can differ from the matching engine's own internal bookkeeping (which is kept only as a
  cross-check).
- **Single-threaded by design.** Every venue interaction is synchronous, so a query can never
  observe a half-applied fill — a fill from an in-flight command lands atomically before any reply
  is sent. This determinism is what lets rehearsal runs reproduce bit-for-bit.
- Pre-trade validation (reject codes, invalid-order classes) is implemented at the personality
  layer to match the real venue's denial semantics, not the matching library's own generic risk
  checks, which would add reject classes the real venue does not have.

## 3. The acceptance harness

Formal acceptance replayed a real historical live window **segmented at the live engine's actual
restarts**, each segment run under the exact binary and environment that traded it (fetched from
rollback copies, hash-verified), seeded from live ground truth at each boundary — not one
continuous run under today's code. A separate full-window run under the *current* binary,
same seed, isolates what recent deploys changed. Every live order-lifecycle row is matched to a
rehearsal row by leg identity and nearest placement time, and every unmatched or mismatched row is
assigned to a named cause class (exact reproduction; tape/clock resolution limit; a fabricated or
unrecoverable seed input; or a genuine defect in the shim) — never left unexplained. One real
defect was found this way, root-caused, fixed, regression-tested, and every affected run was
re-run before acceptance closed.

## 4. The nightly reconciliation pipeline

A systemd timer fires nightly; it runs a driver script that pulls the day's tick/bar data,
regenerates a governed replay (the same law-in-loop engine code the mirror links, not an
independent model), and diffs it against the live engine's witness spine — the append-only record
of what actually happened, not the engine's live memory. Each live/expected pair is matched by
leg identity, session, and price tolerance, then classified: exact match, one of a fixed list of
*known* explained-yellow classes (a documented governance gate, a sizing clamp, a resting order
with no exit yet, …), or unexplained-red. A verdict and digest are written and pushed; anything
still unexplained is red by construction, not silently dropped.

## 5. Boundaries

- **Read-only on live, always.** The mirror's pristine snapshot is pulled over one read-only
  stream and `chmod a-w`'d; nothing in the mirror edits, deploys to, or restarts the live host.
  Verified, not just asserted: the provenance checks above fail loudly if that boundary is ever
  crossed.
- **Recon consumes the witness spine; it cannot order.** The nightly reconciler reads the witness
  log and venue-truth records after the fact. It has no path to place, modify, or cancel a live
  order — the same "watcher cannot author" separation applied to supervision elsewhere in this
  repo (see [STORY.md](../../STORY.md), [VERIFICATION.md](../../VERIFICATION.md)).
- **The deploy gate is a human decision, evidence-backed.** The mirror produces an attributed
  rehearsal verdict against a fixed reference constant; a human reads it and decides whether to
  deploy. The mirror does not deploy itself.
