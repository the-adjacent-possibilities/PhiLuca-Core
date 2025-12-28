#!/usr/bin/env python3
"""
Deep Repo Learner (No Clone)
- Lists files via GitHub Tree API
- Streams .py files over HTTP
- Runs a simple "learning" pass (e.g., counts defs/imports)
- Stores only summarized results locally
"""

import os
import json
import base64
import textwrap
from pathlib import Path
from typing import Dict, Any, List

import requests  # pip install requests

GITHUB_API = "https://api.github.com"

# Optional: set a GitHub token to avoid low rate limits
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

SESSION = requests.Session()
if GITHUB_TOKEN:
    SESSION.headers.update({"Authorization": f"Bearer {GITHUB_TOKEN}"})


def _api_get(url: str, params: Dict[str, Any] = None) -> Any:
    r = SESSION.get(url, params=params or {})
    r.raise_for_status()
    return r.json()


def get_default_branch(owner: str, repo: str) -> str:
    data = _api_get(f"{GITHUB_API}/repos/{owner}/{repo}")
    return data.get("default_branch", "main")


def get_tree_sha(owner: str, repo: str, branch: str) -> str:
    data = _api_get(f"{GITHUB_API}/repos/{owner}/{repo}/branches/{branch}")
    return data["commit"]["commit"]["tree"]["sha"]


def list_repo_files(owner: str, repo: str, branch: str = None) -> List[Dict[str, Any]]:
    """
    Returns full recursive tree metadata (path, type, size, sha, url).
    """
    if branch is None:
        branch = get_default_branch(owner, repo)
    tree_sha = get_tree_sha(owner, repo, branch)
    data = _api_get(
        f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{tree_sha}",
        params={"recursive": "1"},
    )  # recursive listing [web:79][web:82]
    return data.get("tree", [])


def get_file_content(owner: str, repo: str, path: str, ref: str) -> str:
    """
    Fetch file content via contents API (Base64-decoded). [web:71][web:78]
    """
    data = _api_get(
        f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
        params={"ref": ref},
    )
    if isinstance(data, list):
        raise ValueError("Path is a directory, not a file")
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    # Fallback: some contents may be returned unencoded
    return data.get("content", "")


def simple_code_features(text: str) -> Dict[str, int]:
    """
    Very lightweight "learning" pass:
    - count def/class/import lines
    - future: plug into PhiLuca feature extractor
    """
    defs = classes = imports = 0
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("def "):
            defs += 1
        elif s.startswith("class "):
            classes += 1
        elif s.startswith("import ") or s.startswith("from "):
            imports += 1
    return {"defs": defs, "classes": classes, "imports": imports}


def learn_from_repo(owner: str, repo: str, branch: str = None, max_files: int = 500):
    """
    Stream-learn from up to max_files .py files without cloning.
    Writes a compact summary JSON into ~/welcome-to-the-god/ingest_data/REMOTE_LEARN/.
    """
    if branch is None:
        branch = get_default_branch(owner, repo)
    print(f"[LEARN] Remote repo {owner}/{repo}@{branch}")

    files = list_repo_files(owner, repo, branch)
    py_files = [f for f in files if f.get("type") == "blob" and f.get("path", "").endswith(".py")]
    py_files = py_files[:max_files]
    print(f"[LEARN] Found {len(py_files)} Python files (capped at {max_files}).")

    summary = {
        "owner": owner,
        "repo": repo,
        "branch": branch,
        "file_count": len(py_files),
        "files": [],
    }

    for i, meta in enumerate(py_files, 1):
        path = meta["path"]
        try:
            code = get_file_content(owner, repo, path, branch)
            feats = simple_code_features(code)
            summary["files"].append(
                {"path": path, "size": meta.get("size", 0), "features": feats}
            )
            if i % 25 == 0:
                print(f"[LEARN] Processed {i}/{len(py_files)} files...")
        except Exception as e:
            print(f"[WARN] Failed {path}: {e}")

    # Persist only summary, not code
    out_dir = Path("/data/data/com.termux/files/home/welcome-to-the-god/ingest_data/REMOTE_LEARN")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{owner}__{repo}__{branch}.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[LEARN] Summary written to {out_path}")
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            textwrap.dedent(
                """
                Usage:
                  deep_repo_learner.py OWNER REPO [BRANCH] [MAX_FILES]

                Example:
                  deep_repo_learner.py karpathy nanoGPT main 200
                """
            ).strip()
        )
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    branch = sys.argv[3] if len(sys.argv) > 3 else None
    max_files = int(sys.argv[4]) if len(sys.argv) > 4 else 500
    learn_from_repo(owner, repo, branch, max_files)
