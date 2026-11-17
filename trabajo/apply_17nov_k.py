"""Actualización del 17/11/2026, parte K: los arreglos obvios de la revisión completa del 17/11 (cinco revisores
independientes; consolidado en el scratchpad de la sesión, CONSOLIDADO.md). Sólo alinea el texto con decisiones ya
tomadas, con hechos verificados, con el modelo o con otra parte del programa, y con las reglas de escritura: no suma
políticas, dinero ni promesas. Lo que necesita una decisión de Nick queda afuera (DECISIONES_PENDIENTES.md)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}


def _ps(e): return e['texto'].split('\n\n')


def rep(eid, old, new, dentro=False):
    """Cambia old por new en el único párrafo que lo tiene. Corre las marcas que siguen; si el cambio toca una marca,
    se niega, salvo con dentro=True y el cambio entero adentro de esa marca (entonces se corre sólo su final)."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta:
            if dentro and m[0] <= pos and end <= m[1]: m[1] += delta
            else: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


def ins(eid, ancla, texto):
    """Inserta texto justo después de ancla; corre las marcas que empiezan después."""
    e = by[eid]; ps = _ps(e); hits = [i for i, p in enumerate(ps) if p.count(ancla) == 1]
    assert len(hits) == 1 and sum(p.count(ancla) for p in ps) == 1, (eid, ancla[:60])
    i = hits[0]; k = ps[i].index(ancla) + len(ancla)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= k: m[0] += len(texto); m[1] += len(texto)
        elif m[1] > k: raise SystemExit(f'marca {eid} p{i} {m}')
    ps[i] = ps[i][:k] + texto + ps[i][k:]; e['texto'] = '\n\n'.join(ps)


def nuevos(eid, ancla, textos, negrita=None):
    """Agrega párrafos después del único párrafo que tiene ancla; corre las claves de las marcas de los que siguen.
    negrita: para cada párrafo nuevo, cuántos caracteres del principio van en negrita (o None)."""
    e = by[eid]; ps = _ps(e); hits = [i for i, p in enumerate(ps) if ancla in p]; assert len(hits) == 1, (eid, ancla[:60])
    i = hits[0]; n = len(textos); mk = e.get('marcas', {})
    mk = {str(int(k) + n if int(k) > i else int(k)): v for k, v in mk.items()}
    for j, b in enumerate(negrita or []):
        if b: mk[str(i + 1 + j)] = [[0, b, 'b']] if isinstance(b, int) else b
    if mk: e['marcas'] = mk
    e['texto'] = '\n\n'.join(ps[:i + 1] + textos + ps[i + 1:])


def cuadro(eid, old, new, campo='texto'):
    cs = by[eid]['cuadros']; idx = [k for k, c in enumerate(cs) if old in c[campo]]
    assert len(idx) == 1 and cs[idx[0]][campo].count(old) == 1, (eid, old[:60], idx)
    cs[idx[0]][campo] = cs[idx[0]][campo].replace(old, new, 1)


def fuente(eid, old, new):
    e = by[eid]; assert e['fuentes'].count(old) == 1, (eid, old[:60]); e['fuentes'] = e['fuentes'].replace(old, new, 1)


def titulo(eid, old, new):
    assert by[eid]['titulo'] == old, (eid, by[eid]['titulo']); by[eid]['titulo'] = new


AGENTES = 'los 60 agentes que se sumaron a la patrulla en 2026'

# ---- Qué proponemos hacer: la rampa con su condición, la vivienda, la salud mental, la consulta de lugares y los cien días
ins('proponemos', 'va a quedar reservado por ordenanza, para que no se pueda usar en otra cosa.',
    ' Cada escalón se gana: el dinero del siguiente se libera recién cuando la auditoría externa certifica que se cumplió el anterior (6.2).')
ins('proponemos', 'y va a haber más lugares para alquilar en las casas que ya existen.',
    ' Además, los terrenos que nadie usa se van a tener que construir o vender.')
