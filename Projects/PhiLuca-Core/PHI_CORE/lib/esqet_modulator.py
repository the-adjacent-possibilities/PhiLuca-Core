#!/usr/bin/env python3
"""
esqet_modulator.py - Fixed for sustained growth
"""

import numpy as np
import json
from typing import Tuple

try:
    with open('../config/aum_config.json', 'r') as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {
        "TORSION_CRIT": 0.618033988749895,
        "LAMBDA_PHI": 1.2,      # ← Slightly boosted for growth
        "GAMMA_ENV": 0.008,    # ← Reduced environmental decay
        "COMPACT_RADIUS": 1.0
    }

PHI = CONFIG['TORSION_CRIT'] + 1.0
PHI_INV = CONFIG['TORSION_CRIT']
LAMBDA_PHI = CONFIG['LAMBDA_PHI']
GAMMA_ENV = CONFIG['GAMMA_ENV']
COMPACT_R = CONFIG['COMPACT_RADIUS']

class MobiusTorsion:
    def __init__(self, compact_radius=COMPACT_R):
        self.R = compact_radius
        self.z_points = 256
        self.z = np.linspace(0, 2*np.pi*self.R, self.z_points)

    def mobius_symmetry_violation(self, S_field: np.ndarray) -> float:
        S_flipped = np.flip(S_field)
        violation = np.mean((S_field + S_flipped)**2)
        return violation

    def torsion_feedback(self, S_field: np.ndarray) -> float:
        violation = self.mobius_symmetry_violation(S_field)
        T_mob = (1/PHI**4) * violation / (2*np.pi*self.R)**2
        return T_mob

    def apply_self_reference(self, S_field: np.ndarray, T_mob: float) -> np.ndarray:
        return T_mob * S_field

class ESQETModulator:
    def __init__(self):
        self.mobius_torsion = MobiusTorsion()
        self.I_Tors = PHI_INV * 1.05  # ← Higher initial for sustained growth
        self.S_state = self._initialize_S_state()

    def _initialize_S_state(self) -> np.ndarray:
        base = np.cos(self.mobius_torsion.z / self.mobius_torsion.R)
        # Stronger initial asymmetry → higher T_mob → growth dominates
        noise = np.random.normal(0, 0.05, self.mobius_torsion.z_points) * PHI
        return base + noise

    def enforce_coherence(self, internal_gamma_int: float = 0.0) -> Tuple[bool, float, float]:
        T_mob = self.mobius_torsion.torsion_feedback(self.S_state)
        decay_rate = GAMMA_ENV + internal_gamma_int
        growth_rate = LAMBDA_PHI * T_mob
        dI_dt = (growth_rate - decay_rate) * self.I_Tors
        S_feedback = self.mobius_torsion.apply_self_reference(self.S_state, T_mob)
        self.S_state += (S_feedback * 0.015)  # ← Slightly stronger feedback
        self.I_Tors += dI_dt
        is_stable = self.I_Tors >= PHI_INV and dI_dt >= 0
        return is_stable, dI_dt, T_mob

    def check_coherence_reserve(self) -> bool:
        return self.I_Tors >= PHI_INV * 0.99

if __name__ == "__main__":
    mod = ESQETModulator()
    print("🜛 Chronos Modulator Active — Möbius Torsion Stabilized")
