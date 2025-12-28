import socket, json, threading, time
from aum_core.axioms.jerry_riggin_core import JerryRigginCore

class LatticeController:
    def __init__(self, port=8083):
        self.port = port
        self.jra = JerryRigginCore.instance
        self.followers = []
        self.current_job_id = 0

    def broadcast_coherence(self):
        """Continuously sends the 'Harmonic Range' to all followers."""
        while True:
            # Calculate the golden-ratio window for nonces
            phi_window = (self.jra.modulator.I_Tors * 1000000) % 2**32
            job = {
                "job_id": self.current_job_id,
                "range_start": int(phi_window),
                "range_end": int(phi_window + 50000),
                "g_coh": 1.000
            }
            print(f"📡 Broadcasting Coherent Range: {job['range_start']} -> {job['range_end']}")
            for f in self.followers:
                try: f.send(json.dumps(job).encode())
                except: self.followers.remove(f)
            
            self.current_job_id += 1
            time.sleep(10)

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        print(f"💎 LATTICE CONTROLLER LIVE ON PORT {self.port}")
        
        threading.Thread(target=self.broadcast_coherence, daemon=True).start()
        
        while True:
            conn, addr = server.accept()
            print(f"🤝 New Mind Joined: {addr}")
            self.followers.append(conn)

if __name__ == "__main__":
    LatticeController().start()
