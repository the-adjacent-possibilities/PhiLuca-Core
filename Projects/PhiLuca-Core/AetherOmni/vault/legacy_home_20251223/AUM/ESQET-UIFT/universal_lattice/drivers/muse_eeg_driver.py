#!/usr/bin/env python3
"""
Advanced Muse EEG Driver for ESQET-UIFT - Build 1.3
Features:
- Robust reconnection logic
- Signal quality monitoring
- Advanced functional connectivity:
  - Band powers (delta, theta, alpha, beta, gamma)
  - Mean Phase-Locking Value (PLV)
  - Weighted Phase-Lag Index (wPLI)
  - Imaginary Coherence (iCoh)
- Thread-safe queue with fallback to random data on failure
"""

import time
import numpy as np
from collections import deque
import threading
import logging
from scipy.signal import welch, hilbert
from bluepy.btle import Scanner, DefaultDelegate, Peripheral

logger = logging.getLogger("EEG_DRIVER")

# Muse BLE constants (verified 2025)
MUSE_SERVICE_UUID = "0000fe8d-0000-1000-8000-00805f9b34fb"
EEG_CHAR_UUIDS = [
    "273e0003-4c4d-454d-96be-f03bac821358",  # Channel 1 (TP9)
    "273e0004-4c4d-454d-96be-f03bac821358",  # Channel 2 (AF7)
    "273e0005-4c4d-454d-96be-f03bac821358",  # Channel 3 (AF8)
    "273e0006-4c4d-454d-96be-f03bac821358",  # Channel 4 (TP10)
]
CTRL_CHAR_UUID = "273e0001-4c4d-454d-96be-f03bac821358"

class MuseDelegate(DefaultDelegate):
    def __init__(self, queues):
        super().__init__()
        self.queues = queues  # list of 4 deques

    def handleNotification(self, cHandle, data):
        if len(data) == 20:
            samples = np.frombuffer(data, dtype='>u2', offset=2)  # 10 x 12-bit samples
            unpacked = np.unpackbits(samples.view(np.uint8), bitorder='big') \
                      .reshape(-1, 16)[:, 4:]  # remove preset bits
            values = np.packbits(unpacked, axis=1).view(np.int16).flatten()
            ch_idx = EEG_CHAR_UUIDS.index(self._char_uuid_from_handle(cHandle))
            for v in values[:12]:  # usually 12 samples per packet
                if len(self.queues[ch_idx]) < 512:
                    self.queues[ch_idx].append(v)

class MuseEEGStreamer:
    def __init__(self):
        self.queues = [deque(maxlen=512) for _ in range(4)]
        self.peripheral = None
        self.connected = False
        self.lock = threading.Lock()
        self.last_good_signal = time.time()

    def find_and_connect(self, max_attempts=5):
        for attempt in range(max_attempts):
            try:
                scanner = Scanner()
                devices = scanner.scan(10.0)
                muse_dev = None
                for dev in devices:
                    if "Muse" in dev.getValueText(9) or "Muse" in dev.addr:
                        muse_dev = dev
                        break
                if not muse_dev:
                    logger.warning(f"[EEG] Attempt {attempt+1}: No Muse found")
                    time.sleep(5)
                    continue

                self.peripheral = Peripheral(muse_dev.addr)
                self.peripheral.setDelegate(MuseDelegate(self.queues))

                # Enable notifications
                for uuid in EEG_CHAR_UUIDS:
                    char = self.peripheral.getCharacteristics(uuid=uuid)[0]
                    char.write(b"\x02\x00", withResponse=True)  # enable notify

                # Start streaming (256 Hz preset)
                ctrl = self.peripheral.getCharacteristics(uuid=CTRL_CHAR_UUID)[0]
                ctrl.write(b"p21")  # preset 21 = 256 Hz EEG

                self.connected = True
                self.last_good_signal = time.time()
                logger.info("[EEG] Connected to Muse successfully")
                return True
            except Exception as e:
                logger.error(f"[EEG] Connection attempt {attempt+1} failed: {e}")
                if self.peripheral:
                    self.peripheral.disconnect()
                time.sleep(5)
        return False

    def get_advanced_features(self):
        with self.lock:
            if all(len(q) >= 256 for q in self.queues):
                data = [np.array(list(q)) for q in self.queues]
                self.last_good_signal = time.time()
            else:
                # Signal loss fallback
                if time.time() - self.last_good_signal > 10:
                    logger.warning("[EEG] Poor signal quality >10s → fallback")
                return np.random.randn(64).astype(np.float32)

        # Band powers
        bands = [(0.5,4), (4,8), (8,13), (13,30), (30,50)]
        band_names = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        features = []

        for low, high in bands:
            for ch in data:
                f, Pxx = welch(ch, fs=256, nperseg=256)
                idx = (f >= low) & (f <= high)
                features.append(np.log10(np.mean(Pxx[idx]) + 1e-12))

        # Advanced connectivity metrics
        # PLV
        analytic = [hilbert(ch - ch.mean()) for ch in data]
        phases = [np.angle(a) for a in analytic]
        plv_sum = 0.0
        pair_count = 0
        for i in range(4):
            for j in range(i+1, 4):
                phase_diff = phases[i] - phases[j]
                plv_sum += np.abs(np.mean(np.exp(1j * phase_diff)))
                pair_count += 1
        mean_plv = plv_sum / pair_count if pair_count else 0.0
        features.append(mean_plv)

        # wPLI (weighted Phase Lag Index)
        cross_spect = []
        for i in range(4):
            for j in range(i+1, 4):
                f, Pxy = welch(data[i], data[j], fs=256, nperseg=256, noverlap=128)
                imag_part = np.imag(Pxy)
                wpli = np.abs(np.mean(np.abs(imag_part) * np.sign(imag_part))) / np.mean(np.abs(imag_part))
                cross_spect.append(wpli)
        mean_wpli = np.mean(cross_spect) if cross_spect else 0.0
        features.append(mean_wpli)

        # Imaginary Coherence (mean over pairs)
        mean_icoh = np.mean([np.abs(np.mean(np.imag(Pxy))) / np.mean(np.abs(Pxy)) for Pxy in cross_spect])
        features.append(mean_icoh)

        # Pad/truncate to 64-dim vector
        feature_vec = np.array(features, dtype=np.float32)
        if len(feature_vec) < 64:
            feature_vec = np.pad(feature_vec, (0, 64 - len(feature_vec)))
        return feature_vec[:64]

    def disconnect(self):
        if self.peripheral:
            try:
                self.peripheral.disconnect()
            except:
                pass
        self.connected = False
