# Reference: TypeCellOS/BlockNote#2568
Video: videos/TypeCellOS_BlockNote-2568.webm (14.3 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website demo ("Try BlockNote", blocknotejs.org/demo#ga648), image block with a cat picture, image toolbar shown above it.
Key presses (Enter) are not visible; they are inferred from the title of the issue and from the caption under the image updating. The pointer hides while typing.
Start state: image block selected (blue outline); the caption input popover under the toolbar is open with "Shit it's lost" and the caret at its end; the caption under the image reads "Shit it's lost".

## Actions (in order)
1. type @0:05.0-0:09.0 - " I'm hitting enter" at the end of the caption input (input reads "Shit it's lost I'm hitting enter")
2. key @0:09.5 - Enter in the caption input; the caption under the image updates to "Shit it's lost I'm hitting enter" but the input popover stays open (unclear: the Enter itself is not visible, and it may have been pressed more than once between 0:09.5 and 0:11.5)
3. click @0:11.5-0:12.0 - empty editor area to the right of the image; the caption input popover closes

## Bug moment
@0:09.5-0:11.5 - Enter is pressed in the caption input but the input does not close; it only closes after clicking outside at 0:12.0.
