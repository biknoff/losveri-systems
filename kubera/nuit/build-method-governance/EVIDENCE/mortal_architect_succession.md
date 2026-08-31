<!-- WHAT: excerpts from a real architect spawn-prompt document in the source repo
     (ARCHITECT_XIII_SPAWN_PROMPT.md) plus a same-source note on a real mid-cycle stand-down.
     REDACTED: nothing — this is process/governance narrative, no strategy content, no P&L,
     no account data. -->

# The mortal-architect protocol, in its own words

Architects in this project are numbered sequentially (Master Architect I through at least XIII,
observed on disk) and are each a fresh AI chat session with no memory of the sessions before it.
Continuity is carried entirely by written artifacts — never by direct architect-to-architect
conversation, because there is no shared context for one to happen in.

## A real stand-down and handback

From the record cited in the Architect XIII spawn prompt (2026-04-29):

> "Architect XI ran the Path C corpus-redesign cycle (six design domains + two embedded
> checkpoints) and **stood down 2026-04-29 mid-cycle due to bandwidth signal**. Path A handback to
> Architect XII for Checkpoint 2 + Design Domain 6 + cycle close handoff finalization."
>
> "Architect XII (your predecessor) closed the XI cycle 2026-04-29. Authored: ARCHITECT_XII_
> CHECKPOINT_2_DISPOSITION (PASS); DD6 v_stress_aggregator_spec; ARCHITECT_X_5b_BC_RESCOPE_
> COMMISSION_PACKET; HANDOFF_path_C_corpus_redesign FINAL."

Elsewhere in the same repo, a builder-tier equivalent is on record by name:
`HANDOFF_daniel_2_standdown.md` and its addendum — the same discipline applied one level down, at
the Builder role.

## The spawn prompt as the only channel

The opening of `ARCHITECT_XIII_SPAWN_PROMPT.md` — authored by the *outgoing* Architect XII, for
Mariele to paste into a brand-new chat session:

> "You are the Master Architect for the NUIT Spectral Minesweeper rebuild... You are a fresh Claude
> Opus 4.7 chat session... You are designated Master Architect XIII.
>
> You are NOT a Phase Builder. Phase Builders run as Claude Code in the Kubera repo, produce code
> and sealed artifacts, and are bounded by their phase contract. You are the design-and-oversight
> role: dialogue with Mariele on architectural questions, produce amendments/addenda when the
> design substrate needs to evolve, field escalations from Phase Builders, and serve as continuity
> holder for project context that does not fit cleanly inside any single artifact."

Followed by an explicit "OPENING RITUAL" instructing the new architect to read the canonical
continuity packet **in full**, integrate the prior cycle's close artifacts, and only then proceed —
the same "verify before you trust the substrate" discipline as the cryptographic layer, applied to
a human governance role instead of a file hash. Note also the honest self-report embedded in the
handoff: Architect XII explicitly did **not** author a v9 continuity supersession, citing "rot
signal at cycle close (file-authoring memory failure surfaced; not catastrophic but
compounding-risk)" — an architect naming its own degradation rather than pushing through it, which
is exactly what the stand-down rule exists to make normal.

## What this buys

An immortal single context accumulates undocumented state — decisions the operators can't audit
because they were never written down, made by a session whose reasoning nobody outside it can
inspect. Bounding each architect's tenure and forcing every handoff through a written, dated,
filename-citable artifact means every architectural decision in this project's history has a
paper trail, whether or not the architect that made it is still "alive" in any session.
