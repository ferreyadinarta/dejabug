# Reference: adobe/react-spectrum#9994
Video: videos/adobe_react-spectrum-9994.mp4 (24.7 s, Chrome Incognito, Windows). Graded from 2 fps keyframes, before seeing dejabug output.
App: StackBlitz project "rac-numberfield-issue" (App.tsx: `<NumberField minValue={0} aria-label="Count">` with Group, decrement Button "-", Input, increment Button "+"). The preview pane shows the NumberField; Chrome DevTools (Elements panel) is open on the right with the decrement `<button>` selected. A yellow circle marks each mouse click; in this demo a pressed button (`data-pressed`) is styled red.
Start state: value "0", the "-" button is disabled (light grey), pointer in the empty preview area.

## Actions (in order)
1. click @0:02.5-0:05.0 - the "+" (increment) button, clicked repeatedly (value 0 -> 2 at 0:03.0 -> 4 -> 7 -> 11 -> 12 at 0:05.0; the button flashes red while held at 0:04.5 and goes back to grey after each release)
2. click @0:06.0-0:09.5 - the "-" (decrement) button, clicked repeatedly (12 -> 11 at 0:07.0 -> 8 -> 6 -> 4 -> 2 -> 0 at 0:09.5; red while held at 0:08.5, grey again after release at 0:09.0)
3. hover @0:12.0-0:20.0 - DevTools Elements panel, over the selected decrement `<button>` node and its attributes (`disabled data-disabled="true" data-pressed="true"`); the page highlights the element with the tooltip "button#react-aria...-r_8_.react-aria-Button 42 x 42" (the pointer briefly passes over the `<input>` node at 0:12.5)
4. click @0:21.0 - empty area of the preview below the NumberField (the red background on "-" goes away at 0:21.5 and `data-pressed` disappears from the DOM)

Not counted: @0:10.5-0:11.5 the pointer moves off the "-" button into the empty preview, with no click.

## Bug moment
@0:09.5 - the last decrement takes the value to 0 and the "-" button becomes disabled, but it stays red (`data-pressed="true"` alongside `disabled`) after the mouse is released. The pointer is off the button from 0:10.5 and the state persists through 0:20.5. It clears only when the user clicks elsewhere on the page at 0:21.0.
