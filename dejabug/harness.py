"""Browser for repro tests: records replays (DEJABUG_REPLAY_VIDEO) and swaps the URL (DEJABUG_URL)."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

REPRODUCED, SETUP_ERROR, NOT_REPRODUCED = 1, 2, 0

# headless browsers draw no pointer; draw one so replays show clicks
POINTER_JS = """
(() => {
  const install = () => {
    if (document.getElementById('__dejabug_pointer')) return;
    const p = document.createElement('div');
    p.id = '__dejabug_pointer';
    p.innerHTML = '<svg width="18" height="26" viewBox="0 0 18 26"><path d="M1 1 L1 20 L6 15 L10 24 L13 23 L9 14 L16 14 Z" fill="white" stroke="black" stroke-width="1.5"/></svg>';
    Object.assign(p.style, {position: 'fixed', left: '-40px', top: '-40px', width: '18px', height: '26px',
      zIndex: 2147483647, pointerEvents: 'none', transition: 'transform 60ms'});
    document.documentElement.appendChild(p);
    addEventListener('mousemove', e => { p.style.left = e.clientX + 'px'; p.style.top = e.clientY + 'px'; }, true);
    addEventListener('mousedown', () => { p.style.transform = 'scale(0.8)'; }, true);
    addEventListener('mouseup', () => { p.style.transform = ''; }, true);
  };
  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', install); else install();
})();
"""


_ACTIONS: list[dict] = []
_T0 = [0.0]


def _label(locator) -> str:
    """What a person would call the thing being clicked."""
    try:
        text = locator.evaluate(
            """el => el.getAttribute('aria-label')
                  || (el.labels && el.labels[0] && el.labels[0].innerText)
                  || el.innerText || el.value || el.getAttribute('placeholder') || ''""",
            timeout=500,
        ).strip()
    except Exception:
        text = ""
    return text.splitlines()[0][:80] if text else ""


def _human_clicks(pause_ms: int = 500) -> None:
    """Hover and pause before each click, and log it, so replays look like real recordings."""
    from playwright.sync_api import Locator

    if getattr(Locator, "_dejabug_patched", False):
        return
    for name in ("click", "dblclick", "check", "uncheck"):
        original = getattr(Locator, name)

        def wrapped(self, *args, _original=original, **kwargs):
            self.hover()
            self.page.wait_for_timeout(pause_ms)
            _ACTIONS.append({"t": round(time.monotonic() - _T0[0], 2), "type": "click", "label": _label(self)})
            return _original(self, *args, **kwargs)

        setattr(Locator, name, wrapped)
    Locator._dejabug_patched = True


@contextmanager
def open_page(url: str, width: int = 1280, height: int = 800, slow_mo: int = 120):
    url = os.environ.get("DEJABUG_URL", url)
    record_to = os.environ.get("DEJABUG_REPLAY_VIDEO")
    tmp = tempfile.mkdtemp(prefix="dejabug-") if record_to else None
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(channel=os.environ.get("DEJABUG_BROWSER", "chrome"),
                                    slow_mo=slow_mo if record_to else 0)
        opts = {"viewport": {"width": width, "height": height}}
        if os.environ.get("DEJABUG_STORAGE_STATE"):
            opts["storage_state"] = os.environ["DEJABUG_STORAGE_STATE"]  # start logged in
        if record_to:
            opts |= {"record_video_dir": tmp, "record_video_size": {"width": width, "height": height}}
        ctx = browser.new_context(**opts)
        _ACTIONS.clear()
        if record_to:
            ctx.add_init_script(POINTER_JS)
            _human_clicks()
        page: Page = ctx.new_page()
        _T0[0] = time.monotonic()  # the video's first frame is the new page
        page.goto(url)
        try:
            yield page
        finally:
            if record_to:
                page.wait_for_timeout(600)  # let the final state settle on video
            video = page.video
            ctx.close()
            browser.close()
            if record_to and video:
                Path(record_to).parent.mkdir(parents=True, exist_ok=True)
                shutil.move(video.path(), record_to)
                Path(record_to + ".actions.jsonl").write_text(
                    "".join(json.dumps(a, ensure_ascii=False) + "\n" for a in _ACTIONS), encoding="utf-8")
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)


ROLES = ("option", "button", "link", "menuitem", "tab", "checkbox", "radio", "combobox", "textbox", "switch")


def find(page: Page, label: str):
    """The visible element a person would call `label`."""
    candidates = [page.get_by_role(r, name=label, exact=True) for r in ROLES]
    candidates += [page.get_by_label(label, exact=True), page.get_by_placeholder(label, exact=True),
                   page.get_by_text(label, exact=True)]
    candidates += [page.get_by_role(r, name=label) for r in ROLES]
    candidates += [page.get_by_label(label), page.get_by_placeholder(label), page.get_by_text(label)]
    words = " ".join(label.split()[:2])
    if words and words != label:  # OCR often misreads the end of long labels
        candidates.append(page.get_by_text(words))
    for loc in candidates:
        try:
            if loc.count():
                return loc.first
        except Exception:
            continue
    raise LookupError(f'nothing on the page matches "{label}"')


def click(page: Page, label: str) -> None:
    find(page, label).click()


def hover(page: Page, label: str) -> None:
    find(page, label).hover()
