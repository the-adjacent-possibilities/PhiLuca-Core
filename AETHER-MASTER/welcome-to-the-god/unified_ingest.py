#!/usr/bin/env python3
import os, subprocess, shutil, logging
from pathlib import Path
from config import *
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
log = logging.getLogger("INGEST")
def rclone_sync(remote_cfg):
    src, dst = remote_cfg["source"], remote_cfg["target"]
    dst.mkdir(parents=True, exist_ok=True)
    cmd = ["rclone", "sync", src, str(dst), "--checksum", "--retries", "3", "--progress"]
    log.info(f"🔄 {src} → {dst}")
    subprocess.run(cmd, check=True)
def extract_learning():
    learn_dir = INGEST_ROOT / "LEARNING_FLAT"
    learn_dir.mkdir(exist_ok=True)
    count = 0
    for cloud_dir in INGEST_ROOT.glob("EXTERNAL_*"):
        for file in cloud_dir.rglob("*"):
            if file.suffix.lower() in LEARN_EXTS and file.is_file():
                rel = file.relative_to(cloud_dir)
                dest = learn_dir / f"{cloud_dir.name}__{rel.as_posix().replace('/', '__')}"
                if not dest.exists():
                    shutil.copy2(file, dest)
                    count += 1
    log.info(f"📚 {count} files → LEARNING_FLAT/")
if __name__ == "__main__":
    for name, cfg in CLOUD_REMOTE_MAP.items():
        rclone_sync(cfg)
    extract_learning()
    log.info("✅ INGESTION COMPLETE")
