#!/usr/bin/env python3
"""
RECORTE DE LA CABECERA DE LOS EXHIBITS

    python3 03_scripts/recorte_exhibits.py        # recorta y avisa donde corto

Los PNG de 06_charts traen la cabecera dibujada adentro: el rotulo "EXHIBIT NN",
el titulo y la bajada los pinta matplotlib con estilo.marco(). Eso servia cuando
el grafico se miraba suelto. Adentro del PDF no sirve:

  - el titulo se escala con la imagen, asi que su cuerpo depende de cuanto mida
    el grafico en la pagina y no de la jerarquia del documento;
  - queda en el mapa de bits, o sea que no se puede buscar ni copiar;
  - y compite con el titulo de seccion, que si es tipografia del documento.

Asi que el armador recorta la cabecera y la vuelve a componer con las fuentes y
los cuerpos del PDF, leyendo el texto de 06_charts/pies.json, que es donde ya
estaba. NO SE CAMBIA NI UNA PALABRA: el mismo rotulo, el mismo titulo y la misma
bajada que el PNG traia dibujados.

--------------------------------------------------------------------------
COMO ENCUENTRA EL CORTE
--------------------------------------------------------------------------
Por el hueco. estilo.marco() dibuja la cabecera arriba y despues deja un aire
antes del area del grafico, y ese aire es la franja de fondo mas alta de todo el
tercio superior de la imagen. El recorte busca las franjas de filas sin tinta en
el 45% de arriba y corta por el medio de la mas alta.

No se recorta por una altura fija porque la cabecera no mide siempre lo mismo:
el titulo envuelve en una o dos lineas segun su largo y hay exhibits sin bajada.
Una altura fija le comia el grafico a unos y le dejaba media cabecera a otros.

VERIFICADO A OJO sobre los 20 exhibits: ninguno pierde contenido del grafico y
ninguno conserva un resto de la cabecera. Si se agrega un exhibit nuevo, mirar
el recorte antes de darlo por bueno — para eso esta la hoja de contacto:

    python3 03_scripts/recorte_exhibits.py --contacto

--------------------------------------------------------------------------
El recorte NO se versiona. Es cache de armado, se rehace en cada corrida y sale
de 06_charts/, que es la fuente. Vive en _recortes/ y esta en .gitignore.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CHARTS = os.path.join(RAIZ, "06_charts")
CACHE = os.path.join(RAIZ, "_recortes")

# El fondo de todos los exhibits es PAPEL. Un pixel se considera tinta si se
# aparta de PAPEL mas que el umbral, que absorbe el ruido del antialiasing.
PAPEL_RGB = (250, 248, 244)
UMBRAL = 14

# Donde buscar el hueco. La cabecera nunca pasa de aca; mas abajo lo que hay son
# huecos del propio grafico y cortar por uno de esos le comeria una serie.
ZONA = 0.45

# El aire que se le deja al grafico despues de recortar hasta la tinta, en px
# de la imagen original (1600 px de ancho). Cero pegaria el texto al borde.
AIRE = 14


def _corte(ruta):
    """La fila por donde termina la cabecera y empieza el grafico."""
    from PIL import Image
    import numpy as np
    im = Image.open(ruta).convert("RGB")
    a = np.asarray(im).astype(int)
    tinta = np.abs(a - np.array(PAPEL_RGB)).max(axis=2) > UMBRAL
    tinta_por_fila = tinta.any(axis=1)
    alto = len(tinta_por_fila)
    limite = int(alto * ZONA)
    huecos = []
    i = int(np.flatnonzero(tinta_por_fila)[0])
    while i < limite:
        if not tinta_por_fila[i]:
            j = i
            while j < alto and not tinta_por_fila[j]:
                j += 1
            huecos.append((j - i, i, j))
            i = j
        else:
            i += 1
    if not huecos:                                        # pragma: no cover
        raise RuntimeError("sin hueco de cabecera en %s" % ruta)
    _, desde, hasta = max(huecos)
    return im, (desde + hasta) // 2, tinta


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
    im, fila, tinta = _corte(origen)
    # Y TAMBIEN SE LE SACA EL AIRE DE LOS COSTADOS Y DE ABAJO. matplotlib deja
    # margenes que van de 30 a 550 px segun el grafico: adentro del PDF eso se
    # ve como un grafico chico flotando entre dos margenes de papel, con la
    # figura de al lado empezando en otro lugar. Recortando hasta la tinta, con
    # un aire parejo, todos los exhibits ocupan el ancho de la caja y el
    # documento gana densidad sin achicar ni una letra del grafico.
    import numpy as np
    resto = tinta[fila:]
    cols = np.flatnonzero(resto.any(axis=0))
    filas = np.flatnonzero(resto.any(axis=1))
    izq = max(0, int(cols[0]) - AIRE)
    der = min(im.width, int(cols[-1]) + 1 + AIRE)
    abajo = min(im.height, fila + int(filas[-1]) + 1 + AIRE)
    rec = im.crop((izq, fila, der, abajo))
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
