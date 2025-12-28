#!/bin/bash
# Passive Field Capture - No Audio Cues, Total Silence.

mkdir -p ~/AetherOmni/data/field_logs

while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "[🤫] Capturing Lattice State: $TIMESTAMP"
    
    # 1. Silent Photo (Identify objects/geometry)
    termux-camera-photo ~/AetherOmni/data/field_logs/view_$TIMESTAMP.jpg
    
    # 2. Background Audio (Record bees/cows/ringing)
    termux-microphone-record -f ~/AetherOmni/data/field_logs/audio_$TIMESTAMP.wav -l 10
    
    # 3. Log Magnetometer (The Torsion Anchor)
    termux-sensor -n 1 -s magnetometer > ~/AetherOmni/data/field_logs/flux_$TIMESTAMP.json
    
    # 4. Wait for the next Golden Window (approx 1 minute)
    sleep 60
done
