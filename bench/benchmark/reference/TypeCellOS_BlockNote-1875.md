# Reference: TypeCellOS/BlockNote#1875
Video: videos/TypeCellOS_BlockNote-1875.webm (9.3 s; the first of two videos in the issue, the second is a Notion comparison and is not used). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website editor (dark theme). The mouse pointer is not visible; actions are inferred from caret, hover highlights and UI changes.
Start state: expanded toggle "dededede" with "Empty toggle. Click to add a block."; caret at end of "dededede".

## Actions (in order)
1. key @0:01.5 - Enter at the end of the expanded toggle "dededede" (a new sibling toggle "Toggle" appears below instead of a child block)
2. click @0:03.5-0:04.0 - "Empty toggle. Click to add a block." (an empty child paragraph "Enter text or type '/' for commands" appears)
3. click @0:05.0 - end of "dededede" (caret back in the toggle title)
4. key @0:05.5 - Enter (the toggle collapses and a second sibling "Toggle" appears)
5. click @0:07.0-0:07.5 - toggle arrow of "dededede" (expands: "Empty toggle. Click to add a block.")

## Bug moment
@0:01.5 - Enter on an unfolded toggle creates a new sibling toggle block instead of a block inside the toggle (again @0:05.5).
