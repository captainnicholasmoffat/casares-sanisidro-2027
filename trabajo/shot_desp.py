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
        for name, vp in [("d", {"width":1440,"height":900}), ("m", {"width":390,"height":844})]:
            ctx = await b.new_context(viewport=vp); pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto(f"http://127.0.0.1:{port}/despliegue/"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(1200)
            await pg.screenshot(path=str(OUT/f"{name}_top.png"))
            await pg.evaluate("document.getElementById('views').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"{name}_gantt.png"))
            await pg.click('.zoom button[data-z="18"]'); await pg.click('#open-all'); await pg.wait_for_timeout(300)
            await pg.evaluate("window.scrollBy(0, 300)"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/f"{name}_gantt18.png"))
            await pg.click('#tab-c'); await pg.wait_for_timeout(300)
            await pg.evaluate("document.getElementById('views').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/f"{name}_cien.png"))
            await pg.click('#tab-s'); await pg.wait_for_timeout(300)
            await pg.evaluate("document.getElementById('views').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/f"{name}_streams.png"))
            await pg.click('#tab-l'); await pg.wait_for_timeout(300)
            await pg.evaluate("document.getElementById('views').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/f"{name}_lista.png"))
            await pg.click('#tab-c'); await pg.wait_for_timeout(300)
            await pg.evaluate("[...document.querySelectorAll('#cien .item button')].find(b=>b.textContent.indexOf('compromiso 14')>=0 || b.textContent.indexOf('inteligencia artificial')>=0).click()"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(OUT/f"{name}_detalle.png"))
            ov = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
            print(name, "errores:", errs[:4], "anchos:", ov)
            await ctx.close()
        await b.close()
asyncio.run(main())
