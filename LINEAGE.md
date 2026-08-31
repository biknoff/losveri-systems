# LINEAGE — what came from what

Systems are easier to trust when you can see their scars. Three threads.

## 1. The trading stack: consumer-grade → professional

- **Chicago (NT8 + DLL) — BUILT+RETIRED.** The first live pipeline: Python strategy logic bridged into NinjaTrader 8 on a Windows VM via a C# bridge (a NinjaScript transpiler survives as its descendant). It traded. It also taught the limits of consumer-grade platforms — and it is where the parity discipline was born: when your logic lives in two languages, you learn to prove they agree.
- **HaditFugue (Windows era, retired).** The NT8 lineage's last stand: a supervised runner with multi-account routing and live tick recording on a dedicated Windows box. Retired; the box no longer exists.
- **Nautilus/Python.** The strategies moved to an open, scriptable engine — the oracle against which the next stage would be certified.
- **The Rust engine (ws2) — RUNNING.** Certified byte-for-byte against the Nautilus oracle (see VERIFICATION.md), then extended live: witness spine, watchdog, nightly recon, prox-park, netting exits. Deployed via a bare-repo canon with rehearsal in the Time Travel Mirror.
- **Miami (MT5 service) — RUNNING.** The cockpit generalized into a multi-account MT5 service on its own server, because external users wanted in — and their accounts could not live beside the family's own.
- **i-ii.trade — RUNNING (early product).** The productization: the "alone" half (your strategies, your scheduler — the family's own orchestration, offered outward) and the "together" half (chart, draw, drop voice notes, share, trade — one place instead of three apps).

## 2. NUIT's intellectual lineage: a program that corrects itself in writing

- **v2 (2026-04):** the discovery apparatus stated in trading clothes — parameters, simulator, acceptance criterion. Correct instincts, under-stated generality. (An honest artifact: v2's original bytes are lost, but its hash survives inside a signed seal — the governance outlived the document.)
- **v3:** a category error, made and then *caught*: the apparatus collapsed into simulation-based-inference-proper under ambient vocabulary pressure. The machinery drifted toward estimating posteriors when the actual target was discovering representations.
- **v4 (skeleton):** the correction, in writing: Spectral is a *geometry-of-emergence* apparatus — discover the latent terrain representation, the manifestation families, and their correspondence from the geometry of outcomes. Trading named explicitly as proving ground, not definition (manufacturable manifestations, cheap outcomes, failures that cost money rather than people). SEER (terrain discovery) and PROBE (directed search) marked plainly: DESIGNED, not built. The Cold-Firing validation chain that ran — and its verdicts on disk — is what BUILT looks like here.

The self-corrections are the credential. A research program that documents its own wrong turns is one whose right turns you can believe.

**A note on who's doing the correcting.** Both v3 and the v4 skeleton were authored through a named AI consultation role, not a person — but not the same role. "Daniel" (v3-era) is a recurring, numbered design-architect CLI role: spawned per Room via a shell alias, Sonnet 4.6 by default, bounded to design-substrate paths only, never code (`DANIEL_CLI_PROTOCOL_v1.md`), the same discipline as the mortal-architect protocol one level down — Daniel-0 opened the v3 blueprint, Daniel-2 through Daniel-4 carried later Rooms and governance briefs. "Elder" (the v4 skeleton) is a different, one-off role: a single long-conversation consultation explicitly commissioned to catch and correct v3's own drift, and its document says so about itself — "Elder authored this at high conversation-length; treat every specific as provisional." They are not the same lineage under different names; they're sequential and distinct — Daniel is the sustained, protocol-governed architect role that produced v3, Elder is the higher-effort, self-disclaimed corrective pass that produced v4's reframing of what v3 got wrong.

## 3. Fred: the stack followed the epistemology

- **Hume era (bot v6.x):** voice notes analyzed through a hosted affect API — appropriate when benchmarking against *population* norms.
- **The migration:** when the question changed from "how does this voice compare to people in general" to "is *this person* at *their own* baseline," the stack had to change with it — a hosted probabilistic affect model cannot anchor a within-person prosodic floor. Fred moved to **openSMILE/eGeMAPS**: deterministic, reproducible acoustic measurement, personally baselined on longitudinal recordings.
- **Today:** the measurement system is BUILT+VALIDATED (within-person, chronological out-of-sample, pre-declared stress tests) and dormant; the bot line is PAUSED, verified working. Two systems, stated as two.

*Elsewhere in the family tree: the Council grew from Abraxas outward (houses built as needed, the rest stated as designed); CERCA preceded everything and set the operator+AI working tandem; the Build Method was born inside NUIT because building a validation pipeline **with** AI agents demanded governance **of** AI agents.*
