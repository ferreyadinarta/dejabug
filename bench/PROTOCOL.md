# Benchmark protocol

Written and committed on 2026-10-13, before any benchmark run. Results are judged only by the rules below.

## Sample

- Source: closed GitHub issues, collected with one frozen search query. The exact query and the date it was run are recorded in `bench/benchmark/query.txt` before any case is set up.
- Taken in order, most recently closed first, until 20 cases qualify.
- A case qualifies when the issue:
  1. has a `bug` label (or the repo's equivalent, listed in `query.txt`),
  2. has a screen recording attached (mp4, mov or webm),
  3. is fixed by a merged commit or pull request linked from the issue,
  4. is in a web app that runs locally with `npm install` and needs no external service, login or seeded data.
- Every issue looked at is logged in `bench/benchmark/scanned.csv` with the reason it was skipped. The number of issues scanned to find 20 is reported next to the result.

Condition 4 makes this sample easier than real-world bug videos. The result says nothing about apps that need a backend, a login or production data.

## Versions

- "Before" is the code just before the fix; "after" includes the fix.
- Where the fix shipped in a package release, "before" is the last release without the fix and "after" the first release with it. Otherwise both are built from the repository at the commit before the fix and at the fix commit. Which one was used is recorded per case.
- The app around the component is kept as close to the video as reasonably possible (same demo content, same props).

## Run

- `dejabug run <video> --url <before build> --blind` with default settings (model `sonnet`, budget $1.50, up to 3 attempts), on dejabug's version tagged when the benchmark starts.
- The fix build is started only after the run ends.
- Nobody edits the generated test.

## Success

A case is a **success** only if both hold:

1. `dejabug run` ends with `REPRODUCED` on the before build, and
2. the same test, unchanged, exits `0` on the after build.

`REPRODUCED` on before but not `0` on after is a **false positive**. Anything else is a **failure**. A case whose setup can't reach the state shown in the video is reported as **setup failed** and still counts in the denominator.

## Reporting

- Success rate = successes / 20, published whatever it is, with per-case cost, time and outcome.
- With 20 cases the uncertainty is wide: a measured 50% is consistent with roughly 30% to 70%. Decisions treat the result as a rough signal.
