"""Check what dejabug needs and print one exact fix for anything missing."""

from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

OK, MISSING, OPTIONAL = "ok", "missing", "optional"

CHROME_PATHS = {
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
    "win32": [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
    "linux": ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"],
}


def _has(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def _chrome() -> bool:
    paths = CHROME_PATHS.get(sys.platform, [])
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", "")
        paths = paths + [str(Path(local) / "Google/Chrome/Application/chrome.exe")]
    return any(Path(p).exists() for p in paths) or bool(shutil.which("google-chrome"))


def _playwright_chromium() -> bool:
    caches = [Path.home() / "Library/Caches/ms-playwright", Path.home() / ".cache/ms-playwright",
              Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"]
    return any(c.exists() and any(c.glob("chromium*")) for c in caches)


def _github() -> bool:
    try:
        urllib.request.urlopen(urllib.request.Request("https://api.github.com", method="HEAD"), timeout=8)
        return True
    except urllib.error.HTTPError:
        return True  # any reply (even "rate limited") means the network works
    except Exception:
        return False


def checks() -> list[tuple[str, str, str, str]]:
    """(area, status, what, fix) rows."""
    rows = []
    py_ok = sys.version_info >= (3, 12)
    rows.append(("steps", OK if py_ok else MISSING, f"Python {platform.python_version()}",
                 "" if py_ok else "install Python 3.12+ (or: uvx dejabug ... uses its own)"))
    ffmpeg_ok = _has("imageio_ffmpeg")
    rows.append(("steps", OK if ffmpeg_ok else MISSING, "video decoding (bundled ffmpeg)",
                 "" if ffmpeg_ok else "pip install --force-reinstall dejabug"))
    engine = "ocrmac" if sys.platform == "darwin" else "rapidocr"
    ocr_ok = _has(engine)
    rows.append(("steps", OK if ocr_ok else MISSING, f"OCR ({'Apple Vision' if engine == 'ocrmac' else 'RapidOCR'})",
                 "" if ocr_ok else f"pip install {engine}"))
    gh_ok = _github()
    rows.append(("steps", OK if gh_ok else OPTIONAL, "GitHub reachable (issue links)",
                 "" if gh_ok else "check your network; local video files still work"))
    model_ok = bool(shutil.which("claude") or os.environ.get("ANTHROPIC_API_KEY"))
    rows.append(("steps", OK if model_ok else MISSING, "model that writes the steps (Claude Code or ANTHROPIC_API_KEY)",
                 "" if model_ok else "install Claude Code (https://claude.com/claude-code) or set ANTHROPIC_API_KEY; "
                                     "without it only `steps --no-ai` works"))
    pw_ok = _has("playwright")
    rows.append(("run", OK if pw_ok else OPTIONAL, "Playwright (test mode)",
                 "" if pw_ok else "pip install 'dejabug[run]'"))
    browser_ok = _chrome() or _playwright_chromium()
    rows.append(("run", OK if browser_ok else OPTIONAL, "Chrome or Playwright Chromium (test mode)",
                 "" if browser_ok else "install Google Chrome, or run: python -m playwright install chromium "
                                       "and set DEJABUG_BROWSER=chromium"))
    claude_ok = bool(shutil.which("claude")) or bool(os.environ.get("DEJABUG_AGENT"))
    rows.append(("run", OK if claude_ok else OPTIONAL, "coding agent (test mode)",
                 "" if claude_ok else "install Claude Code: https://claude.com/claude-code"))
    return rows


def ready(rows, area: str) -> bool:
    """Every check in `area` passed, except the optional GitHub one (local files still work)."""
    return all(status == OK for a, status, what, _ in rows if a == area and "GitHub" not in what)


def main() -> int:
    rows = checks()
    mark = {OK: "✓", MISSING: "✗", OPTIONAL: "–"}
    for area, status, what, fix in rows:
        line = f"  {mark[status]} {what}"
        if fix:
            line += f"\n      fix: {fix}"
        print(f"[{area:5}]{line}")
    steps_ready = ready(rows, "steps")
    run_ready = steps_ready and ready(rows, "run")
    print(f"\nsteps mode: {'ready' if steps_ready else 'not ready'}   test mode: {'ready' if run_ready else 'not ready'}")
    return 0 if steps_ready else 1
