# Reference: tldraw/tldraw#9223
Video: videos/tldraw_tldraw-9223.mov (11.7 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw editor, zoomed in on a black, unfilled rectangle (draw style, size M) with the style panel open on the right: colour swatches (black, grey, light violet, violet / blue, light blue, orange, dark orange / dark green, green, light red, red), opacity slider, fill row, dash row (draw, dashed, dotted, solid), size row S / M / L / XL.
The recording shows a black ring around the cursor while the mouse button is held; drags are read from it.

## Actions (in order)
1. hover @0:00.5-0:01.0 - the blue and black colour swatches
2. drag @0:01.5-0:03.0 - scrub from the grey swatch down across the colours to dark green, then out of the panel onto the canvas, release next to the rectangle (nothing selected; dark green becomes the highlighted colour)
3. click @0:03.5 - the rectangle (selected)
4. drag @0:04.5-0:08.5 - scrub in the colour section with the button held: black (0:04.5), green (0:05.0, rectangle turns green), light red (0:05.5), dark orange (0:06.0), orange (0:06.5), then down out of the colour section (rectangle back to light red, 0:07.0), across the dash row and release over "dotted" (0:08.0-0:08.5)
5. hover @0:10.0-0:11.0 - over the rectangle

## Bug moment
@0:09.0 - after releasing the colour scrub over the dash row, the rectangle switches to the dotted dash style ("dotted" highlighted in the panel). Releasing over another style section should not select that style.
