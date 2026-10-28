# Reference: mui/mui-x#22080
Video: videos/mui_mui-x-22080.mp4 (13.6 s, Chrome on Windows). Graded from 2 fps keyframes, before seeing dejabug output.
App: MUI X docs, Data Grid "Column dimensions" page, "Fluid width" demo: columns id / username / age, one row (1, @MUI, 20). The pointer is visible; the horizontal scroll is inferred from the scrollbar thumb moving.
Start state: grid fits its width, no horizontal scrollbar.

## Actions (in order)
1. hover @0:02.0-0:03.0 - row "1", then the "id" column header (sort arrow and column-menu icon appear at 0:03.0)
2. drag @0:03.5-0:05.0 - the id|username column separator dragged right, far past the grid's right edge; the id column widens and pushes username/age out of view; a horizontal scrollbar appears at 0:05.5
3. scroll @0:06.0-0:07.5 - grid scrolled horizontally to the far right (thumb moves to the right end; username and age visible again) (unclear: wheel/trackpad, the pointer stays over the header)
4. hover @0:08.5 - horizontal scrollbar thumb at the right end (unclear: may be a scrollbar drag; the thumb does not move further)
5. drag @0:09.0-0:10.5 - the id|username separator dragged left to shrink the id column back, pointer ends past the grid's left edge over the sidebar

## Bug moment
@0:11.0 - after shrinking the column the horizontal scrollbar disappears but the grid stays scrolled: the first (id) column is cut off (only the edge of its sort arrow and its menu icon show, the "1" cell is not visible) and does not recover through 0:13.0.
