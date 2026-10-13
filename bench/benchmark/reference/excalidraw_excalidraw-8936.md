# Reference: excalidraw/excalidraw#8936
Video: videos/excalidraw_excalidraw-8936.mp4 (22.9 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: excalidraw.com (dark theme), empty canvas.

## Actions (in order)
1. double-click @0:00.5 - empty canvas centre (text editor opens: "Press Escape or Ctrl+Enter to finish editing")
2. type @0:01.0-0:02.0 - "asd lkasd aslkjd aslkj d"
3. scroll @0:02.5-0:04.5 - mouse wheel on the canvas so the text being edited moves down and out of view below the bottom edge
4. type @0:05.5-0:09.5 - more text " asdlkasj dlkasj dlkasj daslkjd aslkdj asdlkj" (while the editor is out of view)
5. scroll @0:10.0-0:13.0 - mouse wheel on the canvas, text moves back into view (UI returns to normal)
6. scroll @0:16.0-0:17.0 - mouse wheel again so the text goes below the bottom edge
7. type @0:18.0-0:21.5 - "  aslkdjaslkdj aslkdj aslkdj"

## Bug moment
@0:06.0 - typing while the text editor is scrolled out of view scrolls the whole app: toolbar, Share/Library and the top of the properties panel move up off-screen (again from 0:18.0 the whole UI disappears).
