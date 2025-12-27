#!/usr/bin/env python3
import time
import subprocess
import os
from pathlib import Path

# Configuration
CHECK_INTERVAL = 3600  # Scan every 1 hour
NOTES_TRIGGER_FILE = Path("~/AetherOmni/data/field_traces/new_insight.txt").expanduser()
REFLECTOR_PATH = Path("~/AetherOmni/core/intelligence/reflector.py").expanduser()

def check_for_resonance_triggers():
    """Checks for new code snippets or insights that trigger evolution."""
    if NOTES_TRIGGER_FILE.exists():
        print(f"[!] New Insight Detected in {NOTES_TRIGGER_FILE}")
        
        # Trigger the Reflector to integrate new logic
        # In a production state, this would parse the text for logic strings
        try:
            subprocess.run(["python3", str(REFLECTOR_PATH)], check=True)
            # Archive the trigger after successful evolution
            archive_path = NOTES_TRIGGER_FILE.with_suffix(".processed")
            NOTES_TRIGGER_FILE.rename(archive_path)
            print("[✅] Evolution Cycle Complete. Trigger Archived.")
        except Exception as e:
            print(f"[❌] Evolution Failed: {e}")

def main():
    print("--- Lattice Daemon: Active ---")
    while True:
        check_for_resonance_triggers()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
