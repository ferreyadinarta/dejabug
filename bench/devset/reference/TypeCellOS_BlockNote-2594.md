# Reference: TypeCellOS/BlockNote#2594
Video: videos/TypeCellOS_BlockNote-2594.mp4 (22.3 s). Graded from 2 fps keyframes (cropped to the editor) plus full frames at 15.0 s and 20.5 s.
App: blocknotejs.org docs, "PDF Export" page: "Editor Input" BlockNote editor with a multi-column layout (top: "test" | "Block 3" columns, then "Test" and "Test 1" in the left column), live "PDF Output" preview below, Chrome DevTools console open on the right.
The key presses are not visible; they are inferred from "Test 1" jumping between positions and from the console stack trace (moveBlocksUp / Shift-Mod-ArrowUp), i.e. Ctrl/Cmd+Shift+ArrowUp/ArrowDown. Each move also re-renders the PDF preview (black/blank flashes) and adds console errors.

## Actions (in order)
1. click @0:00.0 - end of the "Test 1" block (caret after "Test 1")
2. key @0:01.0 - Ctrl+Shift+ArrowUp (move block up): "Test 1" jumps into the right-hand column
3. key @0:01.5 - Ctrl+Shift+ArrowUp: "Test 1" goes back to the left column, under "Test"
4. key @0:03.0 - Ctrl+Shift+ArrowDown: "Test 1" moves back to the bottom of the left column
5. key @0:03.5-0:05.0 - Ctrl+Shift+ArrowDown/ArrowUp a few times: "Test 1" disappears from view (0:03.5), then reappears at the bottom (0:04.0-0:05.0)
6. key @0:05.5-0:06.5 - Ctrl+Shift+ArrowUp: "Test 1" moves up under "Test" (with an empty line between, then directly under, 0:06.0)
7. key @0:07.0 - Ctrl+Shift+ArrowDown: "Test 1" back at the bottom, an empty block now sits between "Test" and "Test 1"
8. hover @0:08.0 - side menu ("+" and drag handle) of the empty block between "Test" and "Test 1"
9. click @0:09.0 - "+" (add block) on that empty block; the slash menu opens ("Headings / Heading 1 ...", placeholder "Enter text or type '/' for commands")
10. scroll @0:10.0-0:11.5 - through the slash menu, hovering "Quote", "Code Block", "Table", "Two Columns"
11. key @0:12.0-0:12.5 - close the slash menu without choosing (Escape; inferred)
12. click @0:12.5 - end of "Test 1" (caret in "Test 1")
13. key @0:13.5-0:14.0 - Ctrl+Shift+ArrowUp: "Test 1" jumps into the right-hand column again; the page greys out with "Paused in debugger" (Paused on exception: "Error: Block with ID ... not found") at 0:14.5
14. click @0:20.5 - selects the console text "Uncaught Error: Block with ID b86a58c8-... not found" (stack: moveBlocksUp / Shift-Mod-ArrowUp)

## Bug moment
@0:01.0 - moving "Test 1" up with the keyboard makes it jump out of the left column into the right column instead of staying in the left column (again at 0:14.0), and the moves throw "Uncaught Error: Block with ID ... not found" (DevTools error count grows; debugger pauses on the exception at 0:14.5). Primary: 0:01.0.
