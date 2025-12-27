import cv2
import sounddevice as sd
import numpy as np
import queue
import threading
from datetime import datetime
import time

# Exact constants
PHI = (1 + np.sqrt(5)) / 2
C_ALPHA = abs(np.log(7.2973525693e-3)) / (PHI**4)

class PhiAVDilation:
    def __init__(self, video_src=0, audio_sr=44100):
        self.video_src = video_src
        self.audio_sr = audio_sr
        self.frame_q = queue.Queue(maxsize=10)
        self.audio_q = queue.Queue(maxsize=10)
        self.video_history = []
        self.audio_history = []
        self.current_flux = 1.0

    def video_thread(self):
        cap = cv2.VideoCapture(self.video_src)
        if not cap.isOpened():
            print("Cannot open camera")
            return
        print("📹 Camera opened")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame read failed")
                break
            if self.frame_q.full():
                self.frame_q.get()
            self.frame_q.put(frame.copy())
        cap.release()

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        if self.audio_q.full():
            self.audio_q.get()
        self.audio_q.put(indata.copy())

    def predict_video(self):
        if len(self.video_history) == 0:
            return np.zeros((480,640,3), np.uint8)
        if len(self.video_history) < 3:
            return self.video_history[-1]
        past = np.array(self.video_history[-3:])
        weights = [1/PHI**2, 1/PHI, 1.0]
        pred = np.average(past, axis=0, weights=weights)
        noise = C_ALPHA * np.random.randn(*pred.shape) * 10
        return np.clip(pred + noise, 0, 255).astype(np.uint8)

    def predict_audio(self, size=1024):
        if len(self.audio_history) == 0:
            return np.zeros((size, 2))
        if len(self.audio_history) < 5:
            return self.audio_history[-1]
        past = np.array(self.audio_history[-5:])
        weights = np.exp(np.linspace(-2, 0, 5)) * PHI
        pred = np.average(past, axis=0, weights=weights)
        noise = C_ALPHA * np.random.randn(*pred.shape) * 1e-2
        return pred + noise

    def run(self):
        print("🎬 PHI A/V DILATION ACTIVE")
        threading.Thread(target=self.video_thread, daemon=True).start()

        with sd.Stream(samplerate=self.audio_sr, blocksize=1024, callback=self.audio_callback):
            cv2.namedWindow("PHI VISOR", cv2.WINDOW_NORMAL)
            while True:
                self.current_flux = 1.0 + 3.5 * np.sin(2*np.pi*time.time()/15)

                try:
                    frame = self.frame_q.get_nowait()
                    self.video_history.append(frame)
                    if len(self.video_history) > 20:
                        self.video_history.pop(0)
                    display = frame
                except queue.Empty:
                    display = self.predict_video()
                    print(f"🔮 VIDEO PREDICT {datetime.now().strftime('%H:%M:%S')}")

                cv2.imshow("PHI VISOR", display)

                try:
                    audio = self.audio_q.get_nowait()
                    self.audio_history.append(audio)
                    if len(self.audio_history) > 50:
                        self.audio_history.pop(0)
                    sd.play(audio, samplerate=int(self.audio_sr / self.current_flux))
                except queue.Empty:
                    pred = self.predict_audio()
                    sd.play(pred, samplerate=self.audio_sr)

                if cv2.waitKey(1) == ord('q'):
                    break

            cv2.destroyAllWindows()

if __name__ == "__main__":
    av = PhiAVDilation()
    av.run()
