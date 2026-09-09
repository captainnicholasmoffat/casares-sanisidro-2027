#!/usr/bin/env python3
"""
VERIFICADOR DE MAQUETACION — sobre el PDF ya armado

    python3 03_scripts/verificar_maqueta.py
    -> 0 si el PDF esta bien maquetado, 1 si no.

Los siete verificadores de graficos miran una figura antes de existir el PDF.
Este mira el PDF armado, que es lo unico que el lector ve, y busca las cuatro
cosas que un rediseno rompe cada vez que se toca:

  1. un pendiente colado a traves del marcador de corte
  2. un titulo al pie de su COLUMNA sin nada debajo
  3. una linea suelta arriba de una columna, resto del parrafo anterior
  4. una pagina que termina mucho antes del pie

--------------------------------------------------------------------------
POR QUE LA METRICA DE LLENADO ANTERIOR NO SERVIA
--------------------------------------------------------------------------
Medir "donde termina el ultimo elemento de la pagina" da 97% sobre un documento
fragmentado: con dos columnas alcanza con que UNA llegue al pie para que la
pagina puntue lleno, aunque la otra este a la mitad. Con esa metrica el
documento dio 44 paginas al 97% y estaba partido en filas de columnas cortas.

Aca se mide POR COLUMNA. Una pagina esta bien llena cuando las dos columnas
llegan cerca del pie, o cuando la que no llega es la ultima de su capitulo.

Los elementos que cruzan las dos columnas se excluyen del calculo por columna:
un exhibit ancho aparece en las dos y las hace puntuar alto sin decir nada sobre
el texto.
"""

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PDF = os.path.join(RAIZ, "PROGRAMA_SAN_ISIDRO_2027.pdf")

MARCADOR = "NO VA AL PDF"
CORRIDO = {"Programa", "de", "gobierno", "·", "San", "Isidro", "2027",
           "CAPÍTULO", "INTRODUCCIÓN", "ANEXO", "DE", "FUENTES", "LA", "EL",
           "QUÉ", "CONTRA", "GESTIÓN,", "MEDIDA", "PLATA", "MECANISMO",
           "DIAGNÓSTICO", "HACEMOS", "EN", "CADA", "ÁREA", "QUEREMOS", "QUE",
           "NOS", "MIDAN"}

CUERPO_TITULO = 11.0      # pt: por encima de esto es un titulo
MIN_DEBAJO = 8            # palabras que un titulo necesita debajo, en su columna
MIN_LLENADO = 0.80        # de la altura util, por columna
MIN_LINEA_SUELTA = 4      # palabras: menos que esto arriba de una columna es viuda


def _es_remate(linea):
    """Un remate o una cifra destacada NO es un titulo, aunque mida lo mismo.

    Los dos van en cuerpo grande y los dos cierran una seccion, asi que estar al
    pie de la pagina sin nada debajo es su lugar y no un defecto. Un titulo
    anuncia lo que viene; un remate cierra lo que pasó. Se distinguen por como
    terminan: el remate es una oracion y termina en punto.
    """
    texto = " ".join(w["text"] for w in linea).strip()
    return texto.endswith((".", "!", "?", "”", '"'))


def _lineas(ws, tol=2.6):
    """Agrupa palabras en lineas visuales, ordenadas de arriba a abajo."""
    ls = []
    for w in sorted(ws, key=lambda x: (round(x["top"], 1), x["x0"])):
        if ls and abs(ls[-1][0]["top"] - w["top"]) <= tol:
            ls[-1].append(w)
        else:
            ls.append([w])
    return ls


def _columna_de_linea(linea, mitad):
    """0 izquierda, 1 derecha, None si la LINEA cruza las dos columnas.

    Se clasifica la linea entera y no cada palabra: un titulo de capitulo o un
    exhibit que cruza tiene palabras a los dos lados, y palabra por palabra las
    de la derecha se contaban como columna derecha. Asi la bajada del capitulo 1
    aparecia como 'linea suelta arriba de la columna 2', que es un falso
    positivo — y un verificador ruidoso ensena a ignorar la suite.
    """
    x0 = min(w["x0"] for w in linea)
    x1 = max(w["x1"] for w in linea)
    if x1 <= mitad + 4:
        return 0
    if x0 >= mitad - 4:
        return 1
    return None


def _arranques(pdf):
    """Paginas donde empieza una seccion, por el cuerpo del titulo.

    No sirve buscar la palabra CAPITULO: el encabezado corrido la repite en
    todas las paginas. El h1 se reconoce por su cuerpo, que ningun otro texto
    del documento usa.
    """
    ini = set()
    for i, p in enumerate(pdf.pages, 1):
        if any(w.get("size", 0) > 16
               for w in (p.extract_words(extra_attrs=["size"]) or [])):
            ini.add(i)
    return ini


