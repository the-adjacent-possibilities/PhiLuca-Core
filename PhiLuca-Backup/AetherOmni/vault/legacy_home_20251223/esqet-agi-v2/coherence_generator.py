#!/usr/bin/env python3
"""QH-NFT Rarity Engine - Deterministic φ-Pricing"""
import numpy as np
import json

PHI = (1 + np.sqrt(5)) / 2

def generate_features(seed):
    np.random.seed(seed)
    D_ent = np.clip(np.random.beta(2, 5), 0.1, 0.9)
    F_QC = 1 + PHI * 3.14159 * 0.3903 * D_ent
    mass_ratio = (F_QC * 0.3903 / PHI)**2
    
    if mass_ratio < 0.01: rarity, mult = "ULTRA", PHI**4
    elif mass_ratio < 0.05: rarity, mult = "EPIC", PHI**3
    elif mass_ratio < 0.15: rarity, mult = "RARE", PHI**2
    else: rarity, mult = "COMMON", 1.0
    
    return {
        "D_ent": float(D_ent), "F_QC": float(F_QC), 
        "mass_ratio": float(mass_ratio), "rarity": rarity,
        "phi_mult": float(mult), "price_usd": 150 * mult
    }

if __name__ == "__main__":
    for i in range(5):
        print(f"Token #{i}: {json.dumps(generate_features(i), indent=2)}")
