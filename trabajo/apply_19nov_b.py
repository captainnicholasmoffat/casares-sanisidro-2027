"""Actualización del 19/11/2026, parte B: arreglos de la revisión r8, con lo que decidió el coordinador (la decisión de Nick:
«4 veces lo que paga una casa y 6 si el terreno no está mantenido»).
A. Terrenos sin uso (5.4-r3, Ordenanzas 20 y 21, 3.4, nota del cuadro 20, abogado):
   - San Isidro ya cobra más a los baldíos: Ordenanza Impositiva 2026 (Ordenanza 9415), artículo 2: vivienda 12 por mil,
     baldío 26, inmuebles abandonados 48, construcción inapropiada 96 (PDF oficial de arsi.gob.ar, página 2, abierto el
     19/11/2026). El baldío sube de 26 a 48 por mil (4 veces la vivienda) y a 72 (6 veces) si no está mantenido; las
     categorías que ya pagan 48 o más quedan como están. Pilar y Avellaneda, como antecedentes de que se puede.
   - La tasa se fija como alícuota (4 y 6 veces la de Vivienda), no como «lo que paga una vivienda en una parcela igual».
     Al fondo de la garantía va sólo lo que se cobra por encima de lo que el inmueble pagaría sin la declaración (hoy, 26
     por mil); lo de hoy sigue donde va hoy.
   - Desde cuándo: entra en la ordenanza de tasas de 2029; los declarados en 2028 la pagan desde enero de 2029 y los
     declarados después, desde que se declaran.
   - Pilar: la fórmula está en el artículo 1 (artículos 1 a 3). Avellaneda: fija una alícuota 3,8 veces la de una casa a
     los baldíos y a las obras en construcción; para los ya empadronados, lo de cada mes queda entre lo del mes anterior
     actualizado y un 5% más (Ordenanza 31.322, artículo 1, inciso a).
B. Sueldo de los agentes de tránsito que pasan a la patrulla (5.7, 3.4, cuadro 14, notas del cuadro 14, abogado): el mismo
   paso a pesos de diciembre de 2025 que el sueldo de ingreso de la misma ordenanza (planilla, fila 321;
   trabajo/cuentas_19nov_b.py): de 57,5 a 465,6 M por año (antes 62,3 a 504,7), 1,44 y 4,66 M por agente (antes 1,56 y
   5,05), el 1,4% del gasto de Seguridad (antes 1,6%). El gasto flexible no cambia (51,9 / 48,1 / 44,1). Nadie cobra menos
   que hoy: si una bonificación de tránsito (moto, grúa: 7.547 módulos diarios, Ordenanza 9422, artículo 17, folio 966) es
   más alta que la de la patrulla, la conserva (Ley 14.656, artículo 8).
No agrega párrafos: «orden» no cambia. Se niega a correr dos veces.
Uso: python3 -I trabajo/apply_19nov_b.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if '465,6 millones' in by['5.7']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def _ps(e): return e['texto'].split('\n\n')


def rep(eid, old, new):
    """Cambia old por new en el único párrafo que lo tiene; corre las marcas que siguen y se niega si toca una
    (salvo que el cambio no mueva nada: mismo largo)."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


def parrafo(eid, i, empieza, titulo_viejo, titulo, cuerpo):
    """Rehace el párrafo i entero (título en negrita + cuerpo). La única marca del párrafo es la del título."""
    e = by[eid]; ps = _ps(e)
    assert ps[i].startswith(empieza) and ps[i].startswith(titulo_viejo), (eid, i, ps[i][:80])
    assert e['marcas'][str(i)] == [[0, len(titulo_viejo), 'b']], e['marcas'][str(i)]
    ps[i] = titulo + ' ' + cuerpo; e['marcas'][str(i)] = [[0, len(titulo), 'b']]; e['texto'] = '\n\n'.join(ps)


def cuadro(eid, old, new, k=0):
    c = by[eid]['cuadros'][k]; assert c['texto'].count(old) == 1, (eid, old[:60]); c['texto'] = c['texto'].replace(old, new, 1)


def fuente(eid, old, new):
    e = by[eid]; assert e['fuentes'].count(old) == 1, (eid, old[:60]); e['fuentes'] = e['fuentes'].replace(old, new, 1)