def revisar(ruta=PDF):
    import pdfplumber

    fallas = []
    with pdfplumber.open(ruta) as pdf:
        total = len(pdf.pages)
        arranques = _arranques(pdf)
        # La ultima pagina de un capitulo termina donde termina el texto: cada
        # capitulo empieza en pagina nueva. No es un hueco de maquetacion.
        cierres = {n - 1 for n in arranques}
        for i, p in enumerate(pdf.pages, 1):
            txt = p.extract_text() or ""
            if MARCADOR in txt or "Pendientes de este" in txt:
                fallas.append("p%d: se colo texto de pendientes" % i)
            if i < 3 or i == total:       # tapa, indice y ultima
                continue

            ws = [w for w in (p.extract_words(extra_attrs=["size"]) or [])
                  if w["text"] not in CORRIDO
                  and not re.fullmatch(r"\d+", w["text"])]
            if not ws:
                continue
            mitad = p.width / 2
            util = p.height * 0.93
            lineas = _lineas(ws)
            cols = {0: [], 1: []}
            cruzan = []
            for l in lineas:
                c = _columna_de_linea(l, mitad)
                (cruzan if c is None else cols[c]).append(l)

            # el pie mas bajo de la pagina, cuente en la columna que cuente
            def fondo(grupos):
                return max((max(w["bottom"] for w in l) for l in grupos),
                           default=0)
            fin_pagina = max(fondo(cols[0]), fondo(cols[1]), fondo(cruzan),
                             max([im["bottom"] for im in (p.images or [])
                                  if im["bottom"] <= util] or [0]))

            # --- 2. titulo al pie de su columna ---
            for c in (0, 1):
                tits = [l for l in cols[c]
                        if max(w.get("size", 0) for w in l) > CUERPO_TITULO
                        and not _es_remate(l)]
                if not tits:
                    continue
                y = max(w["top"] for w in tits[-1])
                debajo = sum(len(l) for l in cols[c]
                             if min(w["top"] for w in l) > y + 3)
                # un titulo al final de su columna esta bien si la pagina sigue
                # abajo con algo que cruza (un exhibit, una tabla ancha)
                sigue_cruzando = any(min(w["top"] for w in l) > y + 3
                                     for l in cruzan)
                if debajo < MIN_DEBAJO and not sigue_cruzando:
                    fallas.append("p%d col%d: titulo al pie sin cuerpo debajo (%r)"
                                  % (i, c + 1,
                                     " ".join(w["text"] for w in tits[-1])[:44]))

            # --- 3. linea suelta arriba de la columna derecha ---
            if cols[1] and len(cols[1]) > 1:
                primera, segunda = cols[1][0], cols[1][1]
                hueco = min(w["top"] for w in segunda) - min(w["top"] for w in primera)
                if len(primera) < MIN_LINEA_SUELTA and hueco > 14:
                    fallas.append("p%d col2: arranca con una linea suelta (%r)"
                                  % (i, " ".join(w["text"] for w in primera)[:40]))

            # --- 4. llenado, POR COLUMNA ---
            for c in (0, 1):
                if not cols[c]:
                    continue
                fin = max(fondo([l]) for l in cols[c])
                # si debajo de esa columna hay algo que cruza, la columna no
                # esta vacia: termina donde empieza el elemento ancho
                bajo = [l for l in cruzan if min(w["top"] for w in l) > fin]
                if bajo:
                    continue
                if fin_pagina / util >= MIN_LLENADO and fin / util < MIN_LLENADO:
                    fallas.append("p%d col%d: llena el %.0f%% y la otra llega al pie"
                                  % (i, c + 1, 100 * fin / util))
            if fin_pagina / util < MIN_LLENADO and i not in cierres:
                fallas.append("p%d: la pagina termina al %.0f%% de la altura util"
                              % (i, 100 * fin_pagina / util))
    return fallas, total


def main():
    if not os.path.exists(PDF):
        print("no existe %s — corré antes armar_pdf.py" % PDF)
        return 1
    fallas, total = revisar()
    print("=" * 74)
    print("VERIFICADOR DE MAQUETACION — %d páginas" % total)
    print("=" * 74)
    if not fallas:
        print("  Sin pendientes colados, sin títulos al pie de columna, sin "
              "líneas sueltas\n  y ninguna columna por debajo del %d%% de "
              "llenado." % (MIN_LLENADO * 100))
        return 0
    print("  %d problema(s):" % len(fallas))
    for f in fallas:
        print("   ", f)
    return 1


if __name__ == "__main__":
    sys.exit(main())
