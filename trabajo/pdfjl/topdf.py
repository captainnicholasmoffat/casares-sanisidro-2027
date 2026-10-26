import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto("file:///tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/pdfjl/visita.html")
        await pg.pdf(path="/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/pdfjl/Visita_panaderia_Jose_Luis.pdf", format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
