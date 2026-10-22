# Steps accuracy, dejabug 0.2.0 (run once, 21 October 2026)

Same 20 videos, references and rules as the [first run](steps-accuracy.md), following [PROTOCOL.md](../PROTOCOL.md): `dejabug steps <video>` with default settings on the `v0.2.0` tag, bare video files (no issue text), one run.

**Result: did not pass.** The bar set before the run was a median recall of at least 0.6 and pooled precision of at least 0.7.

| | 0.1.1 | 0.2.0 |
|---|---|---|
| Videos with steps | 20 | 12 (7 timed out, 1 lost its connection) |
| Median recall, failures counted as 0 | 0 | 0.29 |
| Median recall, the 12 with steps | | 0.75 |
| Pooled precision, the 12 with steps | 0.10 | 0.57 |
| Bug moment named | 4 of 20 | 5 of 20 |

What went wrong:

- 0.2.0 stopped each model call after 10 minutes. At its default max effort, Opus thought for longer than that on 7 of the longer videos, so they produced nothing. One more call lost its network connection and wasn't retried. 0.2.1 allows 30 minutes and retries once.
- Where it produced steps, it found most of the actions but too many of the listed steps were wrong, and it rarely named the bug moment. On our development videos both improve a lot when the model gets the issue text, which this benchmark doesn't give it.

Scored by the model judge in [bench/score.py](../score.py), the second-opinion grader in the protocol. Per-case scores: [steps-accuracy-0.2.0-judge.json](steps-accuracy-0.2.0-judge.json). Because these 20 videos have now been seen, the next benchmark will use 20 new videos picked by the same frozen rule.

An earlier attempt the same day failed before producing any output (the background model calls weren't logged in); it was restarted on the same tag.
