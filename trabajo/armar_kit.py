import os,shutil,sys
S,K=sys.argv[1],sys.argv[2]
P='/home/claude/proyecto'
skip_proj={'sitio_sanisidro2027.zip'}
n=0;tot=0
# 1) proyecto: everything except zip, caches
for root,dirs,files in os.walk(P):
    dirs[:]=[d for d in dirs if d not in ('node_modules','__pycache__','.wrangler','.git')]
    for f in files:
        if f in skip_proj or f.endswith('.pyc'): continue
        src=os.path.join(root,f); rel=os.path.relpath(src,P)
        dst=os.path.join(K,'proyecto',rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
        shutil.copy2(src,dst); n+=1; tot+=os.path.getsize(src)
print('proyecto',n,tot//1e6,'MB')
# 2) scratchpad work
EXCL={'repo','wr','repos','sec','comm','ext','lists','pkgchk','tessdata','wf','oldsite','img','hf_out','hf_base','heroprop',
 'v','v3','v4','v5','v5b','v5c','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19','v20','v21',
 'd18','d19','latest','entrega','m10','mob','mm','rev','shots','shots_b','shots_com','shots_f','propart','planart','propdesp',
 'sitio_test','diag','r11','si_img','si','dl','dl1','dl2','donal_dl','tish_dl','indec','bak','kit','chk','tasks'}
TXT={'.py','.sh','.js','.mjs','.ts','.md','.txt','.json','.csv','.tsv','.toml','.yaml','.yml','.svg','.xlsx','.geojson','.qmd'}
m=0;t2=0;skipped={}
for root,dirs,files in os.walk(S):
    rel_root=os.path.relpath(root,S)
    top=rel_root.split(os.sep)[0]
    if rel_root!='.' and top in EXCL: dirs[:]=[]; continue
    if rel_root=='.': dirs[:]=[d for d in dirs if d not in EXCL]
    dirs[:]=[d for d in dirs if d not in ('__pycache__','node_modules','.git','shp','fotos')]
    for f in files:
        src=os.path.join(root,f); ext=os.path.splitext(f)[1].lower(); sz=os.path.getsize(src)
        ok = ext in TXT or (ext=='.html' and sz<400_000 and top not in ('tish',)) or (top=='dl3' and ext=='.pdf') or (top=='chk_imp')
        if f in ('ant1.json','ant2.json','gh_new.json','gh_user.json','tree_worker.json','combined.pem'): ok=False
        if ok and sz>20_000_000: ok=False
        if not ok:
            skipped[ext]=skipped.get(ext,0)+sz; continue
        rel=os.path.relpath(src,S); dst=os.path.join(K,'trabajo',rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
        shutil.copy2(src,dst); m+=1; t2+=sz
print('trabajo',m,t2//1e6,'MB')
print('omitidos por tipo (MB):',sorted(((round(v/1e6,1),k) for k,v in skipped.items()),reverse=True)[:15])
