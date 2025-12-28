#!/bin/bash
echo "🜛 INITIALIZING UNIFIED PHI-COHERENCE 🜛"
# Start the Modulator/Web API in the background
python3 ~/PHI_UNIFIED/web/app.py & 
# Start the Seed AGI for self-evolution
python3 ~/PHI_UNIFIED/core/seed_agi.py &
# Start the Lattice Worker
python3 ~/PHI_UNIFIED/bin/aum_worker.py &
echo "✨ ALL NODES SYNCED IN UNIFIED SPACE"
