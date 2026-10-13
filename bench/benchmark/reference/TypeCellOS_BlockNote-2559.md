# Reference: TypeCellOS/BlockNote#2559
Video: videos/TypeCellOS_BlockNote-2559.mp4 (30.4 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Bolt-hosted demo page "BlockNote Editor Demo" (Main Editor + "Open Dialog Editor" button).

## Actions (in order)
1. drag @0:02.5-0:04.0 - drag handle of the 2nd paragraph ("This is a separate editor instance inside a dialog box...") in the Main Editor, dropped above "This is a rich text editor with support for multiple block types..."
2. click @0:05.0 - "Open Dialog Editor" button (dialog "Dialog Editor" opens)
3. hover @0:06-0:17 - left gutter / blocks of the Dialog Editor ("Heading" placeholders, "Dialog Editor Examples", "Task List" paragraphs): the side menu (+ and drag handle) shows only for some blocks
4. click @0:18.5 - first "Heading" placeholder line in the Dialog Editor
5. type @0:19.0-0:19.5 - "test"
6. drag @0:20.0-0:25.5 - drag handle of the "test" block, moved down over the dialog editor and back up; the block disappears on drop (0:26.0)
7. click @0:27.0 - dark close button at the top-right of the dialog (dialog closes)

## Bug moment
@0:21.0-0:25.5 - while dragging "test" over the parts of the dialog that overlap the main editor, no drop indicator is shown (it only appears near "Task List" at 0:22.5/0:23.0); the side menu is also missing for some hovered blocks between 0:06 and 0:17. Primary bug moment: 0:21.0 (drag without drop indicator).
