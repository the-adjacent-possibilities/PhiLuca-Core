import os
import sys

# Add the lobe directory to path so we can use the RAID logic
sys.path.append(os.path.expanduser("~/AetherOmni/lobes/cyber"))
from vault_raid_encryption import RAIDEncryption

def generate():
    re = RAIDEncryption(block_size=16)
    vault_path = os.path.expanduser("~/AetherOmni/vault/keys")
    os.makedirs(vault_path, exist_ok=True)
    
    # The actual secret we are sharding
    secret = b"PHINPIPI_RESONANCE_2025"
    
    # Create the RAID shards
    d1, d2, p = re.shard_data(secret)
    
    # Write binaries to the vault
    with open(os.path.join(vault_path, "shard_alpha.bin"), "wb") as f: f.write(d1)
    with open(os.path.join(vault_path, "shard_beta.bin"), "wb") as f: f.write(d2)
    with open(os.path.join(vault_path, "parity_goddess.bin"), "wb") as f: f.write(p)
    
    print(f"[💎] Shards successfully materialized in {vault_path}")

if __name__ == "__main__":
    generate()
