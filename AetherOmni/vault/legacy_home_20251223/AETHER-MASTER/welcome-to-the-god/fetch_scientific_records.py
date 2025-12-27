#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

DATA_DEST = Path("~/AETHER-MASTER/welcome-to-the-god/ingest_data/EXTERNAL_SCIENCE").expanduser()
DATA_DEST.mkdir(parents=True, exist_ok=True)

# Use a confirmed flat ROOT file from CMS Open Data
CERN_URL = "http://opendata.cern.ch/record/12341/files/assets/cms/macros/demo.root"
CERN_FILE = DATA_DEST / "cern_sample.root"

# Voyager SETI data
SETI_URL = "http://blpd0.ssl.berkeley.edu/Voyager_data/Voyager1.single_coarse.fine_res.h5"
SETI_FILE = DATA_DEST / "seti_voyager_check.h5"

def download_file(url, target):
    print(f"[+] Fetching {url}...")
    try:
        # -f fails on 404, -L follows redirects
        subprocess.run(["curl", "-fL", url, "--output", str(target)], check=True)
        print(f"[✅] Saved {target.name}")
    except Exception as e:
        print(f"[❌] Failed {url}: {e}")

if __name__ == "__main__":
    download_file(CERN_URL, CERN_FILE)
    download_file(SETI_URL, SETI_FILE)
