# MCP tool surface — whatsapp-mcp

**What this is:** the complete list of MCP tools registered by `whatsapp-mcp/src/mcp.ts` (`whatsapp-baileys-ts` server), read directly from source, plus the full schema for `send_message` — the tool every consuming agent actually calls to deliver a message.

**Redactions:** none needed — this is implementation code with no credentials, phone numbers, or personal content.

---

## The 8 registered tools (`server.tool(...)` calls, in source order)

| Tool | Line | Purpose |
|---|---|---|
| `search_contacts` | 70 | Find a contact's JID by name/number fragment |
| `list_messages` | 113 | Paginated message history for a chat |
| `list_chats` | 184 | Enumerate known chats |
| `get_chat` | 270 | Chat metadata by JID |
| `get_message_context` | 320 | Surrounding messages for a given message |
| `send_message` | 388 | Send a text message |
| `send_document` | 475 | Send a file |
| `search_messages` | 537 | Full-text search across stored messages |

## `send_message` — full schema, from source

```typescript
server.tool(
  "send_message",
  {
    recipient: z
      .string()
      .describe(
        "Recipient JID (user or group, e.g., '12345@s.whatsapp.net' or 'group123@g.us')",
      ),
    message: z.string().min(1).describe("The text message to send"),
  },
  async ({ recipient, message }) => {
    // normalizes JID, checks socket is live, calls sendWhatsAppMessage(),
    // returns the WhatsApp message ID on success or an isError result on failure
  },
);
```

Note the shape: two parameters, `recipient` (a JID string) and `message` (a text string). Nothing in the schema or the handler encodes who is allowed to message whom, or what a message is about — that logic lives entirely in the calling agent, not in the gate. This is the concrete form of the protocols-not-content boundary described in `README.md`.

One naming discrepancy worth stating honestly: internal SKILL.md documentation (`whatsapp-mcp/SKILL.md`) refers to this tool informally as `whatsapp_send_text`; the tool actually registered in code is `send_message`. The MCP server's declared name (`whatsapp-baileys-ts`) namespaces the tool for callers, so this is a documentation/naming drift, not a functional gap — but it's real and worth flagging rather than smoothing over.
