"""The browser that dejabug tests run in.

    from dejabug.harness import open_page

    with open_page("http://localhost:5173") as page:
        page.get_by_role("button", name="Apply").click()

Exit codes for a repro test (so tools can tell outcomes apart):
    1  the bug happened (the test's assertion failed)  -> reproduced
    2  setup error (couldn't reach the state in the video)
    0  the expected behaviour happened -> not reproduced / fixed

When DEJABUG_REPLAY_VIDEO is set, the run is recorded to that path with a
visible mouse pointer drawn into the page, so `dejabug verify` can watch the
replay the same way it watched the original video. DEJABUG_URL overrides the
URL, so one test can run against the buggy and the fixed build.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPRODUCED, SETUP_ERROR, NOT_REPRODUCED = 1, 2, 0

# Headless browsers draw no mouse pointer, so videos of them show no clicks.
# This draws one that follows real mouse events and pulses on mousedown.
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
    """Scripts click instantly; people move to a target, pause, then click. The
    pause makes the click visible on the replay video the way it is in a user's
    recording. Every click is also logged with its time and label, so verify
    knows exactly what the replay did instead of guessing from pixels."""
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
    with sync_playwright() as p:
        browser = p.chromium.launch(channel=os.environ.get("DEJABUG_BROWSER", "chrome"),
                                    slow_mo=slow_mo if record_to else 0)
        opts = {"viewport": {"width": width, "height": height}}
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
                    "".join(json.dumps(a, ensure_ascii=False) + "\n" for a in _ACTIONS))
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
