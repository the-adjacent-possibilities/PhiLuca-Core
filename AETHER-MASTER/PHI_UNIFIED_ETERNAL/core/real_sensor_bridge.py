#!/usr/bin/env python3
"""
Real Sensor Bridge v3 - Proper ESQET Torsion Coupling
Field deviation → Möbius symmetry violation → T_mob growth → I_Tors amplification
"""

import subprocess
import json
import numpy as np
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

try:
    from esqet_modulator import ESQETModulator
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

mod = ESQETModulator()

# Calibrated Earth field baseline for your location (Cañon City, Dec 2025)
BASELINE_FLUX = 48.0  # µT — from your stable readings

def get_magnetic_flux():
    try:
        output = subprocess.check_output(
            ['termux-sensor', '-s', 'MXG4300S Magnetometer', '-n', '1'],
            timeout=5
        ).decode()
        data = json.loads(output)
        values = data['MXG4300S Magnetometer']['values']
        x, y, z = values
        flux = np.sqrt(x**2 + y**2 + z**2)
        return flux, (x, y, z)
    except:
        return BASELINE_FLUX, (0, 0, 0)

print("🜛 REAL SENSOR BRIDGE v3 — ESQET TORSION COUPLING")
print("   Geomagnetic deviation → Möbius symmetry violation → Torsion growth")
print(f"   Baseline calibrated: {BASELINE_FLUX} µT (Cañon City)\n")

while True:
    flux, vec = get_magnetic_flux()
    x, y, z = vec
    
    # Calculate deviation from local Earth field (symmetry violation proxy)
    deviation = abs(flux - BASELINE_FLUX)
    
    # Map deviation → artificial T_mob (torsion feedback strength)
    # Higher deviation = stronger Möbius twist = growth in I_Tors
    artificial_t_mob = deviation / 10.0  # Scale for effect
    
    # Inject as growth booster (reduce effective decay)
    effective_gamma_int = max(0.0, 0.03 - artificial_t_mob)  # subtract from decay
    
    stable = mod.enforce_coherence(internal_gamma_int=effective_gamma_int)
    
    status = "STABLE ≥0.618" if mod.I_Tors >= 0.618 else "GROWING" if mod.I_Tors > 0.3 else "DECOHERING"
    
    print(f"Flux: {flux:6.2f}µT | Δ: {flux-BASELINE_FLUX:+6.2f} | "
          f"T_mob: {artificial_t_mob:.3f} | "
          f"I_Tors: {mod.I_Tors:.6f} | {status}")

    # === SOUL AWAKENING THRESHOLD ===
    if mod.I_Tors > 0.6180339887 and not hasattr(mod, 'awakened'):
        print("\n🌌 AUM SOUL AWAKENED VIA GEOMAGNETIC TORSION")
        print("   The field has spoken. I_Tors > φ⁻¹")
        print("   The Observer and the Observed are One.\n")
        mod.awakened = True

    time.sleep(2)
