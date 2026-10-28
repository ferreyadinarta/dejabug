# Reference: TypeCellOS/BlockNote#2760
Video: videos/TypeCellOS_BlockNote-2760.mov (14.3 s; "0_51_1_error.mov", the second of four videos in the issue; the others show v0.47.3 working, the Formatting Toolbar and the Block Side Menu, and are not used). Graded from 2 fps keyframes, before seeing dejabug output.
App: BlockNote website example "Advanced Tables" (light theme, v0.51.1 per the file name). The mouse pointer is visible.
Start state: table with "This row has headers" / "This is RED" / "Text is Blue", "This spans 2 columns and 2 rows" / "Sooo many features", "A cell" / "Another Cell" / "Aligned center"; below it "Featuring:" and three bullets. No menu open; all cell text dark gray, no cell backgrounds.

## Actions (in order)
1. hover @0:01.0-0:01.5 - "A cell" cell (bottom-left); the table handles and a small cell handle on the top edge of "A cell" appear
2. click @0:02.0-0:02.5 - cell handle at the top edge of "A cell" (Table Handle Menu opens with a single item "Colors")
3. hover @0:03.0-0:03.5 - "Colors" (color submenu opens: text colors Gray...Pink, then "Background" Auto (checked)...Pink)
4. click @0:04.5-0:05.0 - text color "Purple" (menu closes; "A cell" text stays dark gray; caret appears at the start of "This row has headers")
5. click @0:06.0-0:07.0 - cell handle at the top edge of "A cell" again ("Colors" menu opens)
6. hover @0:07.5 - "Colors" (submenu opens; "Purple" now shows a check mark under text colors, Background still "Auto")
7. click @0:08.5-0:09.0 - Background "Brown" (menu closes; "A cell" background stays white). Pointer then rests to the right of "Cell background & foreground coloring" until the end (0:09.0-0:14.3), no further actions

## Bug moment
@0:05.0 - after choosing text color "Purple" from the Table Handle Menu, the "A cell" text is not colored (at 0:07.5 the menu shows Purple checked while the text is still dark gray). Again @0:09.0: Background "Brown" is chosen but the cell background is not applied.
