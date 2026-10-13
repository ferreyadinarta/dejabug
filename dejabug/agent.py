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
    template = resources.files("dejabug").joinpath("prompts/write_repro.md").read_text(encoding="utf-8")
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


TS_CONFIG = """export default {
  testDir: '.',
  testMatch: 'repro.spec.ts',
  use: {
    channel: process.env.DEJABUG_BROWSER === 'chromium' ? undefined : 'chrome',
    storageState: process.env.DEJABUG_STORAGE_STATE || undefined,
  },
};
"""


def playwright_version() -> str:
    from importlib.metadata import version

    return version("playwright")


def prepare_ts_project(folder: Path) -> None:
    """Minimal npm project so the spec can import @playwright/test."""
    pkg = folder / "package.json"
    if not pkg.exists():
        pkg.write_text('{"private": true, "devDependencies": {"@playwright/test": "%s"}}\n' % playwright_version(), encoding="utf-8")
    if not (folder / "node_modules" / "@playwright" / "test").exists():
        subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=folder, check=True)
    (folder / "playwright.dejabug.config.ts").write_text(TS_CONFIG, encoding="utf-8")


def build_port_prompt(test: Path, spec: Path, url: str) -> str:
    prepare_ts_project(spec.parent)
    template = resources.files("dejabug").joinpath("prompts/port_ts.md").read_text(encoding="utf-8")
    return (template
            .replace("{test}", str(test.resolve()))
            .replace("{spec}", str(spec.resolve()))
            .replace("{spec_name}", spec.name)
            .replace("{config_name}", "playwright.dejabug.config.ts")
            .replace("{url}", url)
            .replace("{npx}", "npx")
            .replace("{pw_version}", playwright_version()))


def build_steps_prompt(evidence: Path, out: Path, note: str = "", api: bool = False) -> str:
    template = resources.files("dejabug").joinpath("prompts/write_steps.md").read_text(encoding="utf-8")
    if api:  # one-shot call: the sheets and events are attached, nothing else can be opened
        template = (template.replace("Save `{out}` as JSON:", "Reply with only this JSON:")
                    .replace("Write only the JSON file, then reply with one line: how many steps and the bug moment.\n", "")
                    .replace("## Evidence in {evidence}", "## Evidence (attached below: the film sheets, then events.jsonl; "
                             "full-size frames, keyframes and click close-ups are not available)"))
    return (template.replace("{{", "{").replace("}}", "}")
            .replace("{evidence}", str(evidence.resolve()))
            .replace("{out}", str(out.resolve()))
            .replace("{note}", f"\nWhat the reporter said: {note}\n" if note else ""))


def run_agent(prompt: str, workdir: Path, log: Path, model: str = "sonnet", budget: float | None = None,
              extra_tools: tuple[str, ...] = ()) -> tuple[int, dict]:
    workdir.mkdir(parents=True, exist_ok=True)
    prompt_file = workdir / "agent_prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")

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
            "Bash(python *)", "Bash(python3 *)", f"Bash({py} *)", *extra_tools,
            "--add-dir", str(workdir.resolve()),
            "--output-format", "json",
            "--model", model,
        ]
        if budget:
            cmd += ["--max-budget-usd", f"{budget:.2f}"]
    # `python` in the agent's shell is dejabug's own interpreter; no long paths to quote wrongly
    env = {**os.environ, "PATH": os.path.dirname(sys.executable) + os.pathsep + os.environ.get("PATH", "")}
    run = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    log.with_suffix(".json").write_text(run.stdout, encoding="utf-8")
    usage: dict = {}
    text = run.stdout
    if not custom:
        try:
            data = json.loads(run.stdout)
            text = data.get("result") or f"(no summary: {data.get('subtype', 'unknown')}; see {log.with_suffix('.json').name})"
            u = data.get("usage") or {}
            usage = {"cost_usd": data.get("total_cost_usd") or 0.0,
                     "input_tokens": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                     "output_tokens": u.get("output_tokens", 0),
                     "turns": data.get("num_turns", 0)}
        except (json.JSONDecodeError, AttributeError):
            pass
    log.write_text(text + run.stderr, encoding="utf-8")
    return run.returncode, usage
