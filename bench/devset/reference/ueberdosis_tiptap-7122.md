# Reference: ueberdosis/tiptap#7122
Video: videos/ueberdosis_tiptap-7122.webm (43.7 s). Graded from 1 fps keyframes and 4 fps keyframes (16-28 s, cropped to the editor), before seeing dejabug output.
App: tiptap docs, "Details extension" page, Vue demo with buttons "Set details" / "Unset details" and content "Look at these details", details "This is a summary" (content "Surprise!"), "Nested details are also supported", "This is another summary" ... The pointer is mostly invisible; clicks are inferred from caret moves and toggle highlights.

## Actions (in order)
1. click @0:01.5 - the toggle of "This is a summary" (opens, showing "Surprise!") then at the end of "Surprise!" (caret after it at 0:02.0)
2. type @0:03.0-0:06.0 - ", this works fine" ("Surprise!, this works fine"; details stays open)
3. drag @0:08.0-0:09.0 - select the whole first line "Look at these details"
4. key @0:10.0 - Backspace (line emptied; caret now at the top, document starts with an empty line)
5. click @0:11.0-0:11.5 - "Set details" (a new empty details block is inserted at the very top, caret in its summary at 0:12.0)
6. type @0:14.0-0:16.0 - "look at this" in the new summary
7. click @0:16.5 - the toggle of "look at this" (it opens with an empty content area, 0:17.0)
8. click/type @0:17.2-0:17.5 - in the empty content area; the block collapses again and the caret jumps to the start of "This is a summary"
9. click @0:18.5 - the toggle of "look at this" (opens, caret in its content area at 0:18.8)
10. type @0:20.0 - "y" in the content area: the details collapses and the caret jumps to the start of the next summary "This is a summary" (0:20.2)
11. click @0:21.0 - the toggle of "look at this" (opens; content shows "y")
12. click @0:21.5 - after "y" in the content
13. type @0:22.0 - "y": the block collapses again and the character lands in the next title ("yThis is a summary", caret after it)
14. click @0:22.5 - the toggle of "look at this" (opens, content "yy"), click after "yy" (0:23.0)
15. type @0:23.5 - another character: collapses again, caret jumps to "yThis is a summary"
16. click @0:25.0-0:26.0 - the toggle of "look at this" and its content; typing continues ("yyyy", 0:26.0)
17. key @0:27.0-0:28.0 - an empty paragraph appears above the "look at this" details (Enter at its start; inferred)
18. click @0:30.0-0:35.0 - the summary "look at this", then the end of "yyyy" in its content (opened state)
19. type @0:36.0-0:39.0 - " works now" ("yyyy works now"; the block now stays open)
20. click @0:40.0 - the empty paragraph above the details
21. type @0:42.0-0:43.0 - "new line"

## Bug moment
@0:20.2 - typing the first character inside the content of a details block that is the first node in the document (nothing before it) collapses the block and moves the caret to the next details title (repeats at 0:17.5, 0:22.0, 0:23.5; the stray "y" ends up in "yThis is a summary"). Once a paragraph is above it (0:28.0+) typing works.
