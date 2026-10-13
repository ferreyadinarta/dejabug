# Reference: tldraw/tldraw#9221
Video: videos/tldraw_tldraw-9221.mov (13.6 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw.com-style canvas, empty, with the bottom toolbar (Select, Hand, Draw, Eraser, Arrow, Text, Note, Image, Rectangle, "^") and quick actions (undo, redo, delete, duplicate, more). Eraser is the active tool at the start. Dragging a toolbar button onto the canvas drops a pen-drawn picture of that tool's icon.

## Actions (in order)
1. drag @0:01.0-0:03.0 - the "Select" (pointer) toolbar button up onto the canvas; during the drag the Draw (pencil) tool is highlighted (0:01.5-0:02.5); on release a pointer-shaped drawing is created and selected, and Select becomes active (0:03.0)
2. click @0:05.0 - the "Eraser" toolbar button (Eraser active)
3. drag @0:06.0-0:07.5 - the "Hand" toolbar button onto the canvas to the right of the pointer drawing; Draw is highlighted while dragging (0:06.5-0:07.0); on release a hand-shaped drawing is created and selected, Select active (0:07.5)
4. hover @0:08.0 - the delete (trash) quick action
5. click @0:08.5 - the "Hand" toolbar button (Hand active)
6. drag @0:09.5-0:11.0 - the "Hand" toolbar button onto the canvas again; Draw is highlighted while dragging (0:09.5-0:10.5); a second hand drawing is created and selected, Select active (0:11.0)
7. hover @0:12.0 - empty canvas

## Bug moment
@0:01.5 - while dragging a tool button (Select / Hand) out of the toolbar, the toolbar shows the Draw (pen) tool as selected; it switches back to Select only on release (again 0:06.5, 0:09.5).
