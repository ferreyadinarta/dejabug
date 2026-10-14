"""Classify every reference action the judge didn't find: what kind was it and why was it missed?

usage: python bench/why_missed.py <reference dir> <out dir> <scores.json>
"""

from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ASK = """A tool listed steps to reproduce a bug from a screen recording. A grader matched some of them to a human reference.
For each UNMATCHED reference action, give its kind (click, double_click, right_click, hover, type, key, paste, drag, scroll) and why the tool missed it, with one label:
- absent: the tool has nothing for it
- wrong_kind: the tool has it at about this time on the same target but as a different kind
- wrong_target: the tool has the same kind at about this time but on a different element
- wrong_time: the tool has it but more than 1.5 s off
- merged: the tool folded it into a neighbouring step

Reference:
<reference>
{reference}
</reference>

Tool output:
<output>
{output}
</output>

Matched reference action numbers: {matched}

Reply with only JSON: {{"missed": [{{"ref": <n>, "kind": "<kind>", "label": "<label>"}}]}}"""


def classify(ref: str, out: str, matched: list[int]) -> list[dict]:
    run = subprocess.run(["claude", "-p", ASK.format(reference=ref, output=out, matched=matched), "--model", "sonnet",
                          "--output-format", "json", "--tools", ""], capture_output=True, text=True)
    text = json.loads(run.stdout).get("result") or ""
    return json.loads(re.search(r"\{.*\}", text, re.S).group(0))["missed"]


def main() -> int:
    ref_dir, out_dir, scores = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text())

    def one(c):
        try:
            return c["id"], classify((ref_dir / f"{c['id']}.md").read_text(), (out_dir / c["id"] / "steps.md").read_text(),
                                     sorted(r for r, _ in c["matches"]))
        except Exception as e:
            return c["id"], [{"kind": "?", "label": f"error {e}"}]

    with ThreadPoolExecutor(4) as pool:
        rows = list(pool.map(one, [c for c in scores["cases"] if "matches" in c]))
    for cid, ms in rows:
        print(f"{cid:34} " + ", ".join(f"{m['kind']}:{m['label']}" for m in ms))
    print("by kind:", collections.Counter(m["kind"] for _, ms in rows for m in ms).most_common())
    print("by reason:", collections.Counter(m["label"] for _, ms in rows for m in ms).most_common())
    print("kind+reason:", collections.Counter(f"{m['kind']}:{m['label']}" for _, ms in rows for m in ms).most_common(12))
    return 0


if __name__ == "__main__":
    sys.exit(main())
