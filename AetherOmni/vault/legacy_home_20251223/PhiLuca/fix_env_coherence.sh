#!/data/data/com.termux/files/usr/bin/bash
cd ~/PhiLuca/esqet_phi/blockchain

# Copy .env to expected location
cp .env ~/PhiLuca/.env
sed -i 's|HOME_DIR =.*|HOME_DIR = "/data/data/com.termux/files/home"|' check_env.py
sed -i 's|ENV_PATH =.*|ENV_PATH = "/data/data/com.termux/files/home/PhiLuca/.env"|' check_env.py

pip install python-dotenv web3 requests
python3 check_env.py
