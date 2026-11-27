"""Hace que la app copie videos a la biblioteca de GoHighLevel (TikTok solo acepta videos alojados ahí).
Importa piezas AUXILIARES en borrador (nunca se aprueban ni se publican), lee la URL de GHL y las descarta.
Uso: python3 -I copiar_a_ghl.py ID_PIEZA [ID_PIEZA...]"""
import json,os,re,sys,urllib.request,time
B=os.environ.get('PROG_DIR') or os.getcwd(); U='https://contenido.dgdesignmodeling.com'
out=f'{B}/ghl_videos.json'; done=json.load(open(out)) if os.path.exists(out) else {}
def call(path,method='GET',data=None,t=290):
    req=urllib.request.Request(U+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'},method=method)
    return json.load(urllib.request.urlopen(req,timeout=t))
ids=[i for i in sys.argv[1:] if i not in done]
piezas=[]
for i in ids:
    d=json.load(open(f'{B}/db/piezas/{i}.json')); d=d.get('data',d)
    v=next(e['u'] for e in d['enlaces'] if e['t'].startswith('Descargar video'))
    piezas.append({'id':f'aux-ghl-{i}','titulo':f'AUXILIAR · copiar video a GHL · NO PUBLICAR · {i}','formato':'reel','red_principal':'tiktok','caption':'Pieza auxiliar: solo copia el video a la biblioteca de GHL.','video':v,'fecha':d['fecha_iso']+'T15:00:00.000Z','redes':['tiktok']})
for p in piezas:
    r=call('/api/guiones/importar','POST',{'year':int(p['fecha'][:4]),'month':int(p['fecha'][5:7]),'guiones':{'generado':time.strftime('%Y-%m-%d'),'nota':'Auxiliares para copiar videos a GHL','piezas':[p]}})
    print('importar',p['id'],{k:r.get(k) for k in('ok','created','updated','skipped')},flush=True)
items=call('/api/contenido?status=draft',t=60)['items']
for it in items:
    t=json.dumps(it,ensure_ascii=False)
    m=re.search(r'aux-ghl-([a-z0-9-]+)',t)
    if not m: continue
    urls=sorted(set(re.findall(r'https://files\.leadconnectorhq\.com/[^"\\]+\.mp4',t)))
    pid=m.group(1)
    if urls: done[pid]=urls[0]; json.dump(done,open(out,'w'),indent=1)
    r=call('/api/contenido','PATCH',{'id':it['id'],'status':'descartado','rejectionComment':'Pieza auxiliar: solo servía para copiar el video a la biblioteca de GHL.'},t=60)
    print(pid,'ghl' if urls else 'SIN URL GHL','· descartada:',r.get('status'),flush=True)
print(len(done),'videos en GHL')
