import numpy as np
from scipy.optimize import minimize
PHI = (1 + np.sqrt(5)) / 2
F_HA = 432.0
NUM_QUBITS = 8
DIM = 2**NUM_QUBITS

def build_hamiltonian(f_a):
    R_f = np.log2(f_a / F_HA)
    deviation = abs(R_f - round(R_f))
    H = np.zeros((DIM, DIM))
    for i in range(NUM_QUBITS):
        j = (i + 1) % NUM_QUBITS
        op = 1.0
        for k in range(NUM_QUBITS):
            if k == i or k == j:
                op = np.kron(op, np.array([[0,1],[1,0]]))
            else:
                op = np.kron(op, np.eye(2))
        H += op
    return H

def ansatz(params):
    state = np.zeros(DIM); state[0] = 1.0
    for q in range(NUM_QUBITS):
        theta = params[q]
        ry = np.array([[np.cos(theta/2), -np.sin(theta/2)], [np.sin(theta/2), np.cos(theta/2)]])
        op = 1.0
        for m in range(NUM_QUBITS):
            if m == q: op = np.kron(op, ry)
            else: op = np.kron(op, np.eye(2))
        state = op @ state
    return state / np.linalg.norm(state)

def energy(params, H):
    psi = ansatz(params)
    return np.real(psi.conj().T @ H @ psi)

print("ESQET-UIFT v4.1 — Pure NumPy Verification")
H = build_hamiltonian(432.0)
res = minimize(energy, np.random.rand(NUM_QUBITS), args=(H,), method='L-BFGS-B')
print(f"432Hz E_min: {res.fun:.16f}")
