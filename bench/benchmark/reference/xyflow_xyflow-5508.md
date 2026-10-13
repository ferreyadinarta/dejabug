# Reference: xyflow/xyflow#5508
Video: videos/xyflow_xyflow-5508.mov (11.3 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: React Flow canvas with one node "Resize" (NodeResizer handles on all four sides, "..." menu), grid background.

## Actions (in order)
1. drag @0:01.0-0:06.0 - the body of the "Resize" node (grab cursor), moved up/left several times; it keeps snapping back inside its allowed area
2. drag @0:06.5-0:07.0 - the right-edge resize handle of the node, pulled to the right past the limit (resize refused, node keeps its width at 0:07.0)
3. drag @0:09.5-0:11.0 - the node body again (node selected/highlighted, grab cursor)

## Bug moment
@0:08.0 - after the refused resize the node outline is drawn much wider (to ~555 px) while its right resize handle stays at the old edge (~443 px): the rejected dimensions were applied to the rendered node. Visible until the end.
