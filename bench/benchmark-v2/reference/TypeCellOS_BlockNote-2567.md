# Reference: TypeCellOS/BlockNote#2567
Video: videos/TypeCellOS_BlockNote-2567.webm (29.1 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website demo (blocknotejs.org/demo#ga648, "Try BlockNote"), light theme, with a COMMENTS sidebar.
Start state: the cat image block is selected (blue border) and its toolbar is visible (Edit caption, Replace image, Colors, Delete, Download, ..., alignment, Comment, AI); the image has no caption.

## Actions (in order)
1. click @0:01.0-0:01.5 - "Edit caption" button (first icon) in the image toolbar (an "Edit caption" input opens below the toolbar, focused)
2. type @0:03.0-0:12.5 - "Hey I hope I don't lose this if I click out"
3. click @0:15.5 - empty editor area to the right of the image (pointer moves there at 0:13.0-0:14.5; the caption input closes and no caption appears under the image)
4. click @0:17.0 - on the image (hand cursor, resize handles show; toolbar back at full opacity after fading at 0:16.5) (unclear: may only be a hover)
5. hover @0:18.0 - "Edit caption" button (tooltip "Edit caption")
6. click @0:19.0-0:19.5 - "Edit caption" (the input reopens empty, placeholder "Edit caption")
7. type @0:20.5-0:23.0 - "Shit it's lost"
8. key @0:24.0 - Enter (inferred: the caption "Shit it's lost" appears under the image while the input is still open)
9. click @0:25.5-0:26.0 - empty editor area to the right of the image (the caption input closes; the caption under the image stays)

## Bug moment
@0:15.5 - clicking outside the caption input closes it without saving: no caption appears under the image, and reopening it at 0:19.5 shows an empty input. Only Enter (0:24.0) saves a caption.
