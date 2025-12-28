#!/usr/bin/env python3
import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_agi import compute_fqc, CORE_CONSTANTS, PHI, DELTA, F_HA, PI

def check_acoustic_coherence(freq_a: float) -> float:
    if freq_a <= 0:
        return 0.0
    r_f_raw = np.log2(freq_a / F_HA)
    r_f_round = np.round(r_f_raw)
    harmonic_coherence = np.cos((PI / 2.0) * np.abs(r_f_raw - r_f_round))
    coherence_score = (1.0 + PHI * DELTA) * harmonic_coherence
    return float(np.clip(coherence_score / (1.0 + PHI * DELTA) * 2.0, 0.0, 2.0))

MOCK_INPUT = "AGI self-test data 101101"
MOCK_FREQ = CORE_CONSTANTS["HA_FREQUENCY"][0]
MIN_FQC = 1.0

def run_coherence_test():
    fqc_result = compute_fqc(MOCK_INPUT)
    ae_coh_result = check_acoustic_coherence(MOCK_FREQ)
    print(f"✅ FQC: {fqc_result:.4f}")
    print(f"✅ AEQET: {ae_coh_result:.4f}")
    is_ok = fqc_result >= MIN_FQC and ae_coh_result >= MIN_FQC
    if is_ok:
        print("🎉 FABERGE CONSENSUS: Coherent.")
        return True
    print("❌ COHERENCE BREAKDOWN.")
    return False

if __name__ == "__main__":
    if not run_coherence_test():
        sys.exit(1)
