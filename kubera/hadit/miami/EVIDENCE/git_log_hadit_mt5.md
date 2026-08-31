# Active-development evidence — recent commits

**What this is:** the five most recent commits (as of this excerpt) to the successor/active repository in this lineage, showing continued, real feature work on the multi-account cockpit — not a dormant or one-off build.

**Redactions:** author email redacted. File diff stats kept (they reveal code churn, not secrets).

---

```
commit 44a83b9 (Aug 10)
    fix(ui): restore multi-account execution without a group
    cockpit_baby.html | 2 +-

commit 8f91604 (Aug 10)
    milestone-3.66: Complete UI tweaks and social features
    baby_chart.html                | 2412 +++++++++++++++++++++++++++++++++-------
    baby_hadit.py                  | 1871 ++++++++++++++++++++++++++++---
    cockpit_baby.html              | 1806 +++++++++++++++++++++++++-----
    handwritten.csv                |   27 +
    provision_handwritten_users.py |  221 ++++

commit 81ea391 (Aug 7)
    fix(ui): restore authentic Hadit baseline UI, logo, welcome flow, footer & Target Mode cycle
    baby_chart.html   | 1786 ++++++++++-------------------------------------------
    cockpit_baby.html |    4 +-

commit 811f2a7 (Aug 7)
    feat(superdofi): integrate dynamic account wheel, ticker mapping, and rolling history buffer in UI
    baby_chart.html   | 23 ++++++++++++++++++++++-
    cockpit_baby.html | 24 ++++++++++++++++++++++++

commit 42f19be (Aug 7)
    feat(superdofi): Stage 2 - automatic suffix resolution, SymbolCatalog & rolling history buffer
    baby_hadit.py          | 19 +++++++++++-
    zmq_cockpit_backend.py | 82 ++++++++++++++++++++++++++++++++++++++++++++++++--
```

The Aug 10 "fix(ui): restore multi-account execution without a group" commit is the direct multi-account/copy-trading evidence this excerpt is included for — a regression fix on exactly the feature this project claims (running orders across accounts without requiring a pre-defined account group).
