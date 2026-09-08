# casares-sanisidro-2027

Datos, modelo fiscal y gráficos del programa de gobierno para San Isidro 2027.

## Montar el entorno

```
pip install -r requirements.txt --break-system-packages
```

Las versiones están **fijas a propósito**: matplotlib decide el ancho de cada
glifo, así que con otra versión los 20 exhibits salen distintos aunque el dato
sea el mismo, y el verificador de colisiones acusa colisiones que no existen.
Sin geopandas, `test_censo_zonas.py` no falla: no corre.

## Antes de cualquier push

Los **cinco tests** y los **cinco verificadores de gráficos** tienen que pasar.
El orden importa: `test_parser.py` reescribe los CSV desde los PDF y se lleva
puestas las columnas en pesos constantes, así que va primero y `deflactor.py`
detrás.

```
python3 03_scripts/test_parser.py
python3 03_scripts/deflactor.py
python3 03_scripts/parse_sef.py
python3 03_scripts/modelo.py
python3 03_scripts/test_deflactor.py
python3 03_scripts/test_modelo.py
python3 03_scripts/test_serie_comparable.py
python3 03_scripts/test_censo_zonas.py
python3 03_scripts/generar_todos_los_graficos.py
```

Los cinco verificadores corren dentro del generador, que sale distinto de cero
si salta cualquiera: **paleta**, **desborde**, **colisiones**, **acentos** y
**números escritos a mano**.

El año cero del modelo tiene que seguir reproduciendo la ejecución 2025 con
diferencia cero: **−6.051.064.048**.

## Reglas de datos

- **Cuando existe el conteo, se usa el conteo.** Los porcentajes son para
  mostrar, nunca para calcular otra cosa encima. Derivar de un intermedio ya
  redondeado mete error donde había un dato exacto.
- **Ningún número escrito a mano en un gráfico**, en ninguna parte: título,
  subtítulo, anotación, etiqueta o pie. Todo sale del CSV. El texto de un
  capítulo lo lee alguien; el subtítulo de un gráfico no lo vuelve a mirar
  nadie.

## Dónde está qué

| Carpeta | Qué hay |
|---|---|
| `01_raw/` | fuentes originales, sin tocar |
| `02_clean/` | fuentes parseadas |
| `03_scripts/` | parsers, modelo, gráficos, tests y verificadores |
| `data/` | series y salidas del modelo, en CSV |
| `06_charts/` | los 20 exhibits, PNG a 300 dpi y SVG |

`CORRECCIONES_NUMERICAS.md` registra cada cifra que se corrigió, con su cálculo
y su fuente.
