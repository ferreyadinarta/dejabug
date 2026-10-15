"""Turn a screen recording into a short event log, keyframes and a contact sheet."""

from __future__ import annotations

import json
import os
import re
import shutil
import statistics
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

SAMPLE_FPS = 10         # frames per second pulled from the video
WIDTH = 1280            # wider videos are scaled down to this; smaller ones keep their size
MIN_CHANGE = 0.0002     # fraction of pixels (outside the cursor) that must change
CURSOR_MAX = 48         # change blobs no bigger than this (px) are treated as the cursor
REST_FRAMES = 2         # this many quiet frames in a row end a burst of change
LONG_BURST = 1.5        # seconds; bursts longer than this also keep their middle frame
MAX_EVENTS = 80
PANEL_MIN = 4          # this many texts appearing/vanishing together = a list or panel
MIN_CONF = 0.4

ERROR_WORDS = re.compile(
    r"error|wrong|fail|invalid|exception|cannot|can't|not found|denied|unable|oops|crash",
    re.IGNORECASE,
)
URLISH = re.compile(r"(https?://|localhost|\w+\.(com|org|io|dev|app|net)\b|^/[\w/-]+$)")


@dataclass
class Box:
    text: str
    conf: float
    x: float  # pixels, top-left origin
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    def xy(self) -> list[int]:
        return [round(self.cx), round(self.cy)]

    def iou(self, o: Box) -> float:
        ix = max(0.0, min(self.x + self.w, o.x + o.w) - max(self.x, o.x))
        iy = max(0.0, min(self.y + self.h, o.y + o.h) - max(self.y, o.y))
        inter = ix * iy
        union = self.w * self.h + o.w * o.h - inter
        return inter / union if union else 0.0

    def inside(self, r: list[int], pad: int = 0) -> bool:
        rx, ry, rw, rh = r
        return rx - pad <= self.cx <= rx + rw + pad and ry - pad <= self.cy <= ry + rh + pad


@dataclass
class Keyframe:
    t: float
    path: Path
    burst_start: float | None = None  # when the change that led here began
    boxes: list[Box] = field(default_factory=list)


# ---------------------------------------------------------------- frames

def extract_frames(video: Path, dest: Path) -> list[tuple[float, Path]]:
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(video),
         "-vf", f"fps={SAMPLE_FPS},scale='min({WIDTH},iw)':-2", str(dest / "f%05d.png")],
        check=True,
    )
    return [(i / SAMPLE_FPS, p) for i, p in enumerate(sorted(dest.glob("f*.png")))]


