"""Cambia en index_b.tpl.html la sección «El programa completo» por cuadros + lector con índice."""
from pathlib import Path

P = Path(__file__).resolve().parent / "index_b.tpl.html"
lines = P.read_text().split("\n")


def find(s, start=0):
    for i in range(start, len(lines)):
        if s in lines[i]:
            return i
    raise SystemExit("no encontrado: " + s)


CSS = r"""/* Programa completo: cuadros */
.prog{padding-block:64px 72px}
.prog-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:16px 32px;margin-bottom:24px}
.prog-head h2{font-family:var(--serif);font-size:clamp(2rem,3.6vw,3rem);line-height:1.05}
.prog-head p{color:var(--ink-2);font-size:17px;margin-top:8px;max-width:36em}
.search{display:flex;flex-direction:column;gap:6px;flex:0 1 440px;min-width:0}
.search label{font-size:14px;color:var(--ink-2)}
.search input{font:inherit;padding:13px 16px;border:1px solid var(--field-line);border-radius:8px;background:var(--card);color:var(--ink)}
.results{display:flex;flex-direction:column;gap:8px;margin-bottom:24px}
.res{display:block;width:100%;text-align:left;background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:12px 14px;color:var(--ink)}
.res b{font-family:var(--serif);font-weight:600;font-size:17px;display:block}
.res span{font-size:14px;color:var(--ink-2)}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.tile{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:18px 18px 14px;display:flex;flex-direction:column;gap:10px;text-align:left;color:var(--ink)}
.tile:hover{border-color:var(--link)}
.tile .tag{font-size:13px;font-weight:600;color:var(--sage)}
.tile.ch .tag{color:var(--link)}
.tile .tt{font-family:var(--serif);font-size:22px;line-height:1.2;font-weight:500}
.tile .ld{font-family:var(--serif);font-size:16px;line-height:1.45;color:var(--ink-2);flex-grow:1}
.tile .mt{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px;color:var(--ink-2);border-top:1px solid var(--rule-2);padding-top:10px}
.tile .mt b{color:var(--link);font-weight:600;font-size:14px}

/* Lector */
.lector{position:fixed;inset:0;z-index:20;background:var(--paper);overflow-y:auto;overscroll-behavior:contain}
.lec-bar{position:sticky;top:0;z-index:2;background:var(--ox);color:var(--ox-ink)}
.lec-bar-in{max-width:1240px;margin:0 auto;padding:10px var(--gutter);display:flex;align-items:center;justify-content:space-between;gap:12px}
.lec-btn{font-weight:600;font-size:15px;min-height:44px;padding:8px 14px;border-radius:999px;border:1px solid var(--ox-line);background:transparent;color:var(--ox-ink);display:inline-flex;align-items:center;gap:6px}
.lec-where{font-size:14px;color:var(--ox-soft);text-align:center;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lec-idx-btn{display:none}
.lec-lay{max-width:1240px;margin:0 auto;padding:32px var(--gutter) 64px;display:flex;gap:48px;align-items:flex-start}
.lec-side{flex:0 0 300px;display:flex;flex-direction:column;gap:2px;font-size:15px;position:sticky;top:84px;max-height:calc(100vh - 100px);overflow-y:auto;padding-right:6px}
.lec-side .lbl{font-size:13px;font-weight:600;color:var(--sage);padding-bottom:6px}
.lec-side .grp{display:flex;justify-content:space-between;gap:10px;width:100%;text-align:left;background:none;border:0;border-bottom:1px solid var(--rule);padding:10px 0;color:var(--ink);font-size:15px}
.lec-side .grp span{color:var(--ink-2);font-size:13px;flex-shrink:0}
.lec-side .grp.on{font-weight:600}
.lec-side ul{list-style:none;margin:6px 0 10px;padding:0;display:flex;flex-direction:column;gap:2px}
.lec-side ul button{display:block;width:100%;text-align:left;background:none;border:0;padding:7px 10px;border-radius:6px;color:var(--ink);font-size:14px;line-height:1.3}
.lec-side ul button:hover{background:var(--bubble)}
.lec-side ul button[aria-current="page"]{background:var(--ox);color:var(--ox-ink)}
.lec-main{flex:1 1 auto;min-width:0;max-width:740px;display:flex;flex-direction:column;gap:16px}
.lec-crumb{font-size:14px;color:var(--ink-2);display:flex;flex-wrap:wrap;gap:6px}
.lec-crumb button{background:none;border:0;padding:0;color:var(--link);font-size:14px;text-decoration:underline;text-underline-offset:3px}
.lec-main h1{font-family:var(--serif);font-weight:500;font-size:clamp(1.8rem,3vw,2.5rem);line-height:1.12;letter-spacing:-.01em}
.lec-meta{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--rule);padding-bottom:16px}
.lec-meta span{font-size:14px;color:var(--sage);font-weight:600}
.lec-ask{font-size:14px;font-weight:600;padding:9px 14px;min-height:44px;border-radius:999px;border:1px solid var(--link);background:transparent;color:var(--link)}
.lec-txt{font-family:var(--serif);font-size:19px;line-height:1.65;display:flex;flex-direction:column;gap:14px}
.lec-txt p{white-space:pre-line}
.lec-txt h3{font-family:var(--serif);font-weight:600;font-size:24px;line-height:1.2;margin-top:14px}
.lec-txt h4{font-family:var(--serif);font-weight:600;font-size:21px;line-height:1.25;margin:10px 0 0}
.lec-txt b{font-weight:600}
.lec-box{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--sage);border-radius:8px;padding:16px 18px;display:flex;flex-direction:column;gap:10px}
.lec-box > b{font-family:var(--serif);font-size:19px}
.lec-cuadro{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:14px 16px;font-family:var(--sans);font-size:14px;line-height:1.5;display:flex;flex-direction:column;gap:8px;overflow-x:auto}
.lec-cuadro b{font-size:15px}
.lec-cuadro p{white-space:pre-line}
.lec-fts{font-family:var(--sans);font-size:13px;color:var(--ink-2);white-space:pre-line;border-top:1px solid var(--rule-2);padding-top:10px}
.lec-pn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;border-top:1px solid var(--rule);padding-top:20px;margin-top:8px}
.lec-pn button{display:flex;flex-direction:column;gap:4px;padding:14px 16px;border:1px solid var(--rule);border-radius:10px;background:var(--card);color:var(--ink);text-align:left}
.lec-pn button.nx{text-align:right;grid-column:2}
.lec-pn small{font-size:13px;color:var(--ink-2)}
.lec-pn span{font-family:var(--serif);font-size:17px;line-height:1.3}
@media (max-width:980px){
  .lec-idx-btn{display:inline-flex}
  .lec-lay{display:block;padding-top:16px}
  .lec-side{position:static;max-height:none;overflow:visible;margin-bottom:20px;padding:0}
  .lec-side[data-closed]{display:none}
  .lec-pn{grid-template-columns:minmax(0,1fr)}
  .lec-pn button.nx{grid-column:auto;text-align:left;order:-1}
}
.foot{padding-block:28px 48px;font-size:14px;color:var(--ink-2);border-top:1px solid var(--rule)}
@media (max-width:1100px){.tiles{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:760px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){.tiles{grid-template-columns:minmax(0,1fr)}}
"""

