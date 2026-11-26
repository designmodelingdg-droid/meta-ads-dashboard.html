#!/usr/bin/env python3
"""Deja los subtítulos definitivos de cada clip (data/<id>.json → words, fin, kind, portada) y genera src/clips.ts.

Texto: sale de tres transcripciones reales (la original del workshop/Vimeo y dos pasadas de Whisper sobre la voz ya editada);
EDITS solo corrige lo que una de ellas oyó mal y las otras confirman (o lo que se lee en la pantalla). Nada inventado.
Tiempos: los de Whisper sobre el corte final, ajustados a las «islas» de voz medidas en el audio para que ninguna palabra
aparezca en un silencio.
Uso: finalizar.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import P
from islas import islas

# (token tal como lo dio Whisper, segundo aproximado, texto nuevo | None para quitarlo)
CFG = {
 's1-1880-muros': dict(base='whisper', edits=[('modelo,', 3.5, 'modelo.'), ('vamos', 4, 'Vamos'), ('¿Cuántas', 11.0, '¿cuántas'), ('75,', 12.0, '75.'),
      ('¿Cuántas', 13.8, '¿cuántos', (13.04, 13.78)), ('1859,', 15.2, '1.859.'), ('él', 15.7, 'Él'), ('1800,', 16.0, '1.800…'), (None, 0, 'sí, ahí,', (17.12, 17.61)),
      ('1880,', 17.3, '1.880.', (18.87, 22.67)), ('entonces', 23.2, 'Entonces,'), ('Manager,', 26.5, 'Manager.'), ('en', 26.9, 'En'), ('filtrarlo', 29.1, 'filtrar yo'), ('1859', 30, '1.859')],
      portada=dict(lines=['LA IA DIJO', '1.880 MUROS.', 'REVIT DICE 1.859'], accent=2, t=13.5)),
 's2-niveles': dict(base='whisper', edits=[('compro', 0.7, 'con'), ('un', 1.1, 'un prompt'), ('que', 2.2, 'que diga:'), (None, 0, '¿ok?', (10.33, 10.75)), ('acá,', 12.5, 'acá,', (11.88, 12.44)), ('consultar', 15.8, 'y consultar'),
      ('es...', 20.3, 'es…'), ('el', 22.9, 'El'), ('de', 24.3, 'es'), ('5ch,', 24.5, '5CH…'), ('consulté', 26.4, 'Consulté'), ('niveles', 27.0, 'niveles:'),
      ('423,', 28.4, '4,23,'), ('886,', 29.6, '8,86,'), (None, 0, 'sí,', (30.63, 30.97)), ('2096,', 30.9, '20,96,', (31.18, 32.11)), ('2392', 32.8, '23,92.'), ('que', 33.5, 'Que'),
      ('información', 35.6, 'información.')],
      portada=dict(lines=['LE PREGUNTÉ', 'A MI MODELO DE REVIT', 'POR SUS NIVELES'], accent=2, t=29.0)),
 's3-conectar-chatgpt': dict(base='whisper_l', edits=[('sencillo', 28, 'sencillo,'), ('especializado', 30, 'especializado,'), ('mundo', 32, 'mundo,'), ('¿Ok?', 32.5, '¿ok?')],
      portada=dict(lines=['ASÍ SE CONECTA', 'CHATGPT A REVIT'], accent=1, t=20.5)),
 's4-claude-revit': dict(base='whisper_l', edits=[('Ahí', 0, None), ('está,', 0.1, 'Esta,'), ('está', 0.4, 'esta es'), ('Nonica', 0.9, 'Nonica,'), ('salir', 9.8, 'salir.'), ('y', 10.1, 'Y'),
      ('revisan', 13.5, 'revisa'), ('sanitario,', 24.3, 'sanitario.'), ('dato', 25.4, 'Dato'), ('el', 29.92, None), ('MCP,', 29.98, None),
      ('a', 37.7, None), ('programa', 38.8, 'prompt'), ('maestro', 39.1, 'maestro.')],
      portada=dict(lines=['CONECTÉ CLAUDE', 'A MI MODELO', 'DE REVIT'], accent=1, t=3.0)),
 's5-cualquier-cosa': dict(base='whisper_l', edits=[],
      portada=dict(lines=['SI ENTRA', 'CUALQUIER COSA,', 'SALE CUALQUIER COSA'], accent=2, t=3.0)),
 's6-no-hace-magia': dict(base='whisper', edits=[('Tráeme', 0, 'Créanme'), ('ustedes,', 5.6, 'ustedes.'), ('¿ok?', 5.9, 'Ok,', (6.17, 6.59)), ('magia,', 14.5, 'magia.'),
      ('si', 15, 'Si'), ('lógica,', 22.5, 'lógica.'), ('y', 23, 'Y'), ('del', 25.5, 'el')],
      portada=dict(lines=['LA IA', 'NO HACE MAGIA'], accent=1, t=12.0)),
 's7-mil-cosas': dict(base='whisper', edits=[('Modela', 22.7, 'modela'), ('cuál', 29.4, '¿cuál'), ('GPT', 32.2, 'GPT?'), ('es', 32.8, 'Es'), ('tiempo', 34.2, 'tiempo.'),
      ('y', 34.6, 'Y'), ('expertiz', 36.7, 'expertise'), ('vida.', 39.7, 'IA.')],
      portada=dict(lines=['NO LE PIDAS', 'MIL COSAS', 'A TU GPT'], accent=1, t=6.0)),
 's8-para-que-conectar': dict(base='whisper_l', edits=[],
      portada=dict(lines=['¿PARA QUÉ', 'CONECTAR LA IA', 'A REVIT?'], accent=1, t=3.0)),
 'nav-fragmento-clase-1-reel': dict(base='whisper_l', edits=[('visual,', 0.5, 'visual')],
      portada=dict(lines=['ASÍ SE VE', 'POR DENTRO', 'UN CURSO DE $46.50'], accent=2, t=12.0, chip='CLASE REAL · SAP2000')),
 # 26-nov: corte nuevo con las pausas recortadas y a 1,1× (prep_clase_corte.py); el «¿Sí?» está en la transcripción de Vimeo y Whisper lo salta
 'nav-fragmento-clase-2-reel': dict(base='whisper_l', edits=[('aplicación,', 8.5, 'aplicación'), ('la', 9.0, 'de la'), (None, 0, '¿Sí?', (12.81, 13.11))],
      portada=dict(lines=['¿ASÍ DISEÑAS', 'TUS ZAPATAS?'], accent=1, t=13.5, chip='CLASE REAL · SAFE')),
 # reel «La IA encontró 3 niveles a la misma altura» (dic-ws-clip-niveles-duplicados-reel): Gabriel no lo dice en voz alta, sale en la pantalla de Claude → cierre con el acercamiento real
 's9-niveles-duplicados': dict(base='whisper_l', edits=[('revisan', 3.2, 'revisa'), ('MCP', 7.8, 'MCP.'), ('y', 8.2, 'Y')],
      portada=dict(lines=['LA IA ENCONTRÓ', '3 NIVELES', 'A LA MISMA ALTURA'], accent=1, t=12.6), post=7.6,
      cta=dict(zoom='clip/s9-zoom.jpg', rotulo='LO QUE AVISÓ CLAUDE EN PANTALLA', frase=['3 NIVELES', 'A LA MISMA ALTURA'], pregunta=['¿REVISAS NIVELES', 'DUPLICADOS', 'ANTES DE ENTREGAR?'], boton='COMENTA NIVEL', sub='y te mando el test de nivel BIM')),
}


def retimar(ws, I):
    """Asigna cada palabra a una isla de voz (en orden) con programación dinámica y reparte dentro de la isla lo que Whisper dejó fuera."""
    n, k = len(ws), len(I); INF = 1e9
    mid = [(w['s'] + w['e']) / 2 for w in ws]
    def dist(m, i): a, b = I[i]; return 0 if a - 0.08 <= m <= b + 0.08 else min(abs(m - a), abs(m - b))
    vacio = [0.1 + min(0.45, 0.5 * (b - a)) if b - a > 0.22 else 0.02 for a, b in I]
    # cost[j][i]: mejor costo con las primeras j palabras, la j-ésima en la isla i
    cost = [[INF] * k for _ in range(n)]; back = [[0] * k for _ in range(n)]
    pre = [0.0]
    for i in range(k): pre.append(pre[-1] + vacio[i])
    for i in range(k): cost[0][i] = dist(mid[0], i) + pre[i]
    for j in range(1, n):
        for i in range(k):
            best = INF; bi = 0
            for p in range(i + 1):
                c = cost[j - 1][p] + (pre[i] - pre[p + 1] if i > p else 0)
                if c < best: best, bi = c, p
            cost[j][i] = best + dist(mid[j], i); back[j][i] = bi
    end = min(range(k), key=lambda i: cost[n - 1][i] + pre[k] - pre[i + 1])
    asg = [0] * n; asg[n - 1] = end
    for j in range(n - 1, 0, -1): asg[j - 1] = back[j][asg[j]]
    out = []; movidas = 0
    for i in range(k):
        g = [j for j in range(n) if asg[j] == i]
        if not g: continue
        a, b = I[i]
        dentro = [ws[j].get('fijo') or (a - 0.1 <= ws[j]['s'] and ws[j]['e'] <= b + 0.15) for j in g]
        res = [None] * len(g)
        if sum(dentro) >= 0.5 * len(g):
            for q, j in enumerate(g):
                if dentro[q]: res[q] = [ws[j]['s'] if ws[j].get('fijo') else max(ws[j]['s'], a - 0.05), ws[j]['e']]
            q = 0
            while q < len(g) and res is not None:
                if res[q] is not None: q += 1; continue
                r = q
                while r < len(g) and res[r] is None: r += 1
                x0 = res[q - 1][1] if q else a; x1 = res[r][0] if r < len(g) else b
                if x1 - x0 < 0.1 * (r - q): res = None; break          # no cabe: se reparte toda la isla
                tot = sum(len(ws[g[z]]['w']) + 1 for z in range(q, r)); x = x0
                for z in range(q, r):
                    dd = (x1 - x0) * (len(ws[g[z]]['w']) + 1) / tot; res[z] = [x, x + dd]; x += dd
                movidas += r - q; q = r
        else: res = None
        if res is None:
            movidas += len(g); tot = sum(len(ws[j]['w']) + 1 for j in g); x = a; res = []
            for j in g:
                dd = (b - a) * (len(ws[j]['w']) + 1) / tot; res.append([x, x + dd]); x += dd
        for q, j in enumerate(g): out.append(dict(w=ws[j]['w'], s=round(res[q][0], 3), e=round(res[q][1], 3)))
    for j in range(len(out) - 1): out[j]['e'] = round(max(out[j]['s'] + 0.02, min(out[j]['e'], out[j + 1]['s'])), 3)
    vac = [(a, b) for a, b in I if b - a > 0.3 and not any(a - 0.1 <= (w['s'] + w['e']) / 2 <= b + 0.1 or (w['s'] <= a and w['e'] >= b) for w in out)]
    if vac: print('   islas de voz sin palabra:', vac)
    return out, movidas


clips = {}
for sid, c in CFG.items():
    js = f'{P}/data/{sid}.json'; d = json.load(open(js))
    ws = [dict(w) for w in d[c['base']]]; usados = set()
    for ed in c['edits']:
        tok, at, new = ed[:3]; forz = ed[3] if len(ed) > 3 else None
        if tok is None:                                   # palabra que Whisper no dio y sí está en la transcripción original
            ws.append(dict(w=new, s=forz[0], e=forz[1], fijo=True)); ws.sort(key=lambda w: w['s']); usados = set(); continue
        cand = [i for i, w in enumerate(ws) if w['w'] == tok and abs(w['s'] - at) < 2.5]
        if not cand: cand = [i for i, w in enumerate(ws) if w['w'] == tok] if sum(w['w'] == tok for w in ws) == 1 else []
        if not cand: print('  !! no encuentro', sid, tok, at); continue
        i = min(cand, key=lambda i: abs(ws[i]['s'] - at)); ws[i]['w'] = new
        if forz: ws[i].update(s=forz[0], e=forz[1], fijo=True)
    ws.sort(key=lambda w: w['s'])
    fin_ws = []
    for w in ws:
        if w['w'] is None: continue
        parts = w['w'].split(' '); dd = (w['e'] - w['s']) / len(parts)
        for q, ptxt in enumerate(parts): fin_ws.append(dict(w=ptxt, s=w['s'] + q * dd, e=w['s'] + (q + 1) * dd, fijo=w.get('fijo', False)))
    I = islas(f'{P}/audio/{sid}-voz.wav')
    words, mov = retimar(fin_ws, I)
    fin = round(d['dur'] - 0.02 if c.get('fin_al_final') else min(d['dur'] - 0.02, max(words[-1]['e'], I[-1][1] if I[-1][1] - words[-1]['e'] < 0.6 else 0) + 0.3), 3)
    kind = 'clase' if sid.startswith('nav-') else 'short'
    po = c['portada']; po.setdefault('chip', 'CLIP DEL WORKSHOP EN VIVO')
    d.update(words=words, fin=fin, kind=kind, portada=po); extra = {k: c[k] for k in ('post', 'cta') if k in c}; d.update(extra)
    json.dump(d, open(js, 'w'), ensure_ascii=False, indent=1)
    clips[sid] = dict(id=sid, kind=kind, fin=fin, empalmes=[e for e in d['empalmes'] if e < fin - 0.3], hook=d['hook'], pie=d['pie'], words=words, portada=po, **extra)
    print(f"{sid}: {len(words)} palabras ({mov} recolocadas en su isla) · fin {fin}s de {d['dur']}s")
    print('   ', ' '.join(w['w'] for w in words))
open(f'{P}/src/clips.ts', 'w').write('// Generado por scripts/finalizar.py — no editar a mano.\nimport type { ClipData } from "./Clip";\nexport const CLIPS: Record<string, ClipData> = '
                                     + json.dumps(clips, ensure_ascii=False, indent=1) + ' as any;\n')
