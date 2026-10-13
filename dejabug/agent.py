"""Hand the extracted evidence to a coding agent (DEJABUG_AGENT overrides the default, Claude Code)."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
from importlib import resources
from pathlib import Path

BLIND_RULES = """
Work only from the video evidence and the running app. Do not search the web,
issue trackers or changelogs for this bug, and do not read the app's source code
to find it.
""".strip()


def build_prompt(evidence: Path, url: str, test: Path, note: str = "", blind: bool = False,
                 feedback: str = "") -> str:
    template = resources.files("dejabug").joinpath("prompts/write_repro.md").read_text()
    prompt = (template
              .replace("{evidence}", str(evidence.resolve()))
              .replace("{url}", url)
              .replace("{test}", str(test.resolve()))
              .replace("{python}", shlex.quote(sys.executable))
              .replace("{note}", f"\nWhat the reporter said about the bug: {note}\n" if note else "")
              .replace("{rules}", f"\n{BLIND_RULES}\n" if blind else ""))
    if feedback:
        prompt += (
            "\n\n## Your previous attempt\n\n"
            "dejabug replayed your test and compared the replay with the video. Its report:\n\n"
            f"{feedback}\n\n"
            "Fix the test so the replay follows the video (✗ lines are moments the replay "
            "did not show) and it fails on the bug itself. Edit the existing file."
        )
    return prompt


def run_agent(prompt: str, workdir: Path, log: Path, model: str = "sonnet", budget: float | None = None) -> tuple[int, dict]:
    workdir.mkdir(parents=True, exist_ok=True)
    prompt_file = workdir / "agent_prompt.md"
    prompt_file.write_text(prompt)

    custom = os.environ.get("DEJABUG_AGENT")
    if custom:
        cmd = shlex.split(custom.replace("{prompt_file}", str(prompt_file)))
        cmd = [c.replace("{prompt}", prompt) for c in cmd]
    else:
        if not shutil.which("claude"):
            sys.exit("dejabug needs a coding agent. Install Claude Code (https://claude.com/claude-code) "
                     "or set DEJABUG_AGENT to another agent's command.")
        py = sys.executable
        cmd = [
            "claude", "-p", prompt,
            "--permission-mode", "acceptEdits",
            "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep",
            f"Bash({py} *)", f"Bash({shlex.quote(py)} *)",
            "--add-dir", str(workdir.resolve()),
            "--output-format", "json",
            "--model", model,
        ]
        if budget:
            cmd += ["--max-budget-usd", f"{budget:.2f}"]
    run = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)
    usage: dict = {}
    text = run.stdout
    if not custom:
        try:
            data = json.loads(run.stdout)
            text = data.get("result", "")
            u = data.get("usage") or {}
            usage = {"cost_usd": data.get("total_cost_usd") or 0.0,
                     "input_tokens": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                     "output_tokens": u.get("output_tokens", 0),
                     "turns": data.get("num_turns", 0)}
        except (json.JSONDecodeError, AttributeError):
            pass
    log.write_text(text + run.stderr)
    return run.returncode, usage
