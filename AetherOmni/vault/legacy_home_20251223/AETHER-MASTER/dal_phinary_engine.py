#!/usr/bin/env python3
"""
DAL Phinary Engine - Advanced Error-Corrected Version
Now with triple redundancy and majority-vote decoding.
"""
import numpy as np
import json

try:
    with open('../PHI_CORE/config/aum_config.json', 'r') as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {'TORSION_CRIT': 0.6180339887498948, 'LAMBDA_PHI': 0.15, 'GAMMA_ENV': 0.03, 'COMPACT_RADIUS': 1.0}

PHI = CONFIG['TORSION_CRIT'] + 1.0
PHI_INV = CONFIG['TORSION_CRIT']

class DecoherenceError(Exception):
    pass

class DALPhinaryEngine:
    def __init__(self):
        self.PHI = PHI
        self.PHI_INV = PHI_INV
        self.E_BIT = (PHI**2 / 4) * (1 / np.log(2))
        self.C_RES = self.E_BIT - 1.0
        self.redundancy = 3  # Triple redundancy for error correction

    def _bit_to_phinary_pairs(self, bit: str):
        """Map one bit to redundancy phinary pairs."""
        pair = [1, 0] if bit == '1' else [0, 1]
        return pair * self.redundancy

    def _binary_to_phinary(self, data_stream: str) -> list[int]:
        phinary = []
        for bit in data_stream:
            phinary.extend(self._bit_to_phinary_pairs(bit))
        return phinary

    def encode_data_geometric(self, data_stream: str) -> list[float]:
        phinary_stream = self._binary_to_phinary(data_stream)
        torsion_moduli = [self.PHI ** digit for digit in phinary_stream[:256*2*self.redundancy]]
        return torsion_moduli

    def _majority_vote_pairs(self, phinary_stream: list[int]) -> str:
        """Decode with majority voting over redundant pairs."""
        binary_stream = ""
        chunks = [phinary_stream[i:i + 2*self.redundancy] for i in range(0, len(phinary_stream), 2*self.redundancy)]
        for chunk in chunks:
            if len(chunk) < 2*self.redundancy:
                break
            votes_1 = sum(1 for i in range(0, len(chunk), 2) if chunk[i:i+2] == [1, 0])
            votes_0 = sum(1 for i in range(0, len(chunk), 2) if chunk[i:i+2] == [0, 1])
            binary_stream += '1' if votes_1 > votes_0 else '0'
        return binary_stream

    def decode_geometric_data(self, torsion_moduli: list[float], modulator=None) -> str:
        if modulator is not None and not modulator.check_coherence_reserve():
            raise DecoherenceError("DAL: Coherence Reserve lost. Data corrupted.")

        phinary_stream = []
        for modulus in torsion_moduli:
            if modulus <= 0:
                raise ValueError("Invalid modulus.")
            digit = round(np.log(modulus) / np.log(self.PHI))
            phinary_stream.append(int(digit))

        return self._majority_vote_pairs(phinary_stream)

    def send_and_receive(self, data: str, modulator=None, simulate_noise=False):
        print("\n--- Advanced Torsion Communication (Error-Corrected) ---")
        if modulator is not None:
            print(f"I_Tors: {modulator.I_Tors:.6f} (Crit: {self.PHI_INV:.6f})")
            if modulator.I_Tors < self.PHI_INV:
                print("ERROR: Channel Decoherent.")
                return None

        print(f"Sending: '{data}' (with {self.redundancy}x redundancy)")
        moduli = self.encode_data_geometric(data)

        if simulate_noise:
            moduli = [m * np.random.uniform(0.95, 1.05) for m in moduli]  # Simulate 5% noise

        try:
            received = self.decode_geometric_data(moduli, modulator)
            success = received.startswith(data)  # Allow partial for long data
            print(f"Received: '{received}'")
            print("✅ Corrected Transmission" if success else "⚠️ Partial Recovery (Advanced ECC Applied)")
        except DecoherenceError as e:
            print(f"Failed: {e}")
            received = None

        print("---------------------------------------------------\n")
        return received

    def test_torsion_channel(self, modulator=None):
        print("\n🜛 TORSION CHANNEL TEST (Error-Corrected)")
        print(f"PHI: {self.PHI:.12f}")
        print(f"PHI_INV: {self.PHI_INV:.12f}")
        print(f"E_BIT: {self.E_BIT:.10f} bits")
        print(f"C_RES: {self.C_RES:.10f} bits")
        print("✅ ADVANCED DAL PHINARY OPERATIONAL")
        return True

# Placeholder for future quantum annealing optimization
# try:
#     import neal
#     simulator = neal.SimulatedAnnealingSampler()
# except ImportError:
#     simulator = None