# ============ A · terrenos sin uso ====================================================================================
parrafo('5.4-r3', 3, '3 · Paga más desde que se declara',
        '3 · Paga más desde que se declara, y si no cumple, cada año más.',
        '3 · Paga más desde 2029, y si no cumple, cada año más.',
        'San Isidro ya le cobra a un baldío 26 por mil de su valuación, 2,2 veces lo que a una casa, que paga 12 por mil. '
        'Con la ordenanza de tasas de 2029, cada terreno baldío, edificio en ruinas u obra parada con la obligación de '
        'construir va a pagar 4 veces lo que paga una casa por cada peso de valuación, 48 por mil, y 6 veces, 72 por mil, si '
        'no está mantenido. Quedan como están los inmuebles que ya pagan 48 por mil o más: los abandonados, 48, y los de '
        'construcción inapropiada, 96. Los terrenos declarados en 2028 la pagan desde enero de 2029, y los declarados '
        'después, desde que se declaran. Hay antecedentes de que se puede: Pilar le cobra a un baldío 3,7 veces lo que a una '
        'casa por cada peso de valuación, y 5,6 veces si no está mantenido, y Avellaneda les fija a los baldíos y a las obras '
        'en construcción una alícuota 3,8 veces la de una casa. Si el dueño no cumple el plazo, sobre esa tasa corre el '
        'recargo de la ley: sube cada año durante cinco años, hasta el 50% de la tasa, el máximo que permite, y después sigue '
        'en el máximo hasta que el dueño cumpla. Así, quien no construye termina pagando 6 veces lo de una casa por cada peso '
        'de valuación, o 9 si tampoco mantiene el terreno. Como sube una tasa, la aprueba también la asamblea de concejales y '
        'mayores contribuyentes (Constitución de la Provincia, artículo 193, inciso 2). Lo que se cobre por encima de lo que '
        'esos terrenos pagan hoy, por esa tasa y por el recargo, va a ir al fondo de la garantía de alquiler; lo que pagan hoy '
        'sigue en las cuentas del Municipio. Cuánto suma a lo que cobra el Municipio se va a saber con el registro de terrenos '
        'del primer año, que se arma en la primera ronda (punto 6): hoy no se sabe cuántos terrenos sin uso hay, y por eso '
        'estas cuentas no lo suman.')
fuente('5.4-r3', 'La tasa más alta: Pilar, Ordenanza Impositiva 2026 (Ordenanza 112/2025), artículos 2 y 3:',
       'Lo que cobra hoy San Isidro: Ordenanza Impositiva 2026 (Ordenanza 9415), artículo 2: «Baldío» 26 ‰, «Vivienda» 12 ‰, '
       '«Inmuebles abandonados» 48 ‰ y «Construcción inapropiada» 96 ‰ '
       '(https://arsi.gob.ar/pdf/ordenanzas/Ordenanza_Impositiva_2026-Nro_9415-2025.pdf, página 2, consultado el 19 de '
       'noviembre de 2026). Antecedentes: Pilar, Ordenanza Impositiva 2026 (Ordenanza 112/2025), artículos 1 a 3:')
fuente('5.4-r3', 'y de 1,30 para «A – VIVIENDA»: 3,8 veces, cálculo propio',
       'y de 1,30 para «A – VIVIENDA»: 3,8 veces, cálculo propio; para los inmuebles ya empadronados, lo que paga cada uno '
       'por mes queda entre lo del mes anterior actualizado y un 5% más, según el inciso a del mismo artículo')
rep('anexo-21', 'Desde la declaración del artículo 3, la Ordenanza Impositiva fija para los inmuebles de ese artículo una Tasa por '
    'Alumbrado, Limpieza y Servicios Generales de cuatro (4) veces la que corresponde a una vivienda en una parcela igual, de '
    'la misma superficie y zona, y de seis (6) veces si el inmueble no está mantenido. La reglamentación fija qué se considera '
    'mantenido. El gravamen del artículo 4 se calcula sobre esa tasa. Lo que se recauda por encima de la tasa de esa vivienda '
    'va al fondo de la Ordenanza 20.',
    'Desde la Ordenanza Impositiva del ejercicio 2029, la alícuota de la Tasa por Alumbrado, Limpieza y Servicios Generales '
    'de los inmuebles del artículo 3 es de cuatro (4) veces la de la categoría Vivienda, y de seis (6) veces si el inmueble no '
    'está mantenido, salvo que su categoría ya tenga una alícuota de cuatro (4) veces la de Vivienda o mayor, que no cambia. '
    'Los inmuebles cuya declaración se notificó antes del 1 de enero de 2029 pagan esa alícuota desde esa fecha, y los demás, '
    'desde la notificación. La reglamentación fija qué se considera mantenido. El gravamen del artículo 4 se calcula sobre '
    'esa tasa. Lo que se recauda por encima de lo que el inmueble pagaría sin la declaración del artículo 3 va al fondo de la '
    'Ordenanza 20, y el resto sigue el destino de la tasa.')
