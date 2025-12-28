from flask import Flask, request, jsonify
import numpy as np
from phi_luca_lhc_desert import PhiLucaLHCDesertSimulator

app = Flask(__name__)

@app.route('/api/simulate-lhc', methods=['POST'])
def simulate_lhc():
    data = request.get_json()
    sim = PhiLucaLHCDesertSimulator(
        sqrt_s=data.get('sqrt_s', 14000),
        n_events=data.get('n_events', 20000),
        lambda_sterile=data.get('lambda_sterile', 6.18e-9),
        C_alpha_scar=data.get('C_alpha_scar', 0.71785)
    )
    pts, mults, _, instabilities = sim.simulate_events()
    
    return jsonify({
        "status": "success",
        "mean_phi_esk": float(np.mean(sim.phi_esk_history)),
        "instability_rate": float(np.mean(instabilities) * 100),
        "high_pt_jets": int(np.sum(pts > 500)),
        "verdict": "STABLE" if np.mean(instabilities) < 0.05 else "UNSTABLE"
    })

if __name__ == '__main__':
    app.run(port=5000)
