import asyncio, sys
from playwright.async_api import async_playwright
A=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={"width":390,"height":3000}); pg.on("pageerror", lambda e: errs.append(str(e)))
        for sec,img in [("1.1","g_mapa_zonas"),("4.4","g_mapa_radios")]:
            await pg.goto(A+"/#ap-"+sec, wait_until="networkidle"); await pg.wait_for_timeout(1500)
            r=await pg.evaluate("n=>{const i=[...document.querySelectorAll('img')].find(x=>x.src.includes(n)); if(!i) return 'sin img'; i.scrollIntoView(); return i.complete+' '+i.naturalWidth}", img)
            print(sec,img,r)
        print('errores',errs); await b.close()
asyncio.run(main())
