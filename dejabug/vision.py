"""Steps from the evidence in one Claude API call, for people without Claude Code (needs ANTHROPIC_API_KEY)."""

from __future__ import annotations

import base64
import json
import os
import re
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


def write_steps_api(prompt: str, evidence: Path, target: Path, model: str = "sonnet") -> dict:
    """Ask the API for the steps JSON and save it to `target`; returns token usage."""
    key = os.environ["ANTHROPIC_API_KEY"]
    body = {"model": MODELS.get(model, model), "max_tokens": 4000,
            "messages": [{"role": "user", "content": _content(prompt, evidence)}]}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Claude API error {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
    text = "".join(b.get("text", "") for b in data.get("content", []))
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit(f"the model didn't return steps: {text[:300]}")
    target.write_text(json.dumps(json.loads(m.group(0)), indent=1, ensure_ascii=False), encoding="utf-8")
    u = data.get("usage") or {}
    return {"input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0)}
