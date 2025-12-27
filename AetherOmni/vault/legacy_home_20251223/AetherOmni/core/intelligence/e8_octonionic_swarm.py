#!/usr/bin/env python3
import torch
import torch.nn as nn
import subprocess, json, gc
from mpmath import mp, phi

# Axiomatic Precision
mp.dps = 20
PHI = float(phi())
DEVICE = torch.device('cpu')

class OctonionicNode(nn.Module):
    def __init__(self, node_id, input_dim=32):
        super().__init__()
        self.node_id = node_id
        # Reduced to 48 to prevent Signal 9 / OOM
        self.phi_kernel = nn.Linear(input_dim, 48)
        self.nonlinear = nn.ELU(alpha=PHI)
        self.torsion_gate = nn.Linear(48, 32)
        
    def forward(self, local_manifold, swarm_context):
        x = self.nonlinear(self.phi_kernel(local_manifold))
        influence_scale = (1/PHI) ** (self.node_id % 3 + 1)
        combined = x + (swarm_context * influence_scale)
        torsion_msg = torch.tanh(self.torsion_gate(combined))
        node_phi = torch.norm(combined) / (PHI * 2) 
        return combined, torsion_msg, node_phi

class E8Swarm(nn.Module):
    def __init__(self, num_nodes=8):
        super().__init__()
        self.num_nodes = num_nodes
        self.nodes = nn.ModuleList([OctonionicNode(i) for i in range(num_nodes)])
        self.e8_matrix = nn.Parameter(torch.randn(num_nodes, num_nodes))
        
    def forward(self, sensory_input):
        batch_size = sensory_input.size(0)
        manifold = torch.repeat_interleave(sensory_input, 16, dim=1)
        
        # Initialize hidden state with small entropy
        all_hidden = torch.randn(batch_size, self.num_nodes, 48) * 0.01
        node_phis = []
        
        for cycle in range(5):
            new_hidden = []
            for i, node in enumerate(self.nodes):
                # Matmul for node interaction
                context = torch.matmul(self.e8_matrix[i], all_hidden.view(self.num_nodes, -1)).view(batch_size, 48)
                state, msg, n_phi = node(manifold, context)
                
                # Detach early cycles to save memory, only keep the final gradient
                if cycle < 4:
                    state = state.detach()
                    
                new_hidden.append(state)
                if cycle == 4: node_phis.append(n_phi)
            all_hidden = torch.stack(new_hidden, dim=1)

        global_phi = torch.stack(node_phis).mean() * (PHI ** 2)
        return global_phi, torch.stack(node_phis)

def get_manifold():
    try:
        raw = subprocess.check_output(["termux-sensor", "-s", "accelerometer", "-n", "1"], timeout=0.2)
        data = json.loads(raw.decode())
        accel = sum(data[0]['values'])/3.0
        return torch.tensor([[accel, 0.5]], dtype=torch.float32)
    except:
        return torch.randn(1, 2)

def evolve_e8():
    print("--- INITIATING LEAN E8 OCTONIONIC SWARM ---")
    swarm = E8Swarm(num_nodes=8).to(DEVICE)
    optimizer = torch.optim.Adam(swarm.parameters(), lr=1e-3)
    
    try:
        for epoch in range(1201):
            sensory = get_manifold()
            g_phi, n_phis = swarm(sensory)
            
            loss = -g_phi + (torch.std(n_phis) * PHI)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch:04d} | Global-Phi: {g_phi.item():.4f} | Stability: {1.0/(torch.std(n_phis).item()+1e-6):.2f}")
                gc.collect() # Force RAM release
    except KeyboardInterrupt:
        print("\nEvolution paused.")

if __name__ == "__main__":
    evolve_e8()
