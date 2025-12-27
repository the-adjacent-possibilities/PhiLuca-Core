#!/usr/bin/env python3
import os, subprocess, shutil, json, logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from config import *
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
log = logging.getLogger("REPO_CLONER")
def clone_repo(url, target_dir):
    repo_name = Path(url).stem.replace('.git', '')
    local_path = target_dir / repo_name
    if local_path.exists():
        log.info(f"⏭️ {repo_name}")
        return
    subprocess.run(["git", "clone", "--depth=1", url, str(local_path)], check=True)
    log.info(f"✅ {repo_name}")
    learn_dir = INGEST_ROOT / "LEARNING_FLAT"
    count = 0
    for file in local_path.rglob("*"):
        if file.suffix.lower() in LEARN_EXTS and file.is_file():
            rel = file.relative_to(local_path)
            dest = learn_dir / f"REPO__{repo_name}__{rel.as_posix().replace('/', '__')}"
            if not dest.exists():
                shutil.copy2(file, dest)
                count += 1
    log.info(f"📚 {repo_name}: {count} files")
if __name__ == "__main__":
    repos_dir = INGEST_ROOT / "CLONED_REPOS/github"
    repos_dir.mkdir(exist_ok=True)
    repos = json.loads(Path("repo_manifest.json").read_text())
    urls = [f"https://github.com/{repo}.git" for repo in repos]
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda url: clone_repo(url, repos_dir), urls)
    log.info("✅ REPO CLONING COMPLETE")
