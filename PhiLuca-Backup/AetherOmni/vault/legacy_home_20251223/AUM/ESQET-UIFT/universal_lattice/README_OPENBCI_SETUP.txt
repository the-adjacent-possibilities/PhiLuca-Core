=== OPENBCI INTEGRATION SETUP ===

1. Install BrainFlow (primary library):
   pip install brainflow

2. Platform requirements:
   - Linux/PC strongly recommended (USB dongle for Cyton, BLED112 for Ganglion)
   - Android/Termux: limited/no direct OpenBCI support → Muse fallback used

3. For Ganglion BLE:
   - Requires BLED112 USB dongle
   - On Linux: ensure bluepy installed if fallback needed

4. Run:
   python kernel.py

When OpenBCI detected, system automatically prefers it over Muse.
Global Φ now reflects true multi-channel integrated information.

The open-source lattice embraces the highest-resolution human coherence.
