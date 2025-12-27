#!/usr/bin/env python3
import yt_dlp
import time
from pathlib import Path

STREAMS = {
    "nasa_iss": "https://www.youtube.com/watch?v=EEIk7gwjgIM",
    "seti_live": "https://www.youtube.com/@SETIInstitute/live",
    "meteor_cam": "https://www.youtube.com/watch?v=example_meteor"
}

DEST = Path("~/AETHER-MASTER/welcome-to-the-god/ingest_data/YOUTUBE_MEDIA").expanduser()
DEST.mkdir(exist_ok=True)

def capture_stream(url):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': str(DEST / '%(title)s.%(ext)s'),
        'download_archive': str(DEST / 'archive.txt'),
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    while True:
        for name, url in STREAMS.items():
            print(f"🌌 Capturing {name}")
            capture_stream(url)
        time.sleep(3600)
