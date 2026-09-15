#!/usr/bin/env python3
"""Baja el listado completo del Boletin Oficial de San Isidro (TESI) a CSV/JSONL.

Fuente: https://tesi.sanisidro.gob.ar/boletin?page=N  (30 actos por pagina).
Solo lee el listado publico; no descarga los PDF.
"""
import re, csv, json, html, time, sys, urllib.request, urllib.error
import concurrent.futures as cf

BASE = "https://tesi.sanisidro.gob.ar/boletin?page={}"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
      "Accept-Language": "es-AR,es;q=0.9"}

FILA = re.compile(r"<tr class=\"hover:bg-gray-50[^\"]*\">(.*?)</tr>", re.S)
CELDA = re.compile(r"<td\b[^>]*>(.*?)</td>", re.S)
FECHA = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
SPAN = re.compile(r"<span\b[^>]*>(.*?)</span>", re.S)
PPAR = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S)
PDF = re.compile(r'href="(https://tesi\.sanisidro\.gob\.ar/boletin/pdf/[^"]+)"')


def limpiar(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def bajar(pagina, reintentos=4):
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(BASE.format(pagina), headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if intento == reintentos - 1:
                raise
            time.sleep(2 ** intento)


def parsear(pagina, doc):
    filas = []
    for bruto in FILA.findall(doc):
        celdas = CELDA.findall(bruto)
        if len(celdas) < 6:
            continue
        c_bol, c_tipo, c_obj, c_firma, c_tags, c_pdf = celdas[:6]

        f_pub = FECHA.search(c_bol)
        num = PPAR.findall(c_tipo)
        tipo = SPAN.findall(c_tipo)
        f_firma = FECHA.search(c_firma)
        enlace = PDF.search(c_pdf)

        filas.append({
            "pagina": pagina,
            "boletin": limpiar(SPAN.search(c_bol).group(1)) if SPAN.search(c_bol) else "",
            "fecha_publicacion": f_pub.group(1) if f_pub else "",
            "tipo": limpiar(tipo[0]) if tipo else "",
            "numero": re.sub(r"^Nro\.\s*", "", limpiar(num[0])) if num else "",
            "objeto": limpiar(PPAR.search(c_obj).group(1)) if PPAR.search(c_obj) else limpiar(c_obj),
            "fecha_firma": f_firma.group(1) if f_firma else "",
            "tags": " | ".join(t for t in (limpiar(x) for x in SPAN.findall(c_tags)) if t),
            "pdf": enlace.group(1) if enlace else "",
        })
    return filas


def main():
    ultima = int(sys.argv[1]) if len(sys.argv) > 1 else 516
    salida = sys.argv[2] if len(sys.argv) > 2 else "tesi"
    todo, fallos = [], []

    def tarea(p):
        return p, parsear(p, bajar(p))

    with cf.ThreadPoolExecutor(8) as ex:
        for n, (p, filas) in enumerate(ex.map(tarea, range(1, ultima + 1)), 1):
            if not filas:
                fallos.append(p)
            todo.extend(filas)
            if n % 50 == 0:
                print(f"  {n}/{ultima} paginas, {len(todo)} actos", flush=True)

    # orden estable: por pagina y posicion original
    campos = ["pagina", "boletin", "fecha_publicacion", "tipo", "numero",
              "objeto", "fecha_firma", "tags", "pdf"]
    with open(f"{salida}.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(todo)
    with open(f"{salida}.jsonl", "w", encoding="utf-8") as f:
        for r in todo:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"TOTAL {len(todo)} actos en {ultima} paginas")
    if fallos:
        print(f"PAGINAS VACIAS/FALLIDAS: {fallos}")


if __name__ == "__main__":
    main()
