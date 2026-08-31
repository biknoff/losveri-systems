# REDACTION_LOG.md — internal, delete before publish

Two independent sweeps over the complete repo (Phase 4 of the build plan), plus per-project audit catches during Phase 3. Zero-findings-twice is the gate.

## Phase 3 per-project audit catches (fixed at commit time)
| Where | What | Fix |
|---|---|---|
| time-travel-mirror/README | internal host codename kept with false justification | → "the live host" |
| engine/* (many) | host codenames in agent output | → "execution host"/"research host" (repo-wide sed) |
| miami/* | `datacore_canonical` (leaks server hostname) + broker name "AMP" throughout | → neutral panel name; → "the futures FCM"/generic |
| nt8-chicago/EVIDENCE | one stray host codename | → "remote-host" |
| Source-side (not repo): `1193/Hadit - Chicago.txt` on the Mac | live plaintext RDP credentials discovered during evidence gathering; never copied anywhere | file vaulted to `Los Veri/Vault/RETIRED_CRED_Hadit-Chicago_vaulted_20260901.txt` (operator-instructed; host retired, credential dead) |

## Sweep A — pattern/secret scan (2026-09-01)
Tooling: gitleaks/trufflehog/exiftool not installed on this host; systematic grep by class + context judgment. Verdicts: 1 LEAK, 6 SUSPECT, 12+ classes OK-intentional (loopback IPs, approved i-ii hostnames, operator names as attribution, Leo's public GPG fingerprint, `{project}` template vars, shell `$1` positionals, fictional ledger example).

| Finding | Verdict | Fix (commit 3a47387 / 991ae8e) |
|---|---|---|
| `altamar.info@gmail.com` in GPG verify transcript uid line | LEAK | → `leo <redacted>` |
| Real order ticket id `44125828` in witness sample | redact | → `"<redacted>"` |
| `spirit_mgc_c08` / `certify_mgc_rfd_g3` (leg names tying strategy to instrument) | redact | → `spirit_<leg>` / `certify_<leg>` (+ residual `mgc_c08_entry` fragment) |
| `/home/hadit/hadit-ws2/state` path + username | redact | → `<state-dir>` |
| Watchdog risk thresholds (ALERT/TRIP fracs, min-USD) | redact | → `<redacted>` |
| CERCA photos: EXIF present, GPS unverifiable (no exiftool) | strip | full EXIF stripped via PIL re-encode, both photos |
| All secret/key/JID/phone/staff-name/PII classes | none found | — |

## Sweep B — contextual human-reader pass
(appended when sweep B reports)

## Standing policy (final confirm at publish gate)
Allowed: `i-ii.trade`, `glass.i-ii.trade`, Leo & Mariele as operators/co-founders, Leo's public GPG fingerprint, loopback IPs, dates and structural counts. Everything else in the handoff §6 list stays out.

## Sweep B — contextual human-reader pass (2026-09-01)
~100 files read end-to-end. Verdict: label discipline strong repo-wide; fixes applied:
- HIGH privacy: `collect_leo_turns`→operator; voice-enrollment filenames→operator_a/b.wav; named+timestamped utterance log→`<operator>`/`<ts>`; workspace paths genericized (abraxas/chris/watchers).
- HIGH: broken relative links (11, kubera/nuit + miami subtrees) — all fixed, link-checker now clean.
- Inference: `cross_pollination_amp_cockpit.md` renamed (broker in filename); contract codes→`<gold-future>`/`<index-future>`; fleet-capacity number genericized; retired-cred filename dropped from chicago inventory.
- Internal bleed: "this pass"/atlas jargon/receipt name-pending genericized; private repo/branch name genericized in spectral headers; `/api/bugatti_src`→`/api/<internal>`.
- Label: `BUILT+VALIDATED, dormant`→`BUILT+DORMANT (validated)`.
- Architect overrules (recorded): "Los Verí" stays (the repo's own public identity); strategy count stays (scale ≠ edge); BUILT+RETIRED stays (in the legend); `mortal_architect_succession.md` session-mechanics content stays (it IS the protocol being showcased — conscious publish decision).
- Note: sweep B ran parallel to sweep A's fixes; its gmail/watchdog/state-path items were already fixed in 3a47387.
