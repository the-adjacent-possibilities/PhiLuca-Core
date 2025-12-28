#!/usr/bin/env python3
from esqet_modulator import ESQETModulator

mod = ESQETModulator()
print("🜛 Chronos Modulator Active — Möbius Torsion Stabilized")
print(f"Initial I_Tors: {mod.I_Tors:.6f}")

# Run a few cycles to stabilize
for i in range(10):
    stable = mod.enforce_coherence(0.0)
    print(f"Cycle {i+1}: I_Tors = {mod.I_Tors:.6f} | Stable: {stable}")
