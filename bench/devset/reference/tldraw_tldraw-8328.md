# Reference: tldraw/tldraw#8328
Video: videos/tldraw_tldraw-8328.mp4 (5.6 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw editor, cropped to the top-left corner (main menu, "Page 1" page menu), canvas panned away from all shapes. At 0:00.0 the skip link "Move focus to canvas" is already shown with a blue focus ring under the page menu (focus reached it before the recording starts).
No click is visible: the cursor only moves onto the buttons; the button swap happens with the pointer resting on them.

## Actions (in order)
1. hover @0:00.5-0:02.5 - the focused "Move focus to canvas" button
2. hover @0:03.0-0:04.5 - "← Back to content", which now covers the same spot (the "Move focus to canvas" button's right edge "s" and focus ring stick out behind it)
3. hover @0:05.0 - pointer leaves; "Move focus to canvas" is shown alone again

## Bug moment
@0:03.0 - the "Back to content" helper button appears in the same top-left spot as the focused "Move focus to canvas" skip button and overlaps it; the two swap back and forth (flicker) between 0:00.0 and 0:05.0.
