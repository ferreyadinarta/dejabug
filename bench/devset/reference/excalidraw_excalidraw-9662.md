# Reference: excalidraw/excalidraw#9662
Video: videos/excalidraw_excalidraw-9662.mov (21.3 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Excalidraw, recording cropped to the canvas (no toolbar or properties panel visible). An ellipse with the bound text "- client" in its upper left.
Tool and alignment changes are made with controls outside the crop or the keyboard; the ones marked "inferred" are read from their effect. The text moving to the top (0:13.5) and then to the left (0:14.0) of the new rectangle is done with no visible input and is not listed.

## Actions (in order)
1. click @0:01.0 - the ellipse (selected)
2. key @0:01.5-0:02.0 - shape switch (inferred, Tab): the popup □ ◇ ○ appears under the shape, then the ellipse becomes a rectangle with very round corners, "- client" moves to its top-left corner
3. double-click @0:03.0-0:03.5 - the "- client" text (text editor, text selected)
4. click @0:04.5 - empty canvas above the shape (text editing ends)
5. key @0:05.0 - rectangle tool (inferred, R; crosshair cursor)
6. drag @0:06.0-0:08.0 - draw a new rectangle from the switched shape's top-left corner to its bottom-right corner, same size; its corners are much less round
7. double-click @0:09.0-0:09.5 - inside the new rectangle (inferred; a text caret appears at its centre)
8. type @0:10.5-0:12.0 - "- client"
9. key @0:12.5 - leave text editing (inferred, Escape; text centred in the new rectangle)
10. click @0:15.0 - the new rectangle (selected)
11. drag @0:15.5-0:16.5 - the new rectangle down, so both shapes can be compared
12. click @0:17.5 - the top edge of the switched shape (selected)
13. key @0:18.5 - Delete (inferred; the switched shape is removed)
14. drag @0:19.5-0:20.0 - the new rectangle up into the old place (selected until the end)

## Bug moment
@0:02.0 - switching the ellipse to a rectangle gives a rectangle with far rounder corners than a normal rounded rectangle of the same size; the difference is clearest when the new rectangle is drawn over it (0:07.5-0:08.0) and when the two are side by side (0:16.0-0:18.0).
