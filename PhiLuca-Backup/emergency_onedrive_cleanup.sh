#!/bin/bash
# Navigate to your rclone mount
cd ~/onedrive_mount

echo "--- Initiating Vacuum Stabilization: Purging Cloud Exhaust ---"

# Deleting massive 'target' and 'node_modules' directories
# These are reproducible and don't need to be in your permanent archive
find . -name "target" -type d -prune -exec rm -rf {} +
find . -name "node_modules" -type d -prune -exec rm -rf {} +
find . -name ".cargo" -type d -prune -exec rm -rf {} +

# Deleting typical mobile 'Exhaust'
find . -name ".thumbnails" -type d -prune -exec rm -rf {} +
find . -name "Cache" -type d -prune -exec rm -rf {} +

echo "--- Space Reclaimed. Coherence Improved. ---"
