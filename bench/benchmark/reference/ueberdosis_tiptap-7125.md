# Reference: ueberdosis/tiptap#7125
Video: videos/ueberdosis_tiptap-7125.mp4 (13.3 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Tiptap default editor demo ("Hi there, this is a basic example of Tiptap...") with a height-limited editor and the menu bar (Bold ... Hard break, Undo, Redo). A keystroke visualiser shows the keys pressed.

## Actions (in order)
1. key @0:00.0 - Option+Space (visualiser shows "Option Space"; no visible change in the editor)
2. click @0:01.5-0:02.0 - empty line below the "- Mom" quote (caret in an empty paragraph; "Paragraph" button active)
3. key @0:03.0-0:09.0 - Shift+Enter pressed repeatedly (hard breaks; caret moves down until it reaches the bottom edge of the editor and goes out of view at ~0:06.5)
4. type @0:09.5-0:11.5 - "hello" (the editor finally scrolls so the caret line is visible)

## Bug moment
@0:06.5 - after Shift+Enter on the last visible line the caret moves below the visible area and the editor does not scroll (0:06.5-0:09.0 no caret visible); it only scrolls when typing starts at 0:09.5.
