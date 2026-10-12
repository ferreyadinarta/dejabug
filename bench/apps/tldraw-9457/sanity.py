from playwright.sync_api import sync_playwright
def drag(pg, src, dst, steps=12):
    b = src.bounding_box(); x0, y0 = b['x']+b['width']/2, b['y']+b['height']/2
    pg.mouse.move(x0, y0); pg.mouse.down()
    for i in range(1, steps+1):
        pg.mouse.move(x0+(dst[0]-x0)*i/steps, y0+(dst[1]-y0)*i/steps); pg.wait_for_timeout(30)
    pg.wait_for_timeout(300); pg.mouse.up(); pg.wait_for_timeout(500)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome')
    for port in (5183, 5184):
        for mode in ('toolbar', 'popup'):
            pg = br.new_page(viewport={'width':1280,'height':720})
            pg.goto(f'http://localhost:{port}'); pg.wait_for_selector('.tl-canvas'); pg.wait_for_timeout(1200)
            fr = pg.locator('.tl-shape[data-shape-type=frame]').bounding_box()
            if mode == 'toolbar':
                src = pg.locator('[data-testid="tools.rectangle"]').first
            else:
                pg.locator('[data-testid="tools.more-button"]').click(); pg.wait_for_timeout(400)
                src = pg.locator('.tlui-popover__content [data-testid="tools.more.rectangle"], [data-testid="tools.more.rectangle"]').first
            drag(pg, src, (fr['x']+fr['width']*0.45, fr['y']+fr['height']*0.5))
            geo = pg.locator('.tl-shape[data-shape-type=geo]')
            cp = geo.first.evaluate("e => getComputedStyle(e).clipPath") if geo.count() else None
            print(port, mode, 'frame', fr, 'geo count', geo.count(), 'clip', cp)
            pg.screenshot(path='/private/tmp/claude-501/-Users-mkpmobile-Documents-Ferrey-Code/f8e96c02-04ce-4241-b9b7-d906a4fe83f5/scratchpad/9457_%d_%s.png'%(port,mode))
            pg.close()
    br.close()
