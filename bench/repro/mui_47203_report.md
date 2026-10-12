# mui_material-ui-47203: repro report

## Inferred steps
1. Click the "Checkboxes" multiple Autocomplete input. The popup opens (0.0s).
2. Click the input again, which closes the popup (0.3s: the list is gone and the "Limit tags" demo shows).
3. Click the input again to reopen the popup (1.1s).
4. Scroll the listbox down with the wheel until "Inception" is visible (3.4s `content_replaced`, 3.8s frame).
5. Click "Inception" (3.8s frame: hand cursor on the Inception row).

## Inferred bug
- Observed: after you select an option in the reopened popup, the listbox jumps back to the top. At 4.3s the Inception chip has appeared, but the list shows "The Shawshank Redemption…" again.
- Expected: the popup stays open (disableCloseOnSelect) at the same scroll position, so you can keep checking nearby options.
- Live finding: the reset happens only after the popup has been closed and reopened. On the first open, the scroll position is kept (scrollTop 480 -> 480). After a close/reopen, it resets (480 -> 0). The close/reopen at 0.3s and 1.1s in the video turned out to be a required step, not noise.

## Evidence used
- events.jsonl: the 0.3s `panel_closed` and 1.1s `panel_opened` showed the popup toggling. The 3.4s `content_replaced` showed the scroll. The 4.3s `text_appeared "Inception & Favorites"` together with `content_replaced` (after = Shawshank…) was the bug.
- Keyframes 0000.3s (popup closed, I-beam on the input), 0003.8s (hovering Inception, scrolled), 0004.3s (chip added, list back at top).

## Test output (bench/repro/mui_47203_test.py, exit 1)
```
listbox scrollTop before click: 480, Inception in view: True
chip 'Inception' count: 1, aria-selected: true
listbox scrollTop after click: 0, Inception in view: False, first visible option: 'The Shawshank Redemption'
ASSERTION FAILED: selecting an option reset the listbox scroll position (scrollTop 480 -> 0; first visible option now 'The Shawshank Redemption'); expected the list to stay scrolled with 'Inception' visible.
```
Iterations: 2 test runs plus 1 exploration script. The first test skipped the close/reopen and PASSED, so the bug did not show. Adding the close/reopen made it fail on the bug assertion.

## Confusing or missing evidence
1. **The real clicks were not logged.** No click event was emitted for the click on Inception (3.8s to 4.3s) or for the clicks on the input that toggled the popup (0.0s to 1.1s). These were the essential steps.
2. **The cursor track follows the text caret.** The track sits at (286,145) and (448,145), which is the blinking caret in the input, not the mouse. That produced a bogus `click` at 5.7s labelled "Inception & Favorites", and the track keeps jumping between the mouse and the caret.
3. **No event for the cause.** The popup toggling was reported as generic `panel_opened`/`panel_closed` with the other demo's texts ("Limit tags", "Show code"). Nothing said "dropdown closed / reopened by clicking the input", so it looked like noise. Labelling it as a dropdown close/open on the focused field would help.
4. **A false `text_changed`.** The 8.3s event "Part II" -> "Part lI" is an OCR flicker, not a UI change. The "Inception & Favorites" merge (chip plus placeholder) is also slightly confusing.
5. **The scroll had no label.** The scroll was only implied by `content_replaced`. An explicit "list scrolled down/up" event, with direction, would make the reset at 4.3s obviously the anomaly.
