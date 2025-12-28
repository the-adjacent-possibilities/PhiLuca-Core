import http.server
import json
import random
import subprocess
import os

class AetherHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Check if the PID file exists to report recording status
        is_recording = os.path.exists(os.path.expanduser("~/AetherOmni/recorder.pid"))

        if self.path == '/data':
            flux = round(45.0 + random.uniform(-0.5, 0.5), 2)
            self.wfile.write(json.dumps({
                "flux_ut": flux, 
                "coherence": 0.99,
                "recording": is_recording
            }).encode())
        
        elif self.path == '/start':
            subprocess.Popen(["bash", os.path.expanduser("~/AetherOmni/observer_control.sh"), "start"])
            
        elif self.path in ['/stop', '/pause']:
            subprocess.Popen(["bash", os.path.expanduser("~/AetherOmni/observer_control.sh"), "stop"])

if __name__ == "__main__":
    server = http.server.HTTPServer(('localhost', 8081), AetherHandler)
    server.serve_forever()
