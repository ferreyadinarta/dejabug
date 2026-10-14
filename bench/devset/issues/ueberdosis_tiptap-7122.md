# Details/Summary: collapses on type if no content precedes it

### Affected Packages

@tiptap/extension-details

### Version(s)

3.8.0

### Bug Description

When the Details block is the very first node in the document, clicking inside the content area keeps it open, but it collapses as soon as I type the first character. The caret then jumps to the extension’s title instead of staying where I typed.

https://github.com/user-attachments/assets/437c17f6-9b7e-4295-a24d-d6461b5467ff

### Browser Used

Chrome

### Code Example URL

https://tiptap.dev/docs/editor/extensions/nodes/details

### Expected Behavior

- Start with an empty document (no content before the Details block).
- Insert a Details block.
- Click inside the content area.
- Type any character.

### Additional Context (Optional)

_No response_

### Dependency Updates

- [x] Yes, I've updated all my dependencies.
