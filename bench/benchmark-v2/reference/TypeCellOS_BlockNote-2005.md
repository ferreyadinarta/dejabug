# Reference: TypeCellOS/BlockNote#2005
Video: videos/TypeCellOS_BlockNote-2005.webm (26.2 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website editor (dark theme). The mouse pointer is not visible (a static white arrow drawn at the bottom right is not the pointer); actions are inferred from caret, hover handles, menus and highlights.
Start state: blocks "RAWR", "dsfsdfsdfds sdfsdfsdf", "s", bold "sdfsdfsdf", "Something somewhere dekijde kdj,ek,nd jndkejdken" (default text color); caret at the end of the last line.

## Actions (in order)
1. click @0:00.5 - inside "Something somewhere dekijde ..." (caret moves to between "dek" and "ijde")
2. click @0:02.5-0:03.0 - drag handle (⠿) of the "Something somewhere ..." block (side menu: "Delete", "Colors")
3. hover @0:03.5 - "Colors" (submenu: text colors Gray ... Pink, Background with "Default" checked)
4. click @0:04.0 - menu closes with no visible change (unclear: clicked away or pressed Escape, or picked an item that changes nothing; text stays default color)
5. click @0:05.0-0:05.5 - drag handle (⠿) of the same block again, then hover "Colors" (submenu reopens)
6. click @0:07.0-0:07.5 - "Red" (whole block text turns red)
7. drag @0:10.5-0:13.0 - select text in the red line, ending on "ekijde kdj,e" (formatting toolbar appears at 0:13.5)
8. click @0:15.0-0:16.0 - "A" (Colors) button in the formatting toolbar (dropdown "Text": Default ✓, Gray, Brown, Red, Orange)
9. click @0:16.5-0:17.0 - "Default" (dropdown closes; the selected text stays red)
10. click @0:17.5 - empty line below the red block (placeholder "Enter text or type '/' for commands"; selection gone)
11. drag @0:19.0-0:19.5 - select "ijde kdj,ek,nd jndk" in the red line (formatting toolbar appears at 0:20.0)
12. click @0:20.5-0:21.0 - "A" (Colors) button, tooltip "Colors" (dropdown again shows "Default" checked)
13. click @0:21.5-0:22.0 - "Default" (dropdown closes; the text stays red)
14. click @0:23.0 - in the editor away from the selection (selection and toolbar disappear; unclear exact target, side handle shows at the empty last line)

## Bug moment
@0:17.0 - choosing text color "Default" on red text does nothing: the text stays red (the dropdown also showed "Default" checked while the text was red). Again @0:22.0.
