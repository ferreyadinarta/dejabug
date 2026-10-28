# Reference: mui/mui-x#15352
Video: videos/mui_mui-x-15352.mov (16.9 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: MUI X Data Grid demo (columns Desk / Commodity / Trader Name / Trader Email / Quantity, "MUI X Missing license key" watermark, footer "N row(s) selected", "1-10 of 100").
Clicks are inferred from the macOS click ring and from the row selection and cell focus outline changing; Cmd+A is shown by an on-screen keystroke overlay.
Start state: row D-2434 selected with the "Coffee C" cell focused; footer "1 row selected".

## Actions (in order)
1. click @0:00.5 - "Oats" cell (row D-6784); that row becomes selected
2. click @0:01.0 - "Soybeans" cell (row D-608); that row becomes selected
3. key @0:02.0 - Cmd+A; "100 rows selected" at 0:02.5
4. click @0:03.0-0:03.5 - "Oats" cell (row D-6784); "1 row selected"
5. key @0:04.0 - Cmd+A; "100 rows selected"
6. click @0:04.5-0:05.0 - "Cotton No.2" cell (row D-2437); "1 row selected"
7. key @0:05.5 - Cmd+A; "100 rows selected"
8. click @0:06.5 - whitespace right of the last column (Quantity) in row D-6784 (Oats); row selected, no cell focus outline
9. click @0:07.5 - whitespace right of the last column in row D-608 (Soybeans)
10. click @0:08.0 - whitespace right of the last column in row D-6784 (Oats); row selected at 0:08.5
11. key @0:09.0 - Cmd+A; page text gets highlighted (browser text selection), footer still "1 row selected"
12. click @0:10.0 - whitespace right of the last column in row D-608 (text selection cleared, D-608 selected) (inferred, no click ring captured)
13. key @0:10.5 - Cmd+A; page text highlighted again, still "1 row selected"
14. click @0:12.0 - whitespace right of the last column in row D-2925 (Cotton No.2) (inferred, no click ring captured)
15. key @0:12.5 - Cmd+A; page text highlighted, still "1 row selected"
16. click @0:13.5 - "Cotton No.2" cell (row D-2925); cell focus outline, text selection cleared
17. key @0:14.0 - Cmd+A; "100 rows selected"
18. click @0:15.0 - "Cotton No.2" cell (row D-2437); "1 row selected"
19. key @0:15.5 - Cmd+A; "100 rows selected"

## Bug moment
@0:09.0 - after selecting a row by clicking the whitespace right of the last column, Cmd+A selects the page's DOM text instead of all rows; footer stays "1 row selected" (again @0:10.5 and @0:12.5). Clicking a cell first makes Cmd+A work.
