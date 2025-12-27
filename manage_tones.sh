#!/bin/bash

# Function to generate a tone
gen_tone() {
    local freq=$1
    local name=$2
    echo "Generating $name ($freq Hz)..."
    ffmpeg -y -f lavfi -i "sine=frequency=$freq:duration=10" -ar 44100 -ac 1 "$name.wav" -loglevel error
}

# Generate your specific tones (shortened to 10s for testing)
gen_tone 699 "phi_tone_699"
gen_tone 698.49 "phi_tone_precise"
gen_tone 267 "phi_tone_267"

echo "---"
echo "To play a file in Termux, use: play-audio <filename>"
echo "Example: play-audio phi_tone_699.wav"
