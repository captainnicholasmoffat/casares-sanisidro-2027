#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version A4 (dispatch 10, 08/10): el mismo diseño de la version de pantalla, todo al 90% (660 -> 595,28 pt de
ancho), pero el contenido corre seguido de hoja en hoja. Solo empiezan hoja nueva la tapa, el indice y cada capitulo.

Cada capitulo se dibuja entero, con el mismo HTML y el mismo CSS de build.py, como una sola tira (sin los cortes de
pagina de la version de pantalla), y se reparte en hojas A4 cortando solo entre bloques:
- un titulo nunca queda separado de lo que sigue, ni un cuadro o grafico de su rotulo y de su fuente;
- los graficos, los recuadros y las fotos nunca se parten (si un recuadro no entra en una hoja entera, se parte
  entre sus puntos y se avisa); los cuadros largos se parten entre filas repitiendo el encabezado, y las listas
  largas entre sus puntos;
- cada capitulo arranca arriba de todo de una hoja, con su titulo (y su foto de apertura pegada, arriba).

Ninguna hoja puede quedar con mas de un tercio en blanco, salvo la ultima del documento (regla de Nick). Para
llenar un hueco, en este orden: subir el bloque siguiente si entra entero; mostrar mas alta una foto de esa
seccion (menos recortada, nunca deformada); subir una foto de esa seccion. La foto de apertura de un capitulo puede
ir al final del capitulo anterior, si ahi sobra lugar. Cuando un capitulo sin fotos termina con una hoja casi
vacia, el corte se reparte entre sus ultimas hojas para que ninguna pase del tercio. Nunca se cambia el tamaño de
la letra ni se estira el texto. Ninguna foto corta una cara ni su motivo principal (a4_caras.json y MOTIVOS).

Cada hoja lleva el encabezado y el pie de pantalla; el pie dice el numero de hoja de la A4. El indice es el mismo,
con los numeros de hoja de la A4. Cada hoja guarda solo el texto que se ve en ella (dispatch 9).

Uso:  python3 doc/corte_a4.py                    (la A4 entera, a salida/PROGRAMA_SAN_ISIDRO_2027_A4.pdf)
      python3 doc/corte_a4.py --muestras N N ...  (esas hojas, a salida/muestras_a4/, sin tocar la A4)
