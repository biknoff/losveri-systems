# EVIDENCE: structural read-only boundary

What: a source-level grep across the watcher fleet's shared library and every watcher script,
run on the research host, for any order-placement/modification/cancellation call. Redacted:
nothing — this is a structural absence, not a data excerpt.

```
$ grep -rn "order_send\|positions_close\|OrderSend\|place_order\|cancel_order" \
      /home/nuit/nuit_supervisor/*.py
(no matches)
```

Every watcher that touches the execution host does so through one shared helper
(the fleet's common module) that runs a caller-supplied *read* script over an
SSH channel and returns stdout — see `SNIPPETS/readonly_consumption_pattern.py`. No caller in
the fleet constructs anything other than a query/read command through that channel. The only
outbound effects any watcher can produce are: a Telegram message (`tg_send`), a line appended
to a local alert log (`append_alert`), and — for the one process this fleet meta-watches but
does not replace, the separate equity watchdog — a flatten-and-latch, whose latch only a human
clears.

This is the structural form of the claim in STORY.md and VERIFICATION.md: "the watcher cannot
author what it watches."
