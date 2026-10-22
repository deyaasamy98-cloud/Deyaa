# usage: add_row.py NN "title" "pdf name without .pdf" "source label" "source url" "artifact url"
import sys
nn,title,pdf,label,src,art=sys.argv[1:7]
import os
p=os.path.join(os.environ.get('SUMMARIES_DIR','ملخصات'),'README.md')
t=open(p,encoding='utf-8').read()
row=f'| {nn} | [{title}](<{pdf}.pdf>) | [{label}]({src}) | [فتح]({art}) |\n'
prev=f'| {int(nn)-1:02d} |'
i=t.index(prev); j=t.index('\n',i)+1
open(p,'w',encoding='utf-8').write(t[:j]+row+t[j:])
