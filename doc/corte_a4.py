#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version A4: la version de pantalla tal cual, achicada en forma pareja (660 -> 595,28 pt de ancho, un 90%)
y cortada en hojas A4. No rehace nada: toma cada pagina del PDF de pantalla y la reparte en hojas, cortando
solo entre bloques (parrafo, bloque de dos columnas, recuadro, cuadro, grafico, foto). Un titulo nunca queda
separado de lo que sigue, ni un cuadro o grafico de su rotulo y de su fuente.

Cada hoja lleva el encabezado y el pie de la pagina de pantalla; el pie dice el numero de hoja de la A4.
Si un bloque no entra en una hoja, o si alguna letra queda por debajo de 8 pt, se avisa: no se cambia nada.

Uso:  python3 doc/corte_a4.py --muestras   (cuatro hojas de muestra, al lado de la version de pantalla)
Lee salida/PROGRAMA_SAN_ISIDRO_2027.pdf y out/sNN.html, que deja doc/build.py."""
import json, os, pathlib, re, sys
import pymupdf as fitz
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build as B          # solo se lee: el HTML y el script de columnas de la version de pantalla

ROOT = HERE.parent
PANTALLA = ROOT / "salida" / "PROGRAMA_SAN_ISIDRO_2027.pdf"
A4_W, A4_H = 595.2756, 841.8898
ESC = A4_W / B.PAGE_W_PT                  # 0,9019: todo se achica igual
HOJA = A4_H / ESC                         # alto de una hoja A4, en pt de la pagina de pantalla (933,4)
# los margenes de la pagina de pantalla (design.css): encabezado arriba, pie abajo
ARRIBA_CONT = 40.5 + 6.75 + 16.5          # en una hoja que sigue: el encabezado y el aire de un titulo h2
ABAJO = 28.1 + 7 + 0.75 + 6.4 + 30        # aire antes del pie, el pie y el margen de abajo
FONDO = None                              # el beige de la pagina de pantalla, tal como lo dibujo Chrome (--ground)
GRIS = (0x6E / 255, 0x62 / 255, 0x5A / 255)       # --taupe, el color del pie
INTER = HERE / "_fonts" / "Inter-Regular.ttf"

JS_MEDIR = r"""() => {
  const pg = document.getElementById('pg');
  const r0 = pg.getBoundingClientRect();
  const pt = v => v * 0.75;
  const caja = e => { const r = e.getBoundingClientRect(); return [pt(r.top - r0.top), pt(r.bottom - r0.top)]; };
  const out = {alto: pt(r0.height), bloques: []};
  for (const e of pg.children) {
    const [top, bottom] = caja(e);
    const b = {tag: e.tagName.toLowerCase(), cls: e.className || '', top, bottom,
               txt: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
               tabla: e.tagName === 'TABLE' || !!e.querySelector('table'),
               dibujo: !!e.querySelector('svg, img') || ['FIGURE', 'IMG', 'SVG'].includes(e.tagName)};
    // una lista larga se puede cortar entre sus puntos, como entre parrafos
    if (e.tagName === 'OL' || e.tagName === 'UL') b.items = [...e.children].map(caja);
    out.bloques.push(b);
  }
  return out;
}"""


def medir():
    """Los bloques de primer nivel de cada pagina de pantalla, como los dibujo build.py (con las columnas
    llenadas por su mismo script)."""
    archivos = sorted(B.OUT.glob("s[0-9][0-9].html"))
    res = []
    with sync_playwright() as pw:
        exe = os.environ.get("PW_CHROMIUM")
        br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pg = br.new_page(viewport={"width": int(B.PAGE_W_PX), "height": 1200})
        for f in archivos:
            pg.goto(f.as_uri())
            pg.wait_for_timeout(450)
            try:
                pg.evaluate("document.fonts.ready")
            except Exception:
                pass
            pg.wait_for_timeout(250)
            pg.evaluate(B.JS_COLFILL)
            m = pg.evaluate(JS_MEDIR)
            m["archivo"] = f.name
            res.append(m)
        br.close()
    return res


def grupos(m):
    """Bloques que van juntos: un titulo con lo que sigue; el rotulo de un cuadro o grafico con el cuadro o
    grafico; un cuadro o grafico con su fuente y sus notas. Una lista larga se puede cortar entre sus puntos."""
    bl = [b for b in m["bloques"] if b["cls"] not in ("runhead", "runfoot") and b["tag"] != "style"
          and b["bottom"] - b["top"] > 0.1]
    out = []
    pegar_al_siguiente = False
    for b in bl:
        previo = out[-1]["partes"][-1] if out else None
        de_cuadro = previo is not None and (previo["tabla"] or previo["dibujo"] or previo["tag"] == "table"
                                            or (previo["tag"] == "p" and previo["cls"].startswith("cap")))
        es_cola = ((b["tag"] == "p" and b["cls"].startswith("cap")) or b["tag"] == "figcaption"
                   or (b["cls"] == "note" and de_cuadro))
        if out and (pegar_al_siguiente or es_cola):
            g = out[-1]
            g["bottom"] = max(g["bottom"], b["bottom"])
            g["partes"].append(b)
        else:
            out.append({"top": b["top"], "bottom": b["bottom"], "partes": [b]})
        titulo = b["tag"] in ("h1", "h2", "h3", "h4") or b["cls"] in ("stand", "igrp", "hairline")
        rotulo = b["cls"].split(" ")[0] == "ex" and not (b["tabla"] or b["dibujo"])
        pegar_al_siguiente = titulo or rotulo
    # una lista que no entra en una hoja se ofrece partida entre sus puntos
    final = []
    for g in out:
        lista = next((p for p in g["partes"] if p.get("items")), None)
        if lista and g["bottom"] - g["top"] > HOJA - ARRIBA_CONT - ABAJO and len(g["partes"]) <= 2:
            items = lista["items"]
            cab = g["top"]
            for k, (t, b) in enumerate(items):
                final.append({"top": cab if k == 0 else t, "bottom": b, "partes": g["partes"] if k == 0 else [],
                              "item": True})
        else:
            final.append(g)
    return final


def cortar(m):
    """Reparte los grupos de una pagina en hojas. Devuelve [(desde, hasta, primera)] en pt de pantalla y la
    lista de grupos que no entran en una hoja."""
    gs = grupos(m)
    hojas, no_entran = [], []
    lim_primera = HOJA - ABAJO
    desde, primera, hasta = 0.0, True, None
    for g in gs:
        alto_hoja = (g["bottom"] - (0 if primera else desde)) + (0 if primera else ARRIBA_CONT)
        if hasta is not None and alto_hoja > lim_primera:
            hojas.append((desde, hasta, primera))
            desde, primera = g["top"], False
        if g["bottom"] - g["top"] + ARRIBA_CONT > lim_primera:
            no_entran.append(g)
        hasta = g["bottom"]
    if hasta is not None:
        hojas.append((desde, hasta, primera))
    return hojas, no_entran


def pie_original(src_pg, m):
    """Donde esta el pie en la pagina de pantalla: la raya de arriba, y desde donde empieza el numero."""
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    num = [s for b in src_pg.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]
           if s["text"].strip().startswith("Página") and s["bbox"][1] > pie["top"] - 2]
    x_num = num[0]["bbox"][0] if num else 520.0
    base = num[0]["origin"][1] if num else pie["bottom"] - 2
    return pie, x_num, base


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


def componer(dst, src, pno, m, desde, hasta, primera, n_hoja, total):
    """Una hoja A4: fondo, encabezado, el pedazo de la pagina de pantalla y el pie con el numero de hoja."""
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    E = ESC
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    hasta = min(hasta + 2, pie["top"] - 0.1) - 2     # el pedazo nunca se lleva la raya del pie
    if primera:
        pg.show_pdf_page(fitz.Rect(0, 0, A4_W, (hasta + 2) * E), src, pno, clip=fitz.Rect(0, 0, 660, hasta + 2))
    else:
        cab = next(b for b in m["bloques"] if b["cls"] == "runhead")
        pg.show_pdf_page(fitz.Rect(0, 0, A4_W, (cab["bottom"] + 2) * E), src, pno,
                         clip=fitz.Rect(0, 0, 660, cab["bottom"] + 2))
        y0 = ARRIBA_CONT
        pg.show_pdf_page(fitz.Rect(0, (y0 - 2) * E, A4_W, (y0 + hasta - desde + 2) * E), src, pno,
                         clip=fitz.Rect(0, desde - 2, 660, hasta + 2))
    # el pie: la raya y el titulo, tal cual; el numero, el de la hoja
    pie, x_num, base = pie_original(src[pno], m)
    dy = HOJA - m_alto_pdf(src, pno, m)        # el pie va al fondo de la hoja, como en pantalla
    raya = fitz.Rect(0, pie["top"] + 0.1, 660, pie["top"] + 0.85)     # solo la raya (0,75 pt), nada de arriba
    izq = fitz.Rect(0, pie["top"] + 0.85, x_num - 2, m_alto_pdf(src, pno, m))
    for r in (raya, izq):
        pg.show_pdf_page(fitz.Rect(r.x0 * E, (r.y0 + dy) * E, r.x1 * E, (r.y1 + dy) * E), src, pno, clip=r)
    escribir(pg, (660 - 45) * E, (base + dy) * E, f"Página {n_hoja} de {total}", 6.4 * E, 0.25 * E)
    return pg


def m_alto_pdf(src, pno, m):
    """El alto de la pagina de pantalla tal como se dibujo (el de la caja, sin el sobrante que agrega Chrome)."""
    return max(m["alto"], 841.89)


def fondo(src):
    """El color del fondo, leido de una pagina de pantalla (Chrome lo dibuja apenas distinto del CSS)."""
    global FONDO
    if FONDO is None:
        px = src[1].get_pixmap(clip=fitz.Rect(2, 2, 6, 6)).pixel(1, 1)
        FONDO = tuple(v / 255 for v in px[:3])
    return FONDO


def portada(dst, src):
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    pg.show_pdf_page(pg.rect, src, 0)
    return pg


def letras_chicas(src):
    """Las letras que, achicadas al 90%, quedan por debajo de 8 pt."""
    tam = {}
    for i, pg in enumerate(src):
        if i == 0:
            continue
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip() and s["size"] * ESC < 8.0:
                        k = round(s["size"], 2)
                        tam[k] = tam.get(k, 0) + len(s["text"].strip())
    return tam


def plan_completo():
    """Mide, corta y numera: [(pagina de pantalla, desde, hasta, primera, numero de hoja)], el total de hojas y
    los bloques que no entran en una hoja."""
    med = medir()
    src = fitz.open(str(PANTALLA))
    assert len(src) == len(med) + 1, (len(src), len(med))
    for i, m in enumerate(med):
        h_pdf = src[i + 1].rect.height
        assert abs(max(m["alto"], 841.89) - h_pdf) < 9, (i + 2, m["alto"], h_pdf)
    hojas, no_entran, n = [], [], 1
    for i, m in enumerate(med):
        hs, ne = cortar(m)
        for (a, b, prim) in hs:
            n += 1
            hojas.append((i + 1, a, b, prim, n))
        no_entran += [(i + 2, g) for g in ne]
    return med, src, hojas, n, no_entran


def lado_a_lado(src, dst, pno_src, desde, hasta, pno_dst, rotulo_izq, rotulo_der, salida, dpi=110):
    """La misma parte de la version de pantalla (izquierda) y la hoja A4 (derecha), a la misma escala."""
    from PIL import Image, ImageDraw, ImageFont
    clip = fitz.Rect(0, max(0, desde - 24), 660, hasta + 24)
    izq = src[pno_src].get_pixmap(dpi=dpi, clip=clip)
    der = dst[pno_dst].get_pixmap(dpi=dpi)
    a = Image.frombytes("RGB", (izq.width, izq.height), izq.samples)
    b = Image.frombytes("RGB", (der.width, der.height), der.samples)
    f = ImageFont.truetype(str(HERE / "_fonts" / "Inter-SemiBold.ttf"), 22)
    m, cab = 40, 60
    lienzo = Image.new("RGB", (a.width + b.width + 3 * m, max(a.height, b.height) + cab + m), "white")
    lienzo.paste(a, (m, cab))
    lienzo.paste(b, (2 * m + a.width, cab))
    d = ImageDraw.Draw(lienzo)
    d.text((m, 18), rotulo_izq, font=f, fill=(124, 46, 35))
    d.text((2 * m + a.width, 18), rotulo_der, font=f, fill=(124, 46, 35))
    lienzo.save(salida)


if __name__ == "__main__":
    if "--muestras" not in sys.argv:
        sys.exit("Por ahora solo --muestras: el A4 completo se arma con el visto bueno de Nick.")
    elegidas = [int(x) for x in sys.argv[sys.argv.index("--muestras") + 1:]] or [78, 26, 57]
    med, src, hojas, total, no_entran = plan_completo()
    print(f"A4: {total} hojas (con la portada)")
    for p, g in no_entran:
        print(f"  !! pag. {p}: un bloque de {g['bottom'] - g['top']:.0f} pt no entra en una hoja "
              f"({(g['bottom'] - g['top']) * ESC:.0f} pt en A4): {g['partes'][0]['txt'][:60]}")
    dst = fitz.open()
    portada(dst, src)
    detalle = []
    for n_hoja in elegidas:
        pno, a, b, prim, n = next(h for h in hojas if h[4] == n_hoja)
        componer(dst, src, pno, med[pno - 1], a, b, prim, n, total)
        detalle.append((pno, a, b, n))
    carpeta = ROOT / "salida" / "muestras_a4"
    carpeta.mkdir(parents=True, exist_ok=True)
    pdf = carpeta / "MUESTRAS_A4.pdf"
    dst.save(str(pdf), garbage=3, deflate=True)
    dst = fitz.open(str(pdf))
    lado_a_lado(src, dst, 0, 0, src[0].rect.height - 24, 0, "PANTALLA · tapa", "A4 · hoja 1 (al 90%)",
                carpeta / "muestra_1_portada.png")
    nombres = ["muestra_2_texto_y_recuadro", "muestra_3_cuadro", "muestra_4_grafico"]
    for k, (pno, a, b, n) in enumerate(detalle):
        lado_a_lado(src, dst, pno, a, b, k + 1, f"PANTALLA · pág. {pno + 1} (la misma parte)",
                    f"A4 · hoja {n} de {total} (al 90%)", carpeta / f"{nombres[k]}.png")
    print("muestras:", pdf, [d[3] for d in detalle])
