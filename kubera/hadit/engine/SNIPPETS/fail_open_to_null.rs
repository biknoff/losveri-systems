// Source: crates/engine/src/gateway.rs (build clone). Redacted: nothing.
//
// WHAT THIS PROVES: when venue truth cannot be established cleanly (a merged/netted position
// where individual sibling deals cannot be separately identified), the engine records a NULL
// exit price / profit rather than a best-effort estimate. Downstream (witness, recon), a null
// field is a visible, honest gap — never a plausible-looking wrong number.

/// A survivor's SHARE of a netted position's closing deals (survivor-on-own-bracket root fix).
/// The survivor is the FINAL leg to close (it survived to symbol-flat while siblings left
/// earlier via inner fills), so its deals are the TRAILING `survivor_qty` lots of OUT volume,
/// time-ordered.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct SurvivorShare {
    /// Volume-weighted mean price over the survivor's leftover OUT deals; `None` when there are
    /// no closing deals (fail-open — the leg is still torn down, just with a null exit price).
    pub exit_px: Option<f64>,
    /// Summed realized profit over the survivor's leftover OUT deals; `None` when none.
    pub profit: Option<f64>,
    pub deal_tickets: Vec<String>,
    /// `deal_qty_match` — leftover volume reconciles EXACTLY to `survivor_qty` (high confidence);
    /// or `residual_fallback` — leftover volume does not reconcile (lower confidence); or
    /// `none` — no closing deals at all (fail-open; null profit/px).
    pub method: &'static str,
    pub source: Option<&'static str>,
}

// Elsewhere in the same file, the same discipline is stated for the whole-position path:
//
//   "On a merged/non-solo gold position the day-book falls back to the mark (the pre-existing
//   select_realized_profit fail-open) instead of over-attributing the combined position to one
//   leg. Either way the gate never books a sibling-inclusive total to a single leg."
//
// and again at the witness-write boundary:
//
//   "(fail-open: caller leaves the new witness fields null, never fabricates a number)."
//
// The rule recurs at three separate call sites in this file because it is a project-wide
// invariant, not a one-off guard: silence (a null field) is recoverable by a later reconciliation
// pass; a fabricated number is not.
