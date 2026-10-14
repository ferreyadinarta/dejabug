# More fills button in style panel doesn't select correctly

### What happened?

When clicking on the rightmost Fill button in the style panel, a side panel opens with more fill options. This has a bunch of confusing small UI bugs:
- By default the leftmost icon (Fill -- Pattern) in the side panel is selected, despite not being clicked by the user yet. This appears selected at the same time as the currently selected fill button.
- After selecting a side panel icon, the rightmost button shows no indication of being selected.
- The rightmost button can't be "scrubbed" onto.
- The rightmost button has no preview when being "scrubbed" off of, until the mouse pointer is released.

Semi-relatedly, the different fill styles have very strange naming - might be worth making a separate issue for that.

### How can we reproduce the bug?

https://github.com/user-attachments/assets/60b36ce1-d10e-4c58-baca-2b1f8480b8a7

### What browsers are you seeing the problem on?

Chrome

### Where did this happen?

tldraw SDK (@tldraw/tldraw npm package)
