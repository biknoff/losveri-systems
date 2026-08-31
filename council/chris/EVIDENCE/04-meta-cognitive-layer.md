# Evidence: the meta-cognitive review layer

**What this is:** the commit that introduced the layer, and the module-level design it added — a second pass that reviews Chris's own outputs (parsed intent, confidence, thread continuity) before they're trusted enough to act on, plus a companion self-healing module that can react when confidence is low.

**Redactions applied:** the commit's author line included a local-network machine identifier; removed below and replaced with `<redacted>`.

## The commit

```
commit 9b292f1247d8d34e306616c07bc12812cf4b8eff
Author: <redacted>
    Add meta-cognitive review layer

 app/command_engine.py           | 121 ++++
 app/config.py                   |  10 +
 app/meta_layer.py                | 357 ++++++++++
 app/routes/webhooks.py           | 772 ++++++++++++++++++++-
 app/self_heal.py                 | 146 ++++
 app/sync_engine.py               |  43 +-
 ledger_manager.py                | 417 +++++++++++
 tests/test_meta_contracts.py     | 220 ++++++
 ... (mirrored into a backup tree in the same commit)
 31 files changed, 6427 insertions(+), 18 deletions(-)
```

357 new lines in `meta_layer.py` alone, plus a dedicated 220-line contract test file (`tests/test_meta_contracts.py`) — this was built as a testable module, not a prompt tweak.

## What it reviews

`meta_layer.py` classifies every incoming request into one of six intents (`NEW_TRANSACTION`, `CORRECTION_OF_PREVIOUS`, `FEEDBACK_ON_SYSTEM_BEHAVIOR`, `ARCHITECTURAL_INSTRUCTION`, `CONVERSATIONAL`, `AMBIGUOUS` — see EVIDENCE/02) using layered regex hints for correction language, feedback/bug language, and architectural-instruction language, in both English and Spanish:

```python
_CORRECTION_HINTS = re.compile(
    r"\b(fix|fixed|correct|correg|corrige|arregla|parsed wrong|wrong date|wrong subject|should be|debe ser|eso no)\b",
    re.IGNORECASE,
)
_FEEDBACK_HINTS = re.compile(
    r"\b(parsed wrong|wrong parse|bug|error|fallo|issue|problema|feedback|meta)\b",
    re.IGNORECASE,
)
_ARCH_HINTS = re.compile(
    r"\b(update yourself|commit update|decline update|patch|self heal|self-heal|arquitectura|architecture)\b",
    re.IGNORECASE,
)
```

It computes a bounded confidence score by averaging whatever component scores are available:

```python
def _confidence(*scores):
    valid = [float(x) for x in scores if x is not None]
    if not valid:
        return 0.0
    return max(0.0, min(1.0, sum(valid) / float(len(valid))))
```

And it threads related messages together — a correction has to find the transaction it's correcting — by deriving a stable `thread_id` from an explicit thread field, a target event/row reference, or falling back to the request id:

```python
def build_thread_id(payload, request_id):
    source = payload if isinstance(payload, dict) else {}
    explicit = str(source.get("thread_id") or "").strip()
    if explicit:
        return explicit
    target = str(source.get("target_event_id") or source.get("event_id") or "").strip()
    if target:
        return f"event::{target}"
    ...
    return f"request::{str(request_id or '').strip() or 'unknown'}"
```

`app/self_heal.py` (146 new lines, same commit) sits downstream of this: when the review layer flags low confidence or an architectural instruction, self-heal is the module that can act on that signal — the design worth showing is the shape, not the internal decision table (kept out of scope for a redacted showcase).

The commit message itself — "Add meta-cognitive review layer" — is the author's own name for this: an agent that reviews its own outputs before they're allowed to mutate the ledger.
