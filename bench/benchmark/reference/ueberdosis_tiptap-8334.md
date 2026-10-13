# Reference: ueberdosis/tiptap#8334
Video: videos/ueberdosis_tiptap-8334.mov (16.6 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tiptap.dev homepage, "Agent editor" demo tab, document containing "Hello".

## Actions (in order)
1. click @0:00.5 - end of the "Hello" line in the editor
2. key @0:02.0 - Enter (new paragraph)
3. type @0:02.5-0:04.5 - "https://google.com"
4. type @0:05.0-0:06.5 - " rfgrgregre" (the typed URL becomes a link at the space; the following text is plain)
5. key @0:07.0 - Enter (new paragraph)
6. paste @0:08.0 - "https://google.com" (appears at once as a link; Cmd/Ctrl+V inferred)
7. type @0:09.0-0:10.0 - " ergvergvererre"
8. double-click @0:11.0-0:11.5 - the word "ergvergvererre" on the second link line (word highlighted)
9. click @0:12.0 - after the end of the second link line
10. key @0:13.5 - Enter (new empty line)

## Bug moment
@0:09.0 - text typed after the pasted URL and a space stays part of the link (underlined, link colour: "https://google.com ergvergvererre"), unlike the typed URL on the line above.
