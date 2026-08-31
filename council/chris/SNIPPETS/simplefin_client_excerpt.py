# SNIPPET — excerpted from tools/simplefin_client.py (live Vertex AI ADK deployment)
# Redactions: GCP project number fallback default replaced with <redacted>.
# No tokens, URLs-with-credentials, or account data present — the client
# reads the access URL at runtime from a location outside source control
# and never logs it.
# Purpose: shows the read-only SimpleFIN Bridge fetch, and the layered
# credential resolution that makes the same code work in local dev and
# the deployed Vertex runtime without hardcoding secrets.

"""SimpleFIN bank feed client for Chris.

Fetches real bank/card transactions from SimpleFIN Bridge API.
Access URL read from /Users/leo/Los Veri/ANIMA/.auth.info at runtime.
Never log or expose the access URL.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

AUTH_INFO_PATH = Path("/Users/leo/Los Veri/ANIMA/.auth.info")
SANTO_DOMINGO = timezone(timedelta(hours=-4))
MAX_WINDOW_DAYS = 90
DEFAULT_LOOKBACK_DAYS = 7


@dataclass
class BankTransaction:
    id: str
    posted_date: str
    amount: float
    description: str
    account_name: str
    account_id: str
    pending: bool
    category: str | None = None
    institution: str = ""
    currency: str = "USD"

    def to_dict(self) -> dict:
        return asdict(self)


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


def _fetch_simplefin(access_url: str, start_ts: int, end_ts: int) -> dict:
    """Fetch accounts and transactions from SimpleFIN API."""
    parsed = urlparse(access_url)
    base_url = f"{parsed.scheme}://{parsed.hostname}{parsed.path}"
    auth = (parsed.username, parsed.password)

    response = requests.get(
        f"{base_url}/accounts",
        auth=auth,
        params={"start-date": start_ts, "end-date": end_ts},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
