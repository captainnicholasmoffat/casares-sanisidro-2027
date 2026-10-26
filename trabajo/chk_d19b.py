import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={"width":1280,"height":1200}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("https://anticipo.sanisidro2027.pages.dev/despliegue/", wait_until="networkidle"); await pg.wait_for_timeout(2000)
        await pg.click("#open-all"); await pg.wait_for_timeout(1500)
        body=await pg.evaluate("document.body.innerText")
        for k in ['Entra la Ordenanza 17','Asamblea de Concejales y Mayores Contribuyentes por la Ordenanza 17','El Concejo aprueba la Ordenanza 18','Revisión legal de las once ordenanzas','302 acciones','Mostrando las 302']:
            print(k in body, k)
        print('errores',errs); await b.close()
asyncio.run(main())