HTML_TILES = '      <div class="tiles" id="tiles"><p style="color:var(--ink-2)">Cargando el programa…</p></div>'

HTML_LECTOR = r"""<div class="lector" id="lector" hidden role="dialog" aria-modal="true" aria-labelledby="l-title">
  <div class="lec-bar">
    <div class="lec-bar-in">
      <button class="lec-btn" type="button" id="l-home"><svg width="10" height="16" viewBox="0 0 10 16" aria-hidden="true"><path d="M8 2 2 8l6 6" stroke="currentColor" stroke-width="1.8" fill="none"></path></svg>Inicio</button>
      <span class="lec-where" id="l-where"></span>
      <button class="lec-btn lec-idx-btn" type="button" id="l-idx" aria-expanded="false" aria-controls="l-side">Índice</button>
    </div>
  </div>
  <div class="lec-lay">
    <nav class="lec-side" id="l-side" aria-label="Índice del programa" data-closed></nav>
    <article class="lec-main" tabindex="-1" id="l-main">
      <div class="lec-crumb" id="l-crumb"></div>
      <h1 id="l-title"></h1>
      <div class="lec-meta"><span id="l-hoja"></span><button class="lec-ask" type="button" id="l-ask">Preguntale sobre este apartado</button></div>
      <div class="lec-txt" id="l-body"></div>
      <nav class="lec-pn" id="l-pn" aria-label="Apartados vecinos"></nav>
    </article>
  </div>
</div>
"""

