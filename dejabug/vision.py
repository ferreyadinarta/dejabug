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
from pathlib import Path

API = "https://api.anthropic.com/v1/messages"
MODELS = {"sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5", "haiku": "claude-haiku-5-5"}
MAX_SHEETS = 40
MAX_EVENTS_CHARS = 30_000


def _content(prompt: str, evidence: Path) -> list[dict]:
    sheets = sorted((evidence / "film").glob("*.jpg"))
    if len(sheets) > MAX_SHEETS:
        sheets = [sheets[round(i * (len(sheets) - 1) / (MAX_SHEETS - 1))] for i in range(MAX_SHEETS)]
    parts: list[dict] = [{"type": "text", "text": prompt}]
    for s in sheets:
        parts.append({"type": "text", "text": f"film/{s.name}"})
        parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                  "data": base64.b64encode(s.read_bytes()).decode()}})
    events = evidence / "events.jsonl"
    if events.exists():
        parts.append({"type": "text", "text": "events.jsonl:\n" + events.read_text(encoding="utf-8")[:MAX_EVENTS_CHARS]})
    return parts


def _save(text: str, target: Path) -> None:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit(f"the model didn't return steps: {text[:300]}")
    target.write_text(json.dumps(json.loads(m.group(0)), indent=1, ensure_ascii=False), encoding="utf-8")


def _via_claude_code(content: list[dict], model: str) -> tuple[str, dict]:
    msg = {"type": "user", "message": {"role": "user", "content": content}}
    run = subprocess.run(["claude", "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
                          "--model", model, "--max-turns", "1"],
                         input=json.dumps(msg) + "\n", capture_output=True, text=True, encoding="utf-8", errors="replace")
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


def write_steps(prompt: str, evidence: Path, target: Path, model: str = "sonnet") -> dict:
    """Send the film and events in one message, save the steps JSON to `target`, return usage."""
    content = _content(prompt, evidence)
    text, usage = _via_claude_code(content, model) if shutil.which("claude") else _via_api(content, model)
    _save(text, target)
    return usage
