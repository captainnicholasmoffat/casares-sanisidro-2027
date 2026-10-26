"""Prueba la portada: sirve web/ local, intercepta los CDN con copias locales y saca capturas.
Uso: python3 shoot.py <carpeta web> <carpeta salida> [modo: light|dark]
"""
import sys, threading, http.server, functools, socketserver, time
from pathlib import Path
from playwright.sync_api import sync_playwright

WEB = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
SCHEME = sys.argv[3] if len(sys.argv) > 3 else 'light'
PKG = Path(__file__).parent / 'pkgchk' / 'package' / 'dist'
LIBS = {
    'gsap@3.15.0/dist/gsap.min.js': PKG / 'gsap.min.js',
    'gsap@3.15.0/dist/ScrollTrigger.min.js': PKG / 'ScrollTrigger.min.js',
    'lenis@1.3.26/dist/lenis.min.js': PKG / 'lenis.min.js',
}

class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(WEB), **k)
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

# La página publicada no lleva doctype: la envolvemos igual que el publicador
page_html = (WEB / 'index.html').read_text()
wrapped = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
           '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
           '</head><body>' + page_html + '</body></html>')
(WEB / '_test.html').write_text(wrapped)

def route(r):
    u = r.request.url
    for k, p in LIBS.items():
        if k in u:
            return r.fulfill(path=str(p), content_type='application/javascript')
    if 'fonts.googleapis' in u or 'fonts.gstatic' in u:
        return r.fulfill(body='', content_type='text/css')
    return r.continue_()

errors = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [('desk', {'width': 1440, 'height': 900}), ('mob', {'width': 390, 'height': 844})]:
        ctx = b.new_context(viewport=vp, device_scale_factor=1, color_scheme=SCHEME)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.on('console', lambda m: errors.append('console:' + m.text) if m.type == 'error' else None)
        pg.route('**/*', route)
        pg.goto(f'http://127.0.0.1:{port}/_test.html', wait_until='networkidle')
        time.sleep(1.5)
        H = pg.evaluate('document.documentElement.scrollHeight')
        ow = pg.evaluate('document.documentElement.scrollWidth > window.innerWidth')
        print(name, 'scrollHeight', H, 'overflowX', ow, 'scrub', pg.evaluate("document.documentElement.classList.contains('scrub')"))
        vh = vp['height']
        for i, frac in enumerate([0, 0.9, 1.9, 2.9, 3.9, 4.6]):
            pg.evaluate(f'window.scrollTo(0, {int(frac * vh)})')
            time.sleep(1.2)
            pg.screenshot(path=str(OUT / f'{name}_{i}.png'))
        pg.evaluate(f"document.querySelector('#propuestas').scrollIntoView()")
        time.sleep(1.0)
        pg.screenshot(path=str(OUT / f'{name}_nine.png'))
        pg.click('#toggle-all'); time.sleep(0.4)
        pg.screenshot(path=str(OUT / f'{name}_nine_open.png'))
        pg.evaluate("document.querySelector('.cien').scrollIntoView()"); time.sleep(0.8)
        pg.screenshot(path=str(OUT / f'{name}_cien.png'))
        ctx.close()
    b.close()
print('errors', errors[:10])
(WEB / '_test.html').unlink()