def split_change(prev: np.ndarray, cur: np.ndarray):
    """Return (ui_change_fraction, cursor_blobs, ui_rects) for one frame step."""
    diff = cv2.absdiff(prev, cur)
    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    blobs = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(blobs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cursor, ui = [], []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w <= CURSOR_MAX and h <= CURSOR_MAX:
            # (center_x, center_y, w, h); blobs are dilated by ~4 px each way
            cursor.append((x + w / 2, y + h / 2, w - 4, h - 4))
        else:
            ui.append([x, y, w, h])
    ui_px = sum(int(np.count_nonzero(mask[y:y + h, x:x + w])) for x, y, w, h in ui)
    return ui_px / mask.size, cursor, ui


def blink_spots(steps) -> set[tuple[int, int]]:
    """Spots where a small blob keeps reappearing in place (caret, spinner), not the pointer."""
    counts: dict[tuple[int, int], int] = {}
    for _, blobs, _ in steps:
        for x, y, _, _ in blobs:
            k = (round(x / 6), round(y / 6))
            counts[k] = counts.get(k, 0) + 1
    return {k for k, n in counts.items() if n >= 4}


def is_pointer(blob, blinks: set[tuple[int, int]]) -> bool:
    x, y, w, h = blob
    if w <= 4 and h >= 8:
        return False  # thin vertical line: a text caret
    if (round(x / 6), round(y / 6)) in blinks:
        return False
    return 6 <= max(w, h) <= CURSOR_MAX


PATCH = 14  # half-size of the patch compared when looking for the pointer


def _patch(img: np.ndarray, x: float, y: float) -> np.ndarray | None:
    x, y = int(round(x)), int(round(y))
    if x < PATCH or y < PATCH or x + PATCH > img.shape[1] or y + PATCH > img.shape[0]:
        return None
    return img[y - PATCH:y + PATCH, x - PATCH:x + PATCH].astype(np.float32)


def _same(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a - a.mean(), b - b.mean()
    den = float(np.sqrt((a * a).sum() * (b * b).sum()))
    return float((a * b).sum() / den) if den > 1e-6 else 0.0


def pointer_move(prev, cur, blobs, last) -> tuple[float, float] | None:
    """Find a small patch that vanished in one spot and reappeared unchanged in another."""
    best, best_score = None, 0.75
    for ax, ay in blobs:
        before = _patch(prev, ax, ay)
        if before is None:
            continue
        for bx, by in blobs:
            if np.hypot(bx - ax, by - ay) < 6:
                continue
            after = _patch(cur, bx, by)
            if after is None:
                continue
            score = _same(before, after)
            if last is not None:  # prefer continuing the path we were on
                score -= 0.0005 * np.hypot(ax - last[0], ay - last[1])
            if score > best_score:
                best, best_score = (bx, by), score
    return best


@dataclass
class PointerShape:
    image: np.ndarray  # the pointer's pixels, float32
    mask: np.ndarray   # 255 where the pixel belongs to the pointer
    anchor: tuple[int, int]  # where the tracked point sits inside `image`


def learn_shape(prev: np.ndarray, cur: np.ndarray, at: tuple[float, float]) -> PointerShape | None:
    """Learn the pointer's shape from the pixels that changed around it after a clean move."""
    p = _patch(cur, *at)
    q = _patch(prev, *at)
    if p is None or q is None:
        return None
    mask = (np.abs(p - q) > 25).astype(np.uint8) * 255
    n = int(np.count_nonzero(mask))
    if not 25 <= n <= 0.8 * mask.size:
        return None
    ys, xs = np.nonzero(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    if y1 - y0 < 6 or x1 - x0 < 3:
        return None  # a speck or a hairline: not a pointer
    # clicks happen at the pointer's tip, i.e. the top of the shape
    top = np.nonzero(mask[y0:y0 + 2, x0:x1])[1]
    tip = (int(round(top.mean())) if len(top) else 0, 0)
    return PointerShape(p[y0:y1, x0:x1].copy(), mask[y0:y1, x0:x1].copy(), tip)


def find_shape(img: np.ndarray, shapes: list[PointerShape], near: tuple[float, float] | None,
               radius: int = 220) -> tuple[float, float] | None:
    """Find a known pointer shape, comparing only its own pixels so the background doesn't matter."""
    H, W = img.shape
    if near is not None:
        x0, y0 = max(0, int(near[0]) - radius), max(0, int(near[1]) - radius)
        x1, y1 = min(W, int(near[0]) + radius), min(H, int(near[1]) + radius)
    else:
        x0, y0, x1, y1 = 0, 0, W, H
    region = img[y0:y1, x0:x1].astype(np.float32)
    best, best_err = None, 0.012
    for s in shapes:
        h, w = s.image.shape
        if region.shape[0] < h or region.shape[1] < w:
            continue
        sq = cv2.matchTemplate(region, s.image, cv2.TM_SQDIFF, mask=s.mask)
        err_map = sq / (float(np.count_nonzero(s.mask)) * 255.0 * 255.0)
        _, _, loc, _ = cv2.minMaxLoc(err_map)
        err = float(err_map[loc[1], loc[0]])
        if err < best_err:
            best, best_err = (x0 + loc[0] + s.anchor[0], y0 + loc[1] + s.anchor[1]), err
    return best


def scan(frames: list[tuple[float, Path]]):
    """Keyframes at each settle point, plus a track of the mouse pointer."""
    keys = [Keyframe(frames[0][0], frames[0][1])]
    track: list[tuple[float, float | None, float | None]] = []

    grays = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for _, p in frames]
    steps = [(0.0, [], [])] + [split_change(a, b) for a, b in zip(grays, grays[1:])]
    blinks = blink_spots(steps)

    cursor_pos: tuple[float, float] | None = None
    shapes: list[PointerShape] = []
    burst_start, burst_frames, quiet = None, [], 0
    rest = 0                      # index of the last frame before the current burst
    peak, peak_change = None, 0.0  # the burst frame most different from `rest`

    for i, (t, path) in enumerate(frames):
        if i:
            frac, blobs, _ = steps[i]
            blobs = [b[:2] for b in blobs if is_pointer(b, blinks)]
            # find the known pointer shape, else learn it from a clean move
            found = find_shape(grays[i], shapes, cursor_pos) if shapes else None
            if found is None and shapes:
                found = find_shape(grays[i], shapes, None)
            if found:
                cursor_pos = found
            else:
                moved = pointer_move(grays[i - 1], grays[i], blobs, cursor_pos)
                if moved:
                    cursor_pos = moved
                    if frac < 0.01 and len(shapes) < 6:
                        shape = learn_shape(grays[i - 1], grays[i], moved)
                        if shape is not None:
                            shapes.append(shape)
            if frac >= MIN_CHANGE:
                if burst_start is None:
                    burst_start, rest = t, i - 1
                    peak, peak_change = None, 0.0
                burst_frames.append((t, path))
                change = split_change(grays[rest], grays[i])[0]
                if change > peak_change:
                    peak, peak_change = i, change
                quiet = 0
            elif burst_start is not None:
                quiet += 1
                if quiet >= REST_FRAMES:
                    # keep the peak frame so menus/toasts that flash and vanish aren't lost
                    if peak is not None and frames[peak][0] < t \
                            and split_change(grays[peak], grays[i])[0] >= MIN_CHANGE * 10:
                        keys.append(Keyframe(frames[peak][0], frames[peak][1], burst_start))
                    elif t - burst_start > LONG_BURST and len(burst_frames) > 2:
                        mt, mp = burst_frames[len(burst_frames) // 2]
                        keys.append(Keyframe(mt, mp, burst_start))
                    keys.append(Keyframe(t, path, burst_start))
                    burst_start, burst_frames, quiet = None, [], 0
        track.append((t, *(cursor_pos if cursor_pos else (None, None))))

    last_t, last_path = frames[-1]
    if keys[-1].path != last_path:
        keys.append(Keyframe(last_t, last_path, burst_start))
    return keys, track, grays


# ---------------------------------------------------------------- OCR

LEADING_JUNK = re.compile(r"^(?:[^\w(\"'$€£¥₹]+|[DПO□☐]\s+)+")  # bullets, checkboxes OCR'd as letters


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", LEADING_JUNK.sub("", text.strip()))


_RAPID = None


def _raw_ocr(path: Path, W: int, H: int):
    """OCR boxes in pixels: Apple Vision on macOS, RapidOCR elsewhere (DEJABUG_OCR overrides)."""
    global _RAPID
    engine = os.environ.get("DEJABUG_OCR") or ("vision" if sys.platform == "darwin" else "rapid")
    if engine == "vision":
        from ocrmac import ocrmac

        for text, conf, (x, y, w, h) in ocrmac.OCR(str(path), recognition_level="accurate").recognize():
            # Vision returns normalized coords with a bottom-left origin.
            yield text, float(conf), x * W, (1 - y - h) * H, w * W, h * H
        return
    if _RAPID is None:
        from rapidocr import RapidOCR

        _RAPID = RapidOCR()
    r = _RAPID(str(path))
    for quad, text, conf in zip(r.boxes if r.boxes is not None else [], r.txts or [], r.scores or []):
        xs, ys = [p[0] for p in quad], [p[1] for p in quad]
        yield text, float(conf), min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def ocr(path: Path, W: int, H: int) -> list[Box]:
    out = []
    for text, conf, x, y, w, h in _raw_ocr(path, W, H):
        text = clean(text)
        if conf < MIN_CONF or not text:
            continue
        if len(text) == 1 and not text.isdigit():
            continue  # stray glyphs: checkbox squares, icons, cursor carets
        out.append(Box(text, conf, x, y, w, h))
    return out


# ---------------------------------------------------------------- events

def column(boxes: list[Box]) -> tuple[list[Box], list[Box]]:
    """Split texts into the largest left-aligned column (a list or menu) and the rest."""
    best: list[Box] = []
    for b in boxes:
        col = [o for o in boxes if abs(o.x - b.x) < 40]
        if len(col) > len(best):
            best = col
    if len(best) < PANEL_MIN:
        return [], boxes
    best.sort(key=lambda b: b.y)
    return best, [b for b in boxes if b not in best]


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 1}


def ocr_flicker(a: str, b: str) -> bool:
    """Same text read slightly differently ('Part II' vs 'Part lI', 'Inception X' vs 'Inception')."""
    wa, wb = _words(a), _words(b)
    small, big = sorted((wa, wb), key=len)
    if small and small <= big and all(w.isalpha() for w in big - small):
        return True  # same words plus a merged neighbour or an icon read as a letter
    if abs(len(a) - len(b)) > 1:
        return False
    import difflib
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.9


def nearest_label(x: float, y: float, boxes: list[Box], limit: float = 70) -> str | None:
    """What a person would say they clicked."""
    for b in boxes:
        if b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h:
            return b.text
    # list rows are clickable across their width, so the pointer's own row wins
    row = [b for b in boxes if b.y - b.h * 0.5 <= y <= b.y + b.h * 1.5 and b.x < x]
    if row:
        return min(row, key=lambda b: (abs(b.cy - y), -b.x)).text
    best, dist = None, limit
    for b in boxes:
        dx = max(b.x - x, 0, x - (b.x + b.w))
        dy = max(b.y - y, 0, y - (b.y + b.h))
        d = float(np.hypot(dx, dy * 2.5))
        if d < dist:
            best, dist = b.text, d
    return best


def click_before(t0: float, track) -> tuple[float, float] | None:
    """Cursor resting in place just before a change began => probably a click there."""
    window = [(x, y) for t, x, y in track if t0 - 0.6 <= t <= t0 and x is not None]
    if len(window) < 2:
        return None
    xs, ys = [p[0] for p in window[-3:]], [p[1] for p in window[-3:]]
    if max(xs) - min(xs) <= 8 and max(ys) - min(ys) <= 8:
        return xs[-1], ys[-1]
    return None


def detect_scroll(prev: Keyframe, cur: Keyframe) -> tuple[int, list[int]] | None:
    """Same text, same column, shifted vertically together => the content scrolled."""
    shifts, ys = [], []
    by_text = {}
    for b in prev.boxes:
        by_text.setdefault(b.text, []).append(b)
    for nb in cur.boxes:
        for ob in by_text.get(nb.text, []):
            if abs(nb.cx - ob.cx) < 12 and abs(nb.cy - ob.cy) > 6:
                shifts.append(nb.cy - ob.cy)
                ys += [nb.y, nb.y + nb.h, ob.y, ob.y + ob.h]
                xs = (min(nb.x, ob.x), max(nb.x + nb.w, ob.x + ob.w))
    if len(shifts) < 3:
        return None
    med = statistics.median(shifts)
    agree = [s for s in shifts if abs(s - med) < 6]
    if len(agree) < max(3, len(shifts) * 0.6):
        return None
    region = [int(xs[0]) - 40, int(min(ys)) - 20, int(xs[1] - xs[0]) + 80, int(max(ys) - min(ys)) + 40]
    return round(-med), region  # content moving up = scrolled down (positive)


def describe(keys: list[Keyframe], track) -> list[dict]:
    events: list[dict] = [{"t": 0.0, "type": "start", "screen": keys[0].path.stem,
                           "text": [b.text for b in keys[0].boxes][:15]}]
    clicked: set[float] = set()  # one click per burst, even if it has two keyframes
    for prev, cur in zip(keys, keys[1:]):
        base = {"t": round(cur.t, 1), "screen": cur.path.stem}
        step: list[dict] = []

        if cur.burst_start is not None and cur.burst_start not in clicked:
            clicked.add(cur.burst_start)
            hit = click_before(cur.burst_start, track)
            if hit:
                step.append({**base, "t": round(cur.burst_start, 1), "type": "click",
                             "xy": [round(hit[0]), round(hit[1])],
                             "label": nearest_label(hit[0], hit[1], prev.boxes)})

        scroll = detect_scroll(prev, cur)
        if scroll:
            dy, region = scroll
            step.append({**base, "type": "scroll", "direction": "down" if dy > 0 else "up",
                         "dy_px": abs(dy), "box": region})

        def in_scroll(b: Box) -> bool:
            return bool(scroll) and b.inside(scroll[1])

        appeared, gone, matched = [], [], set()
        for nb in cur.boxes:
            pairs = [(nb.iou(ob), i) for i, ob in enumerate(prev.boxes)]
            iou, i = max(pairs, default=(0.0, -1))
            if iou > 0.3:
                matched.add(i)
                old = prev.boxes[i].text
                if old == nb.text or ocr_flicker(old, nb.text):
                    continue
                if URLISH.search(nb.text) and nb.y < 90:
                    step.append({**base, "type": "nav", "from": old, "to": nb.text})
                elif nb.text.startswith(old) and not in_scroll(nb):
                    step.append({**base, "type": "type", "xy": nb.xy(), "text": nb.text})
                elif not in_scroll(nb):
                    step.append({**base, "type": "text_changed", "xy": nb.xy(), "from": old, "to": nb.text})
            elif not in_scroll(nb):
                appeared.append(nb)
        for i, ob in enumerate(prev.boxes):
            if i not in matched and not in_scroll(ob) and not any(ob.iou(nb) > 0.3 for nb in cur.boxes):
                gone.append(ob)

        errors = [b for b in appeared if ERROR_WORDS.search(b.text)]
        for b in errors:
            step.append({**base, "type": "error_shown", "xy": b.xy(), "text": b.text})
        appeared = [b for b in appeared if b not in errors]
        panel, loose = column(appeared)
        if panel:
            step.append({**base, "type": "panel_opened", "count": len(panel),
                         "items": [b.text for b in panel][:6]})
        step += [{**base, "type": "text_appeared", "xy": b.xy(), "text": b.text} for b in loose]
        panel, loose = column(gone)
        if panel:
            step.append({**base, "type": "panel_closed", "count": len(panel),
                         "items": [b.text for b in panel][:6]})
        step += [{**base, "type": "text_gone", "text": b.text} for b in loose]

        # many rows changing at once = the list was replaced (scrolled, filtered)
        changed = [e for e in step if e["type"] == "text_changed"]
        if len(changed) >= 4:
            changed.sort(key=lambda e: e["xy"][1])
            xs = [e["xy"][0] for e in changed]
            ys = [e["xy"][1] for e in changed]
            step = [e for e in step if e["type"] != "text_changed"]
            step.append({**base, "type": "content_replaced", "rows": len(changed),
                         "box": [min(xs) - 150, min(ys) - 20, max(xs) - min(xs) + 300, max(ys) - min(ys) + 40],
                         "before": [e["from"] for e in changed][:4],
                         "after": [e["to"] for e in changed][:4]})

        # only a highlight changed: the pointer hovered, it didn't click
        if any(e["type"] == "click" for e in step) and not substantive(step, prev.boxes):
            for e in step:
                if e["type"] == "click":
                    e["type"] = "hover"
        if not step:
            step.append({**base, "type": "ui_change"})
        events += step
    return typed_after_click(merge_typing(events))[:MAX_EVENTS]


def substantive(step: list[dict], before: list[Box]) -> bool:
    """True if something changed beyond a highlight or an OCR misread."""
    import difflib

    seen = [b.text.lower() for b in before]

    def wobble(text: str) -> bool:
        t = text.lower()
        return any(t in s or s in t or difflib.SequenceMatcher(None, t, s).ratio() >= 0.7 for s in seen)

    for e in step:
        kind = e["type"]
        if kind in ("click", "ui_change", "text_gone"):
            continue
        if kind in ("text_appeared", "error_shown") and wobble(e["text"]):
            continue
        if kind == "text_changed" and wobble(e["to"]):
            continue
        return True
    return False


def typed_after_click(events: list[dict]) -> list[dict]:
    """Typing only counts in a field the user clicked first; otherwise it's text that appeared."""
    out, last_click = [], None
    for e in events:
        if e["type"] == "click":
            last_click = e
        if e["type"] == "type" and not (last_click and e["t"] - last_click["t"] < 10
                                        and abs(last_click["xy"][1] - e["xy"][1]) < 40):
            e = {**e, "type": "text_appeared"}
            e.pop("t_end", None)
        out.append(e)
    return out


def merge_typing(events: list[dict]) -> list[dict]:
    """S, SA, SAV, SAVE10 in one field => one 'type' event with the final text."""
    out: list[dict] = []
    for e in events:
        if e["type"] in ("type", "text_appeared") and "xy" in e:
            for p in reversed(out[-6:]):
                if (p["type"] == "type" or (p["type"] == "text_appeared" and len(p["text"]) <= 2)) \
                        and "xy" in p and abs(p["xy"][1] - e["xy"][1]) < 12 \
                        and abs(p["xy"][0] - e["xy"][0]) < 200 and e["text"].startswith(p["text"]) \
                        and e["t"] - p["t"] < 5:
                    p.update(type="type", text=e["text"], t_end=e["t"])
                    break
            else:
                out.append(e)
        else:
            out.append(e)
    # a field whose placeholder vanished as typing began is not news
    typed_at = {round(e["xy"][1] / 12) for e in out if e["type"] == "type"}
    return [e for e in out if not (e["type"] == "text_appeared" and len(e.get("text", "")) <= 2
                                   and round(e["xy"][1] / 12) in typed_at)]


# ---------------------------------------------------------------- output

def _changed_boxes(a: np.ndarray, b: np.ndarray, limit: int = 6) -> list[tuple[int, int, int, int]]:
    """Largest regions that changed between two frames; small ones only when shaped like text, not a pointer or caret."""
    _, mask = cv2.threshold(cv2.absdiff(a, b), 25, 255, cv2.THRESH_BINARY)
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in contours]
    boxes = [bx for bx in boxes if bx[2] > CURSOR_MAX or bx[3] > CURSOR_MAX or bx[2] >= 1.5 * bx[3]]
    return sorted(boxes, key=lambda bx: -bx[2] * bx[3])[:limit]


def zoom_changes(film_dir: Path, limit: int = 40, pad: int = 24, small: int = 420) -> None:
    """Full-size close-ups of small regions that changed between film frames: tooltips, focus rings, toggles."""
    frames = sorted((film_dir / "frames").glob("*.jpg"))
    dest = film_dir / "zoom"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    found = []
    for a, b in zip(frames, frames[1:]):
        img = cv2.imread(str(b))
        boxes = _changed_boxes(cv2.imread(str(a), cv2.IMREAD_GRAYSCALE), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), limit=3)
        H, W = img.shape[:2]
        for x, y, w, h in boxes:
            if w > small or h > small:  # big changes are readable on the sheets already
                continue
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
            crop = cv2.resize(img[y0:y1, x0:x1], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            found.append((b.stem, (x0, y0), crop))
    for n, (t, (x, y), crop) in enumerate(found[:limit]):
        cv2.imwrite(str(dest / f"{t}-{n:02d}@{x},{y}.jpg"), crop, [cv2.IMWRITE_JPEG_QUALITY, 85])


def film(frames: list[tuple[float, Path]], track, dest: Path, per_sheet: int = 4, thumb: int = 780) -> None:
    """Frames every half second with what changed boxed in red and the pointer ringed in yellow.

    Sheets of 4 for reading the sequence; full-size JPEGs in film/frames/ for reading small text.
    Stretches where nothing changed are skipped."""
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "frames").mkdir(parents=True)
    duration = frames[-1][0]
    fps = 2 if duration <= 90 else 1
    step = max(1, round(SAMPLE_FPS / fps))
    pointer = {round(t, 1): (x, y) for t, x, y in track if x is not None}
    picked, prev = [], None
    for i in range(0, len(frames), step):
        t, path = frames[i]
        img = cv2.imread(str(path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        boxes = _changed_boxes(prev, gray) if prev is not None else []
        moved = prev is not None and bool(cv2.countNonZero(cv2.threshold(cv2.absdiff(prev, gray), 25, 255,
                                                                          cv2.THRESH_BINARY)[1]))
        prev = gray
        if picked and not moved and i + step < len(frames):
            continue
        cv2.imwrite(str(dest / "frames" / f"{t:06.1f}s.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        marked = img.copy()
        for x, y, w, h in boxes:
            cv2.rectangle(marked, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if round(t, 1) in pointer:
            px, py = pointer[round(t, 1)]
            cv2.circle(marked, (int(px), int(py)), 16, (0, 220, 255), 3)
        picked.append((t, marked))
    for n in range(0, len(picked), per_sheet):
        chunk = picked[n:n + per_sheet]
        thumbs = []
        for t, img in chunk:
            img = cv2.resize(img, (thumb, int(img.shape[0] * thumb / img.shape[1])))
            cv2.rectangle(img, (0, 0), (120, 30), (0, 0, 0), -1)
            cv2.putText(img, f"{t:5.1f}s", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            thumbs.append(cv2.copyMakeBorder(img, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=(255, 255, 255)))
        while len(thumbs) % 2:
            thumbs.append(np.full_like(thumbs[0], 255))
        rows = [np.hstack(thumbs[i:i + 2]) for i in range(0, len(thumbs), 2)]
        cv2.imwrite(str(dest / f"{chunk[0][0]:06.1f}s-{chunk[-1][0]:06.1f}s.jpg"), np.vstack(rows),
                    [cv2.IMWRITE_JPEG_QUALITY, 85])


def contact_sheet(keys: list[Keyframe], dest: Path, cols: int = 4) -> None:
    thumbs = []
    for k in keys:
        img = cv2.imread(str(k.path))
        img = cv2.resize(img, (480, int(img.shape[0] * 480 / img.shape[1])))
        cv2.rectangle(img, (0, 0), (130, 32), (0, 0, 0), -1)
        cv2.putText(img, f"{k.t:6.1f}s", (6, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        thumbs.append(img)
    h = max(t.shape[0] for t in thumbs)
    thumbs = [cv2.copyMakeBorder(t, 0, h - t.shape[0], 0, 0, cv2.BORDER_CONSTANT) for t in thumbs]
    while len(thumbs) % cols:
        thumbs.append(np.zeros_like(thumbs[0]))
    rows = [np.hstack(thumbs[i:i + cols]) for i in range(0, len(thumbs), cols)]
    cv2.imwrite(str(dest), np.vstack(rows))


DRAG_MIN = 40  # px the pointer must travel for a drag


def _movements(track) -> list[tuple[int, int]]:
    """(start, end) frame indices of each stretch where the pointer travelled."""
    out, start = [], None
    for i in range(1, len(track)):
        a, b = track[i - 1], track[i]
        moving = a[1] is not None and b[1] is not None and np.hypot(b[1] - a[1], b[2] - a[2]) > 2
        if moving and start is None:
            start = i - 1
        elif not moving and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(track) - 1))
    return out


def _region(img: np.ndarray, x: float, y: float, r: int = 40) -> np.ndarray | None:
    x, y = int(x), int(y)
    if x < r or y < r or x + r > img.shape[1] or y + r > img.shape[0]:
        return None
    return img[y - r:y + r, x - r:x + r].astype(np.float32)


def _local_change(before: np.ndarray, after: np.ndarray, path: list[tuple[float, float]], r: int = 45) -> bool:
    """True if at least half of what changed lies near the pointer's path."""
    _, changed = cv2.threshold(cv2.absdiff(before, after), 25, 255, cv2.THRESH_BINARY)
    total = int(np.count_nonzero(changed))
    if total == 0 or len(path) < 2:
        return False
    corridor = np.zeros_like(changed)
    pts = np.array([[int(x), int(y)] for x, y in path], np.int32)
    cv2.polylines(corridor, [pts], False, 255, thickness=2 * r)
    return np.count_nonzero(changed & corridor) / total >= 0.5


def _stroke_at(diff: np.ndarray, x: float, y: float, off: int = 20) -> bool:
    """Ink is a thin line: changed on the path, unchanged a little to either side."""
    def mean(cx, cy):
        cx, cy = int(cx), int(cy)
        patch = diff[max(cy - 3, 0):cy + 4, max(cx - 3, 0):cx + 4]
        return float(patch.mean()) if patch.size else 0.0
    if mean(x, y) <= 20:
        return False
    sides = [mean(x + off, y), mean(x - off, y), mean(x, y + off), mean(x, y - off)]
    return sum(v < 10 for v in sides) >= 2


def detect_drags(grays, track, keys) -> list[dict]:
    """A drag moves something with the pointer, or leaves a lasting mark along its path."""
    drags = []
    for s, e in _movements(track):
        (t0, x0, y0), (_, x1, y1) = track[s], track[e]
        if np.hypot(x1 - x0, y1 - y0) < DRAG_MIN or track[e][0] - t0 > 6:
            continue
        before, after = grays[max(s - 1, 0)], grays[min(e + 1, len(grays) - 1)]
        path = [(x, y) for _, x, y in track[s:e + 1] if x is not None]
        if not _local_change(before, after, path):
            continue  # most of the change is elsewhere: a menu or page changed, not a drag
        moved = False
        a, b, left = _region(before, x0, y0), _region(after, x1, y1), _region(after, x0, y0)
        if a is not None and b is not None and left is not None and a.std() > 12:
            moved = _same(a, b) > 0.85 and _same(a, left) < 0.6
        diff = cv2.absdiff(before, after)
        inked = len(path) >= 3 and sum(_stroke_at(diff, x, y) for x, y in path) / len(path) >= 0.6
        if not (moved or inked):
            continue
        prior = [k for k in keys if k.t <= t0] or keys[:1]
        boxes = prior[-1].boxes
        drags.append({"t": round(t0, 1), "type": "drag", "xy": [round(x0), round(y0)], "to": [round(x1), round(y1)],
                      "label": nearest_label(x0, y0, boxes), "label_to": nearest_label(x1, y1, boxes),
                      "how": "moved" if moved else "drew"})
    return drags


def add_drags(events: list[dict], drags: list[dict]) -> list[dict]:
    """Drags replace the 'click' that their starting press looks like."""
    def starts_drag(e: dict) -> bool:
        return e["type"] in ("click", "hover") and any(
            abs(d["t"] - e["t"]) <= 0.6 and np.hypot(d["xy"][0] - e["xy"][0], d["xy"][1] - e["xy"][1]) < 30 for d in drags)
    return sorted([e for e in events if not starts_drag(e)] + drags, key=lambda e: e["t"])


def zoom_clicks(events: list[dict], frames: list[tuple[float, Path]], out: Path, half: int = 90) -> None:
    """Save a close-up of each click so the agent can see icon buttons with no text."""
    zdir = out / "clicks"
    if zdir.exists():
        shutil.rmtree(zdir)
    clicks = [e for e in events if e["type"] == "click"]
    if not clicks:
        return
    zdir.mkdir()
    times = [t for t, _ in frames]
    for e in clicks:
        i = max(0, min(range(len(times)), key=lambda k: abs(times[k] - e["t"])) - 1)
        img = cv2.imread(str(frames[i][1]))
        x, y = e["xy"]
        H, W = img.shape[:2]
        x0, y0 = max(0, x - half), max(0, y - half)
        crop = img[y0:min(H, y + half), x0:min(W, x + half)].copy()
        cv2.circle(crop, (x - x0, y - y0), 14, (0, 0, 255), 2)
        crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        name = f"{e['t']:06.1f}s.png"
        cv2.imwrite(str(zdir / name), crop)
        e["zoom"] = f"clicks/{name}"


def ingest(video: Path, out: Path) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_frames"
    frames = extract_frames(video, tmp)
    if not frames:
        sys.exit(f"no frames extracted from {video}")
    keys, track, grays = scan(frames)

    kdir = out / "keyframes"
    if kdir.exists():
        shutil.rmtree(kdir)
    kdir.mkdir()
    H, W = cv2.imread(str(keys[0].path)).shape[:2]
    for k in keys:
        dst = kdir / f"{k.t:06.1f}s.png"
        shutil.copy(k.path, dst)
        k.path = dst
        k.boxes = ocr(dst, W, H)

    events = describe(keys, track)
    if os.environ.get("DEJABUG_DRAGS") == "1":  # experimental: still finds drags that didn't happen
        events = add_drags(events, detect_drags(grays, track, keys))
    zoom_clicks(events, frames, out)
    with open(out / "events.jsonl", "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with open(out / "cursor.jsonl", "w", encoding="utf-8") as f:
        for t, x, y in track:
            if x is not None:
                f.write(json.dumps({"t": round(t, 1), "xy": [round(x), round(y)]}) + "\n")
    contact_sheet(keys, out / "contact_sheet.png")
    film(frames, track, out / "film")
    zoom_changes(out / "film")
    shutil.rmtree(tmp)
    print(f"{len(frames)} frames -> {len(keys)} keyframes -> {len(events)} events  ({out})")
    return events


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python -m dejabug.ingest <video> <out_dir>")
    ingest(Path(sys.argv[1]), Path(sys.argv[2]))