ins('proponemos', 'Quien la use para mejorar el Municipio va a cobrar una parte de lo que le haga ganar o ahorrar.',
    ' También va a escuchar a quien quiera contarle cómo se siente, y le va a acercar un acompañante formado, bajo un profesional (5.6).'
    ' Con la cámara del teléfono, el vecino le va a poder mostrar un terreno, una casa, un local o un pedazo de plaza, y ella le va a decir qué se puede hacer ahí (5.9).')
rep('proponemos', 'la primera asamblea de cada zona ya se va a haber hecho.',
    'la primera asamblea de cada zona ya se va a haber hecho, y los vecinos ya van a haber elegido las obras del primer año.')

# ---- 1.3 y 1.5: cifras exactas y quién aprueba
cuadro('1.3', '572 $/año', '573 $/año'); cuadro('1.3', '1.127 $/año', '1.128 $/año')
rep('1.5', 'recibió 82.268 millones de pesos de la Provincia de Buenos Aires.', 'recibió 82.268 millones de pesos de coparticipación de la Provincia de Buenos Aires.')
rep('1.5', 'puede financiarse sin pedirle permiso a nadie.',
    'puede financiarse sin pedirle permiso a la Provincia: lo deciden acá el Concejo Deliberante y, para la tasa, la asamblea de concejales y mayores contribuyentes.')
rep('1.5', 'La Provincia paga el 25% del gasto de San Isidro.', 'La coparticipación de la Provincia paga el 25% del gasto de San Isidro.')

# ---- 2.3, cuadro 9: lo que dicen hoy el 5.4, el 5.6, el 5.9 y el 4.11
cuadro('2.3', 'Se va a pagar con el dinero de obra que decidan los vecinos. Donde no alcance, se usará el dinero de vivienda. Medir por zona la conexión a internet, que hoy nadie mide.',
       'Las redes de la calle se van a pagar con el dinero de obra que decidan los vecinos, y la conexión de cada casa, con el dinero de vivienda. '
       'Medir por zona la conexión a internet, que hoy nadie mide. Para alquilar, una garantía del Municipio, más lugares en las casas que ya existen y terrenos sin uso que se construyen o se venden.')
cuadro('2.3', 'Además, dirá cuánto pagó cada hospital por cada insumo.',
       'Además, dirá cuánto pagó cada hospital por cada insumo. Acompañamiento en salud mental cerca de casa, con acompañantes formados y bajo un profesional.')
cuadro('2.3', 'También le dirá qué hace falta, cuánto cuesta y el tiempo que lleva. Cualquier vecino podrá preguntarle en qué está su reclamo.',
       'También le dirá qué hace falta, cuánto cuesta y el tiempo que lleva. Lo mismo va a poder hacer cualquier vecino con un terreno, una casa o un pedazo de plaza, para saber qué se puede hacer ahí. '
       'Cualquier vecino podrá preguntarle en qué está su reclamo, y si necesita reclamar o denunciar algo, ella lo va a ayudar a hacerlo.')

# ---- Capítulo 3: los 60 agentes en las cuentas, el bono, el umbral de 1,26% y cifras sueltas
cuadro('3.1', 'La franja rayada es la diferencia: el déficit.', 'En la franja rayada está la diferencia: el déficit.')
cuadro('3.2', 'Cuánto crece lo que recauda el Municipio. Cuánto cae lo que le manda la Provincia.', 'Cuánto crece lo que recauda el Municipio y cuánto cae lo que le manda la Provincia.')
fuente('3.2', 'adjunto de la Provincia, Walter Martello, con datos', 'adjunto de la Provincia, con datos')
ins('3.3', 'un 2,2% por año.', f' El gasto queda como en 2025, más {AGENTES}: unos 1.011 millones por año desde 2028 (5.7).')
cuadro('3.3', 'Nota: las cuentas de este programa usan datos hasta el 31 de diciembre de 2025. Por eso no incluyen el bono de 30.000 millones que el Municipio tomó en agosto de 2026 (3.5).',
       'Nota: el resultado no incluye los intereses del bono de 30.000 millones que el Municipio tomó en agosto de 2026 (3.5), porque su tasa es variable y estas cuentas descuentan la inflación. '
       f'Su capital va debajo de la línea, como en la cuenta oficial. Desde 2028 cuentan también {AGENTES} (5.7).')
