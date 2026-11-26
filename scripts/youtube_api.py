#!/usr/bin/env python3
"""YouTube Data API del canal de Design Modeling Academy.

Lee YT_CLIENT_ID, YT_CLIENT_SECRET y YT_REFRESH_TOKEN del entorno (secretos del
repositorio). Nunca imprime claves ni tokens.

  python3 scripts/youtube_api.py verificar      comprueba el permiso y lista el canal
  python3 scripts/youtube_api.py videos [N]     guarda los últimos N videos con sus cifras
"""
import json, os, sys, urllib.parse, urllib.request, urllib.error

API = 'https://www.googleapis.com/youtube/v3/'
OUT = 'matriz-viral/fuentes/youtube'


def pedir(url, data=None, token=None):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode() if data else None)
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode('utf-8', 'replace')
        try:
            err = json.loads(cuerpo)
            msg = err.get('error_description') or (err.get('error') or {}).get('message') or err.get('error') or cuerpo
        except Exception:
            msg = cuerpo[:300]
        sys.exit(f'ERROR {e.code} en {url.split("?")[0]}: {msg}')


def acceso():
    faltan = [k for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN') if not os.environ.get(k)]
    if faltan:
        sys.exit('Faltan secretos: ' + ', '.join(faltan))
    r = pedir('https://oauth2.googleapis.com/token', dict(
        client_id=os.environ['YT_CLIENT_ID'].strip(), client_secret=os.environ['YT_CLIENT_SECRET'].strip(),
        refresh_token=os.environ['YT_REFRESH_TOKEN'].strip(), grant_type='refresh_token'))
    return r['access_token'], r.get('scope', '')


def get(ruta, token, **q):
    return pedir(API + ruta + '?' + urllib.parse.urlencode(q), token=token)


def canal(token):
    r = get('channels', token, part='snippet,statistics,contentDetails', mine='true')
    if not r.get('items'):
        sys.exit('El permiso no está ligado a ningún canal de YouTube.')
    return r['items'][0]


def ultimos(token, lista, n):
    ids, pag = [], None
    while len(ids) < n:
        q = dict(part='contentDetails', playlistId=lista, maxResults=min(50, n - len(ids)))
        if pag:
            q['pageToken'] = pag
        r = get('playlistItems', token, **q)
        ids += [i['contentDetails']['videoId'] for i in r.get('items', [])]
        pag = r.get('nextPageToken')
        if not pag:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = get('videos', token, part='snippet,status,statistics,contentDetails', id=','.join(ids[i:i + 50]))
        for v in r.get('items', []):
            s, st = v['snippet'], v.get('statistics', {})
            vids.append(dict(id=v['id'], url='https://www.youtube.com/watch?v=' + v['id'], titulo=s['title'],
                             publicado=s['publishedAt'], privacidad=v['status']['privacyStatus'],
                             programado=v['status'].get('publishAt'), duracion=v['contentDetails'].get('duration'),
                             vistas=int(st.get('viewCount', 0)), me_gusta=int(st.get('likeCount', 0)),
                             comentarios=int(st.get('commentCount', 0)), descripcion=s.get('description', '')))
    return vids


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else 'verificar'
    token, scope = acceso()
    c = canal(token)
    s, st = c['snippet'], c['statistics']
    permisos = sorted(x.rsplit('/', 1)[-1] for x in scope.split())
    print(f"Canal: {s['title']} ({s.get('customUrl', '')}) · id {c['id']}")
    print(f"Suscriptores: {st.get('subscriberCount', 'ocultos')} · videos: {st.get('videoCount')} · vistas: {st.get('viewCount')}")
    print('Permisos:', ', '.join(permisos))
    n = int(sys.argv[2]) if len(sys.argv) > 2 else (10 if modo == 'verificar' else 50)
    vids = ultimos(token, c['contentDetails']['relatedPlaylists']['uploads'], n)
    for v in vids[:10]:
        print(f"  {v['publicado'][:10]} · {v['privacidad']:<9} · {v['vistas']:>6} vistas · {v['comentarios']:>3} coment. · {v['id']} · {v['titulo'][:70]}")
    if modo == 'videos':
        os.makedirs(OUT, exist_ok=True)
        json.dump(dict(canal=dict(id=c['id'], titulo=s['title'], url=s.get('customUrl'), suscriptores=st.get('subscriberCount'),
                                  videos=st.get('videoCount'), vistas=st.get('viewCount')), total=len(vids), videos=vids),
                  open(f'{OUT}/videos.json', 'w'), ensure_ascii=False, indent=1)
        print(f'OK → {OUT}/videos.json ({len(vids)} videos)')


if __name__ == '__main__':
    main()
