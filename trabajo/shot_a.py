import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for n, vp in [("d", {"width":1440,"height":900}), ("m", {"width":390,"height":844})]:
            pg = await b.new_page(viewport=vp)
            await pg.goto("https://anticipo.sanisidro2027.pages.dev/", wait_until="networkidle"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(800)
            if n == "m": await pg.evaluate("window.scrollTo(0, 330)"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/propart/A2_{n}.png")
        await b.close()
asyncio.run(main())
