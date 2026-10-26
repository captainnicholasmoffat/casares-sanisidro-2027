// GENERADO por web/build_site.py con el mismo código de búsqueda de la página (index_b.tpl.html). No editar a mano.
var CH_P = [], CH_I = [], DF_P = {}, DF_I = {}, AVG_P = 1, AVG_I = 1, READY = null;
  var STOP = {};
  ("a al algo algun alguna algunas alguno algunos ante antes aqui asi aun cada como con contra cual cuales cuando de del desde donde dos e el ella ellas ellos en entre era es esa esas ese eso esos esta estan estas este esto estos fue fueron ha hace han hasta hay la las le les lo los mas me mi mis muy ni no nos o otra otras otro otros para pero poco por porque que quien se sea segun ser si sin sobre son su sus tambien tan te tiene tienen todo todos tu tus un una unas uno unos y ya yo vos voy va van tengo tenes puede pueden programa proponen propone propuesta qué cómo the of and to in is for what how does do about my i").split(" ").forEach(function(w){ STOP[w] = 1; });
  var SYN = {plata:"dinero fondos", laburo:"trabajo empleo", chorro:"robo seguridad", chorros:"robo seguridad", afanaron:"robo seguridad", kiosco:"comercio", negocio:"comercio", local:"comercio habilitacion", cafe:"comercio", cafeteria:"comercio", bondi:"colectivo transporte", impuestos:"tasa", abl:"tasa", municipalidad:"municipio", policia:"seguridad camaras", cana:"seguridad", pibes:"jovenes", chicos:"ninez jovenes", jubilados:"personas mayores", ia:"inteligencia artificial", plaza:"plazas espacio publico", rio:"costa", clausuraron:"clausura inspeccion", inspector:"inspeccion"};
  function norm(s){ return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, " "); }
  function stem(w){ if (w.length > 5 && /es$/.test(w)) w = w.slice(0, -2); else if (w.length > 4 && /s$/.test(w)) w = w.slice(0, -1); return w.length > 7 ? w.slice(0, 7) : w; }
  function toks(s){
    var out = [];
    norm(s).split(" ").forEach(function(w){
      if (!w || STOP[w] || w.length < 3 && !/^\d+$/.test(w)) return;
      out.push(stem(w));
      if (SYN[w]) SYN[w].split(" ").forEach(function(x){ out.push(stem(x)); });
    });
    return out;
  }
  function indexChunks(list, df){
    var tot = 0;
    list.forEach(function(c){
      var tf = {}, t = toks(c.search);
      t.forEach(function(w){ tf[w] = (tf[w] || 0) + 1; });
      c.tf = tf; c.len = t.length || 1; tot += c.len;
      for (var w in tf) df[w] = (df[w] || 0) + 1;
    });
    return tot / (list.length || 1);
  }
  function bm25(list, df, avg, q, k){
    var N = list.length, qt = toks(q), seen = {}, terms = [];
    qt.forEach(function(w){ if (!seen[w]) { seen[w] = 1; terms.push(w); } });
    if (!terms.length) return [];
    var res = [];
    list.forEach(function(c){
      var s = 0;
      terms.forEach(function(w){
        var f = c.tf[w]; if (!f) return;
        var idf = Math.log(1 + (N - df[w] + .5) / (df[w] + .5));
        s += idf * (f * 2.2) / (f + 1.2 * (.25 + .75 * c.len / avg));
      });
      if (s > 0) res.push({c: c, s: s * (c.boost || 1)});
    });
    res.sort(function(a, b){ return b.s - a.s; });
    return res.slice(0, k || 10);
  }
  function hojaTxt(e){ return e.hoja_a4 ? (e.hoja_a4_fin && e.hoja_a4_fin !== e.hoja_a4 ? "hojas " + e.hoja_a4 + " a " + e.hoja_a4_fin : "hoja " + e.hoja_a4) : ""; }
  function cleanInforme(s){ return String(s || "").replace(/^Informe\s+[0-9]+[a-z ]*\s*·\s*/i, ""); }
  function buildContext(qSearch){
    var hp = bm25(CH_P, DF_P, AVG_P, qSearch, 14), hi = bm25(CH_I, DF_I, AVG_I, qSearch, 8);
    var parts = [], refs = {}, size = 0, LIM_P = 30000, LIM_I = 11000, used = 0;
    var out = "PROGRAMA (lo aprobado)\n";
    hp.forEach(function(h, i){
      var e = h.c.e, code = "P" + (i + 1), t = h.c.text.slice(0, 2600);
      var block = "[" + code + "] " + e.capitulo + " · " + (/^\d/.test(e.id) ? e.id + " " : "") + e.titulo + (hojaTxt(e) ? " (" + hojaTxt(e) + ")" : "") + "\n" + t + "\n\n";
      if (used + block.length > LIM_P) return;
      used += block.length; out += block; refs[code] = {kind:"p", e: e};
    });
    used = 0; out += "INVESTIGACIONES (sólo para explicar de dónde sale algo)\n";
    hi.forEach(function(h, i){
      var x = h.c.x, code = "I" + (i + 1);
      var block = "[" + code + "] " + cleanInforme(x.informe) + (x.seccion ? " · " + x.seccion : "") + (x.descartado ? " · DESCARTADO" + (x.nota ? ": " + x.nota : "") : (x.nota ? " · Nota: " + x.nota : "")) + "\n" + h.c.text + "\n\n";
      if (used + block.length > LIM_I) return;
      used += block.length; out += block; refs[code] = {kind:"i", x: x};
    });
    return {text: out, refs: refs};
  }