rep('anexo-20', 'lo que se cobre por el gravamen y por la diferencia de tasa de los artículos 4 y 5 de la Ordenanza 21 y lo que '
    'asigne el Departamento Ejecutivo',
    'lo que se cobre por el gravamen del artículo 4 de la Ordenanza 21, lo que se cobre por la tasa de su artículo 5 por '
    'encima de lo que el inmueble pagaría sin la declaración, y lo que asigne el Departamento Ejecutivo')
rep('3.4', 'Lo que se cobre de más a los terrenos sin uso va a esa garantía,',
    'Lo que se cobre a los terrenos sin uso por encima de lo que pagan hoy va a esa garantía,')
rep('metodo-notas-3', 'Sólo cambian el gasto de este programa y lo que cobra la tabla nueva.',
    'Sólo cambian el gasto de este programa y lo que cobra la tabla nueva. Lo que se cobre a los terrenos sin uso por '
    'encima de lo que pagan hoy va al fondo de la garantía de alquiler y no entra en estas cuentas, y lo que pagan hoy sigue '
    'en ellas.')
rep('metodo-abogado', 'de 4 veces la de una vivienda en un terreno igual y de 6 si no está mantenido,',
    'de 4 veces la alícuota de una vivienda y de 6 si no está mantenido,')

# ============ B · sueldo de los agentes que pasan a la patrulla =======================================================
rep('5.7', 'Quien pasa no cobra menos: cobra lo mismo que sus compañeros de la patrulla.',
    'Quien pasa cobra lo mismo que sus compañeros de la patrulla.')
rep('5.7', 'cobra la bonificación de la función que ocupa en la patrulla (Ordenanza 9422, artículo 17).',
    'cobra la bonificación de la función que ocupa en la patrulla (Ordenanza 9422, artículo 17). Si hoy cobra por tránsito '
    'más que esa bonificación, como puede pasar con quien maneja una moto o la grúa, que tienen una bonificación propia, '
    'conserva lo que cobra: nadie cobra menos que hoy.')
rep('5.7', 'cuesta de 62,3 a 504,7 millones por año.', 'cuesta de 57,5 a 465,6 millones por año.')
rep('5.7', '1,56 millones más por año cada uno', '1,44 millones más por año cada uno')
rep('5.7', '5,05 millones más cada uno', '4,66 millones más cada uno')
rep('5.7', 'como mucho, el 1,6% de los 32.446 millones', 'como mucho, el 1,4% de los 32.446 millones')
rep('5.7', 'ocupa 62,3 millones del gasto flexible, y 504,7 en el peor caso (3.4)',
    'ocupa 57,5 millones del gasto flexible, y 465,6 en el peor caso (3.4)')
fuente('5.7', 'y artículo 17, compensación del inspector de tránsito y bonificaciones de la Patrulla Municipal y del Cuerpo de '
       'Patrulla a pie',
       'y artículo 17, compensación del inspector de tránsito, bonificaciones de los inspectores de tránsito de la grúa y de '
       'las motos, y de la Patrulla Municipal y del Cuerpo de Patrulla a pie')
fuente('5.7', 'Cálculo propio: trece meses con las cargas del empleador, en pesos de diciembre de 2025.',
       'Cálculo propio: trece meses con las cargas del empleador, en pesos de diciembre de 2025, con el mismo paso que el '
       'sueldo de ingreso de la misma ordenanza (notas del capítulo 4).')
rep('3.4', 'pagarles lo mismo que a sus compañeros, de 62,3 a 504,7 millones por año,',
    'pagarles lo mismo que a sus compañeros, de 57,5 a 465,6 millones por año,')
cuadro('3.4', 'De 62,3 a 504,7 M por año desde los meses 4 a 6', 'De 57,5 a 465,6 M por año desde los meses 4 a 6')
rep('metodo-notas-3', 'lo que se deja de cobrar en multas y los equipos.',
    'lo que se deja de cobrar en multas, el pase de los agentes de tránsito a la patrulla y los equipos.')
rep('metodo-abogado', 'del Cuerpo de Patrulla a pie se suman (Ordenanza 9422, artículo 17), y si la adhesión',
    'del Cuerpo de Patrulla a pie se suman (Ordenanza 9422, artículo 17), si los que pasan cobran también la bonificación '
    'por escalafón de la Secretaría de Seguridad (mismo artículo), cómo conserva lo que cobra quien hoy tiene la '
    'bonificación de la grúa o de las motos de tránsito, y si la adhesión')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
