<!-- What: one real witness JSONL line pulled from the execution host's live witness/ tree (2026-07-21 session
     day), plus the spec statement from witness.rs. Redacted: account_id -> <redacted>; entry/sl/tp
     prices and qty -> <redacted> (values only, field names preserved per the evidence brief); venue
     deal/order tickets kept as opaque ids (they carry no strategy logic, matching the leg-id rule). -->

## Spec (from `crates/engine/src/witness.rs`)

> Phase-1 Witness — durable, append-only per-order execution log. The bot must witness itself: every
> decision (order placed/blocked -> filled/cancelled -> exit -> sit-out) recorded per spirit per ET
> day, so attribution survives a tmux pane restart... Path:
> `{witness_dir}/{session_date}/{leg}.jsonl` — one append-only file per spirit per ET day. Schema
> `hadit.ws2.witness_event/v1`, one JSON object per line.

## One real event, redacted (from `witness/2026-07-21/spirit_<leg>.jsonl`, the execution host)

```json
{
  "account_id": "<redacted>",
  "detail": {
    "entry": "<redacted>",
    "order_type": "LIMIT",
    "qty": "<redacted>",
    "side": "SELL",
    "sl": "<redacted>",
    "tag": "mgc_c08_entry_<redacted>",
    "tp": "<redacted>"
  },
  "dry_run": false,
  "instrument": "MGC.CME",
  "schema": "hadit.ws2.witness_event/v1",
  "source": "route_signal:send_plan_request",
  "spirit": "spirit_<leg>",
  "state": "ORDER_PLACED",
  "ticket": "<redacted>",
  "ts_utc_ns": "<redacted>"
}
```

The next line for the same ticket in the same file is a matching `EXIT` event carrying
`exit_deal_profit`, `exit_deal_tickets`, and `exit_px` sourced from
`reconcile_once:generalized_off_managed_legs` — i.e. the exit fields come from the venue's own
reconciliation pass, not the engine's own order-fill memory (see `SNIPPETS/venue_truth_gate.rs`).

**Failure behavior:** a 2026-07-25 fix (documented in the source, `witness.rs`) replaced a silent
`if let Ok(..)` write with a loud one — a write failure now increments a counter and logs, because
"a witness failure must never block trading" but must also never fail invisibly, since that would
be "the worst possible failure mode for a spine."
