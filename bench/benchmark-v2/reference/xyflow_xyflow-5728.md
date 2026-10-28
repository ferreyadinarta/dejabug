# Reference: xyflow/xyflow#5728
Video: videos/xyflow_xyflow-5728.mp4 (26.1 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: React Flow canvas (dotted background) with one selected node "resize me" (NodeResizer: blue outline, four corner handles, a connection handle on its left side). A pink box (x ~303-653 px, y ~245-345 px in the frame) marks the node's `extent`. The pointer is visible (grab hand over the node, resize arrows over its edges).
Start state: the node sits inside the pink extent at x ~379-560 px, pointer on the node.

## Actions (in order)
1. drag @0:00.0-0:04.0 - the body of the "resize me" node, moved right, left, down and back (it stops at the pink extent's edges each time) (unclear: the pointer crosses the top edge with a resize cursor at 0:02.0, so this may be two separate drags, 0:00.0-0:01.5 and 0:02.5-0:04.0)
2. drag @0:05.0-0:09.0 - the right edge resize handle of the node (resize cursor at 0:05.0), first pulled a little left (node narrower at 0:05.5), then right to the extent's right edge (0:06.0) and on past it to ~890 px (0:07.5-0:08.0), then back to ~638 px (0:09.0), where the node returns to x ~388-638 px
3. drag @0:09.5-0:12.0 - the node body again: left to the extent's left edge (0:10.0), right (0:11.0), then back (0:11.5-0:12.0)
4. drag @0:13.0-0:17.0 - the left edge resize handle (resize cursor at 0:13.0), pulled left past the extent's left edge and off the left side of the frame (0:16.5-0:17.0); released around 0:17.0-0:17.5
5. drag @0:18.0-0:18.5 - the pointer presses near the bottom edge of the oversized node and the node shifts down ~12 px (unclear: a drag of the node body or a bottom edge resize; the height does not change)
6. drag @0:21.0-0:23.5 - the left edge resize handle again, pulled right; the node shrinks back inside the extent (left edge from ~35 px to ~420 px)
7. drag @0:24.0-0:25.5 - the node body: left to the extent's left edge (0:24.5), right to its right edge (0:25.0), then left/up (0:25.5); the video ends with the pointer on the bottom edge (resize cursor)

Not counted: 0:04.5, 0:12.5 and 0:19.0-0:20.5 are pointer moves between drags (resize cursor over the bottom edge at 0:20.5).

## Bug moment
@0:06.5 - while the right edge handle is dragged past the pink extent, the node's right edge stops at the extent (~653 px) but the node keeps growing to the left instead, past the extent's left edge (left edge at ~330 px at 0:06.5, ~147 px at 0:08.0, extent starts at ~303 px): the NodeResizer does not respect `node.extent`. Repeated with the left handle @0:14.5-0:17.0 (the right edge jumps to the extent's right edge and the left edge goes to ~35 px), and the node stays oversized outside the extent after release (0:17.5-0:21.0).
