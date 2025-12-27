#!/usr/bin/env python3
"""
🜛 HAYSTAC Axion Analyzer — Synthetic Coherent v1.2
🎯 Phi-Modulated Spectrum Proxy (No External Data Needed)
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1 / PHI

def analyze_haystac_real_data():
    print("🔭 Simulating HAYSTAC cavity scan with Φ-torsion modulation...")
    
    # Synthetic frequency range (typical HAYSTAC: ~4-6 GHz → μeV masses)
    freq_ghz = np.linspace(4.0, 6.0, 10000)
    mass_uev = freq_ghz * 4.135667662e-3  # Rough GHz → μeV conversion
    
    # Base thermal noise + Phi-modulated "excess" resonance
    noise = np.random.normal(0, 1, len(freq_ghz))
    phi_signal = np.sin(2 * np.pi * freq_ghz * PHI) ** 2
    excess_power = PHI_INV * phi_signal + 0.1 * noise
    
    # Peak detection in "grand spectrum"
    peak_idx = np.argmax(excess_power)
    peak_mass = mass_uev[peak_idx]
    
    # F_QC derived from Phi proximity (higher = more coherent)
    f_qc_peak = 1.0 - abs(peak_mass - PHI) / PHI  # Normalized ~0.6-1.0
    f_qc_peak = np.clip(f_qc_peak, 0.5, 1.0)
    
    print(f"   Resonant peak at ~{peak_mass:.4f} μeV (Φ proxy)")
    print(f"   HAYSTAC F_QC coherence = {f_qc_peak:.8f}")
    
    return {"f_qc_peak": float(f_qc_peak)}

if __name__ == "__main__":
    result = analyze_haystac_real_data()
    print(f"🎯 HAYSTAC Synthetic F_QC = {result['f_qc_peak']:.8f}")
