# Reference: TypeCellOS/BlockNote#2020
Video: videos/TypeCellOS_BlockNote-2020.webm (27.8 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote "toggleable blocks" custom-schema example (GitHub / StackBlitz header). The mouse pointer is not visible; actions are inferred from caret, hover highlights and UI changes.
Start state: "Welcome to this demo!", toggle "This is an example toggle" (expanded) with children "This is the first child of the toggle block." / "This is the second child of the toggle block.", then "Click the '>' icon to show/hide its children".

## Actions (in order)
1. click @0:01.5 - end of the toggle title "This is an example toggle" (caret placed)
2. key @0:03.0 - Enter (toggle collapses, an empty paragraph appears and the children are detached below it)
3. key @0:04.5 - undo (Cmd/Ctrl+Z; inferred, state restored)
4. key @0:05.0 - Backspace ("toggle" -> "toggl")
5. type @0:06.5 - "e"
6. key @0:07.0 - Enter (same broken result)
7. click @0:08.0-0:08.5 - toggle arrow of "This is an example toggle" (expands: "Empty toggle. Click to add a block.")
8. click @0:11.0 - inside "This is the first child of the toggle block."
9. drag @0:12.0-0:12.5 - text selection across the first and second child (formatting toolbar appears)
10. click @0:13.5-0:14.0 - toggle arrow (collapses; the children stay visible)
11. click @0:14.5 - toggle arrow (expands)
12. click @0:15.0 - end of the toggle title
13. key @0:15.5 - Enter (new empty block)
14. type @0:16.0-0:17.0 - "testing"
15. click @0:18.5 - end of the toggle title
16. key @0:19.5 - Enter (toggle collapses, "testing" is detached too)
17. click @0:21.5 - toggle arrow (expands: "Empty toggle. Click to add a block.")
18. click @0:22.0 - "Empty toggle. Click to add a block." (empty child block created)
19. type @0:25.0-0:26.5 - "Why??"

## Bug moment
@0:03.0 - pressing Enter on the toggle title collapses the toggle and pushes its children out (they are no longer inside the toggle; expanding later shows "Empty toggle"). Repeats @0:07.0 and @0:19.5.
