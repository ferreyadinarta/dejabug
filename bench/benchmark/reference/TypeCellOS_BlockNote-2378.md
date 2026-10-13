# Reference: TypeCellOS/BlockNote#2378
Video: videos/TypeCellOS_BlockNote-2378.webm (12.2 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote demo ("Welcome to BlockNote!"). The mouse pointer is not visible in the recording; actions are inferred from UI changes and hover highlights.
Start state: toggle block "Hello" expanded with children "Hi", "There", "dede"; caret at end of "Hello".

## Actions (in order)
1. click @0:01.5-0:02.0 - toggle arrow of "Hello" (collapses it; children hidden)
2. key @0:03.0-0:03.5 - Enter with caret at end of "Hello" (a new empty toggle block with placeholder "Toggle" appears below)
3. click @0:05.0-0:06.0 - toggle arrow of the new "Toggle" block (expands it)
4. click @0:07.5-0:08.0 - toggle arrow of "Hello" (expands it)

## Bug moment
@0:06.0 - the new toggle block, when expanded, contains "Hi", "There", "dede" (the first toggle's content moved); confirmed @0:08.0 when "Hello" shows "Empty toggle. Click to add a block."
