from playwright.sync_api import sync_playwright
SP = '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
FAKE = """
window.SpeechRecognition = function(){ var self = this; this.start = function(){ window.__rec = self; };
  this.stop = function(){ setTimeout(function(){ self.onend && self.onend(); }, 10); }; };
window.__say = function(t, fin){ var r = window.__rec; r.onresult({results: [[{transcript: t}]]}); if (fin) { r.onend(); } };
window.__err = function(e){ var r = window.__rec; r.onerror({error: e}); r.onend(); };
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1280, 400):
        pg = b.new_page(viewport={'width': w, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script(FAKE)
        pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
        m = '#form-main .mic'
        print(w, 'visible', pg.is_visible(m), '| fine:', pg.text_content('#fine-mic'))
        pg.fill('#q-main', 'Hola')
        pg.click(m); print(' estado', pg.get_attribute(m, 'aria-pressed'), pg.text_content(m + ' .mic-t'))
        pg.locator('.hero-in').screenshot(path=f'{SP}/mic_on_{w}.png') if w == 400 else None
        pg.evaluate('__say("tengo un café en Martínez", false)'); print(' parcial:', pg.input_value('#q-main'))
        pg.evaluate('__say("tengo un café en Martínez y me clausuraron", true)'); pg.wait_for_timeout(50)
        print(' final:', pg.input_value('#q-main'), '| estado', pg.get_attribute(m, 'aria-pressed'), '| msg:', pg.text_content('#form-main .mic-msg'))
        pg.click(m); pg.evaluate('__err("not-allowed")'); print(' error msg:', pg.text_content('#form-main .mic-msg'))
        boxes = pg.evaluate('''[...document.querySelectorAll("#form-main .ask > *")].map(e => { const r = e.getBoundingClientRect(); return [e.tagName, Math.round(r.left), Math.round(r.top), Math.round(r.width)] })''')
        print(' layout', boxes, 'pagina', pg.evaluate('document.documentElement.scrollWidth'))
        pg.locator('#form-main').screenshot(path=f'{SP}/mic_{w}.png')
        print(' errores', errs)
    # sin soporte
    pg = b.new_page(viewport={'width': 400, 'height': 900})
    pg.add_init_script('delete window.webkitSpeechRecognition; window.webkitSpeechRecognition = undefined;')
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(400)
    print('sin soporte: visible', pg.is_visible('#form-main .mic'), '| fine:', pg.text_content('#fine-mic'))
    b.close()
