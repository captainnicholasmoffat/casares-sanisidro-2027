import json,sys,re,glob
out=[]; seen=set()
for f in sys.argv[1:]:
    for p in json.load(open(f)):
        if p['productId'] in seen: continue
        seen.add(p['productId'])
        g=lambda k: (p.get(k) or [''])[0]
        cats=' '.join(p.get('categories',[]))
        tipo=g('Tipo de producto')
        if 'elular' not in cats and 'elular' not in tipo and 'martphone' not in tipo: continue
        it=p['items'][0]
        offs=[]
        for s in it['sellers']:
            co=s['commertialOffer']
            if not co.get('IsAvailable'): continue
            inst=co.get('Installments',[])
            best0=max([i['NumberOfInstallments'] for i in inst if i.get('InterestRate',1)==0] or [0])
            names=sorted(set(i['PaymentSystemName'] for i in inst if i.get('InterestRate',1)==0 and i['NumberOfInstallments']==best0)) if best0 else []
            maxn=max([i['NumberOfInstallments'] for i in inst] or [0])
            offs.append((co['Price'],co['ListPrice'],best0,names,maxn,s['sellerName']))
        if not offs: continue
        offs.sort()
        desc=(p.get('description') or '')+' '+' '.join(str(v) for k in p.get('allSpecifications',[]) for v in p.get(k,[]))
        ois='OIS' if re.search(r'\bOIS\b|estabiliza(ci[oó]n)? [oó]ptic|Optical Image Stabil',desc,re.I) else ('EIS/estab' if re.search(r'estabiliz|\bEIS\b',desc,re.I) else '')
        out.append(dict(id=p['productId'],name=p['productName'],ram=g('Memoria RAM'),rom=g('Memoria interna'),bat=g('Capacidad de la batería'),red=g('Red'),ois=ois,price=offs[0][0],lista=offs[0][1],cuotas0=offs[0][2],medios=offs[0][3],maxcuotas=offs[0][4],seller=offs[0][5],link=p.get('link')))
def num(s):
    m=re.search(r'(\d+)',s or ''); return int(m.group(1)) if m else 0
apt=[o for o in out if num(o['ram'])>=8 and num(o['rom'])>=256 and num(o['bat'])>=5000]
print('celulares disponibles:',len(out),' aptos (8GB/256GB/5000mAh):',len(apt))
for o in sorted(apt,key=lambda x:x['price']):
    print(f"{o['price']:>12,.0f} | lista {o['lista']:>12,.0f} | {o['cuotas0']:>2} cuotas tasa 0 ({', '.join(o['medios'])[:60]}) | max {o['maxcuotas']} | {o['name'][:70]} | RAM {o['ram']} | {o['rom']} | bat {o['bat']} | {o['red']} | {o['ois']} | {o['seller']}")
json.dump(out,open('provinciacompras_api/provinciacompras_celulares_resumen.json','w'),ensure_ascii=False,indent=1)
