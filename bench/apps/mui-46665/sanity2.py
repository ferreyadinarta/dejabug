from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for port in (5181,):
        pg = b.new_page(viewport={"width":1280,"height":800})
        pg.goto(f"http://localhost:{port}")
        cb = pg.get_by_role("combobox")
        cb.hover(); pg.wait_for_timeout(300); cb.click()
        pg.wait_for_timeout(800)
        print("hover-then-click open:", pg.locator('[role="listbox"]').is_visible(), pg.locator(".MuiSelect-nativeInput").input_value())
        pg.goto(f"http://localhost:{port}")
        cb = pg.get_by_role("combobox"); cb.click()
        try:
            pg.wait_for_selector('[role="listbox"]', timeout=3000); print("listbox seen after click")
            pg.get_by_role("option", name="20", exact=True).click(timeout=3000); print("clicked 20 ->", pg.locator(".MuiSelect-nativeInput").input_value())
        except Exception as e: print("err", str(e)[:120])
    b.close()
