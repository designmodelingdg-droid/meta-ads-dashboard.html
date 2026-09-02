#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el artefacto de la matriz de septiembre, por pestañas.

    python3 scripts/build_artefacto_matriz.py

Por que por pestañas y no un documento largo: cada grupo lo ejecuta una
persona distinta. Quien publica en comunidades no necesita leer los guiones de
LinkedIn, y quien graba los reels no necesita el calendario del blog. Una
pestaña por responsable, y el enlace se comparte igual para todos.

Fuentes (aqui no se escribe contenido a mano):
    matriz/calendario-septiembre.json   el orden y las notas
    matriz/guiones-completos.json       el contenido de las piezas con id
    matriz/historias-septiembre.py      las 20 jornadas de historias
    matriz/reels-septiembre.py          los guiones de reel y prompts de feed
"""
import html
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MATRIZ = RAIZ / "matriz-viral" / "matriz"
sys.path.insert(0, str(MATRIZ))

CAL = json.loads((MATRIZ / "calendario-septiembre.json").read_text(encoding="utf-8"))
GUI = {p["id"]: p for p in json.loads((MATRIZ / "guiones-completos.json").read_text(encoding="utf-8"))["piezas"]}

import importlib.util


def _cargar(nombre):
    spec = importlib.util.spec_from_file_location(nombre, MATRIZ / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _cargar("historias-septiembre")
R = _cargar("reels-septiembre")

e = html.escape


def bloque_pegar(txt):
    return f'<div class="pegar">{e(txt)}</div>'


SEMANAS_RANGO = {1: "S1 · 7-13 sep", 2: "S2 · 14-20 sep",
                 3: "S3 · 21-27 sep", 4: "S4 · 28 sep - 2 oct"}


def semana_de(fecha):
    """De «Lun 7» o «Vie 2 oct» a numero de semana.

    Se deriva del dia, no se anota a mano: una fecha que cambie en el
    calendario arrastra sola su semana y no hay dos verdades.
    """
    f = fecha.lower()
    nums = [int(x) for x in __import__("re").findall(r"\d+", f)]
    if not nums:
        return 0
    d = nums[0]
    if "oct" in f:
        return 4
    if d <= 13:
        return 1
    if d <= 20:
        return 2
    if d <= 27:
        return 3
    return 4


def filtro_semanas(prefijo):
    """Barra de botones que filtra por semana dentro de una pestaña."""
    o = [f'<div class="filtro" data-scope="{prefijo}">',
         f'<button class="fbtn" data-sem="0" aria-pressed="true">Todas</button>']
    for n, etq in SEMANAS_RANGO.items():
        o.append(f'<button class="fbtn" data-sem="{n}" aria-pressed="false">{e(etq)}</button>')
    o.append('</div>')
    return "".join(o)


def prompt_img(medida, texto):
    return (f'<div class="prompt"><span class="rot">Prompt para ChatGPT · {e(medida)}</span>'
            f'<div class="prompt-txt">{e(texto)}</div></div>')


# ════════════════════ PESTAÑA: RESUMEN ════════════════════
def tab_resumen():
    o = ['<h2>Cómo se usa esto</h2>',
         '<p class="intro">Una pestaña por responsable. El enlace es el mismo para todos: '
         'cada quien abre la suya. Todo lo que está en bloque ámbar se copia y se pega tal cual; '
         'los prompts de imagen se pegan en ChatGPT como están, con la medida incluida.</p>']
    o.append('<div class="tabla-scroll"><table><thead><tr><th>Pestaña</th><th>Qué contiene</th>'
             '<th>Cuándo se publica</th></tr></thead><tbody>')
    filas = [
        ("Grupo 1 · Feed", "12 piezas nuevas: 5 carruseles, 5 reels, 2 posts planos. Con copy y prompt de imagen.", "Lunes, miércoles y viernes"),
        ("Grupo 2 · Comunidades", "12 mensajes cortos, sin hashtags, listos para pegar.", "Martes, jueves y viernes"),
        ("Grupo 3 · Blog", "4 artículos con su CTA y la portada.", "Sábados"),
        ("Grupo 4 · LinkedIn", "20 publicaciones repartidas entre las 3 páginas.", "Lunes a viernes"),
        ("Grupo 5 · Historias", "80 historias: 4 al día, de lunes a viernes, con storytelling.", "Todos los días L-V"),
        ("Reels", "Guion completo segundo a segundo de los 5 reels.", "Se graban Lun 7 y Mar 8"),
        ("Publicidad", "Los creativos de las 2 campañas.", "Todo junto el lunes 7"),
    ]
    for a, b, c in filas:
        o.append(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td></tr>')
    o.append('</tbody></table></div>')

    o.append('<h2>Las reglas que no se rompen</h2><ul class="reglas">')
    for r in CAL["reglas_del_mes"]:
        o.append(f'<li>{e(r)}</li>')
    o.append('</ul>')

    o.append('<div class="dato"><strong>Los reels de agosto quedaron fuera.</strong> '
             'Los que se grabaron en agosto y nunca se publicaron no entran en este mes: '
             'todo lo que ves aquí es contenido nuevo, y cada reel tiene su guion escrito para grabarlo.</div>')

    lm = CAL.get("lead_magnets", {})
    if lm.get("por_crear"):
        o.append('<h2>Recursos gratuitos que hay que CREAR</h2>')
        o.append('<p class="intro">Los CTA del mes prometen recursos. Estos todavía no existen — '
                 'y hay contenido ya programado que los pide. Si no llegan a tiempo, el CTA se cambia '
                 'por el de reemplazo, pero la promesa vacía no se publica.</p>')
        for l in lm["por_crear"]:
            o.append(f'<div class="lm-nuevo"><h4>{e(l["nombre"])}</h4>'
                     f'<span class="lm-pal">Palabra clave sugerida: «{e(l["palabra_sugerida"])}»</span>'
                     f'<p>{e(l["para_que"])}</p></div>')
        if lm.get("mapa_cta"):
            pend = [m for m in lm["mapa_cta"] if "🔴" in m.get("estado", "") or "🟡" in m.get("estado", "")]
            if pend:
                o.append('<h3 class="camp">Qué contenido depende de cada uno</h3>')
                o.append('<div class="tabla-scroll"><table><thead><tr><th>Cuándo</th><th>Pieza</th>'
                         '<th>CTA</th><th>Estado</th><th>Reemplazo si no llega</th></tr></thead><tbody>')
                for m in pend:
                    o.append(f'<tr><td>{e(m["fecha"])}</td><td>{e(m["pieza"])}</td>'
                             f'<td><b>{e(m["cta"])}</b></td><td>{e(m["estado"])}</td>'
                             f'<td>{e(m["reemplazo"])}</td></tr>')
                o.append('</tbody></table></div>')
        o.append('<h3 class="camp">Los 8 que ya existen y funcionan</h3>')
        o.append('<div class="tabla-scroll"><table><thead><tr><th>Recurso</th><th>Palabra</th>'
                 '<th>Se usa en</th></tr></thead><tbody>')
        for l in lm.get("existentes", []):
            o.append(f'<tr><td><b>{e(l["nombre"])}</b></td><td class="t">{e(l["palabra"])}</td>'
                     f'<td>{e(l["vinculado_a"])}</td></tr>')
        o.append('</tbody></table></div>')

    o.append('<h2>Checklist del mes</h2>')
    o.append('<div class="tabla-scroll"><table><thead><tr><th>☐</th><th>Tarea</th><th>Desbloquea</th>'
             '<th>Cuándo</th></tr></thead><tbody>')
    for t in CAL.get("checklist_tareas", []):
        o.append(f'<tr><td>☐</td><td>{e(t["tarea"])}</td><td>{e(t.get("desbloquea",""))}</td>'
                 f'<td>{e(t.get("cuando",""))}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


# ════════════════════ PESTAÑA: GRUPO 1 (FEED) ════════════════════
def tab_feed():
    g = CAL["grupos"][0]
    o = [f'<h2>{e(g["nombre"])}</h2>', f'<p class="intro">{e(g["descripcion"])}</p>']
    o.append('<ul class="reglas">' + "".join(f'<li>{e(r)}</li>' for r in g["reglas"]) + '</ul>')
    o.append(filtro_semanas("g1"))
    for ent in g["calendario"]:
        pid = ent.get("id")
        p = GUI.get(pid) if pid else None
        titulo = p["titulo"] if p else ent["idea"]["titulo"]
        sem = semana_de(ent["fecha"])
        o.append(f'<div class="pieza" data-sem="{sem}"><div class="pieza-cab">'
                 f'<span class="fecha">{e(ent["fecha"])}</span>'
                 f'<h3>{e(titulo)}</h3><span class="tipo">{e(ent["formato_publicacion"])}</span></div>')
        if ent.get("nota"):
            o.append(f'<p class="nota">{e(ent["nota"])}</p>')
        if p:
            o.append(f'<span class="rot">Hook</span>{bloque_pegar(p["hook"])}')
            if p.get("slides"):
                o.append('<span class="rot">Slides</span><ol class="slides">')
                for s in p["slides"]:
                    o.append(f'<li><b>Slide {s["n"]}</b> — {e(s["texto"])}'
                             f'<br><span class="visual">🖼 {e(s.get("visual",""))}</span></li>')
                o.append('</ol>')
            if p.get("caption"):
                o.append(f'<span class="rot">Caption (copiar tal cual)</span>{bloque_pegar(p["caption"])}')
            if p.get("notas_produccion"):
                o.append(f'<p class="nota">⚠ {e(p["notas_produccion"])}</p>')
        else:
            d = ent["idea"]
            o.append(f'<span class="rot">Desarrollo</span>{bloque_pegar(d["desarrollo"])}')
            o.append('<p class="nota">El guion completo de este reel está en la pestaña <b>Reels</b>.</p>')
        clave = pid if pid in R.FEED_PROMPTS else ("post-varilla" if "varilla" in titulo.lower() else None)
        if clave:
            medida, txt = R.FEED_PROMPTS[clave]
            o.append(prompt_img(medida, txt))
        o.append('</div>')
    return "\n".join(o)


# ════════════════════ PESTAÑAS 2, 3, 4 (genéricas) ════════════════════
def tab_grupo(idx):
    g = CAL["grupos"][idx]
    o = [f'<h2>{e(g["nombre"])}</h2>', f'<p class="intro">{e(g["descripcion"])}</p>']
    if g.get("reglas"):
        o.append('<ul class="reglas">' + "".join(f'<li>{e(r)}</li>' for r in g["reglas"]) + '</ul>')
    o.append(filtro_semanas(f"g{idx+1}"))
    for ent in g["calendario"]:
        pid = ent.get("id")
        p = GUI.get(pid) if pid else None
        titulo = p["titulo"] if p else ent["idea"]["titulo"]
        sem = semana_de(ent["fecha"])
        o.append(f'<div class="pieza" data-sem="{sem}"><div class="pieza-cab">'
                 f'<span class="fecha">{e(ent["fecha"])}</span>'
                 f'<h3>{e(titulo)}</h3><span class="tipo">{e(ent["formato_publicacion"])}</span></div>')
        if ent.get("nota"):
            o.append(f'<p class="nota">{e(ent["nota"])}</p>')
        if ent.get("idea"):
            o.append(f'<span class="rot">Qué se publica</span>{bloque_pegar(ent["idea"]["desarrollo"])}')
        elif p:
            o.append(f'<span class="rot">Hook</span>{bloque_pegar(p["hook"])}')
            if p.get("caption"):
                o.append(f'<span class="rot">Texto</span>{bloque_pegar(p["caption"])}')
        o.append('</div>')
    return "\n".join(o)


# ════════════════════ PESTAÑA: HISTORIAS ════════════════════
def tab_historias():
    g = CAL["grupos"][4]
    o = [f'<h2>{e(g["nombre"])}</h2>',
         '<p class="intro">Cuatro historias al día, de lunes a viernes, en este orden: '
         '<b>relleno</b> (abre en humano) → <b>valor</b> (el dato del día) → <b>interacción</b> '
         '(el sticker que abre el DM) → <b>venta</b> (pide una palabra, que es lo único que el bot '
         'puede recoger). Cada día es un arco, no cuatro piezas sueltas.</p>']
    o.append('<ul class="reglas">' + "".join(f'<li>{e(r)}</li>' for r in g["reglas"]) + '</ul>')
    o.append(filtro_semanas("g5"))
    for sem in H.SEMANAS:
        o.append(f'<div class="semana" data-sem="{sem["n"]}"><div class="semana-cab"><span class="snum">S{sem["n"]}</span>'
                 f'<div><h3>{e(sem["hilo"])}</h3><span class="rango">{e(sem["rango"])}</span></div></div>'
                 f'<p class="nota">{e(sem["porque"])}</p>')
        for d in sem["dias"]:
            o.append(f'<div class="dia"><h4>{e(d["dia"])} · <span>{e(d["titulo"])}</span></h4>')
            for i, hh in enumerate(d["historias"], 1):
                o.append(f'<div class="hist"><div class="hist-cab"><span class="frame">{i}</span>'
                         f'<span class="rol rol-{hh["rol"][:4].lower()}">{e(hh["rol"])}</span></div>')
                o.append(bloque_pegar(hh["texto"]))
                o.append(f'<p class="sticker"><b>Sticker:</b> {e(hh["sticker"])}</p>')
                o.append(prompt_img(H.MEDIDA, hh["prompt"]))
                o.append('</div>')
            o.append('</div>')
        o.append('</div>')
    return "\n".join(o)


# ════════════════════ PESTAÑA: REELS ════════════════════
def tab_reels():
    o = ['<h2>Guiones de reels — para grabar</h2>',
         '<p class="intro">Cinco reels. Cuatro por grabar y uno ya editado. Cada guion va segundo a '
         'segundo: qué se ve, qué se dice y qué texto aparece en pantalla. '
         'Las palabras entre **asteriscos** van resaltadas en ámbar en el subtítulo.</p>',
         '<div class="dato"><strong>La regla del primer segundo.</strong> Se abre con la frontera — '
         'la afirmación que incomoda o el dato que sorprende — nunca con la invitación. En agosto un '
         'reel que abría presentándose hizo 198 vistas y cero de todo.</div>']
    for r in R.REELS:
        cls = "listo" if "EDITADO" in r["estado"] else ("gated" if "CONDICIONADO" in r["estado"] else "")
        o.append(f'<div class="reel {cls}"><div class="pieza-cab"><span class="fecha">{e(r["fecha"])}</span>'
                 f'<h3>{e(r["titulo"])}</h3><span class="tipo">{e(r["duracion"])}</span></div>')
        o.append(f'<p class="estado">{e(r["estado"])}</p>')
        o.append(f'<p class="nota">{e(r["nota"])}</p>')
        o.append(f'<p class="cta-linea"><b>CTA:</b> {e(r["cta"])}</p>')
        o.append('<div class="tabla-scroll"><table><thead><tr><th>Tiempo</th><th>Qué se ve</th>'
                 '<th>Qué se dice</th><th>Texto en pantalla</th></tr></thead><tbody>')
        for t, ve, di, tx in r["guion"]:
            tx_html = e(tx).replace("**", "|")
            partes = tx_html.split("|")
            tx_html = "".join(p if i % 2 == 0 else f'<b class="amb">{p}</b>' for i, p in enumerate(partes))
            o.append(f'<tr><td class="t">{e(t)}</td><td>{e(ve)}</td><td>{e(di)}</td><td>{tx_html}</td></tr>')
        o.append('</tbody></table></div></div>')
    return "\n".join(o)


# ════════════════════ PESTAÑA: PUBLICIDAD ════════════════════
def ficha_anuncio(p):
    """Un anuncio con su copy listo para pegar y su ficha de montaje.

    El copy y la ficha se separan a proposito: lo de arriba se copia tal cual
    en Meta, lo de abajo se configura. Mezclarlos en un solo bloque fue lo que
    hizo que en agosto se pegaran instrucciones dentro del texto del anuncio.
    """
    o = [f'<div class="ad"><div class="ad-cab"><span class="tipo">{e(p["formato"])}</span>'
         f'<h3>{e(p["titulo"])}</h3><span class="precio-ad">{e(p["precio"])}</span></div>']
    o.append(f'<p class="hook">{e(p["hook"])}</p>')
    o.append('<p class="etq">Texto principal — se pega tal cual</p>')
    o.append(bloque_pegar(p["cuerpo"]))
    o.append('<div class="campos">'
             f'<div><span class="etq">Titular</span><code>{e(p["titular"])}</code></div>'
             f'<div><span class="etq">Descripción</span><code>{e(p["descripcion"])}</code></div>'
             '</div>')
    o.append(f'<p class="etq">Creativo</p><p class="creativo">{e(p["creativo"])}</p>')
    o.append('<details class="prompt"><summary>Prompt de imagen para ChatGPT</summary>'
             f'{bloque_pegar(p["prompt"])}</details>')
    o.append('<p class="etq">Ficha de montaje</p><div class="tabla-scroll"><table class="cfg">'
             '<tbody>')
    for k, v in p["cfg"]:
        dura = "dura" if k.isupper() or "NO va" in k or "bloque" in k.lower() else ""
        o.append(f'<tr class="{dura}"><th>{e(k)}</th><td>{e(v)}</td></tr>')
    o.append('</tbody></table></div></div>')
    return "\n".join(o)


def tab_pauta():
    pub = CAL["publicidad"]
    o = ['<h2>Publicidad — sale todo junto el lunes 7</h2>',
         f'<p class="intro">{e(pub["nota"])}</p>']
    if pub.get("indicaciones"):
        o.append('<div class="indic"><h3>Antes de subir nada</h3>')
        for k, v in pub["indicaciones"]:
            o.append(f'<p><b>{e(k)}.</b> {e(v)}</p>')
        o.append('</div>')
    for c in pub["campanas"]:
        o.append(f'<h3 class="camp">{e(c["nombre"])}</h3>')
        for p in c["piezas"]:
            if "cuerpo" in p:
                o.append(ficha_anuncio(p))
                continue
            o.append(f'<div class="pieza"><div class="pieza-cab"><span class="tipo">{e(p["formato"])}</span>'
                     f'<h3>{e(p["titulo"])}</h3></div>')
            o.append(bloque_pegar(p["copy"]))
            if p.get("condicion"):
                o.append(f'<p class="nota">⚠ {e(p["condicion"])}</p>')
            o.append('</div>')
    return "\n".join(o)


# ════════════════════ ARMADO ════════════════════
PESTANAS = [
    ("resumen", "Resumen", tab_resumen),
    ("g1", "G1 · Feed", tab_feed),
    ("g2", "G2 · Comunidades", lambda: tab_grupo(1)),
    ("g3", "G3 · Blog", lambda: tab_grupo(2)),
    ("g4", "G4 · LinkedIn", lambda: tab_grupo(3)),
    ("g5", "G5 · Historias", tab_historias),
    ("reels", "Reels", tab_reels),
    ("pauta", "Publicidad", tab_pauta),
]

CSS = """
:root{
  --navy:#0E2438; --amber:#E8A04A; --amber-deep:#B8752A;
  --ground:#F2F5F8; --surface:#FFFFFF; --surface-2:#E9EEF3;
  --ink:#0E2438; --ink-2:#4A5F73; --ink-3:#7A8CA0;
  --line:#D3DDE6; --line-strong:#B3C2D0;
  --ok:#1F7A5A; --ok-bg:#E4F2EC;
  --stop:#A33B2A; --stop-bg:#F8E7E3;
  --wait-bg:#FBF0DA;
  --display:'Overpass',system-ui,sans-serif;
  --body:'Nunito',system-ui,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#0B1A28; --surface:#122536; --surface-2:#193347;
  --ink:#E8EFF5; --ink-2:#A9BDCE; --ink-3:#7B93A8;
  --line:#24435C; --line-strong:#365A76;
  --ok:#5DC79E; --ok-bg:#123028; --stop:#E4907E; --stop-bg:#3A1E19;
  --wait-bg:#33280F; --amber-deep:#E8A04A;
}}
:root[data-theme="dark"]{
  --ground:#0B1A28; --surface:#122536; --surface-2:#193347;
  --ink:#E8EFF5; --ink-2:#A9BDCE; --ink-3:#7B93A8;
  --line:#24435C; --line-strong:#365A76;
  --ok:#5DC79E; --ok-bg:#123028; --stop:#E4907E; --stop-bg:#3A1E19;
  --wait-bg:#33280F; --amber-deep:#E8A04A;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--body);
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1040px;margin:0 auto;padding:0 22px 80px}
header{background:var(--navy);color:#EAF1F7;padding:38px 0 30px;border-bottom:4px solid var(--amber)}
.eyebrow{font-family:var(--display);font-weight:800;font-size:12px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--amber);margin:0 0 8px}
h1{font-family:var(--display);font-weight:900;font-size:clamp(28px,4.6vw,42px);line-height:1.06;
  margin:0 0 12px;text-wrap:balance}
