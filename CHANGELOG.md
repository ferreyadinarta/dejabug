# Changelog

## 0.2.1 — 2026-10-22
- Timeout raised to 30 minutes per model call (0.2.0 timed out on long videos and reported nothing).
- Retries once on a dropped connection.
- Published the 0.2.0 benchmark result (did not pass: 8 of 20 timed out before that fix).

## 0.2.0 — 2026-10-16
- The model now watches the recording and writes the steps; the old frame-by-frame heuristic is gone.
- A second model call checks every step against the frames.
- Full-size close-ups of small changes sent alongside the film.
- `DEJABUG_EFFORT`: controls how hard the model thinks (`--effort` in Claude Code, thinking budget in the API).
- A sweep of all frames finds actions the first draft missed.
- Steps are written at the level a person uses in a bug report, not as low-level mouse events.
- `--no-ai` still gives a labelled local timeline without any model call.

## 0.1.1 — 2026-10-13
- Playwright moved to an optional extra (`pip install dejabug[run]`); steps mode works without it.
- Windows: fixed a crash on cp1252 consoles (UTF-8 output now forced).
- CI checks a clean pip install on Linux, macOS and Windows.
- `dejabug doctor`: GitHub reachability check is optional again; a rate-limited reply counts as reachable.

## 0.1.0 — 2026-10-13
- First release.
- `dejabug steps`: video to steps to reproduce (runs locally, no model needed).
- `dejabug run`: video to verified Playwright test (beta, Claude Code only).
- `dejabug steps <issue-url>`: downloads the attached video and uses the issue text as context.
- `dejabug doctor`: checks that required tools are installed and prints one fix per missing piece.
- GitHub Action: comments steps on issues that have a bug video attached.
- CI on Linux, macOS and Windows.
