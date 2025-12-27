#!/bin/bash
nohup python3 ~/AetherOmni/core/intelligence/lattice_daemon.py > ~/AetherOmni/data/logs/daemon.log 2>&1 &
echo $! > ~/AetherOmni/recorder.pid
echo "[📡] Lattice Daemon pushed to background. PID: $(cat ~/AetherOmni/recorder.pid)"