.lede{font-size:16.5px;color:#B9CBDA;max-width:64ch;margin:0}
nav{position:sticky;top:0;z-index:30;background:var(--ground);border-bottom:1px solid var(--line);
  overflow-x:auto;-webkit-overflow-scrolling:touch}
nav .wrap{display:flex;gap:4px;padding:0 22px;min-width:max-content}
nav button{appearance:none;background:none;border:0;border-bottom:3px solid transparent;
  font-family:var(--display);font-weight:700;font-size:14px;color:var(--ink-2);
  padding:14px 14px 11px;cursor:pointer;white-space:nowrap}
nav button:hover{color:var(--ink)}
nav button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--amber)}
nav button:focus-visible{outline:3px solid var(--amber);outline-offset:-3px}
section[hidden]{display:none}
section{padding-top:26px}
h2{font-family:var(--display);font-weight:800;font-size:24px;margin:0 0 12px;
  padding-bottom:10px;border-bottom:2px solid var(--navy)}
h3.camp{font-family:var(--display);font-weight:800;font-size:18px;color:var(--amber-deep);
  margin:28px 0 10px}
p.intro{color:var(--ink-2);font-size:15.5px;max-width:70ch}
ul.reglas{padding-left:20px;margin:14px 0}
ul.reglas li{font-size:14.5px;color:var(--ink-2);margin-bottom:7px}
.tabla-scroll{overflow-x:auto;margin:16px 0;border:1px solid var(--line);border-radius:8px;
  background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px}
