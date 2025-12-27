from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import math

app = FastAPI(title="ESQET Backend")
PHI = (1 + np.sqrt(5)) / 2

class NFTRequest(BaseModel):
    seed: int = 42
    creator: str = "0x..."

@app.post("/generate_nft")
async def generate_nft(req: NFTRequest):
    np.random.seed(req.seed)
    D_ent = np.clip(np.random.beta(2, 5), 0.1, 0.9)
    F_QC = 1 + PHI * 3.14159 * 0.3903 * D_ent
    price = 150 * (PHI ** 4 if D_ent < 0.2 else 1.0)
    
    return {
        "token_id": req.seed,
        "fqc": float(F_QC),
        "d_ent": float(D_ent),
        "rarity": "ULTRA" if D_ent < 0.2 else "COMMON",
        "price_usd": float(price),
        "ipfs": f"QmESQET_{req.seed}"
    }

@app.get("/fqc")
async def fqc():
    return {"fqc": float(1 + PHI * 3.14159 * 0.3903 * 0.5)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