cuadro('3.4', '7.730,9 M, el 2,5% del gasto total', '7.730,9 M, el 2,4% del gasto total')
rep('3.4', 'del gasto flexible que queda libre con todo sumado.', 'del gasto flexible que queda libre aun en el peor caso.')
rep('3.5', 'Ahí presentará la ordenanza. Después la va a aprobar la asamblea de concejales y mayores contribuyentes.',
    'Ahí presentará la ordenanza, que el Concejo tiene que votar como ordenanza preparatoria antes del 22 de diciembre. Después la tiene que aprobar la asamblea de concejales y mayores contribuyentes.')
cuadro('3.5', 'casi se duplicó en dos años y medio', 'casi se duplicó en dos años y cuarto', campo='titulo')
rep('3.6', 'crezca menos de 1,2% por año', 'crezca menos de 1,26% por año', dentro=True)
rep('3.6', 'Ese 1,2% es el límite.', 'Ese 1,26% es el límite.')
cuadro('6.6', 'crece menos de 1,2% por año, descontada la inflación | Ese 1,2% es el límite.', 'crece menos de 1,26% por año, descontada la inflación | Ese 1,26% es el límite.')
rep('metodo-notas-3', 'El escenario base congela el gasto, descontada la inflación, en el nivel de 2025.',
    f'El escenario base congela el gasto, descontada la inflación, en el nivel de 2025, más {AGENTES}: unos 1.011 millones por año desde 2028 (5.7).')
rep('metodo-notas-3', ' El gasto de este programa también entra en las cuentas. En 2029 y 2030, la tabla nueva cobra más que ese gasto. Cobra menos en 2028 y desde 2031 (cuadro 20).',
    ' Muestra sólo lo que pasa si nada cambia. Con este programa, el resultado es el mismo en 2028 y desde 2031, y mejor en 2029 y 2030, porque esos dos años la tabla nueva cobra más de lo que gasta el programa (cuadro 20).')
rep('metodo-notas-3', 'Acassuso da 2,37 veces Boulogne Sur Mer, en vez de 2,94.',
    'Acassuso da 2,37 veces Boulogne Sur Mer en la tabla municipal y 2,94 en la valuación provincial, en vez de 2,32 y 2,80.')
rep('metodo', 'Las cuentas de este programa usan datos hasta el 31 de diciembre de 2025.',
    'Las cuentas de este programa usan datos hasta el 31 de diciembre de 2025, salvo el bono de agosto de 2026 y el costo de los 60 agentes que se sumaron a la patrulla ese año, que sale del presupuesto 2026.')
rep('metodo', 'Se hicieron en octubre de 2026,', 'Se hicieron en octubre y noviembre de 2026,')
rep('metodo', 'quién tiene gratis el profesor digital y los mensajes de texto.',
    'quién tiene gratis el profesor digital, los mensajes de texto, la garantía de alquiler, los terrenos sin uso, las denuncias con la inteligencia artificial del Municipio, '
    'los power users, la salud mental, el ejemplo de Miami y la consulta de lugares.')

# ---- Capítulo 4
cuadro('4.8', 'A la izquierda, cómo funciona hoy. A la derecha, qué cambia.', 'A la izquierda, cómo funciona hoy; a la derecha, qué cambia.')
rep('4.9', 'ya no depende de la discusión del presupuesto de cada año.',
    'ya no depende de la discusión del presupuesto de cada año. Cada escalón nuevo se libera cuando la auditoría externa certifica que se cumplió el anterior (6.2).')
rep('4.11', 'y no sólo la semana de la asamblea.', 'y no sólo en las semanas de asamblea.')
rep('4.11', 'Cada denuncia y su respuesta se van a poder consultar en la inteligencia artificial del Municipio.',
    'Cada denuncia y su respuesta se van a poder consultar en la inteligencia artificial del Municipio, sin los datos de quien denuncia.')
rep('4.11', 'Cada contrato se va a licitar antes de comprometer el dinero.',
    'Cada contrato grande se va a licitar antes de comprometer el dinero. Mientras corre la primera licitación, el uso de los primeros meses se paga con las compras chicas '
    'que la ley permite sin licitación pública (Ley Orgánica de las Municipalidades, artículo 151).')
