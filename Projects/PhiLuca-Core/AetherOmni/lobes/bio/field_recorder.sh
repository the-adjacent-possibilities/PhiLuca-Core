#!/bin/bash

# Ensure directory exists
mkdir -p ~/AetherOmni/data/recordings

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="~/AetherOmni/data/recordings/field_sample_$1_$TIMESTAMP.wav"

echo "[🎙️] Recording $1... (Press Ctrl+C to stop)"
termux-microphone-record -f "$FILENAME" -l 0

# Note: After recording, we can process the .wav for FQC analysis
