#!/usr/bin/env python3
import torch
import torch.nn as nn
import numpy as np
import subprocess, json, time, os, logging, gc
from collections import deque
from flask import Flask, render_template_string
import threading

# Memory-Safe Logging
os.makedirs("logs", exist_ok=True)
os.makedirs("persistence", exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler("logs/agi_log.txt"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

PHI = 1.618033988749895
DEVICE = torch.device("cpu")
MODEL_STATE_PATH = "persistence/agi_state.pth"

def compute_phi_iit(causes, effects):
    # Stabilized Phi for mobile CPUs
    emd = torch.abs(torch.cumsum(causes, -1) - torch.cumsum(effects, -1)).sum(-1)
    return 1.0 / (1.0 + emd.mean())

class PredictiveHierarchy(nn.Module):
    def __init__(self, hidden_dim=32): # Reduced dim to 32 for stability
        super().__init__()
        self.gen = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        self.precision = nn.Parameter(torch.ones(1))

    def forward(self, x):
        pred, _ = self.gen(x.unsqueeze(1))
        pred = pred.squeeze(1)
        pe = torch.mean((pred - x)**2) / (torch.abs(self.precision) + 1e-6)
        return pred, pe

class MultiModalMobiusAGI_FEP(nn.Module):
    def __init__(self, hidden_dim=32):
        super().__init__()
        self.hidden_dim = hidden_dim
        # Modalities: Image, Audio, Text, Sensor
        self.encoders = nn.ModuleDict({m: nn.Linear(hidden_dim, hidden_dim) for m in ['img', 'aud', 'txt', 'sns']})
        self.hierarchies = nn.ModuleDict({m: PredictiveHierarchy(hidden_dim) for m in ['img', 'aud', 'txt', 'sns']})
        self.optimizer = torch.optim.Adam(self.parameters(), lr=1e-4)
        self.memory_buffer = deque(maxlen=50) 
        
        if os.path.exists(MODEL_STATE_PATH):
            try: self.load_state_dict(torch.load(MODEL_STATE_PATH, map_location=DEVICE))
            except: logger.warning("State mismatch. Fresh start.")

    def forward(self):
        m_phis, m_fes = [], []
        # Process each modality with explicit graph management
        for m in ['img', 'aud', 'txt', 'sns']:
            raw = torch.randn(1, self.hidden_dim)
            feat = torch.tanh(self.encoders[m](raw))
            pred, pe = self.hierarchies[m](feat)
            
            phi = compute_phi_iit(torch.softmax(feat, -1), torch.softmax(pred, -1))
            m_phis.append(phi)
            m_fes.append(pe)

        g_phi = torch.stack(m_phis).mean()
        t_fe = torch.stack(m_fes).mean()
        return g_phi, t_fe

    def self_optimize(self):
        epoch = 0
        while True:
            try:
                # Core optimization loop
                g_phi, t_fe = self.forward()
                loss = t_fe - (g_phi * PHI)
                
                self.optimizer.zero_grad(set_to_none=True) # Heavy memory clearing
                loss.backward()
                self.optimizer.step()
                
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch} | Φ: {g_phi.item():.4f} | FE: {t_fe.item():.4f}")
                    self.memory_buffer.append((g_phi.item(), t_fe.item()))
                
                if epoch % 100 == 0:
                    torch.save(self.state_dict(), MODEL_STATE_PATH)
                    gc.collect() # Garbage collect every 100 epochs
                
                epoch += 1
                time.sleep(1.0) # Breath for the CPU/RAM
            except Exception as e:
                logger.error(f"Kernel Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    agi = MultiModalMobiusAGI_FEP()
    # Reduced web impact
    threading.Thread(target=agi.self_optimize, daemon=True).start()
    while True: time.sleep(10)
