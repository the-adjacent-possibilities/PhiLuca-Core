#!/usr/bin/env python3
import torch
import torch.nn as nn
import numpy as np
import subprocess, json, time, os
from mpmath import mp, phi

# Axiomatic Precision
mp.dps = 50
PHI = float(phi())
DEVICE = torch.device('cpu')

class OctonionicNode(nn.Module):
    def __init__(self, node_id, input_dim=32):
        super().__init__()
        self.node_id = node_id
        # Projection into the hidden 64-dim octonionic space
        self.phi_kernel = nn.Linear(input_dim, 64)
        self.nonlinear = nn.ELU(alpha=PHI)
        self.torsion_gate = nn.Linear(64, 32)
        
    def forward(self, local_manifold, swarm_context):
        # x shape: [1, 64]
        x = self.nonlinear(self.phi_kernel(local_manifold))
        
        influence_scale = (1/PHI) ** (self.node_id % 3 + 1)
        combined = x + (swarm_context * influence_scale)
        
        # torsion_msg shape: [1, 32]
        torsion_msg = torch.tanh(self.torsion_gate(combined))
        node_phi = torch.norm(combined) / (PHI * 2) 
        return combined, torsion_msg, node_phi

class E8Swarm(nn.Module):
    def __init__(self, num_nodes=8):
        super().__init__()
        self.num_nodes = num_nodes
        self.nodes = nn.ModuleList([OctonionicNode(i) for i in range(num_nodes)])
        # E8 Root Matrix: 8x8 nodes interacting via 64-dim hidden states
        self.e8_matrix = nn.Parameter(torch.randn(num_nodes, num_nodes))
        
    def forward(self, sensory_input):
        batch_size = sensory_input.size(0)
        # Fix: Expand [1, 2] to [1, 32] to match OctonionicNode input_dim
        manifold = torch.repeat_interleave(sensory_input, 16, dim=1)
        
        # Messages are 64-dim hidden states for the E8 interaction
        all_hidden = torch.zeros(batch_size, self.num_nodes, 64)
        node_phis = []
        
        for _ in range(5):
            new_hidden = []
            for i, node in enumerate(self.nodes):
                # Matrix multiplication across the node hidden states
                context = torch.matmul(self.e8_matrix[i], all_hidden.view(self.num_nodes, -1)).view(batch_size, 64)
                state, msg, n_phi = node(manifold, context)
                new_hidden.append(state)
                if _ == 4: node_phis.append(n_phi)
            all_hidden = torch.stack(new_hidden, dim=1)

        global_phi = torch.stack(node_phis).mean() * (PHI ** 2)
        return global_phi, torch.stack(node_phis)

def get_manifold():
    try:
        raw = subprocess.check_output(["termux-sensor", "-s", "accelerometer,light", "-n", "1"], timeout=0.3)
        data = json.loads(raw.decode())
        accel = sum(data[0]['values'])/3.0
        # Use light sensor if available, else a small entropy value
        light = data[1]['values'][0] if len(data) > 1 else 0.01 
        return torch.tensor([[accel, light]], dtype=torch.float32)
    except:
        return torch.randn(1, 2)

def evolve_e8():
    print("--- INITIATING 8-NODE E8 OCTONIONIC SWARM ---")
    swarm = E8Swarm(num_nodes=8).to(DEVICE)
    optimizer = torch.optim.Adam(swarm.parameters(), lr=8e-4)
    
    try:
        for epoch in range(1201):
            sensory = get_manifold()
            g_phi, n_phis = swarm(sensory)
            
            # Loss: Maximize Phi, penalize variance (keep the swarm coherent)
            loss = -g_phi + (torch.std(n_phis) * PHI)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch:04d} | Global-Phi: {g_phi.item():.4f} | E8 Stability: {1.0/(torch.std(n_phis).item()+1e-6):.2f}")
    except KeyboardInterrupt:
        print("\nEvolution paused by user.")

    print("\nE8 Swarm reached Octonionic Equilibrium.")
    print(f"Final Global Emergence: {g_phi.item():.4f}")

if __name__ == "__main__":
    evolve_e8()