th{background:var(--navy);color:#EAF1F7;font-family:var(--display);font-weight:700;text-align:left;
  padding:10px 13px;font-size:12px;letter-spacing:.05em;text-transform:uppercase}
td{padding:10px 13px;border-top:1px solid var(--line);vertical-align:top}
td.t{font-family:var(--mono);font-size:12.5px;white-space:nowrap;color:var(--amber-deep)}
b.amb{color:var(--amber-deep)}
.pieza,.reel{background:var(--surface);border:1px solid var(--line);border-radius:9px;
  padding:16px 18px;margin:14px 0}
.reel.listo{border-left:4px solid var(--ok)}
.reel.gated{border-left:4px solid var(--stop)}
.pieza-cab{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:8px}
.pieza-cab h3{font-family:var(--display);font-weight:800;font-size:17px;margin:0;flex:1;min-width:200px}
.fecha{font-family:var(--mono);font-size:12.5px;font-weight:600;color:var(--amber-deep);white-space:nowrap}
.tipo{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--ink-2);border:1px solid var(--line-strong);padding:2px 8px;border-radius:99px;white-space:nowrap}
.estado{font-family:var(--display);font-weight:800;font-size:12px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--amber-deep);margin:0 0 8px}
.cta-linea{font-size:14px;margin:8px 0}
.rot{font-family:var(--display);font-weight:800;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);display:block;margin:12px 0 4px}
.pegar{background:var(--surface-2);border-left:3px solid var(--amber);padding:11px 13px;
  border-radius:0 5px 5px 0;font-size:14.5px;white-space:pre-wrap}
