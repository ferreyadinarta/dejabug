# Reference: TypeCellOS/BlockNote#2330
Video: videos/TypeCellOS_BlockNote-2330.mov (13.0 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote homepage hero ("The open source Block-Based rich text editor") with the empty "Try it out here!" editor on the right.
Copy keystrokes (Cmd+C) have no visible effect and are not listed; pastes are listed because the text changes. Typed markdown shortcuts are inferred from the block type changing.
Start state: empty editor showing "Enter text or type '/' for commands".

## Actions (in order)
1. drag @0:00.5-0:01.0 - select "Easily add an e" in the hero text "...Easily add an editor to your..." (outside the editor)
2. click @0:01.5 - inside the empty editor (caret in the first block)
3. type @0:02.5-0:03.0 - "[] " (the block becomes a checklist item with placeholder "List") (unclear: the caret then shows on a new empty paragraph below it)
4. click @0:04.5 - the empty checklist item ("List" placeholder)
5. paste @0:05.0 - "Easily add an e" into the empty checklist item (checkbox disappears; it becomes a plain paragraph)
6. click @0:06.0 - empty area below "Easily add an e" (caret in a new empty paragraph)
7. type @0:06.5-0:07.0 - "1. " (numbered list item "1. List")
8. paste @0:08.0 - "Easily add an e" into the empty numbered item (number disappears; plain paragraph)
9. click @0:08.5-0:09.0 - empty area below (caret in a new empty paragraph)
10. type @0:10.0 - "- " (bullet list item "List") (unclear: exact keystroke not visible)
11. paste @0:10.5 - "Easily add an e" into the empty bullet item (bullet disappears; plain paragraph)

## Bug moment
@0:05.0 - pasting text into an empty checklist item turns the block into a plain paragraph instead of keeping it a list item (again @0:08.0 for the numbered item and @0:10.5 for the bullet item).
