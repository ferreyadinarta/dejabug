# Reference: facebook/lexical#9126
Video: videos/facebook_lexical-9126.mov (16.8 s, Safari; the recorder zooms in at 7.5-8.5 s and 15-15.5 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Lexical playground ("Welcome to the playground") with debug tree view.

## Actions (in order)
1. click @0:00.5-0:01.0 - end of the line "Make sure to check out the various plugins in the toolbar. ... or @-mentions too!"
2. key @0:01.0 - Enter (new empty paragraph)
3. type @0:01.5-0:02.5 - "/card" (slash menu opens, filters to "Card")
4. key @0:03.0 - Enter / select "Card" in the slash menu (a Card with "Title" and "Body" placeholders is inserted)
5. double-click @0:04.0 - the word "find" in "If you'd like to find out more about Lexical" (word selected, floating format toolbar)
6. key @0:04.5 - copy (Cmd+C; inferred)
7. click @0:05.0 - the "Body" placeholder of the card
8. paste @0:05.5 - "find" into the card body
9. click @0:09.5-0:10.0 - the "Title" placeholder of the card
10. paste @0:10.5 - "find" into the card title
11. click @0:16.5 - the "Discord Server" link (pointer moves there at end; no visible effect)

## Bug moment
@0:05.5 - after pasting "find" into the Body slot the grey "Body" placeholder is still drawn on top of / behind the pasted text ("find" overlaps "Body"); same for the Title slot at 0:10.5-0:14.5 (placeholder only disappears on later interaction, 0:15.0).
