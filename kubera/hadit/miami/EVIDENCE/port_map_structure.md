# Per-account service structure (ports redacted)

**What this is:** the shape of the per-account port map used to route each container's services (a broker bridge, a debug VNC console, and the ZMQ tick/order sockets) to the host. One entry per account, keyed by account login.

**Redactions:** the account login (object key) is replaced with `<login>`. Every port number is replaced with `<port>` — the *structure* (which services exist per account) is the evidence, not the topology.

---

```json
{
  "<login>": {
    "user": "<user>",
    "server": "<broker-server>",
    "bridge_port": "<port>",
    "vnc_port": "<port>",
    "novnc_port": "<port>",
    "zmq_tick_port": "<port>",
    "zmq_order_port": "<port>"
  }
}
```

Each account gets its own bridge port, its own debug VNC/noVNC pair (used only for manual troubleshooting, never in the runtime path — see `ARCHITECTURE.md`), and its own ZMQ tick-subscribe and order-request ports on the host. This is the per-account host-port allocation that the fleet's generated Docker Compose file and the cockpit's per-account client connections are both built from.
