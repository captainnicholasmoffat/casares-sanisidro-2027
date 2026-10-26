import asyncio
from playwright.async_api import async_playwright
AN="https://anticipo.sanisidro2027.pages.dev"; MA="https://sanisidro2027.pages.dev"
async def full(pg,url,path):
    await pg.goto(url, wait_until="networkidle")
    for y in range(0,11000,500):
        await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(60)
    await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(1200)
    await pg.screenshot(path=path, full_page=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={"width":390,"height":800}, device_scale_factor=1, is_mobile=True, has_touch=True); pg=await ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for pth in ["","cuentas/","despliegue/"]:
            n=pth.strip("/") or "home"
            await full(pg, AN+"/"+pth, f"mm/an_{n}.png"); await full(pg, MA+"/"+pth, f"mm/ma_{n}.png")
        ctx2=await b.new_context(viewport={"width":390,"height":800}, device_scale_factor=2, is_mobile=True, has_touch=True); q=await ctx2.new_page()
        q.on("pageerror", lambda e: errs.append(str(e)))
        for pth in ["","cuentas/","despliegue/"]:
            n=pth.strip("/") or "home"
            await q.goto(AN+"/"+pth, wait_until="networkidle"); await q.wait_for_timeout(600)
            await q.screenshot(path=f"mm/top_{n}.png")
            await q.evaluate("window.scrollTo(0,2400)"); await q.wait_for_timeout(500)
            await q.screenshot(path=f"mm/scroll_{n}.png")
            await q.click("#mm-open"); await q.wait_for_timeout(300); await q.screenshot(path=f"mm/menu_{n}.png")
            await q.click("#mm-close"); await q.wait_for_timeout(200)
        # tocar un destino desde el menú en la portada
        await q.goto(AN+"/", wait_until="networkidle"); await q.click("#mm-open"); await q.click('.mm-list a[href="/#programa"]'); await q.wait_for_timeout(1200)
        await q.screenshot(path="mm/goto_programa.png")
        print("overflow tras navegar:", await q.evaluate("document.documentElement.style.overflow"), "| ancho:", await q.evaluate("document.documentElement.scrollWidth"))
        # computadora
        ctx3=await b.new_context(viewport={"width":1280,"height":800}); d=await ctx3.new_page()
        for u,n in [(AN,"an"),(MA,"ma")]:
            await d.goto(u+"/", wait_until="networkidle"); await d.wait_for_timeout(500); await d.screenshot(path=f"mm/desk_{n}.png")
        print("errores", errs); await b.close()
asyncio.run(main())
