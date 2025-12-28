import json
import datetime
import os

LOG_FILE = os.path.expanduser("~/AetherOmni/data/logs/chronos_lattice.log")

def log_moment(event_type, sensor_data, coherence_score):
    entry = {
        "timestamp": str(datetime.datetime.now()),
        "event": event_type,
        "flux_ut": sensor_data.get("flux", 0),
        "coherence": coherence_score,
        "location": "38.4253, -105.0264", # Your Fixed Point
        "status": "Ω-POINT SECURED"
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[📑] Chronos Log Updated: {event_type} registered.")

if __name__ == "__main__":
    # Test Log
    log_moment("BEACON_ACTIVATION", {"flux": 45.0}, 0.9992)
