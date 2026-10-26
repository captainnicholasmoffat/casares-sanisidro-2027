import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1440,"height":900})
        await pg.goto("https://anticipo.sanisidro2027.pages.dev/", wait_until="networkidle"); await pg.evaluate("document.fonts.ready")
        await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.querySelectorAll('.ch-card')[3].scrollIntoView({block:'start'})"); await pg.wait_for_timeout(800)
        await pg.screenshot(path="/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/c6_card.png")
        await pg.evaluate("document.querySelectorAll('.ch-card')[5].click()"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path="/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/c6_hero.png")
        await b.close()
asyncio.run(main())
