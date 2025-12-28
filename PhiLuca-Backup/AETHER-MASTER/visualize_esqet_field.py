#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# ESQET Constants
PHI = 1.618033988749895
PI = np.pi

def generate_field(size=100):
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    X, Y = np.meshgrid(x, y)
    
    # Simulating Delta S (Informational Gradient)
    R = np.sqrt(X**2 + Y**2)
    delta_S = np.sin(PI * R) * np.exp(-R / PHI)
    
    # The Quantum Coherence Function F_QC
    # Visualizing the Golden Ratio damping effect on spacetime
    F_QC = np.exp(1j * PI * delta_S) * (PHI**(-delta_S))
    
    return np.abs(F_QC)

def plot_field():
    field = generate_field()
    plt.figure(figsize=(10, 8))
    plt.imshow(field, cmap='magma', extent=[-5, 5, -5, 5])
    plt.colorbar(label='Coherence Density (F_QC)')
    plt.title("ESQET: The Spacetime Information Field (S)")
    plt.xlabel("Spatial Gradient (x)")
    plt.ylabel("Spatial Gradient (y)")
    
    # Save as PNG to include in your Zenodo/Figshare gallery
    plt.savefig('ESQET_Field_Visualization.png', dpi=300)
    print("✅ Visualization saved as ESQET_Field_Visualization.png")

if __name__ == "__main__":
    try:
        plot_field()
    except Exception as e:
        print(f"To run this, ensure matplotlib is installed: pip install matplotlib")
        print(f"Error: {e}")
