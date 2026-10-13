# Reference: tldraw/tldraw#9457
Video: videos/tldraw_tldraw-9457.mov (9.5 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw canvas with one empty frame labelled "Frame" just above the bottom toolbar (hand, draw, eraser, arrow, text, note, image, rectangle, "^" more-shapes button). The "more shapes" popup opens over the frame, so a shape dragged out of it lands on the frame directly.

## Actions (in order)
1. click @0:01.0 - "^" (more shapes) button at the right end of the toolbar (shape popup opens over the frame, 0:01.5)
2. drag @0:01.5-0:06.0 - the rectangle tool from the popup straight onto the frame (0:02.0-0:02.5; the frame does not highlight), on out past the frame's right edge (0:03.0-0:03.5), back into the frame (0:04.0-0:04.5; now the frame highlights blue), and out to the right again; dropped half outside the frame on its right (0:06.0)
3. click @0:06.0 - "^" (more shapes) again (popup opens, 0:06.5)
4. drag @0:07.0-0:08.0 - the rectangle tool from the popup directly into the top-left of the frame and release there (the frame never highlights)
5. hover @0:08.0-0:09.0 - over the new rectangle inside the frame

## Bug moment
@0:08.0 - the rectangle dropped inside the frame is not reparented to it: the frame never highlighted during the drag and the rectangle is drawn over the frame's top edge (not clipped by the frame). Reparenting only happens when the pointer first passes over empty canvas (frame highlight at 0:04.0). First seen at 0:02.0 (no frame highlight while dragging straight from the popup into the frame).
