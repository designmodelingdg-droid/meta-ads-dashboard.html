#!/usr/bin/env python3
"""Clips de clases desde Vimeo, para reels de prueba social.

Pedido de Dayana (7-oct-2026): sacar «cachitos» de las clases grabadas para que
la gente vea lo que se da en los cursos. Dos modos, en este orden:

  transcribir  Busca las clases de un tema (por nombre o por carpeta) y guarda
               su transcripción automática de Vimeo (.vtt) más un índice. Con eso
               se eligen los momentos leyendo, sin bajar horas de video.
  recortar     Baja SOLO el tramo elegido (desde/hasta) de un video, en 720p,
               listo para editar como reel.

Todo lo que produce va a la rama `vimeo-clips` (nunca a la rama principal):
    vimeo-clips/<tema>/indice.md · <id>.vtt · <id>.txt
    vimeo-clips/recortes/<id>_<desde>-<hasta>.mp4

Solo LEE de Vimeo: no cambia privacidad, títulos ni nada de ningún video.
Respeta el límite de 500 peticiones/hora. El token nunca se imprime.

    VIMEO_TOKEN=xxx python3 scripts/vimeo_clips.py transcribir --tema conexiones
    VIMEO_TOKEN=xxx python3 scripts/vimeo_clips.py recortar --video 123456 --desde 12:30 --hasta 13:20
"""
import argparse, json, os, re, subprocess, sys, unicodedata, urllib.parse, urllib.request
from datetime import date

TOKEN = os.environ.get('VIMEO_TOKEN', '').strip()
if not TOKEN:
    sys.exit('ERROR: falta VIMEO_TOKEN.')
API = 'https://api.vimeo.com'
SALIDA = os.environ.get('SALIDA', 'vimeo-clips')
pedidas = 0


