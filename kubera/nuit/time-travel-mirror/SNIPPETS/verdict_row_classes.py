# SOURCE: rust_recon_daily/build_verdict.py — module docstring, the row-classifier legend.
# REDACTED: leg names generalized (e.g. a specific strategy-leg identifier -> opaque token
# "<leg>"); env-var name for one sizing parameter kept since it is a governance knob, not a
# strategy rule; nothing else altered. This is the full legend of every "known, explained"
# yellow class the nightly verdict recognizes — the point is that "explained-yellow" is a fixed,
# named list, not a wildcard, and anything outside it is red by construction.

"""
Match method: each LIVE entry is matched one-to-one to an expected (governed-replay) entry of the
same leg, same session, entry price within +/-1 tick.

Known-YELLOW classes (encoded, never silently promoted to green or dropped to red):
  instrument-class A:
    qty_clamp_known / parked_by_gate / live_governance / live_margin_gate /
    tick_tail_gap / order_pending_or_resting / state_cascade_after_gov_block
  instrument-class B:
    qty_scaling_known       matched but live qty != configured qty (a per-leg risk cap or
                             margin-gate/ramp clamp -- known live governance, not drift)
    qty0_sitout_known       expected trade, but the leg is sized 0 in the live config
                             (a deliberate regime de-risk sit-out -- governance, not drift)
    live_governance         a live ORDER_BLOCKED event explains the gap
    live_margin_gate        that ORDER_BLOCKED was specifically the margin gate: the note
                             carries equity, margin already in use, and wanted-vs-granted size --
                             the account sat the trade out, not the strategy
    order_mechanic          a marketable-limit conversion near the entry (price still faithful)
    bar_tail_gap            expected entry within a grace window of the last data bar
    order_pending_or_resting  live order placed/armed, no fill/exit event yet
    canon_open_end_of_bars  matched, but the expected trade is still open at the last bar
    state_cascade_after_gov_block  an earlier governance gap this session, same leg

Anything else unexplained = RED. Combined nightly verdict = worst of the per-instrument-class
verdicts.
"""
