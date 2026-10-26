import sys, threading, http.server, socketserver, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{port}/"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if Path('/opt/pw-browsers/chromium').exists() else None)
        for name, vp in [("d", {"width":1440,"height":900}), ("m", {"width":390,"height":844})]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(2000)
            await pg.screenshot(path=str(OUT/f"{name}_home.png"), full_page=True)
            for tag, js in [("ch5", "document.querySelectorAll('.tile')[6].click()"), ("ap55", "1"), ("glos", "1"), ("anexo", "1")]:
                if tag == "ch5":
                    await pg.evaluate(js)
                else:
                    target = {"ap55":"5.5","glos":"glosario","anexo":"anexo"}[tag]
                    await pg.evaluate("""(t)=>{ const bs=[...document.querySelectorAll('#l-side button')]; let b; if(t==='5.5'){ b=bs.find(x=>x.textContent.startsWith('5.5')); } else if(t==='glosario'){ b=bs.find(x=>x.textContent.startsWith('Glosario')); } else { b=bs.find(x=>x.textContent.startsWith('Anexo')); } if(b) b.click(); }""", target)
                await pg.wait_for_timeout(500)
                await pg.screenshot(path=str(OUT/f"{name}_{tag}.png"))
                await pg.evaluate("document.getElementById('lector').scrollTop = 1400")
                await pg.wait_for_timeout(200)
                await pg.screenshot(path=str(OUT/f"{name}_{tag}_b.png"))
            print(name, "errors:", errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
