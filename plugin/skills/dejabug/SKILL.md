---
name: dejabug
description: Reproduce a web-app bug from a screen recording (mp4, mov, webm, a Loom export, a video attached to an issue) as a Playwright test that fails the same way, verified against the video. Use when the user shares or mentions a bug video or screen recording and wants it reproduced, turned into a test or regression test, or debugged.
---

# dejabug: bug video → failing test

The user has a recording of a bug. You turn it into a Playwright test that performs what the user did and fails where they saw the bug. Then `dejabug verify` replays your test, watches the replay, and checks it walks through the same moments as the video. Only then is the bug reproduced.

## 0. Setup (once)

Check `dejabug --version`. If missing, install it:

```bash
uv tool install git+https://github.com/ferreyadinarta/dejabug
```

Tests run in Google Chrome by default. Without Chrome, set `DEJABUG_BROWSER=chromium` and run `uvx playwright install chromium`.

You also need the app from the video running locally. Get its URL from the user, or find the project's dev script and start it.

## 1. Watch the video

```bash
dejabug watch <video> -o dejabug-out/<name>
```

This writes, into the output folder:
- `contact_sheet.png`: every keyframe with timestamps. **Look at it first.**
- `events.jsonl`: one line per moment. Types:
  - `click` (`label` = text nearest the resting pointer)
  - `type`, `text_appeared`, `text_gone`, `text_changed`
  - `panel_opened` / `panel_closed` (a list or menu appearing or vanishing as one)
  - `content_replaced` (list rows changed at once: scrolled, filtered)
  - `scroll`, `nav`, `error_shown`

  Coordinates are pixels in the extracted frames (videos wider than 1280 px are scaled down to 1280).
- `keyframes/<time>s.png`: open any frame you need to see in full.

Write down the user's steps and the bug (what happened vs. what they expected) before writing code. The bug is usually the surprising change right after the user acts (something jumps, resets, vanishes, or an error appears); later clicks are often the user retrying. `hover` means the pointer rested on something without clicking. Steps that look incidental often matter: a menu closed and reopened, a scroll before a click, a second click.

## 2. Write the test

Save it as `dejabug-out/<name>/repro_test.py`:

```python
import sys
from dejabug.harness import open_page, REPRODUCED, SETUP_ERROR, NOT_REPRODUCED

URL = "http://localhost:3000"

def main() -> int:
    with open_page(URL) as page:
        # the user's steps, with video timestamps as comments
        # measure what went wrong; print the measured values
        ...
    # SETUP_ERROR (2): couldn't reach the state in the video
    # REPRODUCED  (1): wrong behaviour happened; print "ASSERTION FAILED: <what happened> ; expected <what should>"
    # NOT_REPRODUCED (0): correct behaviour happened
    return ...

if __name__ == "__main__":
    sys.exit(main())
```

- Always use `open_page`. It records the replay that verify compares with the video, and lets the URL be switched with `DEJABUG_URL`.
- Use the labels you saw in the video for locators (`get_by_role`, `get_by_text`, `get_by_label`).
- **Assert the correct behaviour**, so the test fails now and passes once the bug is fixed.

Run it with `dejabug test dejabug-out/<name>/repro_test.py` and iterate until it runs cleanly and fails on your assertion, not on a locator or a timeout. If the app doesn't show the bug, say so. Don't force a failure.

## 3. Verify against the video

```bash
dejabug verify dejabug-out/<name> dejabug-out/<name>/repro_test.py
```

| Verdict | Meaning | Next |
|---|---|---|
| `REPRODUCED` | the test fails and its replay walks through the video | done |
| `FAILS_DIFFERENTLY` | it fails, but the replay doesn't follow the video | read `verify/report.md`: ✗ lines are moments your replay missed. Add those steps |
| `SETUP_ERROR` | the test couldn't reach the video's state | fix the steps |
| `NOT_REPRODUCED` | the correct behaviour happened | the bug may need a step you skipped, other data, or it's already fixed |

`·` lines in the report are context: text from around the bug that the replay never shows. Ignore them.

## 4. Report

Show the user the steps, the bug in one sentence, the test path, and `verify/strip.png` (video frames beside replay frames). Then offer to fix the bug: the test is the proof the fix works, and it becomes a regression test.
