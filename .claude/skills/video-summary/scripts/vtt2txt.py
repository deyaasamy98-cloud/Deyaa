import re,sys,html
src,out=sys.argv[1],sys.argv[2]
txt=open(src,encoding='utf-8').read()
res=[];seen=set();last=None
for b in re.split(r'\n\n+',txt):
    m=re.search(r'(\d+):(\d+):(\d+)\.\d+ -->',b)
    if not m: continue
    t=int(m[1])*3600+int(m[2])*60+int(m[3])
    for l in b.split('\n')[1:]:
        if '-->' in l: continue
        l=html.unescape(re.sub(r'<[^>]+>','',l)).strip()
        if l and l!=last and l not in seen:
            seen.add(l); res.append((t,l)); last=l
o=open(out,'w',encoding='utf-8'); mark=-999
for t,l in res:
    if t-mark>=90:
        o.write(f"\n[{t//60}:{t%60:02d}] "); mark=t
    o.write(l+' ')
