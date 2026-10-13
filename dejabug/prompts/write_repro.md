You are reproducing a bug from a screen recording. Your job: write a Playwright test that performs what the user did in the video and fails exactly where the user saw the bug.

## The evidence (already extracted from the video)

- `{evidence}/events.jsonl`: one line per meaningful moment. Types:
  - `start` (text on screen at the beginning)
  - `click` (`xy` + `label`: the text nearest to where the pointer rested before the screen changed), `hover` (the pointer rested on something but only a highlight changed)
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

## The test

dejabug already drafted `{test}` from the video: one line per user action, in order, with what happened on screen as comments. It uses the harness helpers `click(page, label)` and `hover(page, label)`, which find an element by its visible label.

- **Don't remove or reorder the drafted actions.** You may add steps the video implies but the draft misses (for example a list that opened or closed with no click before it means the user clicked something), and fix a step whose label doesn't match the page.
- Read the notes for steps the video implies: a list or menu already open at the very start was opened before recording began (open it first); a list that closes and opens again with no click in between means the user clicked the field to close and reopen it. Add those clicks.
- Lines marked TODO need you: a click on something without text (open the close-up image named in the comment), and the final check.
- Your check must be about something the video shows **changing for the worse** at the bug moment (a list jumping, a value resetting, an error appearing). Never assert on something that stayed the same throughout the video: that is how the app normally behaves, not the bug.
- At the end, measure the thing that went wrong, print the measured values, and return `REPRODUCED` (1) if the wrong behaviour happened, printing `ASSERTION FAILED: <what happened> ; expected <what should have happened>`; `NOT_REPRODUCED` (0) if the correct behaviour happened; `SETUP_ERROR` (2) if you couldn't reach the state in the video.
- Keep `open_page`: it records the replay that dejabug compares with the video.

## How to work

1. Read the events and look at the contact sheet. Write down, briefly: the user's steps, then what went wrong compared to what they expected.
   The bug is usually the surprising change right after the user acts: something jumps, resets, vanishes, or an error appears. Clicks after that are often the user retrying or reacting to it. `hover` events are the pointer resting on something, not clicks.
2. Run the draft, complete it, and run it again: `{python} {test}`
3. Iterate until the steps run cleanly and the failure comes from your assertion about the bug, not from a locator error or a timeout.
4. If after honest effort the app does not show the bug, keep the test asserting the correct behaviour and let it exit 0. Don't force a failure.

Finish with a short summary: the steps, the bug in one sentence, and the test's last output line.
