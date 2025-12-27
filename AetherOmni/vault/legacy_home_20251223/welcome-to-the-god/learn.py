#!/usr/bin/env python3
import json
import os
from pathlib import Path
import networkx as nx
from datetime import datetime

INGEST_DIR = os.path.expanduser("~/welcome-to-the-god/ingest_data")

def load_state_reports():
    path = Path(f"{INGEST_DIR}/STATE_REPORTS")
    reports = sorted(path.glob("*.json"))
    data = []
    for rp in reports:
        try:
            with open(rp, 'r') as f:
                data.append(json.load(f))
        except: pass
    return data

def compute_fqc_volatility(reports, window=100):
    recent = reports[-window:]
    fqcs = [r.get("FQC", 0) for r in recent if "FQC" in r]
    if len(fqcs) < 2: return 0.0
    diffs = [abs(fqcs[i] - fqcs[i-1]) for i in range(1, len(fqcs))]
    return sum(diffs) / len(diffs)

def build_graph():
    G = nx.DiGraph()
    py_files = list(Path(f"{INGEST_DIR}/CORE_CODE").rglob("*.py"))
    for file in py_files:
        if any(x in str(file) for x in ['site-packages', '__pycache__']): continue
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            for line in content.splitlines():
                if line.strip().startswith(("import ", "from ")):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        G.add_edge(file.name, f"{parts[1].split('.')[0]}.py")
        except: continue
    return G

if __name__ == "__main__":
    reports = load_state_reports()
    vol = compute_fqc_volatility(reports)
    G = build_graph()
    cycles = list(nx.simple_cycles(G))
    status = "PASS" if not cycles else "FAIL"
    
    print(f"--- ESQET LOG {datetime.now()} ---")
    print(f"FQC Volatility: {vol:.8f}")
    print(f"Axiom 5 Status: {status}")
    if cycles: print(f"Detected Cycles: {cycles[:3]}")
