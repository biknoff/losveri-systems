# Los Verí Systems

**If you're evaluating me for technical program / AI systems work, start here (60 seconds):**
- **[VERIFICATION.md](VERIFICATION.md)** — how I know a launch is safe
- **[METHOD.md](METHOD.md)** — how I coordinate AI-built technical work
- **[HADIT](kubera/hadit/engine/)** — one end-to-end production case
- **[DECISIONS.md](kubera/hadit/engine/DECISIONS.md)** — how tradeoffs and rejected alternatives are recorded

A verification-first approach to building and operating production systems with AI agents — proven where being wrong is expensive: a live trading engine, a household of AI copilots that non-technical people use every day, and a research program disciplined enough to publish its own mistakes.

**What this repo proves, concretely:**
- Every change to the live trading engine is rehearsed against a byte-identical copy of the running system before it touches production — not "should behave the same," mechanically proven identical on every build.
- The processes watching that engine can flatten it, halt it, and page a human — and that is *all* they can do. None of them can place, modify, or author an order; the boundary is structural, not a policy.
- Internal AI tools — a finance ledger driven by voice notes, a shared multilingual comms gateway, a voice-interfaced daily coordinator — are in real daily use by people who don't write code, not demos run once for a screenshot.
- Every claim above has an evidence file sitting next to it in this repo: a certification log, a real config diff, a redacted code excerpt. Nothing here asks to be taken on faith.

This was all built and is still run by two people. [METHOD.md](METHOD.md) explains how; [VERIFICATION.md](VERIFICATION.md) explains how every claim here gets checked; [STORY.md](STORY.md) explains how the pieces connect (including the names — Abraxas, NUIT, HADIT — which are covered in one page and never load-bearing for understanding what a thing does).

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
| **HADIT Cockpit** | The family's own web trading cockpit — each of 27 data panels degrades independently rather than taking the whole surface down; watchers/watchdog push status in real time, not polled | RUNNING | `kubera/hadit/cockpit/` |
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
