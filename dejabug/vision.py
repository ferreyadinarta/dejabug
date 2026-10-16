"""Steps from the evidence in one model call: through Claude Code if installed, else the API (ANTHROPIC_API_KEY)."""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from importlib import resources
from pathlib import Path

API = "https://api.anthropic.com/v1/messages"
MODELS = {"sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5", "haiku": "claude-haiku-5-5"}
MAX_SHEETS = 40
MAX_EVENTS_CHARS = 30_000


def _content(prompt: str, evidence: Path, events: bool = True) -> list[dict]:
    sheets = sorted((evidence / "film").glob("*.jpg"))
    if len(sheets) > MAX_SHEETS:
        sheets = [sheets[round(i * (len(sheets) - 1) / (MAX_SHEETS - 1))] for i in range(MAX_SHEETS)]
    parts: list[dict] = [{"type": "text", "text": prompt}]
    for s in sheets:
        parts.append({"type": "text", "text": f"film/{s.name}"})
        parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                  "data": base64.b64encode(s.read_bytes()).decode()}})
    zooms = sorted((evidence / "film" / "zoom").glob("*.jpg")) if (evidence / "film" / "zoom").exists() else []
    if zooms:
        parts.append({"type": "text", "text": "Close-ups at full size of small things that changed (file name: frame time, "
                                              "then x,y of the top-left corner on the frame):"})
    for z in zooms:
        parts.append({"type": "text", "text": f"film/zoom/{z.name}"})
        parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                  "data": base64.b64encode(z.read_bytes()).decode()}})
    log = evidence / "events.jsonl"
    if events and log.exists():
        parts.append({"type": "text", "text": "events.jsonl:\n" + log.read_text(encoding="utf-8")[:MAX_EVENTS_CHARS]})
    return parts


def _save(text: str, target: Path) -> None:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit(f"the model didn't return steps: {text[:300]}")
    target.write_text(json.dumps(json.loads(m.group(0)), indent=1, ensure_ascii=False), encoding="utf-8")


def _via_claude_code(content: list[dict], model: str) -> tuple[str, dict]:
    msg = {"type": "user", "message": {"role": "user", "content": content}}
    effort = os.environ.get("DEJABUG_EFFORT", "max")  # low, medium, high, xhigh, max
    run = subprocess.run([shutil.which("claude") or "claude", "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
                          "--model", model, "--max-turns", "1", "--tools", "", "--strict-mcp-config",
                          *(["--effort", effort] if effort else []),
                          "--disable-slash-commands", "--setting-sources", "",
                          "--system-prompt", "You turn screen recordings of software bugs into reproduction steps."],
                         input=json.dumps(msg) + "\n", capture_output=True, text=True, encoding="utf-8", errors="replace",
                         timeout=600)
    for line in reversed(run.stdout.splitlines()):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "result":
            u = d.get("usage") or {}
            return d.get("result") or "", {"cost_usd": d.get("total_cost_usd") or 0.0,
                                           "output_tokens": u.get("output_tokens", 0)}
    raise SystemExit(f"Claude Code gave no result: {run.stderr[-300:]}")


def _via_api(content: list[dict], model: str) -> tuple[str, dict]:
    body = {"model": MODELS.get(model, model), "max_tokens": 4000, "messages": [{"role": "user", "content": content}]}
    if os.environ.get("DEJABUG_EFFORT", "max") in ("high", "xhigh", "max"):
        body.update(max_tokens=20000, thinking={"type": "enabled", "budget_tokens": 12000})
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST", headers={
        "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
        "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Claude API error {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
    u = data.get("usage") or {}
    return "".join(b.get("text", "") for b in data.get("content", [])), {
        "input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0)}


def available() -> bool:
    return bool(shutil.which("claude") or os.environ.get("ANTHROPIC_API_KEY"))


def _ask(content: list[dict], model: str) -> tuple[str, dict]:
    return _via_claude_code(content, model) if shutil.which("claude") else _via_api(content, model)


KIND = {"select": "drag", "double_click": "click", "press": "press", "paste": "type"}


def vote(drafts: list[dict], window: float = 1.0) -> dict:
    """Keep the steps most drafts agree on: same kind of action at about the same time."""
    need = len(drafts) // 2 + 1
    found = sorted(((float(s.get("t", 0)), n, s) for n, d in enumerate(drafts) for s in d.get("steps", [])),
                   key=lambda x: (x[0], x[1]))
    clusters: list[list[tuple[float, int, dict]]] = []
    for t, n, s in found:
        kind = KIND.get(s.get("action"), s.get("action"))
        for c in clusters:
            if KIND.get(c[0][2].get("action"), c[0][2].get("action")) == kind and abs(t - c[0][0]) <= window \
                    and n not in {m for _, m, _ in c}:
                c.append((t, n, s))
                break
        else:
            clusters.append([(t, n, s)])
    steps = []
    for c in clusters:
        if len({n for _, n, _ in c}) < need:
            continue
        actions = [s.get("action") for _, _, s in c]
        common = max(actions, key=actions.count)  # ties go to the earliest
        steps.append(dict(next(s for _, _, s in c if s.get("action") == common)))
    bugs = sorted((d["bug"] for d in drafts if d.get("bug")), key=lambda b: float(b.get("t", 0)))
    return {"steps": sorted(steps, key=lambda s: float(s.get("t", 0))), "bug": bugs[len(bugs) // 2] if bugs else {}}


def write_steps(prompt: str, evidence: Path, target: Path, model: str = "opus", drafts: int = 1,
                context: str = "", check: bool = True) -> dict:
    """Draft the steps from the film (several drafts are voted on), then a checking call corrects them against the frames."""
    content = _content(prompt, evidence)
    with ThreadPoolExecutor(drafts) as pool:
        results = list(pool.map(lambda _: _ask(content, model), range(drafts)))
    usage: dict = {}
    parsed, reply = [], ""
    for n, (text, u) in enumerate(results, 1):
        draft = target.with_name(f"steps_draft{n}.json")
        reply = text
        try:
            _save(text, draft)
            parsed.append(json.loads(draft.read_text(encoding="utf-8")))
        except (SystemExit, json.JSONDecodeError):
            pass
        usage = {k: usage.get(k, 0) + v for k, v in u.items()}
    if not parsed:  # e.g. a usage limit: show what the model said
        raise SystemExit(f"the model didn't return steps: {reply.strip()[:300] or '(empty reply)'}")
    merged = vote(parsed) if len(parsed) > 2 else parsed[0]
    target.with_name("steps_voted.json").write_text(json.dumps(merged, indent=1, ensure_ascii=False), encoding="utf-8")
    if not check:
        target.write_text(json.dumps(merged, indent=1, ensure_ascii=False), encoding="utf-8")
        return usage
    template = resources.files("dejabug").joinpath("prompts/check_steps.md").read_text(encoding="utf-8")
    joined = f"Draft:\n\n```json\n{json.dumps(merged, indent=1, ensure_ascii=False)}\n```"
    template = template.replace("{context}", f"\n{context}\n" if context else "")
    text, more = _ask(_content(template.replace("{drafts}", joined), evidence, events=False), model)
    _save(text, target)
    return {k: usage.get(k, 0) + more.get(k, 0) for k in usage}
