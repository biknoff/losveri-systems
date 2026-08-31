# METHOD — how two people built this with AI

Not "AI wrote our code." A specific working discipline, developed across two years, that lets a two-person team ship production systems with AI agents without losing control of what is true.

## The shape of the work

- **Operator + architect.** The operators (Leo & Mariele) own intent, requirements, risk decisions, and final acceptance. AI works as architect and builder — but commissioned, bounded, and audited, never free-running. Los Verí is a two-person research/build practice: Leo generally leads technical architecture, signal/domain theory, and low-level engineering; Mariele generally leads research implementation, requirements, AI-agent/collaborator orchestration, production, acceptance criteria, and verification. Many system and product decisions are joint.
- **Bounded commissions.** Work is delegated as scoped tasks with explicit acceptance checks, allowed surfaces, and required evidence. An agent that can't cite evidence for a claim doesn't get the claim into the record.
- **Fresh-eyes audit per phase.** Every substantive change is reviewed by an auditor that did not write it, before it integrates — and for anything touching live money, before it deploys. Audits have teeth: findings block until resolved (see VERIFICATION.md for a real example: an over-attribution bug caught by audit in an already-"working" change).
- **Handoffs as artifacts.** Sessions end with written handoff receipts — objective, decisions, evidence, open risks — so the next session (human or AI) starts from record, not recollection. At its most rigorous this became cryptographic: hash-chained, GPG-sealed handoffs across the AI-session boundary (`kubera/nuit/build-method-governance/`).
- **Label = substance.** Nothing is called "running" that is dormant, "patented" that lapsed, or "production" that is a scaffold. The four-state vocabulary (RUNNING / BUILT / BUILT+DORMANT / DESIGNED) is enforced in every document, including this repo about the repo.

## The guardrails that made it safe

- **The watcher cannot author.** Supervision systems (NUIT watchers) monitor the live engine but are structurally unable to create or modify trading candidates. Separation of discovery, execution, and supervision across separate hosts.
- **Rehearse before deploy.** Changes to the live engine are exercised in the Time Travel Mirror — compiled against the live engine's own bytes — before any live swap. Deploys happen in flat windows, with a written rollback marker (previous binary, hashes, one-command restore) before the swap.
- **Human gates at the money.** Arming live trading is a human's hand on an env file — never set by any unit or script. Halt latches clear only by human action.
- **Fail open to null, never fabricate.** A recurring engineering rule across the reconciliation and witness systems: when venue truth can't be established cleanly, record *nothing* rather than a plausible number. Silence is recoverable; fabrication isn't.
- **Determinism where it counts.** Research workers (the "mongooses") must produce hash-identical outputs on re-run or halt. An interpreter never fabricates a number.

## Why this matters

Anyone can generate code with AI. The hard problem is *knowing what you have* afterward: what runs, what is true, what would break. This method is our answer, developed under the least forgiving supervisor available — our own money, live, every day. This repo itself follows the method: each build session left a receipt in `receipts/`.
