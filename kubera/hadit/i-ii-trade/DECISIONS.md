# DECISIONS

Part of HADIT — see [STORY.md](../../../STORY.md). Each decision states the nearest-wrong
alternative that was rejected, not just what was chosen.

1. **A strictly read-only gateway as the public front door, not the cockpit itself.**
   `glass.i-ii.trade` is a separate process (`glass.py`) that proxies only `GET`/`HEAD`, denies
   an endpoint-exact list of operative paths, strips credentials in both directions, and redacts
   money/identity server-side (`EVIDENCE/01`). *Rejected:* exposing the real cockpit publicly
   behind a login screen or feature flags — a login screen is one bug away from being skipped,
   and a UI toggle is defeated by devtools; a second process that never holds cockpit credentials
   fails closed even if the UI layer fails.

2. **Method-first denial, not path-first.** The gateway's primary rule is "only GET/HEAD reach
   the origin," with the path denylist as a second belt. *Rejected:* a path-based rule alone —
   the cockpit has at least one endpoint that is both a safe `GET` and an operative `POST` on the
   same path, which a purely path-based filter cannot distinguish.

3. **Exact-path denylist over keyword matching, after an incident.** An earlier keyword-based
   version matched a read path (`orders_live.json`) against the operative keyword `/order` and
   blanked the live order tape; the fix moved to exact matching against the origin's own route
   table, with the incident kept in the comment as the reason (`EVIDENCE/01`). *Rejected:* fixing
   the specific collision and leaving keyword matching in place elsewhere — the class of bug, not
   just the instance, was the actual problem.

4. **The product on its own small VM, not cohabiting with live execution.** The public-facing
   surface (glass + the in-progress login-gated app) runs on hardware separate from the engine's
   execution host and separate from the discovery/supervision side. *Rejected:* running the
   product surface on the same host as order routing for operational simplicity — the same
   "hygiene is architecture" reasoning STORY.md states for HADIT/NUIT: what a stranger on the
   internet can reach should never be the same host that can move money.

5. **Book redaction at the gateway, at the byte level, not just JSON-key filtering.** Money keys
   are stripped in structured responses, and the same account/broker identifiers are scrubbed as
   raw byte substrings across every proxied content type (JSON, HTML, YAML, JS), because
   identifiers were found living inside prose strings and static config that a JSON key-walk
   never sees (`EVIDENCE/01`). *Rejected:* redacting only structured API responses — it would
   have left identifiers exposed in the static HTML and YAML the same gateway also proxies.

6. **Show the product honestly as early-product, not demo-ware.** This directory states plainly
   which pieces are running (the glass gateway) and which are roadmap staged on founder-voice
   product thinking (the "alone/together" app itself — drawing, voice notes, sharing, the
   scheduler), rather than presenting a mockup or a pitch deck as if it were shipped
   (`README.md`'s status table, `EVIDENCE/03`). *Rejected:* leading with the product vision and
   letting the reader assume it's live — the whole repo's stance is that a claim without evidence
   next to it is not a claim worth making, and the freshest artifact here (a pitch rewrite,
   2026-08-27) is explicitly evidence of *thinking*, not of a running feature.
