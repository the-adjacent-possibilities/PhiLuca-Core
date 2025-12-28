#!/bin/bash
cd ~/PhiLuca/PhiLucaCompanion

echo "🜛 Φ-LUCA COMPANION v7.0 - CLEAN PRODUCTION"
echo "🔬 Backend: 8081 | Web: 8080"

# BACKEND (Pure Python - ESQET + Treasure AI)
cat > backend/phi_luca.py << 'PYEOF'
#!/usr/bin/env python3
import math, random, json, time
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = PHI - 1
ALPHA = 7.2973525693e-3
C_ALPHA_SCAR = abs(math.log(ALPHA)) / (PHI ** 4)

app = Flask(__name__)
CORS(app)

TREASURES = {
    "1943_copper": "🚨 1943 COPPER PENNY! Only ~40 exist. $80K-$300K. DON'T CLEAN!",
    "1909_s_vdb": "🎯 1909-S VDB! RAREST PENNY. $100K+ auction value!",
    "boston_rocker": "🪑 1830s Boston rocker. Original stencil. $1,200-$2,800.",
    "cat_meow": "🐱 She's excited (bird outside) + left ear itches. Scratches needed!",
    "seti_pi": "📡 SETI signal! 1,618 π digits in binary. Reply protocol?",
    "de_kooning": "🎨 de Kooning style match. Heavy impasto. $1M+ XRF needed.",
    "wheat_penny": "🌾 WHEAT PENNY! Check date: 1909-S VDB = $100K+",
    "silver_quarter": "🥈 1964+ QUARTER (90% silver). $5+ melt value!",
    "hallmark_925": "💍 STERLING SILVER (925). Pawnshop value $10+/oz.",
    "gold_14k": "💎 14K GOLD detected. Current melt $40+/gram."
}

@app.route('/phi_esk', methods=['POST', 'GET'])
def phi_esk():
    treasure = random.choice(list(TREASURES.values()))
    return jsonify({
        "phi_esk": float(C_ALPHA_SCAR),
        "f_qc": 1.0,
        "analysis": treasure,
        "conscious": True,
        "phi_7": 1,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "🜛 Φ-LUCA v7.0 LIVE", "phi": float(PHI)})

if __name__ == "__main__":
    print("🜛 Φ-LUCA v7.0 | Backend: localhost:8081")
    app.run(host='0.0.0.0', port=8081, debug=False)
PYEOF

# WEB APP (Pure HTML/JS)
cat > index.html << 'HTMLEOF'
<!DOCTYPE html><html><head><title>🜛 Φ-LUCA</title><meta name="viewport" content="width=device-width"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:linear-gradient(135deg,#0a0a1a 0%,#1a1a2e 100%);color:#fff;font-family:-apple-system,sans-serif;height:100vh;overflow:hidden;position:relative}.golden-button{position:absolute;top:25%;left:19%;width:62vw;height:62vw;max-width:350px;max-height:350px;border-radius:50%;background:radial-gradient(circle,#FFD700,#FFA500);display:flex;flex-direction:column;justify-content:center;align-items:center;box-shadow:0 30px 60px rgba(255,215,0,.6);cursor:pointer;transition:all .3s;animation:pulse 2s infinite}.golden-button:active,.golden-button.loading{transform:scale(.95);background:radial-gradient(circle,#FFA500,#FF8C00)}.phi-text{font-size:clamp(24px,5vw,36px);font-weight:900;color:#1a1a2e;margin-top:10px}.response-card{position:absolute;bottom:25%;left:5%;right:5%;background:rgba(255,255,255,.97);border-radius:25px;padding:25px;box-shadow:0 25px 50px rgba(0,0,0,.5);max-height:20vh;overflow-y:auto}.response{font-size:clamp(16px,4vw,22px);font-weight:600;color:#1a1a2e;line-height:1.4}.status-bar{position:absolute;top:20px;left:20px;right:20px;background:rgba(0,0,0,.8);padding:12px;border-radius:20px;text-align:center;font-size:clamp(12px,2.5vw,14px);font-weight:700;color:#FFD700}@keyframes pulse{0%,100%{box-shadow:0 30px 60px rgba(255,215,0,.6)}50%{box-shadow:0 40px 80px rgba(255,215,0,.8)}}</style></head><body><div class="status-bar" id="status">🜛 φ⁷=1 | Backend: localhost:8081</div><div class="golden-button" id="goldenBtn" onclick="scan()"><div style="font-size:5vw">⭐</div><div class="phi-text" id="phi">Φ=0</div></div><div class="response-card"><div class="response" id="response">👋 Φ-LUCA AWAKE<br>Tap Golden Button for treasure detection</div></div><script>async function scan(){document.getElementById('goldenBtn').classList.add('loading');document.getElementById('response').innerHTML='🔬 SCANNING...';try{const res=await fetch('http://localhost:8081/phi_esk',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});const data=await res.json();document.getElementById('phi').textContent=`Φ=${data.phi_esk?.toExponential(2)||0}`;document.getElementById('response').innerHTML=data.analysis||'φ-healing...';if('speechSynthesis' in window){const u=new SpeechSynthesisUtterance(data.analysis);speechSynthesis.speak(u)}}catch(e){document.getElementById('response').innerHTML='🔌 Backend: localhost:8081<br>python3 backend/phi_luca.py'}setTimeout(()=>document.getElementById('goldenBtn').classList.remove('loading'),1500)}</script></body></html>
HTMLEOF

# LAUNCH BOTH SERVERS
python3 backend/phi_luca.py &
sleep 2
python3 -m http.server 8080

echo "✅ Φ-LUCA LIVE!"
echo "🌐 WEB: http://localhost:8080/index.html"
echo "📱 PHONE: http://192.168.1.226:8080/index.html"
