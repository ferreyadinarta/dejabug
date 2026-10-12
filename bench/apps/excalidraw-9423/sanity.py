from playwright.sync_api import sync_playwright
JS = "() => { const els = window.__api?.getSceneElements?.(); return null }"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for port in (5181, 5182):
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.goto(f"http://localhost:{port}"); pg.wait_for_timeout(2500)
        stats = pg.locator(".exc-stats")
        print(port, "stats visible:", stats.count(), stats.first.inner_text()[:300].replace("\n"," | ") if stats.count() else "")
        inp = pg.locator(".exc-stats .drag-input").first
        print(port, "inputs:", pg.locator(".exc-stats input").count())
        x = pg.locator(".exc-stats input").first
        x.fill("14600"); x.press("Enter"); pg.wait_for_timeout(500)
        pg.keyboard.press("Control+a"); pg.wait_for_timeout(300)
        print(port, "after X=14600, select all ->", pg.locator(".exc-stats").first.inner_text()[:400].replace("\n"," | "))
        pg.screenshot(path=f"/private/tmp/claude-501/-Users-mkpmobile-Documents-Ferrey-Code/f8e96c02-04ce-4241-b9b7-d906a4fe83f5/scratchpad/ex9423/s{port}.png")
    b.close()
