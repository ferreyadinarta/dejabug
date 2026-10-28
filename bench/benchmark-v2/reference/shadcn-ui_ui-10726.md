# Reference: shadcn-ui/ui#10726
Video: videos/shadcn-ui_ui-10726.mov (22.9 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: ui.shadcn.com docs (dark theme), Chrome with a Russian UI. The browser toolbar and address bar are not in the frame; the pointer is visible, and the status bar at the bottom left shows link URLs on hover.
Start state: the "Registry Directory" page (/docs/directory). The registry list below "Don't see a registry? Learn how to add it here." shows only grey skeleton rows (no search box, no registries).

## Actions (in order)
1. click @0:01.5-0:02.5 - top nav "Components" (status bar shows /docs/components at 0:02.0; the "Components" page opens at 0:02.5)
2. click @0:03.0-0:03.5 - top nav "Directory" (the "Registry Directory" page opens and the list loads at once: "Search", "197 registries", @8bitcn, @8starlabs-ui, @unlumen-ui, @auth0)
3. key @0:05.0 - page reload (unclear: no browser UI or context menu is visible between 0:04.5 and 0:05.0; most likely Cmd+R). The page reloads on /docs/directory and the list is skeleton rows again (0:05.0-0:07.0)
4. click @0:07.5-0:08.0 - top nav "Components" (Components page at 0:08.0)
5. click @0:09.0-0:09.5 - top nav "Directory" (list loads with 197 registries at 0:09.5)
6. right-click @0:10.0 - empty area left of the page content (Chrome context menu opens: "Назад", "Вперед", "Перезагрузить", "Сохранить как...", ...)
7. click @0:10.5-0:11.0 - "Перезагрузить" (Reload) in the context menu (the page reloads; skeleton rows from 0:11.5 to 0:16.5)
8. click @0:16.5-0:17.0 - top nav, on the border between "Directory" and "Create" (the page goes blank at 0:17.0, then the "Create" page with the theme designer opens, 0:17.5-0:18.5) (unclear: the status bar shows /docs/directory, but the page that opens is Create, so the click probably landed on "Create")
9. click @0:18.5-0:19.0 - top nav "Directory" (list loads with 197 registries at 0:19.0)
10. key @0:21.5 - page reload (unclear: no visible UI; probably Cmd+R again). The list is skeleton rows again until the end (0:21.5-0:22.5)

Not counted: @0:22.0 the pointer moves to the top edge of the screen (probably to stop the recording).

## Bug moment
@0:00.0 - when /docs/directory is loaded directly, the registry list stays an endless skeleton loader. This is shown again after each reload (0:05.0-0:07.0, 0:11.5-0:16.5, 0:21.5-0:22.5), while reaching the page through the top nav "Directory" link loads the 197 registries at once (0:03.5, 0:09.5, 0:19.0).
