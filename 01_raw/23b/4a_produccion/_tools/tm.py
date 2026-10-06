# uso: python3 -I tm.py archivo.html  -> lista productos (PrestaShop todomusica)
import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
for b in t.split('data-id-product=')[1:]:
    alt=re.search(r'alt="([^"]+)"',b); url=re.search(r'href="([^"]+\.html)"',b)
    reg=re.search(r'regular-price">([^<]+)',b); pr=re.search(r'product-price" content="([\d\.]+)"',b)
    ds=re.search(r'product-description-short">(.*?)</div>',b,re.S)
    st=re.findall(r'<span (?:style="display: none;" )?class="stock_level_(\w+)">',b)
    vis=[s for s in re.findall(r'<span( style="display: none;")? class="stock_level_(\w+)"',b) if not s[0]]
    d=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',ds.group(1))))[:160] if ds else ''
    print(f"{html.unescape(alt.group(1)) if alt else '?'} | lista {reg.group(1).strip() if reg else '-'} | precio {pr.group(1) if pr else '-'} | stock {','.join(v[1] for v in vis)} | {d} | {url.group(1) if url else ''}")
