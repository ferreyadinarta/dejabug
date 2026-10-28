# Reference: TypeCellOS/BlockNote#2572
Video: videos/TypeCellOS_BlockNote-2572.webm (55.3 s, Firefox on Linux, recorded with Spectacle). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website demo (blocknotejs.org/demo#et2zn) with a comments sidebar. The pointer is visible; clicks are inferred from caret moves, toolbars and tabs opening or closing.
Start state: comments sidebar open with one thread by Kev ("Comment", quoting "Share the URL a..."). The paragraph "Share the URL above to collaborate with others ⚡" carries the yellow comment highlight and is a link (the link toolbar shows for it). Tabs: BlockNote plus two "Example Domain" tabs.

## Actions (in order)
1. hover @0:01.5 - the paragraph "Share the URL above..." (block side menu + and drag handle appear)
2. click @0:02.0 - end of that line, after "⚡" (caret at the end; link toolbar "Edit link / open / remove" appears at 0:02.5)
3. hover @0:03.5-0:04.5 - link toolbar buttons: "Open in new tab" tooltip (0:03.5), "Edit" (0:04.0), "Remove link" (0:04.5)
4. click @0:06.0-0:06.5 - the commented link text "others" (caret in "oth|ers"); at 0:07.0 a new tab opens and is focused on example.org
5. click @0:08.5-0:09.0 - browser tab "BlockNote - Javascript..." (hover preview at 0:08.5); back to the editor, link toolbar shown
6. hover @0:10.5-0:11.0 - link toolbar "Remove link" button (tooltip)
7. click @0:11.0-0:11.5 - "Remove link" (toolbar disappears) (unclear: click inferred from the toolbar closing while the pointer stays on the button)
8. click @0:12.5 - "with" in the paragraph; at 0:13.0 the comment card in the sidebar is selected (outlined, "Add comment..." field) and the highlight darkens
9. click @0:15.5 - "Export" (dropdown PDF / DOCX / ODT opens) (unclear: may have opened on hover; it closes again at 0:16.0)
10. click @0:16.0-0:16.5 - sidebar toggle icon (top right of the editor); the sidebar closes and the thread shows as a floating card under the paragraph
11. click @0:17.0-0:17.5 - "above" in the paragraph (caret "abo|ve"; floating thread stays)
12. click @0:18.5-0:19.0 - right of the line end (caret after "⚡"); the floating thread fades out by 0:19.5
13. drag @0:19.5-0:20.5 - select the whole line from its end back to "Share"; formatting toolbar appears at 0:21.0
14. click @0:23.0-0:23.5 - link button in the formatting toolbar (URL input "Edit URL" opens next to the selection; pointer moves into it at 0:24.0)
15. type @0:24.5-0:31.5 - "https://example.org/" in the URL input (typo "https://example/or" at 0:28.5 corrected back to "https://example" at 0:29.0, then ".org/")
16. key @0:32.0 - Enter (unclear: inferred; the input closes, caret at the end of the line, and the yellow comment highlight is no longer shown)
17. click @0:34.0 - "collaborate" (caret "colla|borate", link toolbar appears); at 0:34.5 another example.org tab opens and is focused
18. hover @0:35.0-0:35.5 - tab bar, the new "Example Domain" tab (preview)
19. click @0:36.5-0:37.0 - close button ("Fermer l'onglet") of that tab; back to the BlockNote tab
20. click @0:38.5-0:39.0 - right of the line end (caret after "⚡"; link toolbar again at 0:39.5)
21. click @0:42.0 - right of the line end again (caret after "⚡", link toolbar at 0:42.5) (unclear: could be the same caret blinking with the pointer just moving)
22. click @0:43.0-0:43.5 - "Remove link" in the link toolbar (tooltip at 0:43.0, toolbar gone at 0:43.5) (unclear: click inferred from the toolbar closing)
23. click @0:44.5-0:45.0 - "to" in the paragraph; the whole line ends up selected with the formatting toolbar (unclear: pointer does not move, likely triple-click or select-all)
24. click @0:46.0-0:46.5 - sidebar toggle icon; sidebar reopens and the thread now reads "Original content deleted" / Kev / "Comment"
25. click @0:48.0-0:48.5 - the comment card "Comment" in the sidebar (card selected, resolve/menu icons show)
26. click @0:49.5-0:50.0 - "collaborate" in the paragraph (caret "collabora|te"; card deselected)
27. drag @0:50.5-0:51.0 - select the whole line from "⚡" back to the start; formatting toolbar at 0:51.5 (unclear: could be a shift-click)
28. click @0:52.0 - empty editor area below the paragraph (selection cleared)

## Bug moment
@0:07.0 - clicking the link that carries the comment ("others", 0:06.5) opens example.org in a new tab and the comment is not shown or selected in the sidebar. For contrast, once the link is removed, clicking the same text (0:12.5) selects the comment at 0:13.0. The link opens a new tab again at 0:34.5 after it is re-added.
