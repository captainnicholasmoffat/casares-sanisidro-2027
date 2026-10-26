import re, html, sys
for f in sys.argv[1:]:
    t = open(f, encoding='utf-8', errors='ignore').read()
    t = re.sub(r'(?s)<(script|style|nav|header|footer)[^>]*>.*?</\1>', ' ', t)
    title = re.search(r'<title>(.*?)</title>', t, re.S)
    dates = re.findall(r'(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}T[\d:]+|\d{1,2} de [a-záéíóú]+ de \d{4})', t)
    m = re.search(r'(?s)<article.*?</article>', t) or re.search(r'(?s)class="[^"]*(field--name-body|node__content|content)[^"]*".*', t)
    body = m.group(0) if m else t
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    txt = re.sub(r'\s+', ' ', txt)
    print('=====', f, '|', title.group(1).strip() if title else '', '| fechas:', dates[:4])
    print(txt[:1800])
