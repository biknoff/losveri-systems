# Source: deploy/mt5_zmq_gateway.py — module docstring (verbatim except redactions).
# What this shows: the ZMQ command surface one gateway process exposes for ONE account.
# Redactions: the hostname in the original PUB/REP endpoint comment removed.
#
# One gateway container per account. Uses the OFFICIAL MetaTrader5 Python API locally
# (no chart, no Expert Advisor, no candles, no cross-arch bridge workaround) and fans
# data + execution out over ZeroMQ.

"""mt5_zmq_gateway — the single MQL5<->host interface for one MT5 account, on Linux.

One per container. Runs in wine-python, uses the OFFICIAL MetaTrader5 API local to
this terminal (connect + request — NO chart, NO Expert Advisor, NO candles, NO
cross-arch bridge). Fans data + execution out over ZeroMQ to the Los Veri infra:

  PUB  tcp://*:<port>  -> complete terminal tick flow {sym,time,bid,ask,last,vol,ta}
  REP  tcp://*:<port>  -> request/response JSON commands:
       {"cmd":"ping"}                         -> {ok, symbol, login, trade_allowed}
       {"cmd":"snapshot"}                      -> {balance,equity,positions,working_orders}
       {"cmd":"account"} / {"cmd":"positions"} / {"cmd":"orders"}
       {"cmd":"place","side","order_type","entry","sl","tp","qty","volume"?} -> bracket
       {"cmd":"modify","ticket","price"?,"sl"?,"tp"?}   -> drag entry/SL/TP lines
       {"cmd":"cancel","ticket"}               -> cancel ONE working order
       {"cmd":"flatten_all"}                   -> close ALL positions (priority #1)
       {"cmd":"cancel_all"}                    -> cancel ALL pending orders + detach position SL/TP (priority #2)
       {"cmd":"history_ticks","count"}         -> copy_ticks_from count
       {"cmd":"history_rates","count"}         -> native MT5 M1 OHLC bars

This is the exec logic (LIMIT entry with atomic server-side SL/TP, filling-mode
fallback), local to the terminal and reachable over ZMQ. Candles are built downstream.
"""

# The command dispatch itself (process_command), showing the surface is a flat,
# auditable switch — no dynamic dispatch, no hidden commands:
#
# def process_command(req, sym):
#     cmd = req.get("cmd")
#     if cmd == "ping": ...
#     elif cmd == "snapshot":       res = _snapshot(sym)
#     elif cmd == "account":        res = {"ok": True, "account": mt5.account_info()._asdict()}
#     elif cmd == "positions":      res = {"ok": True, "positions": [...]}
#     elif cmd == "orders":         res = {"ok": True, "orders": [...]}
#     elif cmd == "place":          res = _place(sym, req)
#     elif cmd == "modify":         res = _modify(req)
#     elif cmd == "cancel":         res = _cancel(req["ticket"], req)
#     elif cmd == "close_position": res = _close_position_ticket(req["ticket"], req)
#     elif cmd == "flatten_all":    res = _flatten_all(req)
#     elif cmd == "cancel_all":     res = _cancel_all(req)
#     elif cmd == "closed_deals":   ...   # position journaling
#     elif cmd == "history_report": ...   # full deals + orders for account reports
#     elif cmd == "shutdown":       ...
#     elif cmd == "history_ticks":  ...
#     elif cmd == "history_rates":  ...
