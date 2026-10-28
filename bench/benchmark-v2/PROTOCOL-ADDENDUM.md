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