def api(ruta):
    global pedidas
    pedidas += 1
    r = urllib.request.Request(API + ruta, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/vnd.vimeo.*+json;version=3.4'})
    with urllib.request.urlopen(r, timeout=40) as x:
        restantes = x.headers.get('X-RateLimit-Remaining')
        if restantes and int(restantes) < 20:
            print(f'  AVISO: quedan {restantes} peticiones a la API esta hora')
        return json.load(x)


def bajar_texto(url):
    with urllib.request.urlopen(urllib.request.Request(url), timeout=60) as x:
        return x.read().decode('utf-8', 'replace')


def paginar(ruta, campos, tope=200):
    out, pagina = [], 1
    sep = '&' if '?' in ruta else '?'
    while len(out) < tope:
        d = api(f'{ruta}{sep}per_page=100&page={pagina}&fields={campos}')
        out += d.get('data', [])
        if not d.get('paging', {}).get('next'):
            break
        pagina += 1
    return out[:tope]


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or 'tema'


def a_segundos(t):
    """Acepta 75, 1:15 o 1:01:15."""
    p = [float(x) for x in str(t).strip().split(':')]
    s = 0.0
    for v in p:
        s = s * 60 + v
    return s


def hms(s):
    s = int(round(s))
    return f'{s // 3600:d}:{s % 3600 // 60:02d}:{s % 60:02d}' if s >= 3600 else f'{s // 60:d}:{s % 60:02d}'


def vtt_a_texto(vtt):
    """Texto por bloques de ~30 s con su minuto, para leer rápido."""
    bloques, actual, inicio = [], [], None
    for m in re.finditer(r'(\d+:)?(\d+):(\d+)[.,]\d+ --> [^\n]+\n(.+?)(?:\n\n|\Z)', vtt, re.S):
        h = int((m.group(1) or '0:')[:-1])
        seg = h * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        txt = ' '.join(m.group(4).split())
        if inicio is None:
            inicio = seg
        if seg - inicio >= 30 and actual:
            bloques.append(f'[{hms(inicio)}] ' + ' '.join(actual))
            actual, inicio = [], seg
        actual.append(txt)
    if actual:
        bloques.append(f'[{hms(inicio or 0)}] ' + ' '.join(actual))
    return '\n'.join(bloques)


def transcribir(tema, carpeta, maximo):
    destino = os.path.join(SALIDA, slug(carpeta or tema))
    os.makedirs(destino, exist_ok=True)
    vids, origen = [], ''
    if carpeta:
        cs = [c for c in paginar('/me/projects', 'uri,name') if c['name'].strip().lower() == carpeta.strip().lower()]
        if cs:
            origen = f"carpeta «{cs[0]['name']}»"
            vids = paginar(f"/me/projects/{cs[0]['uri'].split('/')[-1]}/videos", 'uri,name,duration,created_time', maximo)
        else:
            print(f'  AVISO: no encontré la carpeta «{carpeta}»; busco por nombre')
    if not vids and tema:
        origen = f'búsqueda «{tema}»'
        vids = paginar(f'/me/videos?query={urllib.parse.quote(tema)}&sort=relevant', 'uri,name,duration,created_time', maximo)
    vids = vids[:maximo]
    print(f'→ {len(vids)} videos ({origen})')

    filas = []
    for v in vids:
        vid = v['uri'].split('/')[-1]
        fila = {'id': vid, 'nombre': v['name'], 'min': round((v.get('duration') or 0) / 60), 'pista': None}
        try:
            tt = api(f'/videos/{vid}/texttracks').get('data', [])
            if tt:
                vtt = bajar_texto(tt[0]['link'])
                open(os.path.join(destino, f'{vid}.vtt'), 'w', encoding='utf-8').write(vtt)
                open(os.path.join(destino, f'{vid}.txt'), 'w', encoding='utf-8').write(vtt_a_texto(vtt))
                fila['pista'] = tt[0].get('language') or tt[0].get('type')
        except Exception as e:
            fila['error'] = str(e)[:80]
        filas.append(fila)
        print(f"  · {fila['nombre'][:60]} — {'con texto' if fila['pista'] else 'sin texto'}")

    md = [f'# Clases de Vimeo · {tema or carpeta} — {date.today().isoformat()}\n',
          f'_{len(filas)} videos · fuente: {origen} · {pedidas} peticiones a la API_\n',
          '| id | min | texto | Clase |', '|---|---|---|---|']
    for f in filas:
        md.append(f"| {f['id']} | {f['min']} | {'✅' if f['pista'] else '—'} | {f['nombre']} |")
    md.append('\nCada `<id>.txt` trae la clase en bloques de ~30 s con su minuto, para elegir el tramo.')
    open(os.path.join(destino, 'indice.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    json.dump(filas, open(os.path.join(destino, 'indice.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def elegir_archivo(v):
    """El MP4 más cercano a 720p entre las descargas del dueño."""
    cands = []
    for f in (v.get('download') or []) + (v.get('files') or []):
        link = f.get('link')
        h = f.get('height') or 0
        if link and h and (f.get('type', 'video/mp4') == 'video/mp4' or '.mp4' in link):
            cands.append((abs(h - 720), -h, link, h))
    if not cands:
        return None, 0
    cands.sort()
    return cands[0][2], cands[0][3]


def recortar(video, desde, hasta):
    d, h = a_segundos(desde), a_segundos(hasta)
    if not (0 <= d < h) or h - d > 90:
        sys.exit('ERROR: el tramo debe ir de «desde» a «hasta» y durar como mucho 90 s.')
    v = api(f'/videos/{video}?fields=name,duration,download,files')
    link, alto = elegir_archivo(v)
    if not link:
        sys.exit('ERROR: Vimeo no devolvió un archivo descargable para este video '
                 '(la cuenta necesita plan Pro o superior para descargar desde la API).')
    destino = os.path.join(SALIDA, 'recortes')
    os.makedirs(destino, exist_ok=True)
    nombre = f"{video}_{hms(d).replace(':', '-')}_{hms(h).replace(':', '-')}.mp4"
    salida = os.path.join(destino, nombre)
    print(f"→ Recortando «{v.get('name', '')[:60]}» {hms(d)}–{hms(h)} desde {alto}p")
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{d:.2f}', '-to', f'{h:.2f}', '-i', link,
           '-vf', 'scale=-2:720', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', salida]
    subprocess.run(cmd, check=True)
    mb = os.path.getsize(salida) / 1e6
    print(f'  listo: {salida} ({mb:.1f} MB)')
    with open(os.path.join(destino, 'registro.md'), 'a', encoding='utf-8') as r:
        r.write(f"- {date.today().isoformat()} · {video} · «{v.get('name', '')}» · {hms(d)}–{hms(h)} → `{nombre}`\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='modo', required=True)
    t = sub.add_parser('transcribir')
    t.add_argument('--tema', default='')
    t.add_argument('--carpeta', default='')
    t.add_argument('--max', type=int, default=8)
    r = sub.add_parser('recortar')
    r.add_argument('--video', required=True)
    r.add_argument('--desde', required=True)
    r.add_argument('--hasta', required=True)
    a = ap.parse_args()
    if a.modo == 'transcribir':
        if not (a.tema or a.carpeta):
            sys.exit('ERROR: pon un tema o una carpeta.')
        transcribir(a.tema, a.carpeta, max(1, min(a.max, 20)))
    else:
        desdes, hastas = a.desde.split(','), a.hasta.split(',')
        if len(desdes) != len(hastas):
            sys.exit('ERROR: «desde» y «hasta» deben tener la misma cantidad de tramos.')
        for d, h in zip(desdes, hastas):
            recortar(a.video.strip(), d, h)
    print(f'Peticiones a la API: {pedidas}')


if __name__ == '__main__':
    main()
