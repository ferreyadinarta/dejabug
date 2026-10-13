# Reference: TypeCellOS/BlockNote#2109
Video: videos/TypeCellOS_BlockNote-2109.webm (19.4 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website editor (dark theme, cropped to the editor). The mouse pointer is not visible; actions are inferred from hover handles, drop indicators and UI changes.
Start state: collapsed toggle "dede", check-list item "List" (placeholder), empty paragraph.

## Actions (in order)
1. click @0:01.5-0:02.0 - toggle arrow of "dede" (expands: "Empty toggle. Click to add a block.")
2. drag @0:03.5-0:09.0 - drag handle of the "List" check-list block, moved up over the empty toggle; the drop indicator only appears between blocks (below "Empty toggle..." at block level / above "dede"), never inside the toggle; the block ends where it started
3. click @0:10.0-0:10.5 - "Empty toggle. Click to add a block." (an empty child paragraph is created inside the toggle)
4. drag @0:11.0-0:17.0 - drag handle of "List" again, now dropped inside the toggle (indicator inside, under "dede"); "List" becomes a child of "dede"

## Bug moment
@0:04.5-0:09.0 - while dragging "List" over the empty toggle there is no drop target inside it (indicator only at block level). Primary: 0:05.0.