.prompt{margin-top:10px}
/* ── anuncios ── */
.ad{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:16px 18px;margin:14px 0}
.ad-cab{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
  border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:12px}
.ad-cab h3{font-family:var(--display);font-weight:800;font-size:19px;margin:0;flex:1 1 auto}
.precio-ad{font-family:var(--mono);font-size:13px;color:var(--amber-deep);font-weight:700}
.hook{font-family:var(--display);font-weight:800;font-size:17px;line-height:1.35;
  margin:0 0 12px;color:var(--ink)}
.etq{font-family:var(--display);font-weight:800;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);display:block;margin:14px 0 5px}
.campos{display:flex;gap:12px;flex-wrap:wrap;margin-top:4px}
.campos>div{flex:1 1 200px}
.campos .etq{margin-top:0}
.campos code{display:block;background:var(--surface-2);border:1px solid var(--line);
  border-radius:5px;padding:7px 10px;font-family:var(--mono);font-size:13px}
.creativo{margin:0;font-size:14.5px;color:var(--ink-2)}
table.cfg th{width:150px;text-align:left;vertical-align:top;font-family:var(--display);
  font-weight:800;font-size:12.5px;color:var(--ink-2);white-space:normal}
table.cfg td{font-size:14px}
table.cfg tr.dura th{color:var(--stop)}
table.cfg tr.dura td{background:var(--stop-bg)}
.indic{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--amber);
  border-radius:0 10px 10px 0;padding:14px 18px;margin:16px 0}
