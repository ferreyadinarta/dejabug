import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for port in (5183, 5184):
        pg = b.new_page(viewport={'width':1280,'height':720})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(f'http://localhost:{port}'); pg.wait_for_selector('.tl-canvas', timeout=30000); pg.wait_for_timeout(1500)
        pg.screenshot(path='/private/tmp/claude-501/-Users-mkpmobile-Documents-Ferrey-Code/f8e96c02-04ce-4241-b9b7-d906a4fe83f5/scratchpad/s%d_a.png'%port)
        pg.keyboard.press('d'); pg.wait_for_timeout(300)
        pg.mouse.click(900, 550, button='right'); pg.wait_for_timeout(800)
        n = pg.locator('.tlui-menu').count()
        print(port, 'menus', n, 'errs', errs[:2])
        pg.screenshot(path='/private/tmp/claude-501/-Users-mkpmobile-Documents-Ferrey-Code/f8e96c02-04ce-4241-b9b7-d906a4fe83f5/scratchpad/s%d_b.png'%port)
    b.close()
