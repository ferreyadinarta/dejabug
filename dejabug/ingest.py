"""Turn a screen recording into a short, readable event log.

    uv run python -m dejabug.ingest bug.mov out/

Writes:
    out/events.jsonl       one line per meaningful moment (clicks, typing, scrolls, errors...)
    out/cursor.jsonl       where the mouse cursor was, per sampled frame
    out/keyframes/*.png    the frames those events came from
    out/contact_sheet.png  every keyframe in one image, with timestamps

A 60 s recording is 1,800 frames, which no model reads well, and most of them
are identical. We find the moments the screen *settles* after a change, OCR
those, and describe what changed between them as text an agent can reason over.
"""

from __future__ import annotations

import json
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
from ocrmac import ocrmac

SAMPLE_FPS = 10         # frames per second pulled from the video
WIDTH = 1280            # frames are scaled to this width; all coordinates use this space
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
         "-vf", f"fps={SAMPLE_FPS},scale={WIDTH}:-2", str(dest / "f%05d.png")],
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
    """Places where a small blob keeps reappearing without moving: the text caret
    blinking, a spinner, a pulsing dot. The mouse pointer moves, so it never piles
    up in one spot like this."""
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
    """The pointer is a small thing that *travels*: the patch that vanished from
    spot A reappears, unchanged, at spot B. A checkbox ticking or a caret blinking
    changes in place and never forms such a pair."""
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


def scan(frames: list[tuple[float, Path]]):
    """Keyframes at each settle point, plus a track of the mouse pointer."""
    keys = [Keyframe(frames[0][0], frames[0][1])]
    track: list[tuple[float, float | None, float | None]] = []

    grays = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for _, p in frames]
    steps = [(0.0, [], [])] + [split_change(a, b) for a, b in zip(grays, grays[1:])]
    blinks = blink_spots(steps)

    cursor_pos: tuple[float, float] | None = None
    burst_start, burst_frames, quiet = None, [], 0

    for i, (t, path) in enumerate(frames):
        if i:
            frac, blobs, _ = steps[i]
            blobs = [b[:2] for b in blobs if is_pointer(b, blinks)]
            moved = pointer_move(grays[i - 1], grays[i], blobs, cursor_pos)
            if moved:
                cursor_pos = moved
            if frac >= MIN_CHANGE:
                if burst_start is None:
                    burst_start = t
                burst_frames.append((t, path))
                quiet = 0
            elif burst_start is not None:
                quiet += 1
                if quiet >= REST_FRAMES:
                    if t - burst_start > LONG_BURST and len(burst_frames) > 2:
                        mt, mp = burst_frames[len(burst_frames) // 2]
                        keys.append(Keyframe(mt, mp, burst_start))
                    keys.append(Keyframe(t, path, burst_start))
                    burst_start, burst_frames, quiet = None, [], 0
        track.append((t, *(cursor_pos if cursor_pos else (None, None))))

    last_t, last_path = frames[-1]
    if keys[-1].path != last_path:
        keys.append(Keyframe(last_t, last_path, burst_start))
    return keys, track


# ---------------------------------------------------------------- OCR

LEADING_JUNK = re.compile(r"^(?:[^\w(\"'$€£¥₹]+|[DПO□☐]\s+)+")  # bullets, checkboxes OCR'd as letters


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", LEADING_JUNK.sub("", text.strip()))


def ocr(path: Path, W: int, H: int) -> list[Box]:
    out = []
    for text, conf, (x, y, w, h) in ocrmac.OCR(str(path), recognition_level="accurate").recognize():
        text = clean(text)
        if conf < MIN_CONF or not text:
            continue
        if len(text) == 1 and not text.isdigit():
            continue  # stray glyphs: checkbox squares, icons, cursor carets
        # Vision returns normalized coords with a bottom-left origin.
        out.append(Box(text, float(conf), x * W, (1 - y - h) * H, w * W, h * H))
    return out


# ---------------------------------------------------------------- events

def column(boxes: list[Box]) -> tuple[list[Box], list[Box]]:
    """Split texts into the largest left-aligned column (a list, menu or panel
    appearing as one) and everything else."""
    best: list[Box] = []
    for b in boxes:
        col = [o for o in boxes if abs(o.x - b.x) < 40]
        if len(col) > len(best):
            best = col
    if len(best) < PANEL_MIN:
        return [], boxes
    best.sort(key=lambda b: b.y)
    return best, [b for b in boxes if b not in best]


def ocr_flicker(a: str, b: str) -> bool:
    """'Part II' vs 'Part lI': the same text read slightly differently."""
    if abs(len(a) - len(b)) > 1:
        return False
    import difflib
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.9


def nearest_label(x: float, y: float, boxes: list[Box], limit: float = 70) -> str | None:
    best, dist = None, limit
    for b in boxes:
        # distance from point to box edge (0 if inside)
        dx = max(b.x - x, 0, x - (b.x + b.w))
        dy = max(b.y - y, 0, y - (b.y + b.h))
        d = float(np.hypot(dx, dy))
        if d < dist:
            best, dist = b.text, d
    if best is None:
        # Rows in lists and menus are clickable across their full width, while
        # their text sits at the left. Fall back to text on the same row.
        row = [b for b in boxes if abs(b.cy - y) < max(16, b.h * 1.6) and b.x < x]
        if row:
            best = max(row, key=lambda b: b.x).text
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
    for prev, cur in zip(keys, keys[1:]):
        base = {"t": round(cur.t, 1), "screen": cur.path.stem}
        step: list[dict] = []

        if cur.burst_start is not None:
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

        # Many rows in one column changing at once is a list being replaced
        # (scrolled past, filtered, re-sorted), not a dozen separate edits.
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

        if not step:
            step.append({**base, "type": "ui_change"})
        events += step
    return merge_typing(events)[:MAX_EVENTS]


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


def ingest(video: Path, out: Path) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_frames"
    frames = extract_frames(video, tmp)
    if not frames:
        sys.exit(f"no frames extracted from {video}")
    keys, track = scan(frames)

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
    with open(out / "events.jsonl", "w") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with open(out / "cursor.jsonl", "w") as f:
        for t, x, y in track:
            if x is not None:
                f.write(json.dumps({"t": round(t, 1), "xy": [round(x), round(y)]}) + "\n")
    contact_sheet(keys, out / "contact_sheet.png")
    shutil.rmtree(tmp)
    print(f"{len(frames)} frames -> {len(keys)} keyframes -> {len(events)} events  ({out})")
    return events


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python -m dejabug.ingest <video> <out_dir>")
    ingest(Path(sys.argv[1]), Path(sys.argv[2]))
