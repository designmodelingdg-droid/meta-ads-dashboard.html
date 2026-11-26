#!/usr/bin/env python3
"""Genera las láminas (HTML) de una pieza con el sistema visual de noviembre + Navidad + Autodesk ATC.
uso: gen.py pieza.json salida_dir   → salida_dir/l1.html … (render con render.js)"""
import json, sys, os, re, html

P = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

FONDOS = {
    'navy':  dict(bg='#0A1A33', tx='#F5EFE6', mut='#9FB3CF', acc='#E07A2E', line='rgba(255,255,255,.18)', dg='dg-blanco.png', atc='atc-wht.png', plate='fondo-navy.png', card='rgba(255,255,255,.06)', cardb='rgba(255,255,255,.16)'),
    'navy2': dict(bg='#0A1A33', tx='#F5EFE6', mut='#9FB3CF', acc='#E07A2E', line='rgba(255,255,255,.18)', dg='dg-blanco.png', atc='atc-wht.png', plate='fondo-navy2.png', card='rgba(255,255,255,.06)', cardb='rgba(255,255,255,.16)'),
    'crema': dict(bg='#FBF5EE', tx='#0E2240', mut='#5C6B80', acc='#D2691E', line='rgba(14,34,64,.25)', dg='dg-color.png', atc='atc-blk.png', plate='fondo-crema.png', card='#FFFFFF', cardb='rgba(14,34,64,.10)'),
}
ICONOS = {'revit': 'revit-ico.png', 'robot': 'robot-ico.png', 'navisworks': 'navis-ico.png', 'acero': 'as-ico.png', 'autocad': 'autocad-ico.png'}


def mk(t):
    t = html.escape(t)
    t = re.sub(r'\*(.+?)\*', r'<span class="a">\1</span>', t, flags=re.S)
    t = re.sub(r'~(.+?)~', r'<span class="b">\1</span>', t, flags=re.S)
    return t.replace('\n', '<br>')


