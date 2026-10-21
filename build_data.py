import json,re
A='/workspace/reading-archive/'
def r(p): return open(p,encoding='utf-8').read().rstrip('\n')
def first(t): return t.split('\n',1)[0].strip()
items=[
 ('2026-10-21','06:08','晨读',A+'morning/2026-10-21.txt',None),
 ('2026-10-20','06:11','晨读',A+'morning/2026-10-20.txt',None),
 ('2026-10-21','10:11','30u30',A+'30u30/day03.txt',None),
 ('2026-10-20','10:00','30u30',A+'30u30/day02.txt','日期/时间为推断（progress.json 只记录了第3天 10-21 10:11 发出）'),
 ('2026-10-21','12:04','午读',A+'noon/ep05.txt',None),
 ('2026-10-20','12:05','午读',A+'noon/ep04.txt',None),
 ('2026-10-17','12:12','午读',A+'noon/ep03.txt',None),
 ('2026-10-16','12:18','午读',A+'noon/ep02.txt',None),
 ('2026-10-16','11:26','午读',A+'noon/ep01.txt',None),
 ('2026-10-21','19:00','夜读',A+'night/2026-10-21.txt',None),
 ('2026-10-20','19:05','夜读',A+'night/2026-10-20.txt',None),
 ('2026-10-17','19:09','夜读','/workspace/night/beiying_paras.txt','正文取自选文原稿 beiying_paras.txt；当日实际发出的完整消息（含标题/导语）未存档，可能与此略有出入'),
 ('2026-10-16','19:19','夜读','/workspace/night/excerpt_xiaowangzi_ch21.txt','正文取自选文原稿 excerpt_xiaowangzi_ch21.txt；当日实际发出的完整消息未存档，可能与此略有出入'),
]
titles={'/workspace/night/beiying_paras.txt':'夜读 · 2026.10.17　朱自清《背影》','/workspace/night/excerpt_xiaowangzi_ch21.txt':'夜读 · 2026.10.16　《小王子》第21章·狐狸（周克希译）'}
out=[]
for d,t,c,p,note in items:
  b=r(p); ti=titles.get(p)
  if not ti:
    ti=first(b)
    if ti=='标题': ti='午读｜'+b.split('\n')[1].strip()
    m=re.search(r'第(\d+)集',ti)
    if c=='午读' and m: ti=f'午读 Ep.{m.group(1)}｜'+b.split('\n')[1].strip()
    if c=='夜读': ti=ti+'　'+[l for l in b.split('\n')[1:] if l.strip()][0].strip()
  e=dict(id=f'{d}-{c}'+('-trial' if p.endswith('ep01.txt') else ''),date=d,time=t,category=c,title=ti,body=b)
  if note: e['note']=note
  out.append(e)
out.sort(key=lambda e:(e['date'],e['time']),reverse=True)
json.dump(out,open('data/pushes.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
