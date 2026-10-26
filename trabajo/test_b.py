import sys, threading, http.server, socketserver, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright
WEB = Path('/home/claude/proyecto/web'); OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a, directory=str(WEB), **k)
    def log_message(self,*a): pass
srv = socketserver.TCPServer(('127.0.0.1',0),Q); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
page = (WEB/'index.html').read_text()
(WEB/'_t.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'+page+'</body></html>')
MOCK = """
window.__inputs = [];
window.claude = { use: function(n){ if(n!=='sample') return Promise.resolve(null);
  var f = function(input, opts){ window.__inputs.push(input);
    var txt = 'Las inspecciones de comercios van a quedar grabadas. Sin grabación sellada, no valen el acta, la clausura ni la habilitación.\\n\\n- El comerciante también va a poder grabar.\\n- El video queda guardado.\\n\\nFUENTES: P1, P2, I1\\nSEGUIR: ¿Cuándo empieza? | ¿Qué más propone para los comercios?';
    return new Promise(function(res){ setTimeout(function(){ opts && opts.onText && opts.onText({text: txt.slice(0,60), delta: txt.slice(0,60)}); setTimeout(function(){ res({text: txt, truncated:false, modelTierApplied:'default'}); }, 300); }, 300); }); };
  f.json = function(){ return Promise.resolve({es:'¿Qué propone para los comercios?'}); };
  return Promise.resolve(f); } };
"""
errs=[]
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [('desk',{'width':1440,'height':900}),('mob',{'width':390,'height':844})]:
        ctx = b.new_context(viewport=vp)
        ctx.add_init_script(MOCK)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
        pg.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(body='', content_type='text/css'))
        pg.goto(f'http://127.0.0.1:{port}/_t.html', wait_until='networkidle'); time.sleep(1)
        print(name, 'overflowX', pg.evaluate('document.documentElement.scrollWidth > window.innerWidth'))
        pg.screenshot(path=str(OUT/f'{name}_0.png'))
        pg.fill('#q-main','Tengo un café en Martínez y me clausuraron sin motivo')
        pg.click('#form-main .go'); time.sleep(2.5)
        pg.screenshot(path=str(OUT/f'{name}_1.png'))
        inp = pg.evaluate('window.__inputs[window.__inputs.length-1]')
        total = sum(len(t['content'].encode()) for t in inp) if isinstance(inp,list) else len(inp.encode())
        print(name, 'turns', len(inp) if isinstance(inp,list) else 'str', 'bytes', total)
        last = inp[-1]['content']
        print('  P blocks', last.count('\n[P'), 'I blocks', last.count('\n[I'))
        print('  first P lines:', [l[:90] for l in last.split('\n') if l.startswith('[P')][:6])
        pg.click('#thread .src-b'); time.sleep(0.8)
        pg.screenshot(path=str(OUT/f'{name}_2.png'))
        pg.click('#r-close'); time.sleep(0.3)
        # follow-up
        pg.click('#thread .chip-f'); time.sleep(2.5)
        inp2 = pg.evaluate('window.__inputs[window.__inputs.length-1]')
        print('  follow turns', len(inp2), [t['role'] for t in inp2])
        # card leer mas
        pg.evaluate("document.querySelector('#propuestas').scrollIntoView()"); time.sleep(0.5)
        pg.click('.card .lnk'); time.sleep(0.3)
        pg.screenshot(path=str(OUT/f'{name}_3.png'))
        pg.evaluate("document.querySelector('#programa').scrollIntoView()"); time.sleep(0.3)
        pg.fill('#buscar','cloacas'); time.sleep(0.8)
        pg.screenshot(path=str(OUT/f'{name}_4.png'))
        print('  results', pg.evaluate("document.querySelectorAll('#results .res').length"), pg.evaluate("[...document.querySelectorAll('#results .res b')].map(b=>b.textContent).slice(0,5)"))
        ctx.close()
    b.close()
print('errors', errs[:8])
(WEB/'_t.html').unlink()
