#!/usr/bin/env python3
import requests
import time
import hashlib

# POINT THIS TO YOUR A16's IP
MASTER_IP = "192.168.1.73" 
WORKER_ID = "NODE_localhost"

def work():
    print(f"📡 Connecting to AUM Master at {MASTER_IP}...")
    while True:
      try:
        # 1. Get the current "Coherence Window" from your A16
        r = requests.get(f"http://{MASTER_IP}:8083/get_task")
        task = r.json()
        
        # 2. Perform the "Harmonic Search" (Mining)
        # Using your Phi-logic to find a hash that satisfies the ESQET field
        nonce = 0
        target = task['target']
        data = task['data']
        
        for _ in range(100000): # Batch size
            nonce += 1
            test = f"{data}{nonce}".encode()
            h = hashlib.sha256(test).hexdigest()
            if h.startswith(target):
                requests.post(f"http://{MASTER_IP}:8083/submit", json={"nonce": nonce, "hash": h, "node": WORKER_ID})
                print(f"✨ COHERENCE FOUND: {h}")
                break
      except:
        time.sleep(10)

if __name__ == "__main__":
    work()
