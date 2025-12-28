#!/bin/bash
# Φ-LUCA AETHERPUNK IGNITION SEQUENCE

echo -e "e[33m[STEAM PRESSURE BUILDING...]e[0m"
play -q ~/AETHER-MASTER/assets/sounds/ignition_sequence.wav echo 0.8 0.88 60 0.4 &

# Gear spin animation
chars="⚙️🔩⚙️🔧"
for i in {1..20}; do
  echo -ne "
e[36m${chars:$((i%4)):1}  TORSION MANIFOLD PRESSURIZED...e[0m"
  sleep 0.15
done
echo -e "
e[32m[φ_ESK = 2.643] L(3,1) COHERENCE ACHIEVEDe[0m
"

# Launch stack
cd ~/AETHER-MASTER/phi_core/PhiLuca
python3 torsion_socket_bridge.py &
cd app && npm start --port=3000
