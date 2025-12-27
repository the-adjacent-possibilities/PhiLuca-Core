#!/bin/bash
cd "$(dirname "$0")" || { echo "Failed to cd to project dir"; exit 1; }
echo "🌀 ONE-CLICK ESQET DEPLOYMENT..."

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "🛑 python3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "🛑 node not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "🛑 npm not found"; exit 1; }

# Python venv
python3 -m venv esqet-env || { echo "Failed to create venv"; exit 1; }
source esqet-env/bin/activate || { echo "Failed to activate venv"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install Python requirements"; deactivate; exit 1; }

# Node NFT service
cd nft || { echo "Failed to enter nft directory"; exit 1; }
npm install || { echo "Failed to install Node dependencies"; cd ..; exit 1; }
cd ..

# Test coherence
python tests/test_faberge_consensus.py || { echo "Coherence test failed"; exit 1; }

# Launch services (background with basic status check)
python seed_agi.py > logs/agi.log 2>&1 & 
AGI_PID=$!
echo "AGI Oracle started (PID $AGI_PID, port 5000)"

cd nft
node lazy_mint_service.js > ../logs/nft.log 2>&1 &
NFT_PID=$!
echo "NFT Server started (PID $NFT_PID, port 3000)"
cd ..

echo "✅ DEPLOYED! Check logs/ for output."
echo "AGI: localhost:5000 | NFT: localhost:3000"
echo "To stop: kill $AGI_PID $NFT_PID"
