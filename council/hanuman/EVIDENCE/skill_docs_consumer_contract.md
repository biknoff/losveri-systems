# Two independent skill docs, one rule: use the gate

**What this is:** excerpts from two separately maintained SKILL.md files — one living inside `whatsapp-mcp/` itself, one living in the shared `skills/` directory other agents discover — both converging on the same rule: route WhatsApp sends through Hanuman, never build or fall back to a second transport.

**Redactions:** the shared-skill doc's worked example originally named a specific contact and a specific WhatsApp JID; both are replaced with `<contact>` / `<jid>` below. No other content altered.

---

### `whatsapp-mcp/SKILL.md` (excerpt)

> Herramientas MCP Expuestas Automáticamente:
> - `whatsapp_send_text` (Envia texto directo)
> - `whatsapp_send_document` (Envia PDFs o archivos locales)
> - ...
>
> Si el tool MCP de Hanuman **no** esta montado en la sesion actual:
> - no uses OpenClaw
> - no uses Playwright / WhatsApp Web
> - no inventes otra superficie
> - usa el repo local `3rd House - Hanuman/whatsapp-mcp` con `npx tsx` como fallback canonico

### `skills/send-whatsapp-via-hanuman/SKILL.md` (excerpt, redacted)

> ## Rules
> 1. Do not use OpenClaw for this skill.
> 2. Do not use Playwright, WhatsApp Web, browser automation, or any manual web surface for this skill.
> 3. Do not route through generic "open a browser and send it" fallbacks just because the MCP tool is absent in the current agent session.
> ...
>
> Canonical sender:
> - `.../whatsapp-mcp/send_whatsapp_once.ts`
>
> ```bash
> cd '.../whatsapp-mcp'
> npx tsx ./send_whatsapp_once.ts \
>   --recipient '<jid>' \
>   --message-file '/abs/path/to/message.md'
> ```

Both documents were written independently (different directories, different authorship context, different language register — one is Spanish/emoji-annotated, one is plain English procedural) and both land on the identical architectural rule. That convergence, not either document alone, is the evidence: the "one gate, no side channels" design is enforced as policy at the documentation layer, not just implied by the code's existence.
