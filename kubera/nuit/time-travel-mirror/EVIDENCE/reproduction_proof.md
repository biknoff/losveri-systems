<!-- WHAT: excerpt of the mirror's REPRODUCTION_PROOF — mirror output vs. the prior (forked)
     harness across 4 configuration cells. REDACTED: all $ P&L figures removed (dollar figures
     redacted per policy); leg/breaker-week identifiers replaced with opaque tokens; instrument
     names generalized. What remains: round-turn counts, a governance-event count, and the
     content-hash equality that is the actual proof — a multiset hash over the full round-turn
     ledger, not a statistical summary. -->

# Reproduction proof — mirror vs. the harness it replaced

Every configuration cell run on the mirror reproduces the prior (forked) harness' published
result **exactly**, including the full round-turn ledger as a byte-identical multiset (a content
hash over every round-turn's fields, order-independent). Four independent configurations, run
twice each (mirror + the old fork), all four hash-match:

| cell | round-turns | governance events (breaker weeks / day-caps) | ledger multiset hash — mirror | ledger multiset hash — prior fork |
|---|---:|---:|---|---|
| cell 1 (reference/canon config) | 2,497 | 15 / 3 | `0344dd3b5418c54c…` | `0344dd3b5418c54c…` (match) |
| cell 2 (reproduction config) | 2,163 | 14 / 2 | `dc2262af38f08aa1` | `dc2262af38f08aa1` (match) |
| cell 3 (parameter variant) | 2,180 | 13 / 0 | `d900addfc66feab2` | `d900addfc66feab2` (match) |
| cell 4 (parameter variant) | 2,495 | 15 / 4 | `f587fc5901bb715a` | `f587fc5901bb715a` (match) |

Also identical between mirror and prior fork on cell 1: per-leg round-turn counts (three opaque
leg tokens), the full set of breaker-week keys, and the day-cap trigger dates. All P&L figures are
redacted from this excerpt; the underlying record carries them and the hash above covers them —
this table proves *structural* reproduction, not a restated total.

## The one known, bounded difference

The mirror also surfaces a **pre-existing, latent ordering instability** in the harness the fork
inherited too: when two round-turns share both an entry and exit timestamp to the nanosecond, the
serialization order between them is not deterministic (roughly 2% of rows, in contiguous blocks,
each block a pure permutation of the same rows — verified). The mirror does not introduce this;
old-binary reruns of the reference config reproduce the same two orderings the mirror produces.
Every statistic and every governance counter is invariant to it. It is flagged rather than hidden
because, in principle, a tied pair could straddle a breaker threshold and flip a governance
decision — priced as immaterial in the historical window checked, and left open as a named,
cheap-to-close item rather than silently accepted (see [`../DECISIONS.md`](../DECISIONS.md)).
