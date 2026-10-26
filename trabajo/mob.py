import asyncio
from playwright.async_api import async_playwright
A="https://sanisidro2027.pages.dev"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in (360,390):
            ctx=await b.new_context(viewport={"width":w,"height":800}, device_scale_factor=2, is_mobile=True, has_touch=True); pg=await ctx.new_page()
            await pg.goto(A+"/", wait_until="networkidle"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"mob/home_top_{w}.png")
            if w==390:
                await pg.screenshot(path="mob/home_full.png", full_page=True)
                h=await pg.evaluate("document.documentElement.scrollHeight"); print("alto",h)
                await pg.mouse.wheel(0,900); await pg.evaluate("window.scrollTo(0,1200)"); await pg.wait_for_timeout(500)
                await pg.screenshot(path="mob/home_scrolled.png")
            for path in ("cuentas/","despliegue/"):
                await pg.goto(A+"/"+path, wait_until="networkidle"); await pg.wait_for_timeout(500)
                await pg.screenshot(path=f"mob/{path.strip('/')}_top_{w}.png")
            await ctx.close()
        await b.close()
asyncio.run(main())
