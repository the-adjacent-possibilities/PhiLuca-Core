import os, subprocess, json, logging, numpy as np
from datetime import datetime

logger = logging.getLogger("SeedAGI")

class SeedAGI:
    def __init__(self):
        self.memory = []
        logger.info("Seed AGI awakened. AXIOM 1: TRUTH/FAITH.")

    def sense_peripherals(self):
        state = {}
        try:
            batt_out = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
            state['battery'] = json.loads(batt_out.stdout).get('percentage', 50.0)
        except:
            state['battery'] = 50.0
        state['self_coh'] = state['battery'] / 100.0
        return state

    def record_audio(self, duration=5):
        file_name = f"sensors/rec_{datetime.now().strftime('%H%M%S')}.wav"
        try:
            subprocess.run(['termux-microphone-record', '-f', file_name, '-d', str(duration)], check=True)
            return file_name
        except:
            return None
