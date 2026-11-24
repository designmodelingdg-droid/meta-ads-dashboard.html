"""Enlaces de descarga directa (MP4 1080p o 720p) de varios videos de Vimeo. Solo LEE.
La salida va cifrada con acero/cert.pem: solo se abre con la llave privada."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from vimeo_clips import api  # noqa: E402

def mejor(v):
    c = []
    for f in (v.get('download') or []) + (v.get('files') or []):
        l, h = f.get('link'), f.get('height') or 0
        if l and h in (1080, 720) and (f.get('type', 'video/mp4') == 'video/mp4' or '.mp4' in l):
            c.append((-h, l, h, f.get('size') or 0, f.get('expires') or f.get('link_expiration_time') or ''))
    c.sort()
    return c[0][1:] if c else (None, 0, 0, '')

out = []
for vid in [x.strip() for x in sys.argv[1].split(',') if x.strip()]:
    v = api(f'/videos/{vid}?fields=name,duration,download,files')
    l, h, s, e = mejor(v)
    out.append({'id': vid, 'name': v.get('name'), 'dur': v.get('duration'), 'alto': h, 'mb': round(s / 1e6), 'expira': e, 'link': l})
    print(vid, v.get('duration'), h, 'OK' if l else 'SIN ENLACE', flush=True)
os.makedirs('enl', exist_ok=True)
json.dump(out, open('enl/e.json', 'w'), ensure_ascii=False)
subprocess.run(['openssl', 'cms', '-encrypt', '-binary', '-aes256', '-in', 'enl/e.json', '-outform', 'DER', '-out', 'enl/e.json.cms', 'acero/cert.pem'], check=True)
os.remove('enl/e.json')
