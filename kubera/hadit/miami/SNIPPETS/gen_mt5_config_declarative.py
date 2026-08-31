# Source: gen_mt5_config.py — declarative MT5 startup-config generator (excerpt).
# What this shows: config-as-code terminal login/governor setup, replacing GUI
# automation entirely. No hardcoded credentials here — this is the generator, not
# a filled-in config; the secret file it reads is never committed or shown.

"""
gen_mt5_config — deterministic MT5 startup-config generator (no GUI, no LLM in the loop).

Reads the per-user account secret and emits a complete MT5 `mt5cfg.ini` whose
[Common] section carries Login/Password/Server. A terminal launched with
`terminal64.exe /portable /config:mt5cfg.ini` then auto-connects headlessly on
boot — the "Open an account" wizard modal never appears, so nothing downstream
ever blocks on it.

Idempotent: same account in -> same config out. The resolved broker server is
cached in the persistent wineprefix volume on first connect, so restarts
reconnect without re-resolving over the network.
"""

_CHARTS_EXPERT = """[Charts]
MaxBars=1000000
PrintColor=0

[Expert]
AllowDllImport=1
AllowWebRequest=1
AllowTrailingStop=1
AllowAlgoTrading=1
EnableAlgoTrading=1
"""


def build_config(acct: dict) -> str:
    login = str(acct["login"]).strip()
    password = str(acct["password"])
    server = str(acct["server"]).strip()
    # KeepPrivate=1 persists the password between connections so the watchdog
    # restart reconnects without re-prompting. ProxyEnable/CertInstall pinned off.
    common = (
        "[Common]\n"
        f"Login={login}\n"
        f"Password={password}\n"
        f"Server={server}\n"
        "KeepPrivate=1\n"
        "NewsEnable=0\n"
        "EventsEnable=0\n"
        "Portable=1\n"
        "ProxyEnable=0\n"
        "CertInstall=0\n\n"
    )
    return common + _CHARTS_EXPERT

# Never echoes the password on write — only reports non-secret identity:
#   sys.stderr.write(f"wrote {args.out} (login={acct['login']} server={acct['server']})\n")
