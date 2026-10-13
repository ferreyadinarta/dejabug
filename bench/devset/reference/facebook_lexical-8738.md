# Reference: facebook/lexical#8738
Video: videos/facebook_lexical-8738.mov (10.4 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Lexical playground in Firefox (>=152): default "Welcome to the playground" content followed by a poll component titled "Test" with inputs "Option 1", "Option 2", an "Add Option" button; the caret starts just after the poll (0:00.0).

## Actions (in order)
1. click @0:01.5 - in the "Option 1" input of the poll
2. type @0:02.5-0:05.0 - "fdsfdsfds" (the characters appear after the poll, outside the component, in reverse order: "fds", "fdsfds", "sfdsfds" ...)
3. double-click @0:06.0 - the word "constantly" in "Lastly, we're constantly adding cool new features..." (word selected, floating format toolbar B / I / U / ... appears)
4. click @0:06.5 - in the "Option 1" input again
5. type @0:07.0-0:08.5 - "sdfsdfsfd" (now goes into the Option 1 input as expected)
6. click @0:09.0 - inside the "sdfsdfsfd" text in the Option 1 input

## Bug moment
@0:02.5 - typing into the poll's "Option 1" input puts the text outside the poll component (after it, in the editor body, reversed because the caret stays in place). After moving the selection elsewhere (0:06.0) and clicking the input again, typing works (0:07.0).
