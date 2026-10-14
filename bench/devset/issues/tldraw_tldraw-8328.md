# "Move focus to canvas" button overlaps "Back to content" and flickers

## Description

The "Move focus to canvas" skip-to-content button (`SkipToMainContent` / `.tl-skip-to-main-content`) appears in the same spot as the "Back to content" helper button when both are visible. It also flickers as event handlers trigger.

Both buttons show in the top left, seemingly in the same spot.

## Steps to reproduce

1. Open the editor with shapes on the canvas
2. Pan away so all shapes are off-screen (triggers "Back to content" button)
3. Tab into the UI so the skip-to-content button gains focus
4. Both buttons overlap in the top-left area

## Expected behavior

The buttons should not overlap. The skip-to-content button should appear in a position that doesn't conflict with the helper buttons area.

## Actual behavior

"Move focus to canvas" renders on top of "Back to content". Additionally, the button flickers as event handlers fire.

## Video

https://github.com/user-attachments/assets/0e3ae422-fe41-4683-8e49-06e25d0c3262
