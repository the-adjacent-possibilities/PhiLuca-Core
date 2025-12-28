import numpy as np
import os

class RAIDEncryption:
    def __init__(self, block_size=16):
        self.block_size = block_size

    def shard_data(self, data):
        """Stripes data into blocks and computes parity."""
        # Padding
        pad_len = self.block_size - (len(data) % self.block_size)
        data += b'\x00' * pad_len
        
        # Sharding into 2 data blocks (D1, D2)
        mid = len(data) // 2
        d1 = np.frombuffer(data[:mid], dtype=np.uint8)
        d2 = np.frombuffer(data[mid:], dtype=np.uint8)
        
        # XOR Parity
        parity = np.bitwise_xor(d1, d2)
        return d1.tobytes(), d2.tobytes(), parity.tobytes()

    def reconstruct(self, d1, d2, parity_unlocked):
        """Reverses RAID to recover data using unlocked parity."""
        b1 = np.frombuffer(d1, dtype=np.uint8)
        b2 = np.frombuffer(d2, dtype=np.uint8)
        p = np.frombuffer(parity_unlocked, dtype=np.uint8)
        
        # Validation: D1 ^ D2 must equal P
        if not np.array_equal(np.bitwise_xor(b1, b2), p):
            return None
            
        return (d1 + d2).rstrip(b'\x00')

if __name__ == "__main__":
    re = RAIDEncryption()
    d1, d2, p = re.shard_data(b"AetherOmni_Master_Key_2025")
    print(f"[*] Shards Created. Parity Size: {len(p)} bytes.")
    recovered = re.reconstruct(d1, d2, p)
    print(f"[*] Recovery Test: {recovered.decode()}")
