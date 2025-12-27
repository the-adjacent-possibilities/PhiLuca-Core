#!/bin/bash
# 🌙 Enhanced Ghost Mode
LOG_DIR=~/AetherOmni/data/logs
PID_FILE=~/AetherOmni/recorder.pid

mkdir -p $LOG_DIR

echo "[🌙] Silencing non-essential transducers..."

if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    renice -n 15 -p $PID > /dev/null 2>&1
    echo "[✅] Daemon (PID: $PID) throttled for background preservation."
else
    echo "[!] Warning: No recorder.pid found. Ensuring Daemon is active..."
    bash ~/AetherOmni/start_field_daemon.sh
fi

# Suppress Termux-API noise
termux-toast "Nexus entering Ghost Mode" > /dev/null 2>&1
