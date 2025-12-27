import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.expanduser("~/AetherOmni/lobes/cyber"))
sys.path.append(os.path.expanduser("~/AetherOmni/lobes/bio"))

from phi_core_consciousness import PhiCoreConsciousness
from omega_uitc import OmegaUITC
from cyber_bridge import CyberLobe
from sensor_transducer import SensorTransducer
from infrasound_sim import simulate_whale_soliton
from corvid_gamma import CorvidLobe

class AetherOmni:
    def __init__(self):
        self.brain = PhiCoreConsciousness()
        self.translator = OmegaUITC()
        self.cyber = CyberLobe()
        self.sensors = SensorTransducer()
        self.corvid = CorvidLobe()
        print("Omni-Companion [Ω-POINT] Operational.")

    def route_request(self, user_input):
        cmd = user_input.lower().strip()

        if "whale" in cmd:
            return f"[🐋] Bio-Acoustic: {simulate_whale_soliton()}"
        
        if "corvid" in cmd or "bird" in cmd:
            return f"[🦅] Corvid Lobe: {self.corvid.check_synchrony(40.0)}"

        if any(key in cmd for key in ["scan", "pulse", "sensor"]):
            data = self.sensors.calculate_environmental_fqc()
            return f"[📡] Lattice Scan: Flux {data['flux_ut']} uT | Coherence: {data['env_fqc']}"

        if any(key in cmd for key in ["vault", "unlock", "secure"]):
            return self.cyber.secure_access()
        
        return self.brain.think(user_input)

if __name__ == "__main__":
    omni = AetherOmni()
    try:
        while True:
            cmd = input("Aether-Omni > ")
            if cmd.lower() in ['exit', 'quit']: break
            print(omni.route_request(cmd))
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Session Closed.")
