# Reference: tldraw/tldraw#8942
Video: videos/tldraw_tldraw-8942.mp4 (7.1 s). Graded from 2 fps keyframes plus 10 fps crops around the cursor (0:00.0-0:01.5), before seeing dejabug output.
App: tldraw editor zoomed out to 5% (zoom menu "- 5% + <" and minimap bottom-left), a small cluster of shapes (a grey ellipse, a doodle, two small squares) near the top-left. The recording shows a blue ring on click and a "⌘" keystroke overlay while Cmd is held.
The zoom is done with Cmd + mouse wheel (inferred from the ⌘ overlay and the zoom level changing while the pointer stays still).

## Actions (in order)
1. click @0:00.4 - empty canvas below the shapes (blue click ring)
2. scroll @0:01.0-0:06.5 - mouse wheel with Cmd held, pointer still on the empty canvas: zoom flips between 5% and 6% (6% at 0:01.5, 0:02.5, 0:03.5; 5% at 0:02.0, 0:03.0, 0:04.0-0:06.5) as the user zooms out against the minimum and back in

## Bug moment
@0:02.0 - each time the zoom is clamped at the 5% minimum, the viewport still moves: the shape cluster jumps up and to the right (0:02.0, 0:03.0, 0:04.5, 0:05.5, 0:06.0) although the zoom no longer changes.
