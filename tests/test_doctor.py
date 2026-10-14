from dejabug.doctor import MISSING, OK, OPTIONAL, ready


def test_github_being_unreachable_does_not_block_steps_mode():
    rows = [("steps", OK, "Python 3.12", ""), ("steps", OPTIONAL, "GitHub reachable (issue links)", "check network")]
    assert ready(rows, "steps")


def test_a_missing_steps_requirement_blocks_steps_mode():
    rows = [("steps", MISSING, "OCR (RapidOCR)", "pip install rapidocr"), ("steps", OK, "Python 3.12", "")]
    assert not ready(rows, "steps")


def test_test_mode_needs_every_run_check():
    rows = [("run", OK, "Playwright (test mode)", ""), ("run", OPTIONAL, "coding agent (test mode)", "install")]
    assert not ready(rows, "run")


def test_steps_mode_needs_a_model():
    rows = [("steps", OK, "Python 3.12", ""), ("steps", MISSING, "model that writes the steps (Claude Code or ANTHROPIC_API_KEY)", "x")]
    assert not ready(rows, "steps")
