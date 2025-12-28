import subprocess
import json

class SensorTransducer:
    def __init__(self):
        self.phi = 1.61803398875

    def get_magnetic_flux(self):
        try:
            # -n 5 captures a small average to ensure the sensor wakes up
            res = subprocess.run(['termux-sensor', '-n', '5', '-s', 'magnetometer'], 
                                 capture_output=True, text=True, timeout=5)
            # Termux-sensor output can be messy; we take the last valid reading
            output = res.stdout.strip().split('\n')
            for line in reversed(output):
                if '"values"' in line or '{' in line:
                    data = json.loads(line)
                    mag = data['magnetometer']['values']
                    return (mag[0]**2 + mag[1]**2 + mag[2]**2)**0.5
            return 45.0 # Default Earth average if hardware is shy
        except:
            return 45.0 # Earth's ambient magnetic field in uT

    def get_location_alignment(self):
        try:
            res = subprocess.run(['termux-location'], capture_output=True, text=True, timeout=5)
            data = json.loads(res.stdout)
            return data['latitude'], data['longitude']
        except:
            return 38.4253, -105.0264 # Last known fix: Penrose, CO

    def calculate_environmental_fqc(self):
        mag = self.get_magnetic_flux()
        lat, lon = self.get_location_alignment()
        e_fqc = (mag / self.phi) % 1.0
        return {
            "flux_ut": round(mag, 4),
            "coordinates": (lat, lon),
            "env_fqc": round(e_fqc, 8)
        }
