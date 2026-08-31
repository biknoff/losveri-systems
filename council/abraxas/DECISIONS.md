# Decisions — Abraxas

Each entry: the choice made, and the alternative considered and rejected.

## 1. Hard-fail boot without the constitution
**Chosen:** `tools/abraxas` checks for `FIVE_PRINCIPLES.md` (and seven other canonical files) at process start and exits `1` before any model call if any are missing.
**Rejected:** treating the constitution as a suggestion — loading it when convenient, falling back to a generic system prompt if the file is absent, or logging a warning and continuing. A constitution that's optional to load isn't a constitution; the cost of an occasional hard failure (a moved file, a broken symlink) was accepted specifically to make "Abraxas without its principles" structurally impossible rather than merely unlikely.

## 2. Voice as the primary interface
**Chosen:** Abraxas is reached by voice note over Telegram, and replies by voice note back — text is a byproduct (the archived `.md` script), not the primary channel.
**Rejected:** another chat app or dashboard. The family already interacts by voice elsewhere in the Council (see Fred's prosody work); a text interface would discard the somatic information a spoken exchange carries and would compete with, rather than fit into, how the family already talks to each other.

## 3. House agents consulted, not merged
**Chosen:** Abraxas sits above Chris, Kubera, Fred, and Fay in the `agent_contracts.json` hierarchy and calls into them via a declared routing table, scoped to when "domain is load-bearing" — never absorbing their scope into its own.
**Rejected:** one omniscient agent that knows finance, work-quant detail, and prosody equally well. A single agent covering every domain either shallows out on each one or grows an unmanageable context/prompt surface. Consultation with a bounded, scoped call keeps each domain agent's contract (and its `forbidden_actions`) intact and auditable independently.

## 4. Prompt-injected constitution, stated as such — not claimed as code enforcement
**Chosen:** the constitution's full text is injected into every prompt inside explicit delimiters, and the project's own documentation says plainly that compliance is a prompt convention, not a validated constraint.
**Rejected:** claiming or implying "constitutional AI" — a term that specifically means the model's outputs are checked (or trained) against a constraint set programmatically. Building that validation loop was not attempted here; claiming it anyway would be exactly the kind of euphemism Principle III of the constitution itself forbids ("Words must match reality. No euphemisms."). The honest, weaker claim — boot requires the file, the prompt injects it, nothing downstream checks it — is the one this project makes.

## 5. Two models in series: reasoning, then TTS
**Chosen:** a separate chunked pipeline (`abraxas_tts.py`) renders the reasoning model's text output through a dedicated TTS model, with its own chunking/retry logic against a hard API byte limit.
**Rejected:** a single multimodal call expected to both reason and speak. Splitting the concerns means the byte-limit chunking, silence-stitching, and retry logic live in one small, testable module instead of being entangled with reasoning-prompt construction — and lets each agent get a distinct fixed voice (Leda for Abraxas, Achernar for Kubera) without touching the reasoning pipeline at all.

## 6. Headless mode as a bounded oracle call, not a second chat surface
**Chosen:** `--headless` (optionally `--json-envelope`) lets other agents (GARUDA, MUSHAKA, Kubera) invoke Abraxas as a one-shot, caller-identified, envelope-constrained call, distinct from the interactive path.
**Rejected:** giving other agents the same open-ended interactive session a human gets. The wrapper explicitly instructs headless calls to "preserve ABRAXAS bandwidth" and restricts them to synthesis/continuity/escalation/pattern-reading framing — cross-agent calls are cheap and scoped by design, not another full conversation thread competing for context.

## 7. Escalate through memory tiers on demand, never bulk-preload
**Chosen:** the six ecological memory tiers are read lazily — the wrapper's injected protocol says to start at the lightest relevant layer and climb only when scope, urgency, or stakes require it.
**Rejected:** loading all tiers into every prompt "just in case." The vessel file states the reasoning directly: the context window is treated as a finite resource under the same discipline as Principle I (the body) — preloading everything would spend that budget on context that's usually irrelevant to the turn at hand.
