"""Compara lo programado en el planificador (lectura guardada de get-posts) con plan.json.
Uso: python3 -I verificar.py ARCHIVO_LECTURA [ARCHIVO_LECTURA...]"""
import json,sys,os
B=os.environ.get('PROG_DIR') or os.getcwd()
plan=json.load(open(f'{B}/plan.json'))['posts']
def posts_de(path):
    t=open(path).read()
    try: d=json.loads(t)
    except Exception: return []
    out=[]
    def walk(o):
        if isinstance(o,dict):
            if isinstance(o.get('posts'),list): out.extend(o['posts']); return
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o:
                if isinstance(v,dict) and v.get('type')=='text' and isinstance(v.get('text'),str):
                    try: walk(json.loads(v['text']))
                    except Exception: pass
                else: walk(v)
        elif isinstance(o,str) and o.startswith('{'):
            try: walk(json.loads(o))
            except Exception: pass
    walk(d); return out
real=[]
for p in sys.argv[1:]: real+=posts_de(p)
real=[r for r in real if not r.get('deleted')]
idx={}
for r in real:
    for a in r.get('accountIds') or [r.get('accountId')]:
        idx.setdefault((a,(r.get('scheduleDate') or r.get('displayDate') or '')[:16]),[]).append(r)
ok=0;falt=[];dif=[];usados=set()
for p in plan:
    b=p['body']; k=(b['accountIds'][0],b['scheduleDate'][:16]); c=idx.get(k,[])
    m=[r for r in c if (r.get('summary') or '').strip()==b['summary'].strip()]
    if not c: falt.append(p['key']); continue
    r=(m or c)[0]; usados.add(r['_id']); probs=[]
    if (r.get('summary') or '').strip()!=b['summary'].strip(): probs.append('texto distinto')
    if [x['url'] for x in r.get('media') or []]!=[x['url'] for x in b['media']]: probs.append('medios distintos')
    if r.get('status')!='scheduled': probs.append('estado '+str(r.get('status')))
    if r.get('type')!=b['type']: probs.append(f"tipo {r.get('type')}≠{b['type']}")
    if len(c)>1 and len(m)>1: probs.append(f'DUPLICADO x{len(m)}')
    if probs: dif.append((p['key'],probs))
    else: ok+=1
extra=[(r.get('platform'),(r.get('scheduleDate') or '')[:16],(r.get('summary') or '')[:50]) for r in real if r['_id'] not in usados]
print('leídos',len(real),'· plan',len(plan),'· coinciden',ok)
print('FALTAN',falt); print('DIFERENCIAS',dif); print('FUERA DEL PLAN',extra[:20])
