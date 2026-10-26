import asyncio, json
from playwright.async_api import async_playwright
A="https://anticipo.sanisidro2027.pages.dev"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for name,vp in [("m",{"width":390,"height":844}),("d",{"width":1280,"height":900})]:
            ctx=await b.new_context(viewport=vp, device_scale_factor=2 if name=="m" else 1); pg=await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(A+"/contacto/", wait_until="networkidle")
            await pg.screenshot(path=f"shots_f/contacto_{name}.png", full_page=True)
            sw=await pg.evaluate("document.documentElement.scrollWidth"); print(name,"scrollWidth",sw)
            await pg.goto(A+"/", wait_until="networkidle")
            await pg.evaluate("document.querySelector('footer.foot').scrollIntoView()"); await pg.wait_for_timeout(400)
            await pg.locator("footer.foot").screenshot(path=f"shots_f/home_foot_{name}.png")
            await pg.locator("p.fine").first.screenshot(path=f"shots_f/home_fine_{name}.png")
            await ctx.close()
        # envío del formulario (respuesta simulada, no guarda nada)
        ctx=await b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2); pg=await ctx.new_page()
        await pg.route("**/api/contacto", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true}'))
        await pg.goto(A+"/contacto/", wait_until="networkidle")
        await pg.fill("#texto","En mi cuadra de Boulogne se inunda cada vez que llueve."); await pg.fill("#mail","vecina@mail.com")
        await pg.click("#go"); await pg.wait_for_selector("#ok:not([hidden])")
        await pg.screenshot(path="shots_f/contacto_ok.png")
        # panel con datos simulados
        datos={"email":"x","dias":30,"resumen":{"n":120,"sd":14,"ct":0,"fb":5,"personas":61},"sinDato":[],"comentarios":[],"todas":[],"fuentes":[],"retencion":{"mas5":0,"mas6":0,"total":120},
               "mensajes":[{"id":"1","ts":1791797201114,"pagina":"/cuentas/","texto":"Falta hablar de las inundaciones en Boulogne.","mail":"vecina@mail.com"},{"id":"2","ts":1791797101114,"pagina":"/","texto":"¿Qué pasa con el tren de la costa?","mail":None}],"retencionMensajes":{"mas5":0,"mas6":0}}
        await pg.route("**/api/panel/datos*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(datos)))
        await pg.goto("file:///home/claude/proyecto/sitio/public/panel/index.html")
        await pg.route("**/*", lambda r: r.continue_())
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path="shots_f/panel_m.png", full_page=True)
        print("errores", errs); await b.close()
asyncio.run(main())