def src(p):
    if not p:
        return ''
    return 'file://' + (p if p.startswith('/') else os.path.join(P, p))


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{background:var(--bg) url('%(plate)s') center/cover no-repeat;color:var(--tx);font-family:'Oswald',sans-serif;position:relative}
.a{color:var(--acc)} .b{color:var(--mut)}
header{position:absolute;z-index:3;top:70px;left:72px;right:72px;display:flex;align-items:center;justify-content:space-between}
.marcas{display:flex;align-items:center;gap:22px}
.marcas img.dg{height:%(dgh)spx} .marcas i{width:2px;height:64px;background:var(--line)} .marcas img.atc{height:64px}
.cont{font-family:'Anton';font-size:58px;letter-spacing:1px;line-height:1;text-align:right}
.cont span{color:var(--acc)} .cont:after{content:'';display:block;height:5px;background:var(--acc);margin-top:12px;width:100%%}
footer{position:absolute;z-index:3;left:72px;right:72px;bottom:58px;display:flex;white-space:nowrap;justify-content:space-between;align-items:center;font-family:'Barlow';font-weight:600;font-size:23px;letter-spacing:6px;color:var(--mut)}
footer b{font-family:'Anton';font-weight:400;letter-spacing:3px;font-size:40px;color:var(--acc)}
footer .tag em{font-style:normal;color:var(--acc);margin:0 14px}
.zona{position:absolute;left:72px;right:72px;top:210px;bottom:150px;display:flex;flex-direction:column;justify-content:center}
h1{max-width:%(hmax)spx;font-family:'Anton';font-weight:400;text-transform:uppercase;line-height:.98;letter-spacing:.5px}
.raya{width:240px;height:7px;background:var(--acc);margin-top:34px}
.kicker{font-family:'Barlow Condensed';font-weight:700;font-size:46px;letter-spacing:6px;color:var(--acc);text-transform:uppercase;margin-bottom:18px}
h2{max-width:%(hmax)spx;font-family:'Oswald';font-weight:600;font-size:76px;line-height:1.06}
p.sub{font-family:'Oswald';font-weight:500;font-size:52px;line-height:1.2;margin-top:22px;color:var(--tx)}
ul{list-style:none;margin-top:40px;display:flex;flex-direction:column;gap:30px}
li{display:flex;gap:30px;align-items:flex-start;font-family:'Oswald';font-weight:500;font-size:58px;line-height:1.14}
li .ck{flex:0 0 66px;height:66px;border:3.5px solid var(--acc);border-radius:50%%;display:flex;align-items:center;justify-content:center;margin-top:4px}
li .ck svg{width:30px;height:30px}
.cards{display:flex;gap:30px;margin-top:36px}
.card{flex:1;background:var(--card);border:2px solid var(--cardb);border-radius:28px;padding:34px 30px;text-align:center;box-shadow:0 18px 40px rgba(0,0,0,.12)}
.card .l{font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:3px}
.card .v{font-family:'Anton';font-size:190px;line-height:1.05}
.card .n{font-family:'Barlow';font-weight:600;font-size:28px;color:var(--mut);line-height:1.3}
.pie{font-family:'Oswald';font-weight:600;font-size:48px;margin-top:38px;line-height:1.15}
.shot{position:relative;flex-shrink:0;margin-top:34px;border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);border:2px solid var(--cardb);background:#000}
.shot img{display:block;width:100%%;height:%(shoth)spx;object-fit:cover;object-position:%(shotpos)s}
.shot .bar{height:34px;background:#1d2a3d;display:flex;gap:10px;align-items:center;padding-left:16px}
.shot .bar i{width:12px;height:12px;border-radius:50%%;background:#ff5f57}.shot .bar i:nth-child(2){background:#febc2e}.shot .bar i:nth-child(3){background:#28c840}
.cap{font-family:'Barlow';font-weight:600;font-size:27px;color:var(--mut);margin-top:16px;letter-spacing:.5px}
.hero{position:absolute;z-index:0}
.zona{z-index:2}
.ico{position:absolute;z-index:3;filter:drop-shadow(0 16px 22px rgba(0,0,0,.35))}
.pino{position:absolute;z-index:4;pointer-events:none}
.pill{display:inline-block;margin-top:44px;background:var(--acc);color:#fff;font-family:'Anton';font-size:64px;letter-spacing:2px;padding:20px 46px;border-radius:999px}
.tabla{display:grid;grid-template-columns:1fr 1fr;gap:12px 40px;margin-top:30px}
.tf{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--line);padding:8px 4px;font-family:'Oswald';font-size:44px}
.tf b{font-weight:600;color:var(--acc)} .tf span{font-weight:500}
.foto{display:flex;gap:30px;align-items:center;margin-top:36px}
.foto img{width:190px;height:190px;border-radius:50%%;object-fit:cover;border:6px solid var(--acc)}
.foto b{display:block;font-family:'Oswald';font-weight:600;font-size:46px} .foto span{font-family:'Barlow';font-weight:600;font-size:30px;color:var(--mut)}
.det{font-family:'Oswald';font-weight:500;font-size:44px;margin-top:26px;line-height:1.2}
"""

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="color:var(--acc)"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
QUOTE = '<svg viewBox="0 0 24 24" style="color:var(--acc)"><text x="3" y="21" font-family="Anton" font-size="22" fill="currentColor">“</text></svg>'

n = len(spec['slides'])
for i, s in enumerate(spec['slides'], 1):
    f = FONDOS[s.get('fondo', 'navy')]
    plate = s.get('plate', f['plate'])
    css = CSS % dict(plate=src(plate), dgh=s.get('dgh', 74 if 'blanco' in f['dg'] else 86), shoth=s.get('shot_h', 520), shotpos=s.get('shot_pos', 'center'), hmax=s.get('hmax', 820 if s.get('pino','tr') in ('tr',) and s.get('navidad', spec.get('navidad', True)) else 936))
    vars_ = f":root{{--bg:{f['bg']};--tx:{f['tx']};--mut:{f['mut']};--acc:{f['acc']};--line:{f['line']};--card:{f['card']};--cardb:{f['cardb']}}}"
    body = []
    body.append(f"<header><div class='marcas'><img class='dg' src='{src(f['dg'])}'><i></i><img class='atc' src='{src(f['atc'])}'></div>"
                + (f"<div class='cont'><span>{i:02d}</span>/{n:02d}</div>" if n > 1 else '') + "</header>")
    if s.get('velo'):
        body.append(f"<div style='position:absolute;inset:0;z-index:1;background:{s['velo']}'></div>")
    for h in s.get('heroes', []):
        body.append(f"<img class='hero' src='{src(h['src'])}' style='{h.get('style', '')}'>")
    z = []
    t = s['tipo']
    if s.get('kicker'):
        z.append(f"<div class='kicker'>{mk(s['kicker'])}</div>")
    if t in ('portada', 'cta', 'grande') and s.get('titulo'):
        z.append(f"<h1 style='font-size:{s.get('tam', 132)}px'>{mk(s['titulo'])}</h1>")
        if t == 'portada':
            z.append("<div class='raya'></div>")
    elif s.get('titulo'):
        z.append(f"<h2 style='font-size:{s.get('tam', 92)}px'>{mk(s['titulo'])}</h2>")
    if s.get('sub'):
        z.append(f"<p class='sub'>{mk(s['sub'])}</p>")
    if s.get('puntos'):
        z.append('<ul>' + ''.join(f"<li><span class='ck'>{QUOTE if p.startswith('«') else CHECK}</span><span>{mk(p)}</span></li>" for p in s['puntos']) + '</ul>')
    if s.get('cards'):
        z.append("<div class='cards'>" + ''.join(
            f"<div class='card'><div class='l'>{mk(c['label'])}</div><div class='v' style='color:{c.get('color', 'var(--tx)')};font-size:{c.get('size', 190)}px'>{mk(c['valor'])}</div><div class='n'>{mk(c.get('nota', ''))}</div></div>" for c in s['cards']) + '</div>')
    if s.get('tabla'):
        filas=''.join(f"<div class='tf'><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>" for a,b in s['tabla'])
        z.append(f"<div class='tabla'>{filas}</div>")
    if s.get('foto'):
        z.append(f"<div class='foto'><img src='{src(s['foto'])}'><div><b>{mk(s.get('foto_nombre',''))}</b><span>{mk(s.get('foto_rol',''))}</span></div></div>")
    if s.get('captura'):
        z.append(f"<div class='shot'><div class='bar'><i></i><i></i><i></i></div><img src='{src(s['captura'])}'></div>")
        if s.get('cap'):
            z.append(f"<div class='cap'>{mk(s['cap'])}</div>")
    if s.get('pie'):
        z.append(f"<div class='pie'>{mk(s['pie'])}</div>")
    if s.get('palabra'):
        z.append(f"<div><span class='pill'>COMENTA {html.escape(s['palabra'])}</span></div>")
    if s.get('detalle'):
        z.append(f"<p class='det'>{mk(s['detalle'])}</p>")
    zs = s.get('zona_style', '')
    body.append(f"<div class='zona' style='{zs}'>{''.join(z)}</div>")
    for ic in s.get('iconos', []):
        body.append(f"<img class='ico' src='{src(ICONOS[ic['k']])}' style='width:{ic.get('w', 120)}px;left:{ic['x']}px;top:{ic['y']}px;transform:rotate({ic.get('r', 0)}deg)'>")
    if s.get('navidad', spec.get('navidad', True)):
        pz = s.get('pino', 'tr')
        pos = {'tr': 'right:-46px;top:150px;width:230px;transform:rotate(8deg)', 'bl': 'left:-70px;bottom:120px;width:230px;transform:rotate(-160deg)',
               'br': 'right:-60px;bottom:120px;width:230px;transform:rotate(200deg)', 'tl': 'left:-60px;top:150px;width:230px;transform:scaleX(-1)'}[pz]
        body.append(f"<img class='pino' src='{src('pino.png')}' style='{pos}'>")
    tag = mk(s.get('tagline', spec.get('tagline', 'MODELA | ENTREGA | COBRA'))).replace('|', '<em>|</em>')
    fin = s.get('fin', 'DESLIZA →' if i < n else spec.get('fin_ultima', 'GUARDA ESTE POST'))
    body.append(f"<footer><span class='tag'>{tag}</span><b>{html.escape(fin)}</b></footer>")
    open(os.path.join(out, f'l{i}.html'), 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Anton&family=Oswald:wght@500;600;700&family=Barlow:wght@500;600;700&family=Barlow+Condensed:wght@600;700&display=swap'><style>{vars_}{css}</style></head><body>{''.join(body)}</body></html>")
print(n, 'láminas en', out)
