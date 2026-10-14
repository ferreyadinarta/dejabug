# Viewport shifts slightly when zooming out to minimum zoom

## Description

When zooming out to the minimum zoom level (`0.05` by default), the viewport position shifts slightly. Unclear whether this is intentional or a bug.

## Steps to reproduce

1. Open the editor at any zoom level.
2. Zoom out repeatedly (mouse wheel, pinch, zoom-out button, or `-` shortcut) until the zoom is clamped at the minimum.
3. Observe the viewport shifting position slightly when the zoom hits the limit.

## Expected

Once zoom is clamped at the minimum, the camera position should stay put — further zoom-out gestures shouldn't translate the viewport.

## Actual

The viewport translates slightly at the moment the zoom clamps to the minimum.

## Video

https://github.com/user-attachments/assets/ea3d92ec-1fab-42e4-8f79-0204bd6afe15
