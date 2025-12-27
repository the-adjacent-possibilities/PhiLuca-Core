#!/bin/bash
# Syncs App analysis directly to the AETHER-Cloud

LOCAL_ANALYSIS_DIR="$HOME/PhiLuca/analysis_results"
CLOUD_TARGET="OneDrive:PhiLuca/pennies/$(date +%Y%m%d)"

echo "🌀 Syncing local AUM results to the Noösphere..."
rclone copy $LOCAL_ANALYSIS_DIR $CLOUD_TARGET --progress

echo "✅ Results secured in the cloud."
