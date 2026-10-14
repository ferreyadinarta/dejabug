"""Render docs/steps-demo.gif: the bug video on the left, dejabug's steps appearing on the right as they happen.

usage: python docs/make_steps_demo.py <video> <steps.json> <command shown> <out.gif>
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H, VIDEO_W, FPS, HOLD = 1200, 560, 640, 8, 4.0
BG, PANEL, INK, DIM, RED, BAR = (250, 250, 249), (255, 255, 255), (28, 28, 30), (120, 120, 128), (200, 40, 40), (30, 30, 34)
SANS = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 17)
SANS_BOLD = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 19)
MONO = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 15)
VERB = {"click": "Click", "double_click": "Double-click", "type": "Type", "press": "Press", "drag": "Drag",
        "scroll": "Scroll", "hover": "Hover over", "right_click": "Right-click"}


def frames(video: Path, tmp: Path) -> list[Image.Image]:
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(video), "-vf",
                    f"fps={FPS},scale={VIDEO_W}:-2", str(tmp / "f%04d.png")], check=True)
    return [Image.open(p).convert("RGB") for p in sorted(tmp.glob("f*.png"))]


def step_lines(data: dict, now: float) -> list[tuple[str, tuple]]:
    out = []
    for n, s in enumerate(data["steps"], 1):
        if s["t"] <= now:
            what = f'"{s["text"]}" in ' if s.get("text") and s["action"] in ("type",) else ""
            out.append((f"{n}. {VERB.get(s['action'], s['action'])} {what}{s['target']} ({s['t']:.1f}s)", INK))
    bug = data.get("bug") or {}
    if bug and bug["t"] <= now:
        out.append(("", INK))
        out.append((f"Bug ({bug['t']:.1f}s): {bug['what']}", RED))
    return out


def render(video_frame: Image.Image, data: dict, now: float, command: str) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 44), fill=BAR)
    d.text((18, 13), f"$ {command}", font=MONO, fill=(230, 230, 230))
    y0 = 44 + (H - 44 - video_frame.height) // 2
    img.paste(video_frame, (16, y0))
    d.text((16, H - 26), f"the reporter's video  {now:4.1f}s", font=MONO, fill=DIM)
    x, y = VIDEO_W + 40, 64
    d.rectangle((x - 16, 56, W - 16, H - 16), fill=PANEL, outline=(225, 225, 228))
    d.text((x, y), "Steps to reproduce", font=SANS_BOLD, fill=INK)
    y += 36
    for line, color in step_lines(data, now):
        for part in (textwrap.wrap(line, 56) or [""]):
            d.text((x, y), part, font=SANS, fill=color)
            y += 24
        y += 4
    return img


def main() -> int:
    video, steps, command, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
    data = json.loads(steps.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        vf = frames(video, Path(tmp))
    shots = [render(f, data, i / FPS, command) for i, f in enumerate(vf)]
    shots += [shots[-1]] * int(HOLD * FPS)
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=int(1000 / FPS), loop=0, optimize=True)
    print(out, f"{out.stat().st_size / 1e6:.1f} MB", len(shots), "frames")
    return 0


if __name__ == "__main__":
    sys.exit(main())
