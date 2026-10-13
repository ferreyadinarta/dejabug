# Reference: excalidraw/excalidraw#9423
Video: videos/excalidraw_excalidraw-9423.mp4 (20.2 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Excalidraw (light theme) with a selected frame "Frame" containing a yellow and a black rounded rectangle; Properties panel open (Shape properties > Frame: X / Y / W / H).

## Actions (in order)
1. drag @0:00.0-0:00.5 - the frame by its "Frame" title (frame + rectangles move up; Y -1673 -> -1613)
2. drag @0:01.5-0:03.5 - the frame by its "Frame" title again, left/right (frame and both rectangles move together; X 14401 -> 14511 -> 14304 -> 14439)
3. drag @0:05.0-0:09.5 - scrub the "X" label in Properties > Shape properties (horizontal-resize cursor), left and right; X changes 14438 -> 14506 -> 14792 -> 14233 -> 13986 -> 14257 -> 14439
4. drag @0:10.0-0:16.5 - scrub the "Y" label the same way; Y changes -1663 -> -1829 -> -1948 -> -1670 -> -1501 -> -1817 -> -1950

## Bug moment
@0:06.0 - changing X via the Properties panel moves the frame but its two rectangles stay where they were (the frame slides over/away from them); same for Y from 0:11.0, ending with both rectangles outside the frame (0:14.0-0:19.5). Primary: 0:06.0.
