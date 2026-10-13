"""Run by action.yml: write steps for one issue's video and post them as a comment."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

MARKER = "<!-- dejabug -->"


def comment_body(steps_md: str, run_url: str) -> str:
    return (f"{MARKER}\n{steps_md.strip()}\n\n<sub>Written from the video by a model, so check before relying on it. "
            f"Steps marked \"not sure\" were inferred. [Run log]({run_url})</sub>\n")


def _api(path: str, data: dict | None = None) -> object:
    req = urllib.request.Request(f"https://api.github.com{path}", method="POST" if data else "GET",
                                 data=json.dumps(data).encode() if data else None,
                                 headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                                          "Accept": "application/vnd.github+json", "User-Agent": "dejabug"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main() -> int:
    repo, issue = os.environ["REPO"], os.environ["ISSUE"]
    if not issue:
        print("no issue number; nothing to do")
        return 0
    comments = _api(f"/repos/{repo}/issues/{issue}/comments?per_page=100")
    if any(MARKER in (c.get("body") or "") for c in comments):
        print("already commented on this issue")
        return 0
    out = Path("dejabug-out/action")
    run = subprocess.run([sys.executable, "-m", "dejabug.cli", "steps", f"https://github.com/{repo}/issues/{issue}",
                          "-o", str(out), "--ai", "--model", os.environ.get("MODEL") or "opus"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(run.stdout[-3000:], run.stderr[-3000:], sep="\n")
    if "no video found" in run.stderr or "didn't lead to a video" in run.stderr:
        print("no video in this issue")
        return 0
    steps = out / "steps.md"
    if run.returncode or not steps.exists():
        return 1
    body = comment_body(steps.read_text(encoding="utf-8"), os.environ.get("RUN_URL", ""))
    if os.environ.get("DRY_RUN"):
        print(body)
        return 0
    _api(f"/repos/{repo}/issues/{issue}/comments", {"body": body})
    print("commented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
