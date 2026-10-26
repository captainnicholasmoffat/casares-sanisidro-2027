import asyncio, sys
from playwright.async_api import async_playwright
URL = sys.argv[1]; Q = sys.argv[2]; OUT = sys.argv[3]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":390,"height":844})
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL, wait_until="networkidle")
        await pg.fill("#q-main", Q); await pg.click("#form-main .go")
        try:
            await pg.wait_for_selector("#thread .a .src, #thread .a .err", timeout=120000)
        except Exception as e:
            errs.append("timeout")
        await pg.wait_for_timeout(1500)
        a = await pg.evaluate("(()=>{const c=[...document.querySelectorAll('#thread .a')].pop(); return c? c.innerText : ''})()")
        print(a[:1500]); print("errores:", errs)
        await pg.evaluate("[...document.querySelectorAll('#thread .a')].pop().scrollIntoView({block:'start'})")
        await pg.screenshot(path=OUT)
        await b.close()
asyncio.run(main())
