import hashlib, time, numpy as np
from multiprocessing import Pool, cpu_count

class AnnealingMiner:
    def __init__(self, header_prefix, target):
        self.header = header_prefix
        self.target = target

    def energy(self, x):
        nonce = int(abs(x[0])) % (2**32)
        hsh = hashlib.sha256(hashlib.sha256(self.header + nonce.to_bytes(4, 'little')).digest()).digest()
        return int.from_bytes(hsh[::-1], 'big')

    def __call__(self, x):
        return self.energy(x)
