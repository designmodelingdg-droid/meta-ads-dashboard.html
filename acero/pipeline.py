"""Arma lecciones cortas de la Especialización de Acero dentro de GitHub Actions.
Uso: python3 acero/pipeline.py 1-20   (números de lección de acero/plan.json)
Solo LEE de Vimeo. Cada lección sale cifrada con acero/cert.pem (solo se abre con la llave privada, que no está en el repo)."""
import json, os, re, subprocess, sys, unicodedata
AQ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQ, '..', 'scripts'))
from vimeo_clips import api, elegir_archivo  # noqa: E402

def rango(s):
    out = []
    for p in s.split(','):
        a, _, b = p.partition('-'); out += list(range(int(a), int(b or a) + 1))
    return out

def slug(t):
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t)).strip('-')

P = json.load(open(os.path.join(AQ, 'plan.json')))
W = os.path.abspath('trabajo'); os.makedirs(W, exist_ok=True)
for d in ['plan', 'tramos', 'portadas', 'fonts', 'tmpB', 'out']: os.makedirs(os.path.join(W, d), exist_ok=True)
subprocess.run(f'cp {AQ}/portadas/* {W}/portadas/ && cp {AQ}/fonts/* {W}/fonts/ && cp {AQ}/cur_*.png {AQ}/version_b.py {AQ}/enc2.py {W}/', shell=True, check=True)
L = {l['n']: l for l in P['lecciones']}
sel = [n for n in rango(sys.argv[1]) if n in L]
links = {}
cu = {'curso': P['curso'], 'modulos': P['modulos'], 'lecciones': []}; ref = {}; mute = {}
for n in sel:
    l = L[n]; segs = []
    for k, (vid, a, b) in enumerate(l['segs']):
        if vid not in links:
            links[vid] = elegir_archivo(api(f'/videos/{vid}?fields=name,duration,download,files'))[0]
        tr = f'{n:03d}_{k}'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', links[vid], '-vf', 'scale=1280:720',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-c:a', 'aac', '-b:a', '128k', f'{W}/tramos/{tr}.mp4'], check=True)
        segs.append([tr, 0, round(b - a, 2)])
    cu['lecciones'].append(l); ref[str(n)] = segs
    if l.get('mute'): mute[f'{n:03d}'] = l['mute']
json.dump(cu, open(f'{W}/plan/curso.json', 'w'), ensure_ascii=False)
json.dump(ref, open(f'{W}/plan/refinado.json', 'w')); json.dump(mute, open(f'{W}/plan/mute.json', 'w'))
# portadas
js = """const {chromium}=require('playwright');const C=require('./plan/curso.json');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
for(const l of C.lecciones){const n=String(l.n).padStart(3,'0');const m='Módulo '+l.mod+' · '+C.modulos[l.mod-1];
await p.goto('file://'+__dirname+'/portadas/portada.html?n='+String(l.n).padStart(2,'0')+'&m='+encodeURIComponent(m)+'&t='+encodeURIComponent(l.t)+'&c='+encodeURIComponent(C.curso)+'&i='+encodeURIComponent(l.instr||''));
await p.waitForTimeout(300);await p.screenshot({path:__dirname+'/portadas/p'+n+'.png'});}
await b.close();})();"""
open(f'{W}/render.cjs', 'w').write(js)
subprocess.run(['node', 'render.cjs'], cwd=W, check=True)
for n in sel:
    l = L[n]; les = f'{n:03d}'; name = f'acero-{les}-{slug(l["t"])}.mp4'
    subprocess.run(['python3', 'version_b.py', les], cwd=W, check=True)
    subprocess.run(['python3', 'enc2.py', f'tmpB/{les}hq.mkv', f'tmpB/{name}'], cwd=W, check=True)
    subprocess.run(['openssl', 'cms', '-encrypt', '-binary', '-aes256', '-in', f'tmpB/{name}', '-outform', 'DER', '-out', f'out/{name}.cms', os.path.join(AQ, 'cert.pem')], cwd=W, check=True)
    subprocess.run(f'rm -f tmpB/{les}mid.mkv tmpB/{les}hq.mkv tmpB/{name} tramos/{les}_*.mp4', shell=True, cwd=W)
    print('LISTA', name, flush=True)
