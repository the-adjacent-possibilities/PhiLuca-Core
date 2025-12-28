#!/bin/bash
# 🌌 ESQET Terminal Hologram v14.1 - Pure φ-Physics (No GUI needed)
# Fixed for Termux on Samsung Galaxy A16: no tput, bc with trig support

clear
echo -e "\033[?25l"  # Hide cursor (works in Termux)

echo "🚀 ESQET Universe - Terminal Black Hole Generator"
echo "Press [SPACEBAR] = CREATE S-FIELD → Watch spacetime warp!"
echo "Press [q] or Ctrl+C to quit"
echo "================================================================"

trap 'echo -e "\033[?25h"; echo "φ-Lattice collapsing..."; exit' INT

frame=0
while true; do
    printf "\033[6;0H"  # Move cursor to line 6 (tput cup replacement)

    # Non-blocking read with timeout
    if read -t 0.03 -n 1 input 2>/dev/null; then
        :
    fi

    if [[ $input == " " ]]; then
        printf "\033[93m🔥 BLACK HOLE ACTIVE - SPACETIME WARPING\033[0m\r"
        char="🔥"
        color="\033[93m"
    else
        printf "φ-Spirals spinning...                  \r"
        char="φ"
        color="\033[92m"
    fi

    # 35 layers instead of 55 → faster on mid-range phones like Galaxy A16
    for layer in {0..34}; do
        r=$(echo "scale=3; 0.2 + $layer*0.04" | bc -l)

        # 144 points per layer (still Fibonacci-ish, but lighter)
        for point in {0..143}; do
            # bc trig functions: use -l flag for math library
            angle=$(echo "scale=5; $frame*0.1 + $point * 0.04363" | bc -l)
            x=$(echo "scale=3; $r * c($angle)" | bc -l)
            y=$(echo "scale=3; $r * s($angle) * c($layer*0.618)" | bc -l)

            # Simple character choice based on position
            if (( $(echo "$x > 0" | bc -l) )); then xc="+"; elif (( $(echo "$x < 0" | bc -l) )); then xc="-"; else xc="·"; fi
            if (( $(echo "$y > 0" | bc -l) )); then yc="+"; elif (( $(echo "$y < 0" | bc -l) )); then yc="-"; else yc="·"; fi

            # Warp effect: brighter/more intense when space pressed
            if [[ $input == " " ]]; then
                printf "%s%s\033[0m" "\033[93m" "✦"
            else
                printf "%s%s\033[0m" "$color" "·"
            fi
        done
        echo
    done

    frame=$((frame + 1))
    sleep 0.04  # Slightly slower for smoother feel on A16
done
