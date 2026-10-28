### Affected Packages

extension-bullet-list

### Version(s)

2.0.0, 3.0.0

### Description of the Bug

Instead of moving up the items of the list, the items get deleted on pressing DEL.
The error occurs when the user presses DEL in the end of the first item of a bullet list that has this shape:

- Item 1
   -  Item 1.1
       - Item 1.1.1
       - Item 1.1.2
   - Item 1.2
- Item 2

We talked about it in slack @bdbch 
Video of the error:

https://github.com/user-attachments/assets/0828e5b9-a59d-41f5-9a79-4bc3a80f15e6

### Browser Used

Chrome

### Code Example (Preferred)

_No response_

### Expected Behavior

The items should move up instead of being deleted.

### Additional Context (Optional)

_No response_

### Dependency Updates

- [x] Yes, I've updated all my dependencies.