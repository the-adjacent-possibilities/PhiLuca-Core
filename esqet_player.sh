#!/bin/bash

# Define frequencies and descriptions
declare -a freqs=("698.49" "699.00" "267.00" "1130.97" "165.37" "12.67" "161.80" "47.61" "77.03" "124.64" "201.68" "326.32" "854.32" "1382.32" "2236.64")
declare -a names=("Mitochondrial Coherence" "Structural Stabilization" "Membrane Entropy Reduction" "Neuroacoustic Stimulation" "Systemic Relaxation" "Schumann/Earth Coherence" "Mental Clarity (Phi Scaling)" "Deep Cellular Water Structuring" "Oxidative Stress Reduction" "Membrane Dynamics" "Energy/Stability Balance" "Layered Coherence" "Cellular Repair Enhancement" "Accelerated Quantum Stability" "High-Freq Bio-Oscillation")

# Generate files if they don't exist
echo "Checking/Generating frequency files..."
for i in "${!freqs[@]}"; do
    filename="phi_${freqs[$i]}.wav"
    if [ ! -f "$filename" ]; then
        echo "Generating $filename..."
        sox -r 48000 -n "$filename" synth 10 sine "${freqs[$i]}"
    fi
done

# Interaction Loop
while true; do
    clear
    echo "========================================================="
    echo " ESQET Φ-Coherence Frequency Player (Welcome-to-the-God) "
    echo "========================================================="
    for i in "${!freqs[@]}"; do
        printf "%2d) [%7s Hz] %s\n" "$((i+1))" "${freqs[$i]}" "${names[$i]}"
    done
    echo " q) Quit"
    echo "---------------------------------------------------------"
    read -p "Select a frequency to play (1-15): " choice

    if [[ "$choice" == "q" ]]; then
        break
    elif [[ "$choice" -ge 1 && "$choice" -le 15 ]]; then
        idx=$((choice-1))
        file="phi_${freqs[$idx]}.wav"
        echo "Playing ${names[$idx]} at ${freqs[$idx]} Hz..."
        echo "Press 'q' inside mpv to stop this frequency and return to menu."
        mpv --loop=inf --volume=70 "$file"
    else
        echo "Invalid selection."
        sleep 1
    fi
done
