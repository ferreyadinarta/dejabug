from playwright.sync_api import sync_playwright
JS = "() => [...document.querySelectorAll('input[type=radio]:checked')].map(e => e.getAttribute('data-testid') || e.getAttribute('aria-label')).join(',')"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for port in (5181, 5182):
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.goto(f"http://localhost:{port}"); pg.wait_for_timeout(2500)
        pg.mouse.click(1000, 600)
        print(port, "start:", pg.evaluate(JS), "embeds:", pg.locator("iframe").count())
        pg.keyboard.press("Alt+r"); pg.wait_for_timeout(400)
        print(port, "view mode:", pg.locator(".excalidraw.excalidraw--view-mode").count())
        pg.keyboard.press("k"); pg.wait_for_timeout(300)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        pg.keyboard.press("Alt+r"); pg.wait_for_timeout(500)
        print(port, "after exit view mode:", pg.evaluate(JS), "view mode:", pg.locator(".excalidraw--view-mode").count())
    b.close()
