# Steps-mode accuracy, 20 real bug videos (2026-10-13)

## Founder hand re-grade: 5 cases
Picked after scoring with `random.Random(20261013).sample(sorted(case_ids), 5)` (seed **20261013**):

1. `xyflow_xyflow-5508`
2. `ueberdosis_tiptap-5472`
3. `excalidraw_excalidraw-8936`
4. `facebook_lexical-9126`
5. `ueberdosis_tiptap-7125`

For each case: video in `videos/`, reference in `reference/<id>.md`, dejabug output in `out/<id>/steps.md` (click close-ups in `out/<id>/clicks/`), and scores in `steps-accuracy.json`. Report disagreements as they are; don't resolve them quietly.

## Headline
| metric | value |
|---|---|
| issues scanned to find 20 | **308** (`scanned.csv`; query frozen in `query.txt`) |
| median click precision | **0.00** (16 cases with at least one listed action; also 0.00 when the 4 empty outputs count as 0). Mean 0.12. Pooled: 9 of 90 listed actions matched |
| median recall | **0.00** (mean 0.05). Pooled: 9 of 175 reference actions found |
| bug-moment hit rate | **4/20 (20%)** clear. 9/20 if the 5 borderline cases count |
| gap flags ("no click seen before this") | 11 flags, **11/11** at a real action that dejabug didn't list |
| lenient precision (right target, wrong action type allowed) | 20 of 90 (pooled) |

The numbers are low. In this sample, steps mode almost never produces a usable action list. Its notes ("X appeared / changed") and its gap flags are the parts that hold up.

dejabug version: package `0.1.1`. The repo has no `v0.1.1` git tag; the working tree was clean at `v0.1.0-9-g5bbd4c7`. `dejabug steps` ran with default settings, about 8 s per video, locally.

## Scoring rules used (set before scoring, written in the JSON)
- Action types: click, double/triple-click, right-click, hover, type, key, paste, drag, scroll. The type must match exactly.
- A listed action matches when it has the same type, the same target (by its label, or by the click close-up when it has no label) and the same order, within 1.5 s of the reference action's time range.
- Numbered steps are actions. Sub-bullet notes aren't actions, and "no click seen before this" notes are counted separately as gap flags.
- Bug moment = **yes** when a note lies within 1 s of a reference bug time and names the affected element or the visible symptom. Notes that only partly fit are marked *borderline* and count as **no**.
- Gap flag correct = a reference action that dejabug didn't match lies within 1 s of the flag.

## Per case
| id | sec | ref actions | listed | matched | precision | recall | bug moment | gap flags ok |
|---|---|---|---|---|---|---|---|---|
| TypeCellOS_BlockNote-1875 | 9 | 5 | 0 | 0 | n/a | 0.00 | yes | 0/0 |
| TypeCellOS_BlockNote-2020 | 28 | 19 | 3 | 0 | 0.00 | 0.00 | no | 0/0 |
| TypeCellOS_BlockNote-2109 | 19 | 4 | 13 | 0 | 0.00 | 0.00 | no (borderline) | 0/0 |
| TypeCellOS_BlockNote-2378 | 12 | 4 | 2 | 1 | 0.50 | 0.25 | yes | 0/0 |
| TypeCellOS_BlockNote-2559 | 30 | 7 | 11 | 3 | 0.27 | 0.43 | no (borderline) | 1/1 |
| adobe_react-spectrum-6809 | 15 | 9 | 6 | 1 | 0.17 | 0.11 | no (borderline) | 0/0 |
| excalidraw_excalidraw-8936 | 23 | 7 | 7 | 0 | 0.00 | 0.00 | yes | 0/0 |
| excalidraw_excalidraw-9277 | 38 | 17 | 7 | 1 | 0.14 | 0.06 | no (borderline) | 0/0 |
| excalidraw_excalidraw-9423 | 20 | 4 | 2 | 0 | 0.00 | 0.00 | no | 0/0 |
| facebook_lexical-8885 | 11 | 5 | 4 | 0 | 0.00 | 0.00 | no | 3/3 |
| facebook_lexical-9126 | 17 | 11 | 4 | 0 | 0.00 | 0.00 | no | 0/0 |
| mui_mui-x-20364 | 18 | 12 | 2 | 1 | 0.50 | 0.08 | no (borderline) | 0/0 |
| mui_mui-x-23735 | 11 | 2 | 8 | 0 | 0.00 | 0.00 | no | 0/0 |
| tldraw_tldraw-6191 | 9 | 4 | 0 | 0 | n/a | 0.00 | no | 0/0 |
| ueberdosis_tiptap-5472 | 16 | 10 | 0 | 0 | n/a | 0.00 | no | 1/1 |
| ueberdosis_tiptap-7125 | 13 | 4 | 3 | 0 | 0.00 | 0.00 | no | 1/1 |
| ueberdosis_tiptap-8014 | 46 | 32 | 7 | 2 | 0.29 | 0.06 | yes | 5/5 |
| ueberdosis_tiptap-8164 | 9 | 6 | 9 | 0 | 0.00 | 0.00 | no | 0/0 |
| ueberdosis_tiptap-8334 | 17 | 10 | 0 | 0 | n/a | 0.00 | no | 0/0 |
| xyflow_xyflow-5508 | 11 | 3 | 2 | 0 | 0.00 | 0.00 | no | 0/0 |

