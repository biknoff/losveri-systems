# Cross-pollination: the family's own family futures cockpit, ported from Miami

**What this is:** an excerpt from the family's own session-status notes (a separate project, the family's own futures cockpit) documenting that its manual-trading panel was ported *from* Miami's cockpit — evidence of design flowing back into the family's own infrastructure from the external-facing service, without the infrastructure itself merging.

**Redactions:** hostnames/URLs and IPs removed throughout (the source names a specific box and domain; neither appears here). Byte sizes and file names kept — they are not identifying.

---

> ## the family futures cockpit LIVE (2026-07-01)
>
> ### What was built
> Self-contained manual trading panel ported from the canonical Miami panel directory (`cockpit_baby.html` ~153KB + `baby_chart.html` ~237KB) and venue-translated to the family's futures venue. All code lives on [the family's own box].
>
> ### Venue translation applied
> - `XAUUSD → <gold-future>`, `BTCUSD → <index-future>` in all symbol selectors, JS defaults, and iframe src
> - Volume: default 0.10 lot → 1 contract; step 1; label "lot" → "ctr"
> - Title: "MT5 Cockpit" → "the family futures cockpit"
> - A shim script bypasses login/config, hardcodes the account selection, stubs endpoints
> - 0 functional references to the original (MT5/gold) symbol remain (1 is a leftover comment)

`the canonical Miami panel` is the family's own name for Miami's canonical cockpit panel — the same `cockpit_baby.html` / `baby_chart.html` design documented in this directory's `ARCHITECTURE.md` and `README.md`. The family reused Miami's manual-trading UI design for their own futures futures account rather than building a second panel from scratch — the design traveled outward to Miami's external users first, then a version of it came back for the family's own use on a different venue. Infrastructure did not merge; only the UI design and its venue-translation pattern did.
