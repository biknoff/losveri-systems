# Dispatch script's dependency on Hanuman — redacted excerpt

**What this is:** the header and sender-invocation portion of Fay's time-of-day dispatch script, showing that it calls directly into Hanuman's `whatsapp-mcp` repository and canonical sender — the cross-link between the two projects, at the code level.

**Redactions:** the household staff member's name replaced with `<staff>`; the WhatsApp JID replaced with `<jid>`; the local absolute paths shortened to their project-relative form (both point to real, verifiable locations in the source repos, but the operator's home-directory username is not the point here).

---

```bash
#!/bin/bash
# Schedule script for <staff>'s morning messages
CORPUS_DIR=".../6th House - Fay/Fay's Corpus/<staff>/Lunes"
HANUMAN_DIR=".../3rd House - Hanuman/whatsapp-mcp"
STAFF_JID="<jid>"

send_msg() {
    local file="$1"
    local label="$2"
    echo "[$(date '+%H:%M')] Sending $label..."
    cd "$HANUMAN_DIR" && npx tsx ./send_whatsapp_once.ts \
        --recipient "$STAFF_JID" \
        --message-file "$file"
}

# 7:30 AM — scheduled send
SECONDS_UNTIL_730=$(( (7*3600 + 30*60) - ($(date '+%H')*3600 + $(date '+%M')*60 + $(date '+%S')) ))
if [ "$SECONDS_UNTIL_730" -gt 0 ]; then
    (sleep "$SECONDS_UNTIL_730" && send_msg "$CORPUS_DIR/<message file>" "7:30AM") &
else
    send_msg "$CORPUS_DIR/<message file>" "7:30AM"
fi
# ...a second, later-in-the-morning send follows the same pattern
```

`HANUMAN_DIR` points at the exact repository documented in `council/hanuman/`; `send_whatsapp_once.ts` is the same canonical fallback sender named in Hanuman's own `SKILL.md` (see `council/hanuman/EVIDENCE/skill_docs_consumer_contract.md`). Fay's script contains no WhatsApp protocol code of its own — it `cd`s into Hanuman's directory and shells out to Hanuman's sender, passing only a JID and a file path.
