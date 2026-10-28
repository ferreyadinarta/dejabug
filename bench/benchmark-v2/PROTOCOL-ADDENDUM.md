# Benchmark v2: protocol addendum

Written and committed on 2026-10-28, before any v2 candidate was looked at and before any v2 run. Everything in [PROTOCOL.md](../PROTOCOL.md) applies; this file adds one thing and fixes the scoring summary.

## Two conditions

1. **Bare video (the headline result).** `dejabug steps <video>` with default settings, as PROTOCOL.md says. This is the number reported first and the one the pass bar applies to.
2. **With the issue text (secondary).** The same command with `--report <id>.md`, where `<id>.md` is the issue body as it was at scan time, saved under `issues/` when the case is set up. This matches how dejabug is mostly used (an issue link or a ticket), and is reported next to the headline, never instead of it.

Both conditions run on the same tagged version, one run each, on the same 20 videos.

## Scoring

Same references and the same model judge (`bench/score.py`) for both conditions, as in the first benchmark: median recall (failures count as 0), pooled precision, and how many of the 20 name the bug moment. The founder re-grades 5 cases picked at random after scoring.

**Pass bar (bare video):** median recall of at least 0.6 and pooled precision of at least 0.7, the same as before.

The result is published whatever it is.

## Video choice (added 2026-10-28, before any v2 run)

The scan took the first video in the issue body. Only one case has more than one: TypeCellOS/BlockNote#2760 has four, and the first is the reporter's "0_47_3_OK.mov", the working version, which shows no bug. The grader caught this while writing the reference. As in v1, where BlockNote#1875's second video was a comparison and wasn't used, the case uses the video that shows the bug: "0_51_1_error.mov" (asset b477af80). `cases.json` was changed to match and the reference was written from that video. No dejabug output existed for any v2 video at that point.

## Hovers (added 2026-10-28, before any v2 run)

The v2 graders listed far more hovers than v1's references (45 of 208 actions, against 3 of 174), which would have made the two results hard to compare. The references follow v1's practice: a hover is listed only when it causes a visible change the user then uses or the bug depends on, such as a menu, submenu, tooltip, popup or handle appearing. The pointer passing over items on its way somewhere else, or resting with no visible change, is not an action. Ten hovers were removed on that basis, leaving 198 actions. No dejabug output existed for any v2 video at that point.
