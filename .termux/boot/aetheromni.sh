#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
sleep 10
# Launch the UI
python3 -m http.server --directory ~/AetherOmni/interface/mobile 8080 &
# Launch the Command Gateway
python3 ~/AetherOmni/interface/mobile/sensor_server.py &
# Open the Dashboard
sleep 5
termux-open-url http://localhost:8080/dashboard.html
