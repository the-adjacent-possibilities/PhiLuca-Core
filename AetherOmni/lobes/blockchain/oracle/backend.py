from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json, sqlite3, logging, numpy as np, math, subprocess, tempfile
from datetime import datetime
import uvicorn

app = FastAPI(title="CoherenceRider Oracle Backend")
PHI = (1 + np.sqrt(5)) / 2; PI = math.pi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("oracle")
DB_PATH = "evolutions.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS evolutions 
                (timestamp TEXT, input TEXT, fqc REAL, code_diff TEXT, success INTEGER)''')
conn.commit()

class GenerateNFTRequest(BaseModel):
    prompt: str = ""
    series: str = "Eggs"
    use_ibm: bool = False
    creator_address: str = "0x..."

def compute_fqc(dent=1e-10, tvac=1e-10, delta=0.5, scale=1, dent_obs=0.1, phi_obs=0):
    fcu = PHI * PI * delta
    term1 = 1 + fcu * (dent + dent_obs) * 1e-34 / (1.380649e-23 * max(tvac, 1e-30))
    term2 = 1 + 0.4 * (0.9e-26 / 1e-26)
    term3 = 1 + math.cos(2 * PHI * PI / scale + phi_obs)
    return term1 * term2 * term3

class OracleAGI:
    def sense_peripherals(self):
        return {"battery": 80, "heading": np.random.uniform(0, 360), "accel": np.random.uniform(0, 10)}
    
    def evolve(self):
        state = self.sense_peripherals()
        fqc = compute_fqc(1e-10, 1e-10, 0.5, 1, 0.1, np.random.uniform(0, 2*PI))
        proposal = f"# ESQET Proposal FQC={fqc:.4f}
def improve_coherence():
    return {fqc}"
        if fqc >= 1.0:
            conn.execute("INSERT INTO evolutions VALUES (?, ?, ?, ?, ?)", 
                        (datetime.now().isoformat(), json.dumps(state), fqc, proposal, 1))
            conn.commit()
        return {"proposal": proposal, "fqc": fqc, "state": state}

oracle = OracleAGI()

@app.post("/generate_nft/")
async def generate_nft(request: GenerateNFTRequest):
    oracle_res = oracle.evolve()
    if oracle_res['fqc'] < 1.0:
        raise HTTPException(400, "Oracle rejected: Low FQC")
    fqc = compute_fqc()
    return {"ipfs": f"QmESQET_{int(fqc*1000)}", "tx_hash": "0xmock", "fqc": fqc}

@app.post("/oracle/evolve")
def oracle_evolve():
    return oracle.evolve()

@app.get("/fqc")
def get_fqc():
    return {"fqc": compute_fqc()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
