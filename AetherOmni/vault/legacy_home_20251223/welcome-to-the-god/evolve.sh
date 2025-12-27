#!/bin/bash
REPORT_FILE=~/welcome-to-the-god/evolve_report.txt
echo "[EVOLVE] Analyzing module centrality..."

python3 -c '
import networkx as nx
from pathlib import Path
G = nx.DiGraph()
for file in Path("ingest_data/CORE_CODE").rglob("*.py"):
    try:
        content = file.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            if line.strip().startswith(("import ", "from ")):
                mod = line.strip().split()[1].split(".")[0]
                G.add_edge(file.name, f"{mod}.py")
    except: continue
central = nx.degree_centrality(G)
top = sorted(central.items(), key=lambda x: -x[1])[:3]
for node, score in top:
    print(f"TARGET:{node}|SCORE:{score:.4f}")
' > $REPORT_FILE

cat $REPORT_FILE
