You are reproducing a bug from a screen recording. Your job: write a Playwright test that performs what the user did in the video and fails exactly where the user saw the bug.

## The evidence (already extracted from the video)

- `{evidence}/events.jsonl`: one line per meaningful moment. Types:
  - `start` (text on screen at the beginning)
  - `click` (`xy` + `label`: the text nearest to where the pointer rested before the screen changed)
  - `type` (text typed into a field)
  - `text_changed`, `text_appeared`, `text_gone`
  - `panel_opened` / `panel_closed` (a list, menu or panel appearing or vanishing as one)
  - `content_replaced` (a list's rows changed at once: scrolled, filtered or re-sorted)
  - `scroll`, `nav`, `error_shown`, `ui_change`

  Coordinates are pixels in the extracted frames (videos wider than 1280 px are scaled down to 1280), not page coordinates.
- `{evidence}/contact_sheet.png`: every keyframe in one image, with timestamps. Look at it first.
- `{evidence}/keyframes/*.png`: full-size keyframes, named by time. Open the ones around anything confusing.
- `{evidence}/cursor.jsonl`: where the mouse pointer was over time.

The app from the video is running at {url}. You may open it and inspect the DOM.
{note}
{rules}

## What to write

Write `{test}`: a plain Python script with this shape.

```python
import sys
from dejabug.harness import open_page, REPRODUCED, SETUP_ERROR, NOT_REPRODUCED

URL = "{url}"

def main() -> int:
    with open_page(URL) as page:
        # 1. the user's steps, in order, with the video timestamps as comments
        # 2. measure the thing that went wrong (print the measured values)
        ...
    # Exit with:
    #   SETUP_ERROR     (2) if you could not reach the state shown in the video
    #   REPRODUCED      (1) if the wrong behaviour happened; print "ASSERTION FAILED: <what happened> ; expected <what should have happened>"
    #   NOT_REPRODUCED  (0) if the correct behaviour happened
    return ...

if __name__ == "__main__":
    sys.exit(main())
```

Rules for the test:
- Use `open_page` from `dejabug.harness`. Don't launch browsers yourself: the harness records the replay that dejabug compares with the video.
- Prefer robust locators (`get_by_role`, `get_by_text`, `get_by_label`) using the labels you see in the video.
- Reproduce the steps the video shows, including ones that look incidental (closing and reopening a menu, scrolling before clicking). Bugs often depend on them.
- The assertion must check the **correct** behaviour, so it fails while the bug exists and passes once the bug is fixed. Never assert the buggy behaviour.

## How to work

1. Read the events and look at the contact sheet. Write down, briefly: the user's steps, then what went wrong compared to what they expected.
2. Write the test, then run it: `{python} {test}`
3. Iterate until the steps run cleanly and the failure comes from your assertion about the bug, not from a locator error or a timeout.
4. If after honest effort the app does not show the bug, keep the test asserting the correct behaviour and let it exit 0. Don't force a failure.

Finish with a short summary: the steps, the bug in one sentence, and the test's last output line.
