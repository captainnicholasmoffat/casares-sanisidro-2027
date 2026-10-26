import asyncio
from playwright.async_api import async_playwright
A="https://anticipo.sanisidro2027.pages.dev"; S="/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/shots_com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for w in [390,1280]:
            ctx=await b.new_context(viewport={"width":w,"height":2000}); pg=await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(A+"/#ap-5.11", wait_until="networkidle"); await pg.wait_for_timeout(1200)
            meta=await pg.evaluate("[...document.querySelectorAll('.lec-hero-meta span')].map(s=>s.textContent).join(' | ')")
            txt=await pg.evaluate("document.getElementById('l-body').innerText")
            print(w,'5.11 meta:',meta,'| Su tope:', 'Su tope no cambia' in txt)
            await pg.goto(A+"/#ap-6.4", wait_until="networkidle"); await pg.wait_for_timeout(1200)
            txt=await pg.evaluate("document.getElementById('l-body').innerText")
            print(w,'6.4: diez', 'las diez ordenanzas' in txt, '| Ord 17 fila', 'Se presenta la Ordenanza 17' in txt)
            await pg.goto(A+"/despliegue/", wait_until="networkidle"); await pg.wait_for_timeout(2500)
            body=await pg.evaluate("document.body.innerText")
            print(w,'plan: C64', 'Ordenanza 17' in body, '| C61', 'Ordenanza 18' in body, '| largo', len(body))
            await pg.screenshot(path=f"{S}/desp_{w}.png")
            await ctx.close()
        print('errores', errs); await b.close()
asyncio.run(main())
