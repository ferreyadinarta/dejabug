# Reference: ueberdosis/tiptap#8164
Video: videos/ueberdosis_tiptap-8164.mov (8.8 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Tiptap "Table of Contents" node demo ("Insert TOC Node" button, heading "Table of Contents Sidebar Demo", TOC node below).

## Actions (in order)
1. triple-click @0:00.5-0:01.0 - the heading "Table of Contents Sidebar Demo" (whole heading selected; TOC node not highlighted)
2. click @0:2.5 - end of the heading (caret after "Demo")
3. type @0:03.0-0:04.0 - "fff" (heading becomes "...Demofff", TOC entry updates)
4. drag @0:04.5-0:05.0 - select the last two added characters "ff" with the mouse (click-drag over them)
5. drag @0:06.0-0:07.5 - re-select / change the selection inside "fff" a few times (click and drag)
6. click @0:08.5 - end of the heading (caret placed, selection cleared)

## Bug moment
@0:05.0 - with only "ff" in the heading selected, the whole Table of Contents node gets the selected-node highlight (purple background), as if it were selected (again 0:06.0 and 0:07.0).
