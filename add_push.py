#!/usr/bin/env python3
"""Append/replace one push in data/pushes.json (dedupe by date+category), then redeploy.
Usage: add_push.py [--image card.png] --date 2026-10-22 --time 19:00 --category 夜读 --title "..." --body-file path [--no-deploy]
Deploy hook: if /workspace/push-site/deploy.sh exists and is executable, it is run."""
import argparse,json,os,subprocess,sys,tempfile
H=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(H,'data','pushes.json')
a=argparse.ArgumentParser()
for k in ('date','time','category','title','body-file'): a.add_argument('--'+k,required=True)
a.add_argument('--image',help='card png/jpg; converted to img/<id>.webp at original size')
a.add_argument('--no-deploy',action='store_true'); o=a.parse_args()
body=open(o.body_file,encoding='utf-8').read().rstrip('\n')
data=json.load(open(P,encoding='utf-8')) if os.path.exists(P) else []
e=dict(id=f'{o.date}-{o.category}',date=o.date,time=o.time,category=o.category,title=o.title,body=body)
if o.image:
    sys.path.insert(0,H); from webpconv import convert
    os.makedirs(os.path.join(H,'img'),exist_ok=True)
    rel=f"img/{e['id']}.webp"; dst=os.path.join(H,rel)
    if not (os.path.exists(dst) and os.path.getmtime(dst)>=os.path.getmtime(o.image)):
        r=convert(o.image,dst); print('image',rel,r)
    from PIL import Image
    w,h=Image.open(dst).size; e.update(image=rel,image_w=w,image_h=h)
old=[x for x in data if x['date']==o.date and x['category']==o.category and not x['id'].endswith('-trial')]
if old and all(x.get('title')==e['title'] and x.get('body')==body and x.get('time')==o.time and x.get('image')==e.get('image') for x in old):
    print('unchanged:',e['id']); changed=False
else:
    data=[x for x in data if x not in old]+[e]; changed=True
    data.sort(key=lambda x:(x['date'],x['time']),reverse=True)
    fd,tmp=tempfile.mkstemp(dir=os.path.dirname(P)); 
    with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=1)
    os.replace(tmp,P); print('replaced' if old else 'added',e['id'],'total',len(data))
d=os.path.join(H,'deploy.sh')
if changed and not o.no_deploy and os.access(d,os.X_OK):
    sys.exit(subprocess.call([d],cwd=H))
