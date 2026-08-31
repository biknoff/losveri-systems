# ARCHITECTURE — i-ii.trade

Part of HADIT — see [STORY.md](../../../STORY.md). Scope of this document: the one surface that
is actually proven running, `glass.i-ii.trade`, and the boundary that keeps it safe. The
login-gated product app is described only as far as its documented shape; it is not probed here.

## The boundary: public surface can never reach order placement

The live HADIT cockpit (the same operative surface `../engine/` and `../miami/` run on) exposes
order/cancel/flatten/arm-live/modify endpoints over HTTP on its own small VM. `glass.py` sits in
front of it as a second, independent process — not a code path inside the cockpit, not a
feature flag inside it — and is the only thing the public hostname ever reaches:

```
cloudflared tunnel: glass.i-ii.trade  ->  http://localhost:[port]   (glass.py)
                                            |
                                            v  (GET/HEAD only, filtered + redacted)
                                          cockpit origin, localhost-only, no public ingress
```

The cockpit itself has **no public ingress at all**. The only network path from the internet to
the cockpit's process is *through* `glass.py`, and `glass.py` is built to refuse everything that
isn't a safe read.

## Privilege separation, enforced in code (not hidden in the UI)

`glass.py`'s own header states the reasoning directly: devtools defeat a UI-only guarantee, so
the guarantee has to live at the gateway. Five independent layers, each doing a different job
(excerpted in `EVIDENCE/01_glass_privilege_separation.md`):

1. **Method default-deny.** Only `GET`/`HEAD` are relayed to the origin at all; every
   `POST`/`PUT`/`PATCH`/`DELETE`/`OPTIONS` is refused before it reaches the cockpit. This is the
   real boundary — method-first, not path-first — because at least one cockpit endpoint exists as
   both a safe `GET` and an operative `POST` on the same path, so a path-based rule alone would
   have been wrong.
2. **Endpoint-exact path denylist**, as a second belt. An earlier keyword-matching version is
   documented as having matched a *read* path (`/orders_live.json`) as if it were the *write*
   path `/order`, and blanked the live order tape — the fix (exact-path matching against the
   origin's own route table) is in the current file, with the incident left in the comment as
   the reason the rule exists.
3. **Credential isolation.** Observer `Cookie`/`Authorization` headers are stripped before the
   request reaches the origin, and `Set-Cookie` from the origin is stripped before the response
   leaves — observers are never handed a session with the real cockpit.
4. **No protocol upgrades.** WebSocket/`Upgrade` requests are refused outright; one-way,
   read-only Server-Sent-Events traffic is left alone.
5. **Server-side book redaction.** Every proxied body — JSON, HTML, YAML, JS — is walked and
   scrubbed before it leaves the gateway: money-shaped keys (balance/equity/margin/P&L/etc.) are
   replaced with a redaction marker while structural/telemetry keys (price, state, timestamp,
   qty) are left intact so the cockpit still reads as the real thing; account and broker
   identifiers are substituted for fixed placeholders at the byte level, not just in JSON keys,
   so the same identifiers can't leak through prose strings, static HTML, or config files the
   JSON walker never sees. Internal hostnames/paths/ports are scrubbed the same way before
   anything crosses the glass.

A cosmetic sixth layer — an injected "VIEW ONLY" bar and a client-side `fetch`/`confirm` shim —
is explicitly commented in the source as **not** the boundary: "the boundary is the gateway,
which refuses every non-GET and every operative path regardless of what this script does." The
shim is there so a human observer isn't confused by UI that still looks clickable; it does no
enforcement work.

## What "its own small VM" adds

The product surface runs on its own small VM, separate from the machine(s) that carry live order
routing (`../engine/`'s execution host) and separate from the discovery/supervision side
(`../nuit/`). That separation is the same "hygiene is architecture" principle STORY.md states for
HADIT/NUIT generally: the surface a stranger on the internet can reach is deliberately not
colocated with the process that can move money. Even a full compromise of the glass process's
host does not, by itself, hand an attacker a path to order placement — `glass.py` never holds
cockpit credentials, never forwards them, and the cockpit has no listener reachable from the
public internet in the first place.

The login-gated product app (chart, draw, voice notes, share, "alone" scheduler) is documented
as living on the same small VM, under active iteration; it is not evidenced here as a public,
authenticated multi-user service — see README.md's status table. Its own privilege boundary
(session handling, per-user data isolation, and its own relationship to the cockpit) is future
work and is stated as such, not implied by the glass design above.

## Failure mode this is designed against

An observer, or a scraper, or a link shared on social media, reaches `glass.i-ii.trade` and can
watch the real floor — the point of the product's public face — while structurally unable to:
place, cancel, or modify an order; arm or disarm live trading; read account balance, equity, or
P&L; obtain a session cookie or bearer token for the real cockpit; or reach any non-glass
internal host or port named in the response body. `EVIDENCE/02_blocked_log_enforcement.md` shows
this being exercised, not just designed: refused write attempts recorded by the gateway itself.
