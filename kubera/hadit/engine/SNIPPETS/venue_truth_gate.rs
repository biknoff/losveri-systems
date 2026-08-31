// Source: crates/engine/src/gateway.rs (build clone: ws2_live_ownqty_build).
// Excerpt shows the design pattern, not the surrounding order-routing logic. Redacted: nothing —
// this is pure data-shape reduction over broker deal history, no strategy parameters involved.
//
// WHAT THIS PROVES: the venue's own closing-deal records — never the engine's own fill memory —
// decide what a position's exit was. `in_volume == out_volume == expected_qty` is the gate that
// proves a position was solely this leg's before its P&L is attributed to that leg, preventing a
// netted sibling position from having its combined P&L wrongly credited to one leg.

/// Volume-weighted summary of the CLOSING deals in a `history_deals` gateway reply — the
/// venue-truth exit fields the witness EXIT event carries. The MT5 deal `entry` field is
/// 0=DEAL_ENTRY_IN, 1=DEAL_ENTRY_OUT, 2=DEAL_ENTRY_INOUT (reversal), 3=DEAL_ENTRY_OUT_BY; only
/// OUT / OUT_BY deals are the position's close, so IN legs are excluded from the price/profit.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct ExitDeals {
    /// Volume-weighted mean price over the OUT/OUT_BY deals; `None` when there is no closing deal
    /// (fail-open: reconciliation then falls back to its old bracket reconstruction).
    pub exit_px: Option<f64>,
    pub deal_tickets: Vec<String>,
    pub profit: Option<f64>,
    /// Total CLOSING volume on this position. A recovery path uses
    /// `in_volume == out_volume == its own qty` to prove the position it is about to book is
    /// SOLO and FLAT — i.e. no sibling leg ever netted into it — so it can never attribute a
    /// merged position's combined P&L to one leg.
    pub out_volume: f64,
    pub in_volume: f64,
}

/// Does this whole-position exit summary prove the position was EXCLUSIVELY this leg's and fully
/// closed — the precondition for booking a merged position's combined P&L to a SINGLE leg without
/// risking cross-leg over-attribution (crediting a merged position's combined $ to one leg)?
/// True iff there is a closing deal AND `in_volume == out_volume == expected_qty`.
pub fn exit_is_solo_and_flat(deals: &ExitDeals, expected_qty: u32) -> bool {
    let q = expected_qty as f64;
    deals.profit.is_some()
        && (deals.in_volume - q).abs() < 1e-9
        && (deals.out_volume - q).abs() < 1e-9
}
