import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={"width":390,"height":760}, device_scale_factor=2, is_mobile=True, has_touch=True); pg=await ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file:///tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/mob/menu_test.html"); await pg.wait_for_timeout(1500)
        for o in "abc":
            await pg.click(f'.seg button[data-o="{o}"]'); await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"mob/o{o}_top.png")
            await pg.evaluate("window.scrollTo(0,1500)"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"mob/o{o}_scroll.png")
            print(o, "ancho", await pg.evaluate("document.documentElement.scrollWidth"))
            if o=="a":
                await pg.click("#open"); await pg.wait_for_timeout(300); await pg.screenshot(path="mob/oa_menu.png")
                await pg.click('.sheet a[data-k="2"]'); await pg.wait_for_timeout(900); await pg.screenshot(path="mob/oa_after.png")
        print("errores", errs); await b.close()
asyncio.run(main())
