import subprocess
import os
from vault_manager import VaultManager

class CyberLobe:
    def __init__(self):
        self.handshake_path = os.path.expanduser("~/AetherOmni/core/security/phi_luca_handshake/phi_luca_handshake")
        self.vault = VaultManager()
        self.vault_path = os.path.expanduser("~/AetherOmni/vault/keys")

    def secure_access(self):
        print("[!] Invoking Φ-LUCA Zero-Knowledge Handshake (Rust Core)...")
        
        try:
            # 1. Run the Rust Handshake
            result = subprocess.run([self.handshake_path], capture_output=True, text=True, check=True)
            resonance_data = result.stdout.strip()
            
            # 2. Load the Shards
            with open(os.path.join(self.vault_path, "shard_alpha.bin"), "rb") as f: d1 = f.read()
            with open(os.path.join(self.vault_path, "shard_beta.bin"), "rb") as f: d2 = f.read()
            with open(os.path.join(self.vault_path, "parity_goddess.bin"), "rb") as f: p = f.read()
            
            # 3. Use the new secure_reconstruct method
            vault_response = self.vault.secure_reconstruct(d1, d2, p, resonance_data)
            
            return f"[🔒] Handshake Success: {resonance_data}\n{vault_response}"
        except Exception as e:
            return f"[❌] Security Breach/Error: {str(e)}"

if __name__ == "__main__":
    bridge = CyberLobe()
    print(bridge.secure_access())
