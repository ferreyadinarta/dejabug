# Reference: mui/mui-x#23735
Video: videos/mui_mui-x-23735.mov (11.1 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: MUI X docs, Event Timeline "Day and hour preset" demo (rows Cupra Leon / Fiat 500 / Peugeot 3008 / Volkswagen ID3; "MUI X Missing license key" watermark).

## Actions (in order)
1. scroll @0:00.5-0:04.0 - mouse wheel down inside the timeline grid (rows scroll away, a large blank area follows)
2. scroll @0:04.0-0:08.0 - mouse wheel back up inside the timeline grid (rows reappear with gaps, back to top at 0:08.0)

(No clicks, typing or drags are visible; the pointer stays over the grid. The scrollbar thumb moves while the pointer is still.)

## Bug moment
@0:01.5-0:03.5 - most of the viewport is blank while scrolling: only 1-3 rows are mounted and the scroll area is far taller than the rows (rows estimated too tall). Primary: 0:02.0.
