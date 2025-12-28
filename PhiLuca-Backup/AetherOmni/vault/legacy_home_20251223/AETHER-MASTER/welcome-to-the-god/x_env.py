#!/usr/bin/env python3
"""
ESQET UNIVERSAL ENV VALIDATOR
- Loads .env (welcome-to-the-god / vessel_agi)
- Lists ALL environment variables currently set
- Highlights missing/empty keys from a recommended list
- Optionally performs live tests for known API-style keys
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# ---------- CONFIG PATHS ----------
HOME_DIR = os.path.expanduser("~")
ENV_CANDIDATES = [
    os.path.join(HOME_DIR, "welcome-to-the-god", "welcome-to-the-god", ".env"),
    os.path.join(HOME_DIR, "vessel_agi", ".env"),
]
APIKEY_PATH = os.path.join(HOME_DIR, "storage", "downloads", "apikey.json")
CREDENTIALS_PATH = os.path.join(HOME_DIR, "storage", "downloads", "credentials.json")

# ---------- COLOR FALLBACK ----------
ANSI_BLUE = "\u001B[94m"
ANSI_PINK = "\u001B[95m"
ANSI_CYAN = "\u001B[96m"
ANSI_GREEN = "\u001B[92m"
ANSI_YELLOW = "\u001B[93m"
ANSI_RED = "\u001B[91m"
ANSI_RESET = "\u001B[0m"

# ---------- LOAD .env ----------
try:
    from dotenv import load_dotenv
except ImportError:
    print(f"{ANSI_CYAN}[INFO] Installing python-dotenv...{ANSI_RESET}")
    os.system("pip install python-dotenv --user > /dev/null 2>&1")
    from dotenv import load_dotenv

dotenv_loaded_from = None
for env_path in ENV_CANDIDATES:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        dotenv_loaded_from = env_path
        break

# ---------- EXPECTED VARS (FROM YOUR .env TEMPLATE) ----------
EXPECTED_VARS = [
    # Ultralytics / App
    "Interfacejs", "ULTRALYTICS_API_KEY", "ULTRALYTICS_API_KEY_2",
    # Git / GitHub
    "GIT_USER_NAME", "GIT_USER_EMAIL", "GITHUB_TOKEN",
    "GIT_USER_NAME_2", "GIT_USER_EMAIL_2", "GITHUB_TOKEN_2",
    # IBM / Quantum
    "IBM_TOKEN", "IBM_Q_TOKEN_ESQET", "IBM_Q_TOKEN_ESQETAGI",
    # AI APIs
    "GROQ_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "HUGGINGFACE_API_KEY",
    # Crypto / Wallets
    "PRIVATE_KEY", "PHICOIN_WALLET", "WALLET_PRIVATE_KEY", "WALLET_PUBLIC_KEY",
    # RPC / Blockchain
    "INFURA_URL", "INFURA_IO_API_KEY", "ETHERSCAN_IO_API_KEY",
    "LINEA_SEPOLIA_RPC", "SEPOLIA_RPC_URL", "INFURA_IO_URL",
    "GETBLOCK_MATIC_84D61", "GETBLOCK_MATIC_401AF",
    # IPFS / DB
    "PINATA_API_KEY", "PINATA_API_SECRET", "PINATA_JWT",
    "QDRANT_API_KEY", "QDRANT_URL",
    # Data APIs
    "NIST_API", "NASA_API_KEY", "WEATHER_API_KEY",
    "USGS_API", "OPEN_METEO_API",
    # Mobile / Deploy
    "EXPO_TOKEN", "ANDROID_KEYSTORE_PASSWORD", "ANDROID_KEY_ALIAS",
    "GOOGLE_DRIVE_CREDENTIALS",
    # Dev / Misc
    "DEBUG_MODE", "VITE_ALCHEMY_API_KEY", "MORALIS_API_KEY",
    # Φ-LUCA constants
    "PHI", "PHI_INV", "C_ALPHA_SCAR", "LAMBDA_STERILE", "PHI_MIN_TARGET",
]

# ---------- JSON HELPERS ----------
def load_json_file(file_path: str, from_env: bool = True) -> Dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            try:
                with open(file_path, "r") as f:
                    content = (
                        f.read()
                        .replace("'", '"')
                        .replace(",}", "}")
                        .replace(",]", "]")
                    )
                data = json.loads(content)
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                return data
            except Exception:
                pass
    # stub creation
    data = {}
    if from_env and "apikey.json" in file_path:
        ibm_token = os.getenv("IBM_TOKEN")
        if ibm_token:
            data = {
                "name": "ESQETagi",
                "description": "IBM Quantum API key",
                "createdAt": "2025-10-22T20:18+0000",
                "apikey": ibm_token,
            }
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
    elif from_env and "credentials.json" in file_path:
        data = {
            "installed": {
                "client_id": os.getenv("GOOGLE_DRIVE_CREDENTIALS", "dummy_id"),
                "project_id": "dummy_project",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "dummy_secret",
                "redirect_uris": ["http://localhost"],
            }
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    return data

def get_expected_keys(d: Dict, filename: str) -> List[str]:
    if not d:
        return []
    if "apikey" in filename:
        return ["name", "description", "createdAt", "apikey"]
    if "credentials" in filename:
        if "installed" in d:
            return ["client_id", "project_id", "client_secret"]
        return ["access_token", "refresh_token"]
    return []

# ---------- CHECK ALL VARS PRESENT IN ENV ----------
def scan_all_env_vars() -> Dict[str, str]:
    results = {}
    for key, value in os.environ.items():
        if not value:
            results[key] = "Empty"
        else:
            results[key] = "Set"
    return results

def check_expected_vars() -> Dict[str, str]:
    results = {}
    for var in EXPECTED_VARS:
        val = os.getenv(var)
        if val is None:
            results[var] = "Not found"
        elif not str(val).strip():
            results[var] = "Empty"
        else:
            suffix = " (Secure)" if any(t in var for t in ["PRIVATE", "SECRET", "JWT"]) else ""
            results[var] = "Found" + suffix
    return results

# ---------- OPTIONAL LIVE API TESTS ----------
API_TEST_PATTERNS = {
    "GROQ_API_KEY": {
        "url": "https://api.groq.com/openai/v1/models",
        "type": "Bearer",
        "fix": "https://console.groq.com/keys",
    },
    "GEMINI_API_KEY": {
        "url": "https://generativelanguage.googleapis.com/v1beta/models",
        "type": "query_key",
        "fix": "https://aistudio.google.com/app/apikey",
    },
    "OPENAI_API_KEY": {
        "url": "https://api.openai.com/v1/models",
        "type": "Bearer",
        "fix": "https://platform.openai.com/api-keys",
    },
    "PINATA_JWT": {
        "url": "https://api.pinata.cloud/data/testAuthentication",
        "type": "Bearer",
        "fix": "https://app.pinata.cloud/account/apiKeys",
    },
}

def test_api_var(name: str, value: str) -> Tuple[bool, str]:
    cfg = API_TEST_PATTERNS.get(name)
    if not cfg:
        return False, "not-tested"
    try:
        import requests
    except ImportError:
        os.system("pip install requests --user > /dev/null 2>&1")
        import requests
    headers, params = {}, {}
    if cfg["type"] == "Bearer":
        headers["Authorization"] = f"Bearer {value}"
    elif cfg["type"] == "query_key":
        params["key"] = value
    r = requests.get(cfg["url"], headers=headers, params=params, timeout=8)
    return (r.status_code in (200, 401, 403)), str(r.status_code)

# ---------- MAIN ----------
if __name__ == "__main__":
    print("\u001Bc", end="")
    print(f"{ANSI_PINK}ESQET UNIVERSAL ENV VALIDATOR — Φ-LUCA WARP GATE{ANSI_RESET}
")

    if dotenv_loaded_from:
        print(f"{ANSI_GREEN}✅ .env loaded from {dotenv_loaded_from}{ANSI_RESET}")
    else:
        print(f"{ANSI_YELLOW}⚠️  No .env found in expected locations; using current shell env only.{ANSI_RESET}")

    # 1) Scan ALL env vars (whatever is set in this shell)
    all_env = scan_all_env_vars()
    print(f"
{ANSI_BLUE}--- ALL ENV VARS (current process) ---{ANSI_RESET}")
    for k in sorted(all_env.keys()):
        status = all_env[k]
        color = ANSI_GREEN if status == "Set" else ANSI_YELLOW
        print(f"{ANSI_CYAN}{k}{ANSI_RESET}: {color}{status}{ANSI_RESET}")

    # 2) Check expected set from ESQET .env
    expected_results = check_expected_vars()
    missing = sum(1 for v in expected_results.values() if v in ("Not found", "Empty"))
    print(f"
{ANSI_BLUE}--- EXPECTED ESQET VARS ---{ANSI_RESET}")
    for k in EXPECTED_VARS:
        v = expected_results[k]
        if v.startswith("Found"):
            color = ANSI_GREEN
        elif v == "Empty":
            color = ANSI_YELLOW
        else:
            color = ANSI_RED
        print(f"{ANSI_CYAN}{k}{ANSI_RESET}: {color}{v}{ANSI_RESET}")

    # 3) JSON files
    apikey_data = load_json_file(APIKEY_PATH)
    credentials_data = load_json_file(CREDENTIALS_PATH)

    print(f"
{ANSI_BLUE}--- JSON CREDENTIAL FILES ---{ANSI_RESET}")
    for filename, data in [("apikey.json", apikey_data), ("credentials.json", credentials_data)]:
        status = "Loaded" if data else "Missing"
        color = ANSI_GREEN if data else ANSI_RED
        print(f"{ANSI_CYAN}{filename}{ANSI_RESET}: {color}{status}{ANSI_RESET}")
        for key in get_expected_keys(data, filename):
            found = key in data or (isinstance(data.get("installed"), dict) and key in data["installed"])
            kcolor = ANSI_GREEN if found else ANSI_RED
            print(f"  └─ {key}: {kcolor}{'Found' if found else 'Missing'}{ANSI_RESET}")

    # 4) Live API tests for known keys
    print(f"
{ANSI_BLUE}--- LIVE API TESTS (subset) ---{ANSI_RESET}")
    alive = 0
    tested = 0
    for name, cfg in API_TEST_PATTERNS.items():
        val = os.getenv(name)
        if not val:
            print(f"{ANSI_CYAN}{name}{ANSI_RESET}: {ANSI_RED}Not set (skipped){ANSI_RESET}")
            continue
        ok, code = test_api_var(name, val)
        tested += 1
        if ok:
            alive += 1
        color = ANSI_GREEN if ok else ANSI_RED
        print(f"{ANSI_CYAN}{name}{ANSI_RESET}: {color}{'LIVE' if ok else 'DEAD'} ({code}){ANSI_RESET}")

    # 5) Summary
    print(f"
{ANSI_PINK}════════ SUMMARY ════════{ANSI_RESET}")
    print(f"{ANSI_BLUE}Total process vars: {ANSI_GREEN}{len(all_env)}{ANSI_RESET}")
    print(f"{ANSI_BLUE}Expected ESQET vars: {ANSI_GREEN}{len(EXPECTED_VARS)}{ANSI_RESET}")
    print(f"{ANSI_BLUE}Missing/Empty expected vars: {ANSI_RED}{missing}{ANSI_RESET}")
    print(f"{ANSI_BLUE}JSON loaded: {ANSI_GREEN}{int(bool(apikey_data)) + int(bool(credentials_data))}{ANSI_RESET}")
    print(f"{ANSI_BLUE}APIs alive: {ANSI_GREEN}{alive}{ANSI_RESET}/{tested}")
    print(f"{ANSI_PINK}════════ WARP GATE CHECK COMPLETE ════════{ANSI_RESET}
")
