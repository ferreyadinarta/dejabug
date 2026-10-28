### What platform were you using when you found the bug?

- React Flow / Svelte Flow version: 12.10.1
- Browser and version: browsers tested (Arc 146.0.7680.76, Chrome 146, Safari 26.3.1 (21623.2.7.11.7))
- OS and version: MacOS 26.3.1

### Live code example

https://codesandbox.io/p/sandbox/broken-node-resizer-does-not-respect-node-extents-m5g8wv

### Describe the Bug

When using the node resizer on a node with the `extent` property set, the node is not bound by the extent value. 

### Steps to reproduce the bug or issue

1. Drag an edge of the node beyond the bounds of the node extent (I've annotated with the red box)
2. Ensure that the edge is dragged sufficiently beyond the node extent to fully see the issue.

### Expected behavior

As a user, I expect that the node resizer respects the extent of the node it is used with.

### Screenshots or Videos

https://github.com/user-attachments/assets/d31ab1f2-baac-4e81-b9ff-89e4650d98be

### Additional context

_No response_