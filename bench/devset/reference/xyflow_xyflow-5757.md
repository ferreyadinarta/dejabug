# Reference: xyflow/xyflow#5757
Video: videos/xyflow_xyflow-5757.mov (6.7 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: React Flow in dark mode, nodes "React", "Flow", "your", "with", "ideas", "Wire" (selected, white border), each with a top and a bottom handle. A new node is created when a connection is dropped on the pane (add-node-on-edge-drop behaviour). The console, where the reporter logs `onPaneClick`, is not visible.
At 0:00.0 a connection drag from "Wire" is already in progress.

## Actions (in order)
1. drag @0:00.0-0:02.0 - a new connection from the top handle of "Wire" up to the bottom handle of "your", released on it (edge "your" - "Wire" created)
2. hover @0:02.0 - the "your" node (outline highlight)
3. drag @0:03.5-0:04.0 - a new connection from the top handle of "Wire" to the bottom handle of "with", released just below that handle (no further input until the end)

## Bug moment
@0:04.5 - the connection dropped at the "with" handle, with the pointer just off the node, counts as a drop on the pane: no edge to "with" is made and a new node, connected to "Wire", is created right under "with" instead (it shows the label "!" at 0:06.0). In the reporter's app the same drop also fires `onPaneClick` (not visible in the video).
