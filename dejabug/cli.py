"""dejabug: turn a screen recording of a bug into a test that fails the same way."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

from dejabug import __version__

GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def _say(msg: str) -> None:
    print(msg, flush=True)


def _need_playwright() -> None:
    import importlib.util

    if importlib.util.find_spec("playwright") is None:
        sys.exit("Test mode needs Playwright. Install it with:  pip install 'dejabug[run]'\n"
                 "or run through uvx:  uvx --from 'dejabug[run]' dejabug run ...")


def _input(a: argparse.Namespace) -> tuple[Path, Path]:
    from dejabug.source import resolve

    video, name = resolve(a.video, Path("dejabug-out"))
    return video, (a.out or Path("dejabug-out") / name).resolve()


def cmd_watch(a: argparse.Namespace) -> int:
    from dejabug.ingest import ingest

    video, out = _input(a)
    events = ingest(video, out)
    _say(f"{len(events)} events -> {out / 'events.jsonl'}\nfilm (every 0.5 s, changes boxed) -> {out / 'film'}\n"
         f"contact sheet -> {out / 'contact_sheet.png'}")
    return 0


MAX_ISSUE_CHARS = 4000


def _context(a: argparse.Namespace, video: Path) -> str:
    """The reporter's note, or the issue's title and text when the video came from an issue link."""
    issue = video.parent / "issue.md"
    if a.note:
        return f"What the reporter said: {a.note}"
    if not issue.exists():
        return ""
    text = re.sub(r"https?://\S+", "", issue.read_text(encoding="utf-8"))[:MAX_ISSUE_CHARS]
    return ("The issue the video came from is below. Use it to understand the bug and name things, "
            f"but list only actions the video shows.\n\n<issue>\n{text}\n</issue>")


def _ai_steps(a: argparse.Namespace, out: Path, video: Path) -> str | None:
    from dejabug import vision
    from dejabug.agent import build_steps_prompt, run_agent
    from dejabug.steps import ai_markdown, tidy

    target = out / "steps.json"
    target.unlink(missing_ok=True)
    custom = os.environ.get("DEJABUG_AGENT")
    if not custom and not vision.available():
        _say(f"{RED}--ai needs Claude Code (https://claude.com/claude-code) or ANTHROPIC_API_KEY{RESET}")
        return None
    _say(f"{DIM}a model is reading the film...{RESET}")
    if custom:  # other agents read the files themselves
        code, usage = run_agent(build_steps_prompt(out, target, _context(a, video)), out, out / "agent_steps.log",
                                a.model, a.max_cost)
        if not target.exists():
            _say(f"{RED}no steps written (exit {code}); see {out / 'agent_steps.log'}{RESET}")
            return None
    else:
        usage = vision.write_steps(build_steps_prompt(out, target, _context(a, video), api=True), out, target, a.model,
                                   check=os.environ.get("DEJABUG_CHECK", "1") == "1")
    data = tidy(json.loads(target.read_text(encoding="utf-8")))
    target.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    if usage.get("cost_usd"):
        _say(f"{DIM}model: ${usage['cost_usd']:.2f}{RESET}")
    return ai_markdown(data, a.video)


def cmd_steps(a: argparse.Namespace) -> int:
    from dejabug.ingest import ingest
    from dejabug.steps import load, markdown

    video, out = _input(a)
    if not (a.reuse and (out / "events.jsonl").exists() and (out / "film").exists()):
        ingest(video, out)
    if a.ai:
        md = _ai_steps(a, out, video)
        if md is None:
            return 1
    else:
        md = markdown(load(out), a.video)
    (out / "steps.md").write_text(md, encoding="utf-8")
    _say(md)
    _say(f"{DIM}saved to {out / 'steps.md'}; close-ups of each click are in {out / 'clicks'}{RESET}")
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    _need_playwright()
    from dejabug.verify import verify

    v = verify(a.evidence, a.test, a.url)
    return 0 if v["verdict"] == "REPRODUCED" else 1


def cmd_doctor(a: argparse.Namespace) -> int:
    from dejabug.doctor import main as doctor

    return doctor()


def cmd_test(a: argparse.Namespace) -> int:
    _need_playwright()
    """Run a repro test with the Python that has dejabug installed."""
    import os
    import subprocess

    env = {**os.environ, **({"DEJABUG_URL": a.url} if a.url else {})}
    return subprocess.run([sys.executable, str(a.test)], env=env).returncode


def cmd_run(a: argparse.Namespace) -> int:
    _need_playwright()
    from dejabug.agent import build_port_prompt, build_prompt, run_agent
    from dejabug.ingest import ingest
    from dejabug.verify import verify

    from dejabug.steps import load, test_draft

    video, out = _input(a)
    test = out / "repro_test.py"
    started = time.monotonic()

    _say(f"{BOLD}dejabug{RESET} {DIM}{__version__}{RESET}  {video.name} -> {a.url}\n")
    _say(f"{BOLD}1. watch{RESET}   reading the video")
    events = ingest(video, out)
    steps = load(out)
    actions = sum(s.kind != "note" for s in steps)
    if not test.exists():
        test.write_text(test_draft(steps, a.url), encoding="utf-8")
    _say(f"          {len(events)} moments, {actions} user actions drafted as a test  {DIM}{out / 'contact_sheet.png'}{RESET}\n")

    feedback, verdict = "", {}
    spent = {"cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "turns": 0}
    for attempt in range(1, a.tries + 1):
        _say(f"{BOLD}2. write{RESET}   attempt {attempt}/{a.tries}: agent is writing the repro test")
        prompt = build_prompt(out, a.url, test, note=a.note or "", blind=a.blind, feedback=feedback)
        left = a.max_cost - spent["cost_usd"]
        if left < 0.05:
            _say(f"          {RED}budget of ${a.max_cost:.2f} used up{RESET}")
            break
        code, usage = run_agent(prompt, out, out / f"agent_attempt{attempt}.log", a.model, left)
        for k, v in usage.items():
            spent[k] += v
        if not test.exists():
            _say(f"          {RED}agent did not produce a test (exit {code}); see agent_attempt{attempt}.log{RESET}")
            continue
        _say(f"          {DIM}{test}{RESET}\n")

        _say(f"{BOLD}3. verify{RESET}  replaying the test and comparing it with the video")
        verdict = verify(out, test, a.url)
        if verdict["verdict"] == "REPRODUCED":
            break
        feedback = (out / "verify" / "report.md").read_text(encoding="utf-8")
        _say("")

    spec = out / "repro.spec.ts"
    if a.format == "ts" and verdict.get("verdict") == "REPRODUCED":
        _say(f"\n{BOLD}4. port{RESET}    agent is porting the test to @playwright/test (TypeScript)")
        code, usage = run_agent(build_port_prompt(test, spec, a.url), out, out / "agent_port.log", a.model,
                                max(a.max_cost - spent["cost_usd"], 0.25), extra_tools=("Bash(npx *)",))
        for k, v in usage.items():
            spent[k] += v
        _say(f"          {DIM}{spec}{RESET}" if spec.exists() else f"          {RED}no spec written; see agent_port.log{RESET}")

    took = time.monotonic() - started
    final = verdict.get("verdict", "ERROR")
    color = GREEN if final == "REPRODUCED" else RED
    _say(f"\n{color}{BOLD}{final}{RESET}  in {took:.0f}s")
    if spent["turns"]:
        _say(f"  agent:  ${spent['cost_usd']:.2f}, {spent['input_tokens'] // 1000}k tokens in, "
             f"{spent['output_tokens'] // 1000}k out, {spent['turns']} turns")
    if final == "REPRODUCED":
        _say(f"  test:   {test}\n  proof:  {out / 'verify' / 'strip.png'}")
        if spec.exists():
            _say(f"  spec:   {spec}")
    (out / "result.json").write_text(json.dumps({**verdict, "seconds": round(took), "agent": spent}, indent=2), encoding="utf-8")
    return 0 if final == "REPRODUCED" else 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows consoles default to a code page without ✓ or →
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="dejabug", description=__doc__.split("\n\n")[0])
    ap.add_argument("--version", action="version", version=f"dejabug {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="video -> verified failing test (the whole loop)")
    r.add_argument("video", help="video file or GitHub issue link")
    r.add_argument("--url", required=True, help="where the app from the video is running")
    r.add_argument("-o", "--out", type=Path, help="output folder (default: dejabug-out/<video name>)")
    r.add_argument("--note", help="anything the reporter said about the bug")
    r.add_argument("--tries", type=int, default=3, help="attempts before giving up (default 3)")
    r.add_argument("--model", default=os.environ.get("DEJABUG_MODEL", "sonnet"),
                   help="model for the agent (default: sonnet)")
    r.add_argument("--max-cost", type=float, default=float(os.environ.get("DEJABUG_MAX_COST", "1.50")),
                   help="stop when the agent has spent this many US dollars (default 1.50)")
    r.add_argument("--format", choices=("py", "ts"), default="py",
                   help="ts: also write a @playwright/test TypeScript spec once the bug is reproduced")
    r.add_argument("--blind", action="store_true",
                   help="forbid the agent from looking the bug up (for benchmarks)")
    r.set_defaults(fn=cmd_run)

    w = sub.add_parser("watch", help="video -> film, event log and contact sheet (evidence only)")
    w.add_argument("video", help="video file or GitHub issue link")
    w.add_argument("-o", "--out", type=Path)
    w.set_defaults(fn=cmd_watch)

    s = sub.add_parser("steps", help="video -> written steps to reproduce (no app needed)")
    s.add_argument("video", help="video file or GitHub issue link")
    s.add_argument("-o", "--out", type=Path)
    s.add_argument("--ai", action="store_true", help="have a model write the steps from the evidence (uses Claude Code)")
    s.add_argument("--note", help="anything the reporter said about the bug")
    s.add_argument("--reuse", action="store_true", help="reuse what an earlier run already extracted into the output folder")
    s.add_argument("--model", default=os.environ.get("DEJABUG_STEPS_MODEL", "opus"))
    s.add_argument("--max-cost", type=float, default=float(os.environ.get("DEJABUG_MAX_COST", "1.00")))
    s.set_defaults(fn=cmd_steps)

    v = sub.add_parser("verify", help="check that a test reproduces the video")
    v.add_argument("evidence", type=Path, help="folder from `dejabug watch`")
    v.add_argument("test", type=Path)
    v.add_argument("--url")
    v.set_defaults(fn=cmd_verify)

    d = sub.add_parser("doctor", help="check what dejabug needs and how to fix anything missing")
    d.set_defaults(fn=cmd_doctor)

    t = sub.add_parser("test", help="run a repro test (exit 1 = bug reproduced)")
    t.add_argument("test", type=Path)
    t.add_argument("--url", help="run against this URL instead of the one in the test")
    t.set_defaults(fn=cmd_test)

    for p in (r, v, t):
        p.add_argument("--storage-state", type=Path,
                       help="Playwright storage state file (cookies, local storage) so tests start logged in")
    a = ap.parse_args(argv)
    if getattr(a, "storage_state", None):
        os.environ["DEJABUG_STORAGE_STATE"] = str(a.storage_state.resolve())
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
