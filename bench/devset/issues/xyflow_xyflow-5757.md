# `onPaneClick` is triggered when a connection finishes being dragged

### What platform were you using when you found the bug?

- React Flow / Svelte Flow version: 12.10.2
- Browser and version: Both chromium based and firefox


 

### Live code example

_No response_

### Describe the Bug

MWE: I have a simple React Flow flow with

```tsx
  const onPaneClick = useCallback(
    (evt: React.MouseEvent<Element, MouseEvent>) => {
      console.log('on pane click', evt);
    }, []);
```

Then `onPaneClick` is passed as `onPaneClick` to `<ReactFlow/>`.
When you drag a new connection (unfinished edge): 
- If you drop the connection on the background pane (shouldn't add an edge), then the `onPaneClick` event is fired
- If you drop the connection on a handle (should add a new edge by default and fire only `onConnect`): if the mouse cursor ends up being precisely above the node element,  `onPaneClick` is not fired (correct), but if you drop the mouse cursor next to the handle, but precisely on the pane and not on the node, then `onPaneClick` is fired (bug, incorrect behavior).

Attaching video


### Steps to reproduce the bug or issue

See above

### Expected behavior

`onPaneClick` is not fired when dragging connections

### Screenshots or Videos

https://github.com/user-attachments/assets/482f9081-bd36-4104-8423-0ecb25ec19b5

### Additional context

_No response_
