# Fay

**Status: RUNNING (~months of daily use)** — 6th-house domestic coordination: schedule → prioritized task list → Haitian Creole translation → dispatch to the household staff over [Hanuman](../hanuman/)'s WhatsApp transport.

## What it is

Fay reads a household schedule, turns it into a prioritized, day-specific task list, and — the actual point of this project — translates it into Haitian Creole for the operators who do the work, then dispatches it on a real schedule. Fay owns the *what* and the *language*; it never touches WhatsApp itself — that's Hanuman's job (see [Hanuman](../hanuman/) for the shared comms gate). The cross-language operation is not a side feature; it's the reason this exists. Household coordination that stays in the operators' own language, delivered on the same daily rhythm the household actually runs on, is the working product.

```mermaid
flowchart LR
    S["schedule<br/>(weekly rotation, day-specific tasks)"] --> P["prioritize<br/>(today's objectives)"]
    P --> T["translate<br/>→ Haitian Creole"]
    T --> D["dispatch"]
    D -->|"send_message via<br/>Hanuman MCP / npx tsx"| HAN[["Hanuman<br/>WhatsApp transport"]]
    HAN --> Staff["the household staff"]
```

## What's proven, not asserted

- **Months of real, dated operational artifacts** — not a demo. Corpus files span April 9 – July 20, 2026 (~3.5 months of this snapshot), on a recurring weekly cadence (Monday / Wednesday / Friday, plus ad hoc items like a payment reminder) — see `EVIDENCE/corpus_structure.md`.
- **The full pipeline is real**, not a design doc: a weekly schedule document, day-named output folders, Spanish-language drafts, and Haitian-Creole-suffixed final versions (`_KREYOL`) sitting next to each other for the same day, plus a dispatch script that calls straight into Hanuman's WhatsApp sender.
- **Cross-language operation is structural, not incidental** — every dispatch day produces a Creole-language artifact as a distinct, separately named file, not a translation-on-request afterthought.
- **Consumes Hanuman's transport directly**: the dispatch script (redacted excerpt in SNIPPETS) shells straight into `.../whatsapp-mcp/send_whatsapp_once.ts` — the same canonical sender documented in Hanuman's own SKILL.md. Fay never re-implements messaging.

## Honest notes

- An earlier scaffold for Fay existed under a different platform (Vertex AI Agent Engine / google-adk, Gemini 2.0 Flash) — `agent.py`, `agent.md`, `tools/household_tools.py`. It is **dead**: last touched March 31, 2026, before the working corpus below even starts (April 9). It was superseded, not iterated on. See `EVIDENCE/dead_adk_scaffold.md` — one line of evidence, no more.
- Fay's WhatsApp delivery rides Hanuman's transport, which is built on Baileys, **an unofficial WhatsApp bridge library** — stated plainly here as it is in the source operator's own notes, not smoothed over.

## Evidence index

| File | What it shows |
|---|---|
| [EVIDENCE/corpus_structure.md](EVIDENCE/corpus_structure.md) | Dated, day-organized corpus structure — filenames and dates only, no message content |
| [EVIDENCE/dispatch_dependency_on_hanuman.md](EVIDENCE/dispatch_dependency_on_hanuman.md) | The dispatch script's dependency on Hanuman's canonical sender, redacted |
| [EVIDENCE/dead_adk_scaffold.md](EVIDENCE/dead_adk_scaffold.md) | One-line dating evidence that the ADK scaffold predates and was superseded by the working system |
| [EVIDENCE/design_principles_excerpt.md](EVIDENCE/design_principles_excerpt.md) | Structural excerpt of Fay's operating principles — the coordination discipline, not household detail |

## Snippets

| File | What it shows |
|---|---|
| [SNIPPETS/schedule_dispatch.sh](SNIPPETS/schedule_dispatch.sh) | Redacted dispatch script — time-of-day scheduling straight into Hanuman's sender |
| [SNIPPETS/dead_scaffold_agent.md](SNIPPETS/dead_scaffold_agent.md) | The dead ADK scaffold's own self-description — dated, then abandoned |

## Related

- [ARCHITECTURE.md](ARCHITECTURE.md) — the schedule→prioritize→translate→dispatch flow in detail.
- [DECISIONS.md](DECISIONS.md) — choices and rejected alternatives.
- [Hanuman](../hanuman/) — owns the WhatsApp transport Fay dispatches through; Hanuman never sees Fay's scheduling logic.
- [STORY.md](../../STORY.md) · [council/README.md](../README.md)

**Adoption:** dispatch corpus spans 2026-04-09 → 2026-07-20 on a steady multiple-times-per-week cadence — months of real household use, not a demo. Per-dispatch analytics: not instrumented — stated as a gap.
