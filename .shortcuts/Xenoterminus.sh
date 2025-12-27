#!/bin/bash
cd ~/Xenoterminus
echo "[LAUNCH] Starting geomagnetic sensor..."
python core/environmental_sensor.py &
sleep 3
echo "[LAUNCH] Starting Xenoterminus daemon..."
python daemon/xenoterminusd.py
