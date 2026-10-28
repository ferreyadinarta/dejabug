# Reference: ueberdosis/tiptap#6906
Video: videos/ueberdosis_tiptap-6906.mp4 (19.1 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tiptap docs "BulletList extension" page, React demo with buttons "Toggle bullet list / Split list item / Sink list item / Lift list item".
Key presses are not visible; they are inferred from the caret and the list changing.
Start state: bullet list "A list item" / "Bug? -> im going to press DEL" (with nested "1234" > "testing", "wow", ":O" and "test") / "And another one".

## Actions (in order)
1. drag @0:02.0-0:02.5 - select "im going to press DEL"
2. click @0:03.5 - right of "DEL" at the end of the line "Bug? -> im going to press DEL" (selection collapses, caret at end of the line)
3. key @0:05.5-0:06.0 - Delete at the end of "Bug? -> im going to press DEL" (all nested items "1234", "testing", "wow", ":O", "test" vanish; caret lands at start of "And another one")
4. key @0:10.0 - Ctrl+A (all three remaining items highlighted) (unclear: could be a select-all via another gesture; pointer sits at the end of "And another one")
5. key @0:10.5 - Ctrl+Z (nested list restored, caret at end of "And another one") (inferred)
6. click @0:11.5 - end of "Bug? -> im going to press DEL"
7. key @0:13.5-0:14.0 - Delete again (nested items vanish again; caret at start of "And another one")

## Bug moment
@0:06.0 - pressing Delete at the end of "Bug? -> im going to press DEL" deletes the whole nested sub-list instead of lifting its items up (again @0:14.0).
