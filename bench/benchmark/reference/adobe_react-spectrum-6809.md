# Reference: adobe/react-spectrum#6809
Video: videos/adobe_react-spectrum-6809.mp4 (14.7 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: small React Aria form: "Favorite Sports" Select ("Select an item") and a "Submit" button (react-hook-form validation).

## Actions (in order)
1. click @0:01.0 - "Submit" (validation error "Please select one option" appears, Select gets red border)
2. click @0:03.5 - "Submit" again
3. click @0:05.0 - the "Select an item" trigger (list Football / Basketball / Tennis opens)
4. click @0:06.0 - "Submit" (list closes; Submit pressed 0:06.0-0:07.5)
5. key @0:08.5 - Tab / Shift+Tab to the Select (blue focus ring shows on the Select)
6. key @0:10.0 - open the Select with the keyboard (list opens with "Football" highlighted)
7. key @0:11.0 - Escape/Tab (list closes, focus ring on "Submit")
8. key @0:12.0 - Shift+Tab back to the Select (focus ring on the Select)
9. click @0:13.0 - "Submit"

## Bug moment
@0:01.5 - after clicking Submit, react-hook-form focuses the invalid Select but no focus ring (isFocusVisible) is shown; repeats at 0:04.0, 0:08.0 and 0:13.5, while keyboard focus (0:08.5, 0:12.0) does show the ring. Primary: 0:01.5.
