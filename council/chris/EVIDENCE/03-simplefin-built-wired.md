# Evidence: SimpleFIN bank feed — BUILT and WIRED

**What this is:** proof the SimpleFIN client is not a stub — it's imported and called by a live, routed sub-agent. Three pieces: the import line in `household_query_tools.py`, the routing line in `agent.py`, and the sub-agent's own instruction prompt naming the tool as primary. Full client excerpt in `SNIPPETS/simplefin_client_excerpt.py`.

**Redactions applied:** the credential-resolution code below references `<workspace-root>/ANIMA/.auth.info` and a bundled `.simplefin_url` file — paths are kept (they contain no secret) but the secret values themselves were never read, printed, or included anywhere in this directory. The GCP project number that appears as a Secret Manager fallback default in source is replaced with `<redacted>`.

## 1. The client is imported by the tool layer

`tools/household_query_tools.py`:

```python
from .simplefin_client import fetch_recent_transactions, get_account_balances
```

## 2. The tool layer is imported by the sub-agent, and the sub-agent is wired into root routing

`sub_agents/household_query_agent.py`:

```python
from ..tools.household_query_tools import (
    compare_avmf_vs_life_tracker,
    find_unlogged_transactions,
    get_recent_bank_transactions,
    household_finance_snapshot,
    list_sheet_tabs,
    read_life_tracker,
    read_md_balances,
    read_sheet_tab,
)
```

`agent.py` (root orchestrator):

```python
from .sub_agents.household_query_agent import household_query_agent
...
# routing table entry:
# "Household budget, Life Tracker, spending queries, unlogged transactions,
#  MD Balances, fund allocations, ... → household_query_agent"
...
sub_agents=[
    ...,
    household_query_agent,
]
```

## 3. The sub-agent's own instruction prompt names the SimpleFIN tool as primary

```
TOOLS:
- `find_unlogged_transactions(lookback_days)` — THE PRIMARY TOOL. Pulls real bank
  transactions from SimpleFIN, compares against Life Tracker daily entries, returns
  charges not yet logged. Use this when asked about missing/unlogged transactions.
- `get_recent_bank_transactions(lookback_days)` — fetch raw bank/card transactions
  and account balances from SimpleFIN
```

## 4. Credential resolution (layered, never logged) — `tools/simplefin_client.py`

```python
def _read_access_url() -> str:
    """Read SimpleFIN access URL. Checks multiple sources for portability."""
    import os

    # 1. Bundled file in package (works in Vertex AI deployed runtime)
    bundled = Path(__file__).resolve().parent.parent / ".simplefin_url"
    if bundled.exists():
        url = bundled.read_text().strip()
        if url:
            return url

    # 2. Local .auth.info (development)
    if AUTH_INFO_PATH.exists():
        text = AUTH_INFO_PATH.read_text()
        for line in text.splitlines():
            if "FIN ACCESS URL:" in line:
                url = line.replace("FIN ACCESS URL:", "").strip()
                if url:
                    return url

    # 3. Environment variable
    env_url = os.environ.get("SIMPLEFIN_ACCESS_URL")
    if env_url:
        return env_url.strip()

    # 4. Secret Manager (Vertex AI managed runtime)
    try:
        from google.cloud import secretmanager
        project = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT", "<redacted>"))
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project}/secrets/SIMPLEFIN_ACCESS_URL/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8").strip()
    except Exception:
        pass

    raise ValueError("SimpleFIN access URL not found in bundled file, .auth.info, env, or Secret Manager")
```

This is what "built + wired" means concretely here: a real HTTP client against the SimpleFIN Bridge API, reachable through four fallback credential paths so it works identically in local dev and the deployed Vertex runtime, called by a tool that a routed sub-agent actually exposes to the LLM. What it is **not**: an automatic reconciliation engine — see [ARCHITECTURE.md](../ARCHITECTURE.md#reconciliation-the-designed-half).
