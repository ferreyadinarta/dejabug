# Table cell line breaks (<br>) are lost when extracting Markdown from editor

### Affected Packages

extension-markdown

### Version(s)

3.x

### Bug Description

When a Markdown table contains line breaks inside cells using `<br>` tags, parsing the Markdown into the editor works correctly and the `<br>` is rendered as expected. However, when extracting Markdown back from the editor using the Markdown extension's serializer, the `<br>` tags are silently dropped, resulting in data loss.
Example input Markdown:
```markdown
|    desc     |
|   :-----:   |
| foo<br>bar  |
```
After parsing and re-serializing via `editor.storage.markdown.getMarkdown()`, the output becomes:
```markdown
|  desc   |
| :-----: |
| foo bar  |
```
The `<br>` between `foo` and `bar` is completely lost.

https://github.com/user-attachments/assets/32b2be1a-b54a-4046-b4ea-65342c049e61

### Browser Used

Chrome

### Code Example URL

https://tiptap.dev/docs/editor/markdown

### Expected Behavior

The Markdown serializer should preserve `<br>` tags inside table cells when extracting Markdown from the editor. The round-trip (parse → serialize) should produce output that is semantically equivalent to the original input.
Expected output after serialization:
```markdown
|    desc     |
|   :-----:   |
| foo<br>bar  |
```

### Additional Context (Optional)

This issue affects any workflow that relies on round-tripping Markdown through the editor (e.g., loading from a database, editing, then saving back). The `<br>` inside table cells is a common pattern for multi-line cell content in GitHub Flavored Markdown (GFM). The root cause is likely that the Markdown serializer's table cell handler does not account for `hardBreak` nodes (the ProseMirror node type that `<br>` is parsed into), and simply serializes them as space.

### Dependency Updates

- [x] Yes, I've updated all my dependencies.
