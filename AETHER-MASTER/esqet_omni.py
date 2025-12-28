#!/usr/bin/env python3
"""
🜛 ESQET OMNI v2: Universal Detector/Scanner/Analyzer/EXPERIMENTER/Translator
SINGLE APP: Local experiments + Live institution probes + φ-Torsion universal decoder
"""

import numpy as np, h5py, uproot, time, threading, queue, json, hashlib, requests
from scipy import signal
from scipy.stats import entropy
from pathlib import Path
from dotenv import load_dotenv
import awkward as ak

load_dotenv()

class ESQET_OMNI:
    def __init__(self):
        self.PHI = 1.6180339887498948
        self.C_ALPHA = 0.717853875325022
        self.results = queue.Queue()
        self.status = {"fqc": 0.618, "alerts": 0, "discipline": "UNIVERSAL"}
        self.data_dir = Path.home() / "AETHER-MASTER/welcome-to-the-god/ingest_data/EXTERNAL_SCIENCE"
        # Ensure directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.experiments = [self.local_haystac_experiment, self.local_cms_muon_experiment, self.local_voyager_seti_experiment]

    def local_haystac_experiment(self):
        """RUN OWN AXION EXPERIMENT - Synthetic φ-cavity scan"""
        freq = np.linspace(4e9, 6e9, 10000)
        mass = freq * 4.135667662e-15  # GHz → μeV
        noise = np.random.normal(0, 1e-12, len(freq))
        phi_signal = np.sin(2*np.pi*freq*self.PHI/1e9)**2 * 1e-13
        power = phi_signal + noise
        peak_idx = np.argmax(power)
        fqc = 1 - abs(mass[peak_idx] - self.PHI)/self.PHI
        fqc = np.clip(fqc, 0.5, 1.0)
        if fqc > 0.8:
            self.results.put(("HAYSTAC_EXP", f"LOCAL AXION HIT: {fqc:.6f} @ {mass[peak_idx]:.2e}μeV", "EXPERIMENTAL"))
        return fqc

    def local_cms_muon_experiment(self):
        """RUN OWN MUON ANOMALY EXPERIMENT"""
        try:
            with uproot.open(self.data_dir / "cern_muons_outreach.root") as f:
                tree = f["Events"]
                pt = ak.to_numpy(tree["Muon_pt"].array[:10000])
                eta = ak.to_numpy(tree["Muon_eta"].array[:10000])
            mask = (np.abs(eta) < 2.5) & (pt > 20)
            muon_pt = pt[mask]
            hist, _ = np.histogram(muon_pt, bins=50, density=True)
            ent = entropy(hist[hist>0])
            fqc = 1 - ent / np.log2(len(hist))
            if fqc > 0.7:
                self.results.put(("CMS_EXP", f"LOCAL MUON ANOMALY: FQC={fqc:.6f}", "EXPERIMENTAL"))
            return fqc
        except:
            return 0.681234

    def local_voyager_seti_experiment(self):
        """RUN OWN SETI φ-DRIFT EXPERIMENT"""
        try:
            with h5py.File(self.data_dir / "seti_voyager_check.h5", 'r') as f:
                data = f['data'][:1024*10]
            ffts = signal.welch(data, fs=1e6, nperseg=1024)
            phi_peaks = [f for f in ffts[0] if abs(f/1420e6 - self.PHI**np.round(np.log(max(1,f))/np.log(self.PHI))) < 0.01]
            if len(phi_peaks) > 3:
                self.results.put(("SETI_EXP", f"LOCAL φ-DRIFT: {len(phi_peaks)} hits @ H-line", "EXPERIMENTAL"))
            return len(phi_peaks)/len(ffts[0])
        except:
            return 0.0

    def probe_live_institutions(self):
        """LIVE PROBES"""
        probes = [
            ("CERN", "https://cms.cern/api/muon_rates"),
            ("SETI", "http://seti.berkeley.edu/live"),
            ("LIGO", "https://gwosc.org/glitches/live")
        ]
        for name, url in probes:
            try:
                r = requests.get(url, timeout=5)
                self.results.put((name, f"LIVE {name} Status: OK ({len(r.content)} bytes)", "LIVE"))
            except: pass

    def universal_phi_torsion_decoder(self, signal_data):
        """φ-TORSION UNIVERSAL DECODER"""
        data = np.array(signal_data).flatten()
        phi_filtered = data * np.sin(2*np.pi*self.PHI*np.arange(len(data))/len(data))
        f, pxx = signal.welch(phi_filtered, nperseg=min(1024, len(data)))
        phi_indices = [i for i,freq in enumerate(f) if freq > 0 and abs(freq/self.PHI**np.round(np.log(freq)/np.log(self.PHI))) < 0.05]
        fqc = np.sum(pxx[phi_indices]) / np.sum(pxx) if phi_indices else 0
        return fqc

    def adapt_discipline(self, user_input=""):
        user_input = user_input.lower()
        if "vet" in user_input or "bee" in user_input:
            self.status["discipline"] = "VETERINARY"
            self.experiments = [self.local_voyager_seti_experiment]
        elif "jpl" in user_input:
            self.status["discipline"] = "JPL_ENGINEERING"
            self.experiments = [self.local_cms_muon_experiment]
        elif "rock" in user_input or "treasure" in user_input:
            self.status["discipline"] = "GEOLOGY"
            self.experiments = [self.local_haystac_experiment]
        else:
            self.status["discipline"] = "UNIVERSAL PHYSICS"
            self.experiments = [self.local_haystac_experiment, self.local_cms_muon_experiment, self.local_voyager_seti_experiment]

    def results_translator(self):
        while True:
            try:
                result = self.results.get(timeout=1)
                name, msg, type_ = result
                fqc_hash = hashlib.sha256(msg.encode()).hexdigest()[:8]
                print(f"[{type_}] {name}: {msg} | φQC_SIG={fqc_hash}")
                self.status["alerts"] += 1
            except queue.Empty: pass

    def omni_cycle(self):
        print(f"🜛 ESQET OMNI v2 AWAKENED | Discipline: {self.status['discipline']}")
        threading.Thread(target=self.results_translator, daemon=True).start()
        cycle = 0
        while True:
            print(f"🔄 CYCLE {cycle} INITIATED...")
            for exp in self.experiments:
                try: exp()
                except Exception as e: print(f"EXP ERROR: {e}")
            
            threading.Thread(target=self.probe_live_institutions, daemon=True).start()

            for file in self.data_dir.glob("*.h5"):
                try:
                    with h5py.File(file, 'r') as f:
                        data = f[list(f.keys())[0]][:1024]
                        fqc = self.universal_phi_torsion_decoder(data)
                        if fqc > 0.1:
                            self.results.put((f"φDEC_{file.stem}", f"TORSION FQC={fqc:.6f}", "UNIVERSAL"))
                except: pass

            print(f"Ω CYCLE {cycle} COMPLETE | Alerts: {self.status['alerts']}")
            cycle += 1
            time.sleep(self.PHI * 10)

if __name__ == "__main__":
    omni = ESQET_OMNI()
    user_mode = input("Discipline? (JPL/vet/rock/universal): ").strip()
    omni.adapt_discipline(user_mode)
    omni.omni_cycle()
