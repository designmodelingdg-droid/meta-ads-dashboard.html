#!/usr/bin/env python3
"""Anuncios de pauta en 4 formatos (1x1, 3x4, 9x16, 16x9) con el sistema de los anuncios de noviembre.
uso: ads.py anuncio.json out_dir → out_dir/<id>-<fmt>.html"""
import json, sys, os, re, html
P = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)

def mk(t):
    t = html.escape(t)
    t = re.sub(r'\*(.+?)\*', r'<span class="a">\1</span>', t, flags=re.S)
    return t.replace('\n', '<br>')
def src(p): return 'file://' + (p if p.startswith('/') else os.path.join(P, p))

FMT = {
 '1x1':  dict(w=1080, h=1080, pad=60, h1=58, sub=24, li=24, ico=48, hero='right:-10px;bottom:130px;width:500px', shot='right:36px;top:170px;width:400px', text_w=560, foot='row', safe_t=0, safe_b=0,
              slots=['right:470px;bottom:120px','right:30px;top:520px','right:300px;top:150px'], pino='right:-30px;top:120px;width:150px'),
 '3x4':  dict(w=1080, h=1440, pad=66, h1=72, sub=29, li=29, ico=58, hero='right:-20px;bottom:210px;width:600px', shot='right:28px;top:640px;width:380px', text_w=620, foot='col', safe_t=0, safe_b=0,
              slots=['right:520px;bottom:230px','right:30px;top:720px','right:330px;top:220px'], pino='right:-30px;top:140px;width:170px'),
 '9x16': dict(w=1080, h=1920, pad=64, h1=74, sub=31, li=30, ico=56, hero='', shot='', text_w=830, foot='col', safe_t=200, safe_b=300, stack=True,
              slots=['left:80px;top:980px','right:80px;top:760px','right:420px;top:1240px'], pino='right:-30px;top:330px;width:180px'),
 '16x9': dict(w=1920, h=1080, pad=72, h1=74, sub=27, li=26, ico=52, hero='right:60px;bottom:110px;width:740px', shot='right:120px;top:110px;width:520px', text_w=900, foot='row', safe_t=0, safe_b=0,
              slots=['right:740px;bottom:150px','right:50px;top:560px','right:440px;top:120px'], pino='right:-20px;top:110px;width:180px'),
}
ICO = {'edificio': '<path d="M4 21V5l8-3v19M12 21h8V9l-8-2"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
       'equipo': '<circle cx="12" cy="8" r="3"/><circle cx="5" cy="10" r="2"/><circle cx="19" cy="10" r="2"/><path d="M6 20c0-3 3-5 6-5s6 2 6 5M1 20c0-2 2-4 4-4M23 20c0-2-2-4-4-4"/>',
       'engranaje': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
       'cerebro': '<path d="M9 3a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3V3zM15 3a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3V3z"/>',
       'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>'}
SOFT = {'revit': 'revit-ico.png', 'robot': 'robot-ico.png', 'navisworks': 'navis-ico.png', 'acero': 'as-ico.png', 'autocad': 'autocad-ico.png'}

for fk in spec.get('formatos', list(FMT)):
    f = FMT[fk]; W, H = f['w'], f['h']
    stack = f.get('stack')
    items = ''.join(f"<li><span class='ic'><svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'>{ICO[i.get('icono','check')]}</svg></span><span>{mk(i['t'])}</span></li>" for i in spec.get('lista', []))
    hero = spec.get('hero'); shot = spec.get('captura')
    heroes = ''
    if hero and not stack:
        hs = spec.get('hero_style', {}).get(fk, f['hero'])
        heroes += f"<img class='hero' src='{src(hero)}' style='{hs}'>"
    if shot and not stack:
        ss = spec.get('shot_style', {}).get(fk, f['shot'])
        heroes += f"<div class='shot' style='{ss}'><div class='bar'><i></i><i></i><i></i></div><img src='{src(shot)}'></div>"
    icos = ''.join(f"<img class='soft' src='{src(SOFT[k])}' style='width:{int(f['ico']*1.7)}px;{f['slots'][n]};transform:rotate({(-8,7,4)[n]}deg)'>" for n, k in enumerate(spec.get('iconos', [])[:3]))
    pino = f"<img class='pino' src='{src('pino.png')}' style='{f['pino']};transform:rotate(8deg)'>" if spec.get('navidad', True) else ''
    foot_dir = 'column' if f['foot'] == 'col' else 'row'
    css = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:#0B1E3F url('{src(spec.get('fondo','fondo-navy.png'))}') center/cover;color:#fff;font-family:'Montserrat',sans-serif;position:relative}}
