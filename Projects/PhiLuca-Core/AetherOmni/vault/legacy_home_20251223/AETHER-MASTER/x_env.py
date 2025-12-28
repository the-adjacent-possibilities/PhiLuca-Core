#!/usr/bin/env python3
"""
X-ENV UNIVERSAL CHECKER
- Loads .env from the current working directory
- Shows ALL environment variables grouped by prefix
- Explicitly checks a set of important legacy keys
- Safe for Termux (no f-strings, careful string handling)
"""

import os
from collections import defaultdict
from typing import Dict, List

# ANSI color codes
ANSI_BLUE   = "\u001B[94m"
ANSI_PINK   = "\u001B[95m"
ANSI_CYAN   = "\u001B[96m"
ANSI_GREEN  = "\u001B[92m"
ANSI_YELLOW = "\u001B[93m"
ANSI_RED    = "\u001B[91m"
ANSI_RESET  = "\u001B[0m"

# Load .env if available
try:
    from dotenv import load_dotenv
except ImportError:
    print(ANSI_CYAN + "[INFO] Installing python-dotenv..." + ANSI_RESET)
    os.system("pip install python-dotenv --user > /dev/null 2>&1")
    from dotenv import load_dotenv

ENV_LOADED = load_dotenv()  # Loads .env from current directory

# Prefix-based grouping
PREFIX_LABELS = {
    "CORE_":  "Core / Global",
    "SEC_":   "Cybersecurity Assistant",
    "MINER_": "Bitcoin Miner",
    "QNFT_":  "Quantum Holographic NFTs",
    "AGI_":   "AGI / ESQET",
    "APP_":   "Mobile App / Expo",
    "DB_":    "Databases / Vectors",
}

# Important legacy/unprefixed keys to explicitly check
LEGACY_EXPECTED = [
    "GROQ_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "HUGGINGFACE_API_KEY",
    "GITHUB_TOKEN", "NASA_API_KEY", "NIST_API", "IBM_TOKEN",
    "PINATA_API_KEY", "PINATA_API_SECRET", "PINATA_JWT",
    "QDRANT_API_KEY", "QDRANT_URL",
]

def classify_var(name: str) -> str:
    for prefix, label in PREFIX_LABELS.items():
        if name.startswith(prefix):
            return label
    return "Legacy / Unprefixed"

def scan_env() -> Dict[str, Dict[str, str]]:
    groups: Dict[str, Dict[str, str]] = defaultdict(dict)
    for k, v in os.environ.items():
        group = classify_var(k)
        status = "Empty" if (v is None or not str(v).strip()) else "Set"
        groups[group][k] = status
    return groups

def check_legacy(vars_list: List[str]) -> Dict[str, str]:
    status = {}
    for var in vars_list:
        val = os.getenv(var)
        if val is None:
            status[var] = "Not found"
        elif not str(val).strip():
            status[var] = "Empty"
        else:
            status[var] = "Found"
    return status

if __name__ == "__main__":
    # Clear screen (works in most terminals)
    print("\u001Bc", end="")

    # Header
    print(ANSI_PINK + "X-ENV UNIVERSAL CHECKER — Φ-LUCA CONFIG LATTICE" + ANSI_RESET)
    print(ANSI_BLUE + ".env loaded: " + ANSI_GREEN + str(ENV_LOADED) + ANSI_RESET)
    print("")

    # Grouped environment variables
    groups = scan_env()
    for label in sorted(groups.keys()):
        print(ANSI_CYAN + "=== " + label + " ===" + ANSI_RESET)
        for name in sorted(groups[label].keys()):
            status = groups[label][name]
            color = ANSI_GREEN if status == "Set" else ANSI_YELLOW
            print("  " + name + ": " + color + status + ANSI_RESET)
        print("")

    # Legacy keys check
    legacy_results = check_legacy(LEGACY_EXPECTED)
    print(ANSI_BLUE + "=== Legacy / Important Keys ===" + ANSI_RESET)
    missing = 0
    for name in LEGACY_EXPECTED:
        st = legacy_results[name]
        if st in ("Not found", "Empty"):
            missing += 1
            color = ANSI_RED
        elif st == "Found":
            color = ANSI_GREEN
        else:
            color = ANSI_YELLOW
        print("  " + name + ": " + color + st + ANSI_RESET)
    print("")

    # Summary
    total_vars = sum(len(v) for v in groups.values())
    print(ANSI_PINK + "Summary:" + ANSI_RESET)
    print(ANSI_BLUE + "  Total env vars in process: " + ANSI_GREEN + str(total_vars) + ANSI_RESET)
    print(ANSI_BLUE + "  Legacy keys checked: " + ANSI_GREEN + str(len(LEGACY_EXPECTED)) + ANSI_RESET)
    print(ANSI_BLUE + "  Legacy missing/empty: " + ANSI_RED + str(missing) + ANSI_RESET)