JS = r"""  /* ---------- Lector del programa ---------- */
  var PAGES = [], PAGE_OF = {}, GROUPS = [], CUR = null, lastFocus = null;
  var lector = $("#lector"), lside = $("#l-side");
  function hojas(a, b){ if (!a) return ""; if (!b || b === a) return "hoja " + a; return b === a + 1 ? "hojas " + a + " y " + b : "hojas " + a + " a " + b; }
  function isAp(id){ return /^\d+\.\d+$/.test(id); }
  function buildPages(d){
    var by = {}, order = [];
    d.forEach(function(e){ if (!by[e.capitulo]) { by[e.capitulo] = []; order.push(e.capitulo); } by[e.capitulo].push(e); });
    order.forEach(function(g){
      var list = by[g], parents = [], boxes = {}, last = null, chars = 0, ids = {};
      list.forEach(function(e){ chars += String(e.texto || "").length; if (!/-r\d+$/.test(e.id)) ids[e.id] = 1; });
      list.forEach(function(e){
        var m = e.id.match(/^(.*)-r\d+$/);
        if (m) { var pid = ids[m[1]] ? m[1] : last; if (pid) (boxes[pid] = boxes[pid] || []).push(e); }
        else { parents.push(e); last = e.id; }
      });
      var numbered = parents.some(function(e){ return isAp(e.id); });
      var grp = {name: g, pages: [], list: list};
      if (g === "Glosario" || (!numbered && chars < 6000)) grp.pages.push({group: grp, entries: parents, id: parents[0].id, title: g});
      else parents.forEach(function(e){ grp.pages.push({group: grp, entries: [e], id: e.id, title: isAp(e.id) ? e.id + " " + e.titulo : (/^\d+$/.test(e.id) ? e.capitulo : e.titulo)}); });
      grp.pages.forEach(function(pg){
        var a = Infinity, z = 0;
        pg.boxes = {};
        pg.entries.forEach(function(e){
          PAGE_OF[e.id] = pg; pg.boxes[e.id] = boxes[e.id] || [];
          pg.boxes[e.id].forEach(function(b){ PAGE_OF[b.id] = pg; z = Math.max(z, b.hoja_a4_fin || b.hoja_a4 || 0); });
          a = Math.min(a, e.hoja_a4 || Infinity); z = Math.max(z, e.hoja_a4_fin || e.hoja_a4 || 0);
        });
        pg.a = a === Infinity ? 0 : a; pg.z = z;
        PAGES.push(pg);
      });
      grp.a = grp.pages[0].a; grp.z = grp.pages[grp.pages.length - 1].z;
      GROUPS.push(grp);
    });
  }
  var RUNIN = /^((?:Qué|Por qué|Cómo|Cuánto|Cuánta|Cuántos|Cuántas|Dónde|Quién|Quiénes|Cuándo|Para qué|Lo que)[^.!?\n]{0,80}[.:])\s+([\s\S]+)$/;
  function renderText(box, text){
    String(text || "").split(/\n\n+/).forEach(function(p){
      p = p.trim(); if (!p) return;
      if (p.length < 110 && p.indexOf("\n") < 0 && !/[.:;!?»”)]$/.test(p)) { box.appendChild(el("h4", null, p)); return; }
      var m = p.match(RUNIN);
      if (m && m[1].split(/\s+/).length <= 10) { var q = el("p"); q.appendChild(el("b", null, m[1])); q.appendChild(document.createTextNode(" " + m[2])); box.appendChild(q); return; }
      box.appendChild(el("p", null, p));
    });
  }
  function renderSide(){
    lside.textContent = "";
    lside.appendChild(el("span", {"class":"lbl"}, "Índice"));
    GROUPS.forEach(function(g){
      var on = CUR && CUR.group === g;
      var b = el("button", {"class": "grp" + (on ? " on" : ""), type: "button"});
      b.appendChild(document.createTextNode(g.name)); b.appendChild(el("span", null, String(g.a || "")));
      b.addEventListener("click", function(){ show(g.pages[0]); });
      lside.appendChild(b);
      if (on && g.pages.length > 1) {
        var ul = el("ul");
        g.pages.forEach(function(pg){
          var li = el("li"), bt = el("button", {type: "button"}, pg.title);
          if (pg === CUR) bt.setAttribute("aria-current", "page");
          bt.addEventListener("click", function(){ show(pg); });
          li.appendChild(bt); ul.appendChild(li);
        });
        lside.appendChild(ul);
      }
    });
  }
  function openLector(){
    if (lector.hidden) { lastFocus = document.activeElement; lector.hidden = false; document.body.style.overflow = "hidden"; }
  }
  function show(pg, focusId){
    CUR = pg; openLector();
    var g = pg.group;
    $("#l-where").textContent = g.name;
    var cr = $("#l-crumb"); cr.textContent = "";
    var home = el("button", {type: "button"}, "El programa"); home.addEventListener("click", closeLector); cr.appendChild(home);
    if (pg !== g.pages[0]) { cr.appendChild(el("span", {"aria-hidden": "true"}, "›")); var gb = el("button", {type: "button"}, g.name); gb.addEventListener("click", function(){ show(g.pages[0]); }); cr.appendChild(gb); }
    $("#l-title").textContent = pg.title;
    $("#l-hoja").textContent = pg.a ? hojas(pg.a, pg.z).replace(/^h/, "H") + " de la versión A4" : "";
    $("#l-ask").hidden = false;
    var body = $("#l-body"); body.textContent = "";
    pg.entries.forEach(function(e){
      if (pg.entries.length > 1 && e.titulo !== pg.title) body.appendChild(el("h3", {id: "e-" + e.id}, (isAp(e.id) ? e.id + " " : "") + e.titulo));
      renderText(body, e.texto);
      (e.cuadros || []).forEach(function(c){
        var d = el("div", {"class": "lec-cuadro"}); d.appendChild(el("b", null, c.titulo || "Cuadro"));
        String(c.texto || "").split(/\n\n+/).forEach(function(t){ if (t.trim()) d.appendChild(el("p", null, t.trim())); });
        body.appendChild(d);
      });
      (pg.boxes[e.id] || []).forEach(function(bx){
        var d = el("div", {"class": "lec-box", id: "e-" + bx.id}); d.appendChild(el("b", null, bx.titulo));
        renderText(d, bx.texto); body.appendChild(d);
      });
      if (e.fuentes) body.appendChild(el("p", {"class": "lec-fts"}, "Fuentes: " + e.fuentes));
    });
    var pn = $("#l-pn"); pn.textContent = ""; pn.hidden = false;
    var i = PAGES.indexOf(pg);
    if (i > 0) { var pv = PAGES[i - 1], b1 = el("button", {type: "button"}); b1.appendChild(el("small", null, "Anterior")); b1.appendChild(el("span", null, pv.title)); b1.addEventListener("click", function(){ show(pv); }); pn.appendChild(b1); }
    if (i < PAGES.length - 1) { var nx = PAGES[i + 1], b2 = el("button", {"class": "nx", type: "button"}); b2.appendChild(el("small", null, "Siguiente")); b2.appendChild(el("span", null, nx.title)); b2.addEventListener("click", function(){ show(nx); }); pn.appendChild(b2); }
    lside.setAttribute("data-closed", ""); $("#l-idx").setAttribute("aria-expanded", "false");
    renderSide();
    var target = focusId && document.getElementById("e-" + focusId);
    if (target) target.scrollIntoView({block: "start"}); else lector.scrollTop = 0;
    $("#l-main").focus({preventScroll: true});
  }
  function openEntry(id){
    loadProg().then(function(){ var pg = PAGE_OF[id]; if (pg) show(pg, pg.id === id ? null : id); }).catch(function(){});
  }
  function openInv(x){
    CUR = null; openLector();
    $("#l-where").textContent = "Investigación";
    var cr = $("#l-crumb"); cr.textContent = "";
    var home = el("button", {type: "button"}, "Volver"); home.addEventListener("click", closeLector); cr.appendChild(home);
    $("#l-title").textContent = cleanInforme(x.informe);
    $("#l-hoja").textContent = "Investigación que respalda el programa";
    $("#l-ask").hidden = true;
    var body = $("#l-body"); body.textContent = "";
    if (x.seccion) body.appendChild(el("p", {"class": "lec-fts"}, x.seccion));
    renderText(body, x.texto);
    if (x.descartado && x.nota) { var d = el("div", {"class": "lec-box"}); d.appendChild(el("b", null, "El programa decidió distinto")); d.appendChild(el("p", null, x.nota)); body.appendChild(d); }
    $("#l-pn").hidden = true;
    renderSide();
    lector.scrollTop = 0; $("#l-main").focus({preventScroll: true});
  }
  function closeLector(){ lector.hidden = true; document.body.style.overflow = ""; if (lastFocus && lastFocus.focus) lastFocus.focus(); }
  $("#l-home").addEventListener("click", closeLector);
  $("#l-idx").addEventListener("click", function(){
    var closed = lside.hasAttribute("data-closed");
    if (closed) lside.removeAttribute("data-closed"); else lside.setAttribute("data-closed", "");
    this.setAttribute("aria-expanded", closed ? "true" : "false");
  });
  lector.addEventListener("keydown", function(ev){ if (ev.key === "Escape") closeLector(); });
  $("#l-ask").addEventListener("click", function(){
    if (!CUR) return;
    var t = CUR.title; closeLector();
    ask("Explicame " + (isAp(CUR.id) ? "el apartado " : "") + t + " del programa.");
  });
  document.addEventListener("click", function(ev){
    var t = ev.target.closest ? ev.target.closest("[data-open]") : null;
    if (t) openEntry(t.getAttribute("data-open"));
  });

  /* Cuadros del índice */
  loadProg().then(function(d){
    buildPages(d);
    var box = $("#tiles"); box.textContent = "";
    GROUPS.forEach(function(g){
      var m = g.name.match(/^(\d+) · (.*)$/), first = g.list[0];
      var tag, title = g.name, lead, left = "";
      if (m) { tag = "Capítulo " + m[1]; title = m[2]; left = g.pages.filter(function(p){ return isAp(p.id); }).length + " apartados · " + hojas(g.a, g.z); }
      else if (/^Anexo/.test(g.name)) { tag = "Anexo"; title = g.name.replace(/^Anexo · /, ""); left = g.list.filter(function(e){ return /^anexo-\d+$/.test(e.id); }).length + " ordenanzas · " + hojas(g.a, g.z); }
      else if (g.name === "Glosario") { tag = "Glosario"; left = g.list.filter(function(e){ return /^glosario-/.test(e.id); }).length + " palabras · " + hojas(g.a, g.z); }
      else { tag = hojas(g.a, g.z).replace(/^h/, "H"); left = g.name === "Qué proponemos hacer" ? "9 puntos" : (g.pages.length > 1 ? g.pages.length + " partes" : ""); }
      lead = g.name === "Qué proponemos hacer" ? "Nueve puntos, y los primeros cien días." : (String(first.texto || "").trim().match(/^[\s\S]*?[.!?](?=\s|$)/) || [String(first.texto || "").slice(0, 140)])[0];
      var t = el("button", {"class": "tile" + (m ? " ch" : ""), type: "button"});
      t.appendChild(el("span", {"class": "tag"}, tag));
      t.appendChild(el("span", {"class": "tt"}, title));
      t.appendChild(el("span", {"class": "ld"}, lead));
      var mt = el("span", {"class": "mt"}); mt.appendChild(el("span", null, left)); mt.appendChild(el("b", null, "Leer")); t.appendChild(mt);
      t.addEventListener("click", function(){ show(g.pages[0]); });
      box.appendChild(t);
    });
  }).catch(function(){ $("#tiles").textContent = "No se pudo cargar el programa. Recargá la página."; });

"""

