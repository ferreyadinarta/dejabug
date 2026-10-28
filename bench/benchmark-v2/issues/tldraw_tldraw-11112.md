🗣️: Pressing escape mid-drag when drag-reordering pages in a file causes it to be stuck in the drag state when next opening the dropdown of pages.

---

Reproduced in the examples app with five pages. While dragging a row in the page menu to reorder it, pressing Escape closes the whole menu but leaves the drag in progress. The next time the menu opens, the dragged row is still drawn at its mid-drag position, the other rows are still shifted around it, and the row follows the cursor on hover even though no button is held. The page order itself is not changed. Escape mid-drag should cancel only the drag: the dragged row snaps back to its original slot, the page menu stays open, and releasing the mouse afterwards doesn't reorder anything. Escape with no drag in progress still closes the menu as it does today.

Recording: open the page menu, drag "Page 2" down two rows, press Escape while still holding the mouse button, release, reopen the menu, then hover over the list.

https://github.com/user-attachments/assets/473fa5db-d028-41cd-9b18-dce5b3b9ebbd

## Open questions

1. **Should Escape mid-drag cancel only the drag and keep the page menu open, or cancel the drag and close the menu as it does today?**
   Cancel only the drag and keep the page menu open.

Confidence: 92%, ready to get started.

