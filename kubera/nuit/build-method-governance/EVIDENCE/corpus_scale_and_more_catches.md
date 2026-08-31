<!-- WHAT: (1) a verified re-count of the HANDOFF-shaped document corpus across both machines that
     hosted this build (the research host and a separate Mac-side cache), correcting an earlier undersell; (2) a
     read of an unopened governance-artifact zip's file listing; (3) three additional real,
     redacted integrity-catch examples drawn from the receipts/ corpus already pointed to (not
     duplicated) by spectral-minesweeper/EVIDENCE/receipts_and_seals.md. REDACTED: candidate/cluster
     identifiers, exact PF/trade-count values tied to a specific strategy, and any gate-threshold
     numbers are replaced with <redacted>; QA-level counts (violation counts, file counts, dates)
     are kept because they describe process outcomes, not strategy content. -->

# Corpus scale, re-verified — and three more integrity catches

## The undersell, corrected

`seals_inventory.md` (this project) and `spectral-minesweeper/EVIDENCE/receipts_and_seals.md`
both state "50 receipts" for one directory — `5th-house-kubera/receipts/` on the research host. That count is
still accurate for that directory (49 dated files + 1 `README.md` = 50, re-verified). What it
undersold is scope: that's one receipts folder in one repo. The "handoffs as artifacts" discipline
ran across the whole multi-month, multi-machine build, and the real corpus is much larger and
messier than a single folder count implies.

**Re-counted directly, this pass** (`find … -iname 'HANDOFF*.md'`, both machines):

