# Uso: python3 ov.py salida.json "consulta overpass QL"
# Prueba varios espejos de Overpass con reintentos. Guarda la respuesta JSON cruda.
import sys, time, json, urllib.request, urllib.parse
out, q = sys.argv[1], sys.argv[2]
mirrors = ['https://maps.mail.ru/osm/tools/overpass/api/interpreter',
           'https://overpass-api.de/api/interpreter',
           'https://overpass.kumi.systems/api/interpreter',
           'https://overpass.private.coffee/api/interpreter']
for attempt in range(6):
    for m in mirrors:
        try:
            data = urllib.parse.urlencode({'data': q}).encode()
            req = urllib.request.Request(m, data=data, headers={'User-Agent': 'investigacion-costa-sanisidro/1.0'})
            r = urllib.request.urlopen(req, timeout=180).read()
            j = json.loads(r)
            if 'remark' in j and 'error' in j['remark'].lower():
                print('remark', m, j['remark'][:200]); continue
            open(out, 'wb').write(r)
            print('OK', m, len(r), 'bytes', j.get('osm3s', {}).get('timestamp_osm_base'), len(j['elements']), 'elements')
            sys.exit(0)
        except Exception as e:
            print('fail', m, str(e)[:120])
    time.sleep(20)
sys.exit(1)
