from dejabug.verify import Moment, align, moments, similarity


def m(kind, text, t=0.0):
    return Moment(t, kind, text, "")


def test_moments_keep_what_matters_and_drop_noise():
    events = [
        {"t": 0, "type": "start", "text": ["x"]},
        {"t": 1, "type": "click", "label": "Add to cart"},
        {"t": 1, "type": "text_gone", "text": "Coupon code"},
        {"t": 2, "type": "error_shown", "text": "Something went wrong"},
        {"t": 2, "type": "ui_change"},
        {"t": 3, "type": "content_replaced", "after": ["A", "B"], "rows": 2},
    ]
    got = [(x.kind, x.text, x.error) for x in moments(events)]
    assert got == [("click", "Add to cart", False), ("show", "Something went wrong", True), ("list", "A | B", False)]


def test_similarity_respects_kinds():
    assert similarity(m("click", "Apply"), m("click", "Apply")) == 1.0
    assert similarity(m("click", "Apply"), m("list", "Apply")) == 0.0


def test_ocr_merged_words_still_match():
    assert similarity(m("show", "Inception & Favorites"), m("show", "Inception ( Favorites")) >= 0.8


def test_lists_match_by_items():
    video = m("list", "The Shawshank Redemption | The Godfather | The Dark Knight")
    replay = m("list", "The Shawshank Redemption | The Godfather | The Godfather: Part II")
    assert similarity(video, replay) >= 0.6


def test_align_keeps_order():
    video = [m("click", "Add"), m("type", "SAVE10"), m("click", "Apply"), m("show", "Something went wrong")]
    replay = [m("click", "Add"), m("click", "Apply"), m("type", "SAVE10"), m("show", "Something went wrong")]
    pairs = align(video, replay)
    matched = [(i, j) for i, j, _ in pairs]
    # Apply and SAVE10 are swapped in the replay, so only one of them can pair up in order.
    assert (0, 0) in matched and (3, 3) in matched
    assert len(matched) == 3
    assert all(a < b for (a, _), (b, _) in zip(matched, matched[1:]))
    assert all(a < b for (_, a), (_, b) in zip(matched, matched[1:]))