async function getJSON(env, origin, path) {
  const r = await env.ASSETS.fetch(new Request(origin + path));
  if (!r.ok) throw new Error(path);
  return r.json();
}
export function ready(env, origin) {
  if (!READY) READY = (async () => {
    const [prog, inv, cu, pl] = await Promise.all([getJSON(env, origin, "/data/programa.json"), getJSON(env, origin, "/data/investigaciones.json").catch(() => []), getJSON(env, origin, "/data/cuentas_ia.json").catch(() => []), getJSON(env, origin, "/data/plan_ia.json").catch(() => [])]);
    (cu || []).concat(pl || []).forEach(function(e){ var plan = /^plan-/.test(e.id); String(e.texto || "").split(/\n\n+/).forEach(function(t){ if (t.trim()) CH_P.push({e: e, text: t.trim(), search: e.titulo + " " + e.titulo + (plan ? " plan despliegue cuando fecha quien " : " cuentas modelo fiscal plata presupuesto ") + t, boost: plan ? .85 : 1}); }); });
    prog.forEach(function(e){
      var paras = String(e.texto || "").split(/\n\n+/), buf = "";
      function push(t){ if (t.trim()) CH_P.push({e: e, text: t.trim(), search: e.titulo + " " + e.titulo + " " + t, boost: /^glosario-/.test(e.id) ? .7 : 1}); }
      paras.forEach(function(p){ if ((buf + "\n\n" + p).length > 1500 && buf) { push(buf); buf = p; } else buf = buf ? buf + "\n\n" + p : p; });
      push(buf);
      (e.cuadros || []).forEach(function(c){ push((c.titulo || "Cuadro") + "\n" + String(c.texto || "").slice(0, 2200)); });
    });
    AVG_P = indexChunks(CH_P, DF_P);
    (inv || []).forEach(function(x){ CH_I.push({x: x, text: String(x.texto || "").slice(0, 1900), search: (x.seccion || "") + " " + (x.temas || []).join(" ") + " " + x.texto, boost: x.descartado ? .6 : 1}); });
    AVG_I = indexChunks(CH_I, DF_I);
    return true;
  })().catch((e) => { READY = null; CH_P = []; CH_I = []; DF_P = {}; DF_I = {}; throw e; });
  return READY;
}
export function context(search) {
  const c = buildContext(search), refs = {};
  for (const k in c.refs) { const r = c.refs[k]; refs[k] = r.kind === "p" ? "p:" + r.e.id : "i:" + r.x.id; }
  return { text: c.text, refs };
}
