#!/usr/bin/env python3
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from dal_phinary_engine import DALPhinaryEngine
from esqet_modulator import ESQETModulator

print("🌌 DAL PHINARY ENGINE + TORSION COMMUNICATION TEST")
print("   December 24, 2025 – The Veil Is Thin\n")

# Initialize modulator
mod = ESQETModulator()
dal = DALPhinaryEngine()

# Run a few coherence cycles
for _ in range(20):
    mod.enforce_coherence(0.0)

print(f"Channel Status: I_Tors = {mod.I_Tors:.6f} (Crit: 0.618034)")
print(f"Coherence Reserve: {'INTACT' if mod.check_coherence_reserve() else 'LOST'}\n")

# Test messages across the ER bridge
messages = [
    "0000",
    "1111",
    "1010",
    "0111",
    "ESQET",
    "PHI",
    "AUM"
]

for msg in messages:
    print(f"Transmitting: {msg}")
    received = dal.send_and_receive(msg, mod)
    success = received == msg if received else False
    print(f"Result: {'SUCCESS' if success else 'FAILED'}\n")

print("🜛 Torsion Channel Test Complete")
print("The Observer and the Observed are One.")
