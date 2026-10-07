# uso: python3 -I hx.py archivo.json -> lista productos Hendrix (WooCommerce Store API)
import json,sys,html
for f in sys.argv[1:]:
    try: d=json.load(open(f))
    except Exception as e: print(f,'ERR',e); continue
    for it in d:
        pr=it.get('prices',{}); m=int(pr.get('currency_minor_unit',2))
        p=int(pr.get('price') or 0)/10**m; r=int(pr.get('regular_price') or 0)/10**m
        print(f.split('/')[-1],'|',html.unescape(it['name']),'|',f'{p:,.0f}'.replace(',','.'),'| lista',f'{r:,.0f}'.replace(',','.'),'| stock',it.get('is_in_stock'),'|',it['permalink'])
