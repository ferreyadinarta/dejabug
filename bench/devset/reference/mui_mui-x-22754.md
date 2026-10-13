# Reference: mui/mui-x#22754
Video: videos/mui_mui-x-22754.mov (13.4 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: MUI X docs, Event Calendar "External drag and drop" demo: chips "External Event 1 (30 mins)" ... "External Event 5 (45 mins)" above a week view of "July 2025" (Sun 29 - Fri 4, an "All day" row with "Alice's Birthday" from Thu 3, hour rows 1:00 AM ...).
At 0:00.0 "External Event 5 (45 mins)" is already being dragged (its chip is faded, a small "External Event 5" ghost follows the pointer). The whole video is one drag; its path is given step by step.

## Actions (in order)
1. drag @0:00.0-0:11.5 - "External Event 5" over the calendar and back out several times, then dropped:
   - 0:00.5 into Tue 1 "All day" cell (dashed placeholder shows there)
   - 0:01.0-0:01.5 out, up onto the Tue 1 day header (outside the drop surface, ghost shown)
   - 0:02.0-0:03.5 back into the same Tue 1 "All day" cell: no placeholder
   - 0:04.0 to the Mon 30 "All day" cell (placeholder shows), 0:04.5-0:05.0 back to Tue 1 (placeholder shows)
   - 0:05.5-0:06.0 out again over the header / "July 2025" bar
   - 0:06.5-0:07.0 back into Tue 1 "All day" and down toward 1:00 AM: no placeholder until 0:07.5 (placeholder "External Event 5..." at Tue 1:00 AM)
   - 0:08.0-0:08.5 out over the header, 0:09.0-0:09.5 back into Tue 1 "All day": no placeholder
   - 0:10.0 out over the header, 0:10.5 back into Tue 1 "All day": no placeholder
   - 0:11.0 to the Wed 2 "All day" cell (placeholder shows), released at 0:11.5 (event "External Event 5" added on Wed 2 all-day; the chip is removed from the list)
2. hover @0:12.0 - the new "External Event 5" all-day event on Wed 2
3. hover @0:12.5 - down to the Thu 3 / 3:00 AM area

## Bug moment
@0:02.0 - after the dragged external event leaves the calendar and re-enters at the same cell (Tue 1 "All day"), the drop placeholder stays hidden; it only comes back when the pointer moves to a different slot (0:04.0). Repeats at 0:06.5, 0:09.0 and 0:10.5.
