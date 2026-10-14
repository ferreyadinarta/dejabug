"""Classify every listed step the judge didn't match: why is it wrong?

usage: python bench/why_wrong.py <reference dir> <out dir> <scores.json>
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
For each UNMATCHED listed step, say why it doesn't match, with one label:
- wrong_kind: the reference has this action at about this time on the same target, but a different kind (click vs drag, key vs click...)
- wrong_target: same kind and time, different element
- wrong_time: same action and target, more than 1.5 s off
- split_or_duplicate: part of one reference action that the tool split into several, or listed twice
- app_not_user: the tool listed something the app did on its own as a user action
- missing_from_reference: looks like a real user action the reference didn't list
- invented: no sign of it in the reference at all

Reference:
<reference>
{reference}
</reference>

Tool output (numbered steps):
<output>
{output}
</output>

Matched listed step numbers: {matched}

Reply with only JSON: {{"unmatched": [{{"step": <n>, "label": "<label>"}}]}}"""


def classify(ref: str, out: str, matched: list[int]) -> list[dict]:
    run = subprocess.run(["claude", "-p", ASK.format(reference=ref, output=out, matched=matched), "--model", "sonnet",
                          "--output-format", "json", "--tools", ""], capture_output=True, text=True)
    text = json.loads(run.stdout).get("result") or ""
    return json.loads(re.search(r"\{.*\}", text, re.S).group(0))["unmatched"]


def main() -> int:
    ref_dir, out_dir, scores = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text())
    cases = [c for c in scores["cases"] if "matches" in c]

    def one(c):
        try:
            return c["id"], classify((ref_dir / f"{c['id']}.md").read_text(), (out_dir / c["id"] / "steps.md").read_text(),
                                     sorted(l for _, l in c["matches"]))
        except Exception as e:
            return c["id"], [{"label": f"error {e}"}]

    with ThreadPoolExecutor(4) as pool:
        rows = list(pool.map(one, cases))
    total = collections.Counter(u["label"] for _, us in rows for u in us)
    for cid, us in rows:
        print(f"{cid:34} {dict(collections.Counter(u['label'] for u in us))}")
    print(json.dumps(total.most_common(), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
