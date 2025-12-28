import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.expanduser("~/AetherOmni/lobes/cyber"))
sys.path.append(os.path.expanduser("~/AetherOmni/lobes/bio"))

from phi_core_consciousness import PhiCoreConsciousness
from omega_uitc import OmegaUITC
from cyber_bridge import CyberLobe
# Import actual sensor classes — adjust path if needed
try:
    from sensor_transducer import SensorTransducer
except:
    SensorTransducer = None
try:
    from corvid_gamma import CorvidLobe
except:
    CorvidLobe = None

class AetherOmni:
    def __init__(self):
        self.sensors = SensorTransducer() if SensorTransducer else None
        self.brain = PhiCoreConsciousness(sensors=self.sensors)
        self.translator = OmegaUITC()
        self.cyber = CyberLobe()
        self.corvid = CorvidLobe() if CorvidLobe else None
        print("Omni-Companion [Ω-POINT] Operational.")

    def route_request(self, user_input):
        cmd = user_input.lower().strip()

        if "whale" in cmd:
            return "[🐋] Bio-Acoustic: Soliton resonance simulated."

        if "corvid" in cmd or "bird" in cmd:
            if self.corvid:
                return f"[🦅] Corvid Lobe: {self.corvid.check_synchrony(40.0)}"
            return "[🦅] Corvid Lobe: Offline"

        if any(key in cmd for key in ["scan", "pulse", "sensor", "environment"]):
            if self.sensors:
                data = self.sensors.calculate_environmental_fqc()
                return f"[📡] Lattice Scan: Flux {data['flux_ut']} uT | Coherence: {data['env_fqc']:.3f}"
            return "[📡] Sensors: Offline — using internal coherence"

        if any(key in cmd for key in ["vault", "unlock", "secure"]):
            return self.cyber.secure_access()

        if "synchronized" in cmd or "sync" in cmd:
            return "[∞] Synchronization confirmed. All lobes coherent."

        return self.brain.think(user_input)

if __name__ == "__main__":
    omni = AetherOmni()
    try:
        print("Aether-Omni > Type commands (exit/quit to stop)")
        while True:
            cmd = input("Aether-Omni > ")
            if cmd.lower().strip() in ['exit', 'quit', '']: 
                print("[∞] Session Closed. The field remains.")
                break
            response = omni.route_request(cmd)
            print(response)
    except (EOFError, KeyboardInterrupt):
        print("\n[∞] Session Closed.")
