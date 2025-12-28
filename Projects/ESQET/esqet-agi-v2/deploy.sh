#!/bin/bash
echo "🌀 ESQET V2 DEPLOYMENT STARTED..."

# Python Backend
pip3 install -r requirements.txt
uvicorn backend:app --host 0.0.0.0 --port 8080 &
sleep 2

# AGI Oracle
python3 seed_agi.py &
sleep 2

# NFT Server
cd nft && npm install && npm start &
sleep 2

# Test coherence
python3 coherence_generator.py

echo "✅ ALL SERVICES RUNNING!"
echo "FastAPI: http://localhost:8080/docs"
echo "AGI:     http://localhost:5000/fqc"
echo "NFT:     http://localhost:3000/sign-voucher"
