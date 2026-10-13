# Reference: tldraw/tldraw#9392
Video: videos/tldraw_tldraw-9392.mov (65.7 s). Graded from 1 fps keyframes, before seeing dejabug output.
App: tldraw dev app (debug state shown bottom-left: "select.idle", "select.resizing", "select.translating", "select.crop.idle" ...). Canvas: a group made of an empty rectangle and a small image cropped to the purple/blue corner of a gradient image, a large copy of the gradient image below (with two outlined rectangles marking regions), style panel on the right.
The video is long and repetitive (many drag-resizes of the group); repeated flips are grouped into one action each.

## Actions (in order)
1. click @0:01.0 - the cropped image (the whole group is selected, dashed group box)
2. drag @0:01.0-0:02.0 - the group slightly up
3. double-click @0:04.0 - the cropped image (crop mode: "select.crop.idle", crop slider / fit / check toolbar)
4. key @0:05.0 - leave crop mode (Escape; inferred; group selected again)
5. click @0:06.0 - the cropped image (image selected inside the group, image toolbar)
6. click @0:07.0 - empty canvas (deselect)
7. drag @0:08.0 - the cropped image to the right with a modifier, making a copy outside the group ("select.translating"; inferred Alt-drag duplicate)
8. drag @0:14.0-0:17.0 - the copy's corner resize handle across the shape and back (flipping the lone copy; it keeps showing the right part of the image)
9. click @0:19.0 - the group (rectangle + cropped image)
10. drag @0:22.0-0:25.0 - the group's bottom-left resize handle across to the other side and back ("select.resizing")
11. drag @0:27.0-0:28.0 - the group's top-right resize handle (group made smaller)
12. click @0:29.0 - the rectangle inside the group
13. drag @0:30.0-0:31.0 - the rectangle to the left (inside the group)
14. drag @0:33.0-0:36.0 - the rectangle up and to the left, so it sits above-left of the image (group box grows)
15. drag @0:37.0-0:40.0 - the group's bottom-left resize handle up and to the right past the opposite corner (flipping the group); at 0:38.0 the cropped image shows a yellow/pink area instead of the purple corner
16. drag @0:42.0-0:43.0 - resize the group again (flip back)
17. double-click @0:45.0-0:46.0 - the cropped image, then drag inside it to move the crop ("select.crop.translating_crop"), click empty canvas (0:47.0)
18. click @0:48.0 - the group
19. drag @0:49.0-0:51.0 - the group's top-right resize handle across to flip it (image shows pink/yellow again at 0:49.0)
20. drag @0:52.0-0:57.0 - the group and nearby shapes around over the large image (translating)
21. drag @0:58.0-0:63.0 - the group's corner resize handle back and forth across the group several times (flipped image shows the wrong yellow/pink area at 0:61.0 and 0:63.0)
22. click @0:64.0 - the group (back in its original, unflipped orientation)

## Bug moment
@0:38.0 - flipping the group (dragging a corner handle across) shows the wrong part of the cropped image inside its crop (yellow/pink area instead of the mirrored purple corner); repeats at 0:49.0, 0:61.0, 0:63.0.
