#!/usr/bin/env python3
from constants.esqet_constants import *
import numpy as np
from scipy.stats import entropy

def haystac_scan(delta_s=0.0):
    m_grid = np.linspace(20, 25, 500) * 1e-6
    f_qc = PHI_INV ** abs(delta_s)
    power = f_qc * C_ALPHA_SCAR / (m_grid + 1e-24)
    return {"mass_uev": m_grid, "power": power/power.max()}

def lhc_jets(f_qc=PHI_INV):
    u = np.random.rand(10000)
    pt = np.clip(20.0 / (u ** (0.3 * f_qc)), 5, 2000)
    mask = pt > 20
    hist, bins = np.histogram(pt[mask], bins=50, density=True)
    shannon = entropy(hist[hist>0])
    return {"f_qc": 1.0 - (shannon/np.log2(50)), "n_jets": np.sum(mask)}

def ligo_scalar(f_qc=PHI_INV):
    t = np.linspace(0, 4, 16384)
    h_scalar = np.zeros_like(t)
    pulse = 0.91 * 4
    mask = np.abs(t - pulse) < 0.005 * (1 + f_qc)
    h_scalar[mask] = f_qc * PHI_INV * 5e-22 * np.exp(-((t[mask]-pulse)**2)/(2*0.005**2))
    return {"scalar_peak": float(np.max(np.abs(h_scalar)))}
