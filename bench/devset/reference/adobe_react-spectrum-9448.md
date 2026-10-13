# Reference: adobe/react-spectrum#9448
Video: videos/adobe_react-spectrum-9448.mov (20.8 s). Graded from 1 fps keyframes plus 2 fps crops of the lower table's first row (11-19 s), before seeing dejabug output.
App: StackBlitz-style harness with two react-aria-components tables (checkbox column + "Foo / Bar / Baz" columns, rows "Foo 0 / Bar 0 / Baz 0" ...): the upper one labelled "...: auto", the lower one "overflow: clip auto". Table width is a non-integer (percentage) width.
Keyboard actions are inferred from the focus ring moving between cells.

## Actions (in order)
1. hover @0:01.0-0:04.0 - over the upper table rows (around "Baz 4" / "Baz 5")
2. hover @0:05.0-0:06.0 - the horizontal scrollbar under the upper table (scrollbar thumb darkens)
3. hover @0:07.0-0:09.0 - down to the lower ("overflow: clip auto") table
4. click @0:10.0 - "Foo 0" row of the lower table (row selected, checkbox checked, header checkbox shows partial)
5. key @0:12.0-0:18.0 - ArrowLeft / ArrowRight through the cells of row 0 (focus ring: "Foo 0" 0:12.0, "Baz 0" 0:13.5, "Foo 0" 0:14.5, row checkbox 0:15.0, "Foo 0" 0:15.5, "Bar 0" 0:16.0, "Baz 0" 0:16.5, "Foo 0" 0:17.0, row checkbox 0:17.5)

## Bug moment
@0:00.0 - the upper table shows a horizontal scrollbar although its columns fit (TableLayout rounds the non-integer table width up), most visible when hovering it at 0:05.0. The lower table, with overflow-x: clip, is checked by moving keyboard focus across the cells (0:12.0-0:18.0). Primary: 0:05.0.
