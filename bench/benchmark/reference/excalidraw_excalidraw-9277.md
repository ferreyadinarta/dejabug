# Reference: excalidraw/excalidraw#9277
Video: videos/excalidraw_excalidraw-9277.mp4 (38.3 s). Graded from 2 fps (0-8 s) and 1 fps (8-38 s) keyframes, before seeing dejabug output.
App: excalidraw.com (dark theme) with one text element "Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...". The pointer is tiny and mostly invisible; editing state is read from the hint line ("Double-click or press Enter to edit text" / "Press Escape or Ctrl+Enter to finish editing"), selection boxes and text highlight. Exit-editing actions are inferred.

## Actions (in order)
1. click @0:01.0 - the "Lorem ipsum..." text element (selected, properties panel opens)
2. double-click @0:02.0 - the text element (text editing starts)
3. drag @0:02.0-0:02.5 - from inside the edited text toward the right edge (text scrolls inside the canvas)
4. key @0:03.0 - leave editing (Escape or click on empty canvas; inferred)
5. click @0:03.5 - the text element (selected)
6. double-click @0:05.5 - the text element (editing, whole text highlighted)
7. drag @0:06.0-0:12.0 - from inside the text past the right edge of the window; the toolbar, menu and footer slide left/off-screen from 0:09.0
8. key @0:13.0 - leave editing (UI returns; "Scroll back to content" button shows; inferred)
9. click @0:15.0 - "Scroll back to content"
10. double-click @0:16.0 - the text element (editing, whole text highlighted)
11. drag @0:17.0-0:22.0 - from inside the text toward the bottom edge; the UI slides up/off-screen (0:18-0:22)
12. key @0:23.0 - leave editing (inferred)
13. click @0:24.0 - "Scroll back to content"
14. double-click @0:25.0 - the text element (editing, whole text highlighted)
15. drag @0:26.0-0:32.0 - from inside the text past the right edge; UI slides away again (0:29-0:32)
16. key @0:33.0 - leave editing (inferred)
17. scroll @0:34.0-0:37.0 - zoom out to 10% then back to 70% (Ctrl/Cmd + wheel; inferred from the zoom label)

## Bug moment
@0:09.0 - while dragging inside the edited text past the window edge, the whole Excalidraw UI (toolbar, Share/Library, menu, zoom footer) shifts out of place (again 0:18-0:22, 0:29-0:32). Primary: 0:09.0.
