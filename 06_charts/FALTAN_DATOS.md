# Gráficos que faltaron, y cómo se cerraron

**Ya no falta ninguno: están los veinte.** Este archivo queda como el registro
de los tres datos que faltaron, qué se hizo para conseguirlos y qué quedó
pendiente de validar. Ninguno se rellenó con números aproximados ni con una
fuente distinta de la que pedía: si el dato no estaba, el gráfico no existía.

Fecha: **2026-09-07**.

---

## EXHIBIT 05 — San Isidro contra la mediana provincial

**Faltaba:** la ejecución presupuestaria de los otros 134 municipios. El repo
tenía transferencias por municipio, que es lo que la Provincia les **manda**, no
lo que cada municipio **gasta**.

**Se cerró** con `01_raw/rafam_2025_106_municipios.csv`, que Nick capturó el
2026-09-03 de `la-verdadera-pba.pages.dev` (106 informes municipales, parseados
con pdfplumber).

`03_scripts/parse_rafam.py` no le cree a las columnas `pct_` de la planilla:
recalcula los dos porcentajes desde los importes devengados y **falla** si
alguno difiere más de 0,05 puntos del declarado. Los 106 coinciden.

| | San Isidro | Mediana de los 106 | Puesto |
|---|---:|---:|---|
| Personal sobre gasto devengado | 34,41% | 50,74% | 20 de 106 (1 = menor peso) |
| Obra pública sobre gasto devengado | 17,83% | 5,44% | 4 de 106 (1 = mayor inversión) |

Las medianas son el promedio de los dos valores centrales, que con 106 casos es
la definición. Tomando sólo el valor 54 dan 50,85% y 5,46%. Los puestos no se
mueven con ninguna de las dos.

> **Lo que queda pendiente.** La Verdadera PBA procesa datos oficiales de RAFAM
> pero **no es la fuente oficial**. El dato de San Isidro está validado al millón
> contra la ejecución 2025 del propio Municipio en las siete categorías del
> gasto por objeto. **Los otros 105 no.** Antes de imprimir, cualquier cifra de
> esos 105 que se cite en el documento hay que validarla contra RAFAM o SIMCo.
> La advertencia está escrita en `01_raw/NO_DESCARGADOS.txt`.

---

## EXHIBIT 19 — Las ocho medidas de transparencia

**Faltaba:** el listado de las ocho medidas y el estado de cada una. No era un
dato público que hubiera que ir a buscar a un organismo: es una **definición del
propio programa de gobierno**. Las ocho medidas había que escribirlas, no
parsearlas.

**Se cerró** con `data/transparencia_medidas.csv`, escrito por Nick el
2026-09-07. Ocho filas: medida, estado actual y contra qué se verificó.

El estado de cada una **sí** es verificable, y buena parte de la evidencia ya
estaba en el repo: `01_raw/NO_DESCARGADOS.txt` la registró en su momento, al
intentar descargar las secciones que no existen y el portal de datos que
devuelve 504.

El CSV va en ASCII como todos los datos del repo; los acentos se ponen **al
mostrar**, con `estilo.nombre_medida()`, `nombre_estado()` y
`nombre_evidencia()`. Misma técnica que `nombre_funcion()` y `zona_bonita()`.

> **El EXHIBIT 05 ya no falta.** Nick subió
> `01_raw/rafam_2025_106_municipios.csv` —ejecución 2025 de 106 de los 135
> municipios bonaerenses, del RAFAM provincial— el 7 de septiembre de 2026. El
> gráfico está hecho. Siguen faltando 29 municipios y el gráfico lo dice: no se
> estimó ninguno. Lo que queda pendiente es **registrar la URL de origen de esa
> planilla** en `01_raw/NO_DESCARGADOS.txt`; hoy figura como aportada.

---

## Un tercer dato que faltaba y ya no falta

El **EXHIBIT 13** (reparto de la partida vecinal por zona) necesitaba una regla
de reparto que no estaba en el repo. Ya está, escrita y publicada en
`03_scripts/graficos_cap4.py`, con la salida en
`data/reparto_vecinal_por_zona.csv`:

```
POOL = bienes de uso devengados 2025 x 0,50 = 28.907.854.675,13

indicadores = [pct_nbi, pct_sin_cloaca, pct_sin_gas_red, pct_hacinamiento]
para cada indicador k:  max_k = el mayor valor entre las seis zonas
need_zona = promedio( valor_zona[k] / max_k )  sobre los cuatro

peso_zona = 0,5 x (poblacion_zona / 295.978)
          + 0,5 x (need_zona / suma_need)
monto     = POOL x peso_zona
```

**Por qué se normaliza cada indicador por su propio máximo:** sin eso, "sin gas
de red" —que llega al 41,5%— aplastaría a "NBI" —que llega al 5,8%— y el índice
sería en los hechos un solo indicador disfrazado de cuatro.

**Por qué la población suma 295.978 y no 297.282:** son las personas en
viviendas **particulares**. Los 1.304 restantes viven en viviendas colectivas,
que el Censo no publica por radio y por lo tanto no se pueden asignar a ninguna
zona.

Reproduce los dos valores a etiquetar al centavo: **Beccar 136.996,14** y
**Martínez 72.446,13**.

> Antes de tener esta fórmula se había implementado una aproximación con un solo
> indicador de necesidad (cantidad de hogares con NBI). Daba la proporción
> correcta entre las zonas pero los niveles quedaban 4,8% abajo. Queda anotado
> porque explica por qué un método puede ordenar bien y aun así estar mal: el
> orden lo daba cualquiera de los dos, los niveles sólo la fórmula completa.

---

## Cómo se completan

El gráfico faltante ya está declarado en
`03_scripts/generar_todos_los_graficos.py`, en el diccionario `SIN_DATO`.
Cuando aparezca el dato:

1. Se escribe la función del exhibit en el módulo del capítulo que corresponda.
2. Se la agrega a la lista `EXHIBITS`.
3. Se la saca de `SIN_DATO`.

El orquestador lo cuenta y le corre los cuatro verificadores como a los demás.
Así se completó el EXHIBIT 05: tres pasos, sin tocar nada más.
