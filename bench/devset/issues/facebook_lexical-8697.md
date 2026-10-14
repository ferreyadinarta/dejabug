# Bug: Dead keys on a new paragraph get removed

When attempting to type a code block on a keyboard with dead keys, the backticks (or any other dead key) gets deleted by Lexical.

Lexical version: 0.45.0

## Steps To Reproduce

This issue is specific to Firefox. Tested on 151.0.3.
1. Pick any keyboard layout with dead keys (in my case, ABNT2).
2. Type any dead key, such as backticks or tildes on a new paragraph (if there is any other text on the text node, this doesn't happen).
3. When you press the key once, it renders the dead key. After pressing it a second time, 2 dead keys are shown, and the text node is removed in a few milliseconds.

Link to code example: this can be reproduced in the Lexical playground. https://playground.lexical.dev/

https://github.com/user-attachments/assets/70b82ada-9520-404e-bcda-b34948c54202

## The current behavior
The dead key is removed when typed on a new paragraph on Firefox.

## The expected behavior
Dead keys should be kept regardless of context.

## Impact of fix
This impacts any Firefox user using keyboard layouts with dead keys.
