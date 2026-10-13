"""Accept a video file or a GitHub issue link and return a local video path."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
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
NO_ACCESS = ("GitHub didn't return {what} (HTTP {code}). Without a token GitHub allows 60 requests an hour per network.\n"
             "Fix: set GITHUB_TOKEN (or run `gh auth login`), or download the video and pass the file instead.")


def github_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and shutil.which("gh"):
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        token = r.stdout.strip() if r.returncode == 0 else None
    return token or None


def _get(url: str, token: str | None = None, api: bool = False) -> bytes:
    headers = {"User-Agent": "dejabug"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return r.read()


def issue_text(owner: str, repo: str, num: str, save: Path | None = None) -> str:
    """The issue body from the API, falling back to the issue's web page when the API refuses."""
    token = github_token()
    try:
        issue = json.loads(_get(f"https://api.github.com/repos/{owner}/{repo}/issues/{num}", token, api=True))
        body = issue.get("body") or ""
        if save:  # context for the model that writes steps
            save.parent.mkdir(parents=True, exist_ok=True)
            save.write_text(f"# {issue.get('title', '')}\n\n{body}", encoding="utf-8")
        return body
    except urllib.error.HTTPError as api_err:
        try:
            return _get(f"https://github.com/{owner}/{repo}/issues/{num}", token).decode("utf-8", "replace")
        except urllib.error.HTTPError:
            raise SystemExit(NO_ACCESS.format(what="the issue", code=api_err.code)) from None


def is_video(path: Path) -> bool:
    err = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stderr
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
    urls = list(dict.fromkeys(VIDEO_URL.findall(issue_text(owner, repo, num, dest.parent / "issue.md"))))
    if not urls:
        raise SystemExit(f"no video found in {arg}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    for url in urls:
        try:
            # no token here: attachments redirect to storage that rejects GitHub tokens
            dest.write_bytes(_get(url.rstrip(").,>\"'")))
        except urllib.error.HTTPError:
            continue
        if is_video(dest):
            return dest, name
    dest.unlink(missing_ok=True)
    raise SystemExit(f"links in {arg} didn't lead to a video")
