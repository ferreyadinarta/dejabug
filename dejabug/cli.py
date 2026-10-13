"""dejabug: turn a screen recording of a bug into a test that fails the same way."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dejabug import __version__

GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def _say(msg: str) -> None:
    print(msg, flush=True)


def cmd_watch(a: argparse.Namespace) -> int:
    from dejabug.ingest import ingest

    out = a.out or Path("dejabug-out") / a.video.stem
    events = ingest(a.video, out)
    _say(f"{len(events)} events -> {out / 'events.jsonl'}\ncontact sheet -> {out / 'contact_sheet.png'}")
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    from dejabug.verify import verify

    v = verify(a.evidence, a.test, a.url)
    return 0 if v["verdict"] == "REPRODUCED" else 1


def cmd_test(a: argparse.Namespace) -> int:
    """Run a repro test with the Python that has dejabug installed."""
    import os
    import subprocess

    env = {**os.environ, **({"DEJABUG_URL": a.url} if a.url else {})}
    return subprocess.run([sys.executable, str(a.test)], env=env).returncode


def cmd_run(a: argparse.Namespace) -> int:
    from dejabug.agent import build_prompt, run_agent
    from dejabug.ingest import ingest
    from dejabug.verify import verify

    out = (a.out or Path("dejabug-out") / a.video.stem).resolve()
    test = out / "repro_test.py"
    started = time.monotonic()

    _say(f"{BOLD}dejabug{RESET} {DIM}{__version__}{RESET}  {a.video.name} -> {a.url}\n")
    _say(f"{BOLD}1. watch{RESET}   reading the video")
    events = ingest(a.video, out)
    clicks = sum(e["type"] == "click" for e in events)
    _say(f"          {len(events)} moments, {clicks} clicks  {DIM}{out / 'contact_sheet.png'}{RESET}\n")

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
        if code != 0 or not test.exists():
            _say(f"          {RED}agent did not produce a test (exit {code}); see agent_attempt{attempt}.log{RESET}")
            continue
        _say(f"          {DIM}{test}{RESET}\n")

        _say(f"{BOLD}3. verify{RESET}  replaying the test and comparing it with the video")
        verdict = verify(out, test, a.url)
        if verdict["verdict"] == "REPRODUCED":
            break
        feedback = (out / "verify" / "report.md").read_text()
        _say("")

    took = time.monotonic() - started
    final = verdict.get("verdict", "ERROR")
    color = GREEN if final == "REPRODUCED" else RED
    _say(f"\n{color}{BOLD}{final}{RESET}  in {took:.0f}s")
    if spent["turns"]:
        _say(f"  agent:  ${spent['cost_usd']:.2f}, {spent['input_tokens'] // 1000}k tokens in, "
             f"{spent['output_tokens'] // 1000}k out, {spent['turns']} turns")
    if final == "REPRODUCED":
        _say(f"  test:   {test}\n  proof:  {out / 'verify' / 'strip.png'}")
    (out / "result.json").write_text(json.dumps({**verdict, "seconds": round(took), "agent": spent}, indent=2))
    return 0 if final == "REPRODUCED" else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="dejabug", description=__doc__.split("\n\n")[0])
    ap.add_argument("--version", action="version", version=f"dejabug {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="video -> verified failing test (the whole loop)")
    r.add_argument("video", type=Path)
    r.add_argument("--url", required=True, help="where the app from the video is running")
    r.add_argument("-o", "--out", type=Path, help="output folder (default: dejabug-out/<video name>)")
    r.add_argument("--note", help="anything the reporter said about the bug")
    r.add_argument("--tries", type=int, default=3, help="attempts before giving up (default 3)")
    r.add_argument("--model", default=os.environ.get("DEJABUG_MODEL", "sonnet"),
                   help="model for the agent (default: sonnet)")
    r.add_argument("--max-cost", type=float, default=float(os.environ.get("DEJABUG_MAX_COST", "1.50")),
                   help="stop when the agent has spent this many US dollars (default 1.50)")
    r.add_argument("--blind", action="store_true",
                   help="forbid the agent from looking the bug up (for benchmarks)")
    r.set_defaults(fn=cmd_run)

    w = sub.add_parser("watch", help="video -> event log + contact sheet")
    w.add_argument("video", type=Path)
    w.add_argument("-o", "--out", type=Path)
    w.set_defaults(fn=cmd_watch)

    v = sub.add_parser("verify", help="check that a test reproduces the video")
    v.add_argument("evidence", type=Path, help="folder from `dejabug watch`")
    v.add_argument("test", type=Path)
    v.add_argument("--url")
    v.set_defaults(fn=cmd_verify)

    t = sub.add_parser("test", help="run a repro test (exit 1 = bug reproduced)")
    t.add_argument("test", type=Path)
    t.add_argument("--url", help="run against this URL instead of the one in the test")
    t.set_defaults(fn=cmd_test)

    for p in (r, v, t):
        p.add_argument("--storage-state", type=Path,
                       help="Playwright storage state file (cookies, local storage) so tests start logged in")
    a = ap.parse_args(argv)
    if a.storage_state:
        os.environ["DEJABUG_STORAGE_STATE"] = str(a.storage_state.resolve())
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
