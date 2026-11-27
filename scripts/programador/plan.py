"""Arma el plan de publicaciones del planificador de GoHighLevel a partir de las fichas aprobadas.

Uso: PROG_DIR=<carpeta de trabajo> PROG_PREFIJO=dic26 python3 -I plan.py DESDE HASTA   (AAAA-MM-DD)

Lee de la carpeta de trabajo: db/piezas/*.json y db/respuestas/*.json (fichas y aprobaciones bajadas del
artefacto de aprobación), cuentas.json (ids de las cuentas del planificador), horas.json (hora por pieza),
img_urls.json (imagen -> enlace público), ghl_videos.json (video alojado en GoHighLevel, para TikTok) y,
si existe, retener.json (lista de textos: la pieza cuyo id o contenido los contenga queda retenida).
Escribe plan.json (peticiones listas), plan.txt (para revisar a ojo) y la carpeta cola/."""
import json,glob,os,re,sys
B=os.environ.get('PROG_DIR') or os.getcwd()
PREF=os.environ.get('PROG_PREFIJO','mes')
RET=json.load(open(f'{B}/retener.json')) if os.path.exists(f'{B}/retener.json') else []
DESDE,HASTA=sys.argv[1],sys.argv[2]
CU=json.load(open(f'{B}/cuentas.json'))
ACC={'instagram':CU['instagram:design_modeling_dg'],'facebook':CU['facebook:Design Modeling Academy'],'threads':CU['threads:design_modeling_dg'],
     'linkedin':CU['linkedin:Design Modeling Academy'],'tiktok':CU['tiktok:Design Modeling Academy'],'youtube':CU['youtube:Design Modeling Academy']}
USER=os.environ.get('PROG_USUARIO','zpcSqe5U2qoCbNYqDocu')  # usuario de integración con el que ya publica la app
HORAS=json.load(open(f'{B}/horas.json'))
IMG=json.load(open(f'{B}/img_urls.json')) if os.path.exists(f'{B}/img_urls.json') else {}
GHLVID=json.load(open(f'{B}/ghl_videos.json')) if os.path.exists(f'{B}/ghl_videos.json') else {}
P={};R={}
for f in glob.glob(f'{B}/db/piezas/*.json'):
    d=json.load(open(f)); d=d.get('data',d); P[d['id']]=d
for f in glob.glob(f'{B}/db/respuestas/*.json'):
    d=json.load(open(f)); R[os.path.basename(f)[:-5]]=d.get('data',d)
CTA=re.compile(r'[Cc]omenta\s+[A-ZÁÉÍÓÚÑ]{3,}')
def paras(t): return [p.strip() for p in re.split(r'\n\s*\n',t.strip()) if p.strip()]
def sin_cta(t): return '\n\n'.join(p for p in paras(t) if not CTA.search(p))
def para_threads(t,lim=500):
    ps=[p for p in paras(t) if not CTA.search(p) and not p.lstrip().startswith('#')]
    if not ps: return ''
    q=[i for i,p in enumerate(ps) if '?' in p]
    keep={0}; 
    if q: keep.add(q[-1])
    def txt(k): return '\n\n'.join(ps[i] for i in sorted(k))
    for i in range(1,len(ps)):
        if i in keep: continue
        if len(txt(keep|{i}))<=lim: keep.add(i)
        else: break
    s=txt(keep)
    if len(s)>lim:
        s=ps[0] if len(ps[0])<=lim else ps[0][:lim-1].rsplit(' ',1)[0]+'…'
    return s
def img_urls(d):
    out=[]
    for im in d.get('imagenes') or []:
        a=im['u'].split('/')[-1]
        out.append(IMG.get(a) or f'FALTA:{a}')
    return out
def vid_url(d):
    for e in d.get('enlaces') or []:
        if e['t'].startswith('Descargar video'): return e['u']
    for e in d.get('enlaces') or []:
        if e['t'].startswith('Ver video'): return e['u']
    return None
def M(urls,typ): return [{'url':u,'type':typ} for u in urls]
posts=[];manual=[];hold=[]
def add(d,red,when,typ,summary,media,extra=None,nota=''):
    body={'accountIds':[ACC[red]],'summary':summary,'media':media,'status':'scheduled','scheduleDate':when,'type':typ,'userId':USER}
    body.update(extra or {})
    posts.append({'key':f"{PREF}-{d['id']}-{red}",'pieza':d['id'],'fecha':d['fecha_iso'],'red':red,'nota':nota,'body':body})
