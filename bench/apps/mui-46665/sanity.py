import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", slow_mo=int(sys.argv[1]) if len(sys.argv)>1 else 0)
    for port in (5181, 5182):
        pg = b.new_page()
        pg.goto(f"http://localhost:{port}")
        pg.locator("#age-select").click()
        pg.wait_for_timeout(800)
        print(port, "menu open:", pg.locator('[role="listbox"]').is_visible(), "value:", pg.locator("#age-select").inner_text())
        # click elsewhere in the select (e.g. right part)
        pg.goto(f"http://localhost:{port}")
        box = pg.locator("#age-select").bounding_box()
        pg.mouse.click(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.5)
        pg.wait_for_timeout(800)
        print(port, "center-click open:", pg.locator('[role="listbox"]').is_visible(), "value:", pg.locator("#age-select").inner_text())
    b.close()
