# Releasing mouse after scrubbing in style panel selects style in different section

### What happened?

Styles in the style panel (e.g. colour) can be "scrubbed" by clicking and dragging across the styles, which will select whichever style option is currently under the pointer. You cannot scrub across multiple style sections (e.g. start scrubbing colours, then drag over to border styles), which is intended behaviour.

However, if the drag is released when hovering over another style section, the style that the mouse pointer is released over is selected - even if it is a different style section.

### How can we reproduce the bug?

Note how in the recording below, the border style is selected upon mouse release, which should not happen.

https://github.com/user-attachments/assets/eeb96380-0e6e-4908-8636-a4e0dcbc0a81

### What browsers are you seeing the problem on?

Chrome

### Where did this happen?

tldraw SDK (@tldraw/tldraw npm package)
