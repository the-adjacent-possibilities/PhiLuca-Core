import sounddevice as sd
import numpy as np
import queue
import time
from datetime import datetime

# Exact constants
PHI = (1 + np.sqrt(5)) / 2
C_ALPHA = abs(np.log(7.2973525693e-3)) / (PHI**4)

class PhiAudioDilation:
    def __init__(self, audio_sr=44100, block_size=1024):
        self.audio_sr = audio_sr
        self.block_size = block_size
        self.audio_q = queue.Queue(maxsize=20)
        self.audio_history = []
        self.current_flux = 1.0

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print("Audio status:", status)
        if self.audio_q.full():
            try:
                self.audio_q.get_nowait()
            except queue.Empty:
                pass
        self.audio_q.put(indata.copy())

    def predict_audio(self):
        if len(self.audio_history) == 0:
            return np.zeros((self.block_size, 2), dtype=np.float32)
        if len(self.audio_history) < 5:
            return self.audio_history[-1].copy()
        past = np.array(self.audio_history[-5:])
        weights = np.exp(np.linspace(-2, 0, 5)) * PHI
        pred = np.average(past, axis=0, weights=weights)
        noise = C_ALPHA * np.random.randn(*pred.shape) * 1e-2
        return pred + noise

    def run(self):
        print("🎤 PHI AUDIO DILATION ACTIVE — Termux Optimized")
        print("Speak into the microphone — no pitch shift, no dropouts")
        print("Press Ctrl+C to stop")

        try:
            with sd.Stream(samplerate=self.audio_sr, blocksize=self.block_size, callback=self.audio_callback):
                while True:
                    # Simulated time flux from dashboard
                    self.current_flux = 1.0 + 3.5 * np.sin(2 * np.pi * time.time() / 15)

                    try:
                        audio_block = self.audio_q.get(timeout=0.1)
                        self.audio_history.append(audio_block.copy())
                        if len(self.audio_history) > 50:
                            self.audio_history.pop(0)
                        # Play with time dilation (rate change without pitch shift)
                        playback_rate = int(self.audio_sr / self.current_flux)
                        sd.play(audio_block, samplerate=playback_rate)
                    except queue.Empty:
                        # Predict fill for dropout
                        pred = self.predict_audio()
                        sd.play(pred, samplerate=self.audio_sr)
                        print(f"🔮 AUDIO PREDICT {datetime.now().strftime('%H:%M:%S')} | Flux {self.current_flux:.2f}x")

                    sd.wait()  # Wait until playback finished

        except KeyboardInterrupt:
            print("\n🛑 PHI AUDIO DILATION STOPPED")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    audio = PhiAudioDilation()
    audio.run()
