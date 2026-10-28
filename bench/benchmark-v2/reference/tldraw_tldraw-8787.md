# Reference: tldraw/tldraw#8787
Video: videos/tldraw_tldraw-8787.mov (13.7 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: tldraw.com (dark theme, zoom 10%) with two labelled media shapes: "Video" (a video shape playing a screen recording) and "Image" (an image of a style panel). The pointer is visible throughout.
Start state: the "Image" shape is selected; its toolbar above it shows four buttons: replace media, crop, download, ALT.

## Actions (in order)
1. hover @0:01.0-0:02.0 - "Replace media..." button on the image toolbar (white tooltip "Replace media..." above the button at 0:02.0)
2. hover @0:02.5 - "Crop image" button on the image toolbar (white tooltip above)
3. hover @0:03.0 - "Download original" button on the image toolbar (white tooltip above)
4. hover @0:03.5 - "ALT" button on the image toolbar (white tooltip "Alternative text" above)
5. click @0:04.0-0:04.5 - the "Video" shape (hover outline at 0:04.0, selected at 0:04.5; the video toolbar with replace media, download, ALT appears)
6. hover @0:05.0-0:06.5 - "Replace media..." button on the video toolbar (tooltip appears at 0:06.5, dark and below the button)
7. hover @0:07.0-0:08.0 - "Download original" button on the video toolbar (dark tooltip below the button)
8. hover @0:08.5-0:10.0 - "ALT" button on the video toolbar (white tooltip "Alternative text" above the button from 0:09.0)

Not counted: @0:10.5 the pointer moves off to empty canvas; @0:12.0-0:13.0 the macOS screenshot/recording bar (Options, Capture) appears and the pointer goes to its stop button, which is the recorder being stopped, not an app action.

## Bug moment
@0:06.5 - on the video toolbar, "Replace media..." (and "Download original" at 0:07.0-0:08.0) shows a dark tooltip below the button, while "Alternative text" on the same toolbar (0:09.0) and every button on the image toolbar (0:02.0-0:03.5) show a white tooltip above: the video toolbar's tooltips are inconsistent.
