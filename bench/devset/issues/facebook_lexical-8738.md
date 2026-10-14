# Bug: Typed text in Firefox appears outside the block/component

Somewhat similar issue to #7071. When you type inside a component the text appears after the component in Firefox since version 152 (tested with Browserstack). Reproducible on macOS and Windows.

Lexical version: v0.45.0+dev.esm

## Steps To Reproduce

1. Use Firefox ≥152
2. Open https://playground.lexical.dev/
3. Add a poll component
4. Add text to the first field -> Text appears outside of component (reversed because the cursor stays in place)
5. Change the selection
6. Add text to the first field -> Now it works as expected

## The current behavior

https://github.com/user-attachments/assets/5c43d41b-766b-47fe-a918-7e782b3655ba

Text appears not where it belongs, severely impacting usability.

## The expected behavior

Text appears in the expected position.

## Impact of fix

Editors working in current Firefox versions can not reliably edit using blocks/components.

