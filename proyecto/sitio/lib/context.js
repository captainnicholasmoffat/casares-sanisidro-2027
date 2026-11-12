// GENERADO por web/build_site.py con el mismo código de búsqueda de la página (index_b.tpl.html). No editar a mano.
var CH_P = [], CH_I = [], DF_P = {}, DF_I = {}, AVG_P = 1, AVG_I = 1, READY = null;
  var STOP = {};
  ("a al algo algun alguna algunas alguno algunos ante antes aqui asi aun cada como con contra cual cuales cuando de del desde donde dos e el ella ellas ellos en entre era es esa esas ese eso esos esta estan estas este esto estos fue fueron ha hace han hasta hay la las le les lo los mas me mi mis muy ni no nos o otra otras otro otros para pero poco por porque que quien se sea segun ser si sin sobre son su sus tambien tan te tiene tienen todo todos tu tus un una unas uno unos y ya yo vos voy va van tengo tenes puede pueden programa proponen propone propuesta qué cómo the of and to in is for what how does do about my i").split(" ").forEach(function(w){ STOP[w] = 1; });
  var SYN = {plata:"dinero fondos", laburo:"trabajo empleo", chorro:"robo seguridad", chorros:"robo seguridad", afanaron:"robo seguridad", kiosco:"comercio", negocio:"comercio", local:"comercio habilitacion", cafe:"comercio", cafeteria:"comercio", bondi:"colectivo transporte", impuestos:"tasa", abl:"tasa", municipalidad:"municipio", policia:"seguridad camaras", cana:"seguridad", pibes:"jovenes", chicos:"ninez jovenes", jubilados:"personas mayores", ia:"inteligencia artificial", plaza:"plazas espacio publico", rio:"costa", clausuraron:"clausura inspeccion", inspector:"inspeccion", "robaron":"robo delito", "roban":"robo delito", "asaltaron":"robo delito", "asalto":"robo delito", "afanaron":"robo delito", "inseguridad":"seguridad delito"};
  // Frases que sólo se suman a la pregunta, no a los pasajes (por ejemplo «el bajo»: el barrio, no el adjetivo).
  var FRASES = {"el bajo":"costa ribera cuenca rio", "del bajo":"costa ribera cuenca rio", "al bajo":"costa ribera cuenca rio", "problemas ves":"riesgos riesgo salir mal reduce", "problemas le ves":"riesgos riesgo salir mal reduce", "problemas tiene el programa":"riesgos riesgo salir mal reduce", "problemas tiene este programa":"riesgos riesgo salir mal reduce", "problemas del programa":"riesgos riesgo salir mal reduce", "problemas de este programa":"riesgos riesgo salir mal reduce", "errores":"riesgos riesgo salir mal reduce", "error tiene":"riesgos riesgo salir mal reduce", "debilidades":"riesgos riesgo salir mal reduce", "debilidad":"riesgos riesgo salir mal reduce", "puntos debiles":"riesgos riesgo salir mal reduce", "punto debil":"riesgos riesgo salir mal reduce", "que le falta":"riesgos riesgo salir mal reduce", "le falta al programa":"riesgos riesgo salir mal reduce", "le falta a este programa":"riesgos riesgo salir mal reduce", "confiable":"riesgos riesgo salir mal reduce", "creible":"riesgos riesgo salir mal reduce", "criticaria":"riesgos riesgo salir mal reduce", "criticas":"riesgos riesgo salir mal reduce", "esceptico":"riesgos riesgo salir mal reduce", "contras":"riesgos riesgo salir mal reduce", "salir mal":"riesgos riesgo reduce", "puede fallar":"riesgos riesgo salir mal reduce"};
  function frases(q){ var n = " " + norm(q) + " ", extra = ""; for (var f in FRASES) if (n.indexOf(" " + f + " ") >= 0) extra += " " + FRASES[f]; return q + extra; }
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
    var N = list.length, qt = toks(frases(q)), seen = {}, terms = [];
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
  // Los cuadros largos se leen en partes, cada una con su título y su encabezado (antes se cortaban a los 2.200 caracteres).
  function cuadroPartes(c){
    var filas = String(c.texto || "").split("\n"), cab = filas.shift() || "", tit = c.titulo || "Cuadro", out = [], buf = "";
    filas.forEach(function(f){ if (buf && (buf + "\n" + f).length > 1500) { out.push(buf); buf = f; } else buf = buf ? buf + "\n" + f : f; });
    if (buf || !out.length) out.push(buf);
    return out.map(function(b){ return tit + "\n" + cab + (b ? "\n" + b : ""); });
  }
  // De las investigaciones, el chat no lee el trabajo interno: lo descartado, lo que el programa cambió después,
  // los borradores, lo que no se encontró, el método ni las correcciones. Las páginas de las investigaciones no cambian.
  var INV_SECCION_FUERA = /(no (lo |se )?(encontr|pudo)|sin verificar|no est[aá] verificado|d[oó]nde busqu|borrador|se descart|correcci[oó]n|notas cr[ií]ticas|verificaci[oó]n del cuadro|(^|› )m[eé]todo)/i;
  var FRASE_INTERNA = /(encargo|premisa|grepe|este informe|este borrador|informe \d+[a-z ]*(actualiz|corrigi|aclar|recalcul|encontr)|programa final|\bNick\b)/i;
  function invParaChat(x){
    if (x.descartado || (x.nota && !/coincide en lo central|se sostuvieron/i.test(x.nota)) || INV_SECCION_FUERA.test(x.seccion || "")) return null;
    var t = String(x.texto || "").split("\n").map(function(l){ return l.replace(/([.!?])\s+/g, "$1\u0001").split("\u0001").filter(function(o){ return !FRASE_INTERNA.test(o); }).join(" "); }).filter(function(l){ return l.trim(); }).join("\n");
    return t.trim() ? t : null;
  }
  function seccionChat(s){ return String(s || "").replace(/TAREA [A-Z]\s*[·:]\s*/g, "").replace(/\s*\((re)?verificaci[oó]n\)/gi, ""); }
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
      var block = "[" + code + "] " + cleanInforme(x.informe) + (x.seccion ? " · " + seccionChat(x.seccion) : "") + "\n" + h.c.text + "\n\n";
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
      (e.cuadros || []).forEach(function(c){ cuadroPartes(c).forEach(push); });
    });
    AVG_P = indexChunks(CH_P, DF_P);
    (inv || []).forEach(function(x){ var t = invParaChat(x); if (t) CH_I.push({x: x, text: t.slice(0, 1900), search: seccionChat(x.seccion) + " " + (x.temas || []).join(" ") + " " + t, boost: 1}); });
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
