#!/usr/bin/env python3
"""
Cierra los videos de Vimeo que estén abiertos al público.

    privacy.download -> false     (quita el botón de descarga)
    privacy.view     -> disable   (deja de verse en vimeo.com)

privacy.embed NO se toca: mientras siga en 'public', todo lo que esté
incrustado —GoHighLevel, comunidades, cursos, landings— sigue funcionando
igual. Lo único que deja de funcionar es un enlace directo a vimeo.com, que
es justo lo que se quiere cerrar.

Comprobado el 13-ago-2026 sobre un video de prueba: con view=disable el
reproductor incrustado responde 200 y la página pública deja de exponer el
video. La incrustación no se rompe — mejora.

USO
    export VIMEO_TOKEN=xxxxx          # nunca se guarda en el repo
    python3 scripts/cerrar_vimeo.py --dry-run     # ver qué haría
    python3 scripts/cerrar_vimeo.py               # aplicarlo

SEGURIDAD
  - Es IDEMPOTENTE: lee el estado real de Vimeo en cada corrida y solo toca
    lo que falta. Si se corta a mitad, se vuelve a lanzar y sigue donde iba.
    (Pasó el 14-ago: el contenedor se recicló a los 802 de 1.278.)
  - Guarda el estado anterior de cada video en el registro, para revertir.
  - Respeta el límite de Vimeo (500 peticiones/hora): cuando quedan pocas,
    espera al reinicio en vez de fallar.
"""
import json, os, sys, time, urllib.request, urllib.error, argparse
from datetime import datetime, timezone

TOKEN = os.environ.get('VIMEO_TOKEN', '').strip()
if not TOKEN:
    for ruta in (os.path.expanduser('~/.vimeo_token'), '.secrets/vimeo_token'):
        if os.path.exists(ruta):
            TOKEN = open(ruta).read().strip(); break
if not TOKEN:
    sys.exit('ERROR: falta VIMEO_TOKEN en el entorno.')

CAB = {'Authorization': f'Bearer {TOKEN}',
       'Accept': 'application/vnd.vimeo.*+json;version=3.4',
       'Content-Type': 'application/json'}
DESTINO = {'download': False, 'view': 'disable'}
CAMPOS = 'uri,name,privacy.view,privacy.embed,privacy.download'


def pedir(url, metodo='GET', cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo else None
    r = urllib.request.Request(url, data=datos, headers=CAB, method=metodo)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.load(resp), dict(resp.headers)


def inventario():
    """Lee el estado REAL desde Vimeo. Es lo que hace el script idempotente."""
    out, page = [], 1
    while True:
        d, _ = pedir(f'https://api.vimeo.com/me/videos?per_page=100&page={page}&fields={CAMPOS}')
        out += d['data']
        if not d.get('paging', {}).get('next'):
            return out
        page += 1
        time.sleep(0.2)


def esperar_si_hace_falta(cab, minimo=25):
    quedan = cab.get('x-ratelimit-remaining')
    if quedan is None or int(quedan) > minimo:
        return
    espera = 300
    if cab.get('x-ratelimit-reset'):
        try:
            t = datetime.fromisoformat(cab['x-ratelimit-reset'].replace('Z', '+00:00'))
            espera = max(30, (t - datetime.now(timezone.utc)).total_seconds() + 15)
        except Exception:
            pass
    print(f'  … quedan {quedan} peticiones. Esperando {espera/60:.0f} min.', flush=True)
    time.sleep(espera)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limite', type=int, default=0)
    ap.add_argument('--excluir', default='', help='IDs separados por coma')
    ap.add_argument('--registro', default='registro-cierre-vimeo.jsonl')
    a = ap.parse_args()

    excluidos = {x.strip() for x in a.excluir.split(',') if x.strip()}
    print('Leyendo el estado real desde Vimeo…', flush=True)
    inv = inventario()

    pend = []
    for v in inv:
        vid = v['uri'].split('/')[-1]
        p = v.get('privacy') or {}
        if vid in excluidos:
            continue
        if p.get('view') == 'anybody' or p.get('download') is True:
            pend.append((vid, v.get('name') or '', p))
    if a.limite:
        pend = pend[:a.limite]

    ya = len(inv) - len(pend) - len(excluidos)
    print(f'Total en la cuenta: {len(inv)}')
    print(f'  ya cerrados: {ya}')
    print(f'  por cerrar:  {len(pend)}')
    print(f'Modo: {"SIMULACRO" if a.dry_run else "REAL"}\n')
    if a.dry_run:
        for vid, nom, p in pend[:15]:
            print(f'  {vid}  view={p.get("view")} download={p.get("download")}  {nom[:46]}')
        print(f'  … y {max(0, len(pend)-15)} más')
        return

    reg = open(a.registro, 'a')
    ok = fallo = 0
    for i, (vid, nom, antes) in enumerate(pend, 1):
        try:
            _, cab = pedir(f'https://api.vimeo.com/videos/{vid}', 'PATCH', {'privacy': DESTINO})
            ok += 1
            reg.write(json.dumps({'id': vid, 'nombre': nom, 'antes': antes,
                                  'despues': DESTINO, 'estado': 'ok'}, ensure_ascii=False) + '\n')
            reg.flush()
            esperar_si_hace_falta(cab)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print('  429: límite alcanzado. Esperando 10 min.', flush=True)
                time.sleep(600)
                continue
            fallo += 1
            reg.write(json.dumps({'id': vid, 'nombre': nom, 'antes': antes,
                                  'estado': f'error {e.code}'}, ensure_ascii=False) + '\n')
            reg.flush()
        except Exception as e:
            fallo += 1
            reg.write(json.dumps({'id': vid, 'estado': 'error', 'detalle': str(e)[:120]}) + '\n')
            reg.flush()
        if i % 25 == 0:
            print(f'  {i}/{len(pend)}  ·  ok {ok}  ·  fallos {fallo}', flush=True)
        time.sleep(0.35)

    reg.close()
    print(f'\nTERMINADO · cambiados {ok} · fallos {fallo}')
    print('Si se cortó a mitad, vuelve a lanzarlo: solo toca lo que falte.')


if __name__ == '__main__':
    main()
