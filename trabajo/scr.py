import asyncio, sys
from playwright.async_api import async_playwright
URL=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={"width":390,"height":760}, device_scale_factor=2, is_mobile=True, has_touch=True); pg=await ctx.new_page()
        async def hang(route): await asyncio.sleep(30)
        await pg.route("**/api/ask", hang)
        await pg.goto(URL, wait_until="networkidle")
        await pg.tap("#q-main"); await pg.fill("#q-main","Tengo un café en Martínez, ¿qué me propone el programa?")
        await pg.tap("#form-main .go"); await pg.wait_for_timeout(1500)
        r=await pg.evaluate("""(()=>{const c=[...document.querySelectorAll('#thread .a')].pop(); const q=[...document.querySelectorAll('#thread .q')].pop(); return {scrollY:scrollY, cardTop:c.getBoundingClientRect().top, qTop:q.getBoundingClientRect().top, focused:document.activeElement.id||document.activeElement.tagName}})()""")
        print(r); await pg.screenshot(path=sys.argv[2]); await b.close()
asyncio.run(main())
