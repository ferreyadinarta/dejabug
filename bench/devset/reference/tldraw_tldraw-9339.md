# Reference: tldraw/tldraw#9339
Video: videos/tldraw_tldraw-9339.mov (28.8 s). Graded from 1 fps keyframes plus zoomed crops of the style panel at 7.5, 17.5 and 22.5 s, before seeing dejabug output.
App: tldraw canvas (SDK example) with five blue draw shapes (one large outlined shape, one pattern-filled, solid/semi ones) and the style panel on the right: colors, opacity slider, fill row (Fill - None / Fill - Semi / Fill - Solid / rightmost "Fill" button that opens a side panel with more fills: Pattern / two darker solid fills), dash row, size S/M/L/XL.
Fill button names come from the hover tooltips visible in the video ("Fill", "Fill - Pattern", "Fill - Semi", "Dash - Dashed", "Opacity - 100%").

## Actions (in order)
1. click @0:02.0 - the large outlined shape on the left (selected; fill none)
2. drag @0:03.0-0:05.0 - press on the fill row and scrub across "Fill - Semi" to the third fill button (shape previews white, then light-blue fill), release / click on the third fill button (0:05.0, click ripple)
3. click @0:07.0 - the rightmost "Fill" button (side panel opens with Pattern / dark fill / black fill)
4. hover @0:08.0-0:11.0 - side-panel fills and the rightmost "Fill" button (tooltip "Fill")
5. drag @0:12.0-0:13.0 - scrub from the third fill button off toward the dash row (shape fill disappears, 0:13.0)
6. hover @0:14.0 - the side panel's middle fill
7. click @0:15.0 - side panel "Pattern" fill (shape gets pattern fill at 0:16.0; tooltip "Opacity - 100%")
8. hover @0:17.0-0:18.0 - the rightmost button (tooltip "Fill - Pattern")
9. hover @0:19.0 - dash row (tooltip "Dash - Dashed")
10. click @0:20.0-0:21.0 - the side panel's darkest fill (shape becomes solid blue, 0:21.0)
11. hover @0:23.0 - "Fill - Semi" (tooltip)
12. click @0:24.0 - the first fill button (Fill - None; shape outline only)
13. click @0:25.0 - the rightmost "Fill" button again (side panel opens)
14. click @0:27.0 - empty canvas area right of the shapes (side panel closes)

## Bug moment
@0:07.5 - opening the rightmost "Fill" side panel shows its leftmost "Pattern" option highlighted as selected although it was never chosen, at the same time as the third fill button in the main row is highlighted. Also at 0:22.0 after choosing a side-panel fill, the rightmost "Fill" button shows no selected state. Primary: 0:07.5.
