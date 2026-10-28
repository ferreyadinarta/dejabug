# Reference: hoppscotch/hoppscotch#6154
Video: videos/hoppscotch_hoppscotch-6154.mp4 (62.2 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: Hoppscotch web app (dark theme), REST, request "test" in collection "Bank"; URL field with variables highlighted (<<test>> purple = CollectionVariable "test", <<tio>> blue = Global "testio").
Most of the video is hovering a variable to bring up its popup (CollectionVariable or Global, Initial / Current values; the Global popup has an edit icon at top right) and moving the pointer toward the popup. Hover attempts on the same variable in the same URL are grouped into one action per stretch. Key presses are inferred from text changes and the "Request saved" toast. The recorder zooms in between 0:06.0 and 0:07.0; that is not a user action.
Start state: URL "a<<test>>a", Body tab open, caret at the end of the URL.

## Actions (in order)
1. hover @0:02.5-0:05.5 - <<test>> in "a<<test>>a" (popup appears, then closes as the pointer moves toward it at 0:03.5, 0:04.5 and 0:05.5)
2. hover @0:07.5-0:12.0 - <<test>> again (popup closes at 0:08.5, 0:10.5 and 0:12.0 as the pointer moves down)
3. hover @0:14.0-0:18.0 - <<test>> again; this time the pointer gets into the popup (0:15.5-0:16.5) before it closes at 0:18.0
4. hover @0:19.5-0:20.5 - <<test>> again (popup closes at 0:21.0)
5. key @0:22.0 - Backspace at the end of the URL (trailing "a" removed; URL "a<<test>>")
6. key @0:23.0-0:23.5 - Ctrl+S ("Request saved" toast)
7. hover @0:23.5-0:26.0 - <<test>> in "a<<test>>"; popup stays while the pointer moves into it (closes at 0:26.5 when the pointer goes to the Body tab)
8. hover @0:27.0-0:30.0 - <<test>> again; popup stays, pointer moves inside it
9. key @0:30.5 - Ctrl+A in the URL field (whole URL highlighted) (inferred)
10. paste @0:31.0 - "https://<<test>>/<<tio>>.com" replaces the URL (unclear: paste or very fast typing; the text appears within one frame)
11. key @0:31.5 - Ctrl+S ("Request saved" toast)
12. hover @0:32.0-0:34.0 - <<tio>> in "<<tio>>.com"; Global popup with edit icon appears, closes at 0:32.5 as the pointer moves down, reappears at 0:33.5, closes at 0:34.5 although the pointer had reached the popup at 0:34.0
13. hover @0:35.5-0:39.5 - <<tio>> again several times (popup closes at 0:36.0, 0:37.5, 0:38.5, 0:39.5)
14. hover @0:40.0-0:42.5 - <<tio>> again; pointer reaches the edit icon in the popup at 0:41.5 (hand cursor) and moves back to "Global" at 0:42.0; popup closes at 0:43.0 (unclear: the edit icon may have been clicked at 0:41.5; nothing opens)
15. hover @0:44.0-0:46.0 - <<test>> in "https://<<test>>/" (CollectionVariable popup closes at 0:44.5 and 0:46.0)
16. hover @0:46.5-0:50.5 - <<test>> again; pointer gets into the popup (0:48.0-0:49.0, 0:50.5); popup flickers off at 0:49.5 when the pointer passes back over the variable
17. hover @0:51.0 - <<tio>> (Global popup)
18. drag @0:51.5 - select ".com" after <<tio>> (unclear: drag or Shift+click/arrows)
19. key @0:52.0 - Backspace (".com" removed; URL "https://<<test>>/<<tio>>")
20. key @0:53.0-0:53.5 - Ctrl+S ("Request saved" toast)
21. hover @0:53.5-0:58.5 - <<tio>> now at the end of the URL; popup stays while the pointer moves into it and onto the edit icon at 0:55.5, and back
22. hover @0:59.5-1:01.0 - <<test>> in "https://<<test>>/"; popup closes at 1:00.5, reappears at 1:01.0 with the pointer inside it

## Bug moment
@0:03.5 - the variable popup for <<test>> in "a<<test>>a" closes as soon as the pointer moves toward it, so it can't be used. Clearest at 0:32.5-0:34.5 and 0:35.5-0:39.5: the Global popup for <<tio>> in "<<tio>>.com" (with the edit icon) keeps closing when the pointer heads for it. After removing the trailing text (0:22.0, 0:52.0) the popup stays open and the edit icon can be reached (0:23.5-0:26.0, 0:53.5-0:58.5).
