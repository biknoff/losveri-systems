#!/bin/bash
# Redacted excerpt of Fay's morning-dispatch script.
# Staff name -> <staff>, WhatsApp JID -> <jid>, absolute paths shortened
# to project-relative form. Structure and logic are verbatim from source.

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

# 7:30 AM — first scheduled send of the day
SECONDS_UNTIL_730=$(( (7*3600 + 30*60) - ($(date '+%H')*3600 + $(date '+%M')*60 + $(date '+%S')) ))
if [ "$SECONDS_UNTIL_730" -gt 0 ]; then
    echo "Scheduling 7:30 AM message in $SECONDS_UNTIL_730 seconds..."
    (sleep "$SECONDS_UNTIL_730" && send_msg "$CORPUS_DIR/<message_file>" "7:30AM") &
else
    echo "7:30 AM already passed, sending now..."
    send_msg "$CORPUS_DIR/<message_file>" "7:30AM"
fi

# 8:45 AM — daily briefing (same pattern, second time slot)
# ...
