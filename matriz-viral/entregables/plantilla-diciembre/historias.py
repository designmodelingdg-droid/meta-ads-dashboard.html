#!/usr/bin/env python3
"""Cuadros de historias 1080x1920 desde el calendario (G5). Salida: out/hist/<id>-<n>.html + out/hist/manifest.json"""
import json, os, re, html
P = os.path.dirname(os.path.abspath(__file__))
R = '/home/user/meta-ads-dashboard.html/matriz-viral/matriz/'
B = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/banco-real/'
OUT = os.path.join(P, 'out/hist'); os.makedirs(OUT, exist_ok=True)
cal = json.load(open(R + 'calendario-diciembre.json'))
g = {p['id']: p for p in json.load(open(R + 'guiones-completos.json'))['piezas']}
src = lambda p: 'file://' + (p if p.startswith('/') else os.path.join(P, p))
esc = html.escape
FOTOS = {('dic-hist-1202', 2): (B + 'robot/robot-08-zapatas.jpg', 'Robot · definición del suelo bajo la zapata'),
         ('dic-hist-1229', 1): (B + 'revit/revit-17-armado.jpg', 'Revit · armado de cimentación')}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:'Oswald',sans-serif;position:relative;color:#F5EFE6}
body.navy{background:#0A1A33 url('%(plate)s') center/cover}
body.ambar{background:linear-gradient(160deg,#E07A2E 0%%,#C9601A 100%%)}
header{position:absolute;top:250px;left:80px;display:flex;align-items:center;gap:22px;z-index:3}
header img.dg{height:92px} header i{width:2px;height:78px;background:rgba(255,255,255,.35)} header img.atc{height:78px}
.zona{position:absolute;left:80px;right:80px;top:420px;bottom:400px;display:flex;flex-direction:column;justify-content:%(just)s;z-index:2}
.raya{width:200px;height:8px;background:#E07A2E;margin-bottom:34px}
.ambar .raya{background:#0A1A33}
h1,h2{max-width:%(mw)spx}
h1{font-family:'Anton';font-weight:400;text-transform:uppercase;line-height:1.02;letter-spacing:.5px}
h2{font-family:'Oswald';font-weight:600;line-height:1.14}
.a{color:#E07A2E} .ambar .a{color:#0A1A33}
.sub{font-family:'Oswald';font-weight:500;font-size:54px;line-height:1.22;margin-top:34px}
.pill{display:inline-block;margin-top:26px;background:#0A1A33;color:#fff;font-family:'Anton';font-size:150px;letter-spacing:3px;padding:14px 50px;border-radius:36px;text-transform:uppercase}
.shot{margin-top:44px;border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.45);border:2px solid rgba(255,255,255,.18)}
.shot img{display:block;width:100%%;height:520px;object-fit:cover}
.cap{font-family:'Barlow';font-weight:600;font-size:28px;color:#9FB3CF;margin-top:14px}
.quien{display:flex;gap:28px;align-items:center;margin-top:44px}
.quien img{width:170px;height:170px;border-radius:50%%;object-fit:cover;border:6px solid #E07A2E}
.quien b{display:block;font-weight:600;font-size:50px}.quien span{font-family:'Barlow';font-weight:600;font-size:32px;color:#9FB3CF}
.pino{position:absolute;right:-50px;top:210px;width:210px;transform:rotate(8deg);z-index:4}
"""
HEAD = "<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Anton&family=Oswald:wght@500;600;700&family=Barlow:wght@500;600;700&display=swap'><style>%s</style></head>"


def titulo(t, sticker):
    n = len(t)
    if n <= 75:
        size = 132 if n <= 45 else 110
        return f"<h1 style='font-size:{size}px'>{esc(t)}</h1>"
    size = 90 if n <= 120 else (76 if n <= 180 else 64)
    return f"<h2 style='font-size:{size}px'>{esc(t)}</h2>"


def page(cls, body, just='center', pino=True):
    css = CSS % dict(plate=src('fondo-navy.png'), just=just, mw=920)
    hdr = f"<header><img class='dg' src='{src('dg-blanco.png')}'><i></i><img class='atc' src='{src('atc-wht.png')}'></header>"
    pn = f"<img class='pino' src='{src('pino.png')}'>" if pino else ''
    return HEAD % css + f"<body class='{cls}'>{hdr}<div class='zona'>{body}</div>{pn}</body></html>"


man = {}
for e in cal['grupos'][4]['calendario']:
    pid = e['id']; hs = g[pid].get('historias') or []
    frames = []
    for h in hs:
        n, v, t, s = h.get('n'), (h.get('visual') or ''), (h.get('texto') or ''), (h.get('sticker') or '')
        tiene = not s.lower().startswith('ningun')
        nota = f"Cuadro {n}"
        f = None
        vl = v.lower()
        if vl.startswith('cierre'):
            m = re.search(r'«([^»]+)»', s); kw = m.group(1) if m else ''
            resto = re.sub(r'^Respóndeme\s+' + re.escape(kw) + r'\s*', '', t)
            body = f"<div class='raya'></div><h1 style='font-size:120px'>Respóndeme</h1><div><span class='pill'>{esc(kw)}</span></div><p class='sub' style='color:#fff'>{esc(resto)}</p>"
            f = page('ambar', body, pino=False); nota += f" · cierre · se responde con «{kw}»"
        elif (pid, n) in FOTOS:
            img, cap = FOTOS[(pid, n)]
            body = f"<div class='raya'></div>{titulo(t, tiene)}<div class='shot'><img src='{src(img)}'></div><div class='cap'>{esc(cap)}</div>"
            f = page('navy', body, just='flex-start'); nota += f" · sticker: {s}" if tiene else ''
        elif vl.startswith('tarjeta con la cita'):
            cita, _, quien = t.partition(' — ')
            nombre, _, rol = quien.partition(', ')
            extra = ''
            if '. ' in rol:
                rol, _, extra = rol.partition('. ')
            foto = f"<img src='{src('img/albino.jpg')}'>" if 'Albino' in nombre else ''
            body = f"<div class='raya'></div><h1 style='font-size:92px' class='a'>{esc(cita.replace('«','“').replace('»','”'))}</h1><div class='quien'>{foto}<div><b>{esc(nombre)}</b><span>{esc(rol.rstrip('.'))}</span></div></div>" + (f"<p class='sub'>{esc(extra)}</p>" if extra else '')
            f = page('navy', body); nota += ' · cita (versión fija; el plan la pone sobre el video de la ruta)'
        elif vl.startswith('texto sobre') or vl.startswith('lámina simple'):
            body = f"<div class='raya'></div>{titulo(t, tiene)}"
            f = page('navy', body, just='flex-start' if tiene else 'center')
            nota += f" · sticker debajo: {s}" if tiene else ''
        else:
            nota += f" · SIN ARTE (se hace en Instagram): {v} · Texto: {t}" + (f" · Sticker: {s}" if tiene else '')
        if f:
            fn = f"{pid}-{n}"
            open(os.path.join(OUT, fn + '.html'), 'w').write(f)
            frames.append(dict(n=n, archivo=fn, nota=nota))
        else:
            frames.append(dict(n=n, archivo=None, nota=nota))
    man[pid] = frames
json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
print(sum(1 for v in man.values() for f in v if f['archivo']), 'cuadros con arte de', sum(len(v) for v in man.values()))
