# Flipping group containing cropped image by drag resize shifts image position

### What happened?

This one's much easier to show than tell (please see below) - but in essence, if you have a cropped image within a group and flip/invert the group orientation by dragging the group's corner handles, the portion of the cropped image that is visible in the crop mask gets shifted/mirrored incorrectly.

### How can we reproduce the bug?

- Create/add an asymmterical image
- Crop to a corner of the image
- Add a shape off to the side (e.g. above and to the left) if the image
- Group the image and shape together
- Drag the group corner across to flip the group

See video demo below:

https://github.com/user-attachments/assets/d41b67d2-e3d8-4464-8251-a1d4682b3620

### What browsers are you seeing the problem on?

Chrome

### Where did this happen?

tldraw SDK (@tldraw/tldraw npm package)
