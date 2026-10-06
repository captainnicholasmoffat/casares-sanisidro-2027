#!/usr/bin/env python3
# uso: python3 -I grep.py archivo.txt 'regex' [ancho]
import sys,re
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
w=int(sys.argv[3]) if len(sys.argv)>3 else 300
seen=0
for m in re.finditer(sys.argv[2],t,flags=re.I):
    if m.start()<seen: continue
    s=t[max(0,m.start()-w):m.end()+w].replace('\n',' ')
    print('@',m.start(),':',s); print('--'); seen=m.end()+w
