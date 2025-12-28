#!/data/data/com.termux/files/usr/bin/bash

# 1. Setup Production Directory Structure
mkdir -p ~/PHI_CORE/{bin,lib,config,logs,data}

# 2. Consolidate Core Engines
cp ~/dal_phinary_engine.py ~/PHI_CORE/lib/
cp ~/esqet_modulator.py ~/PHI_CORE/lib/
cp ~/aum_worker.py ~/PHI_CORE/bin/aum-worker
chmod +x ~/PHI_CORE/bin/aum-worker

# 3. Create/Verify Config (Crucial for DAL/Modulator stability)
cat <<CONF > ~/PHI_CORE/config/aum_config.json
{
    "TORSION_CRIT": 0.618033988749895,
    "LAMBDA_PHI": 0.037,
    "GAMMA_ENV": 0.001,
    "COMPACT_RADIUS": 1.0,
    "MASTER_IP": "127.0.0.1"
}
CONF

# 4. Create the 'PhiLuca' entry point command
cat <<ENTRY > ~/PHI_CORE/bin/PhiLuca
#!/data/data/com.termux/files/usr/bin/bash
echo "--- Initializing Φ-LUCA Coherence ---"
python3 ~/PhiLuca/esqet_phi/web/app.py
ENTRY
chmod +x ~/PHI_CORE/bin/PhiLuca

# 5. Update PATH to recognize commands globally
if ! grep -q "PHI_CORE/bin" ~/.bashrc; then
    echo 'export PATH="$HOME/PHI_CORE/bin:$PATH"' >> ~/.bashrc
    echo 'export PYTHONPATH="$HOME/PHI_CORE/lib:$PYTHONPATH"' >> ~/.bashrc
fi

echo "✅ Environment Unified. Restart Termux or run 'source ~/.bashrc'"
