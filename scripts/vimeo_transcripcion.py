#!/usr/bin/env python3
"""¿Las clases tienen transcripcion, y el texto aguanta solo?

De esto depende la opcion A del plan de IA en cursos: un asistente anclado al
material del curso necesita ese material en texto. Si Vimeo ya genero
subtitulos automaticos, el material existe y no hay que regrabar ni
transcribir nada. Si no, hay un paso previo (activar subtitulos o transcribir
aparte) y conviene saberlo ANTES de disenar nada.

Busca videos cuyo nombre suene a la Especializacion en Acero, mira cuales
tienen pistas de texto, y guarda una MUESTRA de una transcripcion para poder
juzgar la calidad con los ojos — una clase de "modelar en pantalla senalando"
puede transcribir en puro «aqui, esto, aca» y no servir sola.

    VIMEO_TOKEN=xxx python3 scripts/vimeo_transcripcion.py
"""
import json, os, re, sys, urllib.request

TOKEN = os.environ.get('VIMEO_TOKEN','').strip()
if not TOKEN: sys.exit('ERROR: falta VIMEO_TOKEN.')
API='https://api.vimeo.com'
SALIDA='matriz-viral/fuentes/vimeo-transcripcion-muestra.md'

def api(ruta):
    r=urllib.request.Request(API+ruta, headers={
        'Authorization':f'Bearer {TOKEN}',
        'Accept':'application/vnd.vimeo.*+json;version=3.4'})
    with urllib.request.urlopen(r, timeout=40) as x:
        return json.load(x)

def bajar(url):
    with urllib.request.urlopen(urllib.request.Request(url), timeout=60) as x:
        return x.read().decode('utf-8','replace')

candidatos=[]
for q in ('acero','especializacion acero','conexiones'):
    try:
        d=api(f'/me/videos?query={urllib.request.quote(q)}&per_page=10&fields=uri,name,duration')
        candidatos+= d.get('data',[])
    except Exception as e:
        print(f'  busqueda «{q}» fallo: {e}')
vistos=set(); unicos=[]
for v in candidatos:
    if v['uri'] not in vistos:
        vistos.add(v['uri']); unicos.append(v)
print(f'Videos que suenan a acero: {len(unicos)}')

filas=[]; muestra=None; con=0
for v in unicos[:12]:
    vid=v['uri'].split('/')[-1]
    try:
        tt=api(f'/videos/{vid}/texttracks').get('data',[])
    except Exception as e:
        filas.append((v['name'],'?',str(e)[:40])); continue
    tipos=', '.join(f"{t.get('type')}/{t.get('language')}" for t in tt) or '—'
    filas.append((v['name'], len(tt), tipos))
    if tt: con+=1
    if tt and muestra is None and tt[0].get('link'):
        vtt=bajar(tt[0]['link'])
        # quitar tiempos y numeros del VTT: dejar solo el habla
        texto=' '.join(l for l in vtt.splitlines()
                       if l and '-->' not in l and not l.strip().isdigit()
                       and not l.startswith(('WEBVTT','NOTE','STYLE')))
        texto=re.sub(r'<[^>]+>','',texto)
        muestra=(v['name'], texto[:2500])

for n,k,t in filas:
    print(f'  {str(k):>2} pistas · {t[:28]:28} · {n[:52]}')
print(f'\nCon transcripcion: {con} de {len(filas)} revisados')

L=[f'# Muestra de transcripcion de Vimeo — {con}/{len(filas)} clases de acero con pistas de texto\n']
L.append('| Pistas | Tipo | Clase |\n|---|---|---|')
for n,k,t in filas: L.append(f'| {k} | {t[:30]} | {n[:60]} |')
if muestra:
    L.append(f'\n## Muestra: «{muestra[0]}»\n\n> {muestra[1]}\n')
    L.append('\n**Como juzgarla:** si se entiende de que habla sin ver la pantalla, '
             'la opcion A va directo. Si es puro «aqui, esto, le damos clic aca», '
             'el texto solo no basta y el asistente necesita tambien los PDF/laminas del curso.')
else:
    L.append('\n**Ninguno de los revisados tiene pista de texto.** Antes de la opcion A '
             'hay que activar los subtitulos automaticos de Vimeo (o transcribir aparte).')
os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
open(SALIDA,'w',encoding='utf-8').write('\n'.join(L))
print(f'muestra guardada en {SALIDA}')