cuadro('4.11', 'Antes de comprometer el dinero, se van a presupuestar y licitar.', 'Antes de comprometer el dinero, se van a presupuestar y licitar, salvo las compras chicas de los primeros meses (6.4).')
ins('4.11-r1', 'que tarda más en Boulogne que en Acassuso.',
    ' Lo que un vecino cuenta sobre su salud, o como víctima de violencia, no entra en esos resúmenes: se usa sólo para su propio servicio (5.6 y 5.13).')
rep('4.11-r4', 'Si no, la deja lista para que el vecino la firme y la presente en la fiscalía.',
    'Si no, la deja lista para que el vecino la firme y la presente en la fiscalía: con firma digital desde el teléfono, donde se acepte así, o en persona.')
rep('4.11-r4', 'en los días que fija el Código Electoral Nacional, deja de hacerlo.', 'en los días que fija la ley electoral, deja de hacerlo.')
rep('4.11-r5', 'Ningún pago sale por decisión de la inteligencia artificial sola: lo aprueba una persona, y queda registrado quién hizo qué. Si la inteligencia artificial sospecha un acuerdo para cobrar, avisa.',
    'Ningún pago sale sólo por decisión de la inteligencia artificial del Municipio: lo aprueba una persona, y queda registrado quién hizo qué. Si ella sospecha un acuerdo para cobrar, avisa.')
rep('4.11-r6', 'Ese uso para el propio vecino tiene un aviso y un botón para apagarlo.',
    'Ese uso para el propio vecino necesita su permiso, dado aparte, que puede retirar cuando quiera, como en el profesor digital (5.8). Nunca se usa lo que cuenta sobre su salud (5.6).')
rep('4.12', 'reúna el apoyo del 60% de los vecinos y haga la obra', 'reúna el apoyo del 60% de los vecinos beneficiados y haga la obra')
rep('4.13', 'Si el 60% de los vecinos lo pide', 'Si el 60% de los vecinos beneficiados lo pide')

# ---- Capítulo 5
rep('5.3', ' en La Cava y en Boulogne. Hoy nadie la midió. Esa medición es la que propone la sección 5.4.',
    ' en cada zona, durante la primera ronda de asambleas (5.4). '
    'Después, los pasantes la van a relevar hogar por hogar en La Cava y en Boulogne (cuadro 33). Hoy nadie la midió.')
rep('5.4', 'Con la partida de vivienda, de 3.092,4 millones por año, se va a pagar',
    'Con la partida de vivienda, que llega a 3.092,4 millones por año cuando el programa funciona completo (cuadro 35), se va a pagar', dentro=True)
