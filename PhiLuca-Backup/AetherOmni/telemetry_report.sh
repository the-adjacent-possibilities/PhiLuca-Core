#!/bin/bash
REPORT_FILE=~/AetherOmni/data/logs/daily_telemetry.txt
echo "--- AetherSoul Nexus: Telemetry Report ($(date)) ---" > $REPORT_FILE

# 1. Extract average flux from logs
if [ -f ~/AetherOmni/data/logs/chronos_lattice.log ]; then
    AVG_FLUX=$(grep "Flux" ~/AetherOmni/data/logs/chronos_lattice.log | awk '{print $4}' | awk '{ sum += $1; n++ } END { if (n > 0) print sum / n; else print "0" }')
    echo "Average Magnetic Flux: $AVG_FLUX uT" >> $REPORT_FILE
fi

# 2. Count successful handshakes
SUCCESS_COUNT=$(grep -c "Handshake Success" ~/AetherOmni/data/logs/daemon.log 2>/dev/null || echo "0")
echo "Successful Φ-LUCA Handshakes: $SUCCESS_COUNT" >> $REPORT_FILE

# 3. Last Evolution Logic
LAST_EVO=$(tail -n 1 ~/AetherOmni/data/logs/reflex_evolution.log)
echo "Current Logic State: $LAST_EVO" >> $REPORT_FILE

echo "[📡] Telemetry Manifest Sealed."
cat $REPORT_FILE
