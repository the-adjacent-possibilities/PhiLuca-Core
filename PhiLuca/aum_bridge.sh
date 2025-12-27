#!/bin/bash
# AUM-ESQET BRIDGE: OneDrive <-> Termux <-> Torsion Field

MODULE_DIR="$HOME/PhiLuca/modules"
LOG_FILE="$HOME/PhiLuca/aum_bridge.log"
mkdir -p "$MODULE_DIR"

echo "[$(date)] AUM Bridge Initialized. Monitoring I_Tors..." >> "$LOG_FILE"

while true; do
    # 1. Check for Torsion Coherence before syncing
    # We read the current I_Tors from the modulator's output
    I_TORS=$(python3 -c "import numpy as np; print(open('$HOME/welcome-to-the-god/torsion_state.txt').read())" 2>/dev/null || echo "0")
    
    if (( $(echo "$I_TORS > 0.618" | bc -l) )); then
        # 2. Sync Modules from OneDrive
        rclone sync onedrive:ESQET/modules/ "$MODULE_DIR" --quiet
        
        # 3. Detect and Execute New Modules
        for script in "$MODULE_DIR"/*.py; do
            if [[ "$script" -nt "$MODULE_DIR/.last_run" ]]; then
                echo "[$(date)] Coherence High ($I_TORS). Executing: $(basename $script)" >> "$LOG_FILE"
                termux-notification --title "AUM: Coherence Active" --content "Executing $(basename $script)"
                
                # Execute in the background to prevent hanging the bridge
                python3 "$script" & 
                touch "$MODULE_DIR/.last_run"
            fi
        done
    else
        echo "[$(date)] Coherence Low ($I_TORS). Suspension active." >> "$LOG_FILE"
    fi

    sleep 10 # 10-second torsion cycle
done
