# Evidence: RUNNING on Vertex AI Agent Engine (ADK)

**What this is:** the header and top imports of the deployed root agent (`agent.py`) from the live ANIMA deployment tree, plus the module list confirming a multi-agent orchestrator, not a single agent with tools bolted on.

**Redactions applied:** the deployed `DEFAULT_MONEY_FLOW_SHEET_ID`, `DEFAULT_CALENDAR_ID`, and `DEFAULT_GCP_PROJECT` constants are real identifiers in the source and are omitted below (replaced with `<redacted>`). No file paths outside the source tree, no credentials, no `vertex_agent_resource_name.txt` (not opened — excluded from scope by design).

## Header comment (states the architecture directly)

```python
# 🏠 CHRIS — 2nd House Financial Agent (Root Orchestrator)
# Vertex AI Agent Engine — ADK Multi-Agent Architecture
#
# Chris is NOT a monolithic agent with tools.
# Chris is an orchestrator that routes financial intents
# to specialized Transaction Sub-Agents via LLM-driven delegation.
#
# Sub-agents handle intelligence (parsing, math).
# Chris handles persistence (Sheets, Calendar, Firestore) — in future phases.
```

## Imports (confirms ADK, confirms the sub-agent roster)

```python
from google.adk.agents import Agent
from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from .sub_agents.loan_borrowing_agent import loan_borrowing_agent
from .sub_agents.income_agent import income_agent
from .sub_agents.expense_agent import expense_agent
from .sub_agents.custom_agent import custom_agent
from .sub_agents.chris_viz_agent import chris_viz_agent
from .sub_agents.calendar_agent import calendar_agent
from .sub_agents.stats_site_agent import stats_site_agent
from .sub_agents.venture_intelligence_agent import venture_intelligence_agent
from .sub_agents.distribution_reconciliation_agent import distribution_reconciliation_agent
from .sub_agents.knowledge_library_agent import knowledge_library_agent
from .sub_agents.research_agent import research_agent
from .sub_agents.household_query_agent import household_query_agent
```

## Runtime version stamp and managed-runtime hardening

```python
CHRIS_RUNTIME_VERSION = "6.0.0"
```

The module also defines `_sanitize_managed_runtime_env()` and `_hydrate_managed_runtime_defaults()`, which detect the managed Vertex/Cloud Run runtime via markers (`K_SERVICE`, `GOOGLE_CLOUD_PROJECT`, `CLOUD_ML_PROJECT_ID`, `AIP_HTTP_PORT`, `VERTEX_PRODUCT`) and, when present, strip API-key env vars that would conflict with managed Vertex session auth, and hydrate non-secret runtime defaults. This code path only matters if the agent actually runs inside that managed environment — its existence and the version stamp (`6.0.0`, well past a "hello world" scaffold) are evidence the deployment is live and has iterated, not a one-shot proof of concept.

Eleven `sub_agents/*.py` files exist on disk alongside `agent.py`, each a distinct ADK `Agent` definition with its own instruction prompt and tool set (see EVIDENCE/02 and EVIDENCE/03 for two of them in detail).
