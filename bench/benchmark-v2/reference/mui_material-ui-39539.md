# Reference: mui/material-ui#39539
Video: videos/mui_material-ui-39539.mov (19.1 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: macOS QuickTime window playing an inner 6 s screen recording ("Screen Recording 2024-09-21 at 19.02.06.mov") of a browser on react-tsmx9v.stackblitz.io that shows one MUI text field with a yellow outline and dropdown arrow. Two layers of actions: the inner recording shows the page being reloaded; the outer user scrubs the QuickTime timeline to step through the page load. Outer clicks are shown with a click ring.
Start state: QuickTime paused at 00:00 of 00:06; the inner frame shows the text field at normal height.

## Actions (in order)
1. click @0:01.0 - browser reload button inside the played-back recording (inner pointer on reload, which turns into "X" while the page loads; page goes white with a spinner at 0:01.5)
2. drag @0:01.0-0:02.5 - QuickTime scrubber from 00:00 to 00:04 (inner frames: loading page, then black page)
3. drag @0:03.5-0:04.0 - on the QuickTime control bar below the timeline; the control bar moves right (unclear: could be a click; the bar's new position stays for the rest of the video)
4. drag @0:04.5-0:05.5 - scrubber to 00:05 and then to the end 00:06 (text field shown at normal height)
5. click @0:06.0-0:06.5 - on the timeline track left of the playhead (click rings visible; playhead stays at 00:06, unclear whether it registered)
6. drag @0:07.5-0:17.5 - scrubber back to 00:05 and 00:04, then small back-and-forth movements around 00:04 that step through the inner frames: loading page (0:10.0), normal field (0:10.5-0:11.0), black page (0:11.5, 0:14.5-0:15.0), tall field (0:13.0, 0:16.0), normal field (0:12.0-0:12.5, 0:13.5-0:14.0, 0:15.5, 0:16.5-0:17.5)
7. 0:18.0 - QuickTime controls and title bar disappear, dashed selection marquee around the screen (unclear: end of the outer screen recording, not an app action)

## Bug moment
@0:13.0 - the scrubbed frame right after the page load shows the text field taller than normal, with the dropdown arrow at the bottom left; the next frame (0:13.5) shows it at normal size. Again @0:16.0.
