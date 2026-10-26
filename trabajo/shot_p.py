import asyncio, json
from playwright.async_api import async_playwright
A="https://anticipo.sanisidro2027.pages.dev"
datos={"email":"x","dias":30,"resumen":{"n":120,"sd":14,"ct":0,"fb":5,"personas":61},"sinDato":[],"comentarios":[],"todas":[],"fuentes":[],"retencion":{"mas5":0,"mas6":0,"total":120},
 "mensajes":[{"id":"1","ts":1791797201114,"pagina":"/cuentas/","texto":"Falta hablar de las inundaciones en Boulogne.","mail":"vecina@mail.com"},{"id":"2","ts":1791797101114,"pagina":"/","texto":"¿Qué pasa con el tren de la costa?","mail":None}],"retencionMensajes":{"mas5":0,"mas6":0}}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for name,vp in [("m",{"width":390,"height":844}),("d",{"width":1280,"height":900})]:
            ctx=await b.new_context(viewport=vp, device_scale_factor=2 if name=="m" else 1); pg=await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            html=open("/home/claude/proyecto/sitio/public/panel/index.html").read()
            await pg.route(A+"/panel/", lambda r: r.fulfill(status=200, content_type="text/html", body=html))
            await pg.route("**/api/panel/datos*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(datos)))
            await pg.goto(A+"/panel/", wait_until="networkidle"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"shots_f/panel_{name}.png", clip={"x":0,"y":0,"width":vp["width"],"height":1100 if name=="m" else 820})
            await ctx.close()
        print("errores", errs); await b.close()
asyncio.run(main())
