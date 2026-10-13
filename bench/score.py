"""Score steps.md files against reference steps with a model judge, using the rules in PROTOCOL.md.

usage: python bench/score.py <reference dir> <out dir> [--ids a,b] [--save scores.json]
<out dir>/<id>/steps.md is scored against <reference dir>/<id>.md.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

JUDGE = """You grade a tool's "steps to reproduce" against a human reference for the same screen recording.

Rules (strict, from the benchmark protocol):
- Action kinds: click, double_click, right_click, hover, type, key, paste, drag, scroll. Treat "press" as key, "select"/"drag to select" as drag, "triple-click" as double_click.
- A listed action matches a reference action when: same kind, same target (same label or clearly the same element), within 1.5 s of the reference time range, and matches keep their order (each reference action matched at most once).
- Typing matches when it is typing into the same field; the exact text may differ slightly.
- Steps marked "not sure" still count as listed actions.
- Notes, the bug line and gap flags are not actions.
- bug_moment is "yes" when the tool's bug line or a note is within 1 s of a reference bug time and names the affected element or the visible symptom.

Reference:
<reference>
{reference}
</reference>

Tool output:
<output>
{output}
</output>

Reply with only JSON:
{{"reference_actions": <int>, "listed_actions": <int>, "matches": [[<reference #>, <listed #>], ...], "bug_moment": "yes"|"no", "why": "<one line>"}}"""


def judge(reference: str, output: str, model: str) -> dict:
    run = subprocess.run(["claude", "-p", JUDGE.format(reference=reference, output=output), "--model", model,
                          "--output-format", "json", "--allowedTools", ""],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    data = json.loads(run.stdout)
    text = data.get("result") or ""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"judge gave no JSON: {text[:200]}")
    result = json.loads(m.group(0))
    result["cost_usd"] = data.get("total_cost_usd") or 0.0
    return result


def score(case: str, ref_dir: Path, out_dir: Path, model: str) -> dict:
    steps = out_dir / case / "steps.md"
    if not steps.exists():
        return {"id": case, "error": "no steps.md"}
    r = judge((ref_dir / f"{case}.md").read_text(encoding="utf-8"), steps.read_text(encoding="utf-8"), model)
    matched = len(r.get("matches", []))
    ref, listed = r.get("reference_actions") or 0, r.get("listed_actions") or 0
    return {"id": case, "matched": matched, "reference": ref, "listed": listed,
            "recall": matched / ref if ref else None, "precision": matched / listed if listed else None,
            "bug_moment": r.get("bug_moment"), "why": r.get("why"), "matches": r.get("matches", []),
            "cost_usd": r["cost_usd"]}


def summary(rows: list[dict]) -> dict:
    ok = [r for r in rows if "error" not in r]
    rec = [r["recall"] for r in ok if r["recall"] is not None]
    prec = [r["precision"] or 0 for r in ok]
    return {"cases": len(rows), "scored": len(ok),
            "median_recall": statistics.median(rec) if rec else None,
            "median_precision": statistics.median(prec) if prec else None,
            "pooled_recall": sum(r["matched"] for r in ok) / max(1, sum(r["reference"] for r in ok)),
            "pooled_precision": sum(r["matched"] for r in ok) / max(1, sum(r["listed"] for r in ok)),
            "bug_moment": sum(r["bug_moment"] == "yes" for r in ok),
            "judge_cost_usd": round(sum(r["cost_usd"] for r in ok), 2)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("reference", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--ids")
    p.add_argument("--model", default="sonnet")
    p.add_argument("--save", type=Path)
    a = p.parse_args()
    cases = a.ids.split(",") if a.ids else sorted(f.stem for f in a.reference.glob("*.md"))
    with ThreadPoolExecutor(4) as pool:
        rows = list(pool.map(lambda c: score(c, a.reference, a.out, a.model), cases))
    for r in rows:
        if "error" in r:
            print(f"{r['id']:34} {r['error']}")
        else:
            print(f"{r['id']:34} {r['matched']:>2}/{r['reference']:<2} listed {r['listed']:<2} bug {r['bug_moment']:3}  {r['why']}")
    s = summary(rows)
    print(json.dumps(s, indent=1))
    if a.save:
        a.save.write_text(json.dumps({"summary": s, "cases": rows}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
