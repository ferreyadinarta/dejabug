# Reference: tldraw/tldraw#11113
Video: videos/tldraw_tldraw-11113.mp4 (15.3 s, scripted recording with on-screen captions and a key-press overlay). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw examples app at 200% zoom, empty canvas. Keys are read from the key overlay at the bottom; the pointer stays still in the lower left for most of the video.
Start state: select tool active, empty canvas.

## Actions (in order)
1. key @0:00.5 - "T" (text tool selected in the toolbar; caption "Text tool, then type "# Heading"")
2. click @0:01.0 - canvas (a text caret appears and the tool returns to select) (unclear: the pointer is not at the caret position; the click is inferred from the new text shape)
3. type @0:01.5-0:03.0 - "# Heading" (the "# " turns the line into a large heading "Heading")
4. key @0:04.5 - ArrowDown (caret moves onto an empty line below the heading; caption "↓ moves the caret onto it")
5. key @0:06.0 - Backspace (caret goes back to the end of "Heading"; caption "Backspace: the line comes straight back")
6. key @0:06.5 - ArrowDown (caret on the empty line again)
7. key @0:07.0 - Backspace
8. key @0:07.5 - ArrowDown (empty line still there)
9. key @0:08.0-0:08.5 - Backspace
10. key @0:08.5 - ArrowDown (empty line still there)
11. key @0:09.5 - ArrowUp
12. key @0:09.5 - End (caret at the end of "Heading"; caption "Delete at the end of the heading: same thing")
13. key @0:10.0 - Delete
14. key @0:10.5 - Delete
15. key @0:11.0 - Delete
16. key @0:11.0 - ArrowDown (caret on the empty line, which is still there)
17. key @0:12.0 - Escape (editing ends, shape selected; its bounds include the empty line below "Heading")

## Bug moment
@0:06.0-0:06.5 - Backspace on the empty line below the heading does not remove it: ArrowDown puts the caret back on the same empty line (again at 0:07.5, 0:08.5 and after three Deletes at 0:11.0). At 0:12.0, after Escape, the selection bounds are still a line taller than the heading.
