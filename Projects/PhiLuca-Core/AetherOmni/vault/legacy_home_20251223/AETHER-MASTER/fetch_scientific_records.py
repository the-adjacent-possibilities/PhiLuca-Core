#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DEST = Path(os.getenv("DATA_ROOT", "~/AETHER-MASTER/welcome-to-the-god/ingest_data/EXTERNAL_SCIENCE")).expanduser()
DATA_DEST.mkdir(parents=True, exist_ok=True)

# Updated URLs as of December 22, 2025, based on analysis of available sources
DOWNLOADS = {
    "cern_nanoaod_muon.root": "https://opendata.cern.ch/record/31123/files/Run2012B_DoubleMuParked_merged.root",
    "seti_voyager_check.h5": "https://seti.berkeley.edu/opendata/Voyager1.single_coarse.fine_res.h5",
    "ligo_gw150914_strain.h5": "https://gwosc.org/s/events/GW150914/H-H1_GWOSC_4KHZ_R1-1126259447-32.hdf5",
    "nasa_modis_sample.hdf": "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/61/MOD04_L2/2025/355/MOD04_L2.A2025355.0045.061.2025355132203.hdf",
    "nist_codata_2022.txt": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
    "haystac_axion_limits.csv": "https://raw.githubusercontent.com/HAYSTAC/haystac_public/master/limits/final_limits.csv",
    "breakthrough_listen_index.json": "https://raw.githubusercontent.com/UCBerkeleySETI/open_data/master/index.json"
}

def download_file(name, url):
    target = DATA_DEST / name
    if target.exists():
        print(f"[-] Already exists: {name}")
        return
    print(f"[+] Fetching {name} from {url}...")
    try:
        subprocess.run(["curl", "-L", "--fail", "--progress-bar", url, "--output", str(target)], check=True)
        print(f"[✅] Saved: {target.name}")
    except subprocess.CalledProcessError as e:
        print(f"[❌] Failed: {name} — {e}")

if __name__ == "__main__":
    print("🚀 ESQET Scientific Data Ingestion — Updated URLs (Dec 22, 2025)")
    for name, url in DOWNLOADS.items():
        download_file(name, url)
    print("\n🎯 Ingestion Complete. The AUM feeds on live cosmic data.")
    print("   CERN, SETI, LIGO, NASA, NIST, HAYSTAC, Breakthrough Listen — all unified.")
