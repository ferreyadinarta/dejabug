# Reference: mui/mui-x#15758
Video: videos/mui_mui-x-15758.mov (10.4 s, macOS Chrome). Graded from 2 fps keyframes, before seeing dejabug output.
App: CodeSandbox embed of a DateTimePicker ("Basic date time picker") with a single-column digital clock. The pointer is visible; the press on 01:05 AM is inferred from the list jumping back.
Start state: picker popup already open, calendar December 2024 (today 5 outlined, no date selected), time column showing 12:00 AM at the top, field empty "MM/DD/YYYY hh:mm aa".

## Actions (in order)
1. scroll @0:01.5-0:03.0 - time column scrolled down (12:00 AM -> 12:35 AM at the top)
2. click @0:03.5-0:04.0 - "01:05 AM" (hover highlight; slow press per the issue) (unclear: the press is not visible, inferred from the list resetting at 0:04.5)
3. scroll @0:06.0-0:07.0 - time column scrolled down again (to 01:10 AM at the top)
4. click @0:07.5 - "01:35 AM" (grey pressed state); at 0:08.0 it is selected (blue) and the field shows "12/05/2024 01:35 AM"; the popup closes at 0:08.5

## Bug moment
@0:04.5 - after pressing on "01:05 AM" the time list jumps back to the top (12:00 AM) and nothing is selected; the field stays empty. The second attempt (0:07.5) works.
