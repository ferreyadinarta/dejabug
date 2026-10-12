# Repro Anything benchmark: seed set (v0, 2026-10-12)

`issues.json` lists 20 real, public GitHub issues. In each one, the reporter attached a screen recording of a bug in a web app that can run locally. Each entry records the video URL(s), the reporter's steps, expected vs actual behavior, a one-line local run command, whether login or seed data is needed, a difficulty rating and the fix PR/commit.

## How they were found
- GitHub Search API, unauthenticated and read-only (`gh` is not installed), with queries like
  `repo:<org>/<repo> is:issue is:closed "user-attachments/assets" in:body`, run against Excalidraw, tldraw, Gitea, Outline, Cal.com, Plane, Hoppscotch, n8n, Directus, MUI, Docusaurus, shadcn/ui, Chakra, Immich, Penpot and Memos.
- A body line was counted as a video when it held a bare `github.com/user-attachments/assets/<uuid>` link (GitHub renders those as `<video>`) or a `user-images...mp4/mov/webm` link. Links inside `<img>` or `![]()` were ignored.
- Each selected video was confirmed with an HTTP **HEAD** on the asset URL. The 302 redirect names the file extension (.mp4/.mov/.webm). No video was downloaded.
- Fix PRs and commits came from the issue timeline API (cross-referenced PRs and closing commits) and from the PR API (`merge_commit_sha`).
- The searches returned about 280 issues with videos. The 20 picks favour closed bugs with a merged fix, desktop browsers, and repros that need only UI actions.

## Composition
| Difficulty | Count | Issues |
|---|---|---|
| easy (pure UI state, no login) | 8 | excalidraw#10840, excalidraw#9423, docusaurus#11213, docusaurus#11232, mui#47203, mui#46665, tldraw#8828, chakra#10490 |
| medium (login and/or seeded data) | 8 | directus#26876, directus#26820, plane#7250, memos#6076, hoppscotch#6154, penpot#11549, immich#31746, outline#12552 |
| hard (timing, drag-and-drop, canvas) | 4 | tldraw#9457, tldraw#8480, excalidraw#9750, hoppscotch#5380 |

By app: Excalidraw 3, tldraw 3, Docusaurus 2, MUI 2, Directus 2, Hoppscotch 2, Chakra 1, Plane 1, Memos 1, Penpot 1, Immich 1, Outline 1.

## Using an entry
- `run_locally` usually checks out `<fix_commit>^1`, the parent of the fix's merge commit, so the bug is present. A good harness test **fails on `<fix>^1` and passes on `<fix>`**. Use that as the oracle for whether a bug was "reproduced".
- `steps_source` says whether the steps are the reporter's own or were derived from the description/video (tldraw#8828, tldraw#9457, tldraw#8480, excalidraw#9423).
- Some issues include a reference video of the expected behavior: excalidraw#9750 video 1 (the correct Alt-before-drag case), hoppscotch#5380 video 2 (after the fix) and docusaurus#11232 video 2 (the non-buggy hidden-navbar case).

## Caveats
- **Duration is not measured** (`duration_s: null`) because videos were not downloaded. Probe each video with ffprobe after downloading, and drop any outside 5–120 s.
- **No verified fix commit** for 2 of the 20:
  - chakra#10490 was closed with no linked PR.
  - plane#7250's community PR was closed without being merged.

  Expected behavior is clear for both, but check them on the target version first.
- mui#46665 and chakra#10490 need a small Vite harness app pinned to the affected package version, not a full app.
- Outline needs an auth provider (OIDC/Slack/Google, or SMTP magic link) and is the heaviest setup. Plane, Penpot and Immich need docker compose stacks. The run commands are best-effort one-liners and have not been executed.
- tldraw#8828 was handled as a behavior change rather than a pure bug.
- outline#12552 and immich#31746 are labelled medium but have timing components.
- Gitea, n8n and Cal.com produced no usable video issues with this search approach: their issue templates and attachment formats differ, and Cal.com's query returned 422. Searching those repos needs a different approach.
- Medium-tier repos: Directus 11.x is easiest to run (single docker run with SQLite). Memos is a single container.