Lee salida/PROGRAMA_SAN_ISIDRO_2027.pdf (solo la tapa) y content.py; correr antes build.py."""
import collections, html as H, json, os, pathlib, re, sys, unicodedata
import pymupdf as fitz
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build as B          # solo se lee: el HTML, el CSS y el script de columnas de la version de pantalla
import content             # solo se lee: las secciones
import content_a as CA

ROOT = HERE.parent
PANTALLA = ROOT / "salida" / "PROGRAMA_SAN_ISIDRO_2027.pdf"
SALIDA = ROOT / "salida" / "PROGRAMA_SAN_ISIDRO_2027_A4.pdf"
A4_W, A4_H = 595.2756, 841.8898
ESC = A4_W / B.PAGE_W_PT                  # 0,9019: todo se achica igual
HOJA = A4_H / ESC                         # alto de una hoja A4, en pt de la pagina de pantalla (933,4)
# los margenes de la pagina de pantalla (design.css): encabezado arriba, pie abajo
ARRIBA_CONT = 40.5 + 6.75 + 16.5          # en una hoja que sigue: el encabezado y el aire de un titulo h2
ABAJO = 28.1 + 7 + 0.75 + 6.4 + 30        # aire antes del pie, el pie y el margen de abajo
LIM = HOJA - ABAJO                        # hasta donde puede llegar el contenido de una hoja
AREA0 = 40.5 + 6.75                       # donde termina el encabezado
AREA1 = LIM + 28.1                        # la raya del pie
TERCIO = 1 / 3                            # el blanco maximo al pie de una hoja, sobre el alto entre encabezado y pie
TOPE = 0.32                               # al cortar se apunta un poco por debajo, por lo que el dibujo agrega al medir
FONDO = None                              # el beige de la pagina de pantalla, tal como lo dibujo Chrome (--ground)
GRIS = (0x6E / 255, 0x62 / 255, 0x5A / 255)       # --taupe, el color del pie
INTER = HERE / "_fonts" / "Inter-Regular.ttf"
FOTO_W, DUO_W = 570.0, (570.0 - 12.0) / 2          # ancho de una foto y de cada una de un par (design.css)

JS_MEDIR = r"""() => {
  const pg = document.getElementById('pg');
  const r0 = pg.getBoundingClientRect();
  const pt = v => v * 0.75;
  const caja = e => { const r = e.getBoundingClientRect(); return [pt(r.top - r0.top), pt(r.bottom - r0.top)]; };
  const out = {alto: pt(r0.height), bloques: [], titulos: []};
  for (const e of pg.children) {
    const [top, bottom] = caja(e);
    const st = getComputedStyle(e);
    const b = {tag: e.tagName.toLowerCase(), cls: e.className || '', top, bottom,
               mt: pt(parseFloat(st.marginTop) || 0), mb: pt(parseFloat(st.marginBottom) || 0),
               txt: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
               tabla: e.tagName === 'TABLE' || !!e.querySelector('table'),
               dibujo: !!e.querySelector('svg, img') || ['FIGURE', 'IMG', 'SVG'].includes(e.tagName),
               sec: e.dataset.sec || null, foto: e.dataset.foto || null, i: e.dataset.i != null ? +e.dataset.i : null};
    if (b.foto) { const [a, z] = caja(e.querySelector('img')); b.img_h = z - a; }
    // una lista larga se parte entre sus puntos; un cuadro, entre sus filas; un recuadro, entre sus parrafos
    if (e.tagName === 'OL' || e.tagName === 'UL') b.items = [...e.children].map(caja);
    const t = e.tagName === 'TABLE' ? e : e.querySelector('table');
    if (t) b.filas = [...t.rows].map(r => { const [a, z] = caja(r);
      return {top: a, bottom: z, th: !!r.querySelector('th'), sub: r.classList.contains('hd') && !r.querySelector('th')}; });
    if (/^callout/.test(b.cls)) b.hijos = [...e.children].map(caja);
    out.bloques.push(b);
  }
  for (const h of pg.querySelectorAll('h1, h2, h3')) {
    const [top] = caja(h);
    out.titulos.push([h.textContent.trim().replace(/\s+/g, ' '), top]);
  }
  return out;
}"""

# el reparto de las fotos: el alto y el encuadre de cada una, y las que se suben a otro lugar
JS_CONFIG = r"""(cfg) => {
  const pg = document.getElementById('pg');
  [...pg.children].forEach((e, i) => { e.dataset.i = i; });
  for (const [f, c] of Object.entries(cfg.fotos)) {
    const el = pg.querySelector(`[data-foto="${f}"]`);
    if (!el) continue;
    const imgs = el.tagName === 'FIGURE' ? [el.querySelector('img')] : [...el.querySelectorAll('img')];
    imgs.forEach((img, k) => {
      img.style.height = c.h + 'pt';
      const p = Array.isArray(c.pos) ? c.pos[k] : c.pos;
      img.style.objectPosition = `center ${p}%`;
    });
  }
  for (const mv of cfg.mover) {
    const el = pg.querySelector(`[data-foto="${mv.foto}"]`);
    const ref = pg.querySelector(`:scope > [data-i="${mv.antes}"]`);
    if (el && ref) pg.insertBefore(el, ref);
  }
  return pg.children.length;
}"""


# ---------------------------------------------------------------------------------------------- las fotos
# Lo que no se puede cortar en cada foto, ademas de las caras (a4_caras.json). En el alto de la foto, 0 es arriba y
# 1 abajo. "debe": tiene que verse entero; "sin_cortar": entero o nada (ningun borde lo atraviesa); "mejor": entero,
# si el alto alcanza. Las caras se protegen como "sin_cortar", con el pelo y el menton.
MOTIVOS = {
    "f_catedral":    {"debe": (0.055, 0.77)},                                   # la Catedral entera, con la aguja
    "f_barrera":     {"debe": (0.37, 0.86), "sin_cortar": [(0.02, 0.36)], "mejor": (0.02, 0.86)},  # y la almeja
    "f_patrullero":  {"debe": (0.53, 0.69), "sin_cortar": [(0.12, 0.20)], "mejor": (0.12, 0.69)},  # y la camara
    "f_escalera":    {"debe": (0.50, 0.80)},
    "f_banda":       {"debe": (0.24, 0.53)},
    "f_show_costa":  {"debe": (0.38, 0.58)},
    "f_mesa":        {"debe": (0.33, 0.72)},                                    # las cabezas y el mapa
    "f_boulogne":    {"debe": (0.52, 0.80)},                                    # la cuadrilla en la zanja
    "f_apoyo":       {"debe": (0.21, 0.62)},                                    # las caras de la mesa
    "f_profesor":    {"debe": (0.45, 0.70)},                                    # el alumno con el profesor digital en la pantalla
    "f_show_club":   {"debe": (0.15, 0.40)},                                    # el escenario
}
_CARAS = json.loads((HERE / "a4_caras.json").read_text(encoding="utf-8"))


def _limites(nombre):
    d = MOTIVOS.get(nombre, {})
    sin_cortar = list(d.get("sin_cortar", []))
    for a, b, conf in _CARAS.get(nombre, {}).get("caras", []):
        alto = b - a
        if conf >= 0.6 and 0.02 <= alto <= 0.25:            # las caras chicas del fondo no; las falsas grandes tampoco
            sin_cortar.append((max(0.0, a - 0.2 * alto), min(1.0, b + 0.1 * alto)))
    return d.get("debe"), sin_cortar, d.get("mejor")


def _franjas(nombre, v):
    """Los comienzos posibles (desde arriba, en fraccion del alto) de una ventana de alto v que no corta nada."""
    if v >= 0.9999:
        return [(0.0, 0.0)]
    debe, sin_cortar, _ = _limites(nombre)
    lo, hi = 0.0, 1.0 - v
    if debe:
        lo, hi = max(lo, debe[1] - v), min(hi, debe[0])
    if lo > hi + 1e-9:
        return []
    ivs = [(lo, hi)]
    for a, b in sin_cortar:
        for x0, x1 in ((a, b), (a - v, b - v)):                  # el borde de arriba y el de abajo
            nuevo = []
            for p, q in ivs:
                if x1 <= p or x0 >= q:
                    nuevo.append((p, q))
                    continue
                if p <= x0:
                    nuevo.append((p, x0))
                if x1 <= q:
                    nuevo.append((x1, q))
            ivs = nuevo
    return ivs


class Foto:
    def __init__(self, nombre, duo=False, h0=None, pos0=52.0):
        self.nombre, self.duo = nombre, duo
        ancho_px, alto_px = _CARAS[nombre]["ancho"], _CARAS[nombre]["alto"]
        self.h_nat = (DUO_W if duo else FOTO_W) * alto_px / ancho_px
        self.h0 = h0 if h0 is not None else (196.0 if duo else 232.0)
        self.pos0 = pos0

    def posible(self, h):
        return bool(_franjas(self.nombre, h / self.h_nat))

    def pos(self, h):
        """El encuadre (object-position, en %) para el alto h: el de pantalla, o el mas cercano que no corta nada."""
        v = h / self.h_nat
        if v >= 0.9999:
            return 50.0
        ivs = _franjas(self.nombre, v)
        if not ivs:
            raise ValueError(f"{self.nombre}: con {h:.0f} pt no hay encuadre que no corte una cara o el motivo")
        t0 = (1 - v) * self.pos0 / 100
        mejor = _limites(self.nombre)[2]
        if mejor:
            m = [(max(p, mejor[1] - v), min(q, mejor[0])) for p, q in ivs]
            m = [(p, q) for p, q in m if p <= q + 1e-9]
            if m:
                ivs = m
        t = min((min(max(t0, p), q) for p, q in ivs), key=lambda x: abs(x - t0))
        return round(t / (1 - v) * 100, 2)

    def h_min(self):
        h = self.h0
        while h < self.h_nat and not self.posible(h):
            h += 1.0
        return min(h, self.h_nat)

    def ajustar(self, h):
        """El alto posible mas grande hasta h (ni menos que en pantalla ni mas que la foto entera)."""
        h = min(h, self.h_nat)
        while h >= self.h_min():
            if self.posible(h):
                return round(h, 1)
            h -= 0.5
        return None


# ---------------------------------------------------------------------------------------------- los capitulos
FIG_RE = re.compile(r'<figure><img src="asset:(f_\w+)\.jpg" alt=""(?: style="object-position:center ([\d.]+)%")?>'
                    r'<figcaption>')
DUO_RE = re.compile(r'<div class="duo"><figure><img src="asset:(f_\w+)\.jpg" alt=""></figure>'
                    r'<figure><img src="asset:(f_\w+)\.jpg" alt=""></figure></div>')


def capitulos():
    """Las secciones de content.py agrupadas por capitulo: uno nuevo en cada titulo de capitulo (h1)."""
    caps = []
    for s in content.SECTIONS[1:]:
        if "<h1" in s["html"] or not caps:
            caps.append({"id": s["id"], "secs": []})
        caps[-1]["secs"].append(s)
    for c in caps:
        c["fotos"] = {}
        for s in c["secs"]:
            for m in FIG_RE.finditer(s["html"]):
                c["fotos"][m.group(1)] = Foto(m.group(1), pos0=float(m.group(2) or 52))
            for m in DUO_RE.finditer(s["html"]):
                c["fotos"]["duo:" + m.group(1)] = Foto(m.group(1), duo=True)
        primera = c["secs"][0]["html"].lstrip()
        m = FIG_RE.match(primera)
        c["apertura"] = None
        if m:                                        # la foto de apertura: la figura de arriba, antes del titulo
            fin = primera.index("</figure>") + len("</figure>")
            c["apertura"] = (m.group(1), primera[:fin])
    return caps


def _marcar(h, sid):
    """El HTML de una seccion con su id en el primer elemento y el nombre de cada foto en su figura."""
    h = DUO_RE.sub(lambda m: m.group(0).replace('<div class="duo">', f'<div class="duo" data-foto="duo:{m.group(1)}">', 1), h)
    h = FIG_RE.sub(lambda m: m.group(0).replace("<figure>", f'<figure data-foto="{m.group(1)}">', 1), h)
    m = re.search(r"<(?!style)(\w+)", h)
    return h[:m.end()] + f' data-sec="{sid}"' + h[m.end():]


def html_capitulo(cap, caps, plan_fotos):
    """El capitulo entero en una sola pagina: encabezado, todas sus secciones seguidas y el pie. Si la foto de
    apertura se fue al capitulo anterior, no esta; si la del siguiente vino a este, va al final."""
    partes = []
    for s in cap["secs"]:
        h = s["html"]
        if s["id"] == "fuentes":                     # las fuentes vuelven a ser un solo cuadro
            h = h[:h.rindex("</table>")]
        if s["id"] == "fuentes2":
            assert h.startswith(content._F_CAB), h[:200]
            h = h[len(content._F_CAB):]
        if s is cap["secs"][0] and cap["apertura"] and cap["apertura"][0] in plan_fotos["al_anterior"]:
            h = h.lstrip()[len(cap["apertura"][1]):]
        partes.append(_marcar(h, s["id"]))
    k = caps.index(cap)
    if k + 1 < len(caps):
        sig = caps[k + 1]
        if sig["apertura"] and sig["apertura"][0] in plan_fotos["al_anterior"]:
            partes.append(_marcar(sig["apertura"][1], sig["secs"][0]["id"] + "-foto"))
    head = f'<div class="runhead">{cap["secs"][0]["runhead"]}</div>'
    foot = f'<div class="runfoot"><span>{content.DOC_TITLE}</span><span>P&aacute;gina 2 de 145</span></div>'
    return f'<div class="page" id="pg">{head}{"".join(partes)}{foot}</div>'


class Dibujante:
    """Un Chromium abierto para dibujar y medir los capitulos."""
    def __init__(self, pw):
        exe = os.environ.get("PW_CHROMIUM")
        self.br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        self.pg = self.br.new_page(viewport={"width": int(B.PAGE_W_PX), "height": 1200})
        self.n = 0

    def dibujar(self, body, nombre, cfg=None, pdf=False):
        f = B.OUT / f"{nombre}.html"
        f.write_text(B.SHELL % {"css": B.CSS, "body": B.inline_images(B.inline_svgs(body))}, encoding="utf-8")
        self.pg.goto(f.as_uri())
        self.pg.wait_for_timeout(350)
        try:
            self.pg.evaluate("document.fonts.ready")
        except Exception:
            pass
        self.pg.wait_for_timeout(150)
        self.pg.evaluate(JS_CONFIG, cfg or {"fotos": {}, "mover": []})
        self.pg.evaluate(B.JS_COLFILL)
        m = self.pg.evaluate(JS_MEDIR)
        self.n += 1
        if not pdf:
            return m, None
        destino = B.OUT / f"{nombre}.pdf"
        h_px = max(m["alto"], 841.89) * B.PT
        for extra in (2, 8, 14, 20, 26, 32):
            self.pg.pdf(path=str(destino), print_background=True, width=f"{B.PAGE_W_PX:.0f}px",
                        height=f"{h_px + extra:.0f}px", margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            d = fitz.open(str(destino))
            if len(d) == 1:
                return m, d
        raise RuntimeError(f"{nombre}: el PDF no entra en una pagina")

    def cerrar(self):
        self.br.close()


# ---------------------------------------------------------------------------------------------- el corte
def grupos(m):
    """Bloques que van juntos: un titulo con lo que sigue; la foto de apertura con el titulo del capitulo; el rotulo
    de un cuadro o grafico con el cuadro o grafico; un cuadro o grafico con su fuente y sus notas."""
    bl = [b for b in m["bloques"] if b["cls"] not in ("runhead", "runfoot") and b["tag"] != "style"
          and b["bottom"] - b["top"] > 0.1]
    out = []
    pegar_al_siguiente = False
    seccion = apartado = None
    for b in bl:
        previo = out[-1]["partes"][-1] if out else None
        de_cuadro = previo is not None and (previo["tabla"] or previo["dibujo"] or previo["tag"] == "table"
                                            or (previo["tag"] == "p" and previo["cls"].startswith("cap")))
        es_cola = ((b["tag"] == "p" and b["cls"].startswith("cap")) or b["tag"] == "figcaption"
                   or (b["cls"] == "note" and de_cuadro)
                   or (b["tag"] == "h1" and previo is not None and previo["tag"] == "figure"))
        if b["tag"] in ("h1", "h2"):
            seccion, apartado = b["txt"][:40], None
        if b["tag"] == "h3":
            apartado = b["txt"][:40]
        if out and (pegar_al_siguiente or es_cola):
            g = out[-1]
            g["bottom"] = max(g["bottom"], b["bottom"])
            g["partes"].append(b)
        else:
            out.append({"top": b["top"], "bottom": b["bottom"], "partes": [b], "sec": seccion, "sub": apartado})
        titulo = b["tag"] in ("h1", "h2", "h3", "h4") or b["cls"] in ("stand", "igrp", "hairline")
        rotulo = b["cls"].split(" ")[0] == "ex" and not (b["tabla"] or b["dibujo"])
        pegar_al_siguiente = titulo or rotulo
        if titulo and b["tag"] in ("h1", "h2", "h3"):
            out[-1]["sec"], out[-1]["sub"] = seccion, apartado
    for g in out:
        g["foto"] = next((p["foto"] for p in g["partes"] if p["foto"]), None)
        g["inicio"] = g["partes"][0]["i"]
    return out


def atomos(m):
    """Los pedazos entre los que se puede cortar. Un grupo va entero, salvo un cuadro largo (entre filas, con el
    encabezado repetido arriba), una lista larga (entre puntos) y un recuadro que no entra en una hoja entera
    (entre sus parrafos, y se avisa). Cada pedazo: arriba, abajo, aire arriba y abajo, encabezado a repetir."""
    entra = LIM - ARRIBA_CONT
    largo = entra / 3
    out, partidos = [], []

    def nuevo(g, top, bottom, pt=2.0, pb=2.0, rep=None, primero=True, parte=None):
        out.append(dict(top=top, bottom=bottom, pt=pt, pb=pb, rep=rep, primero=primero, g=g, parte=parte))

    for g in grupos(m):
        alto = g["bottom"] - g["top"]
        tabla = next((p for p in g["partes"] if p.get("filas")), None)
        lista = next((p for p in g["partes"] if p.get("items")), None)
        recuadro = next((p for p in g["partes"] if p.get("hijos")), None)
        if tabla and alto > largo:
            filas = tabla["filas"]
            enc = [f for f in filas[:2] if f["th"]]
            rep = (enc[0]["top"], enc[-1]["bottom"]) if enc else None
            unidades, actual = [], None
            for f in filas[len(enc):]:                 # una fila de subtitulo va con la que la sigue
                if actual is None:
                    actual = [f["top"], f["bottom"]]
                else:
                    actual[1] = f["bottom"]
                if not f["sub"]:
                    unidades.append(actual)
                    actual = None
            if actual:
                unidades.append(actual)
            if len(unidades) >= 4:
                nuevo(g, g["top"], unidades[1][1], pb=0.0, parte="cuadro")
                for u in unidades[2:-2]:
                    nuevo(g, u[0], u[1], 0.0, 0.0, rep, False, "cuadro")
                nuevo(g, unidades[-2][0], g["bottom"], pt=0.0, rep=rep, primero=False, parte="cuadro")
                partidos.append(("cuadro", g))
                continue
        if lista and alto > largo and len(lista["items"]) >= 4 and not recuadro:
            it = lista["items"]
            nuevo(g, g["top"], it[1][1], parte="lista")
            for a, z in it[2:-2]:
                nuevo(g, a, z, primero=False, parte="lista")
            nuevo(g, it[-2][0], g["bottom"], primero=False, parte="lista")
            partidos.append(("lista", g))
            continue
        if recuadro and alto > entra:
            hijos = recuadro["hijos"]
            cortes = [hijos[1][1]] + [h[1] for h in hijos[2:-1]]      # el rotulo va con el primer punto
            a = g["top"]
            for k, c in enumerate(cortes):
                nuevo(g, a, c, primero=(k == 0), parte="recuadro")
                a = c
            nuevo(g, a, g["bottom"], primero=False, parte="recuadro")
            partidos.append(("recuadro", g))
            continue
        nuevo(g, g["top"], g["bottom"])
    return out, partidos


def uso(at, i, j, primera):
    """Hasta donde llega el contenido de una hoja con los pedazos i..j-1."""
    if primera:
        return at[j - 1]["bottom"]
    rep = at[i]["rep"]
    extra = (rep[1] - rep[0]) if (rep and not at[i]["primero"]) else 0.0
    return ARRIBA_CONT + extra + at[j - 1]["bottom"] - at[i]["top"]


def blanco(u):
    return (AREA1 - u) / (AREA1 - AREA0)


def _hoja(at, i, j, primera):
    tramos = []
    if primera:
        tramos.append([0.0, at[j - 1]["bottom"], 0.0, at[j - 1]["pb"], False])
    else:
        rep = at[i]["rep"]
        if rep and not at[i]["primero"]:
            tramos.append([rep[0], rep[1], 0.0, 0.0, True])
        tramos.append([at[i]["top"], at[j - 1]["bottom"], at[i]["pt"], at[j - 1]["pb"], False])
    u = uso(at, i, j, primera)
    return {"tramos": tramos, "primera": primera, "i": i, "j": j, "uso": u, "blanco": blanco(u)}


def voraz(at):
    """Cada hoja se llena con todo lo que entra: un cuadro o una lista larga se parte solo si dejarlo entero para la
    hoja siguiente deja mas de un tercio en blanco."""
    hojas, i, primera = [], 0, True
    while i < len(at):
        j = i + 1
        while j < len(at) and uso(at, i, j + 1, primera) <= LIM:
            j += 1
        # no partir un grupo si dejarlo entero para la siguiente hoja no deja un hueco grande
        if j < len(at) and not at[j]["primero"]:
            k = j
            while k > i + 1 and not at[k]["primero"]:
                k -= 1
            if at[k]["primero"] and k > i and blanco(uso(at, i, k, primera)) <= TOPE:
                j = k
        hojas.append(_hoja(at, i, j, primera))
        i, primera = j, False
    return hojas


def repartido(at, ultimo_doc, estricto=True):
    """El corte con menos hojas de mas de un tercio en blanco (salvo la ultima del documento) y, entre esos, con
    menos hojas, cortando cada hoja lo mas abajo posible. Estricto: None si alguna hoja pasa del tercio."""
    n = len(at)
    INF = (10 ** 9, 10 ** 9)
    mejor = [INF] * (n + 1)
    mejor[n] = (0, 0)

    def costo(i, j):
        u = uso(at, i, j, i == 0)
        mala = blanco(u) > TOPE and not (j == n and ultimo_doc)
        return u, int(mala)

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            u, mala = costo(i, j)
            if u > LIM and j > i + 1:
                break
            if mejor[j] == INF:
                continue
            c = (mala + mejor[j][0], 1 + mejor[j][1])
            if c < mejor[i]:
                mejor[i] = c
    if mejor[0] == INF or (estricto and mejor[0][0] > 0):
        return None
    hojas, i = [], 0
    while i < n:
        elegido = None
        for j in range(i + 1, n + 1):
            u, mala = costo(i, j)
            if u > LIM and j > i + 1:
                break
            if mejor[j] != INF and (mala + mejor[j][0], 1 + mejor[j][1]) == mejor[i]:
                elegido = j
        hojas.append(_hoja(at, i, elegido, i == 0))
        i = elegido
    return hojas


def malas(hojas, ultimo_doc):
    return [k for k, h in enumerate(hojas) if h["blanco"] > TOPE and not (ultimo_doc and k == len(hojas) - 1)]


# ---------------------------------------------------------------------------------------------- llenar huecos
class Reparto:
    """Las decisiones sobre las fotos de todo el documento: alto y encuadre de cada una, las que se suben dentro de
    su seccion (antes de que bloque) y las fotos de apertura que pasan al final del capitulo anterior."""
    def __init__(self, caps):
        self.caps = caps
        self.fotos = {}                         # nombre -> alto
        self.mover = {}                         # nombre -> data-i del bloque antes del cual va
        self.al_anterior = set()
        self.notas = []
        for c in caps:
            for nombre, f in c["fotos"].items():
                self.fotos[nombre] = f.h_min()

    def foto(self, nombre):
        for c in self.caps:
            if nombre in c["fotos"]:
                return c["fotos"][nombre]

    def cfg(self, cap):
        fotos = {}
        for c in self.caps:
            for nombre, f in c["fotos"].items():
                h = self.fotos[nombre]
                pos = f.pos(h)
                if f.duo:                            # el par: el mismo alto, cada una con su encuadre
                    otra = Foto(_otra_del_duo(nombre), duo=True)
                    pos = [pos, otra.pos(min(h, otra.h_nat))]
                fotos[nombre] = {"h": round(h, 2), "pos": pos}
        mover = [{"foto": f, "antes": i} for f, i in self.mover.items() if f in cap["fotos"]]
        return {"fotos": fotos, "mover": mover}

    def plan(self):
        return {"al_anterior": self.al_anterior}


def _otra_del_duo(nombre):
    for s in content.SECTIONS:
        for m in DUO_RE.finditer(s["html"]):
            if "duo:" + m.group(1) == nombre:
                return m.group(2)


def _fotos_en(hojas_k, at):
    return [a["g"] for a in at[hojas_k["i"]:hojas_k["j"]] if a["g"]["foto"] and a["primero"]]


def armar_capitulo(dib, cap, caps, rep, ultimo_doc, registro):
    """Dibuja el capitulo, lo corta y llena los huecos con las fotos, hasta que ninguna hoja pase del tercio."""
    k_cap = caps.index(cap)
    sin_arreglo = set()                       # huecos que ninguna foto puede llenar (por su lugar en el capitulo)
    for vuelta in range(80):
        body = html_capitulo(cap, caps, rep.plan())
        m, _ = dib.dibujar(body, f"a4_{cap['id']}", rep.cfg(cap))
        at, _ = atomos(m)
        hojas = voraz(at)
        todas = malas(hojas, ultimo_doc)
        mal = [k for k in todas if (hojas[k]["i"], hojas[k]["j"]) not in sin_arreglo]
        if not todas:
            return m, hojas, at, "voraz"
        if not mal:
            # sin fotos que sirvan: se reparte el corte entre las hojas
            r = repartido(at, ultimo_doc)
            if r is not None:
                registro.append(f"{cap['id']}: corte repartido en {len(r)} hojas (sin fotos para llenar "
                                f"{', '.join('la hoja %d' % (k + 1) for k in todas)})")
                return m, r, at, "repartido"
            r = repartido(at, ultimo_doc, estricto=False)
            quedan = malas(r, ultimo_doc)
            if len(quedan) >= len(todas):
                r, quedan = hojas, todas
            for k in quedan:
                registro.append(f"{cap['id']}: !! la hoja {k + 1} queda con {r[k]['blanco']:.0%} en blanco y no hay "
                                f"como llenarla")
            return m, r, at, "repartido"
        s = mal[0]
        h = hojas[s]
        espacio = LIM - h["uso"]
        ultima_del_cap = s == len(hojas) - 1
        hecho = None
        # 1) una foto de esa hoja, mas alta
        cands = _fotos_en(h, at)
        sec_final = at[h["j"] - 1]["g"]["sec"]
        cands.sort(key=lambda g: (g["sec"] != sec_final, -g["top"]))
        for g in cands:
            f = rep.foto(g["foto"])
            nuevo = f.ajustar(rep.fotos[g["foto"]] + espacio - 1.0)
            if nuevo and nuevo > rep.fotos[g["foto"]] + 0.5 and blanco(h["uso"] + nuevo - rep.fotos[g["foto"]]) <= TOPE:
                hecho = f"hoja {s + 1}: {g['foto']} de {rep.fotos[g['foto']]:.0f} a {nuevo:.0f} pt"
                rep.fotos[g["foto"]] = nuevo
                break
        # 2) subir una foto de esa seccion (de mas adelante en el capitulo) al final de la hoja
        if not hecho and not ultima_del_cap and at[h["j"]]["primero"]:
            ref = at[h["j"]]["g"]
            ultimo = at[h["j"] - 1]["g"]["partes"][-1]
            sub_final = at[h["j"] - 1]["g"]["sub"]
            for g in [a["g"] for a in at[h["j"]:] if a["primero"] and a["g"]["foto"]]:
                if (g["sec"], g["sub"]) != (sec_final, sub_final) or g["foto"].startswith("duo:") or g["foto"] in rep.mover:
                    continue
                if ultimo["foto"] or ref["foto"]:              # nunca dos fotos seguidas
                    continue
                if any(p["tag"] == "h1" for p in g["partes"]):
                    continue
                fig = next(p for p in g["partes"] if p["foto"])
                cola = (fig["bottom"] - fig["top"]) - fig["img_h"]
                aire = max(ultimo["mb"], 0) + fig["mt"]
                f = rep.foto(g["foto"])
                nuevo = f.ajustar(espacio - aire - cola - 1.0)
                if nuevo:
                    hecho = f"hoja {s + 1}: sube {g['foto']} ({nuevo:.0f} pt)"
                    rep.fotos[g["foto"]] = nuevo
                    rep.mover[g["foto"]] = ref["inicio"]
                    break
        # 3) en la ultima hoja del capitulo, la foto de apertura del siguiente
        if not hecho and ultima_del_cap and k_cap + 1 < len(caps):
            sig = caps[k_cap + 1]
            if sig["apertura"] and sig["apertura"][0] not in rep.al_anterior:
                nombre = sig["apertura"][0]
                f = sig["fotos"][nombre]
                ultimo = at[h["j"] - 1]["g"]["partes"][-1]
                cola = 18.0                                   # epigrafe de una linea y su aire
                nuevo = f.ajustar(espacio - max(ultimo["mb"], 0) - 13.0 - cola - 1.0)
                if nuevo:
                    hecho = f"hoja {s + 1}: la foto de apertura del capitulo siguiente ({nombre}, {nuevo:.0f} pt)"
                    rep.al_anterior.add(nombre)
                    rep.fotos[nombre] = nuevo
        # 4) una foto de la hoja anterior, mas alta, empuja su ultimo bloque a esta hoja
        if not hecho and s > 0:
            ha = hojas[s - 1]
            for g in _fotos_en(ha, at):
                f = rep.foto(g["foto"])
                for kk in range(1, 6):
                    j2 = ha["j"] - kk
                    if j2 <= ha["i"] or at[j2]["top"] <= g["bottom"] or not at[j2]["primero"]:
                        break
                    if uso(at, j2, h["j"], False) > LIM:
                        break
                    if blanco(uso(at, j2, h["j"], False)) > TOPE:
                        continue
                    nuevo = f.ajustar(rep.fotos[g["foto"]] + LIM - uso(at, ha["i"], j2, ha["primera"]) - 1.0)
                    falta = LIM - uso(at, ha["i"], j2 + 1, ha["primera"])      # lo que hay que crecer para empujar
                    if nuevo and nuevo - rep.fotos[g["foto"]] > falta + 0.5:
                        hecho = f"hoja {s}: {g['foto']} de {rep.fotos[g['foto']]:.0f} a {nuevo:.0f} pt (empuja a la {s + 1})"
                        rep.fotos[g["foto"]] = nuevo
                        break
                if hecho:
                    break
        if hecho:
            registro.append(f"{cap['id']}: {hecho}")
        else:
            sin_arreglo.add((h["i"], h["j"]))
    raise RuntimeError(f"{cap['id']}: no converge")


def rellenar(dib, cap, caps, rep, m, hojas, at, registro, umbral=0.15):
    """Ya sin huecos de mas de un tercio: en cada hoja con mas de 15% en blanco que tenga una foto, la foto se
    muestra mas alta hasta llenarla (no mueve nada de las otras hojas)."""
    for vuelta in range(40):
        cambio = False
        for s, h in enumerate(hojas):
            if h["blanco"] <= umbral or (s == len(hojas) - 1 and caps.index(cap) == len(caps) - 1):
                continue
            espacio = LIM - h["uso"]
            for g in sorted(_fotos_en(h, at), key=lambda g: -g["top"]):
                f = rep.foto(g["foto"])
                nuevo = f.ajustar(rep.fotos[g["foto"]] + espacio - 1.0)
                if nuevo and nuevo > rep.fotos[g["foto"]] + 3:
                    registro.append(f"{cap['id']}: hoja {s + 1} ({h['blanco']:.0%} en blanco): {g['foto']} de "
                                    f"{rep.fotos[g['foto']]:.0f} a {nuevo:.0f} pt")
                    rep.fotos[g["foto"]] = nuevo
                    cambio = True
                    break
            if cambio:
                break
        if not cambio:
            return m, hojas, at
        cortes = [(h["i"], h["j"], h["primera"]) for h in hojas]
        body = html_capitulo(cap, caps, rep.plan())
        m, _ = dib.dibujar(body, f"a4_{cap['id']}", rep.cfg(cap))
        at2, _ = atomos(m)
        if len(at2) != len(at):
            raise RuntimeError(f"{cap['id']}: llenar con una foto cambio los pedazos")
        at = at2
        hojas = [_hoja(at, i, j, p) for i, j, p in cortes]      # los mismos cortes: solo crece esa hoja
        if any(h["uso"] > LIM + 0.5 for h in hojas):
            raise RuntimeError(f"{cap['id']}: llenar con una foto desbordo una hoja")
    return m, hojas, at


# ---------------------------------------------------------------------------------------------- la hoja
def fondo(src):
    """El color del fondo, leido de una pagina dibujada por Chrome (lo dibuja apenas distinto del CSS)."""
    global FONDO
    if FONDO is None:
        px = src[0].get_pixmap(clip=fitz.Rect(2, 2, 6, 6)).pixel(1, 1)
        FONDO = tuple(v / 255 for v in px[:3])
    return FONDO


def pie_original(src_pg, m):
    """Donde esta el pie en la pagina dibujada: la raya de arriba, y desde donde empieza el numero."""
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    num = [s for b in src_pg.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]
           if s["text"].strip().startswith("Página") and s["bbox"][1] > pie["top"] - 2]
    x_num = num[0]["bbox"][0] if num else 520.0
    base = num[0]["origin"][1] if num else pie["bottom"] - 2
    return pie, x_num, base


_RAYAS = {}


def raya_pie(src, pno, pie):
    """La raya del pie tal como la dibujo Chrome: el rectangulo de 0,75 pt a lo ancho de la caja, junto al pie, con su
    color y su transparencia. Se redibuja igual en la hoja, en vez de recortarla, para no llevarse la punta del borde
    de un recuadro o de un cuadro que llega hasta ella."""
    key = (id(src), pno)
    if key not in _RAYAS:
        _RAYAS[key] = None
        for d in src[pno].get_drawings():
            r = d["rect"]
            if abs(r.height - 0.75) < 0.2 and r.width > 500 and abs(r.y0 - pie["top"]) < 3 and d.get("fill"):
                _RAYAS[key] = (fitz.Rect(r), d["fill"], d.get("fill_opacity") or 1.0)
                break
    return _RAYAS[key]


def escribir(pg, x_der, base, texto, tam, espaciado):
    """Texto alineado a la derecha, con la letra y el espaciado del pie de pantalla."""
    f = fitz.Font(fontfile=str(INTER))
    ancho = sum(f.text_length(c, fontsize=tam) for c in texto) + espaciado * (len(texto) - 1)
    tw = fitz.TextWriter(pg.rect, color=GRIS)
    x = x_der - ancho
    for c in texto:
        tw.append((x, base), c, font=f, fontsize=tam)
        x += f.text_length(c, fontsize=tam) + espaciado
    tw.write_text(pg)


# ---------------------------------------------------------------------------------------------- solo lo visible
# show_pdf_page pone en la hoja la pagina dibujada entera y la recorta: lo de afuera del recorte no se ve, pero su
# texto queda guardado en la hoja y lo leen los buscadores y los programas que sacan el texto de un PDF (dispatch 9).
# Por eso cada recorte sale de una copia de la pagina a la que se le borro, con redaccion, el texto de afuera del
# recorte, y los dibujos que quedan enteros afuera (un capitulo es una sola pagina larga: sin esto, cada hoja
# llevaria todos sus graficos). Las imagenes quedan como estan. Lo que se ve no cambia: cada copia se compara con la
# pagina original adentro del recorte, letra por letra y pixel por pixel.
TODO_EL_TEXTO = fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE   # todo el texto, aun fuera de la hoja
_COPIAS, _LETRAS = {}, {}
CONTROL_COPIAS = {"copias": 0, "problemas": []}


def _letras(pg, clip=None):
    """Las letras de una pagina (o de una franja), con su lugar y su centro."""
    out = []
    for b in pg.get_text("rawdict", flags=TODO_EL_TEXTO, clip=clip)["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                for c in s["chars"]:
                    if c["c"].strip():
                        x0, y0, x1, y1 = c["bbox"]
                        out.append(((c["c"], round(c["origin"][0], 1), round(c["origin"][1], 1)),
                                    (x0 + x1) / 2, (y0 + y1) / 2))
    return out


def _pixeles(pg, clip):
    """Los pixeles de adentro del recorte, a 144 dpi, sin la fila y la columna del borde (que caen a medias afuera)."""
    adentro = fitz.Rect(clip.x0 + 0.5, clip.y0 + 0.5, clip.x1 - 0.5, clip.y1 - 0.5)
    return pg.get_pixmap(matrix=fitz.Matrix(2, 2), clip=adentro, alpha=False).samples


def visible(src, pno, clip):
    """La pagina pno de src con solo el texto que se ve en clip, como (documento, numero de pagina) para show_pdf_page."""
    if id(src) not in _COPIAS:
        _COPIAS[id(src)] = (fitz.open("pdf", src.tobytes()), {})   # las copias comparten imagenes y letras
    doc, hechas = _COPIAS[id(src)]
    clave = (pno, tuple(round(v, 3) for v in clip))
    if clave not in hechas:
        doc.fullcopy_page(pno)
        k = len(doc) - 1
        pg = doc[k]
        w, h = pg.rect.width, pg.rect.height
        for r in (fitz.Rect(0, 0, w, clip.y0), fitz.Rect(0, clip.y1, w, h),
                  fitz.Rect(0, clip.y0, clip.x0, clip.y1), fitz.Rect(clip.x1, clip.y0, w, clip.y1)):
            if r.width > 0.01 and r.height > 0.01:
                pg.add_redact_annot(r, fill=False)
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                            text=fitz.PDF_REDACT_TEXT_REMOVE)
        # el control: la copia tiene justo las letras que se ven en el recorte, y adentro del recorte se ve igual
        franja = fitz.Rect(0, clip.y0 - 40, w, clip.y1 + 40)
        se_ven = collections.Counter(c for c, x, y in _letras(src[pno], franja) if clip.x0 <= x <= clip.x1
                                     and clip.y0 <= y <= clip.y1)
        quedan = collections.Counter(c for c, _, _ in _letras(pg))
        igual = _pixeles(src[pno], clip) == _pixeles(pg, clip)
        CONTROL_COPIAS["copias"] += 1
        if se_ven != quedan or not igual:
            CONTROL_COPIAS["problemas"].append((pno + 1, tuple(round(v, 1) for v in clip), sum((se_ven - quedan).values()),
                                                sum((quedan - se_ven).values()), igual))
        hechas[clave] = k
    return doc, hechas[clave]


def componer(dst, src, pno, m, hoja, n_hoja, total):
    """Una hoja A4: fondo, encabezado, los tramos de la pagina dibujada y el pie con el numero de hoja."""
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    E = ESC
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    tope = pie["top"] - 0.1                    # ningun tramo se lleva la raya del pie
    y = 0.0
    if not hoja["primera"]:
        cab = next(b for b in m["bloques"] if b["cls"] == "runhead")
        cl = fitz.Rect(0, 0, 660, cab["bottom"] + 2)
        pg.show_pdf_page(fitz.Rect(0, 0, A4_W, cl.y1 * E), *visible(src, pno, cl), clip=cl)
        y = ARRIBA_CONT
    for (a, z, pa, pz, _) in hoja["tramos"]:
        a0 = max(0.0, a - pa)
        z1 = min(z + pz, tope)
        y0 = y - (a - a0)
        cl = fitz.Rect(0, a0, 660, z1)
        pg.show_pdf_page(fitz.Rect(0, y0 * E, A4_W, (y0 + z1 - a0) * E), *visible(src, pno, cl), clip=cl)
        y += z - a
    # el pie: la raya y el titulo, tal cual; el numero, el de la hoja
    _, x_num, base = pie_original(src[pno], m)
    alto = max(m["alto"], 841.89)
    dy = HOJA - alto                           # el pie va al fondo de la hoja, como en pantalla
    rp = raya_pie(src, pno, pie)
    if rp:                                     # la raya, redibujada igual: nada de lo que la toca arriba
        r, color, opac = rp
        pg.draw_rect(fitz.Rect(r.x0 * E, (r.y0 + dy) * E, r.x1 * E, (r.y1 + dy) * E), color=None, fill=color,
                     fill_opacity=opac, overlay=True)
        izq = fitz.Rect(0, r.y1, x_num - 2, alto)
    else:
        raya = fitz.Rect(0, pie["top"] + 0.1, 660, pie["top"] + 0.85)
        pg.show_pdf_page(fitz.Rect(0, (raya.y0 + dy) * E, A4_W, (raya.y1 + dy) * E), *visible(src, pno, raya), clip=raya)
        izq = fitz.Rect(0, raya.y1, x_num - 2, alto)
    pg.show_pdf_page(fitz.Rect(izq.x0 * E, (izq.y0 + dy) * E, izq.x1 * E, (izq.y1 + dy) * E), *visible(src, pno, izq),
                     clip=izq)
    escribir(pg, (660 - 45) * E, (base + dy) * E, f"Página {n_hoja} de {total}", 6.4 * E, 0.25 * E)
    return pg


def portada(dst, src):
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    pg.show_pdf_page(pg.rect, src, 0)
    return pg


# ---------------------------------------------------------------------------------------------- el indice
def _plano(t):
    t = unicodedata.normalize("NFKC", H.unescape(re.sub(r"<[^>]+>", "", t))).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


def hoja_de_seccion(m, hojas, n_primera, sid, txt):
    """La hoja de la A4 donde cae el titulo de una entrada del indice (o, si no se lo encuentra, el comienzo de su
    seccion)."""
    desde = next((b["top"] for b in m["bloques"] if b["sec"] == sid), None)
    plano = _plano(txt)
    num = re.match(r"(\d+\.\d+)\s", plano)
    y = None
    for t, top in m["titulos"]:
        if desde is not None and top < desde - 1:
            continue
        tp = _plano(t)
        if (num and re.match(re.escape(num.group(1)) + r"(?!\d)", tp)) or (not num and tp.startswith(plano[:24])):
            y = top
            break
    if y is None:
        y = desde if desde is not None else 0.0
    for k, h in enumerate(hojas):
        if any(a - 3 <= y <= z + 3 for a, z, _, _, rep in h["tramos"] if not rep):
            return n_primera + k
    return n_primera


def indice_html(numeros):
    """El mismo indice de la version de pantalla (content_a), con los numeros de hoja de la A4."""
    base = CA._indice()
    cab = base[:base.index('<div class="igrp">')]
    filas, it = [], iter(numeros)
    for kind, txt, key in CA._IDX:
        if kind == "g":
            filas.append(f'<div class="igrp">{txt}</div>')
        else:
            filas.append('<div class="irow"><span class="it">%s</span><span class="ilead"></span>'
                         '<span class="ipg">%s</span></div>' % (txt, next(it)))
    return cab + "".join(filas)


def body_indice(numeros, total):
    s = content.SECTIONS[0]
    assert s["id"] == "indice"
    head = f'<div class="runhead">{s["runhead"]}</div>' if s.get("runhead") else ""
    foot = (f'<div class="runfoot"><span>{content.DOC_TITLE}</span>'
            f'<span>P&aacute;gina 2 de {total}</span></div>')
    return f'<div class="page" id="pg">{head}{indice_html(numeros)}{foot}</div>'


def cortar_parejo(m):
    at, _ = atomos(m)
    return repartido(at, False) or voraz(at)


# ---------------------------------------------------------------------------------------------- todo
def plan_completo():
    """Arma cada capitulo con sus fotos, lo corta, numera las hojas y dibuja el indice con esos numeros."""
    caps = capitulos()
    rep = Reparto(caps)
    registro = []
    res = []
    with sync_playwright() as pw:
        dib = Dibujante(pw)
        for k, cap in enumerate(caps):
            m, hojas, at, modo = armar_capitulo(dib, cap, caps, rep, k == len(caps) - 1, registro)
            m, hojas, at = rellenar(dib, cap, caps, rep, m, hojas, at, registro)
            res.append({"cap": cap, "m": m, "hojas": hojas, "modo": modo,
                        "cortes": [(h["i"], h["j"], h["primera"]) for h in hojas]})
        # el capitulo anterior pudo llevarse la foto de apertura de este despues de cortarlo: se rehacen todos
        # con las decisiones finales, y se comprueba que el corte no cambia
        for k, r in enumerate(res):
            cap = r["cap"]
            body = html_capitulo(cap, caps, rep.plan())
            m, doc = dib.dibujar(body, f"a4_{cap['id']}", rep.cfg(cap), pdf=True)
            at, partidos = atomos(m)
            hojas = [_hoja(at, i, j, p) for i, j, p in r["cortes"]]      # los cortes ya decididos
            assert all(h["uso"] <= LIM + 0.5 for h in hojas), cap["id"]
            r.update(m=m, hojas=hojas, doc=doc, partidos=partidos)
        # el indice: primero con numeros de prueba, para saber cuantas hojas lleva
        n_idx = sum(1 for x in CA._IDX if x[0] == "i")
        m_ind, _ = dib.dibujar(body_indice(["000"] * n_idx, 999), "a4_indice")
        h_ind = len(cortar_parejo(m_ind))
        n = 1 + h_ind
        for r in res:
            r["n_primera"] = n + 1
            n += len(r["hojas"])
        total = n
        por_sec = {s["id"]: r for r in res for s in r["cap"]["secs"]}
        nums = []
        for kind, txt, key in CA._IDX:
            if kind != "i":
                continue
            r = por_sec[key]
            nums.append(hoja_de_seccion(r["m"], r["hojas"], r["n_primera"], key, txt))
        m_ind, doc_ind = dib.dibujar(body_indice(nums, total), "a4_indice", pdf=True)
        hojas_ind = cortar_parejo(m_ind)
        assert len(hojas_ind) == h_ind, (len(hojas_ind), h_ind)
        print(f"  dibujos: {dib.n}")
        dib.cerrar()
    return res, rep, registro, (m_ind, doc_ind, hojas_ind), nums, total


def armar(solo=None, destino=SALIDA):
    res, rep, registro, (m_ind, doc_ind, hojas_ind), nums, total = plan_completo()
    print(f"A4: {total} hojas (con la tapa)")
    for x in registro:
        print("  ", x)
    for r in res:
        for k, g in r["partidos"]:
            print(f"  partido ({k}): {r['cap']['id']}, {g['bottom'] - g['top']:.0f} pt: {g['partes'][0]['txt'][:60]}")
    tapa = fitz.open(str(PANTALLA))
    fondo(res[0]["doc"])                         # el beige, de una pagina dibujada (no de la tapa)
    dst = fitz.open()
    plan = [(None, None, None, 1)]
    for k, h in enumerate(hojas_ind):
        plan.append((doc_ind, m_ind, h, 2 + k))
    for r in res:
        for k, h in enumerate(r["hojas"]):
            plan.append((r["doc"], r["m"], h, r["n_primera"] + k))
    assert plan[-1][3] == total, (plan[-1][3], total)
    for doc, m, h, n in plan:
        if solo and n not in solo:
            continue
        if doc is None:
            portada(dst, tapa)
        else:
            componer(dst, doc, 0, m, h, n, total)
    dst.save(str(destino), garbage=3, deflate=True)
    dst = fitz.open(str(destino))
    print(f"-> {destino} | {len(dst)} hojas | {destino.stat().st_size / 1e6:.1f} MB")
    print(f"  recortes con solo el texto que se ve: {CONTROL_COPIAS['copias']}; con diferencias: "
          f"{len(CONTROL_COPIAS['problemas'])}")
    for p in CONTROL_COPIAS["problemas"]:
        print("     !! pag. %d, recorte %s: faltan %d letras, sobran %d, se ve igual: %s" % p)
    fotos = {n: round(h) for n, h in rep.fotos.items()}
    print("  fotos (alto en pt de pantalla):", fotos)
    print("  subidas:", rep.mover, "| al capitulo anterior:", sorted(rep.al_anterior))
    return dst, plan, res, rep, nums, total


# ---------------------------------------------------------------------------------------------- controles
def blanco_al_pie(dst, desde=2):
    """El blanco de cada hoja, medido en la hoja dibujada: desde el ultimo contenido hasta la raya del pie, sobre el
    alto entre el encabezado y la raya."""
    import numpy as np
    out = []
    y_cab, y_raya = AREA0 * ESC, AREA1 * ESC
    for n in range(desde, len(dst) + 1):
        pm = dst[n - 1].get_pixmap(dpi=72, alpha=False)
        a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, 3).astype(int)
        zona = a[int(y_cab) + 2:int(y_raya) - 2, 40:int(A4_W) - 40]
        distinto = (np.abs(zona - a[3, 3]).sum(axis=2) > 6).any(axis=1)
        filas = np.nonzero(distinto)[0]
        ultimo = int(y_cab) + 2 + (filas[-1] if len(filas) else 0)
        out.append((n, (y_raya - 1 - ultimo) / (y_raya - y_cab)))
    return out


def comparar(dst, total, n_ind):
    """Todo el texto de la A4 (se vea o no) contra el de la version de pantalla, sin la tapa, el indice, los
    encabezados y los pies: tiene que ser el mismo, palabra por palabra; de mas solo pueden estar los encabezados
    repetidos de los cuadros partidos."""
    src = fitz.open(str(PANTALLA))

    def cuerpo(pg, esc):
        H_ = pg.rect.height
        return collections.Counter(w[4] for w in pg.get_text("words", flags=TODO_EL_TEXTO)
                                   if 52 * esc < (w[1] + w[3]) / 2 < H_ - 40 * esc)
    p = collections.Counter()
    for k in range(2, len(src)):
        p += cuerpo(src[k], 1.0)
    a = collections.Counter()
    for k in range(1 + n_ind, len(dst)):
        a += cuerpo(dst[k], ESC)
    return p - a, a - p


def muestras(hojas, carpeta):
    """Esas hojas de la A4, en un PDF y en imagenes, para el visto bueno (la A4 entera queda en out/)."""
    dst, plan, res, rep, nums, total = armar(destino=B.OUT / "a4_completa.pdf")
    carpeta.mkdir(parents=True, exist_ok=True)
    for f in carpeta.glob("*"):
        f.unlink()
    m = fitz.open()
    for n in hojas:
        m.insert_pdf(dst, from_page=n - 1, to_page=n - 1)
        dst[n - 1].get_pixmap(dpi=110).save(str(carpeta / f"hoja_{n:03d}.png"))
    m.save(str(carpeta / "MUESTRAS_A4.pdf"), garbage=3, deflate=True)
    return dst, plan, total


def controles(dst, total, n_ind):
    print("  blanco al pie (de la raya del pie al ultimo contenido, sobre el alto entre encabezado y raya):")
    b = blanco_al_pie(dst)
    malas_h = [(n, f) for n, f in b if f > TERCIO and n != len(dst)]
    print(f"     hojas con mas de un tercio en blanco (sin contar la ultima): {len(malas_h)} {[(n, round(f * 100)) for n, f in malas_h]}")
    print(f"     entre 15% y un tercio: {sum(1 for n, f in b if 0.15 < f <= TERCIO)} | la ultima: {b[-1][1]:.0%}")
    faltan, sobran = comparar(dst, total, n_ind)
    print(f"  texto contra la pantalla: faltan {sum(faltan.values())} {list(faltan.items())[:12]}; "
          f"sobran {sum(sobran.values())} {list(sobran.items())[:12]}")
    return b


if __name__ == "__main__":
    if "--muestras" in sys.argv:
        hojas = [int(x) for x in sys.argv[sys.argv.index("--muestras") + 1:]]
        dst, plan, total = muestras(hojas, ROOT / "salida" / "muestras_a4")
    else:
        dst, plan, res, rep, nums, total = armar()
        print("  indice A4:", ", ".join(map(str, nums)))
    controles(dst, total, sum(1 for x in plan if x[0] is not None and x[0] is plan[1][0]))