| | Raw file matches | Distinct basenames (dedup'd across mirrored trees) |
|---|---|---|
| the research host (`/home/nuit/repos`) | 223 | 139 |
| Mac (`/Users/leo/Los Veri`) | 197 | 115 |

Neither number is the "real" corpus size on its own, and they do **not** simply add (223+197 or
139+115) — most of the gap between raw and distinct counts is the same document sitting in more
than one mirrored directory tree:

- On the research host, `5th-house-kubera-infra/receipts/` (16 files) is a **strict subset** of
  `5th-house-kubera/receipts/` (38 files) — a stale partial mirror, not new content.
- On the Mac, the same underlying project exists as at least three separate directory trees —
  `HADIT/intel/repos/5th-house-kubera` (a partial mirror of the the research host repo), a Google-Drive-style
  project folder (`5th House - Kubera-chemotactic`, `5th House - Kubera-room-5b-bc`), and a further
  `HADIT/intel/colossus_mirror` copy — each catching a different, incomplete slice of the same
  handoff history.

Diffing basenames the research host-vs-Mac directly: **66 shared, 73 the research host-only, 49 Mac-only** — 188 distinct
named documents across both machines by this measure. This is a basename-level dedup (fast, and
conservative against over-counting identical files under different directories); it is not a
byte-level content diff, so it should be read as an estimate, not an audited total. What it proves
cleanly: the Mac cache is **not** simply "the same 50-ish receipts, mirrored" — 49 Mac-only
basenames exist nowhere on the research host, and conversely the research host holds 73 that never reached the Mac. Both
caches are genuinely partial, independently, of one larger project history neither machine holds
in full.

**Bottom line for any future corpus-scale claim in this repo:** state "roughly 150-220 distinct
handoff/audit/dispatch documents across two machines and several mirrored trees, of which one
project directory's 50-file `receipts/` folder and 17-file `seals/` folder are the fully-verified,
individually-inventoried subset this repo's evidence is built from" — not a bare "50 receipts, 17
seals" implying that is the whole corpus.

## An unopened bundle, worth a further look

`Governance Spectral Minesweeper v3.zip` (Mac, under `5th House - Kubera-chemotactic/Spectral
Minesweeper v3/`) is a 42-file, ~238KB governance-artifact bundle never previously opened. A
listing-only pass (`unzip -l`) shows it holds four named-role governance briefs, each paired with
its own commission/handoff artifact — `FOREMAN_GOVERNANCE_v1.md`, `BUILDER_GOVERNANCE_sealed.md`,
`DANIEL_CLI_PROTOCOL_v1.md`, `VM_CAPACITY_PROTOCOL_v1.md` — none of which are currently evidenced
anywhere in this repo (the existing evidence covers the crypto-envelope chain and the
mortal-architect succession, not the Foreman/Builder/Daniel/VM-capacity role governance layer this
zip documents). It is genuinely additive: a fourth governance sub-system (role/permission
boundaries for the Foreman, Builder, and Daniel CLI roles) sitting alongside the crypto-seal layer
this project already documents, not a duplicate of it. Worth a future evidence pass; not opened
further here beyond the one bounded peek (`DANIEL_CLI_PROTOCOL_v1.md` head) used to confirm what
"Daniel" names — see `LINEAGE.md` § 2.

## Three more integrity catches, same rigor as the LOCK-19 rebind

All three are real, on-disk, dated 2026-05-05/06/07, drawn from the same `receipts/` directory
`spectral-minesweeper/EVIDENCE/receipts_and_seals.md` already points to without opening.

### 1. A compliance mongoose caught a real engine bug it was built to catch

**What broke:** the trading engine mishandled five specific CME early-close sessions (day before
July 4th, day after Thanksgiving, MLK Day, and others) — trades on those days violated the
force-flat cutoff window. 40 of 66 daily clusters (61%) and 43 of 69 hourly clusters (62%) in the
affected batch carried the violation.

**How it was caught:** a downstream compliance-checking stage (`V_deploy_report`), built
specifically per its own commission spec to assert force-flat-window compliance on every cluster,
flagged all of them — described in the receipt itself as "exactly what V_deploy_report was designed
to catch," and noted as a case where drift "should have been caught by LEDGER pre-flight" but
instead was caught one stage downstream, not missed entirely.

**How it was resolved:** per the commission's own rule, a compliance violation does not
auto-disqualify a candidate — `compliance_clean: false` is set and propagated forward as an
annotation for a human decision point, not silently dropped or silently passed. The engine fix
itself was spun out as a separate, explicitly deferred commission rather than rushed inside the
audit. The one candidate under live consideration at the time was independently confirmed to fall
outside the violation window before the team relied on that fact.

### 2. A silent metric bug — a "filtered" count that was never actually filtering

**What broke:** a regime-filtering function looked for a per-trade `regime` field that the upstream
backtest engine never emitted. The result: a metric labeled "regime-filtered trade count" silently
equaled the full unfiltered count on every run — a number that looked meaningful and wasn't, with
no error or warning anywhere in the pipeline.

**How it was caught:** an audit cross-referenced the metric's on-disk values against four
independent values already trusted from a separate, already-sealed stage (`V_oos`); once the bug
was hypothesized, all four reproducer values matched the corrected interpretation to zero error —
confirming it as a real bug, not a definitional ambiguity.

**How it was resolved:** the fix landed with both the pre-fix and post-fix data snapshots kept side
by side on disk (`*.PRE_BUGFIX.jsonl`, never overwritten) — the same provenance-over-erasure
instinct as the LOCK-19 companion-tag rebind, applied without any crypto envelope involved this
time, just file-naming discipline. A new regression test was added, and idempotency was re-run and
confirmed (all clusters byte-identical across repeated runs, zero mismatches) before the fix was
considered sealed.

### 3. Adjudicating someone else's audit — disagree in one place, confirm-and-flag in another

**What happened:** an *external* auditor (outside this build's own agent chain) submitted findings
against the pipeline. Rather than accept or wave off the findings wholesale, the team formally
disposed of each one with cited evidence:

- One finding claimed a dispatch stage was silently producing no usable output. Disposition:
  **disagree, stale** — re-inspecting the specific on-disk run artifact the auditor would have seen
  showed real trade data was present; the auditor had evidently examined an earlier run that had
  since been superseded, not the current one.
- A second finding claimed a UTC-midnight session-boundary bug was inflating a risk metric for
  roughly 2% of trades. Disposition: **confirmed, already fixed** — true bug, already fixed before
  the audit's evidence date, in an engine change not itself surfaced in any receipt at the time.
  The team's own corrective action was not to just close the finding, but to flag forward that
  older, pre-fix artifacts elsewhere on disk (<redacted count>-candidate batch) could still carry
  the inflated values and should be regenerated before any downstream reuse.

This third pattern is distinct from the first two: it is not the team catching its own mistake, but
a documented, evidence-cited accept/reject/disclose adjudication of an outside party's review — the
same "trust only what's written down and checkable" discipline, exercised against external input
rather than only internally.
