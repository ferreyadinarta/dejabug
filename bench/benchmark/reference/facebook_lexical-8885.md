# Reference: facebook/lexical#8885
Video: videos/facebook_lexical-8885.mov (10.7 s, Safari). Graded from 2 fps keyframes, before seeing dejabug output.
App: Lexical playground ("Welcome to the playground") with the debug view (tree / selection / commands) below the editor.

## Actions (in order)
1. scroll @0:00.0-0:01.0 - page scrolled down a little (editor toolbar moves to the top)
2. click @0:02.0 - the "Discord Server" link in the last bullet (link popup "https://discord.com/invite/KmG4wQnnD9" with edit/delete icons appears)
3. scroll @0:02.5-0:03.0 - debug view scrolled to the bottom to show the "commands:" list (ends with "9. CLICK_COMMAND")
4. click @0:05.5 - the URL "https://discord.com/invite/KmG4wQnnD9" inside the link popup (a new tab flashes at 0:06.0, then back)
5. drag @0:09.5-0:10.0 - select the text of command "10. { type: SELECTION_CHANGE_COMMAND, payload: undefined }" in the debug view

## Bug moment
@0:05.5 - after clicking the link in the popup, the commands log gains "10. SELECTION_CHANGE_COMMAND" after the CLICK_COMMAND (in Chrome/Firefox the last command would be CLICK_COMMAND). Highlighted by the user at 0:09.5.
