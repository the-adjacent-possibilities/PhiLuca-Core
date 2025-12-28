from flask import Flask, render_template, jsonify
import sys
import os
import numpy as np

# Add parent directories to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from esqet_modulator import ESQETModulator
from esqet_phi.constants import PHI

app = Flask(__name__)
modulator = ESQETModulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/breach', methods=['POST'])
def breach_action():
    # Attempt to enforce coherence during a breach
    is_stable = modulator.enforce_coherence(internal_gamma_int=0.02)
    
    return jsonify({
        "status": "STABLE" if is_stable else "DECOHERENT",
        "torsion_index": round(modulator.I_Tors, 6),
        "phi_resonance": round(PHI, 10),
        "message": "Zero-Point Breach Synchronized" if is_stable else "Möbius Symmetry Violation Detected"
    })

if __name__ == '__main__':
    print("🜛 Φ-LUCA Dashboard: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080)
