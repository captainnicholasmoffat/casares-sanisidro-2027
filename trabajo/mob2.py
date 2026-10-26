import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={"width":390,"height":800}, device_scale_factor=1, is_mobile=True, has_touch=True); pg=await ctx.new_page()
        await pg.goto("https://sanisidro2027.pages.dev/", wait_until="networkidle")
        for y in range(0,10000,400):
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120)
        await pg.wait_for_timeout(1500)
        r=await pg.evaluate("""[...document.querySelectorAll('img')].map(i=>[i.currentSrc.split('/').pop(), i.complete && i.naturalWidth>0, i.loading]).filter(x=>!x[1])""")
        print("sin cargar:", r)
        r2=await pg.evaluate("""[...document.querySelectorAll('#capitulos *, .chap, [class*=cap]')].length""")
        await pg.screenshot(path="mob/full_after.png", full_page=True)
        await b.close()
asyncio.run(main())
