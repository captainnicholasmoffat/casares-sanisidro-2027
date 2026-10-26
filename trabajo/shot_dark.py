import sys, threading, http.server, socketserver, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Q); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":390,"height":844}, color_scheme="dark")
        pg = await ctx.new_page()
        await pg.goto(f"http://127.0.0.1:{port}/"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(1500)
        await pg.evaluate("[...document.querySelectorAll('.ch-card')][4].click()"); await pg.wait_for_timeout(600)
        await pg.evaluate("[...document.querySelectorAll('#l-side ul button')].find(x=>x.textContent.startsWith('5.5')).click()"); await pg.wait_for_timeout(800)
        await pg.evaluate("document.getElementById('lector').scrollTop = 2600"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(OUT/"dark_55.png"))
        await pg.evaluate("[...document.querySelectorAll('#l-side .grp')].find(x=>x.textContent.indexOf('Diagnóstico')>=0).click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("[...document.querySelectorAll('#l-side ul button')].find(x=>x.textContent.startsWith('1.2')).click()"); await pg.wait_for_timeout(800)
        await pg.evaluate("document.querySelector('.lec-cuadro table').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(OUT/"dark_12.png"))
        await b.close()
asyncio.run(main())
