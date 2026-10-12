"""Check that a repro test really reproduces the video, not just *a* failure.

    uv run python -m dejabug.verify out/bug/ repro_test.py [--url http://localhost:5173]

1. Runs the test with DEJABUG_REPLAY_VIDEO set, so the harness records the replay.
2. Watches the replay with the same extractor used on the original video.
3. Aligns the two event sequences: the same clicks, the same text showing up,
   the same lists changing, in the same order.
4. Writes verify/report.md, verify/verdict.json and verify/strip.png
   (original frame | replay frame, one row per matched moment).

A test that fails for some unrelated reason (a timeout, a wrong locator, a
different bug) does not count: the replay has to walk through the video.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from dejabug.ingest import ingest
from dejabug.harness import NOT_REPRODUCED, REPRODUCED, SETUP_ERROR

MATCH = 0.5          # minimum similarity for two moments to count as the same
COMPATIBLE = {
    "click": {"click"},
    "list": {"list"},
    "show": {"show", "type"},
    "type": {"type", "show"},
    "nav": {"nav"},
}


@dataclass
class Moment:
    t: float
    kind: str
    text: str
    screen: str
    error: bool = False

    def __str__(self) -> str:
        label = f'"{self.text[:60]}"' if self.text else ""
        return f"{self.kind} {label}".strip()


def moments(events: list[dict]) -> list[Moment]:
    """The parts of an event log worth matching. Noise (text that vanished,
    unlabeled UI changes) is left out."""
    out = []
    for e in events:
        t, s, kind = e["t"], e.get("screen", ""), e["type"]
        if kind == "click":
            out.append(Moment(t, "click", e.get("label") or "", s))
        elif kind == "type":
            out.append(Moment(t, "type", e["text"], s))
        elif kind in ("text_appeared", "error_shown") and len(e["text"]) >= 3:
            out.append(Moment(t, "show", e["text"], s, error=kind == "error_shown"))
        elif kind == "text_changed" and len(e["to"]) >= 3:
            out.append(Moment(t, "show", e["to"], s))
        elif kind == "content_replaced":
            out.append(Moment(t, "list", " | ".join(e["after"]), s))
        elif kind == "panel_opened":
            out.append(Moment(t, "list", " | ".join(e["items"]), s))
        elif kind == "scroll":
            out.append(Moment(t, "list", "", s))
        elif kind == "nav":
            out.append(Moment(t, "nav", e["to"], s))
    return out


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def similarity(a: Moment, b: Moment) -> float:
    if b.kind not in COMPATIBLE.get(a.kind, set()):
        return 0.0
    if not a.text and not b.text:
        return 0.6
    if not a.text or not b.text:
        return 0.3
    if a.kind == "list":
        items_a = [i for i in a.text.split(" | ") if i]
        items_b = [i for i in b.text.split(" | ") if i]
        hits = sum(1 for i in items_a if max((_ratio(i, j) for j in items_b), default=0) >= 0.8)
        return hits / max(len(items_a), 1)
    # OCR merges neighbouring words ("Inception & Favorites"); allow containment.
    na, nb = _norm(a.text), _norm(b.text)
    if na and nb and (na in nb or nb in na):
        return max(0.8, _ratio(a.text, b.text))
    return _ratio(a.text, b.text)


def align(orig: list[Moment], replay: list[Moment]) -> list[tuple[int, int, float]]:
    """Best in-order pairing (weighted longest common subsequence)."""
    n, m = len(orig), len(replay)
    dp = np.zeros((n + 1, m + 1))
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            s = similarity(orig[i], replay[j])
            take = dp[i + 1, j + 1] + s if s >= MATCH else -1
            dp[i, j] = max(dp[i + 1, j], dp[i, j + 1], take)
    pairs, i, j = [], 0, 0
    while i < n and j < m:
        s = similarity(orig[i], replay[j])
        if s >= MATCH and dp[i, j] == dp[i + 1, j + 1] + s:
            pairs.append((i, j, s))
            i, j = i + 1, j + 1
        elif dp[i + 1, j] >= dp[i, j + 1]:
            i += 1
        else:
            j += 1
    return pairs


def strip(rows: list[tuple[Path | None, Path | None, str, bool]], dest: Path) -> None:
    W = 480
    tiles = []
    for left, right, caption, ok in rows:
        pair = []
        for path in (left, right):
            img = cv2.imread(str(path)) if path and path.exists() else None
            if img is None:
                img = np.full((270, W, 3), 40, np.uint8)
            img = cv2.resize(img, (W, int(img.shape[0] * W / img.shape[1])))
            img = img[:270] if img.shape[0] >= 270 else cv2.copyMakeBorder(
                img, 0, 270 - img.shape[0], 0, 0, cv2.BORDER_CONSTANT)
            pair.append(img)
        row = np.hstack([pair[0], np.full((270, 8, 3), 20, np.uint8), pair[1]])
        color = (80, 200, 80) if ok else (60, 60, 230)
        row = cv2.copyMakeBorder(row, 36, 4, 4, 4, cv2.BORDER_CONSTANT, value=color)
        cv2.putText(row, caption[:90], (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        tiles.append(row)
    header = np.full((40, tiles[0].shape[1], 3), 20, np.uint8)
    cv2.putText(header, "original video", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(header, "replay of the test", (W + 24, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imwrite(str(dest), np.vstack([header, *tiles]))


def verify(evidence: Path, test: Path, url: str | None = None) -> dict:
    out = evidence / "verify"
    out.mkdir(parents=True, exist_ok=True)
    video = (out / "replay.webm").resolve()
    video.unlink(missing_ok=True)

    env = {**os.environ, "DEJABUG_REPLAY_VIDEO": str(video)}
    if url:
        env["DEJABUG_URL"] = url
    run = subprocess.run([sys.executable, str(test)], env=env, capture_output=True, text=True)
    (out / "test_output.txt").write_text(run.stdout + run.stderr)

    verdict: dict = {"test_exit": run.returncode, "test_output": run.stdout.strip().splitlines()[-3:]}
    if not video.exists():
        verdict |= {"verdict": "ERROR", "why": "the test did not produce a replay video (does it use dejabug.harness.open_page?)"}
        return _finish(out, verdict, [])

    replay_events = ingest(video, out / "replay")
    actions = Path(str(video) + ".actions.jsonl")
    if actions.exists():
        # The harness logged the clicks it made; trust that over pixel guesses.
        logged = [json.loads(l) for l in actions.read_text().splitlines()]
        screens = sorted((out / "replay" / "keyframes").glob("*.png"))
        for a in logged:
            after = [p.stem for p in screens if float(p.stem[:-1]) >= a["t"]]
            a["screen"] = after[0] if after else screens[-1].stem
        replay_events = sorted([e for e in replay_events if e["type"] != "click"] + logged,
                               key=lambda e: e["t"])
    orig_events = [json.loads(l) for l in (evidence / "events.jsonl").read_text().splitlines()]
    orig, rep = moments(orig_events), moments(replay_events)
    pairs = align(orig, rep)
    matched = {i: (j, s) for i, j, s in pairs}

    # Text that never shows up anywhere in the replay belongs to whatever was
    # around the bug in the user's video (a docs page, other widgets). It is
    # context, not part of what the test has to reproduce.
    seen = " ".join(_norm(json.dumps(e, ensure_ascii=False)) for e in replay_events)
    context = {i for i, m in enumerate(orig)
               if i not in matched and m.kind == "show" and _norm(m.text) not in seen}
    in_scope = len(orig) - len(context)
    coverage = len(pairs) / max(in_scope, 1)
    tail = list(range(max(0, len(orig) - 3), len(orig)))
    ends_match = any(i in matched for i in tail)
    verdict |= {"moments_in_video": len(orig), "context_only": len(context), "matched": len(pairs),
                "coverage": round(coverage, 2),
                "final_moments_matched": ends_match}

    if run.returncode == SETUP_ERROR:
        verdict |= {"verdict": "SETUP_ERROR", "why": "the test could not reach the state shown in the video"}
    elif run.returncode == NOT_REPRODUCED:
        verdict |= {"verdict": "NOT_REPRODUCED", "why": "the test passed: the expected behaviour happened"}
    elif run.returncode != REPRODUCED:
        verdict |= {"verdict": "ERROR", "why": f"the test crashed (exit {run.returncode})"}
    elif coverage >= 0.5 and ends_match:
        verdict |= {"verdict": "REPRODUCED", "why": "the test fails, and its replay walks through the video"}
    else:
        verdict |= {"verdict": "FAILS_DIFFERENTLY",
                    "why": "the test fails, but its replay does not follow the video closely enough"}

    rows = []
    lines = []
    for i, m in enumerate(orig):
        if i in matched:
            j, s = matched[i]
            r = rep[j]
            lines.append(f"✓ {m.t:5.1f}s  {m}  ↔  replay {r.t:5.1f}s  ({s:.2f})")
            rows.append((evidence / "keyframes" / f"{m.screen}.png",
                         out / "replay" / "keyframes" / f"{r.screen}.png",
                         f"{m.t:.1f}s {m}  <->  {r.t:.1f}s  ({s:.2f})", True))
        elif i in context:
            lines.append(f"· {m.t:5.1f}s  {m}  (context: not part of the reproduced UI)")
        else:
            lines.append(f"✗ {m.t:5.1f}s  {m}  (not seen in replay)")
    if rows:
        strip(rows, out / "strip.png")
    return _finish(out, verdict, lines)


def _finish(out: Path, verdict: dict, lines: list[str]) -> dict:
    (out / "verdict.json").write_text(json.dumps(verdict, indent=2, ensure_ascii=False))
    report = [f"# {verdict['verdict']}", "", verdict.get("why", ""), ""]
    if lines:
        report += ["| | moment |", "|---|---|"] + [f"| {l[0]} | {l[2:]} |" for l in lines]
    report += ["", "Test output:", "```", *verdict.get("test_output", []), "```"]
    (out / "report.md").write_text("\n".join(report) + "\n")
    print("\n".join(lines))
    print(f"\n{verdict['verdict']}: {verdict.get('why', '')}")
    return verdict


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("evidence", type=Path, help="folder written by `dejabug.ingest` for the original video")
    ap.add_argument("test", type=Path, help="repro test script (uses dejabug.harness)")
    ap.add_argument("--url", help="run against this URL instead of the one in the test")
    a = ap.parse_args()
    v = verify(a.evidence, a.test, a.url)
    sys.exit(0 if v["verdict"] == "REPRODUCED" else 1)
