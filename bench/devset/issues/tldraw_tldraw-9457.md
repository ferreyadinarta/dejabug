# Dragging a shape from the toolbar directly into a frame does not reparent it to the frame

🗣️: when creating a shape over a frame the shape is reparented to this frame but when dragging a new shape from the toolbox to a frame does not reparent to the frame if there is no gap from the toolbox to the frame, dragging fast will just never register to the canvas page first and then we're not parenting to the frame, we have to go away from the frame and back into it if we want to be in a state where the frame will encapsulate the shape

---

Creating a shape directly over a frame correctly reparents that shape into the frame. But dragging a new shape out of the toolbar straight onto a frame does not: if the drag path goes from the toolbar into the frame without ever passing over the empty page area first, the shape stays parented to the page instead of the frame. This happens when the frame sits directly under the toolbar — either under the toolbar row itself or under the opened "more shapes" popup — so the pointer crosses from UI straight into the frame with no empty page in between. The reparent only registers once the pointer "visits" the empty page before entering the frame, so introducing a gap (panning the canvas so there's space between the toolbar and the frame, or dragging out of the frame and back in) makes it work. It reproduces with any shape (e.g. geo shapes) and on tldraw.com, so it's an SDK-level problem that affects everywhere frames are used. The expected behavior is that the shape ends up parented to the frame regardless of the drag path.

https://github.com/user-attachments/assets/0ec3c8fd-1f6e-4068-bcb7-1731a69124a2

## Open questions

1. **Which app(s) did you see this in — the examples app, tldraw.com, or both?**
   Seen on tldraw.com. Because it reproduces there, it's an SDK-level bug expected to occur everywhere frames are used.
2. **When it fails, what is the shape's end state?**
   The shape ends up parented to the page, overlapping the frame but not encapsulated by it. Reparenting only happens after the pointer first passes over the empty page, then re-enters the frame.
3. **Which shape/tool from the toolbar reproduces it, and does it happen for all draggable-from-toolbar items or a specific one?**
   Any shape reproduces it (e.g. geo shapes) — it's general to the drag-from-toolbar interaction. The trigger is spatial: the frame sits somewhat under the toolbar, either under the toolbar row itself or under the opened "more shapes" popup, so the drag goes from UI straight into the frame with no empty page in between.

Confidence: 88%, ready to get started.
