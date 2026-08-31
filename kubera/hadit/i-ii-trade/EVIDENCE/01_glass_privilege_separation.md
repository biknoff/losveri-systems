<!-- What: excerpt of glass.py, the read-only gateway process in front of the live HADIT
     cockpit, read from its own small VM. Redacted: broker name and account-id literals used in
     the identifier-scrub table (replaced below with [broker] / [id]); internal hostnames and
     the tunnel-local port (replaced with [node] / [port], matching the script's own scrub
     pattern for the same values). No other content altered. -->

## Module docstring — the design statement

```python
#!/usr/bin/env python3
"""i-ii GLASS — a strictly read-only window onto the live hadit cockpit.

Observers see the real floor working; they cannot touch it. The guarantee is enforced HERE,
at the gateway, not by hiding buttons in the UI (devtools would defeat that):

  1. METHOD DEFAULT-DENY   only GET/HEAD reach the origin. POST/PUT/PATCH/DELETE/OPTIONS ->403.
                           (/api/trips exists as BOTH GET and POST upstream, which is exactly
                            why the rule is method-first rather than path-first.)
  2. PATH DENYLIST         any path naming an operative action is refused even as a GET.
  3. CREDENTIAL ISOLATION  observer Cookie/Authorization headers are never forwarded, and
                           upstream Set-Cookie is never returned. Observers get no session.
  4. NO UPGRADES           WebSocket/upgrade requests are refused; SSE stays fine (GET, one-way).
  5. UI SHIM               injected into HTML: marks the page VIEW ONLY and neuters the operative
                           layer client-side too (belt and braces, never the boundary itself).

It never writes to the origin, never restarts it, never touches server.py.
"""
```

## Layer 1+2 — method default-deny, then an endpoint-exact path denylist

```python
SAFE_METHODS = {"GET", "HEAD"}
# Operative surface — refused even if someone dresses it as a GET.
# Operative surface, endpoint-exact (taken from the origin's own do_POST route table).
# Keyword matching was WRONG: "/order" also matched the read file "/orders_live.json" and blanked
# the live order tape. Method default-deny is the real boundary; this is the second belt, for
# anything dressed as a GET.
DENY_PATHS = {
    "/order", "/cancel_all", "/flatten_all", "/health_ingest",
    "/api/arm_live", "/api/disarm_live", "/api/cancel", "/api/close_position",
    "/api/flatten_all", "/api/modify_order", "/api/modify_position_rails",
    "/api/set_leg_enabled", "/api/set_leg_hotwire", "/api/set_leg_qty", "/api/set_recipe",
    "/api/stage_gold_mode", "/api/stage_roll", "/api/stage_sitout", "/api/push_cocktail",
    "/api/run", "/api/monitor_toggle", "/api/monitor_ingest", "/api/health_ingest",
    "/api/dismiss_sitout", "/hadit/compute/run", "/hadit/engine/weather_ack",
    "/api/<internal>",   # returns a cross-origin URL carrying a bearer token
}
```

The comment documents a real incident: an earlier keyword-matching version conflated the write
path `/order` with the read-only file `/orders_live.json` and blanked the live order tape. The
fix — the exact-match set above, sourced from the origin's own route table — is why method
default-deny is stated as "the real boundary" and the path list is "the second belt."

## Layer 3 — credential isolation

```python
HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers",
       "transfer-encoding","upgrade","set-cookie","strict-transport-security"}
...
if k.lower() in ("host","cookie","authorization","content-length","connection"): continue
```

Observer `Cookie`/`Authorization` headers are dropped before the request is relayed upstream;
`Set-Cookie` and other hop-by-hop/session-shaped headers are dropped before the response is
returned. An observer never receives a cockpit session.

## Layer 4 — no protocol upgrades

```python
if (self.headers.get("Upgrade") or "").lower() == "websocket":
    return self._refuse("upgrade")
```

## Book redaction (money + identity stripped server-side, byte-level)

```python
MONEY_KEYS = re.compile(r"(balance|equity|margin|banked|pnl|p_l|profit|loss|realized|"
                        r"unrealized|cash|deposit|withdraw|nav|_usd|usd_|dollars|funding)", re.I)
KEEP_KEYS  = re.compile(r"(price|level|fib|timestamp|time|ts|symbol|state|status|qty)", re.I)
REDACTED = "•••"

def redact(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "login" and (isinstance(v, int) or (isinstance(v, str) and v.isdigit())):
                out[k] = "[id]"                 # account identity never crosses the glass
            elif k == "server" and isinstance(v, str) and "[broker]" in v:
                out[k] = "[broker] · Live"      # broker/server name stays inside
            elif MONEY_KEYS.search(str(k)) and not KEEP_KEYS.search(str(k)) \
               and isinstance(v, (int, float)) and not isinstance(v, bool):
                out[k] = REDACTED
            else:
                out[k] = redact(v)
        return out
    if isinstance(node, list):
        return [redact(x) for x in node]
    return node

# Identifier scrub, byte-level, applied to EVERY proxied body (json, html, yaml, js).
# Catches account/server literals living inside prose strings, static HTML, and config —
# places the JSON key-walk cannot see.
ID_SCRUB = (
    (b"[account-id-1]", b"[id]"),
    (b"[account-id-2]", b"[id]"),
    (b"[broker]-Live",  b"[broker] \xc2\xb7 Live"),
)

# Infra topology scrub — internal home paths, hostnames, ports never cross the glass.
INFRA_RES = (
    (re.compile(rb"/home/[^\s\"'<>\)\]]*"), b"[internal]"),
    (re.compile(rb"\b[node-a]\.[node-domain]\b"), b"[internal]"),
    (re.compile(rb"\b[node]\b"),              b"[node]"),
    (re.compile(rb":\[glass-port\]\b"),        b":[port]"),
)
```

Structural/telemetry fields (price, state, timestamp, qty) are deliberately left intact "so the
cockpit still reads as the real thing" — this is presentation-preserving redaction, not a blanked
page.

## Ingress shape (redacted)

```
cloudflared tunnel  ->  ingress:
  - hostname: glass.i-ii.trade
    service: http://localhost:[port]
  - service: http_status:404
```

Only `glass.i-ii.trade` is exposed through the tunnel; the cockpit origin itself has no entry.
