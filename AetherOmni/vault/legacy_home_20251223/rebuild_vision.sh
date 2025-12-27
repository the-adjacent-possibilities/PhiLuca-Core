#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "🜛 REBUILDING VISION CORE — Φ-LUCA v2.1 (Pre-built Packages)"

# Add x11-repo for opencv-python (required in recent Termux)
pkg install -y x11-repo

# Update mirrors & system
termux-change-repo
pkg update -y
pkg upgrade -y

# Install pre-built vision stack
pkg install -y python python-numpy opencv-python tesseract pytesseract

# Install English language data (default; add more if needed, e.g. tesseract-data-fra)
pkg install -y tesseract-data-eng

# Test imports
python -c "import cv2, numpy as np, pytesseract; print('✅ Vision Core Rebuilt — Imports Successful')"

echo "🎯 Rebuild Complete! Vision system operational."
