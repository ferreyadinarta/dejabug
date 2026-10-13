import numpy as np
import cv2

from dejabug.agent import build_steps_prompt
from dejabug.ingest import _changed_boxes
from dejabug.steps import ai_markdown, tidy
from dejabug import vision

DATA = {
    "steps": [
        {"t": 1.0, "action": "click", "target": "Add to cart"},
        {"t": 3.1, "action": "type", "target": "Coupon code", "text": "SAVE10"},
        {"t": 4.0, "action": "press", "text": "Enter"},
        {"t": 4.5, "action": "click", "target": "Apply", "uncertain": True},
        {"t": 6.0, "action": "drag", "target": "the red rectangle", "text": "the frame"},
    ],
    "bug": {"t": 5.0, "what": "an error toast instead of a discount"},
}


def test_ai_markdown_reads_like_steps():
    md = ai_markdown(DATA, "bug.mov")
    assert "1. Click Add to cart (1.0s)" in md
    assert '2. Type "SAVE10" in Coupon code (3.1s)' in md
    assert "3. Press Enter (4.0s)" in md
    assert "4. Click Apply (4.5s) _(not sure)_" in md
    assert "5. Drag the red rectangle to the frame (6.0s)" in md
    assert "**Bug** (5.0s): an error toast instead of a discount" in md


def test_api_prompt_has_no_file_instructions(tmp_path):
    cli = build_steps_prompt(tmp_path, tmp_path / "steps.json", note="happens on Safari")
    api = build_steps_prompt(tmp_path, tmp_path / "steps.json", note="happens on Safari", api=True)
    assert "Save `" in cli and "Save `" not in api
    assert "Read every" in cli and "Read every" not in api
    assert "happens on Safari" in api
    assert '"steps": [' in api  # doubled braces collapsed


def test_api_request_samples_long_films(tmp_path):
    (tmp_path / "film").mkdir()
    for i in range(vision.MAX_SHEETS + 10):
        (tmp_path / "film" / f"{i:06.1f}s.jpg").write_bytes(b"x")
    images = [p for p in vision._content("prompt", tmp_path) if p["type"] == "image"]
    assert len(images) == vision.MAX_SHEETS


def test_changed_boxes_keep_text_and_drop_caret():
    a = np.full((200, 400), 255, np.uint8)
    b = a.copy()
    cv2.putText(b, "Items 1", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)  # small, wide: text
    cv2.line(b, (300, 100), (300, 118), 0, 1)                                 # small, tall: caret
    boxes = _changed_boxes(a, b)
    assert len(boxes) == 1 and boxes[0][0] < 100


def test_tidy_joins_split_typing():
    data = {"steps": [{"t": 1.5, "action": "click", "target": "Option 1"},
                      {"t": 2.5, "action": "type", "target": "Option 1", "text": "fds"},
                      {"t": 3.5, "action": "type", "target": "Option 1", "text": "fds"},
                      {"t": 9.0, "action": "type", "target": "Option 1", "text": "x"}]}
    steps = tidy(data)["steps"]
    assert [s.get("text") for s in steps] == [None, "fdsfds", "x"]


def test_action_comment_is_marked_so_it_posts_once():
    from dejabug.action import MARKER, comment_body
    body = comment_body("### Steps\n1. Click x (1.0s)\n", "https://example/run")
    assert body.startswith(MARKER) and "1. Click x" in body and "https://example/run" in body
