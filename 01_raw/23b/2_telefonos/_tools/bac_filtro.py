# Lee award.csv de Buenos Aires Compras (OCDS) por stdin y guarda sólo filas 2025-2026 con palabras clave
import csv, sys, re, unicodedata
csv.field_size_limit(10**9)
out = open(sys.argv[1], "w", newline="")
w = csv.writer(out)
def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
pat = re.compile(r"TELEFONO CELULAR|TELEFONOS CELULARES|SMARTPHONE|TELEFONO MOVIL|EQUIPO CELULAR|EQUIPOS CELULARES|TELEFONIA MOVIL|TELEFONIA CELULAR|DATOS MOVILES|ABONO.{0,40}(CELULAR|MOVIL)|DISCO RIGIDO|DISCOS RIGIDOS|DISCO DURO|HDD|ALMACENAMIENTO|STORAGE|\bNAS\b|CAMARA CORPORAL|CAMARAS CORPORALES|BODY ?CAM|POWER ?BANK|BATERIA EXTERNA|CARGADOR PORTATIL|ARNES|SOPORTE.{0,20}(CELULAR|TELEFONO)")
r = csv.reader(sys.stdin)
hdr = next(r); w.writerow(hdr)
i_date = hdr.index("awards/0/date")
n = k = 0
for row in r:
    n += 1
    if len(row) < len(hdr): continue
    if not (row[i_date].startswith("2025") or row[i_date].startswith("2026")): continue
    txt = norm(" ".join(row[2:4] + row[12:13]))
    if pat.search(txt):
        w.writerow(row); k += 1
print(n, k, file=sys.stderr)
