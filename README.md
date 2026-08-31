# Los Verí Systems

**Leo & Mariele Verí — operator + AI-architect builds, 2025–2026.**

> **If you're evaluating me for a role:** two people design, build, and operate production systems with AI agents — and supervise them safely. That means: internal-ops AI copilots for a small operating company used daily by non-technical operators (a finance ledger driven by voice notes, a shared comms gateway, multilingual staff coordination); a live, real-money trading stack with independent supervision that structurally cannot author trades; and a verification culture — byte-parity certification, adversarial audits, cryptographically sealed handoffs — that makes every claim in this repo checkable. Three docs show how: [METHOD.md](METHOD.md) (how we work with AI), [VERIFICATION.md](VERIFICATION.md) (how we know it works), [STORY.md](STORY.md) (how it fits together).

The through-line: **research into latent space** — disciplined search for latent structure, whether the hidden thing is a trading edge, a prosodic baseline, or a gesture in a conductance field.

This repo is a **curated evidence archive**, not a code mirror. The working repos are private (live capital, personal data). Each project here states what runs, what was built, and what is only designed — with evidence for every claim. Honesty is the aesthetic.

## How to read the labels

| Label | Means |
|---|---|
| **RUNNING** | live right now, doing its job daily |
| **BUILT** | finished and genuinely exercised (real runs on disk), not a continuous service |
| **BUILT+DORMANT** | finished, proven, deliberately parked |
| **BUILT+RETIRED** | ran in production, then superseded — the lineage is the point |
| **DESIGNED** | specified, not built — stated plainly |

## The projects

| Project | One line | Status | Where |
|---|---|---|---|
| **HADIT engine** | Rust execution engine + orchestrator for ~14 live strategies; witness logs, watchdog, nightly recon | RUNNING (real money) | `kubera/hadit/engine/` |
| **HADIT Cockpit** | The family's own web trading cockpit — ~34k lines, 15 pages, 27 named data feeds, real-time watcher/watchdog integration | RUNNING | `kubera/hadit/cockpit/` |
| **Time Travel Mirror** | Backtests compiled against the live engine's own bytes (372/373 files identical, proven per build); every deploy rehearsed here first; nightly reconciliation | BUILT | `kubera/nuit/time-travel-mirror/` |
| **NUIT watchers** | Independent supervision fleet over the live engine — 9 timers + a cron durable layer; the watcher cannot author what it watches | RUNNING | `kubera/nuit/watchers/` |
| **Spectral Minesweeper** | Discovery methodology: latent generative terrain from the geometry of outcomes; Cold-Firing validation chain ran; SEER/PROBE designed | BUILT + DESIGNED | `kubera/nuit/spectral-minesweeper/` |
| **Build Method + crypto governance** | GPG-sealed handoffs, hash chains, halt gates, mortal-architect protocol — how two people built all this with AI agents without losing epistemic integrity | BUILT+DORMANT | `kubera/nuit/build-method-governance/` |
| **HADIT Miami** | Multi-account MT5 trading service (connect a broker, trade, copy-trade); external users trade real money on it | RUNNING | `kubera/hadit/miami/` |
| **i-ii.trade** | The product: trade, draw, drop voice notes on the chart, share with friends — "together"; or run your strategy scheduler — "alone" | RUNNING (early product) | `kubera/hadit/i-ii-trade/` |
| **HADIT ⁄ NT8 (Chicago)** | The origin: Python strategy logic bridged into NinjaTrader 8 via a C# DLL, live-traded, then deliberately outgrown | BUILT+RETIRED | `kubera/hadit/nt8-chicago/` |
| **Abraxas** | The coordinating agent — the one agent the family talks to (by voice), which consults the domain agents below | RUNNING (daily) | `council/abraxas/` |
| **Kubera** | The quant-intelligence agent (formerly *Leona*) — the work realm's advisor, above all the trading builds below | BUILT+DORMANT (agent); its realm runs on | `kubera/` |
| **Fred** | The somatic layer: deterministic prosody measurement from longitudinal voice notes; decisions gate on the speaker's prosodic floor | PAUSED (verified) + detector BUILT+DORMANT | `council/fred/` |
| **Chris** | Household finance operator: voice-note an expense, it lands in the ledger | RUNNING | `council/chris/` |
| **Hanuman** | The comms gate: WhatsApp/Gmail protocols every agent invokes; sub-second local voice pipeline | RUNNING | `council/hanuman/` |
| **Fay** | Domestic coordination in Haitian Creole with the household staff | RUNNING (~months of daily use) | `council/fay/` |
| **CERCA** | Four-body bioelectric touch instrument — hardware, soldered; exhibited 2025; provisional patent filed, later lapsed | BUILT+EXHIBITED | `atelier/cerca/` |
| **Atelier portfolio** | Touch · Plant-Based Music · Grasping for Space · Colorful Sounds · Cromafonía · Chichigua (a kite instrument, built and flown) | mixed, labeled | `atelier/` |

## Start here

1. **[STORY.md](STORY.md)** — how it all connects (one diagram, five minutes).
2. **[VERIFICATION.md](VERIFICATION.md)** — the culture that makes the claims checkable.
3. **[METHOD.md](METHOD.md)** — how two people built this with AI, safely.
4. **[LINEAGE.md](LINEAGE.md)** — what came from what, including the mistakes.
5. Any project directory — each README stands alone.

*Every project directory: `README.md` (status + what it proves) · `ARCHITECTURE.md` · `EVIDENCE/` (redacted artifacts) · `SNIPPETS/` (small real excerpts) · `DECISIONS.md` (choices + the rejected alternatives). Identifiers, credentials, strategy parameters, and P&L are redacted throughout; each redaction is noted where it occurs.*
