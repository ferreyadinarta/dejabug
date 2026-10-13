"""Accept a video file or a GitHub issue link and return a local video path."""

from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from pathlib import Path

import imageio_ffmpeg

ISSUE = re.compile(r"https://github\.com/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)")
VIDEO_URL = re.compile(
    r"https://(?:github\.com/user-attachments/assets/[0-9a-f-]{36}"
    r"|user-images\.githubusercontent\.com/\S+?\.(?:mp4|mov|webm)"
    r"|\S+?\.(?:mp4|mov|webm))",
    re.IGNORECASE,
)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "dejabug", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def is_video(path: Path) -> bool:
    err = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return "Video:" in err


def resolve(arg: str, workdir: Path) -> tuple[Path, str]:
    """Return (local video, short name) for a file path or an issue link."""
    m = ISSUE.match(arg)
    if not m:
        path = Path(arg)
        if not path.exists():
            raise SystemExit(f"no such file: {arg}")
        return path, path.stem
    owner, repo, num = m.groups()
    name = f"{repo}-{num}"
    dest = workdir / name / "video.mp4"
    if dest.exists():
        return dest, name
    issue = json.loads(_get(f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"))
    urls = VIDEO_URL.findall(issue.get("body") or "")
    if not urls:
        raise SystemExit(f"no video found in {arg}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    for url in urls:
        dest.write_bytes(_get(url.rstrip(").,>")))
        if is_video(dest):
            return dest, name
    dest.unlink(missing_ok=True)
    raise SystemExit(f"links in {arg} didn't lead to a video")