rep('5.4-r1', 'Allá hay unas 35.000 garantías del Estado', 'En 2010 había allá unas 35.000 garantías del Estado')
rep('5.4-r1', 'un fondo que le paga al dueño si el inquilino deja de pagar.', 'un fondo que le paga al dueño si el inquilino deja de pagar (Ordenanza 20 del anexo).')
rep('5.4-r1', 'del 40% del ingreso de quien alquila, como en Uruguay.', 'del 40% del ingreso de quien alquila, o del grupo que alquila junto, como en Uruguay.')
rep('5.4-r1', 'A quien cobra del Municipio, el alquiler se le descuenta del sueldo.', 'A quien cobra del Municipio, si está de acuerdo, el alquiler se le descuenta del sueldo.')
rep('5.4-r1', 'En la cuenta de este programa, el fondo alcanza', 'En la cuenta de este programa, si las garantías se dan a lo largo del año, el fondo alcanza')
fuente('5.4-r1', 'mil garantías que entran a lo largo del primer año', '840 garantías que entran a lo largo del primer año')
rep('5.4-r2', 'En San Isidro va a ir por ordenanza (Ordenanza 21 del anexo).', 'En San Isidro va a ir por ordenanza, con una audiencia pública antes de votarla (Ordenanza 21 del anexo).')
rep('5.4-r3', 'con una regla publicada, y no un funcionario.', 'con una regla publicada, y no a criterio de un funcionario. Una persona del Municipio firma cada plazo (4.11).')
rep('5.4-r3', 'hasta el 50% de la tasa, el máximo', 'hasta el 50% de la tasa de servicios generales, el máximo', dentro=True)
rep('5.5-r11', 'proponemos una ordenanza nueva de foodtrucks y un canon', 'proponemos una ordenanza nueva de foodtrucks (Ordenanza 19 del anexo) y un canon')
rep('5.5-r11', 'que en Bosque Alegre sólo permite vender bebidas en kioscos.', 'que en Bosque Alegre sólo permite vender bebidas en kioscos (Ordenanza 19 del anexo).')
rep('5.5-r11', 'la inteligencia artificial la sella y arma la denuncia', 'la inteligencia artificial del Municipio la sella y arma la denuncia')
rep('5.5-r12', 'entre semana y de día,', 'entre semana, hasta las 22,', dentro=True)
rep('5.6', '263.106 pesos por habitante', '263.107 pesos por habitante')
rep('5.6-r5', 'cuyo trabajo ahora hace la inteligencia artificial van', 'cuyo trabajo ahora hace la inteligencia artificial del Municipio van')
rep('5.6-r5', 'avisa a quien corresponda y le da la Línea Nacional', 'avisa a quien corresponda, le indica la guardia o el 107 y le da la Línea Nacional')
rep('5.6-r5', 'La inteligencia artificial no hace terapia', 'La inteligencia artificial del Municipio no hace terapia')
rep('5.7', 'Además, en marzo de 2026 entraron 60 agentes nuevos a la patrulla. Este programa mantiene la cantidad de agentes que haya al asumir, y eso suma unos 1.011 millones por año a las cuentas desde 2028.',
    'Además, en marzo de 2026 empezaron a formarse 60 agentes nuevos para la patrulla. Este programa mantiene la cantidad de agentes que haya al asumir. '
    'Como esos 60 no estaban en el gasto de 2025, las cuentas del capítulo 3 les suman unos 1.011 millones por año desde 2028. '
    'No es un gasto de este programa: está también en la cuenta de lo que pasa si nada cambia.')
by['5.7']['fuentes'] += ('\n\n5.7 · los 60 agentes de 2026: Zona Norte Digital, 4 de marzo de 2026. Su costo: Presupuesto 2026 del Municipio '
                         '(Ordenanza 9422), programa 46.01, 5.743.108.868 pesos para 359 cargos, llevados a pesos de diciembre de 2025 con el IPC del INDEC; cálculo propio.')
rep('5.9', 'Si la habilitación pasa a ser automática,', 'Si la habilitación sale en el momento,', dentro=True)
rep('5.9', 'La patrulla municipal entra en la segunda etapa, que cuesta de 29,5 a 35,3 millones una sola vez, y de 135,7 a 162,4 millones por año.',
    'La patrulla municipal entra en la segunda etapa. Con los agentes que haya al asumir, de 359 a unos 390 (5.7), cuesta de 35,3 a 38,4 millones una sola vez, y de 162,4 a 176,9 millones por año.')
titulo('5.9-r1', 'El ejemplo de Miami: una plataforma que acelera los permisos de obra', 'El ejemplo de Miami: una plataforma elegida para acelerar los permisos de obra')
rep('5.9-r1', 'que junta ocho aplicaciones en una. Ese mismo mes empezó a revisar en el día las obras simples, y en julio el condado de Miami-Dade lo hizo permanente, con un 10% menos de tasa por cada día hábil de demora.',
    'que junta ocho aplicaciones en una, y ese mismo mes empezó a revisar en el día las obras simples. Muy cerca, el condado de Miami-Dade aprueba en el día algunas obras de vivienda '
    'desde hace más de veinte años, y en julio de 2026 lo pasó a su código: si la demora es culpa de su oficina, la tasa baja un 10% por cada día hábil, como pide la ley de Florida.')
