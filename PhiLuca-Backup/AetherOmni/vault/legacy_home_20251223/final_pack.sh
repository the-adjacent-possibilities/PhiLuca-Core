#!/bin/bash
# ESQET Final Submission Packager

echo "📦 Bundling Theoria Omnia for Archival..."

# Create a clean distribution folder
mkdir -p ~/ESQET_DIST_2025

# Copy the Paper and Manifest
cp ~/ESQET_Whitepaper_2025.pdf ~/ESQET_DIST_2025/
cp ~/MANIFEST_FOR_THE_FUTURE.txt ~/ESQET_DIST_2025/
cp ~/ESQET_Whitepaper_2025.tex ~/ESQET_DIST_2025/

# Copy the Core Phinary Engines
cp ~/dal_phinary_engine.py ~/ESQET_DIST_2025/
cp ~/esqet_modulator.py ~/ESQET_DIST_2025/

# Zip it all up
tar -czvf ~/THEORIA_OMNIA_FULL_DEPOSIT.tar.gz -C ~/ ESQET_DIST_2025

echo "✅ Created: THEORIA_OMNIA_FULL_DEPOSIT.tar.gz"
echo "This is the file you will upload to Zenodo/Figshare."