# 1) CSS
a = find("/* Programa completo */"); b = find("@media (max-width:980px){.cards", a)
lines[a:b] = CSS.rstrip("\n").split("\n")
# 2) cuadros
i = find('<div class="chap" id="chapters">')
lines[i] = HTML_TILES
# subtítulo de la sección
i = find('<h2 id="t-prog">El programa completo</h2>')
lines[i] = '        <div><h2 id="t-prog">El programa completo</h2><p>Elegí una parte para leerla entera. Adentro podés pasar de un apartado al siguiente.</p></div>'
# 3) lector
a = find('<div class="reader" id="reader" hidden>'); b = find('<script type="application/json" id="nueve-data">', a)
lines[a:b] = HTML_LECTOR.split("\n")
# 4) JS
a = find("  /* ---------- Lector del programa ---------- */"); b = find("  var sTimer = null;", a)
lines[a:b] = JS.rstrip("\n").split("\n") + [""]
# 5) tarjetas: enlace al apartado
i = find('if (it.cap) full.appendChild(el("span", {"class":"cap"}, "Capítulo " + it.cap));')
lines[i] = ('    var go = LINK[it.n];\n'
            '    if (go) { var gb = el("button", {"class":"ask-it", type:"button", style:"align-self:flex-start;background:var(--ox);color:var(--ox-ink);border-color:var(--ox)"}, go[1]); '
            'gb.addEventListener("click", function(){ openEntry(go[0]); }); full.appendChild(gb); }')
i = find("  var IMGS = {1:")
lines.insert(i + 1, '  var LINK = {1:["4.3","Leer el apartado 4.3 en el programa"],2:["5.3","Leer el apartado 5.3 en el programa"],3:["5.3","Leer el apartado 5.3 en el programa"],4:["4.11","Leer el apartado 4.11 en el programa"],5:["4.11","Leer el apartado 4.11 en el programa"],6:["5.7","Leer el apartado 5.7 en el programa"],7:["5.9","Leer el apartado 5.9 en el programa"],8:["5.5-r12","Leer el apartado 5.5 en el programa"],9:["3","Leer el capítulo 3 en el programa"]};')

P.write_text("\n".join(lines))
print("ok")