rep('5.9-r1', 'Según los críticos, la tecnología ya existe.', 'Según un análisis del Independent Institute, la tecnología ya existe.')
rep('5.9-r2', 'También le llegará a la auditoría externa y, si hay delito, a la fiscalía.',
    'También le llegará a la auditoría externa y, si hay delito, a la fiscalía. Mientras no se contrate la auditoría externa, la recibe sólo la comisión, y la fiscalía si hay delito; '
    'al empezar, la auditoría recibe todas las anteriores (anexo, Ordenanza 4).')
titulo('5.9-r3', 'Nuestra propuesta: le mostrás un lugar y te dice qué se puede hacer',
       'Nuestra propuesta: mostrarle un lugar a la inteligencia artificial del Municipio y saber qué se puede hacer ahí')
rep('5.9-r3', 'la inteligencia artificial lo ayuda a definirlo.', 'la inteligencia artificial del Municipio lo ayuda a definirlo.', dentro=True)
rep('5.9-r3', 'nada que cierre, cobre o se quede con una parte del espacio.', 'nada que lo cierre, cobre la entrada o reserve una parte para uso exclusivo.', dentro=True)
rep('5.9-r3', 'La inteligencia artificial acelera, pero no aprueba sola.', 'La inteligencia artificial del Municipio acelera, pero no aprueba sola.')
_p6 = '6 · Con los datos cuidados.'
nuevos('5.9-r3', 'que responde por el proyecto.', [_p6 + ' El video y la ubicación del vecino son datos personales: se usan sólo para contestarle, '
                                                   'y las caras de otras personas se difuminan (Ley 25.326).'], [len(_p6)])
assert by['5.10']['hoja_a4_fin'] == 96; by['5.10']['hoja_a4_fin'] = 97
rep('5.11-r1', 'mandará un aviso por la propia inteligencia artificial.', 'mandará un aviso por la propia inteligencia artificial del Municipio.')
rep('5.11-r1', 'la inteligencia artificial se lo avisa al vecino', 'la inteligencia artificial del Municipio se lo avisa al vecino')
rep('5.11-r1', 'todo lo que escucha la inteligencia artificial, con plazo', 'todo lo que escucha la inteligencia artificial del Municipio, con plazo')
rep('5.11-r1', 'Antes de cada vencimiento, la inteligencia artificial le avisa.', 'Antes de cada vencimiento, la inteligencia artificial del Municipio le avisa.')
rep('5.11-r1', 'el proveedor de la inteligencia artificial.', 'el proveedor de la inteligencia artificial del Municipio.')
rep('5.12', 'En las cuentas del capítulo 3, ese gasto es fijo, justamente porque este programa no lo toca.',
    f'En las cuentas del capítulo 3, ese gasto queda fijo, porque este programa no lo toca: es el de 2025, más {AGENTES} (5.7).')
cuadro('5.14', 'Queda afuera del programa. Sólo se trata cómo se dan las excepciones: con audiencia pública y la opinión de la comisión de la zona (5.5 y anexo, Ordenanza 13).',
       'Queda afuera del programa, salvo dos puntos: cómo se dan las excepciones, con audiencia pública y la opinión de la comisión de la zona (5.5 y anexo, Ordenanza 13), '
       'y la segunda y la tercera vivienda en el lote, con audiencia pública y dentro de la altura y la ocupación que ya fija el Código, junto con la obligación de construir '
       'en los terrenos sin uso (5.4 y anexo, Ordenanza 21).')
rep('5.15', 'se le puede preguntar a su inteligencia artificial.', 'se le puede preguntar a la inteligencia artificial del Municipio.')
rep('5.15', 'patrullar donde está el delito, usar mejor', 'patrullar donde está el delito con los agentes que haya al asumir, usar mejor')

# ---- Capítulo 6
rep('6.1', 'También va a poder anotar a su hijo en el primer centro de apoyo escolar.', 'Además, cada familia va a poder anotar a sus hijos en el primer centro de apoyo escolar.')
cuadro('6.1', 'y para elegir las obras del primer año, que hace el Ejecutivo |',
       'y para elegir las obras del primer año, que hace el Ejecutivo. Depende de que el Concejo apruebe antes la ordenanza de la partida (4.7) |')
