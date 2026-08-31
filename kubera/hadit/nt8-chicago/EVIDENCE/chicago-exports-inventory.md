# Evidence: Chicago-era export inventory (second machine)

**What this is:** a type/count inventory of a folder of exports pulled off the Chicago
pipeline and kept on a second machine (the team's Mac), independent of the build-host
copy used for `production-tree-counts.md`. This is corroborating evidence that the
Chicago artifacts were deliberately preserved in more than one place, not left to rot on
a single retired box.

**Redactions applied:** individual file names withheld; only extension/type counts given.

## Inventory — `chicago_exports/`

60 files total, by type:

| Type | Count |
|---|---|
| `.cs` (C# source) | 19 |
| `.csv` (data export) | 26 |
| `.json` | 1 |
| `.txt` | 10 |
| `.DS_Store` | 1 |
| loose files under a `wtf/` subfolder | 3 |

The mix — C# strategy/indicator source alongside CSV data exports and text notes — is
consistent with a manual "grab what matters before the box goes away" export rather than
an automated backup job, which fits the "deliberately outgrown, not abandoned" framing:
someone took the time to pull artifacts off before decommissioning.

**Note:** a separate file in this same parent folder (`<retired-credentials note — vaulted separately>`, a
description-style document) was found during research to contain live, plaintext
remote-access credentials rather than pipeline documentation. It was not read past its
first lines and is not quoted or otherwise reproduced anywhere in this project directory.
Flagged out-of-band for credential rotation; out of scope for this evidence set.

**Source commands (read-only):** directory listing with extension grouping, via ssh to
the mirror host.
