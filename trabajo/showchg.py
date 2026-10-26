import json,sys,difflib
a={e['id']:e for e in json.load(open(sys.argv[1]))}
b={e['id']:e for e in json.load(open(sys.argv[2]))}
for k in ['5.5-r11','anexo-14','metodo-abogado']:
    pa=a[k]['texto'].split('\n\n'); pb=b[k]['texto'].split('\n\n')
    print('#####',k,'title:',b[k].get('titulo'), '| paras',len(pa),'->',len(pb))
    sm=difflib.SequenceMatcher(None,pa,pb)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        for i in range(i1,i2): print(f'  - [{i}]',pa[i])
        for j in range(j1,j2): print(f'  + [{j}]',pb[j])
    if k=='5.5-r11':
        print('  marcas antes',a[k].get('marcas')); print('  marcas ahora',b[k].get('marcas'))
fa=a['5.5']['fuentes']; fb=b['5.5']['fuentes']
print('##### 5.5 fuentes')
for x in fb:
    if x not in fa: print('  +',x)
for x in fa:
    if x not in fb: print('  -',x)
print('pos', [i for i,x in enumerate(fb) if x not in fa], 'of', len(fb))
