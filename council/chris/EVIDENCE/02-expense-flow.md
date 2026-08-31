# Evidence: voice-note → ledger expense flow

**What this is:** two layers of the same pipeline. (1) Intent classification constants from `meta_layer.py`, the module that decides what kind of thing an incoming message is before anything is written. (2) The `expense_agent` sub-agent tool that turns a classified expense into a schedule and persists it. Full excerpt of the latter is in `SNIPPETS/expense_agent_excerpt.py`.

**Redactions applied:** none needed — this excerpt contains no identifiers, credentials, or financial data, only control-flow constants and function signatures.

## 1. Intent classification (`app/meta_layer.py`)

```python
INTENT_NEW = "NEW_TRANSACTION"
INTENT_CORRECTION = "CORRECTION_OF_PREVIOUS"
INTENT_FEEDBACK = "FEEDBACK_ON_SYSTEM_BEHAVIOR"
INTENT_ARCH = "ARCHITECTURAL_INSTRUCTION"
INTENT_CONVO = "CONVERSATIONAL"
INTENT_AMBIG = "AMBIGUOUS"

OP_CREATE = "CREATE"
OP_UPDATE = "UPDATE"
OP_DELETE = "DELETE"
OP_NOOP = "NOOP"
```

Regex hints feed the classifier before the LLM pass — correction language (`fix|fixed|correct|corrige|arregla`), feedback language, architectural-instruction language, conversational fillers, amount patterns, and ISO date patterns. A voice note that says "spent forty bucks at the pharmacy" is expected to land as `INTENT_NEW` / `OP_CREATE`.

## 2. Expense sub-agent tool (`sub_agents/expense_agent.py`, excerpted — full file in SNIPPETS/)

The tool signature and persistence call:

```python
def calculate_expense_schedule(
    amount: float,
    subject: str,
    tool_context: ToolContext,
    expense_type: str = "ONE_TIME",
    start_date: str = "",
    frequency: str = "",
    count: int = 0,
    interval: int = 1,
) -> dict:
    ...
    schedule = FinancialEngine.calculate_schedule(parsed_data)

    # 💾 PERSISTENCE
    from ..tools.persistence_tools import write_schedule_to_sheet, create_calendar_events
    try:
        write_sheet_res = write_schedule_to_sheet(schedule, tool_context=tool_context)
        write_cal_res = create_calendar_events(schedule, tool_context=tool_context)
    except Exception as e:
        write_sheet_res = str(e)
        write_cal_res = str(e)

    return {
        "status": "success",
        "schedule": schedule,
        "entry_count": len(schedule),
        "persistence_info": {"sheets": write_sheet_res, "calendar": write_cal_res}
    }
```

One tool call computes the schedule and writes both surfaces (Sheet-of-record, Calendar) in the same pass — the "it lands in the ledger" claim in one function.

## Where the voice part happens

Chris's own codebase contains no speech-to-text — grepping the webhook and command-engine layers for `voice`/`transcri` turns up nothing. This is intentional separation of concerns: **Hanuman** (`../hanuman/`) is the Council's comms gate and owns the voice pipeline; it transcribes and hands Chris a text intent over its existing webhook surface (`app/routes/webhooks.py`), which is where `_extract_meta_feedback`, idempotency-key construction, and command parsing already live for text-originated requests.
