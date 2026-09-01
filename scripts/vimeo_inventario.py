#!/usr/bin/env python3
"""Inventario para el tutor de la Especializacion en Acero.

Paso 1 del piloto (GO de Dayana, 04-sep-2026): casar cada video de Vimeo con
los cuatro cursos del paquete y saber que transcripcion tiene cada uno. El
portal es solo video —comprobado con Ask AI, cero PDF y cero texto— asi que
esta lista ES el indice de todo el material que el tutor puede saber.

Estrategia: primero las CARPETAS de Vimeo (si el equipo organizo por curso, el
mapeo ya existe y no se adivina); lo que no aparezca por carpeta se busca por
palabras del nombre. Solo lectura. Respeta el limite de 500 peticiones/hora.

    VIMEO_TOKEN=xxx python3 scripts/vimeo_inventario.py
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import date

TOKEN = os.environ.get('VIMEO_TOKEN','').strip()
if not TOKEN: sys.exit('ERROR: falta VIMEO_TOKEN.')
API='https://api.vimeo.com'
SALIDA_JSON='matriz-viral/fuentes/vimeo-inventario-acero.json'
SALIDA_MD  ='matriz-viral/fuentes/vimeo-inventario-acero.md'
TOPE_VIDEOS=140   # techo de cortesia para no comerse el limite de la API

CURSOS = {
  "estructuras-complejas": {
    "nombre": "Análisis y Diseño Simplificado de Estructuras Complejas de Acero",
    "claves": ["complejas", "acero-dm", "sesión n°"],   # las Sesión N°X-Acero-DM
  },
  "cerchas-naves": {
    "nombre": "Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales",
    "claves": ["cercha", "nave"],
  },
  "uniones": {
    "nombre": "Teoría y Cálculo de Uniones Metálicas en Edificaciones",
    "claves": ["union", "unione", "conexion", "conexión"],
  },
  "modelado-bim": {
    "nombre": "Modelado BIM en Hormigón Armado y Acero Estructural",
    "claves": ["modelado"],
  },
}

pedidas=0
def api(ruta):
    global pedidas; pedidas+=1
    r=urllib.request.Request(API+ruta, headers={
        'Authorization':f'Bearer {TOKEN}',
        'Accept':'application/vnd.vimeo.*+json;version=3.4'})
    with urllib.request.urlopen(r, timeout=40) as x:
        return json.load(x)

def paginar(ruta, campos, tope=200):
    out=[]; pagina=1
    sep = '&' if '?' in ruta else '?'
    while len(out)<tope:
        d=api(f'{ruta}{sep}per_page=100&page={pagina}&fields={campos}')
        out+=d.get('data',[])
        if not d.get('paging',{}).get('next'): break
        pagina+=1
    return out[:tope]

def norm(s): return (s or '').lower()

# ── 1 · carpetas ─────────────────────────────────────────────────────
print('→ Carpetas de la cuenta…')
carpetas = paginar('/me/projects','uri,name')
print(f'  {len(carpetas)} carpetas')
for c in carpetas: print('   ·', c['name'])

def carpeta_de(curso):
    n=norm(CURSOS[curso]['nombre']); claves=CURSOS[curso]['claves']
    for c in carpetas:
        cn=norm(c['name'])
        if cn and (cn in n or any(k in cn for k in claves)):
            return c
    return None

# ── 2 · videos por curso ─────────────────────────────────────────────
inventario={}; total=0
for clave,info in CURSOS.items():
    vids=[]; origen=None
    c=carpeta_de(clave)
    if c:
        origen=f"carpeta «{c['name']}»"
        vids=paginar(f"/me/projects/{c['uri'].split('/')[-1]}/videos","uri,name,duration")
    if not vids:
        origen="búsqueda por nombre"
        vistos=set()
        for k in info['claves']:
            for v in paginar(f'/me/videos?query={urllib.parse.quote(k)}',"uri,name,duration",60):
                if v['uri'] not in vistos:
                    vistos.add(v['uri']); vids.append(v)
    inventario[clave]={"curso":info['nombre'],"origen":origen,"videos":vids}
    total+=len(vids)
    print(f'→ {clave}: {len(vids)} videos ({origen})')

# ── 3 · transcripciones ──────────────────────────────────────────────
print(f'→ Comprobando pistas de texto ({min(total,TOPE_VIDEOS)} videos)…')
revisados=0
for clave,d in inventario.items():
    for v in d['videos']:
        if revisados>=TOPE_VIDEOS:
            v['pistas']=None; continue
        revisados+=1
        try:
            tt=api(f"/videos/{v['uri'].split('/')[-1]}/texttracks").get('data',[])
            v['pistas']=len(tt)
            v['idioma']=tt[0].get('language') if tt else None
        except Exception as e:
            v['pistas']=None; v['error']=str(e)[:60]

# ── 4 · salida ───────────────────────────────────────────────────────
res={"generado":date.today().isoformat(),"peticiones_api":pedidas,
     "carpetas_en_cuenta":[c['name'] for c in carpetas],
     "cursos":inventario}
os.makedirs(os.path.dirname(SALIDA_JSON),exist_ok=True)
json.dump(res,open(SALIDA_JSON,'w',encoding='utf-8'),ensure_ascii=False,indent=1)

L=[f"# Inventario Vimeo · Especialización en Acero — {res['generado']}\n"]
tot_v=tot_t=0
for clave,d in inventario.items():
    con=sum(1 for v in d['videos'] if (v.get('pistas') or 0)>0)
    tot_v+=len(d['videos']); tot_t+=con
    L.append(f"## {d['curso']}\n")
    L.append(f"_{len(d['videos'])} videos · {con} con transcripción · fuente: {d['origen']}_\n")
    L.append("| ✓ | min | Video |\n|---|---|---|")
    for v in sorted(d['videos'], key=lambda x:norm(x.get('name'))):
        m=round((v.get('duration') or 0)/60)
        marca='✅' if (v.get('pistas') or 0)>0 else ('❌' if v.get('pistas')==0 else '·')
        L.append(f"| {marca} | {m} | {v.get('name','?')[:70]} |")
    L.append("")
L.append(f"**Total: {tot_v} videos · {tot_t} con transcripción · "
         f"{tot_v-tot_t} sin ella.**\n")
L.append("Los ❌ necesitan que Vimeo les genere subtítulos (se activan en el "
         "video) antes de poder entrar al índice del tutor.")
open(SALIDA_MD,'w',encoding='utf-8').write('\n'.join(L))
print(f'\n  {tot_v} videos · {tot_t} con transcripcion · {pedidas} peticiones API')
print(f'  guardado en {SALIDA_MD}')
