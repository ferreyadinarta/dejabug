# Reference: ueberdosis/tiptap#5472
Video: videos/ueberdosis_tiptap-5472.mov (15.8 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Tiptap docs code-block demo (React/Vue tabs, "Toggle code block" / "Set code block" buttons). The pointer is mostly hidden while typing; keys are inferred from caret moves and text changes.
Start state: a code block with "asdasdasd" is the only content.

## Actions (in order)
1. key @0:01.0 - select all + Backspace/Delete (code block content and the block removed; empty paragraph)
2. click @0:02.5 - empty editor area (caret moves)
3. type @0:04.5-0:05.0 - "```" (markdown shortcut turns the line into a code block)
4. type @0:06.0-0:06.5 - "hello" inside the code block
5. key @0:07.0-0:09.0 - ArrowLeft/Home to the start of "hello", then ArrowUp (caret stays at the start of the code block)
6. type @0:09.5-0:11.0 - "can't go up" (inserted at the start: "can't go uphello")
7. click @0:12.5 - empty area below the code block (caret in a paragraph below; "Set code block" enabled)
8. hover @0:13.0 - "Toggle code block" button (hover tint)
9. click @0:13.5 - start of the code block text (caret back at the start of "can't go uphello")
10. key @0:14.0-0:15.5 - ArrowUp pressed again (caret stays; nothing created above)

## Bug moment
@0:08.0 - ArrowUp at the very start of the first-node code block does not exit it (no paragraph above, caret stays), which the user annotates by typing "can't go up" at 0:09.5; repeats 0:14.0-0:15.5.
