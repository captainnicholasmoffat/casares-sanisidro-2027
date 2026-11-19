"""Actualización del 19/11/2026, parte A: las dos últimas decisiones de Nick (19/11).
A. Los agentes de tránsito que pasan a la patrulla (de 40 a 100, meses 4 a 6) cobran lo mismo que sus compañeros de la
   patrulla, con el presupuesto de Seguridad. Ordenanza 9422, artículo 17: compensación del inspector de tránsito 31.694
   módulos por mes; bonificación de la Patrulla Municipal 126.416; del Cuerpo de Patrulla a pie 212.153 (la ordenanza no
   dice si se suman). Diferencia por agente y por año, 13 meses con cargas, a pesos de diciembre de 2025: 1,56 M o 5,05 M.
   Rango: 62,3 M por año (40 agentes, la menor) a 504,7 M (100, la mayor). Planilla, bloque AI (trabajo/cuentas_19nov.py):
   como todo lo que un área paga con su presupuesto, ocupa gasto flexible; el mínimo en la cuenta de base y el resto en el
   peor caso: 51,8% → 51,9% ocupado, 48,2% → 48,1% libre, 44,7% → 44,1% en el peor caso. Cambia en 5.7, 3.4 (texto y
   cuadro 14), cuadro 42, 3, 5.1, 6.5, glosario, método y la nota del abogado. 5.9 no cambia: sus costos no dependen del sueldo.
B. Terrenos sin uso: desde que se declara, la tasa es 4 veces la de una casa en un terreno igual, y 6 veces si no está
   mantenido; el recargo de la Ley 14.449 (hasta 50%) va encima para quien no construye en plazo; lo que se cobre de más
   va al fondo de la garantía de alquiler. Precedentes: Pilar (Ordenanza 112/2025, artículos 2 y 3: 3,7 y 5,6 veces) y
   Avellaneda (Ordenanza 31.322, artículo 1: 3,8 veces), abiertos el 19/11/2026. Cuántos terrenos hay no se sabe: se va a
   saber con el registro de terrenos del primer año. Cambia en 5.4-r3, Ordenanza 21 (artículo 5), 3.4 y la nota del
   abogado. La Ordenanza 20 no cambia: ya manda al fondo «la diferencia de tasa» del artículo 5 de la 21.
No agrega párrafos: «orden» no cambia. Se niega a correr dos veces.
Uso: python3 -I trabajo/apply_19nov_a.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if '504,7 millones' in by['5.7']['texto']:
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


def cuadro(eid, old, new, k=0):
    c = by[eid]['cuadros'][k]; assert c['texto'].count(old) == 1, (eid, old[:60]); c['texto'] = c['texto'].replace(old, new, 1)


def fuente(eid, old, new):
    e = by[eid]; assert e['fuentes'].count(old) == 1, (eid, old[:60]); e['fuentes'] = e['fuentes'].replace(old, new, 1)


# ============ A · los agentes que pasan a la patrulla cobran como sus compañeros ======================================
rep('5.7', 'Por eso, quien pasa no cobra menos que hoy.',
    'Quien pasa no cobra menos: cobra lo mismo que sus compañeros de la patrulla. Deja la compensación de inspector de '
    'tránsito y cobra la bonificación de la función que ocupa en la patrulla (Ordenanza 9422, artículo 17).')
rep('5.7', 'No suma sueldos, porque los agentes que pasan a la patrulla ya son empleados del Municipio. Formarlos cuesta, una '
    'sola vez, de 9,2 a 55,0 millones por cada grupo de hasta 60 agentes, es decir, de 0,15 a 0,92 millones por agente, y se '
    'paga con el presupuesto de Seguridad, que ya forma a quienes entran a la patrulla.',
    'No suma empleados, porque los agentes que pasan a la patrulla ya trabajan en el Municipio. Formarlos cuesta, una sola '
    'vez, de 9,2 a 55,0 millones por cada grupo de hasta 60 agentes, es decir, de 0,15 a 0,92 millones por agente, y se paga '
    'con el presupuesto de Seguridad, que ya forma a quienes entran a la patrulla. Pagarles lo mismo que a sus compañeros '
    'cuesta de 62,3 a 504,7 millones por año. El costo más bajo es con 40 agentes que cobran la bonificación de la Patrulla '
    'Municipal: 1,56 millones más por año cada uno. Con 100 agentes en la patrulla a pie, que cobran además la bonificación '
    'de ese cuerpo, es el más alto: 5,05 millones más cada uno. Depende de tres cosas: cuántos pasan, que fija el '
    'relevamiento; qué función ocupa cada uno, porque la ordenanza no aclara si las dos bonificaciones se suman, y los montos '
    'que fija cada año la ordenanza de presupuesto (los de hoy son de 2026). Lo paga Seguridad desde los meses 4 a 6, con '
    'otros gastos de su presupuesto: como mucho, el 1,6% de los 32.446 millones que gastó en 2025. En las cuentas del '
    'capítulo 3, ocupa 62,3 millones del gasto flexible, y 504,7 en el peor caso (3.4).')
fuente('5.7', 'y artículo 17, compensaciones del inspector de tránsito y de la Patrulla Municipal',
       'y artículo 17, compensación del inspector de tránsito y bonificaciones de la Patrulla Municipal y del Cuerpo de '
       'Patrulla a pie')
fuente('5.7', '«Capacitan 60 nuevos agentes…», 3 de marzo de 2026 (https://www.sanisidro.gob.ar/novedades/capacitan-60-nuevos-agentes-para-reforzar-la-patrulla-municipal-y-el-sistema-de-prevenci%C3%B3n). Cálculo propio, consultado el 18 de noviembre de 2026.',
       '«Capacitan 60 nuevos agentes…», 3 de marzo de 2026 (https://www.sanisidro.gob.ar/novedades/capacitan-60-nuevos-agentes-para-reforzar-la-patrulla-municipal-y-el-sistema-de-prevenci%C3%B3n). Cálculo propio: trece meses con las cargas del empleador, en pesos de diciembre de 2025. Consultado el 18 de noviembre de 2026; las bonificaciones, revisadas en las páginas escaneadas (folios 964 a 967) el 19 de noviembre de 2026.')

# 3.4: el gasto flexible ocupado, el libre y el peor caso
rep('3.4', 'ocupa el 51,8% de esa parte. Queda libre el 48,2%.', 'ocupa el 51,9% de esa parte. Queda libre el 48,1%.')
rep('3.4', 'los tomógrafos ahorran sólo 660 millones y las obras vecinales',
    'los tomógrafos ahorran sólo 660 millones, pasan a la patrulla 100 agentes de tránsito que cobran las dos bonificaciones '
    '(5.7) y las obras vecinales')
rep('3.4', 'Aun así, queda libre el 44,7%.', 'Aun así, queda libre el 44,1%.')
rep('3.4', 'entra dentro del 44,7% del gasto flexible', 'entra dentro del 44,1% del gasto flexible')
rep('3.4', 'Tampoco suma sueldos el pase de agentes de tránsito a la patrulla: formarlos cuesta, una sola vez, de 9,2 a 55,0 '
    'millones por cada grupo de hasta 60, y lo paga el presupuesto de Seguridad (5.7).',
    'Pasar agentes de tránsito a la patrulla no suma empleados, y Seguridad lo paga con su presupuesto: formarlos cuesta, '
    'una sola vez, de 9,2 a 55,0 millones por cada grupo de hasta 60, y pagarles lo mismo que a sus compañeros, de 62,3 a '
    '504,7 millones por año, que ya están en la cuenta de arriba (5.7).')
cuadro('3.4', 'Agentes de tránsito que pasan a la patrulla (5.7) | De 9,2 a 55,0 M por cada grupo de hasta 60 agentes, una sola '
       'vez* | No. Los agentes ya son empleados del Municipio y cobran lo mismo. |',
       'Agentes de tránsito que pasan a la patrulla (5.7) | De 62,3 a 504,7 M por año desde los meses 4 a 6, para que cobren lo '
       'mismo que sus compañeros de la patrulla. Formarlos, de 9,2 a 55,0 M por cada grupo de hasta 60 agentes, una sola vez* '
       '| No. Los agentes ya son empleados del Municipio. Lo que suma su sueldo sale de otros gastos de Seguridad. |')
cuadro('6.4', 'pasan a la patrulla, con la formación que ya da el Municipio, y ninguno cobra menos.',
       'pasan a la patrulla, con la formación que ya da el Municipio, y cobran lo mismo que sus compañeros de la patrulla, con '
       'el presupuesto de Seguridad.')

# el mismo 51,9%, 48,1% y 44,1% donde se repite
rep('3', 'el programa ocupa el 51,8% del gasto flexible (3.4)', 'el programa ocupa el 51,9% del gasto flexible (3.4)')
rep('5.1', 'ocupa el 51,8% del gasto flexible:', 'ocupa el 51,9% del gasto flexible:')
rep('5.1', 'Queda libre el 48,2% (3.4).', 'Queda libre el 48,1% (3.4).')
cuadro('6.5', 'Todo este programa ya ocupa el 51,8% de ese gasto. Queda libre el 48,2%, o el 44,7% en el peor caso',
       'Todo este programa ya ocupa el 51,9% de ese gasto. Queda libre el 48,1%, o el 44,1% en el peor caso')
rep('glosario-gasto-flexible', 'Este programa ocupa el 51,8% de esa parte (3.4).', 'Este programa ocupa el 51,9% de esa parte (3.4).')

# método: lo que sale del presupuesto 2026; abogado: si las dos bonificaciones se suman
rep('metodo', 'salvo el bono de agosto de 2026 y el costo de los 60 agentes que se sumaron a la patrulla ese año, que sale del '
    'presupuesto 2026.',
    'salvo el bono de agosto de 2026 y lo que sale del presupuesto 2026: el costo de los 60 agentes que se sumaron a la '
    'patrulla ese año, y la formación y las bonificaciones de los agentes de tránsito que pasan a ella.')
rep('metodo-abogado', 'el decreto que define las tareas de cada uno, y si la adhesión',
    'el decreto que define las tareas de cada uno, si las bonificaciones de la Patrulla Municipal y del Cuerpo de Patrulla a '
    'pie se suman (Ordenanza 9422, artículo 17), y si la adhesión')

# ============ B · la tasa de los terrenos sin uso: 4 veces lo de una casa, 6 si no está mantenido =====================
rep('5.4-r3', 'La ordenanza de tasas va a fijar para los terrenos baldíos, los edificios en ruinas y las obras paradas una tasa '
    'de servicios generales más alta que la de un terreno con casa de la misma zona, desde que se declara la obligación de '
    'construir, como ya hace Bahía Blanca.',
    'Desde que se declara la obligación de construir, la ordenanza de tasas le va a cobrar a cada terreno baldío, edificio '
    'en ruinas u obra parada 4 veces la tasa de servicios generales de una casa en un terreno igual, y 6 veces si no está '
    'mantenido. Pilar ya le cobra a un baldío 3,7 veces lo que a una casa por cada peso de valuación, y 5,6 veces si no está '
    'mantenido; Avellaneda, 3,8 veces.')
rep('5.4-r3', 'y después sigue en el máximo hasta que el dueño cumpla.',
    'y después sigue en el máximo hasta que el dueño cumpla. Así, quien no construye termina pagando 6 veces lo de una casa, '
    'o 9 si tampoco mantiene el terreno.')
rep('5.4-r3', 'Lo que se cobre de más por esa tasa y por el recargo va a ir a la garantía de alquiler. Estas cuentas no suman lo '
    'que se cobre de más, porque todavía no se sabe cuántos terrenos sin uso hay: se cuentan en la primera ronda (punto 6).',
    'Lo que se cobre de más por esa tasa y por el recargo va a ir al fondo de la garantía de alquiler. Cuánto suma a lo que '
    'cobra el Municipio se va a saber con el registro de terrenos del primer año, que se arma en la primera ronda (punto 6): '
    'hoy no se sabe cuántos terrenos sin uso hay, y por eso estas cuentas no lo suman.')
fuente('5.4-r3', 'La tasa más alta: Bahía Blanca, Ordenanza Impositiva 2026, capítulo XXI, artículo 59, «Tasa especial para los '
       'inmuebles baldíos, edificaciones derruidas y paralizadas»: la tasa de servicios urbanos multiplicada por el factor de '
       'ocupación total de la zona, con un adicional del 10% al 50% en cinco años '
       '(https://www.bahia.gob.ar/wp-content/uploads/2026/01/Ordenanza-Impositiva-2026.pdf, consultado el 18 de noviembre de 2026).',
       'La tasa más alta: Pilar, Ordenanza Impositiva 2026 (Ordenanza 112/2025), artículos 2 y 3: la Tasa por Servicios '
       'Generales es la valuación por la alícuota, por el coeficiente de cada destino, por el módulo; la vivienda unifamiliar '
       'paga 3,5 por mil con coeficiente 1,0, y el «TERRENO A: Baldío» y el «TERRENO D: Inmuebles libres de edificaciones, '
       'baldíos con falta de mantenimiento y/o edificación derruida», 6,5 por mil con coeficiente 2,0 y 3,0: 3,7 y 5,6 veces, '
       'cálculo propio (https://pilar.gov.ar/wp-content/uploads/2025/12/ORDENANZA-IMPOSITIVA-2026.pdf, consultado el 19 de '
       'noviembre de 2026). Avellaneda, Ordenanza 31.322 (Ordenanza Impositiva 2026, 27 de noviembre de 2025), artículo 1: '
       'alícuota de 5,00 para «E - BALDIO Y/U OBRA EN CONSTRUCCION» y de 1,30 para «A – VIVIENDA»: 3,8 veces, cálculo propio '
       '(https://sibom.slyt.gba.gob.ar/bulletins/13987/contents/2317247, consultado el 19 de noviembre de 2026).')
rep('anexo-21', 'La Ordenanza Impositiva fija para los inmuebles del artículo 3 una Tasa por Alumbrado, Limpieza y Servicios '
    'Generales mayor que la de los inmuebles edificados de la misma zona. El gravamen del artículo 4 se calcula sobre esa tasa. '
    'Lo que se recauda por encima de la tasa de los inmuebles edificados de la misma zona va al fondo de la Ordenanza 20.',
    'Desde la declaración del artículo 3, la Ordenanza Impositiva fija para los inmuebles de ese artículo una Tasa por '
    'Alumbrado, Limpieza y Servicios Generales de cuatro (4) veces la que corresponde a una vivienda en una parcela igual, de '
    'la misma superficie y zona, y de seis (6) veces si el inmueble no está mantenido. La reglamentación fija qué se considera '
    'mantenido. El gravamen del artículo 4 se calcula sobre esa tasa. Lo que se recauda por encima de la tasa de esa vivienda '
    'va al fondo de la Ordenanza 20.')
rep('3.4', 'Lo que se cobre de más a los terrenos sin uso va a esa garantía, y estas cuentas no lo suman.',
    'Lo que se cobre de más a los terrenos sin uso va a esa garantía, y estas cuentas no lo suman hasta que el registro de '
    'terrenos del primer año diga cuántos hay.')
rep('metodo-abogado', 'La tasa más alta para los terrenos sin uso en la Ordenanza Impositiva,',
    'La tasa más alta para los terrenos sin uso en la Ordenanza Impositiva, de 4 veces la de una vivienda en un terreno igual '
    'y de 6 si no está mantenido,')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
