# Reference: radix-ui/primitives#3709
Video: videos/radix-ui_primitives-3709.mp4 (13.6 s). Graded from 2 fps keyframes plus 2 fps crops of the input row, before seeing dejabug output.
App: minimal Vite page (dark) with a Radix One-Time Password Field: four single-character inputs (placeholder "0") and a hidden input; Chrome DevTools Elements panel open on the right showing the inputs ("Character 1 of 4" ...) and the hidden input's value.
Key presses are read from focus and value changes; the pointer is off the input row while typing.

## Actions (in order)
1. hover @0:00.5 - the first input
2. click @0:01.0 - the first input (focused)
3. type @0:02.0-0:04.5 - "1" four times, focus moving one input to the right each time: "1" in input 1 (0:02.0), input 2 (0:03.0-0:03.5), input 3 (0:04.0), input 4 (0:04.5)
4. key @0:06.5 - a key press (not identifiable in the video) moves focus from input 4 to input 2; input 4 keeps "1"
5. click @0:08.0 - outside the inputs, below the row (no input focused; pointer shows below at 0:08.5)
6. click @0:09.0 - the first input (focused, empty)
7. click @0:10.5 - the second input (focused, empty)
8. hover @0:11.0-0:12.0 - along the third and fourth inputs, back to the second

## Bug moment
@0:03.0 - when the next "1" is typed and focus moves on, the previously entered digit disappears: after four digits only input 4 shows "1" (0:04.5) instead of "1 1 1 1". The keyboard move at 0:06.5 doesn't clear or step back one input as expected.
