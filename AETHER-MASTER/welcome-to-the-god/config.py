import os
from pathlib import Path
PROJECT_ROOT = Path(".")
INGEST_ROOT = PROJECT_ROOT / "ingest_data"
CLOUD_REMOTE_MAP = {
    "onedrive_remote": {"source": "onedrive_remote:/", "target": INGEST_ROOT / "EXTERNAL_ONEDRIVE_DATA"},
    "google_drive_remote": {"source": "google_drive_remote:/", "target": INGEST_ROOT / "EXTERNAL_GDRIVE_DATA"},
    "google_photos_remote": {"source": "google_photos_remote:/", "target": INGEST_ROOT / "EXTERNAL_GPHOTOS_DATA"},
}
LEARN_EXTS = {".py", ".js", ".json", ".html", ".css", ".ts", ".md", ".txt", ".doc", ".docx", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
