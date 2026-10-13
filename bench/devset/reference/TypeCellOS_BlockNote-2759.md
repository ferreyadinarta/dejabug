# Reference: TypeCellOS/BlockNote#2759
Video: videos/TypeCellOS_BlockNote-2759.mp4 (15.2 s). Graded from 2 fps keyframes, before seeing dejabug output.
App: La Suite Docs (French UI, logged in: "Se déconnecter", "Français") on a new "Document sans titre" with one empty BlockNote block (placeholder "Entrez du texte ou tapez '/' pour faire apparaître les options de mise en page"), Chrome DevTools Elements panel open on the right showing the block with data-id="initialBlockId". The bug itself is in BlockNote's side menu.
The repeated "+" clicks can't be counted exactly at 2 fps; they are inferred from the cursor resting on "+" and the DevTools panel flashing the editor's aria-expanded attribute.

## Actions (in order)
1. hover @0:00.0-0:01.5 - DevTools Elements nodes (editor div, bn-block-outer, bn-block); the matching block is highlighted on the page
2. hover @0:02.0 - the empty first block, then the "+" button of its side menu
3. click @0:03.0-0:05.0 - "+" (side menu add button), several times; no slash menu stays open
4. click @0:06.0 - the drag handle (⠿) next to "+" (block menu "Supprimer" / "Couleurs" opens)
5. click @0:07.0-0:09.0 - "+" again, several times (block menu closes; still no slash menu)
6. click @0:10.0 - the drag handle (block menu "Supprimer" / "Couleurs" opens again)
7. click @0:11.0 - in the empty block's text (block menu closes, caret in the block)
8. type @0:11.5-0:12.0 - "Test"
9. hover @0:12.5 - "+" next to the "Test" block
10. click @0:13.0 - "+" (a new empty block is added below "Test" and the slash menu opens: "Titres", "Titre 1", "Titre 2", "Titre 3", "Blocs de base", "Citation")
11. hover @0:14.0 - up toward the "Document sans titre" title (slash menu stays open)

## Bug moment
@0:03.0 - clicking "+" on the empty initial block (id "initialBlockId") of a new document doesn't open the slash menu (it opens and closes instantly). Once the block has content, "+" works (0:13.0).
