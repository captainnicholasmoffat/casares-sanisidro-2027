import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":800})
        await pg.goto("https://anticipo.sanisidro2027.pages.dev/#ap-5.5", wait_until="networkidle"); await pg.wait_for_timeout(1500)
        print("lector abierto:", await pg.evaluate("!document.getElementById('lector').hidden"), "|", await pg.evaluate("document.getElementById('l-title') && document.getElementById('l-title').textContent"))
        await pg.goto("https://anticipo.sanisidro2027.pages.dev/despliegue", wait_until="networkidle"); await pg.wait_for_timeout(1500)
        print("plan:", pg.url, "|", await pg.evaluate("document.getElementById('count').textContent"))
        pg2 = await b.new_page(); pg = pg2; await pg.goto("https://anticipo.sanisidro2027.pages.dev/despliegue/#a-M22", wait_until="networkidle"); await pg.wait_for_timeout(1500)
        print("ficha:", await pg.evaluate("document.getElementById('sh-title') && document.getElementById('sh-title').textContent"), "| link:", await pg.evaluate("(document.querySelector('.src-link')||{}).href"))
        await b.close()
asyncio.run(main())
