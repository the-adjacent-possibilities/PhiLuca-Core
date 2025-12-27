#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

DATA_DEST = Path("~/AETHER-MASTER/welcome-to-the-god/ingest_data/EXTERNAL_SCIENCE").expanduser()
DATA_DEST.mkdir(parents=True, exist_ok=True)

CERN_URL = "https://opendata.cern.ch/record/6004/files/assets/cms/upload/NanoAODRun1/01-Jul-22/Run2012B_DoubleMuParked/01-Jul-22Run2012B_DoubleMuParked/03C5684F-8BAF-4312-8235-2B0039F2FB93.root"
SETI_URL = "http://blpd0.ssl.berkeley.edu/Voyager_data/Voyager1.single_coarse.fine_res.h5"

def download_file(url, filename):
    path = DATA_DEST / filename
    if path.exists():
        print(f"[-] Already exists: {filename}")
        return
    print(f"[+] Downloading {url}...")
    subprocess.run(["curl", "-L", url, "-o", str(path)], check=True)
    print(f"[✅] Saved: {filename}")

if __name__ == "__main__":
    print("🜛 Initializing Scientific Data Ingestion...")
    download_file(CERN_URL, "cern_nanoaod_muon.root")
    download_file(SETI_URL, "seti_voyager_check.h5")
    print("🎯 Ingestion Complete — Data Ready for Φ-LUCA")
