#!/usr/bin/env python3
"""QH-NFT Features: Deterministic D_ent/F_QC/mass_ratio + φ-Rarity"""
import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PI = np.pi
DELTA = 0.3903

def generate_nft_features(seed: int) -> dict:
    np.random.seed(seed)
    D_ent = np.clip(np.random.beta(2, 5), 0.1, 0.9)
    F_QC = 1 + PHI * PI * DELTA * D_ent
    mass_ratio = (F_QC * DELTA / PHI)**2
    
    if mass_ratio < 0.01: rarity, mult = "ULTRA", PHI**4  # 6.85x
    elif mass_ratio < 0.05: rarity, mult = "EPIC", PHI**3  # 4.23x
    elif mass_ratio < 0.15: rarity, mult = "RARE", PHI**2  # 2.62x
    else: rarity, mult = "COMMON", 1.0
    
    return {
        "D_ent": float(D_ent), "F_QC": float(F_QC), "mass_ratio": float(mass_ratio),
        "rarity": rarity, "phi_mult": float(mult), "price_usd": 150 * mult
    }

if __name__ == "__main__":
    for i in range(5): print(f"#{i}: {generate_nft_features(i)}")
