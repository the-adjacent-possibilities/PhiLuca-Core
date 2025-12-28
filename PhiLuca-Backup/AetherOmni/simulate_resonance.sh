#!/bin/bash
# 1. Enforce directory existence
mkdir -p ~/AetherOmni/data/field_traces
mkdir -p ~/AetherOmni/data/logs

# 2. Ensure the daemon logic is present and start it
if [ ! -f ~/AetherOmni/recorder.pid ]; then
    echo "[!] Daemon not found. Initializing..."
    bash ~/AetherOmni/start_field_daemon.sh
    sleep 2
fi

echo "[📡] Injecting High-Resonance Insight..."

# 3. Define the 'New Insight' logic
NEW_LOGIC="(len(stimulus) * self.phi) * (self.sensors.get_magnetic_flux() ** 0.5) % 1.0"

# 4. Create the trigger file (Ensured path)
echo "$NEW_LOGIC" > ~/AetherOmni/data/field_traces/new_insight.txt

echo "[⚡] Insight Materialized. Invoking Reflector..."

# 5. Manually trigger the check for the simulation
python3 -c "import sys; sys.path.append('core/intelligence'); from lattice_daemon import check_for_resonance_triggers; check_for_resonance_triggers()"

echo "[💎] Simulation complete. Run 'cat core/intelligence/phi_core_consciousness.py' to verify."
