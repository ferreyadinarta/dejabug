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


def test_film_skips_still_frames_and_keeps_full_size_copies(tmp_path):
    from dejabug.ingest import film
    frames = []
    for i in range(30):  # 3 s at 10 fps: still, then a change at 1.5 s
        img = np.full((120, 200, 3), 255, np.uint8)
        if i >= 15:
            cv2.rectangle(img, (20, 20), (120, 80), (0, 0, 0), -1)
        path = tmp_path / f"f{i:05d}.png"
        cv2.imwrite(str(path), img)
        frames.append((i / 10, path))
    film(frames, [], tmp_path / "film")
    kept = sorted(p.name for p in (tmp_path / "film" / "frames").glob("*.jpg"))
    assert kept == ["0000.0s.jpg", "0001.5s.jpg", "0002.5s.jpg"]  # first, the change, the last
    assert len(list((tmp_path / "film").glob("*.jpg"))) == 1


def test_vote_keeps_steps_most_drafts_share():
    a = {"steps": [{"t": 1.0, "action": "click", "target": "A"}, {"t": 3.0, "action": "click", "target": "B"}],
         "bug": {"t": 5.0, "what": "x"}}
    b = {"steps": [{"t": 1.5, "action": "double_click", "target": "A"}, {"t": 7.0, "action": "drag", "target": "C"}],
         "bug": {"t": 6.0, "what": "y"}}
    c = {"steps": [{"t": 0.8, "action": "click", "target": "A"}, {"t": 7.2, "action": "select", "target": "C"}],
         "bug": {"t": 9.0, "what": "z"}}
    voted = vision.vote([a, b, c])
    assert [(s["action"], s["target"]) for s in voted["steps"]] == [("click", "A"), ("drag", "C")]
    assert voted["bug"]["what"] == "y"  # the middle bug time
