from playwright.sync_api import sync_playwright
U = 'http://localhost:8765/despliegue/'
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1280, 400):
        pg = b.new_page(viewport={'width': w, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(U); pg.wait_for_selector('#gantt .g-row')
        pg.click('#open-all')
        for z in ('y2', 'y4'):
            pg.click(f'.zoom button[data-z="{z}"]'); pg.wait_for_timeout(200)
            bad = pg.evaluate('''() => { const g = document.querySelector('#gantt'); const lab = g.querySelector('.g-lab').getBoundingClientRect().right;
              return [...g.querySelectorAll('.g-bar,.g-hito')].filter(e => e.getBoundingClientRect().left < lab - 1 && g.scrollLeft === 0).length }''')
            print(w, z, 'hint', pg.is_visible('#z-hint'), 'barras sobre etiquetas', bad, 'ancho', pg.evaluate('document.querySelector("#gantt").scrollWidth'), 'pagina', pg.evaluate('document.documentElement.scrollWidth'))
        pg.screenshot(path=f'z_{w}.png')
        pg.click('.zoom button[data-z="all"]'); print('hint en todo', pg.is_visible('#z-hint'))
        # hoja
        pg.evaluate('location.hash = "#a-T02"'); pg.wait_for_timeout(300)
        print('abre T02', pg.text_content('#sh-code'), 'volver visible', pg.is_visible('#sh-back'))
        pg.click('#sh-b .deps button >> nth=0'); pg.wait_for_timeout(200)
        print('salto a', pg.text_content('#sh-code'), '|', pg.text_content('#sh-back'))
        pg.click('#sh-b .deps button >> nth=-1'); pg.wait_for_timeout(200)
        print('salto a', pg.text_content('#sh-code'), '|', pg.text_content('#sh-back'))
        if w == 400: pg.screenshot(path='sheet_400.png')
        pg.click('#sh-back'); pg.wait_for_timeout(200); print('volver ->', pg.text_content('#sh-code'), '|', pg.text_content('#sh-back'))
        pg.go_back(); pg.wait_for_timeout(300); print('gesto atras ->', pg.text_content('#sh-code'), 'abierta', pg.is_visible('#sheet'), 'volver', pg.is_visible('#sh-back'))
        pg.go_back(); pg.wait_for_timeout(300); print('gesto atras ->', 'abierta', pg.is_visible('#sheet'), pg.evaluate('location.hash'))
        pg.click('#spine button >> nth=3'); pg.wait_for_timeout(200); pg.click('#sh-b .deps button >> nth=0'); pg.wait_for_timeout(200)
        pg.click('#sh-x'); pg.wait_for_timeout(300); print('cerrar ->', 'abierta', pg.is_visible('#sheet'), repr(pg.evaluate('location.hash')))
        print('errores', errs)
    b.close()
