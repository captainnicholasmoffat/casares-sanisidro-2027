#!/usr/bin/env python3
"""
RECORTE DEL AIRE DE LOS EXHIBITS

    python3 03_scripts/recorte_exhibits.py            # recorta y avisa
    python3 03_scripts/recorte_exhibits.py --contacto # hoja de contacto

matplotlib deja margenes de entre 30 y 550 px alrededor del dibujo, distintos
en cada grafico. Adentro del PDF eso se ve como una figura chica flotando entre
dos margenes de papel, con la de al lado empezando en otro lugar. Este modulo
recorta hasta la tinta y deja un aire parejo, asi que todos los exhibits ocupan
el ancho de la caja de texto y el documento gana densidad sin achicar ni una
letra del grafico.

YA NO RECORTA LA CABECERA. Antes el rotulo, el titulo y la bajada venian
dibujados adentro del PNG y habia que buscarlos y cortarlos: se localizaba la
franja de fondo mas alta del tercio superior y se cortaba por ahi. Funcionaba
mientras el grafico empezaba con aire debajo del titulo, y dejo de funcionar el
dia que los mapas ganaron fondo —agua y partidos vecinos que llegan hasta el
borde—: el corte se fue por el hueco equivocado y la bajada quedo impresa dos
veces, una adentro de la imagen y otra compuesta por el armador.

Ahora el grafico directamente NO dibuja su cabecera (estilo.CABECERA_EXTERNA) y
el armador la compone con la tipografia del documento leyendo 06_charts/
pies.json. Un problema menos, en vez de un arreglo mas.

El recorte NO se versiona: es cache de armado, sale de 06_charts/ y vive en
_recortes/, que esta en .gitignore.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CHARTS = os.path.join(RAIZ, "06_charts")
CACHE = os.path.join(RAIZ, "_recortes")

# El fondo de todos los exhibits es PAPEL. Un pixel se considera tinta si se
# aparta de PAPEL mas que el umbral, que absorbe el ruido del antialiasing.
PAPEL_RGB = (245, 240, 232)      # CREMA, el fondo de todos los exhibits
UMBRAL = 14

# El aire que se le deja al grafico despues de recortar hasta la tinta, en px
# de la imagen original (1600 px de ancho). Cero pegaria el texto al borde.
AIRE = 14


def _tinta(ruta):
    """La mascara de pixeles que no son fondo."""
    from PIL import Image
    import numpy as np
    im = Image.open(ruta).convert("RGB")
    a = np.asarray(im).astype(int)
    return im, np.abs(a - np.array(PAPEL_RGB)).max(axis=2) > UMBRAL


def recortar(nombre_png):
    """Recorta un exhibit y devuelve la ruta del recorte y su proporcion."""
    os.makedirs(CACHE, exist_ok=True)
    origen = os.path.join(CHARTS, nombre_png)
    destino = os.path.join(CACHE, nombre_png)
    if (os.path.exists(destino)
            and os.path.getmtime(destino) > os.path.getmtime(origen)):
        from PIL import Image
        with Image.open(destino) as im:
            return destino, im.width / im.height
    im, tinta = _tinta(origen)
    import numpy as np
    cols = np.flatnonzero(tinta.any(axis=0))
    filas = np.flatnonzero(tinta.any(axis=1))
    if not len(cols) or not len(filas):                   # pragma: no cover
        raise RuntimeError("el exhibit %s salio en blanco" % nombre_png)
    caja = (max(0, int(cols[0]) - AIRE),
            max(0, int(filas[0]) - AIRE),
            min(im.width, int(cols[-1]) + 1 + AIRE),
            min(im.height, int(filas[-1]) + 1 + AIRE))
    rec = im.crop(caja)
    rec.save(destino)
    return destino, rec.width / rec.height


def _contacto():
    """Una hoja de contacto con los 20 recortes, para mirarlos de una."""
    from PIL import Image
    import math
    fs = sorted(f for f in os.listdir(CHARTS)
                if f.startswith("EXHIBIT") and f.endswith(".png"))
    tiles = []
    for f in fs:
        ruta, _ = recortar(f)
        im = Image.open(ruta)
        escala = 430 / im.width
        tiles.append(im.resize((430, int(im.height * escala))))
    filas = math.ceil(len(tiles) / 4)
    altos = [max(t.height for t in tiles[i * 4:(i + 1) * 4])
             for i in range(filas)]
    hoja = Image.new("RGB", (430 * 4, sum(altos)), (255, 255, 255))
    y = 0
    for r in range(filas):
        for c, t in enumerate(tiles[r * 4:(r + 1) * 4]):
            hoja.paste(t, (c * 430, y))
        y += altos[r]
    salida = os.path.join(CACHE, "_contacto.png")
    hoja.save(salida)
    print("hoja de contacto: %s" % salida)


def main():
    if "--contacto" in sys.argv:
        _contacto()
        return 0
    for f in sorted(os.listdir(CHARTS)):
        if f.startswith("EXHIBIT") and f.endswith(".png"):
            _, prop = recortar(f)
            print("  %-46s proporcion %.2f" % (f, prop))
    return 0


if __name__ == "__main__":
    sys.exit(main())
