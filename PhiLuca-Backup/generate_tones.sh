#!/bin/bash

# Generates a 10-second high-quality sine wave at 236.64 Hz
sox -n phi_tone_236.64.wav synth 10 sine 236.64

# Generates the 'Cosmic OM' frequency (136.1 Hz)
sox -n cosmic_om_136.1.wav synth 10 sine 136.1

echo "Tones generated successfully."
