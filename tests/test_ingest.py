import numpy as np
import pytest

from dejabug.ingest import (
    Box,
    Keyframe,
    clean,
    click_before,
    column,
    detect_scroll,
    merge_typing,
    nearest_label,
    ocr_flicker,
    pointer_move,
)


def box(text, x, y, w=120, h=20):
    return Box(text, 1.0, x, y, w, h)


@pytest.mark.parametrize("raw, want", [
    ("• The Godfather", "The Godfather"),
    ("D 12 Angry Men", "12 Angry Men"),
    ("П Pulp Fiction", "Pulp Fiction"),
    ("  Rp   250.000 ", "Rp 250.000"),
    ("(SAVE10", "(SAVE10"),
])
def test_clean_strips_bullets_and_checkbox_glyphs(raw, want):
    assert clean(raw) == want


def test_ocr_flicker_is_not_a_real_change():
    assert ocr_flicker("The Godfather: Part II", "The Godfather: Part lI")
    assert not ocr_flicker("Rp 0", "Rp 250.000")


def test_column_groups_left_aligned_rows_and_leaves_the_rest():
    rows = [box(t, 300, 100 + i * 40) for i, t in enumerate(["A1", "B2", "C3", "D4"])]
    chip = box("Inception", 120, 40)
    panel, loose = column(rows + [chip])
    assert [b.text for b in panel] == ["A1", "B2", "C3", "D4"]
    assert loose == [chip]


def test_column_needs_enough_rows():
    panel, loose = column([box("one", 10, 10), box("two", 10, 50)])
    assert panel == [] and len(loose) == 2


def test_click_on_a_wide_row_takes_the_text_of_that_row():
    rows = [box("Forrest Gump", 350, 525, h=34), box("Inception", 350, 598, h=34)]
    assert nearest_label(624, 596, rows) == "Inception"


def test_click_label_prefers_text_under_the_pointer():
    assert nearest_label(60, 20, [box("Apply", 40, 10, w=50)]) == "Apply"


def test_click_needs_the_pointer_to_rest_first():
    resting = [(1.0, 100, 100), (1.1, 100, 101), (1.2, 101, 100), (1.3, 100, 100)]
    assert click_before(1.3, resting) == (100, 100)
    moving = [(1.0, 10, 10), (1.1, 60, 60), (1.2, 120, 90), (1.3, 200, 140)]
    assert click_before(1.3, moving) is None


def test_scroll_is_detected_from_text_moving_together():
    before = Keyframe(0.0, None, boxes=[box(t, 300, 200 + i * 40) for i, t in enumerate("ABCDE")])
    after = Keyframe(1.0, None, boxes=[box(t, 300, 120 + i * 40) for i, t in enumerate("ABCDE")])
    dy, region = detect_scroll(before, after)
    assert dy == 80  # content moved up 80 px: the user scrolled down


def test_typing_collapses_into_one_event():
    events = [
        {"t": 1.0, "type": "text_appeared", "xy": [400, 270], "text": "S"},
        {"t": 1.4, "type": "type", "xy": [410, 270], "text": "SA"},
        {"t": 2.0, "type": "type", "xy": [430, 271], "text": "SAVE10"},
    ]
    merged = merge_typing(events)
    assert [(e["type"], e["text"]) for e in merged] == [("type", "SAVE10")]


def test_pointer_is_the_patch_that_travels():
    prev = np.full((200, 200), 255, np.uint8)
    cur = prev.copy()
    arrow = np.zeros((16, 10), np.uint8)
    prev[50:66, 50:60] = arrow   # pointer was here
    cur[120:136, 130:140] = arrow  # and is now here
    blobs = [(55, 58), (135, 128)]
    assert pointer_move(prev, cur, blobs, None) == (135, 128)


def test_a_patch_changing_in_place_is_not_the_pointer():
    prev = np.full((200, 200), 255, np.uint8)
    cur = prev.copy()
    cur[50:66, 50:60] = 0  # a checkbox ticking: change in one spot only
    assert pointer_move(prev, cur, [(55, 58)], None) is None


def _arrow():
    a = np.zeros((18, 12), np.uint8)
    for r in range(18):
        a[r, : min(12, r // 1 + 1)] = 255  # white wedge
    a[:, 0] = 0  # dark outline on the left edge
    return a


def _scene(bg_shift, pointer_at=None):
    rng = np.random.default_rng(0)
    rows = (rng.integers(40, 90, size=(400, 1)) * np.ones((1, 400))).astype(np.uint8)
    img = np.roll(rows, bg_shift, axis=0)  # a "list" that scrolls
    if pointer_at:
        x, y = pointer_at
        arrow = _arrow()
        region = img[y:y + 18, x:x + 12]
        img[y:y + 18, x:x + 12] = np.where(arrow > 0, arrow, region)
    return img


def test_pointer_shape_is_learned_from_a_clean_move():
    from dejabug.ingest import learn_shape

    prev, cur = _scene(0, (100, 100)), _scene(0, (200, 150))
    shape = learn_shape(prev, cur, (206, 159))
    assert shape is not None
    assert shape.mask.any()


def test_learned_shape_is_found_while_the_background_scrolls():
    from dejabug.ingest import find_shape, learn_shape

    shape = learn_shape(_scene(0, (100, 100)), _scene(0, (200, 150)), (206, 159))
    later = _scene(37, (260, 220))  # list scrolled by 37 px, pointer moved
    found = find_shape(later, [shape], (200, 150))
    assert found is not None
    # The arrow's tip is its top-left white pixel: column 1, row 1 of the drawing.
    assert abs(found[0] - 261) <= 2 and abs(found[1] - 221) <= 2


def test_click_label_prefers_the_same_row_over_a_long_title_below():
    rows = [box("Inception", 120, 270, w=90, h=24), box("The Lord of the Rings: The Two Towers", 120, 302, w=320, h=24)]
    assert nearest_label(300, 284, rows) == "Inception"
