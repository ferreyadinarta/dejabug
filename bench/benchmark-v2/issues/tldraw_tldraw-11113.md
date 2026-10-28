🗣️: Creating e.g. a h1 heading in a text shape on the canvas creates a blank line underneath the heading, acting as padding. However, this line then can't be deleted.

---

When a heading is the last block in a text shape, an empty line is added underneath it. The caret can move onto that line, but Backspace and Delete can't remove it: it comes straight back. The line is saved with the shape, so the shape's bounds stay a line taller than the heading after editing ends. A heading at the end of a text shape should be the last line, with no extra line unless the user adds one. This is the same bug #7641 fixed for bullet and numbered lists.

https://github.com/user-attachments/assets/bbc6e210-bb5c-47ea-9fb0-7a856d3e07df

## Steps to reproduce

1. Select the text tool and click the canvas.
2. Type `# Heading`.
3. Press ↓. The caret moves onto an empty line below the heading.
4. Press Backspace, or Delete at the end of the heading. The empty line reappears.
5. Press Escape. The selection bounds still include the empty line.

## Root cause

Our TipTap setup keeps StarterKit's `TrailingNode` extension. Whenever the document's last block isn't in its `notAfter` list, it appends an empty paragraph, and it re-appends one in `appendTransaction` after any edit that removes it. #7643 set `notAfter` to `['paragraph', 'bulletList', 'orderedList', 'listItem']` in `getTipTapDefaultExtensions` (`packages/tldraw/src/lib/utils/text/richText.ts`) but left out `heading`. With blockquote, code block and horizontal rule disabled, heading is the only enabled block type missing from that list, so a trailing heading always gets a paragraph after it.

Checked in the examples app on main: after typing `# Heading` the shape's stored `richText` is `heading + paragraph`, and it stays that way after Backspace ×3, Delete ×3 and Escape. A TipTap editor built from the same extensions with `heading` added to `notAfter` keeps the document as just `heading`, and nothing re-adds the paragraph.

Fix direction: add `'heading'` to `notAfter`, or disable `trailingNode` altogether, since none of the enabled block types needs a trailing paragraph to escape from. Either way, shapes already saved with the extra paragraph keep it (it just becomes deletable) unless it's stripped.

## Open questions

1. **Should shapes that already have the extra empty line be cleaned up, or should the fix only stop new ones?**
   _Awaiting answer._

Confidence: 85%, ready to get started.
