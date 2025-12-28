import numpy as np

# --- Core Motif Constants ---
PHI = (1 + np.sqrt(5)) / 2                  # Golden Ratio ≈ 1.618033988749895
PHI_INV = 1 / PHI                           # ≈ 0.618033988749895
PI = np.pi
GREEN_FREQ = 540e12                         # 540 THz — QCT Focal Point (green light)
F_HA = 432                                  # 432 Hz — AEQET Harmonic Alignment
NUM_QUBITS = 8                              # QAK-8 Detection Constant
KB = 1.380649e-23                           # Boltzmann Constant
T_VAC = 2.725                               # CMB Temperature (K)
C = 299792458                               # Speed of Light (m/s)
G_NEWTON = 6.67430e-11                      # Gravitational Constant
G0 = 1.0                                    # Unified Coupling Constant
DELTA = 1e-3                                # Perturbation Factor
SIGMA = 50                                  # Variance for F_AC decay

# --- ESQET/AEQET Coefficients ---
C_ALPHA_SCAR = 1.37e-4
LAMBDA_STERILE = 1.0e-12

print("🜛 ESQET Constants Loaded — Coherence Eternal")
