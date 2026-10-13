# Reference: ueberdosis/tiptap#7731
Video: videos/ueberdosis_tiptap-7731.mov (12.4 s). Graded from 1 fps keyframes, before seeing dejabug output.
App: tiptap docs, Markdown > Introduction page. React demo with buttons "Parse Markdown →", "← Extract Markdown", "Bold", "Italic", a "Markdown Input" textarea holding a one-column table (`| desc |` / `| :-------: |` / `| foo bar |`) and a "Tiptap Editor" showing the table (header "desc", cell "foo bar").

## Actions (in order)
1. click @0:01.0 - in the "Markdown Input" textarea, between "foo" and "bar" in `| foo bar |`
2. key @0:02.0 - Backspace (removes the space: `| foobar |`)
3. type @0:04.0-0:05.0 - "<br>" between "foo" and "bar" (`| foo<br>bar |`)
4. click @0:06.0 - "Parse Markdown →" (the Tiptap Editor cell now shows "foo" and "bar" on two lines)
5. hover @0:07.0 - the "foo / bar" cell in the Tiptap Editor
6. click @0:09.0 - "← Extract Markdown"

## Bug moment
@0:10.0 - after "← Extract Markdown" the Markdown Input shows `| foo bar |`: the `<br>` line break inside the table cell is dropped (the editor still shows "foo" / "bar" on two lines).
