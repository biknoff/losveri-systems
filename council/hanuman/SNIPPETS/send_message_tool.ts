// Excerpt from whatsapp-mcp/src/mcp.ts — the send_message MCP tool.
// Verbatim from source (redundant duplicate blank line at the end of the
// original block preserved as-is). No credentials or personal data here —
// this is the tool implementation, not a call site.

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
    mcpLogger.info(`[MCP Tool] Executing send_message to ${recipient}`);
    if (!sock) {
      mcpLogger.error(
        "[MCP Tool Error] send_message failed: WhatsApp socket is not available.",
      );
      return {
        isError: true,
        content: [
          { type: "text", text: "Error: WhatsApp connection is not active." },
        ],
      };
    }

    let normalizedRecipient: string;
    try {
      normalizedRecipient = jidNormalizedUser(recipient);
      if (!normalizedRecipient.includes("@")) {
        throw new Error('JID must contain "@" symbol');
      }
    } catch (normError: any) {
      return {
        isError: true,
        content: [
          {
            type: "text",
            text: `Invalid recipient format: "${recipient}". Please provide a valid JID (e.g., number@s.whatsapp.net or group@g.us).`,
          },
        ],
      };
    }

    try {
      const result = await sendWhatsAppMessage(
        waLogger,
        sock,
        normalizedRecipient,
        message,
      );

      if (result && result.key && result.key.id) {
        return {
          content: [
            {
              type: "text",
              text: `Message sent successfully to ${normalizedRecipient} (ID: ${result.key.id}).`,
            },
          ],
        };
      } else {
        return {
          isError: true,
          content: [
            {
              type: "text",
              text: `Failed to send message to ${normalizedRecipient}. See server logs for details.`,
            },
          ],
        };
      }
    } catch (error: any) {
      return {
        isError: true,
        content: [
          { type: "text", text: `Error sending message: ${error.message}` },
        ],
      };
    }
  },
);
