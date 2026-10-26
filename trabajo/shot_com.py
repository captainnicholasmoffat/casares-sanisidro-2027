import asyncio
from playwright.async_api import async_playwright
A="https://anticipo.sanisidro2027.pages.dev"
S="/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/shots_com"
JOBS=[("5.11","Además, proponemos cuatro medidas","Escuela de"),("3.6","puede traer juicios",None),("anexo","Tope para el comercio monotributista",None),("metodo-abogado","estudiar un abogado tributarista",None)]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for name,w in [("m",390),("d",1280)]:
            for sec,txt,_ in JOBS:
                ctx=await b.new_context(viewport={"width":w,"height":9000}); pg=await ctx.new_page()
                pg.on("pageerror", lambda e: errs.append(str(e)))
                await pg.goto(A+"/#ap-"+sec, wait_until="networkidle"); await pg.wait_for_timeout(1500)
                y=await pg.evaluate("""t=>{const w=document.createTreeWalker(document.getElementById('l-body'),NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.textContent.includes(t)){const r=n.parentElement.getBoundingClientRect();return r.top+window.scrollY}}return -1}""", txt)
                await pg.screenshot(path=f"{S}/{sec}_{name}.png", full_page=False)
                print(sec,name,y)
                await ctx.close()
        print("errores", errs); await b.close()
asyncio.run(main())
