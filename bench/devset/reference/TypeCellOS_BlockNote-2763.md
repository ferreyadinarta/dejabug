# Reference: TypeCellOS/BlockNote#2763
Video: videos/TypeCellOS_BlockNote-2763.mp4 (21.5 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote docs, example "Comments with Sidebar": "Editor" (User: John Doe (Editor)) next to a "Comments" sidebar (Filter: Open, Sort: Position) that already lists older threads ("Original content deleted", John Doe May 10 / May 12); Chrome DevTools docked on the right. The live example syncs through a hosted Yjs room (that is where the older threads come from); the bug itself is in BlockNote's comment UI.
Clicks on the small reaction button are read from its hover tooltip and the picker opening; exact click counts are uncertain at 2 fps.

## Actions (in order)
1. click @0:00.5 - the empty editor (caret)
2. type @0:01.0 - "Test"
3. double-click @0:01.5 - "Test" (selected; formatting toolbar appears)
4. hover @0:02.5 - the toolbar's link button (tooltip "Create link Ctrl+K"), then the comment button next to it
5. click @0:03.0 - the toolbar's comment button ("Write a comment..." composer opens)
6. click @0:04.0 - in the "Write a comment..." field
7. type @0:04.5 - "Test"
8. click @0:05.0 - "Save" (new thread "Test" / John Doe May 20 / "Test" at the top of the sidebar; "Test" highlighted in the editor)
9. hover @0:06.0-0:06.5 - the new thread, then its top-right "Add reaction" button (tooltip)
10. click @0:07.0 - top-right "Add reaction" (emoji picker opens: Frequently used, Smileys & People ...)
11. scroll @0:08.0-0:08.5 - the page down a little
12. click @0:09.0 - the "Face Screaming in Fear" emoji (picker closes; reaction "😱 1" and a small "add reaction" button appear under the comment)
13. hover @0:10.0 - "Add comment..." under the thread
14. click @0:10.5-0:12.0 - the small add-reaction button under the comment (tooltip "Add reaction"), twice: nothing opens on the first click, the picker opens after the second (0:12.0)
15. scroll @0:13.0-0:13.5 - the comments sidebar, with the picker open
16. click @0:14.0 - an emoji in "Smileys & People" ("Grinning Squinting Face") (picker closes; no reaction added)
17. click @0:15.5-0:16.5 - the add-reaction button under the comment again, twice (picker opens at 0:16.5)
18. click @0:17.0 - an emoji / the "Smileys & People" area in the picker (picker closes; nothing added)
19. click @0:18.0-0:19.0 - the add-reaction button under the comment, twice (picker opens at 0:19.0)
20. click @0:19.0-0:19.5 - an emoji near "Smileys & People" (picker closes; nothing added)

## Bug moment
@0:14.5 - picking an emoji from the picker opened by the add-reaction button under the comment adds no reaction (the picker just closes); it repeats at 0:17.5 and 0:19.5. That button also needs two clicks before the picker opens (0:11.0). The top-right "Add reaction" button works (0:09.5).
