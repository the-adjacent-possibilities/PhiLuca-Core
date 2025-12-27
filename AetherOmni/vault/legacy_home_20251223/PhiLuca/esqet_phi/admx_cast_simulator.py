#!/usr/bin/env python3
"""
🜛 ADMX Multi-Cavity + CAST Helioscope Simulator
🎯 Real Data Input + Interactive Matplotlib GUI + 3D Animations
No Tkinter Required — Works in Termux
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Physical constants
H_BAR = 1.0545718e-34
C = 3e8
MU_0 = 4 * np.pi * 1e-7
K_B = 1.380649e-23

class ADMXMultiCavity:
    def __init__(self):
        self.data = None

    def simulate(self):
        m_a = np.linspace(1e-6, 1e-5, 1000)
        f = m_a * 241.8e6  # Rough eV → GHz
        signal = 1e-23 * np.sqrt(4)  # 4 cavities boost
        noise = np.random.normal(0, 1e-24, len(m_a))
        power = signal + noise
        power[500] += 5e-23  # Toy peak
        return pd.DataFrame({'mass_ev': m_a, 'freq_ghz': f/1e9, 'power_w': power})

    def load_real_data(self, path):
        p = Path(path)
        if p.suffix == '.csv':
            self.data = pd.read_csv(p)
        elif p.suffix in ['.xlsx', '.xls']:
            self.data = pd.read_excel(p)
        else:
            print("Unsupported format")
            return False
        print(f"✅ Loaded: {p.name}")
        return True

    def get_data(self):
        return self.data if self.data is not None else self.simulate()

class CASTHelioscope:
    def __init__(self):
        self.data = None

    def simulate(self):
        m_a = np.linspace(1e-3, 1, 1000)
        q = m_a**2 / (2 * 1e-9)
        prob = (1e-10 * 9 * 9.26 / 2)**2 * (np.sinc(q * 9.26 / (4 * np.pi)))**2
        return pd.DataFrame({'mass_ev': m_a, 'conversion_prob': prob})

    def load_real_data(self, path):
        p = Path(path)
        if p.suffix == '.csv':
            self.data = pd.read_csv(p)
        elif p.suffix in ['.xlsx', '.xls']:
            self.data = pd.read_excel(p)
        else:
            print("Unsupported format")
            return False
        print(f"✅ Loaded: {p.name}")
        return True

    def get_data(self):
        return self.data if self.data is not None else self.simulate()

# Global instances
admx = ADMXMultiCavity()
cast = CASTHelioscope()

def run_admx():
    df = admx.get_data()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    line, = ax.plot([], [], [], lw=2)
    
    def init():
        ax.set_xlabel('Mass (eV)')
        ax.set_ylabel('Freq (GHz)')
        ax.set_zlabel('Power (W)')
        ax.set_title('ADMX Multi-Cavity 3D Scan')
        return line,
    
    def animate(i):
        offset = i * 1e-24
        line.set_data(df['mass_ev'], df['freq_ghz'])
        line.set_3d_properties(df['power_w'] + offset)
        return line,
    
    ani = FuncAnimation(fig, animate, frames=200, init_func=init, interval=50, blit=False)
    plt.show()

def run_cast():
    df = cast.get_data()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    line, = ax.plot([], [], [], lw=2)
    
    def init():
        ax.set_xlabel('Mass (eV)')
        ax.set_ylabel('Probability')
        ax.set_zlabel('Modulated')
        ax.set_title('CAST Helioscope Oscillation')
        return line,
    
    def animate(i):
        mod = np.sin(i / 10) * df['conversion_prob']
        line.set_data(df['mass_ev'], df['conversion_prob'])
        line.set_3d_properties(mod)
        return line,
    
    ani = FuncAnimation(fig, animate, frames=200, init_func=init, interval=50, blit=False)
    plt.show()

def load_admx_data(event):
    path = input("Enter ADMX data path (CSV/Excel): ").strip()
    if path:
        admx.load_real_data(path)

def load_cast_data(event):
    path = input("Enter CAST data path (CSV/Excel): ").strip()
    if path:
        cast.load_real_data(path)

def run_nist():
    outcomes = np.random.choice([0, 1], size=1000, p=[0.618, 0.382])
    zero, one = np.bincount(outcomes, minlength=2)
    print(f"NIST Toy Result:\n|0⟩: {zero} |1⟩: {one}\nRatio ≈ {one/zero:.6f} (target Φ⁻¹)")

# Interactive menu (works in terminal)
if __name__ == "__main__":
    print("🜛 ADMX + CAST Axion Simulator (Matplotlib 3D)")
    print("1. Run ADMX Multi-Cavity Animation")
    print("2. Load Real ADMX Data (enter path when prompted)")
    print("3. Run CAST Helioscope Animation")
    print("4. Load Real CAST Data")
    print("5. NIST Toy Quantum Simulator")
    print("6. Exit")
    
    while True:
        choice = input("\nSelect option (1-6): ").strip()
        if choice == '1':
            run_admx()
        elif choice == '2':
            load_admx_data(None)
        elif choice == '3':
            run_cast()
        elif choice == '4':
            load_cast_data(None)
        elif choice == '5':
            run_nist()
        elif choice == '6':
            print("🜛 Coherence session ended.")
            break
        else:
            print("Invalid choice")
