import asyncio, sys, io
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
SVG = Path(sys.argv[1]); OUT = Path(sys.argv[2]); names = sys.argv[3:]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1500, "height": 1000}, device_scale_factor=1)
        for n in names:
            svg = (SVG / f"{n}.svg").read_text(encoding="utf-8")
            svg = svg[svg.index("<svg"):]
            html = ('<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">'
                    '<style>body{margin:0;background:#F5F0E8}#w{width:1440px;padding:0}#w svg{width:1440px;height:auto;display:block}</style></head><body><div id="w">' + svg + '</div></body></html>')
            await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
            png = await (await pg.query_selector("#w")).screenshot()
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(OUT / f"{n}.webp", "WEBP", quality=88, method=6)
            print(n, im.size, (OUT / f"{n}.webp").stat().st_size)
        await b.close()
asyncio.run(main())
