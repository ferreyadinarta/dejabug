# Reference: tldraw/tldraw#11112
Video: videos/tldraw_tldraw-11112.mp4 (11.6 s, scripted recording with on-screen captions and a key badge). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw examples app, empty canvas, document with five pages. The pointer is visible; the "Esc" badge shows the key press.
Start state: page menu closed; captions read "Open the page menu".

## Actions (in order)
1. click @0:00.5-0:01.0 - page menu button "Page 1" (top left); menu opens: Page 1, Page 2, Page 3, Page 4, Page 5, "Create new page"
2. drag @0:02.0-0:04.0 - press on the "Page 2" row (tooltip "Go to page") and drag it down two rows; while held the list shows Page 1, Page 3, Page 4, Page 2, Page 5 (caption: Drag "Page 2" down to reorder it)
3. key @0:04.5 - Escape while still holding the mouse button ("Esc" badge); the whole page menu closes (caption: Press Escape while still dragging)
   (unclear: the mouse release is not visible; it happens while the menu is closed, around 0:05.0)
4. click @0:06.0-0:06.5 - page menu button again; menu reopens with the rows still in the mid-drag layout (Page 1, Page 3, Page 4, gap, Page 2, Page 5)
5. hover @0:07.5-0:11.0 - pointer moved up and down over the list with no button held; the "Page 2" row follows the pointer (to the top at 0:07.5, below Page 3 at 0:08.0, bottom at 0:08.5, back up at 0:09.5-0:11.0)

## Bug moment
@0:06.5 - after Escape mid-drag, reopening the page menu shows the list still stuck in the drag state (Page 2 drawn at its dragged slot, other rows shifted); from 0:07.5 the Page 2 row follows the cursor with no button held (caption: "The list is stuck mid-drag").
