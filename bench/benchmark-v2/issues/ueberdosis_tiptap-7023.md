### Affected Packages

@tiptap/extension-file-handler

### Version(s)

3.6.1

### Bug Description

When `FileHandler` is enabled and `Image` is configured with `inline: true`, dragging an image within the editor does not move it.
Instead, the editor inserts a new copy of the image at the drop position while also leaving the original image in its old position.

### Browser Used

Chrome

### Code Example URL

https://codesandbox.io/p/sandbox/amazing-glade-fcp3qj

### Expected Behavior

The image should be moved to the new position.

### Additional Context (Optional)

https://github.com/user-attachments/assets/614865ff-a178-441e-ad91-997583a90023

### Dependency Updates

- [x] Yes, I've updated all my dependencies.