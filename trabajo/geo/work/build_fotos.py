# -*- coding: utf-8 -*-
"""Convierte las fotos aprobadas (assets/doc/f_*.jpg de c462fcf) a WebP y arma fotos.json con el
epigrafe exacto y el apartado donde aparece cada una en el programa final.

Uso: python3 -I build_fotos.py <carpeta fotos> <sections.json> <paginas_pdf.json> <pj.txt> <carpeta salida>
"""
import html, json, os, re, sys
from PIL import Image

FOTOS, SECS, PAGS, PJ, OUT = sys.argv[1:6]
EXCLUIDAS = {
    "f_plaza": "«Plaza de barrio, un sábado. Ilustración.» Se sacó del programa (corrección de lectura del A4, 10 de octubre).",
    "f_mesa": "«Trabajo sobre el mapa del partido. Ilustración.» Se sacó del programa (corrección de lectura del A4, 10 de octubre).",
}
secs = json.load(open(SECS, encoding="utf-8"))
pags = json.load(open(PAGS, encoding="utf-8"))
pj = re.sub(r"\s+", " ", open(PJ, encoding="utf-8").read())

def limpio(t):
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t).replace("\xa0", " ")).strip()

# recorrer el programa en orden: capitulo (h1), apartado (h2 numerado), subtitulo (h3) y fotos
TOK = re.compile(r'<h1[^>]*>(?P<h1>.*?)</h1>|<h2[^>]*>(?P<h2>.*?)</h2>|<h3[^>]*>(?P<h3>.*?)</h3>'
                 r'|<div class="duo"><figure><img src="asset:(?P<d1>f_\w+)\.jpg"[^>]*></figure><figure><img src="asset:(?P<d2>f_\w+)\.jpg"[^>]*></figure></div>\s*<figcaption[^>]*>(?P<dcap>.*?)</figcaption>'
                 r'|<figure><img src="asset:(?P<f>f_\w+)\.jpg" alt=""(?: style="object-position:center (?P<pos>[\d.]+%)")?><figcaption>(?P<cap>.*?)</figcaption></figure>', re.S)
en_prog = {}
cap_label, cap_id = None, None


def encabezado(raw):
    """(numero, titulo) de un h1/h2, sin las etiquetas de color (Fondos nuevos, Reasignacion...)."""
    raw = re.sub(r'<span class="tag[^"]*">.*?</span>', "", raw, flags=re.S)
    m = re.match(r'\s*<span class="n">([^<]+)</span>(.*)$', raw, re.S)
    return (limpio(m.group(1)), limpio(m.group(2))) if m else (None, limpio(raw))


apart, sub = None, None          # las paginas de continuacion siguen el apartado de la anterior
for s in secs:
    h = s["html"]
    pend = []
    for m in TOK.finditer(h):
        if m.group("h1") is not None:
            n, t = encabezado(m.group("h1"))
            cap_label, cap_id = (f"Capítulo {n} · {t}", n) if n else (t, None)
            for e in pend:                       # foto de apertura: va antes del h1 de su capitulo
                e["apartado"] = f"{cap_label} (apertura del capítulo)"
                if cap_id:
                    e["apartado_id"] = cap_id
            pend, apart, sub = [], None, None
            continue
        if m.group("h2") is not None:
            apart, sub = encabezado(m.group("h2")), None
            continue
        if m.group("h3") is not None:
            sub = limpio(m.group("h3"))
            continue
        if m.group("d1"):
            items, cap, par = [(m.group("d1"), None), (m.group("d2"), None)], limpio(m.group("dcap")), True
        else:
            items, cap, par = [(m.group("f"), m.group("pos"))], limpio(m.group("cap")), False
        for nombre, pos in items:
            e = {"archivo": nombre, "epigrafe": cap, "pagina_programa": s["id"]}
            if par:
                e["par_con"] = [x for x, _ in items if x != nombre][0]
            if pos:
                e["encuadre_vertical_en_el_programa"] = pos
            if re.search(r"<h1", h[m.end():]) and not re.search(r"<h1", h[:m.start()]):
                pend.append(e)
            elif apart is not None:
                n, t = apart
                e["apartado"] = f"{n} {t}" if n else f"{cap_label} · {t}"
                if n:
                    e["apartado_id"] = n
                if sub:
                    e["subtitulo"] = sub
            else:
                e["apartado"] = cap_label
            en_prog[nombre] = e
    assert not pend, pend

os.makedirs(OUT, exist_ok=True)
lista, problemas = [], []
for f in sorted(os.listdir(FOTOS)):
    if not (f.startswith("f_") and f.endswith(".jpg")):
        continue
    nombre = f[:-4]
    if nombre in EXCLUIDAS:
        continue
    im = Image.open(os.path.join(FOTOS, f)).convert("RGB")
    w, h = im.size
    salida = {}
    for ancho, cal in ((1600, 78), (800, 72)):
        alto = round(h * ancho / w)
        r = im.resize((ancho, alto), Image.LANCZOS)
        ruta = os.path.join(OUT, f"{nombre}-{ancho}.webp")
        r.save(ruta, "WEBP", quality=cal, method=6)
        salida[str(ancho)] = {"archivo": f"{nombre}-{ancho}.webp", "ancho": ancho, "alto": alto, "calidad": cal,
                              "bytes": os.path.getsize(ruta)}
    e = {"archivo": nombre, "original": f, "original_px": [w, h],
         "webp_1600": salida["1600"], "webp_800": salida["800"]}
    if nombre in en_prog:
        p = en_prog[nombre]
        e.update({"en_programa": True, "epigrafe": p["epigrafe"], "apartado": p.get("apartado")})
        for k in ("apartado_id", "subtitulo", "par_con", "encuadre_vertical_en_el_programa", "pagina_programa"):
            if k in p:
                e[k] = p[k]
        if nombre in pags:
            e["pagina_pdf_pantalla"] = pags[nombre]
        if p["epigrafe"] not in pj:
            problemas.append(f"{nombre}: el epígrafe no está en el PDF de pantalla")
        if nombre not in pags:
            problemas.append(f"{nombre}: no se encontró en el PDF de pantalla")
    else:
        e.update({"en_programa": False, "epigrafe": None, "apartado": None})
        if nombre in pags:
            problemas.append(f"{nombre}: no está en el HTML pero sí en el PDF")
    lista.append(e)

orden = {n: i for i, n in enumerate(en_prog)}
lista.sort(key=lambda e: (not e["en_programa"], orden.get(e["archivo"], 999), e["archivo"]))
doc = {
    "descripcion": "Fotos del programa «San Isidro 2027» (versión final, c462fcf), en WebP. Todas son ilustraciones, como dice cada epígrafe.",
    "convenciones": "epigrafe: el texto exacto que lleva la foto en el programa. apartado: dónde aparece. pagina_pdf_pantalla: página del PDF de pantalla final. en_programa: false si la foto está en el repositorio pero no en el programa final.",
    "fotos": lista,
    "excluidas": [{"archivo": k, "motivo": v} for k, v in EXCLUIDAS.items()],
}
json.dump(doc, open(os.path.join(OUT, "fotos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fotos:", len(lista), "en programa:", sum(e["en_programa"] for e in lista), "problemas:", problemas)
