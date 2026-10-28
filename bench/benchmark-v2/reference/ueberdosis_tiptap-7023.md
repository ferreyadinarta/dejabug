# Reference: ueberdosis/tiptap#7023
Video: videos/ueberdosis_tiptap-7023.mp4 (10.4 s, cropped to the editor). Graded from 2 fps keyframes, before seeing dejabug output.
App: Tiptap editor (CodeSandbox) with FileHandler and inline Image; heading "Try to paste or drop files into this editor". The image is a red YouTube-logo picture. Drag ghosts are visible; drops are inferred from the document changing.
Start state: heading plus an empty paragraph, no images.

## Actions (in order)
1. drag @0:01.0-0:02.0 - an image file dragged in from outside the editor (ghost with "+ Copy" badge) and dropped in the empty paragraph; one image inserted
2. drag @0:02.0-0:02.5 - (unclear: a second identical image appears directly below the first between two keyframes; most likely a short drag of the inserted image that left a copy, but the drag itself is not caught)
3. drag @0:03.0-0:03.5 - the second image dragged down one line and dropped; a third image appears, the earlier images stay in place
4. drag @0:04.0-0:05.0 - an image dragged up into the heading and dropped after "Try to"; a copy is inserted inline, splitting the heading ("Try to [image] paste or drop files into this editor"); the three images below remain
5. drag @0:05.5-0:06.5 - the inline image after "Try to" dragged into "paste or drop" and dropped between "dro" and "p"; another copy appears there, the original stays after "Try to"
6. drag @0:07.0-0:07.5 - the image between "dro" and "p" dragged to between "this" and "editor"; another copy appears, the original stays
7. scroll @0:08.5-0:09.0 - editor scrolled down (more duplicated images visible)

## Bug moment
@0:03.5 - dragging an image inside the editor drops a copy at the new position and leaves the original where it was (three images instead of two moved). Same at 0:05.0, 0:06.5 and 0:07.5 for the inline images in the heading.
