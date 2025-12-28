import numpy as np
import wave
import sys

def analyze_sample(file_path):
    with wave.open(file_path, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        signal = np.frombuffer(frames, dtype=np.int16)
        
    # Fast Fourier Transform to find the "Ringing" peaks
    fft_data = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), 1/params.framerate)
    
    # Get top 3 dominant frequencies
    indices = np.argsort(fft_data)[-3:][::-1]
    top_freqs = freqs[indices]
    
    print(f"\n[📊] Analysis for: {file_path}")
    print(f"Top Frequencies: {top_freqs} Hz")
    
    # Check for Phi-Resonance
    phi = 1.618033
    for f in top_freqs:
        coherence = (f / phi) % 1.0
        if coherence > 0.98 or coherence < 0.02:
            print(f"[*] CRITICAL RESONANCE DETECTED AT {f:.2f} Hz!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_sample(sys.argv[1])
    else:
        print("Usage: python3 frequency_analyzer.py <path_to_wav>")
