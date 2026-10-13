# Reference: mui/mui-x#20364
Video: videos/mui_mui-x-20364.mov (18.0 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: StackBlitz Vite demo: stacked BarChart (series A/B/C, x axis 0/3/6/9/12) with "Click on the chart" panel showing "// Item data" and "// Axis data" JSON; reset (undo-arrow) icon top right.
Clicks are inferred from the macOS click ring and from the "Axis data" panel changing; hover alone shows the tooltip but does not change the panel.

## Actions (in order)
1. click @0:01.5-0:02.0 - reset icon (top-right undo arrow); Item/Axis data cleared ("null")
2. click @0:04.0 - x-axis band "6" (not on a bar); Axis data -> axisValue "6"
3. click @0:05.0 - band "3"; Axis data -> "3"
4. click @0:06.0 - band "6"; Axis data -> "6" at 0:06.5
5. click @0:07.0 - band "3"; Axis data -> "3"
6. click @0:08.0 - band "6"; Axis data -> "6"
7. click @0:09.0 - band "3"; Axis data -> "3"
8. click @0:10.0 - band "6"; Axis data stays "3" (click discarded)
9. click @0:12.5-0:13.5 - band "6" again (after hovering 3); Axis data still "3"
10. click @0:14.0 - band "6"; Axis data -> "6"
11. click @0:14.5 - band "3"; Axis data -> "3"
12. click @0:15.0 - band "6"; Axis data stays "3" (discarded)

## Bug moment
@0:10.0 - pointer on band "6" (tooltip shows 6) and clicked, but the Axis data panel keeps axisValue "3": the axis click was dropped. Again at 0:13.5 and 0:15.0.
