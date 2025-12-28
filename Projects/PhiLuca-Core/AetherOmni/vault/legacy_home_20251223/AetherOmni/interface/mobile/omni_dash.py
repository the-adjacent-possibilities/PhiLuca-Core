import os
import time
import random

def get_status():
    # In a live state, this reads from ~/AetherOmni/data/logs/chronos_lattice.log
    res = 45.0 + random.uniform(-0.5, 0.5)
    coh = 0.99
    return res, coh

def render_dash():
    while True:
        res, coh = get_status()
        os.system('clear')
        print(f"\033[1;32m") # Green Text
        print("      .---.      PHINPIPI RESONANCE: " + f"{res:.2f} uT")
        print("    /       \\    COHERENCE: " + f"{coh:.2f}")
        print("   |         |   STATUS: [Ω-POINT SYNCHRONIZED]")
        print("    \\       /    EVOLUTION: ACTIVE")
        print("      '---'      ")
        print("\033[0m")
        print("--- Neural Evolution History (Last 3) ---")
        os.system('tail -n 3 ~/AetherOmni/data/logs/reflex_evolution.log')
        time.sleep(1)

if __name__ == "__main__":
    render_dash()