rep('6.2', 'El año 1 sirve para probar que las seis comisiones pueden formarse, elegir obras y justificar cada peso.',
    'El año 1 sirve para probar que las asambleas de las seis zonas pueden elegir obras, y que las comisiones pueden formarse y controlar cada peso.')
rep('6.2', 'Como las obras se eligen en marzo,', 'Como las obras se eligen en el mes 3 de cada año, entre febrero y marzo,')
cuadro('6.4', 'También se cuentan los baldíos, las ruinas y las obras paradas de cada zona (5.4).',
       'También se mide la conexión a internet y se cuentan los baldíos, las ruinas y las obras paradas de cada zona (5.4).')
cuadro('6.4', 'Se presentan al Concejo las diez ordenanzas del anexo que todavía faltan:', 'Se presentan al Concejo diez de las catorce ordenanzas del anexo que todavía faltan:')
cuadro('6.4', 'y obliga a construir en los terrenos sin uso (5.4) |', 'y obliga a construir en los terrenos sin uso, con una audiencia pública antes de votarla (5.4) |')
cuadro('6.4', 'Mes 12 | Termina el año 1 de la rampa (cuadro 21). Cada escalón se cuenta por ejercicio, que cierra el 31 de diciembre |',
       'Mes 12 | Terminan las obras del año 1 de la rampa (cuadro 21). El escalón se cuenta con el ejercicio, que cierra el 31 de diciembre, y la auditoría externa lo certifica hacia marzo (6.2) |')
cuadro('6.4', 'Mes 24 | Termina el año 2 de la rampa (cuadro 21).', 'Mes 24 | Terminan las obras del año 2 de la rampa (cuadro 21).')
cuadro('6.4', 'Mes 36 | Termina el año 3 de la rampa (cuadro 21).', 'Mes 36 | Terminan las obras del año 3 de la rampa (cuadro 21).')
cuadro('6.5', 'Para cada una hay un plan mientras tanto: la grabación con su huella, la beca municipal, la auditoría externa (6.2, 6.4 y 6.6).',
       'Para algunas hay un plan mientras tanto: la grabación con su huella, la beca municipal, la auditoría externa y el mapa con los hechos que registra el Municipio (6.2, 6.4 y 6.6).')
cuadro('6.5', 'Las asambleas se transmiten desde que funciona esa parte de la inteligencia artificial del Municipio.',
       'Las asambleas se transmiten desde que funciona esa parte de la inteligencia artificial del Municipio. Después de las tres primeras partes, la inteligencia artificial '
       'del Municipio suma sus funciones nuevas a medida que se construyen, con el dictamen del abogado donde la Nota de método lo pide: las denuncias de los vecinos, '
       'los power users, las historias cortas, la consulta de lugares, la conversación sobre salud mental y el encuentro entre dueños e inquilinos.')

# ---- Nota de método: las notas, las fuentes y lo que tiene que confirmar un abogado
rep('metodo-notas-4', 'Hay cuatro asambleas por zona y por año, 24 en total, como el ciclo mínimo de la Ciudad de Buenos Aires.',
    'Alcanza para cuatro asambleas por zona y por año, 24 en total, como el ciclo mínimo de la Ciudad de Buenos Aires: el doble de las dos rondas del calendario (6.4).')
_caba = '6.1 · cómo abría su ciclo el presupuesto participativo de la Ciudad: '
assert by['6.1']['fuentes'].startswith(_caba) and '\n' not in by['6.1']['fuentes'] and not by['metodo-notas-4']['fuentes']
by['metodo-notas-4']['fuentes'] = 'Notas del capítulo 4 · el ciclo de la Ciudad de Buenos Aires: ' + by['6.1']['fuentes'][len(_caba):]
by['6.1']['fuentes'] = ''
rep('metodo-notas-5', 'La Ciudad de Miami anunció que adoptaba la plataforma en marzo de 2026.', 'La Ciudad de Miami eligió la plataforma en marzo de 2026.')
rep('metodo-notas-6', 'Tres compromisos, el 15, el 16 y el 21, dependen sólo del Ejecutivo.', 'Tres compromisos, el 15, el 16 y el 21, salen por decreto del Ejecutivo.')
rep('metodo-abogado', 'Mostrarle a cada vecino historias según lo que usa, con aviso y botón para apagarlo, sin un permiso aparte (Ley 25.326, artículo 5).',
    'Mostrarle a cada vecino historias según lo que usa, sólo con su permiso, dado aparte y revocable, como en el profesor digital, sin usar nunca sus datos de salud (Ley 25.326, artículos 5 y 7).')
