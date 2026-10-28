# Reference: ueberdosis/tiptap#7776
Video: videos/ueberdosis_tiptap-7776.mov (26.9 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Tiptap docs, Markdown page (tiptap.dev/docs/editor/markdown), React demo with "Parse Markdown →", "← Extract Markdown", "Bold", "Italic", a "Markdown Input" textarea and a "Tiptap Editor" pane.
Start state: Markdown Input is focused (caret on an empty first line) and holds the list "- 123", nested "- 123" / "- 123", "- 123", "- 123." with blank lines between items; Tiptap Editor is empty.

## Actions (in order)
1. click @0:04.0-0:04.5 - "Parse Markdown →" (Tiptap Editor shows bullets 123, nested 123 / 123, 123, "123.")
2. click @0:08.0-0:09.0 - "← Extract Markdown" (click ring visible at 0:08.5; Markdown Input is replaced by "- 123 / - 123 / - 123 / - 123 / -")
3. hover @0:12.0-0:13.5 - "Parse Markdown →" (unclear: button looks pressed/hovered, but the editor does not change, so no click is counted)
4. click @0:18.5-0:19.0 - "Parse Markdown →" (pointer passes over "Italic" at 0:18.0; the editor's last bullet becomes empty)

## Bug moment
@0:09.0 - Extract Markdown drops the text of the last list item: "123." becomes an empty "-" item. Re-parsing at 0:19.0 shows the loss in the editor (last bullet now empty).
