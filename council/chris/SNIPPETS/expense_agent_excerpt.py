# SNIPPET — excerpted from sub_agents/expense_agent.py (live Vertex AI ADK deployment)
# Redactions: none — no identifiers, credentials, or financial data present.
# Purpose: shows the full path from a classified expense intent to a written
# ledger entry — one tool call computes the schedule and persists to both
# the Sheet-of-record and Calendar in the same pass.

# 💸 EXPENSE AGENT
# Handles: ONE_TIME, SUBSCRIPTION
# Elevated from existing FinancialEngine math.

from google.adk.agents import Agent
from google.adk.tools import ToolContext

from ..shared.financial_engine import FinancialEngine


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
    """Calculate an expense entry or recurring subscription schedule.

    For one-time expenses, returns a single entry. For subscriptions,
    generates the full recurring schedule.

    Args:
        amount: The expense amount (positive number, will be stored as negative).
        subject: What the expense is for (e.g. 'Netflix', 'Electricity Bill').
        expense_type: ONE_TIME or SUBSCRIPTION.
        start_date: ISO date string YYYY-MM-DD. Defaults to today if empty.
        frequency: Recurrence frequency for subscriptions — monthly, weekly, yearly.
        count: Number of occurrences for subscriptions. Defaults to 12 if frequency is set.
        interval: Interval between occurrences. Defaults to 1.
    """
    # Expenses are negative cashflows
    expense_amount = -abs(amount)

    parsed_data = {
        "transaction_type": expense_type,
        "amount": expense_amount,
        "subject": subject,
        "date": start_date or "",
        "payment_status": "Unpaid",
    }

    if frequency and expense_type == "SUBSCRIPTION":
        parsed_data["recurrence"] = {
            "frequency": frequency,
            "count": count if count else 12,
            "interval": interval,
        }

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
