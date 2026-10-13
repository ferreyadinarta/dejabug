# Reference: facebook/lexical#8697
Video: videos/facebook_lexical-8697.webm (16.7 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Lexical playground (v0.45.0 dev) in Firefox with the default "Welcome to the playground" content and the debug tree view below the editor. The keyboard layout has dead keys (ABNT2 per the issue): ` ~ ^ are typed as dead keys (COMPOSITION_START_COMMAND in the debug log). The caret is already at the end of the "Lastly, ... get a chance 😊 ." paragraph at 0:00.0.
No mouse clicks are visible; everything is typed.

## Actions (in order)
1. type @0:01.5-0:06.5 - " this works fine ~~~ ````` ^^^" at the end of the "Lastly, ..." paragraph (the dead-key characters stay)
2. key @0:07.0-0:08.0 - Enter twice (two new paragraphs, caret in the second)
3. type @0:08.0-0:09.5 - "this does not work"
4. key @0:10.0 - Enter (new empty paragraph)
5. type @0:11.5-0:13.0 - the ` dead key, twice: "`" appears (0:11.5, 0:12.5) and is removed again (0:12.0, 0:13.0)
6. type @0:14.0-0:15.5 - the ~ dead key, then the ^ dead key twice: "~" (0:14.0), "^" (0:14.5), "^" (0:15.5); each one disappears again (0:15.0, 0:16.0)

## Bug moment
@0:12.0 - in a new empty paragraph, a dead-key character ("`") shows briefly and is then deleted (the paragraph is empty again in the debug tree); it repeats for "`", "~" and "^" until the end. The same keys typed after existing text (0:03.0-0:06.5) are kept.
