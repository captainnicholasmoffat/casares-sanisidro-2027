import sys, threading, http.server, socketserver, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Q); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{port}/"
OPEN_CH = "(n)=>{ [...document.querySelectorAll('.ch-card')][n].click(); }"
OPEN_AP = "(t)=>{ const b=[...document.querySelectorAll('#l-side ul button')].find(x=>x.textContent.startsWith(t)); if(b) b.click(); else throw new Error('no '+t); }"
OPEN_GRP = "(t)=>{ const b=[...document.querySelectorAll('#l-side .grp')].find(x=>x.textContent.indexOf(t)>=0); b.click(); }"
async def settle(pg):
    await pg.wait_for_timeout(400)
    await pg.evaluate("Promise.all([...document.querySelectorAll('#lector img')].map(i=>{i.loading='eager'; return i.complete?1:new Promise(r=>{i.onload=i.onerror=r; setTimeout(r,3000);});}))")
    await pg.wait_for_timeout(300)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp in [("d", {"width":1440,"height":900}), ("m", {"width":390,"height":844})]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=1)
            pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto(URL); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(1500)
            await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(OUT/f"{name}_home.png"), full_page=True)
            # capítulo 5 (portada del capítulo)
            await pg.evaluate(OPEN_CH, 4); await settle(pg)
            await pg.screenshot(path=str(OUT/f"{name}_c5.png"))
            await pg.evaluate("document.getElementById('lector').scrollTop = %d" % (700 if name=='d' else 600)); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/f"{name}_c5b.png"))
            # 5.5 Ambiente
            await pg.evaluate(OPEN_AP, "5.5"); await settle(pg)
            await pg.screenshot(path=str(OUT/f"{name}_55.png"))
            for i, y in enumerate([900, 1900, 3200]):
                await pg.evaluate("document.getElementById('lector').scrollTop = %d" % y); await pg.wait_for_timeout(200)
                await pg.screenshot(path=str(OUT/f"{name}_55_{i}.png"))
            # 4.5 con el esquema del mecanismo
            await pg.evaluate(OPEN_GRP, "El mecanismo"); await settle(pg)
            await pg.evaluate(OPEN_AP, "4.5"); await settle(pg)
            await pg.evaluate("document.querySelector('.lec-cuadro').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"{name}_45.png"))
            # 1.1 con gráficos y fotos de a dos
            await pg.evaluate(OPEN_GRP, "Diagnóstico"); await settle(pg)
            await pg.evaluate(OPEN_AP, "1.1"); await settle(pg)
            await pg.evaluate("document.querySelector('.lec-cuadro').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"{name}_11.png"))
            await pg.evaluate("document.querySelector('.lec-fig').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"{name}_11b.png"))
            # 6.1 con un cuadro grande
            await pg.evaluate(OPEN_GRP, "El plan, con fechas"); await settle(pg)
            await pg.screenshot(path=str(OUT/f"{name}_c6.png"))
            await pg.evaluate(OPEN_AP, "6.1"); await settle(pg)
            await pg.evaluate("document.querySelector('.lec-cuadro').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"{name}_61.png"))
            # glosario
            await pg.evaluate(OPEN_GRP, "Glosario"); await settle(pg)
            await pg.screenshot(path=str(OUT/f"{name}_glos.png"))
            # zoom de un gráfico
            await pg.evaluate(OPEN_GRP, "Diagnóstico"); await settle(pg)
            await pg.evaluate(OPEN_AP, "1.1"); await settle(pg)
            await pg.evaluate("document.querySelector('.cimg').click()"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(OUT/f"{name}_zoom.png"))
            # overflow horizontal
            ov = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth, document.getElementById('lector').scrollWidth]")
            print(name, "errores:", errs[:5], "anchos:", ov)
            await ctx.close()
        await b.close()
asyncio.run(main())
