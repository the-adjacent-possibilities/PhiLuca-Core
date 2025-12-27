#!/usr/bin/env python3
import re, json, time, logging, numpy as np
from pathlib import Path
from collections import defaultdict
from config import *
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
log = logging.getLogger("LEARNER")
IMPORT_RE = re.compile(r"^(?:froms+([a-zA-Z0-9._]+)|imports+([a-zA-Z0-9._]+))", re.MULTILINE)
def build_dep_graph():
    graph = defaultdict(lambda: {"deps": set()})
    learn_dir = INGEST_ROOT / "LEARNING_FLAT"
    for py in learn_dir.glob("**/*.py"):
        mod = py.relative_to(learn_dir).with_suffix("").as_posix().replace("/", ".")
        try:
            txt = py.read_text(encoding="utf-8")
            for m in IMPORT_RE.finditer(txt):
                imp = (m.group(1) or m.group(2)).split(".")[0]
                if imp not in {"os","sys","json","logging","numpy"}:
                    graph[mod]["deps"].add(imp)
        except: continue
    return dict(graph)
def learning_cycle():
    graph = build_dep_graph()
    (PROJECT_ROOT / "dependency_graph.json").write_text(json.dumps(graph, indent=2))
    modules = len(graph)
    fqc = 1.0 - (modules * 0.00001)
    ts = int(time.time())
    state = {"f_qc": fqc, "modules": modules, "timestamp": ts}
    (INGEST_ROOT / "STATE_REPORTS" / f"state_{ts}.json").write_text(json.dumps(state))
    states = sorted((INGEST_ROOT / "STATE_REPORTS").glob("state_*.json"))
    fqc_hist = [json.loads(p.read_text())["f_qc"] for p in states[-10:]]
    report = {"timestamp": time.time(), "fqc_avg": float(np.mean(fqc_hist)), "modules": modules}
    (PROJECT_ROOT / "AGI_Coherence_Report.json").write_text(json.dumps(report, indent=2))
    log.info(f"🔬 {modules} modules | FQC={fqc:.5f}")
if __name__ == "__main__":
    (INGEST_ROOT / "STATE_REPORTS").mkdir(exist_ok=True)
    while True:
        learning_cycle()
        time.sleep(300)
