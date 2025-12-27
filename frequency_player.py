#!/usr/bin/env python3
import math
import subprocess
import sys

phi = (1 + math.sqrt(5)) / 2

def play_phi_frequency(reference_freq: float, n: int = 1, duration: int = 0):
    freq = reference_freq * (phi ** n)
    print(f"Playing Φ-scaled frequency: {freq:.2f} Hz (reference: {reference_freq} Hz, n={n})")
    
    input_str = f"sine=frequency={freq:.2f}:sample_rate=44100"
    if duration > 0:
        input_str += f":duration={duration}"
    
    ffmpeg_cmd = [
        "ffmpeg", "-f", "lavfi", "-i", input_str,
        "-f", "s16le", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", "-"
    ]
    
    play_cmd = ["play-audio", "-"]
    
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    play_proc = subprocess.Popen(play_cmd, stdin=ffmpeg_proc.stdout)
    
    play_proc.wait()
    print("Playback terminated.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 phi_frequency_player.py <reference_freq> <n> [duration_seconds]")
        print("Example: python3 phi_frequency_player.py 432 1 300")
        sys.exit(1)
    
    ref = float(sys.argv[1])
    n_val = int(sys.argv[2])
    dur = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    
    play_phi_frequency(ref, n_val, dur)