nuevos('metodo-abogado', '• 4.11. Mostrarle a cada vecino historias', [
    '• 4.11. Pedirles a las asociaciones vecinales, que son asociaciones civiles, que acepten la inscripción en línea de los vecinos para inscribirse en el registro del Municipio '
    '(Ordenanza 1 del anexo, artículo 11).'], [[[2, 7, 'b']]])
rep('metodo-abogado', 'La edificación obligatoria y la segunda y tercera vivienda en el lote (Ordenanza 21 del anexo; Ley 14.449).',
    'La edificación obligatoria y la segunda y tercera vivienda en el lote, y si la Ordenanza 21 necesita antes la aprobación de la Provincia, como las normas de '
    'ordenamiento urbano (Ordenanza 21 del anexo; Ley 14.449; Decreto-Ley 8912/77, artículo 83).')
rep('metodo-abogado', 'Que la inteligencia artificial del Municipio acompañe a un vecino en salud mental bajo un profesional responsable,',
    'El acompañamiento de la inteligencia artificial del Municipio a un vecino en salud mental, bajo un profesional responsable,')
nuevos('metodo-abogado', '• 5.9. La sanción a la denuncia falsa contra un inspector', [
    '• 5.9. La consulta de lugares: el video y la ubicación del vecino como datos personales, y la imagen marcada como ilustración, que no es una aprobación (Ley 25.326).'],
    [[[2, 6, 'b']]])

# ---- Anexo
rep('anexo-1', 'Toda persona puede consultarlo en el Sistema de Información Municipal.',
    'Toda persona puede consultarlo en el Sistema de Información Municipal. Para inscribirse, cada asociación vecinal acepta que los vecinos de su zona se asocien en línea, en ese mismo sistema.')
nuevos('anexo-1', 'Su uso se limita a los fines de la asociación', [
    'Artículo 13 — Comisión zonal y alcance',
    'Es comisión zonal la asociación vecinal registrada de cada zona; si hay más de una, actúan como una sola comisión, con una sola partida. Donde no hay ninguna en condiciones, '
    'el Departamento Ejecutivo convoca a una asamblea abierta y ayuda a los vecinos a formar una. Mientras tanto, los vecinos de la zona priorizan igual en asamblea, y el '
    'Departamento Ejecutivo ejecuta la obra en esa misma zona. La comisión zonal prioriza sólo las obras que sirven sobre todo a su zona —desagüe cloacal, gas de red, desagües '
    'pluviales, veredas, alumbrado y calles—, y no las que sirven a varias zonas a la vez.'])
rep('anexo-no-dicen', 'Las comisiones zonales son las asociaciones vecinales que ya existen, reconocidas por la propia Ordenanza 6045.',
    'Las comisiones zonales son las asociaciones vecinales que ya existen, registradas según la Ordenanza 6045, a las que la Ordenanza 1 les da ese papel (artículo 13).')
_pu = 'Todavía no regula el pago a los power users.'
nuevos('anexo-no-dicen', 'No toca lo que no es municipal.', [
    _pu + ' Pagarles a vecinos y a empleados del Municipio una parte de lo que su aviso hace cobrar o ahorrar (4.11) necesita antes el dictamen de un abogado sobre su base legal (Nota de método).'],
    [len(_pu)])
rep('anexo-21', 'de la tasa de alumbrado, barrido y limpieza, sin exenciones.', 'de la Tasa por Alumbrado, Limpieza y Servicios Generales, sin exenciones.')

# ---- Glosario
rep('glosario', 'que aparecen en el texto, explicadas', 'que aparecen en el texto y en las cuentas, explicadas')
rep('glosario-copyleft', 'Un tipo de licencia de software.', 'Un tipo de licencia de software, como la AGPL (4.11).')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
