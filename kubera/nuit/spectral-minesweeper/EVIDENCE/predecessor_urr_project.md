<!-- What: structural evidence that a predecessor project (URR, April 2026) directly preceded and
     fed into what became NUIT — dated documents, directory names, and governance artifacts. What
     is deliberately absent: the trading mechanism URR investigated, its parameters, and its
     performance figures — trade-secret "reconstructive detail" per this repo's redaction policy.
     Everything below is process/infrastructure evidence, never the edge. -->

# The predecessor: URR (April 2026)

Before "NUIT" was the name of anything, a single-pattern research project — workspace name
`5th House/urr_15m_fractal/`, dated 2026-04-17 — was already building the infrastructure NUIT
would later generalize. Real, dated, on-disk artifacts:

- **`URR_Research_Console_Architecture_20260417.md`** — a full systems-architecture document for
  a local web research console: one shell, shared chrome components, a health-color-coded panel
  system, explicitly timeframe-plural (parallel workspaces per timeframe, one shared console).
- **`URR_System_Specifications_20260417.md`** — a config-driven registry of every candidate system
  under research: each with its own hashed config ID, its own health status (`under_review`,
  re-scored on a cadence), its own config file as the single source of truth for parameters — the
  same "never trust memory, trust the file on disk" discipline that later hardened into the
  mongoose-determinism contract.
- **`stress_battery/`** and **`mechanism_discovery/`** — two dedicated tool directories: one for
  pre-declared adversarial stress testing, one for competing-hypothesis falsification testing
  (the deployment spec for the project's first live-ready system cites falsification tests run
  against "4,104 combined IS+OOS trades across 6 sibling configs" before any mechanism story was
  trusted — the count is cited here as evidence of rigor; the mechanism itself is not).
- **A formal deployment contract**, multi-party signed: authored by Abraxas, approved by a human
  operator, audited and signed off by a separate AI reviewer, status `LOCKED` ("no parameter
  tuning allowed; only per-trade logging may evolve"). Its own document header states:
  **`supersedes: none (first NUIT deployment spec)`** — this is the literal first document to
  carry the NUIT name, and it names URR as what it supersedes.
- **Real automation**: `~/Library/LaunchAgents/com.losveri.urr-*.plist` — scheduled pipeline jobs,
  not a one-off script.
- **Real cross-agent handoffs**: `claude_codex_handoffs/kubera_mushaka_urr_v1_nautilus_verify.md`
  — Kubera and a planning/execution agent role were already coordinating on this project before
  NUIT existed as a name.

## Why this belongs in the record

Every discipline this repo documents as NUIT's own — the reusable-template-over-one-result
philosophy, pre-declared adversarial gates, config-as-source-of-truth, multi-party AI+human
sign-off before anything goes live — is independently visible here, a project earlier, under a
different name, at smaller scale. See [LINEAGE.md](../../../../LINEAGE.md) § 2 for the fuller
account of how URR's own paper trail names itself NUIT's origin point.
