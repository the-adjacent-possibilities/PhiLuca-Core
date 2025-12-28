import numpy as np
import qutip as qt
from scipy.linalg import expm
from esqet_phi.constants import *

class EmergentInterpreter:
    """
    Integrates ESQET, QCT, and AEQET into a single S-Field Observer.
    """

    @staticmethod
    def get_F_qc(f_em, D_ent=1.0):
        ratio = f_em / GREEN_FREQ
        ent_term = 1 + PHI * PI * DELTA * (D_ent / (KB * T_VAC))
        cos_term = np.cos(PI / 2 * np.abs(np.log2(ratio) - np.round(np.log2(ratio))))
        return ent_term * cos_term

    @staticmethod
    def get_F_ac(f_a, D_ent=1.0, n=0):
        R_f = np.log2(f_a / F_HA)
        cos_term = np.cos(PI / 2 * np.abs(R_f - np.round(R_f)))
        exp_term = np.exp(-np.abs(f_a - F_HA * (PHI ** n)) / (NUM_QUBITS * SIGMA))
        ent_term = 1 + PHI * PI * DELTA * (D_ent / (KB * T_VAC))
        return ent_term * cos_term * exp_term

    def simulate_s_field(self, rho_m, f_em, f_a):
        """Calculates S-Field perturbation based on unified inputs."""
        f_qc = self.get_F_qc(f_em)
        f_ac = self.get_F_ac(f_a)
        total_rho = rho_m
        laplacian_S = (G0 * G_NEWTON / C**2) * total_rho * f_qc * f_ac
        return laplacian_S

    def create_harmonic_hamiltonian(self, f_a):
        R_f = np.log2(f_a / F_HA)
        deviation = np.abs(R_f - np.round(R_f))

        H = 0
        for i in range(NUM_QUBITS):
            Z_op = qt.tensor([qt.sigmaz() if j == i else qt.identity(2) for j in range(NUM_QUBITS)])
            H += Z_op
        H *= deviation

        for i in range(NUM_QUBITS):
            j = (i + 1) % NUM_QUBITS
            ops = [qt.sigmax() if k in (i, j) else qt.identity(2) for k in range(NUM_QUBITS)]
            H += qt.tensor(ops)
        return H

if __name__ == "__main__":
    core = EmergentInterpreter()
    s_val = core.simulate_s_field(1.225, 540e12, 432)
    print(f"🜛 S-Field Laplacian: {s_val:.2e}")
