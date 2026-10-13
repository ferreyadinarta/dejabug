from dejabug.source import ISSUE, VIDEO_URL
from dejabug.steps import markdown, steps_from
from dejabug.steps import test_draft as draft_for

EVENTS = [
    {"t": 0.3, "type": "text_appeared", "text": "Show code"},
    {"t": 0.3, "type": "text_appeared", "text": "Expand code"},
    {"t": 0.3, "type": "text_appeared", "text": "Limit tags"},
    {"t": 1.0, "type": "click", "xy": [100, 60], "label": "Checkboxes"},
    {"t": 1.2, "type": "panel_opened", "items": ["A", "B", "C", "D"]},
    {"t": 3.0, "type": "panel_closed", "items": ["A", "B", "C", "D"]},
    {"t": 3.0, "type": "panel_opened", "items": ["E", "F", "G", "H"]},
    {"t": 4.0, "type": "click", "xy": [300, 280], "label": "Inception"},
    {"t": 5.0, "type": "click", "xy": [50, 50], "label": None, "zoom": "clicks/0005.0s.png"},
    {"t": 6.0, "type": "hover", "xy": [300, 320], "label": "12 Angry Men"},
]


def test_actions_stay_in_order_and_page_context_is_dropped():
    steps = steps_from(EVENTS)
    actions = [(s.kind, s.target) for s in steps if s.kind != "note"]
    assert actions == [("click", "Checkboxes"), ("click", "Inception"), ("click", None), ("hover", "12 Angry Men")]
    notes = " ".join(s.text for s in steps if s.kind == "note")
    assert "Show code" not in notes
    assert "the list changed to: E, F, G, ..." in notes  # closed+opened at once is one change


def test_markdown_numbers_actions_and_indents_notes():
    md = markdown(steps_from(EVENTS), "bug.mov")
    assert '1. Click "Checkboxes" (1.0s)' in md
    assert "3. Click the element in `clicks/0005.0s.png` (5.0s)" in md
    assert '4. Hover over "12 Angry Men" (6.0s)' in md


def test_draft_is_valid_python_with_every_action():
    src = draft_for(steps_from(EVENTS), "http://localhost:3000")
    compile(src, "draft", "exec")
    assert 'click(page, "Checkboxes")' in src and 'click(page, "Inception")' in src
    assert "TODO 5.0s" in src


def test_issue_links_and_video_urls_are_recognised():
    assert ISSUE.match("https://github.com/mui/material-ui/issues/47203").groups() == ("mui", "material-ui", "47203")
    body = "see https://github.com/user-attachments/assets/0f0e3a2b-1c2d-4e5f-8a9b-0c1d2e3f4a5b and x.png"
    assert VIDEO_URL.findall(body) == ["https://github.com/user-attachments/assets/0f0e3a2b-1c2d-4e5f-8a9b-0c1d2e3f4a5b"]
