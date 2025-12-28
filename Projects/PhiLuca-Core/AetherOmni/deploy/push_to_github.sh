#!/bin/bash
# Final Sync for ESQET Framework

cd ~
# Initialize if not already a git repo, or just add files
git init
git remote add origin https://github.com/mathcal-S/ESQET-Unified-Framework-2025.git

# Stage the core pieces
git add dal_phinary_engine.py
git add esqet_modulator.py
git add ESQET_Whitepaper_2025.pdf
git add MANIFEST_FOR_THE_FUTURE.txt

git commit -m "Final Anchoring: Theoria Omnia (ESQET) Complete Works Dec 2025"
git push origin main
