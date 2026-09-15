#!/usr/bin/env python3
"""Cortes tematicos del listado del Boletin Oficial (TESI).

Entrada:  tesi_listado.jsonl (salida de bajar_tesi.py)
Salida:   los CSV derivados que usan los capitulos 1, 4 y 5.
"""
import json, csv, re, sys, collections

CAMPOS = ["boletin", "fecha_publicacion", "fecha_firma", "tipo", "numero",
          "objeto", "tags", "pdf"]


def cargar(ruta):
    return [json.loads(l) for l in open(ruta, encoding="utf-8")]


def orden(r):
    d = r["fecha_firma"]
    return (d[6:10], d[3:5], d[0:2], r["numero"])


def escribir(ruta, filas, extra=()):
    with open(ruta, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(extra) + CAMPOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(filas, key=orden))
    print(f"  {len(filas):6d}  {ruta}")


def etiquetas(r):
    return {t.strip() for t in r["tags"].split(" | ") if t.strip()}


def main():
    R = cargar(sys.argv[1] if len(sys.argv) > 1 else "tesi_listado.jsonl")
    print(f"total {len(R)}")

    # --- adjudicaciones: tag propio del sistema, o "adjudic" en la referencia
    adj = [r for r in R if "Adjudicación" in etiquetas(r)
           or re.search(r"adjudic", r["objeto"], re.I)]
    escribir("tesi_adjudicaciones.csv", adj)

    # --- lo que el Ejecutivo hace con lo que vota el Concejo
    conc = [r for r in R if r["tipo"] == "Decreto"
            and re.search(r"-HCD-|Honorable Concejo|Ordenanza",
                          r["objeto"] + " " + r["tags"], re.I)]
    for r in conc:
        t = r["objeto"] + " " + r["tags"]
        r["accion"] = ("veto" if re.search(r"\bvetar\b|\bveto\b", t, re.I)
                       and not re.search(r"observar ciertos", r["objeto"], re.I)
                       else "observa_o_suprime" if re.search(r"observ|suprim", t, re.I)
                       else "promulga")
    escribir("tesi_concejo.csv", conc, extra=["accion"])
    print("     ", dict(collections.Counter(r["accion"] for r in conc)))

    # --- residuos e higiene urbana
    rub = re.compile(r"higiene urbana|recolecci[oó]n de residuos|residuos|barrido|"
                     r"limpieza|17/08\b|17/2008|17/14\b|17/2014|CLIBA|ROGGIO|"
                     r"5229|12653|9835", re.I)
    res = [r for r in R if rub.search(r["objeto"])]
    escribir("tesi_residuos.csv", res)

    return conc


if __name__ == "__main__":
    main()
