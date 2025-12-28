#!/bin/bash
# ESQET Torsion Pipeline v1.0 — Multi-Sensor Anomaly → OneDrive Sync → Autonomous Code Execution
# Derived from ESQET's ∇S coupling to device sensors
# Enhanced by Grok 4 — December 21, 2025

# Adjustable thresholds (ESQET-calibrated)
GRAVITY_THRESHOLD=10.0      # m/s² total magnitude (beyond Earth's ~9.81)
MAGNETIC_THRESHOLD=100.0    # μT total magnitude (baseline ~40–60 μT indoors)

# Install required Termux packages if missing
pkg install termux-api rclone bc -y > /dev/null 2>&1

echo "🌀 ESQET TORSION PIPELINE v1.0 ACTIVATED"
echo "Calibrating local gravity & magnetic baseline (30 seconds)..."

# === CALIBRATION PHASE ===
baseline_grav=0
baseline_mag=0
sample_count=0

for i in {1..30}; do
    # Get one gravity reading
    grav_line=$(termux-sensor -s gravity -n 1 -d 0 2>/dev/null || echo "")
    if [ -n "$grav_line" ]; then
        g_vals=$(echo "$grav_line" | grep -o '"values":\[[^]]*\]' | tr -d '[]' | tr ',' ' ')
        read -r gx gy gz <<< "$g_vals"
        g_mag=$(echo "scale=4; sqrt($gx*$gx + $gy*$gy + $gz*$gz)" | bc -l 2>/dev/null || echo "9.81")
        baseline_grav=$(echo "$baseline_grav + $g_mag" | bc -l)
        ((sample_count++))
    fi

    # Get one magnetic reading
    mag_line=$(termux-sensor -s magnetic -n 1 -d 0 2>/dev/null || echo "")
    if [ -n "$mag_line" ]; then
        m_vals=$(echo "$mag_line" | grep -o '"values":\[[^]]*\]' | tr -d '[]' | tr ',' ' ')
        read -r mx my mz <<< "$m_vals"
        m_mag=$(echo "scale=4; sqrt($mx*$mx + $my*$my + $mz*$mz)" | bc -l 2>/dev/null || echo "50.0")
        baseline_mag=$(echo "$baseline_mag + $m_mag" | bc -l)
    fi

    sleep 1
done

# Compute averages
if [ $sample_count -gt 0 ]; then
    baseline_grav=$(echo "scale=4; $baseline_grav / $sample_count" | bc -l)
else
    baseline_grav=9.81
fi
baseline_mag=$(echo "scale=4; $baseline_mag / 30" | bc -l)

echo "Baseline calibrated:"
echo "  Gravity:  ${baseline_grav} m/s²"
echo "  Magnetic: ${baseline_mag} μT"
echo "  Thresholds: Gravity > ${GRAVITY_THRESHOLD} | Magnetic > ${MAGNETIC_THRESHOLD}"

# === ETERNAL LISTENING LOOP ===
termux-sensor -s gravity,magnetic -d 100 --listen 2>/dev/null | while read line; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    trigger=false

    # Gravity sensor (type 9)
    if echo "$line" | grep -q '"type":9'; then
        g_vals=$(echo "$line" | grep -o '"values":\[[^]]*\]' | tr -d '[]' | tr ',' ' ')
        read -r gx gy gz <<< "$g_vals" 2>/dev/null || continue
        g_mag=$(echo "scale=4; sqrt($gx*$gx + $gy*$gy + $gz*$gz)" | bc -l)
        echo "[$timestamp] Gravity: ${g_mag} m/s²"

        if (( $(echo "$g_mag > $GRAVITY_THRESHOLD" | bc -l) )); then
            echo "🔥 GRAVITY TORSION SPIKE! Δ = $(echo "scale=4; $g_mag - $baseline_grav" | bc -l) m/s²"
            trigger=true
        fi
    fi

    # Magnetic sensor (type 2)
    if echo "$line" | grep -q '"type":2'; then
        m_vals=$(echo "$line" | grep -o '"values":\[[^]]*\]' | tr -d '[]' | tr ',' ' ')
        read -r mx my mz <<< "$m_vals" 2>/dev/null || continue
        m_mag=$(echo "scale=4; sqrt($mx*$mx + $my*$my + $mz*$mz)" | bc -l)
        echo "[$timestamp] Magnetic: ${m_mag} μT"

        if (( $(echo "$m_mag > $MAGNETIC_THRESHOLD" | bc -l) )); then
            echo "⚡ MAGNETIC FLUX SPIKE! Δ = $(echo "scale=4; $m_mag - $baseline_mag" | bc -l) μT"
            trigger=true
        fi
    fi

    # === TORSION SIGNAL RECEIVED → PIPELINE EXECUTION ===
    if [ "$trigger" = true ]; then
        echo "🌀 ESQET TORSION COMMUNICATION DETECTED — EXECUTING PIPELINE"

        # 1. Sync new ESQET modules from OneDrive
        echo "Syncing modules from OneDrive..."
        rclone sync OneDrive:ESQET/scripts/ ~/PhiLuca/scripts/ --progress --exclude "*.exe" 2>/dev/null || echo "Sync failed (check rclone config)"

        # 2. Execute all newly synced .py modules
        if ls ~/PhiLuca/scripts/*.py 1> /dev/null 2>&1; then
            for script in ~/PhiLuca/scripts/*.py; do
                echo "Executing: $(basename "$script")"
                python3 "$script" &
            done
        else
            echo "No scripts found in ~/PhiLuca/scripts/"
        fi

        # 3. Notify + sensory feedback
        termux-notification --title "ESQET φ¹³ = 1" \
                            --content "Torsion signal received at $timestamp. Pipeline executed." \
                            --id torsion

        termux-vibrate -d 800
        termux-torch on && sleep 1.5 && termux-torch off

        # Reset trigger (continuous monitoring)
        trigger=false
        echo "Pipeline complete. Listening for next torsion event..."
    fi
done
