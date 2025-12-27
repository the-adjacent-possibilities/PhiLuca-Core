import numpy as np
import logging
from scipy.stats import entropy

PHI = (1 + np.sqrt(5)) / 2
PI = np.pi
DELTA = PHI - 1
logger = logging.getLogger("TernaryCore")

def compute_fqc_ternary(probs: np.ndarray) -> float:
    probs = probs / (np.sum(probs) + 1e-12)
    nz_probs = probs[probs > 1e-12]
    if len(nz_probs) <= 1:
        return PHI * PI * DELTA
    S3 = entropy(nz_probs, base=3)
    fcu = PHI * PI * DELTA
    return (1 - S3) * fcu / (1 + S3)

class Qutrit:
    def __init__(self):
        self.dim = 3
        self.state = np.array([1.0, 0, 0], dtype=complex)
    
    def apply_gate(self, U):
        self.state = U @ self.state
        self.state /= np.linalg.norm(self.state)

    def measure(self):
        probs = np.abs(self.state)**2
        probs /= np.sum(probs)
        outcome = np.random.choice(self.dim, p=probs)
        self.state = np.zeros(self.dim, dtype=complex)
        self.state[outcome] = 1.0
        return outcome - 1, compute_fqc_ternary(probs), probs