The JSON has a one-line note for each case.

## The 3 most common failure reasons
1. **Keyboard-driven steps don't become actions (12/20 cases).** Typing, Enter, Shift+Enter, paste, undo and shortcut keys are what reproduce most editor bugs. dejabug reports them at most as text-change notes or a gap flag. Examples: tiptap-8334 (type URL, paste, space: 0 actions listed), tiptap-5472 (ArrowUp at the start of a code block: 0 actions), BlockNote-1875/2378 (Enter on a toggle: missing), tldraw-6191 ("w" to rotate while dragging: 0 actions).
2. **Clicks on the wrong target, or clicks that never happened (13/20 cases have at least one).** When the pointer is hidden or idle, dejabug reports clicks where it rests or on static page elements. Examples: excalidraw-8936 (7 clicks on the resting pointer in empty canvas while the user types and scrolls), BlockNote-2020 (3 clicks on the GitHub/StackBlitz header), mui-x-23735 (clicks and a "Type" on the "MUI X Missing license key" watermark when the user only scrolled), lexical-8885 (click on the "Discord Server" link labelled "Quote"; the close-up shows the Underline button). Text recognition (OCR) errors in labels make it worse ("Open, Pialog Editor", "Click on the chart" for a reset icon).
3. **Drags, scrubs, double-clicks, right-clicks and scrolls reduced to click/hover (8/20 cases).** Examples: BlockNote-2109 (two drags of the "List" handle became 2 clicks and 4 hovers on "List"), excalidraw-9423 (scrubbing the X label became two clicks on the X value), xyflow-5508 (node and resize-handle drags became two hovers on "Resize"), tiptap-8014 (right-click on a selection listed as a click). With the action type relaxed, pooled matches go from 9 to 20.

What works: gap flags were right every time (11/11), but they are rare (5 cases). In 4 cases a plain note sits right on the bug: BlockNote-1875 "Toggle appeared", BlockNote-2378 "Empty toggle... appeared", excalidraw-8936 "scrolled down 187 px", and tiptap-8014 "the list changed to: Explore the magic, of having AI that sea, …" (the split paragraphs).

## By app type
| group | cases | median precision | median recall | matched / reference actions | bug moment (clear) |
|---|---|---|---|---|---|
| forms/lists (react-spectrum form, MUI X timeline) | 2 | 0.08 | 0.06 | 1 / 11 | 0/2 |
| canvas/drawing (excalidraw ×3, tldraw, xyflow) | 5 | 0.00 | 0.00 | 1 / 35 | 1/5 |
| other: rich-text editors (BlockNote ×5, tiptap ×5, lexical ×2) + MUI X chart | 13 | 0.00 | 0.00 | 7 / 129 | 3/13 |

The sample is mostly rich-text editors (12/20). That comes from the frozen repo list and the most-recently-closed order, not from choice. The forms/lists group has only 2 cases, so no conclusion can be drawn about it.

## Caveats
- One grader (this agent) wrote all 20 references from 1–2 fps keyframes, before seeing any dejabug output. Some reference actions are inferred from visible effects (e.g. "leave editing", keyboard focus moves), and recordings with a hidden pointer (BlockNote, tiptap typing) make the counts uncertain. The founder re-grade above checks this.
- The frozen fix rule in `query.txt` requires a closing keyword or a GitHub-linked closing PR. Four issues with an obviously merged fix PR were skipped under it (tldraw#8828, material-ui#49038, mui-x#14906, BlockNote#2801); see `scanned.csv`.
- Condition 4 was judged from the repos without setting anything up. react-spectrum#10220 was skipped because its bug exists only in VoiceOver speech. Desktop Safari-only bugs (lexical#8885, #9126) were kept.
- Bug-moment calls for "absence" bugs (missing focus ring, missing drop indicator, a dropped click) are inherently borderline; 5 are marked as such and counted as no.
