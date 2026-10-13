# Reference: ueberdosis/tiptap#8014
Video: videos/ueberdosis_tiptap-8014.mp4 (46.2 s). Graded from 1 fps keyframes, before seeing dejabug output.
App: tiptap.dev homepage editor demos with tabs "Agent editor / Docx editor / Notion-like editor / Simple editor".
Copy keystrokes (Cmd+C) have no visible effect and are not listed; pastes are listed because the text changes. Consecutive pastes at one spot are one action.

## Actions (in order)
1. drag @0:00.0 - select "of having AI that sea" in "Explore the magic of having AI that seamlessly..." (Agent editor)
2. paste @0:01.5 - over the selection (text splits into separate paragraphs at 0:02.0)
3. click @0:03.0 - "Docx editor" tab
4. drag @0:05.0-0:06.0 - select "Non-Disclosure Agreement" in "This Non-Disclosure Agreement ("Agreement")..."
5. right-click @0:07.0 - on the selection (browser context menu: Search the web / Translate / ... / Inspect)
6. paste @0:09.5 - over the selection (paragraph splits at 0:10.0)
7. click @0:11.0 - "Notion-like editor" tab
8. drag @0:14.0 - select "writing your" in "Start writing your thoughts here ..."
9. paste @0:15.0 - over the selection (splits into "Start" / "writing you" / "r thoughts here")
10. click @0:17.0 - after "Just copy the URL from" in the blockquote
11. paste @0:18.0 - at the caret (blockquote line splits)
12. double-click @0:20.0 - the word "copy" in "Just copy the URL from"
13. paste @0:21.0-0:22.0 - several times after "copy" ("Just copy copy copy copy copy the URL from", inline)
14. click @0:22.0-0:23.0 - end of "writing you"
15. paste @0:23.5-0:24.0 - several times ("writing youyouyouyouyouyou")
16. click @0:25.0 - "Simple editor" tab
17. drag @0:26.0 - select "Welcome" in "Welcome to the Simple Editor template!"
18. paste @0:27.0 - over the selection ("Welcome" split into its own paragraph with blank paragraphs)
19. drag @0:28.0 - select "integrates open source UI components ... MIT."
20. paste @0:29.0 - over it ("template" split onto its own paragraph)
21. click @0:30.0-0:31.0 - "Notion-like editor" tab
22. double-click @0:32.0 - the word "your" in "Invite your colleagues to make this fun!"
23. paste @0:33.0-0:35.0 - several times ("Invite" / "your your your your your colleagues ..." split)
24. double-click @0:36.0 - "copy" in "Just copy copy ..." line
25. paste @0:36.5-0:37.0 - several times (more "copy" words, inline)
26. click @0:37.0-0:38.0 - "Docx editor" tab
27. click @0:39.0 - inside "entered" in "("Agreement") is entered into as of"
28. drag @0:41.0 - select "entered into as of"
29. paste @0:42.0 - over the selection (splits: "("Agreement") is" / "entered into as of [")
30. double-click @0:43.0 - "Agreement" in "("Agreement") is"
31. paste @0:44.0 - over it (splits into "("" / "Agreement")
32. hover @0:45.0 - site header menu (Quickstart / Learn & compare dropdown opens)

## Bug moment
@0:02.0 - pasting text copied from the editor inserts extra empty paragraphs before and after the pasted text (first seen in the Agent editor; repeats at 0:10.0, 0:15.0, 0:18.0, 0:27.0, 0:29.0, 0:33.0, 0:42.0, 0:44.0).
