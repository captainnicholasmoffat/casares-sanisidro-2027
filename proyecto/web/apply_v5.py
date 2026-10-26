from pathlib import Path
W = Path(__file__).resolve().parent
t = (W / "index_b.tpl.html").read_text()
css = (W / "patch_v5_css.txt").read_text()
js = (W / "patch_v5_js.txt").read_text()
def rep(old, new, count=1):
    global t
    assert t.count(old) == count, (old[:80], t.count(old))
    t = t.replace(old, new)
# 1) tokens
rep("--bubble:#EFE6DA; --link:#7C2E23; --focus:#7C2E23; --shade:rgba(30,20,15,.55);",
    "--bubble:#EFE6DA; --link:#7C2E23; --focus:#7C2E23; --shade:rgba(30,20,15,.55);\n  --prop-bg:#F8EAE3; --ctx-bg:#EFE8DC; --amber:#8F6A24; --coral-txt:#B04E2E;")
rep("--bubble:#3A2F28; --link:#E8A08F; --focus:#E8A08F; --sage:#A3B597; --shade:rgba(0,0,0,.65); color-scheme:dark;",
    "--bubble:#3A2F28; --link:#E8A08F; --focus:#E8A08F; --sage:#A3B597; --shade:rgba(0,0,0,.65); --prop-bg:#3A2520; --ctx-bg:#2E2621; --amber:#D9B169; --coral-txt:#F0A184; color-scheme:dark;", 2)
rep("p{margin:0}", "p{margin:0}\n[hidden]{display:none!important}")
# 2) CSS: bloque de programa + lector + pie
a = t.index("/* Programa completo: cuadros */"); b = t.index("@media (max-width:980px){.cards{")
t = t[:a] + css + t[b:]
# 3) Portada: foto en la pregunta
rep('.hero-in{display:flex;flex-direction:column;gap:20px;max-width:1000px}',
    '.hero-grid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr);gap:56px;align-items:center}\n.hero-in{display:flex;flex-direction:column;gap:20px;min-width:0}\n.hero-fig{margin:0;display:flex;flex-direction:column;gap:8px}\n.hero-fig img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:20px;display:block;box-shadow:0 24px 60px rgba(0,0,0,.28)}\n.hero-fig figcaption{color:var(--ox-soft);font-size:13px}\n@media (max-width:900px){.hero-grid{grid-template-columns:minmax(0,1fr)}.hero-fig{display:none}}')
rep('    <div class="wrap hero-in">\n      <h1 id="t-hero">', '    <div class="wrap hero-grid">\n    <div class="hero-in">\n      <h1 id="t-hero">')
rep('      <p class="note" id="avail-note" hidden></p>\n    </div>\n  </section>',
    '      <p class="note" id="avail-note" hidden></p>\n    </div>\n    <figure class="hero-fig"><img src="img/f_costanera-800.webp" alt="La costanera de San Isidro." width="800" height="1072"><figcaption>La costanera de San Isidro. Ilustración.</figcaption></figure>\n    </div>\n  </section>')
# 4) Tarjetas: misma altura cerradas
rep('.lead{font-family:var(--serif);font-size:19px;line-height:1.3}',
    '.lead{font-family:var(--serif);font-size:19px;line-height:1.3}\n@media (min-width:981px){.card .lead{min-height:5.2em}}\n.card{transition:box-shadow .2s}\n.card:hover{box-shadow:0 10px 30px rgba(42,33,28,.10)}')
# 5) Programa completo: capítulos con foto + partes
rep('      <div class="results" id="results" aria-live="polite"></div>\n      <div class="tiles" id="tiles"><p style="color:var(--ink-2)">Cargando el programa…</p></div>',
    '      <div class="results" id="results" aria-live="polite"></div>\n      <div class="tiles" id="tiles-a"></div>\n      <h3 class="more-h">Los seis capítulos</h3>\n      <div class="chs" id="chs"><p style="color:var(--ink-2)">Cargando el programa…</p></div>\n      <h3 class="more-h">Al final del programa</h3>\n      <div class="tiles" id="tiles-b"></div>')
# 6) Pie
rep('<footer class="wrap foot">\n  <p>Programa de gobierno San Isidro 2027. Las imágenes son ilustraciones del programa.</p>\n</footer>',
    '<footer class="foot">\n  <div class="wrap foot-in">\n    <a class="brand" href="#inicio"><b>San Isidro 2027</b><span>Programa de gobierno</span></a>\n    <nav aria-label="Secciones"><a href="#inicio">Preguntale al programa</a><a href="#propuestas">Qué proponemos</a><a href="#programa">El programa completo</a></nav>\n    <p>Las imágenes son ilustraciones del programa. Los gráficos y los cuadros son los de la versión A4.</p>\n  </div>\n</footer>')
# 7) Lector: nueva estructura
a = t.index('<div class="lector" id="lector"'); b = t.index('<script type="application/json" id="nueve-data">')
t = t[:a] + '''<div class="lector" id="lector" hidden role="dialog" aria-modal="true" aria-labelledby="l-title">
  <div class="lec-bar">
    <div class="lec-bar-in">
      <button class="lec-btn" type="button" id="l-home"><svg width="10" height="16" viewBox="0 0 10 16" aria-hidden="true"><path d="M8 2 2 8l6 6" stroke="currentColor" stroke-width="1.8" fill="none"></path></svg>Inicio</button>
      <span class="lec-where" id="l-where"></span>
      <button class="lec-btn lec-idx-btn" type="button" id="l-idx" aria-expanded="false" aria-controls="l-side">Índice</button>
    </div>
  </div>
  <header class="lec-hero" id="l-hero"></header>
  <div class="lec-lay" id="l-lay">
    <nav class="lec-side" id="l-side" aria-label="Índice del programa" data-closed></nav>
    <article class="lec-main" tabindex="-1" id="l-main">
      <details class="lec-toc-in" id="l-tocin" hidden></details>
      <div class="lec-txt" id="l-body"></div>
      <nav class="lec-pn" id="l-pn" aria-label="Apartados vecinos"></nav>
    </article>
    <aside class="lec-toc" id="l-toc" aria-label="En esta página" hidden></aside>
  </div>
</div>

''' + t[b:]
# 8) JS del lector y de los cuadros de la portada
a = t.index("  /* ---------- Lector del programa ---------- */"); b = t.index("  var sTimer = null;")
t = t[:a] + js + t[b:]
assert "renderText(" not in t, "queda renderText"
assert '$("#l-ask")' not in t, "queda l-ask"
(W / "index_b.tpl.html").write_text(t)
print("ok", len(t))
