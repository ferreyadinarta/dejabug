"""Record a bug video of demo/shop.html, the way a user would see it."""
from pathlib import Path
from playwright.sync_api import sync_playwright

here = Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport={"width": 1280, "height": 720},
                        record_video_dir=str(here / "videos"),
                        record_video_size={"width": 1280, "height": 720})
    page = ctx.new_page()
    page.goto((here / "shop.html").as_uri())
    page.wait_for_timeout(1200)
    page.click("#add"); page.wait_for_timeout(1000)
    page.click("#code"); page.wait_for_timeout(500)
    page.type("#code", "SAVE10", delay=180); page.wait_for_timeout(800)
    page.click("#apply"); page.wait_for_timeout(2500)
    ctx.close(); b.close()
vids = sorted((here / "videos").glob("*.webm"))
vids[-1].rename(here / "bug.webm")
print("recorded", here / "bug.webm")