body:before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 75% 60%,rgba(255,122,26,.10),transparent 60%)}}
.a{{color:#FF7A1A}}
.wrap{{position:absolute;left:{f['pad']}px;right:{f['pad']}px;top:{f['pad']+f['safe_t']}px;bottom:{f['pad']+f['safe_b']}px;display:flex;flex-direction:column;z-index:3}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:20px}}
.kick{{border-left:9px solid #FF7A1A;padding-left:18px;font-weight:800;font-size:{int(f['sub']*1.0)}px;color:#FF7A1A;text-transform:uppercase;letter-spacing:.5px;line-height:1.1;max-width:72%}}
.top img{{height:{int(f['sub']*2.3)}px}}
.heroin{{height:430px;display:flex;align-items:center;justify-content:center;margin:10px 0}} .heroin img{{height:430px;max-width:100%;object-fit:contain;filter:drop-shadow(0 40px 50px rgba(0,0,0,.5))}}
h1{{font-weight:900;text-transform:uppercase;font-size:{spec.get('h1_scale',1)*f['h1']}px;line-height:1.02;margin-top:{int(f['pad']*0.55)}px;max-width:{f['text_w']}px;text-wrap:balance}}
.sub{{font-weight:600;font-size:{f['sub']}px;line-height:1.3;margin-top:22px;max-width:{min(f['text_w'],620 if not stack else 936)}px;color:#E8EEF8}}
ul{{list-style:none;display:flex;flex-direction:column;gap:{int(f['li']*0.55)}px;margin-top:{int(f['pad']*0.6)}px}}
li{{display:flex;align-items:center;gap:22px;font-weight:800;font-size:{f['li']}px;line-height:1.1;text-transform:{spec.get('lista_case','uppercase')};max-width:{620 if not stack else 936}px}}
.ic{{flex:0 0 {f['ico']}px;height:{f['ico']}px;border:4px solid #FF7A1A;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#FF7A1A}}
.ic svg{{width:55%;height:55%}}
.dato{{font-weight:600;font-size:{int(f['sub']*0.92)}px;margin-top:{int(f['pad']*0.5)}px;color:#E8EEF8}}
.sp{{flex:1}}
.foot{{display:flex;flex-direction:{foot_dir};gap:{26 if foot_dir=='column' else 30}px;align-items:{'flex-start' if foot_dir=='column' else 'center'};justify-content:space-between}}
.cta{{background:#FF7A1A;color:#fff;font-weight:900;font-size:{int(f['sub']*1.25)}px;padding:{int(f['sub']*0.55)}px {int(f['sub']*1.2)}px;border-radius:999px;white-space:nowrap;box-shadow:0 14px 30px rgba(255,122,26,.35)}}
.avales{{height:{int(f['sub']*1.9)}px;{'align-self:center' if foot_dir=='column' else ''}}}
.hero{{position:absolute;z-index:1;filter:drop-shadow(0 40px 50px rgba(0,0,0,.5))}}
.shot{{position:absolute;z-index:2;border-radius:18px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.5);border:2px solid rgba(255,255,255,.18);background:#000;transform:rotate(2deg)}}
.shot img{{display:block;width:100%}} .shot .bar{{height:28px;background:#1d2a3d;display:flex;gap:8px;align-items:center;padding-left:14px}}
.shot .bar i{{width:10px;height:10px;border-radius:50%;background:#ff5f57}}.shot .bar i:nth-child(2){{background:#febc2e}}.shot .bar i:nth-child(3){{background:#28c840}}
.soft{{position:absolute;z-index:4;filter:drop-shadow(0 14px 20px rgba(0,0,0,.45))}}
.pino{{position:absolute;z-index:5}}
"""
    body = f"""<div class='wrap'><div class='top'><div class='kick'>{mk(spec['kicker'])}</div><img src='{src('dg-blanco.png')}'></div>
<h1>{mk(spec['titulo'])}</h1>{f"<p class='sub'>{mk(spec['sub'])}</p>" if spec.get('sub') else ''}
{f"<div class='heroin'><img src='{src(hero)}'></div>" if stack and hero else ''}
{f'<ul>{items}</ul>' if items else ''}{f"<p class='dato'>{mk(spec['dato'])}</p>" if spec.get('dato') else ''}
{'' if stack else "<div class='sp'></div>"}<div class='foot'><span class='cta'>{html.escape(spec.get('cta','MÁS INFORMACIÓN →'))}</span><img class='avales' src='{src('img/avales.png')}'></div></div>
{heroes}{icos}{pino}"""
    open(os.path.join(out, f"{spec['id']}-{fk}.html"), 'w').write(
        f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap'><style>{css}</style></head><body>{body}</body></html>")
print('ok', spec['id'])
