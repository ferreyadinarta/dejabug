Write the steps to reproduce the bug shown in a screen recording, from evidence already extracted from the video.

## Evidence in {evidence}

- `timeline/*.png`: one frame per second, in grids with timestamps. Read all of them, in order. This is where typing, dragging and keyboard actions show up.
- `contact_sheet.png` and `keyframes/<time>s.png`: frames where the screen settled after a change. Open keyframes to read small text.
- `events.jsonl`: what changed on screen, detected automatically. Treat it as hints, not truth: `click` events come from a pointer that rested before the screen changed and can be wrong; `hover` is the pointer resting with only a highlight changing; text from OCR can be misread.
- `clicks/<time>s.png`: close-ups of where each detected click happened (red circle).

## What to write

Save `{out}` as JSON:

```json
{{
  "steps": [
    {{"t": 2.2, "action": "click", "target": "Checkboxes field", "text": "", "evidence": "timeline 2s-3s: list opens", "uncertain": false}}
  ],
  "bug": {{"t": 8.1, "what": "after clicking Inception the list jumps back to the top"}}
}}
```

- `action` is one of: click, double_click, right_click, type, press (a key such as Enter, Backspace, Tab, Escape, or a shortcut like Cmd+B), paste, drag, select (selecting text or items by dragging), scroll, hover.
- `target` is what a person would call the thing acted on: a visible label, or a short description ("the second paragraph", "the red rectangle", "the toolbar's bold button").
- `text` is what was typed or pasted, or the key for `press`.
- One step per user action, in order. Typing a word is one `type` step, not one per letter.
- Only include an action you can see evidence for in the frames. If something changed and you can't tell which action caused it, add a step with your best guess and `"uncertain": true`, and say what you saw in `evidence`.
- Fewer correct steps beat many guessed ones. Don't pad.
- `bug` is the moment the user would point at as wrong, and what's wrong, in plain words.
{note}
Write only the JSON file, then reply with one line: how many steps and the bug moment.
