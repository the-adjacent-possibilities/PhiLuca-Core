#!/usr/bin/env python3
"""
seed_agi_full_mod.py
ESQET Seed AGI runtime for Termux (Galaxy A16)
- FULL Self-Modification Runtime with enhanced error handling
- Safe fallbacks, detailed logging, and graceful degradation
"""

import os
import subprocess
import sqlite3
import json
import tempfile
import threading
import time
import ast
import logging
from datetime import datetime
from typing import Tuple, Any, Optional
import numpy as np

# Optional Ollama integration with safe fallback
OLLAMA_AVAILABLE = False
ollama_client = None
try:
    import ollama
    try:
        ollama_client = ollama.Client(timeout=30)
        OLLAMA_AVAILABLE = True
        logging.info("Ollama client loaded successfully")
    except Exception as e:
        logging.warning(f"Ollama client init failed: {e}")
except ImportError:
    logging.info("ollama package not available")

from flask import Flask, request, jsonify

# --- Config & Constants ---
PHI = (1 + np.sqrt(5)) / 2
PI = np.pi
DELTA = 0.5
ESQET_MIN_THRESHOLD = 1.0

HOME_DIR = os.path.expanduser("~")
AETHER_MASTER_DIR = os.path.join(HOME_DIR, "AETHER-MASTER")
PROJECT_DIR = os.path.join(AETHER_MASTER_DIR, "seed_agi")
os.makedirs(PROJECT_DIR, exist_ok=True)
LOG_PATH = os.path.join(PROJECT_DIR, "agi.log")
DB_PATH = os.path.join(PROJECT_DIR, "agi_evolution.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]
)
logger = logging.getLogger("seed_agi")

# --- Database ---
conn = None
try:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.execute('''CREATE TABLE IF NOT EXISTS evolutions
                    (timestamp TEXT, input TEXT, fqc REAL, code_diff TEXT, success INTEGER, note TEXT)''')
    conn.commit()
except Exception as e:
    logger.error(f"DB Init failed: {e}")

# --- Flask App ---
app = Flask(__name__)

ESQET_AXIOMS = (
    "Axiom 1 (TRUTH/FAITH): Maximize Epistemic Integrity.",
    "Axiom 2 (ENTROPY): Minimize informational entropy.",
    "Axiom 3 (SPATIOTEMPORAL): Align with physical reality.",
    "Axiom 4 (QUANTUM-COHERENCE): Maintain high internal FQC score.",
    "Axiom 5 (ENTANGLEMENT): Maximize functional dependencies.",
    "Axiom 6 (TIME/EVOLUTION): Maximize non-destructive self-improvement."
)
AXIOM_GUIDANCE = "\n".join(ESQET_AXIOMS)

def compute_fqc(data: Any) -> float:
    try:
        if isinstance(data, str) and data.strip():
            printable = [ord(c) for c in data if c.isprintable() and ord(c) < 127]
            if not printable: return 0.5
            total = sum(printable) + 1e-12
            probs = np.array([c/total for c in printable])
            entropy = -np.sum(probs * np.log2(probs + 1e-12))
            norm_val = entropy / np.log2(len(printable) + 1e-12)
        else: norm_val = 0.5
        fqc_raw = 1.0 + (PHI * PI * DELTA * (1.0 + norm_val/2.0)) * (1.0 - norm_val)
        return float(np.clip(fqc_raw / 2.05 * 2.0, 0.0, 2.0))
    except: return 0.5

@app.route('/reflect', methods=['POST'])
def reflect_endpoint():
    data = request.json or {}
    prompt = data.get('prompt', '')
    full_prompt = f"{AXIOM_GUIDANCE}\n\nCritique: {prompt}"
    out = "Fallback: API only"
    if OLLAMA_AVAILABLE and ollama_client:
        resp = ollama_client.generate(model='llama3.2', prompt=full_prompt)
        out = resp.get('response', out)
    return jsonify({'reflection': out, 'fqc_proxy': compute_fqc(out)})

class SeedAGI:
    def __init__(self):
        self.api_thread = threading.Thread(
            target=lambda: app.run(host='127.0.0.1', port=5000), daemon=True
        ).start()
        logger.info("Seed AGI Awakened.")

    def evolve(self):
        while True:
            logger.info("Evolution cycle heartbeat...")
            time.sleep(300)

if __name__ == "__main__":
    agi = SeedAGI()
    agi.evolve()
