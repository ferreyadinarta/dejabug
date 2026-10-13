# Reference: adobe/react-spectrum#10092
Video: videos/adobe_react-spectrum-10092.mov (5.4 s). Graded from 4 fps keyframes, before seeing dejabug output.
App: local Vite reproducer (localhost:5173) "React Aria Components - DropZone + FileTrigger scroll-jump reproducer": buttons "1. Capture before", "2. Capture after", "Clear log", a "Live scrollTop: 721.0" readout, a scrollable box containing a DropZone with a "Click to upload" FileTrigger button ("or drag a file here") and a pink "Filler 2 - content below the DropZone" area, and a capture log below. The page is already scrolled so the upload button is mid-view (scrollTop 721.0).

## Actions (in order)
1. click @0:00.5-0:00.8 - "1. Capture before" (log shows "BEFORE - scrollTop=721.0, activeEl=BUTTON text="1. Capture before" ...")
2. click @0:01.2 - "Click to upload" inside the DropZone (the scroll box jumps: "Live scrollTop: 356.5", the box now shows "Inner DropZone filler - the hidden DropZone accessibility button sits at the top of this region..."; the macOS file picker opens at 0:01.8)
3. click @0:02.8-0:03.0 - "Cancel" in the native file picker (dialog closes)
4. click @0:03.8-0:04.0 - "2. Capture after" (log adds "AFTER - scrollTop=356.5, activeEl=BUTTON text="2. Capture after", hiddenBtnTop=440.9 ...")

## Bug moment
@0:01.5 - clicking the FileTrigger's "Click to upload" button inside the DropZone makes the surrounding scroll container jump (scrollTop 721.0 -> 356.5) as focus moves to the DropZone's hidden accessibility button; the visible button scrolls out of view.
