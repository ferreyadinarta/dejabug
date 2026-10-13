# Reference: tldraw/tldraw#6191
Video: videos/tldraw_tldraw-6191.mov (9.2 s, Safari). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw (Vite demo, "Page 1") with one pink heart shape. Per the issue, the "w" key is bound to "rotate 45 degrees clockwise"; the rotations are key presses (no rotate handle is used).

## Actions (in order)
1. click @0:00.5 - the heart shape (selected, style panel shows "Shape")
2. key @0:01.0-0:03.0 - "w" pressed repeatedly (heart rotates 45 deg -> 90 -> 180 -> 270 -> back upright, in place)
3. drag @0:03.5-0:08.5 - press and hold on the heart and move it (translate); while holding, "w" is pressed several times (0:05.5, 0:06.0, 0:06.5, 0:07.0, 0:07.5) so the shape rotates during the drag; released around 0:08.5
   (counted as two reference actions: 3a drag/hold the heart, 3b key "w" during the drag)

## Bug moment
@0:05.5 - rotating while the heart is held makes it jump: it rotates around a different point and is translated far from the pointer (top-left at 0:06.0-0:07.0), instead of rotating in place under the cursor.
