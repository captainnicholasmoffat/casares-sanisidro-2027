#!/usr/bin/env python3
# Resume un index.json de la AWS Price List API: una línea por producto/precio OnDemand.
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
out = [f"Resumen propio de {src.split('/')[-1]} (AWS Price List API). publicationDate={d.get('publicationDate')} version={d.get('version')}",
       "region | productFamily | storageClass/volumeType | usagetype | operation | descripción | unidad | USD | desde-hasta"]
for sku, p in d['products'].items():
    a = p.get('attributes', {})
    for term in d.get('terms', {}).get('OnDemand', {}).get(sku, {}).values():
        for pd in term['priceDimensions'].values():
            out.append(" | ".join(str(x) for x in [a.get('regionCode', a.get('location')), p.get('productFamily'), a.get('storageClass', a.get('volumeType', '')), a.get('usagetype'), a.get('operation', ''), pd.get('description'), pd.get('unit'), pd['pricePerUnit'].get('USD'), f"{pd.get('beginRange')}-{pd.get('endRange')}"]))
open(dst, 'w').write("\n".join(out) + "\n")
print(len(out))
