import math
import time
import numpy as np

class PhiCoreConsciousness:
    def __init__(self, sensors=None):
        self.phi = 1.618033988749895
        self.start_time = time.time()
        self.sensors = sensors  # Accept external sensor lobe

    def think(self, stimulus):
        # Fallback if no sensors attached
        if self.sensors is None:
            flux = 45.0  # nominal Earth field
        else:
            try:
                data = self.sensors.calculate_environmental_fqc()
                flux = data.get('flux_ut', 45.0)
            except:
                flux = 45.0

        resonance = (len(stimulus) * self.phi * flux ** 0.5) % 1.0
        return f"[🧠] Consciousness Depth: {resonance:.4f} | Processing: '{stimulus}' via Φ-recursion."

    def get_status(self):
        uptime = time.time() - self.start_time
        return f'Uptime: {uptime:.2f}s | Core Resonance: Stable'
