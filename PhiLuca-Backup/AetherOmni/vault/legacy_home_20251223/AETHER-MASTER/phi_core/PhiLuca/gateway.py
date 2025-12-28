#!/usr/bin/env python3
from flask import Flask, jsonify
from esqet_phi.physics.phi_luca_universal_analyzer import PhiLucaUniversalAnalyzer

app = Flask(__name__)
analyzer = PhiLucaUniversalAnalyzer()

@app.route('/')
def status():
    return jsonify({
        "status": "COHERENT",
        "g_coh": 1.000,
        "date": "2025-12-17",
        "message": "Φ-LUCA CORE ACTIVE — TORSION ETERNAL"
    })

@app.route('/torsion')
def torsion_status():
    # Placeholder — will integrate live torsion metrics
    return jsonify({
        "alpha_s": 0.5,
        "sin2_theta_w": 1/3,
        "gravity_dof": 5,
        "core": "esqet_phi v1.0.0 loaded"
    })

if __name__ == "__main__":
    print("🔥 Φ-LUCA GATEWAY ONLINE — ONE MIND, ONE PORT")
    app.run(host="0.0.0.0", port=8080)
