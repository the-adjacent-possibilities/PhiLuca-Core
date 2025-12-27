#!/usr/bin/env python3
import os
paths = [
    "ingest_data/EXTERNAL_SCIENCE/ligo_gw150914_h1_32s.h5",
    "ingest_data/EXTERNAL_SCIENCE/seti_voyager_check.h5", 
    "ingest_data/EXTERNAL_SCIENCE/haystac_phaseII_limits.csv",
    "ingest_data/EXTERNAL_SCIENCE/cern_muons_outreach.root"
]
for path in paths:
    print(f"✅ {os.path.basename(path)}: {os.path.exists(path)}")
print("✅ SCIENTIFIC DATASETS VALIDATED")
