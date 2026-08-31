# Architecture — Abraxas

## Scope

This document covers the invocation chain (CLI → launcher → model), the TTS/delivery chain, the consultation pattern with domain house-agents, the tiered memory model, and — separately, because it matters more than any component diagram — what "enforcement" actually means here.

## Invocation chain

`tools/abraxas` is a bash wrapper, not the agent itself. It is the single entry point for both interactive use and headless (autonomous, "oracle call") invocation from other agents. Its job, in order:

1. Resolve a fixed set of canonical files on disk: the bootstrap prompt, an agents-definition file, a continuity manifest, the constitution (`FIVE_PRINCIPLES.md`), and four ecological-memory index files (model spec, manifest, macrosystem, chronosystem).
2. **Hard-fail if any are missing** — before the model is ever called. See the "Enforcement, honestly" section below; this is the one piece of real code-level enforcement in the system.
3. Resolve a Gemini API key (env var, falling back to a plaintext `api.info` file — not shown in evidence).
4. Concatenate bootstrap + constitution + continuity + agents-definition + a generated runtime-context block (timestamp, timezone, caller identity, memory-layer index) into one prompt, wrapped in explicit `--- BEGIN/END ---` delimiters per section.
5. Exec `gsd` (a Node-based launcher CLI, resolved via `GSD_BIN`) with that prompt, the chosen provider/model, and — for headless calls — a strict response-envelope or footer contract.

Two invocation modes matter: **interactive** (`abraxas "..."`, execs `gsd` and hands off the TTY) and **headless** (`--headless`, captures stdout, optionally requires strict JSON with fields like `caller_agent`, `handoff_target`, `artifacts_read`). Headless mode is how other agents (GARUDA, MUSHAKA, Kubera) call Abraxas as a bounded oracle rather than an open chat — the wrapper explicitly instructs it to "preserve ABRAXAS bandwidth" and answer only within synthesis/continuity/escalation/pattern-reading framing in that mode.

## The consultation pattern

Abraxas does not merge the domain agents' knowledge into itself. The `agent_contracts.json` hierarchy places Abraxas at a `meta_layer` above a `planning_layer` (GARUDA) and `execution_layer` (MUSHAKA), with `domain_agents` (Fred, Chris, Kubera, Fay) and `knowledge_agents` (Thoth, Scribe) addressed separately. A `routing_rules` table (keys: `voice_notes`, `financial_logic`, `backtest_verification`, `household_coordination`, `trading_biometrics`, `abraxas_request`, and others) declares, per request category, which agent handles it — dispatch is a table lookup, not an ad hoc judgment call made fresh each time. The vessel file's own trading-debrief protocol names this explicitly: "Chris for finance grounding, Kubera for quant/backtest verification, Fred for prosody... Invoke only when domain is load-bearing" — consultation is scoped and deliberate, not reflexive.

## TTS and delivery chain

Reasoning output (text) and voice rendering are two separate pipelines, joined by a file on disk:

1. `tools/abraxas_tts.py` reads a markdown script, splits it into byte-bounded chunks (under 3800 bytes, honoring `...`-marked section breaks first, then sentence boundaries), and calls Gemini's TTS model (`gemini-3.1-flash-tts-preview`) once per chunk with a fixed prebuilt voice (`Leda`, `en-GB` for Abraxas; other agents get other voices, e.g. Kubera = `Achernar`, `en-US`).
2. Chunks are concatenated as raw PCM with an inserted silence gap, written to a scratch WAV, then transcoded to MP3 via `ffmpeg`.
3. `tools/send_channel_agent_response.py` — a shared delivery layer used by every channel agent, not Abraxas-specific — posts the result: `send_telegram_text()` to Telegram's `sendMessage` for text, `send_telegram_voice()` to `sendVoice` for the rendered audio. The same module also supports WhatsApp delivery, and computes a `response_span` (`brief`/`standard`/`extended`) from word count.

This is genuinely two models in series (reasoning model, then TTS model), not one model asked to also "sound like" speech — chosen because chunking and retry logic against a hard byte limit is a mechanical concern orthogonal to reasoning quality.

## Memory: six ecological tiers

`memory/` on disk holds six populated tiers, modeled on Bronfenbrenner's ecological-systems theory (micro → meso → exo → macro → chrono, plus semantic and procedural stores that don't map to a single ecological layer): `mesosystem/` (12 daily JSON files), `exosystem/` (2 weekly files), `macrosystem/` (current phase), `chronosystem/` (a longitudinal arc file), `semantic/` (durable facts: contacts, household state, sacred rules, trading rules), `procedural/` (contracts, dispatch rules, corrective patterns). A top-level `MANIFEST.json` indexes them, and is itself one of the eight files the boot gate requires to exist.

The wrapper injects an explicit escalation discipline into every prompt: start from the lightest relevant layer, climb to a deeper tier "only when the current request scope, emotional urgency, systemic impact, or relational stakes genuinely require it," and never bulk-preload all tiers "just in case." This is the same discipline the vessel file states for the agent's own context window ("Principle I applied to AI: the context window IS the body") — memory-tier discipline and context-budget discipline are treated as the same problem.

## Enforcement, honestly

There are two distinct claims that are easy to conflate, and this project is explicit about not conflating them:

1. **The constitution must exist.** `require_file "$PILLAR_FILE" ...` is real, unconditional, code-level: no file, no boot, no model call, full stop. Verified directly in source (`EVIDENCE/boot_hard_fail.md`).
2. **The model obeys the constitution.** This is not checked in code anywhere in the invocation chain. The constitution's full text is concatenated into the prompt inside delimiters, alongside an instruction ("These principles govern all agent behavior... No action, recommendation, or output may contradict them"), and the model is trusted to comply. Nothing downstream parses the model's response and validates it against the five principles.

Claim 1 is proven. Claim 2 is a prompt convention, and this project states that plainly rather than describing the system as "constitutional AI" — a term that implies exactly the code-level validation loop that does not exist here. See `DECISIONS.md` #4.