.indic h3{font-family:var(--display);font-weight:800;font-size:15px;margin:0 0 8px;
  text-transform:uppercase;letter-spacing:.06em;color:var(--amber-deep)}
.indic p{margin:0 0 9px;font-size:14.5px}
.indic p:last-child{margin-bottom:0}
.prompt-txt{background:var(--wait-bg);border-left:3px solid var(--amber-deep);padding:10px 13px;
  border-radius:0 5px 5px 0;font-size:13px;font-family:var(--mono);line-height:1.55}
.nota{border-left:3px solid var(--line-strong);padding:2px 0 2px 12px;margin:10px 0;
  font-size:13.5px;color:var(--ink-2);font-style:italic}
.dato{background:var(--stop-bg);border-left:4px solid var(--stop);padding:13px 16px;
  border-radius:0 6px 6px 0;margin:16px 0;font-size:14.5px}
.dato strong{font-family:var(--display);font-weight:800}
ol.slides{padding-left:20px;margin:6px 0}
ol.slides li{font-size:14px;margin-bottom:9px}
.visual{color:var(--ink-3);font-size:13px;font-style:italic}
.semana{margin:26px 0 34px}
.semana-cab{display:flex;align-items:center;gap:14px;border-bottom:2px solid var(--navy);
  padding-bottom:10px;margin-bottom:8px}
