Write the steps to reproduce the bug shown in a screen recording, from evidence already extracted from the video.

## Evidence in {evidence}

- `film/*.jpg`: the recording every half second (every second for long videos), 4 frames per sheet with the time in the corner. A red box marks what changed since the previous frame; a yellow ring marks the mouse pointer when it was found. Frames where nothing changed are left out. Read every sheet, in order: this is where clicks, typing, keyboard actions and drags show up.
- `film/frames/<time>s.jpg`: the same frames at full size. Open one when you need to read small text, such as what was typed.
- `contact_sheet.png` and `keyframes/<time>s.png`: frames where the screen settled after a change.
- `events.jsonl`: what changed on screen, detected automatically. Treat it as hints, not truth: `click` events come from a pointer that rested before the screen changed and can be wrong; `hover` is the pointer resting with only a highlight changing; text from OCR can be misread.
- `clicks/<time>s.png`: close-ups of where each detected click happened (red circle).

## Reading the frames

- The pointer is often missing or tiny (many recorders hide it). Then read actions from their effects: the caret moving, a highlight, a menu opening.
- Text appearing at the caret is typing. A new line or block appearing with the caret moving into it is Enter. Text vanishing at the caret is Backspace or Delete.
- Formatting or structure changing with no click on a toolbar (bold, a heading, a list, undo) is usually a keyboard shortcut; say which key if you can tell, otherwise mark it uncertain.
- A blue selection highlight growing over text or items is a select (drag). One word highlighted at once is a double-click.
- Something moving along with the pointer, or a drop indicator line, is a drag. Name what was dragged and where it ended up.
- Menus that open at the pointer with no left-click before them are a right-click.
- Panning or content sliding with no scrollbar movement may be scroll or a drag on the canvas; use the pointer to decide.

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
