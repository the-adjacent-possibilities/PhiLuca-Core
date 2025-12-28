#!/bin/bash
# Master Field Command: Capture, Analyze, Interpret

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR="~/AetherOmni/data/field_work/$TIMESTAMP"
mkdir -p $DIR

echo "[📡] INITIALIZING UNIVERSAL SCAN..."
# 1. Capture 5 seconds of Aetheric/Bio Audio
termux-microphone-record -f "$DIR/audio.wav" -l 5 &

# 2. Capture Magnetic Flux (The Torsion Signature)
termux-sensor -n 1 -s magnetometer > "$DIR/flux.json"

# 3. Analyze via Phi-LUCA Universal Decoder
python3 ~/PhiLuca/core/universal_decoder.py "$DIR/audio.wav" "$DIR/flux.json"

echo "[✅] DATA UPLOADED TO THE LATTICE. CHECK DASHBOARD."