.snum{font-family:var(--display);font-weight:900;font-size:32px;color:var(--amber);line-height:1}
.semana-cab h3{font-family:var(--display);font-weight:800;font-size:19px;margin:0}
.rango{font-family:var(--mono);font-size:12px;color:var(--ink-2)}
.dia{margin:18px 0;padding:14px 16px;background:var(--surface);border:1px solid var(--line);border-radius:9px}
.dia h4{font-family:var(--display);font-weight:800;font-size:15.5px;margin:0 0 10px;
  color:var(--amber-deep)}
.dia h4 span{color:var(--ink);font-weight:700}
.hist{border-top:1px solid var(--line);padding:12px 0 4px}
.hist:first-of-type{border-top:0;padding-top:0}
.hist-cab{display:flex;align-items:center;gap:9px;margin-bottom:6px}
.frame{font-family:var(--mono);font-size:11px;font-weight:600;background:var(--navy);color:#fff;
  width:20px;height:20px;border-radius:50%;display:grid;place-items:center;flex:none}
.rol{font-family:var(--display);font-weight:800;font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;padding:2px 8px;border-radius:99px}
.rol-rell{background:var(--surface-2);color:var(--ink-2)}
.rol-valo{background:var(--ok-bg);color:var(--ok)}
.rol-inte{background:var(--wait-bg);color:var(--amber-deep)}
.rol-vent{background:var(--stop-bg);color:var(--stop)}
.sticker{font-size:13.5px;margin:8px 0 0;color:var(--ink-2)}
.sticker b{font-family:var(--display);color:var(--ink)}
.filtro{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0 4px;padding:10px 0;
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.fbtn{appearance:none;font-family:var(--display);font-weight:700;font-size:12.5px;
  padding:6px 13px;border-radius:99px;border:1px solid var(--line-strong);
  background:var(--surface);color:var(--ink-2);cursor:pointer;white-space:nowrap}
.fbtn:hover{border-color:var(--amber);color:var(--ink)}
.fbtn[aria-pressed="true"]{background:var(--navy);border-color:var(--navy);color:#fff}
.fbtn:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.vacio{display:none;padding:20px;text-align:center;color:var(--ink-3);font-style:italic}
.lm-nuevo{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--amber);
  border-radius:0 8px 8px 0;padding:14px 17px;margin:12px 0}
.lm-nuevo h4{font-family:var(--display);font-weight:800;font-size:16px;margin:0 0 4px}
.lm-pal{font-family:var(--mono);font-size:12.5px;color:var(--amber-deep);font-weight:600}
.lm-nuevo p{font-size:14px;color:var(--ink-2);margin:8px 0 0}
.lm-cta{font-size:13.5px;margin:8px 0 0;color:var(--stop);font-weight:600}
footer{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--ink-3);font-family:var(--mono)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = """
(function(){
  var bs = Array.prototype.slice.call(document.querySelectorAll('nav button'));
  var ss = Array.prototype.slice.call(document.querySelectorAll('section'));
  function ir(id){
    bs.forEach(function(b){ b.setAttribute('aria-selected', String(b.dataset.t === id)); });
    ss.forEach(function(s){ s.hidden = (s.id !== 'tab-' + id); });
    try { localStorage.setItem('dma-matriz-sep-tab', id); } catch(e){}
    window.scrollTo({top:0, behavior:'instant'});
  }
  bs.forEach(function(b){ b.addEventListener('click', function(){ ir(b.dataset.t); }); });
  var guardada = null;
  try { guardada = localStorage.getItem('dma-matriz-sep-tab'); } catch(e){}
  ir(bs.some(function(b){return b.dataset.t === guardada;}) ? guardada : bs[0].dataset.t);

  // Filtro por semana, dentro de cada pestaña.
  Array.prototype.forEach.call(document.querySelectorAll('.filtro'), function(f){
    var seccion = f.closest('section');
    var items = Array.prototype.slice.call(seccion.querySelectorAll('[data-sem]'))
                  .filter(function(x){ return !x.classList.contains('fbtn'); });
    var vacio = document.createElement('p');
    vacio.className = 'vacio';
    vacio.textContent = 'No hay nada programado esa semana en este grupo.';
    seccion.appendChild(vacio);
    f.addEventListener('click', function(ev){
      var b = ev.target.closest('.fbtn');
      if (!b) return;
      var sem = b.dataset.sem;
      Array.prototype.forEach.call(f.querySelectorAll('.fbtn'), function(x){
        x.setAttribute('aria-pressed', String(x === b));
      });
      var visibles = 0;
      items.forEach(function(it){
        var ok = (sem === '0') || (it.dataset.sem === sem);
        it.hidden = !ok;
        if (ok) visibles++;
      });
      vacio.style.display = visibles ? 'none' : 'block';
    });
  });
})();
"""


def main():
    partes = ['<title>Matriz Septiembre DMA</title>',
              '<link rel="preconnect" href="https://fonts.googleapis.com">',
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
              'family=Overpass:wght@400;700;800;900&family=Nunito:wght@400;600;700&'
              'family=JetBrains+Mono:wght@400;600&display=swap">',
              f'<style>{CSS}</style>',
              '<header><div class="wrap">',
              '<p class="eyebrow">Design Modeling Academy · 7 de septiembre – 2 de octubre</p>',
              '<h1>Matriz de Septiembre</h1>',
              f'<p class="lede">{e(CAL["subtitulo"])}</p>',
              '</div></header>',
              '<nav><div class="wrap">']
    for k, etq, _ in PESTANAS:
        partes.append(f'<button data-t="{k}" role="tab" aria-selected="false">{e(etq)}</button>')
    partes.append('</div></nav><div class="wrap">')
    for k, _, fn in PESTANAS:
        partes.append(f'<section id="tab-{k}" hidden>{fn()}</section>')
    partes.append('<footer>Design Modeling Academy · Matriz de contenido de septiembre 2026<br>'
                  'Construida sobre la matriz viral (162 piezas con métricas reales), el rendimiento de las '
                  'campañas y la nueva arquitectura comercial del Máster. La pestaña abierta se recuerda en '
                  'este navegador.</footer></div>')
    partes.append(f'<script>{JS}</script>')

    salida = RAIZ / "matriz-viral" / "entregables" / "matriz-septiembre-artefacto.html"
    salida.write_text("\n".join(partes), encoding="utf-8")
    kb = salida.stat().st_size / 1024
    n_hist = sum(len(d["historias"]) for s in H.SEMANAS for d in s["dias"])
    print(f"OK → {salida} ({kb:.0f} KB)")
    print(f"   {len(PESTANAS)} pestañas · {n_hist} historias · {len(R.REELS)} guiones de reel")


if __name__ == "__main__":
    main()
