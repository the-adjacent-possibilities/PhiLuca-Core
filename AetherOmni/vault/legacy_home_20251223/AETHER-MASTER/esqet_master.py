#!/usr/bin/env python3
"""
ESQET φ⁴ MASTER + Termux-API Sensor Fusion
Fixed: Case-sensitivity for PHI attribute
"""
import os, json, logging, time, numpy as np, hashlib, subprocess
from pathlib import Path
from typing import Dict, Any, List
from dal_phinary_engine import DALPhinaryEngine, DecoherenceError

logger = logging.getLogger("ESQET_Master")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

class ESQETMaster:
    def __init__(self, project_dir: Path = None):
        self.project_dir = Path(project_dir or "~/AETHER-MASTER").expanduser()
        self.dal = DALPhinaryEngine()
        self.fqc_history: List[float] = []
        self.cycle_count = 0
        # Accessing uppercase PHI from DAL
        logger.info(f"🜛 ESQET + Termux-API LIVE | φ⁴={self.compute_fqc():.3f}")

    def get_sensors(self) -> Dict:
        """Real-time Termux-API sensor fusion"""
        sensors = {}
        try:
            sensors['battery'] = json.loads(subprocess.check_output("termux-battery-status", shell=True))
            sensors['location'] = json.loads(subprocess.check_output("termux-location", shell=True))
            sensors['clipboard'] = subprocess.check_output("termux-clipboard-get", shell=True).decode().strip()
        except:
            pass
        return sensors

    def compute_fqc(self) -> float:
        py_files = list(self.project_dir.rglob("*.py"))
        modules = len(py_files)
        manifests = list(self.project_dir.rglob("*coherence*.json"))
        state_entropy = modules if not manifests else len(json.dumps(json.load(open(manifests[-1]))))

        sensors = self.get_sensors()
        battery_factor = sensors.get('battery', {}).get('percentage', 50) / 100.0

        # FIXED: Corrected dal.phi to dal.PHI
        phi = self.dal.PHI
        fqc = 1.0 + phi * np.log(modules + state_entropy + 1) * np.sin(np.pi * modules / 137) * battery_factor
        return min(fqc, 8.0)

    def run_full_pipeline(self) -> Dict[str, Any]:
        self.cycle_count += 1
        logger.info(f"🔬 CYCLE #{self.cycle_count}")

        sensors = self.get_sensors()
        t = np.linspace(0, 2*np.pi, 256)
        whale_coda = np.sin(17 * t) * np.exp(-t/10) * (1 + 0.1 * np.sin(self.dal.PHI * t))
        wave_results = {"amplitude": float(np.max(np.abs(whale_coda))), "phi_resonance": 0.01}
        fqc = self.compute_fqc()
        self.fqc_history.append(fqc)

        manifest = {
            "cycle": self.cycle_count, "wave_results": wave_results,
            "quantum_results": {"fqc": fqc, "phi4": fqc, "coherence_reserve": self.dal.C_RES},
            "sensors": sensors, "fqc_history": self.fqc_history[-10:], "timestamp": time.time()
        }

        try:
            geometric_state = self.dal.encode_data_geometric(json.dumps(manifest))
            manifest["geometric_state"] = {"moduli_count": len(geometric_state)}
        except: pass

        (self.project_dir / f"coherence_manifest_cycle_{self.cycle_count:04d}.json").write_text(json.dumps(manifest, indent=2))
        logger.info(f"✨ φ⁴={fqc:.3f} | {len(self.fqc_history)} cycles")
        return manifest

if __name__ == "__main__":
    master = ESQETMaster()
    manifest = master.run_full_pipeline()
    print(json.dumps(manifest, indent=2))