for d in sorted(P.values(),key=lambda d:(d['fecha_iso'],d.get('orden') or 999)):
    if not (DESDE<=d['fecha_iso']<=HASTA): continue
    g=d['grupo']; ep=d['estado_prod']; i=d['id']
    if g in ('pauta','correos','comunidades','blog'): continue
    if ep.startswith(('DESCARTADA','YA ESCRITA','EN RESERVA')): continue
    if ep.startswith('POR GRABAR'): manual.append((i,d['fecha'],'Falta grabar (Gabriel)')); continue
    if g=='historias': manual.append((i,d['fecha'],'Historia: se publica a mano por los stickers'+(' · GRABA GABRIEL' if d.get('graba_gabriel') else ''))); continue
    blob=json.dumps(d,ensure_ascii=False)
    if any(r in i or r in blob for r in RET): hold.append((i,d['fecha'],'Retenida (retener.json)')); continue
    cap=d.get('caption') or ''; fmt=d['formato']; redes=d.get('redes') or []
    day=d['fecha_iso']
    if g=='feed':
        when=(HORAS.get(i) or [f'{day}T15:00:00Z'])[0].replace('Z','.000Z')
        v=vid_url(d); imgs=img_urls(d)
        es_reel=bool(v) and not imgs
        for red in redes:
            if red in('instagram','facebook'):
                if es_reel: add(d,red,when,'reel',cap,M([v],'video/mp4'),{f'{red}PostDetails':({'type':'reel','showOnFeed':True} if red=='instagram' else {'type':'reel'})})
                else:
                    media=M(imgs[:10] if red=='instagram' else imgs,'image/jpeg'); nota=''
                    if v and red=='instagram': media=media+M([v],'video/mp4'); nota='carrusel: imagen + video del testimonio'
                    add(d,red,when,'post',cap,media,{f'{red}PostDetails':{'type':'post'}},nota)
            elif red=='threads':
                add(d,red,when,'post',para_threads(cap),M([v],'video/mp4') if es_reel else M(imgs,'image/jpeg'))
            elif red=='tiktok' and es_reel:
                gv=GHLVID.get(i)
                add(d,red,when,'reel',sin_cta(cap),M([gv or 'FALTA_GHL:'+i],'video/mp4'),{'tiktokPostDetails':{'privacyLevel':'PUBLIC_TO_EVERYONE','enableComment':True,'enableDuet':False,'enableStitch':False}})
            elif red=='youtube' and es_reel:
                add(d,red,when,'reel',sin_cta(cap),M([v],'video/mp4'),{'youtubePostDetails':{'title':d['titulo'][:100],'type':'short','privacyLevel':'public'}})
    elif g=='shorts':
        when=f'{day}T23:00:00.000Z'; v=vid_url(d)
        add(d,'youtube',when,'reel',cap,M([v],'video/mp4'),{'youtubePostDetails':{'title':d['titulo'][:100],'type':'short','privacyLevel':'public'}})
        capig=re.sub(r'#Shorts\s*','',cap).strip()
        add(d,'instagram',when,'reel',capig,M([v],'video/mp4'),{'instagramPostDetails':{'type':'reel','showOnFeed':True}},'sin #Shorts')
    elif g=='youtube':
        when=f'{day}T15:00:00.000Z'; v=vid_url(d); th=img_urls(d)
        m=M([v],'video/mp4'); 
        if th: m[0]['thumbnail']=th[0]
        add(d,'youtube',when,'post',cap,m,{'youtubePostDetails':{'title':d['titulo'][:100],'type':'video','privacyLevel':'public'}})
    elif g=='linkedin':
        if not fmt.startswith('Página Design Modeling Academy'):
            manual.append((i,d['fecha'],'LinkedIn: '+fmt[:60])); continue
        when=f'{day}T13:00:00.000Z'; extra={}
        for gline in d.get('guion') or []:
            mm=re.match(r'Primer comentario[^:]*:\s*(.+)',gline,re.S)
            if mm: extra['followUpComment']=mm.group(1).strip()
        if d.get('pdf'): extra['linkedinPostDetails']={'postAsPdf':True,'pdfTitle':d['titulo'][:100]}
        add(d,'linkedin',when,'post',cap,M(img_urls(d)[:300 if d.get('pdf') else 9],'image/jpeg'),extra)
json.dump({'posts':posts,'manual':manual,'hold':hold},open(f'{B}/plan.json','w'),ensure_ascii=False,indent=1)
with open(f'{B}/plan.txt','w') as f:
    for p in posts:
        b=p['body']; f.write(f"\n### {p['key']} · {b['scheduleDate']} · {b['type']} · media {len(b['media'])} · {p['nota']}\n")
        f.write('media: '+' | '.join(m['url'][-48:] for m in b['media'])+'\n')
        for k in ('youtubePostDetails','followUpComment','linkedinPostDetails'):
            if k in b: f.write(f"{k}: {json.dumps(b[k],ensure_ascii=False)}\n")
        f.write(f"({len(b['summary'])} car.) {b['summary']}\n")
hechos=set(json.load(open(f'{B}/hechos.json'))) if os.path.exists(f'{B}/hechos.json') else set()
os.makedirs(f'{B}/cola',exist_ok=True)
for f in os.listdir(f'{B}/cola'): os.remove(f'{B}/cola/{f}')
n=0
for p in posts:
    if p['key'] in hechos or any('FALTA' in m['url'] for m in p['body']['media']): continue
    n+=1
    json.dump({'operationId':'create-post','idempotencyKey':p['key'],'reason':f"Programar {p['pieza']} en {p['red']} (matriz aprobada por Dayana)",'params':{'body':p['body']}},open(f"{B}/cola/{n:03d}-{p['key']}.json",'w'),ensure_ascii=False)
print('posts',len(posts),'manual',len(manual),'hold',len(hold),'· en cola',n)
bad=[p['key'] for p in posts if any('FALTA' in m['url'] or not m['url'] for m in p['body']['media']) or not p['body']['media']]
print('con faltantes:',bad)
lims={'threads':500,'instagram':2200,'tiktok':2200,'linkedin':3000,'youtube':5000,'facebook':60000}
print('exceden:',[(p['key'],len(p['body']['summary'])) for p in posts if len(p['body']['summary'])>lims[p['red']]])
for m in manual: print(' MANUAL',m)
for m in hold: print(' HOLD',m)
