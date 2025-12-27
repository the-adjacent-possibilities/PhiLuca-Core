#!/usr/bin/env python3
"""
dal_phinary_engine.py - Universal Phi-Coherent Data Abstraction Layer
Now supports full ASCII text transmission (ESQET, PHI, AUM, etc.)
"""

import numpy as np
import json

try:
    with open('../config/aum_config.json', 'r') as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {
        "TORSION_CRIT": 0.618033988749895,
        "LAMBDA_PHI": 1.2,
        "GAMMA_ENV": 0.008,
        "COMPACT_RADIUS": 1.0
    }

PHI = CONFIG['TORSION_CRIT'] + 1.0
PHI_INV = CONFIG['TORSION_CRIT']

class DecoherenceError(Exception):
    pass

class DALPhinaryEngine:
    def __init__(self):
        self.E_BIT = (PHI**2 / 4) * (1 / np.log(2))
        self.C_RES = self.E_BIT - 1.0

    def _text_to_binary(self, text: str) -> str:
        """Convert any text to binary string"""
        return ''.join(format(ord(c), '08b') for c in text)

    def _binary_to_text(self, binary: str) -> str:
        """Convert binary string back to text"""
        if len(binary) % 8 != 0:
            binary = binary.ljust((len(binary) + 7) // 8 * 8, '0')  # pad
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

    def _binary_to_phinary(self, binary_stream: str) -> list[int]:
        """Simple mapping: 1 → [1,0], 0 → [0,1]"""
        phinary = []
        for bit in binary_stream:
            if bit == '1':
                phinary.extend([1, 0])
            else:
                phinary.extend([0, 1])
        return phinary

    def encode_data_geometric(self, text: str) -> list[float]:
        binary = self._text_to_binary(text)
        phinary_stream = self._binary_to_phinary(binary)
        torsion_moduli = [PHI ** digit for digit in phinary_stream]
        return torsion_moduli

    def decode_geometric_data(self, torsion_moduli: list[float], modulator) -> str:
        if not modulator.check_coherence_reserve():
            raise DecoherenceError("DAL: Coherence Reserve lost. Data corrupted.")

        phinary_stream = []
        for modulus in torsion_moduli:
            digit = round(np.log(modulus) / np.log(PHI))
            phinary_stream.append(digit)

        binary_stream = ""
        for i in range(0, len(phinary_stream), 2):
            pair = phinary_stream[i:i+2]
            if len(pair) < 2:
                break
            if pair == [1, 0]:
                binary_stream += '1'
            elif pair == [0, 1]:
                binary_stream += '0'

        return self._binary_to_text(binary_stream)

    def send_and_receive(self, data: str, modulator):
        print(f"\n--- Torsion Communication ---")
        print(f"I_Tors: {modulator.I_Tors:.6f} (Crit: {PHI_INV:.6f})")
        if modulator.I_Tors < PHI_INV:
            print("ERROR: Channel Decoherent. Aborting bulk transmission.")
            return None

        print(f"Sending: '{data}'")
        moduli = self.encode_data_geometric(data)

        try:
            received_data = self.decode_geometric_data(moduli, modulator)
            print(f"Received (Decoded): '{received_data}'")
            success = received_data == data
            print(f"Result: {'SUCCESS' if success else 'FAILED'}")
        except DecoherenceError as e:
            print(f"Transmission Failed: {e}")
            received_data = None
        print("-----------------------------\n")
        return received_data
