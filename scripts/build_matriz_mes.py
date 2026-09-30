#!/usr/bin/env python3
"""Artefacto por pestañas y JSON completo de la matriz de UN mes.

    python3 scripts/build_matriz_mes.py --mes 2026-10
      → matriz-viral/entregables/matriz-octubre-artefacto.html
      → matriz-viral/entregables/matriz-octubre-2026-COMPLETA.json

Por qué existe: septiembre tiene sus generadores escritos a mano
(build_artefacto_matriz.py y export_matriz_json.py leen historias-septiembre.py,
reels-septiembre.py…). Desde octubre TODO el contenido vive en
guiones-completos.json y el orden en calendario-<mes>.json, así que un solo
generador sirve para cualquier mes: pinta cada pieza con todos sus campos y no
depende de ficheros sueltos del mes.

Regla de este generador: ningún campo de una pieza se pierde. Lo que no tiene
un sitio conocido sale al final de la ficha con su nombre, como texto o tabla.
"""
import argparse
import ast
import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MATRIZ = RAIZ / "matriz-viral" / "matriz"
ENTREGABLES = RAIZ / "matriz-viral" / "entregables"
MESES = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio", "07": "julio",
         "08": "agosto", "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}
e = html.escape


def estilos_de_septiembre():
    """CSS y JS del artefacto de septiembre, leídos sin ejecutar su módulo.

    Así los dos artefactos se ven igual y el de septiembre no se toca.
    """
    arbol = ast.parse((RAIZ / "scripts" / "build_artefacto_matriz.py").read_text(encoding="utf-8"))
    out = {}
    for n in arbol.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("CSS", "JS"):
            out[n.targets[0].id] = n.value.value
    return out["CSS"], out["JS"]


def clave(*partes):
    txt = "-".join(str(x) for x in partes).lower()
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", txt)).strip("-")[:70]


def chk(k):
    return (f'<label class="chk" title="Marcar como hecho — la pieza se cierra">'
            f'<input type="checkbox" data-k="{e(k)}"><span aria-hidden="true"></span></label>')


def pegar(t):
    return f'<div class="pegar">{e(str(t))}</div>'


def rot(t):
    return f'<span class="rot">{e(t)}</span>'


def tabla(cab, filas):
    o = ['<div class="tabla-scroll"><table><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in cab) + '</tr></thead><tbody>']
    for f in filas:
        o.append("<tr>" + "".join(f"<td>{valor_corto(c)}</td>" for c in f) + "</tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


def valor_corto(v):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)) and all(not isinstance(x, (dict, list)) for x in v):
        return e(", ".join(str(x) for x in v))
    if isinstance(v, (dict, list)):
        return f'<code>{e(json.dumps(v, ensure_ascii=False))}</code>'
    return e(str(v)).replace("\n", "<br>")


def valor(v):
    """Cualquier valor de una pieza, en HTML legible."""
    if isinstance(v, str):
        return pegar(v)
    if isinstance(v, list):
        if not v:
            return ""
        if all(isinstance(x, str) for x in v):
            return '<ul class="reglas">' + "".join(f"<li>{e(x)}</li>" for x in v) + "</ul>"
        if all(isinstance(x, dict) for x in v):
            cols = []
            for x in v:
                cols += [k for k in x if k not in cols]
            return tabla(cols, [[x.get(c) for c in cols] for x in v])
        if all(isinstance(x, list) for x in v):
            return tabla([""] * max(len(x) for x in v), v)
    if isinstance(v, dict):
        return tabla(["Campo", "Contenido"], [[k.replace("_", " "), x] for k, x in v.items()])
    return pegar(v)


META = {"id", "fecha", "fecha_iso", "semana", "grupo", "tipo", "formato", "formato_detalle", "redes", "red_principal",
        "origen", "cta", "guion_columnas", "guion_video_columnas", "estado", "titulo", "eje", "pilar", "audiencia",
        "producto", "angulo", "reparto", "cuenta", "guion"}


def guion_filas(filas, cols):
    cols = cols or ["tiempo", "escena", "voz", "en pantalla"]
    o = ['<div class="tabla-scroll"><table><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in cols) + "</tr></thead><tbody>"]
    for r in filas:
        celdas = []
        for i, c in enumerate(r):
            txt = e(str(c))
            txt = "".join(x if j % 2 == 0 else f'<b class="amb">{x}</b>' for j, x in enumerate(txt.split("**")))
            celdas.append(f'<td class="t">{txt}</td>' if i == 0 else f"<td>{txt}</td>")
        o.append("<tr>" + "".join(celdas) + "</tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


def cuerpo_pieza(p):
    """Todos los campos de una pieza, en el orden en que se usan."""
    o, hecho = [], set(META)

    def usa(k, etiqueta, fn=valor):
        if p.get(k) not in (None, "", [], {}):
            o.append(rot(etiqueta) + fn(p[k]))
        hecho.add(k)

    if p.get("condicion"):
        o.append(f'<p class="nota">⚠ {e(p["condicion"])}</p>')
    hecho.add("condicion")
    usa("hook", "Hook (primeros 3 segundos / primera diapositiva)")
    if isinstance(p.get("guion"), list) and p["guion"] and isinstance(p["guion"][0], list):
        o.append(rot("Guion — segundo a segundo") + guion_filas(p["guion"], p.get("guion_columnas")))
        hecho.add("guion_reel")
    elif p.get("guion_reel"):
        o.append(rot("Guion — segundo a segundo") + guion_filas(
            [[g.get("tiempo", ""), g.get("accion", ""), g.get("voz", "")] for g in p["guion_reel"]], ["tiempo", "qué se ve", "qué se dice"]))
        hecho.add("guion_reel")
    if isinstance(p.get("guion_video"), list) and p["guion_video"]:
        o.append(rot("Guion del video de pizarrón") + guion_filas(p["guion_video"], p.get("guion_video_columnas")))
    hecho.add("guion_video")
    if p.get("slides"):
        o.append(rot(f"Diapositivas ({len(p['slides'])})") + '<ol class="slides">')
        for i, s in enumerate(p["slides"]):
            s = s if isinstance(s, dict) else {"texto": s}
            vis = (s.get("visual") or "").strip()
            o.append(f'<li><b>Slide {s.get("n", i + 1)}</b> — {e(str(s.get("texto", "")))}'
                     + (f'<br><span class="visual">🖼 {e(vis)}</span>' if vis else "") + "</li>")
        o.append("</ol>")
    hecho.add("slides")
    usa("slides_nota", "Nota de las diapositivas")
    usa("imagen", "Imagen del post")
    usa("historias", "Frames de la historia")
    if p.get("texto_principal"):
        o.append(rot("Texto principal del anuncio — se pega tal cual") + pegar(p["texto_principal"]))
        o.append('<div class="campos">' + "".join(
            f'<div><span class="etq">{e(k)}</span><code>{e(str(p.get(c) or "—"))}</code></div>'
            for k, c in (("Titular", "titular"), ("Descripción", "descripcion"), ("Botón", "boton"))) + "</div>")
    hecho |= {"texto_principal", "titular", "descripcion", "boton"}
    usa("mensaje_bienvenida", "Mensaje de bienvenida (WhatsApp)")
    usa("creativo", "Creativo")
    usa("publico_sugerido", "Público")
    usa("que_medir", "Qué medir")
    usa("por_que", "Por qué")
    if p.get("asunto"):
        o.append(tabla(["Correo", ""], [["Asunto", p.get("asunto")], ["Preencabezado", p.get("preencabezado")],
                                        ["A quién", p.get("segmento")], ["Enlace", p.get("enlace_recurso")]]))
    hecho |= {"asunto", "preencabezado", "segmento", "enlace_recurso"}
    if p.get("cuerpo"):
        c = p["cuerpo"]
        o.append(rot("Cuerpo del correo — se pega tal cual") + pegar("\n\n".join(c) if isinstance(c, list) else c))
    hecho.add("cuerpo")
    usa("caption", "Caption — se copia tal cual")
    usa("copy", "Texto — se copia tal cual")
    usa("mensajes", "Mensajes")
    usa("primer_comentario", "Primer comentario")
    usa("post_linkedin", "Post de LinkedIn")
    usa("seo", "SEO del artículo")
    usa("estructura", "Estructura del artículo")
    if p.get("articulo_markdown"):
        o.append(f'<details class="prompt"><summary>Artículo completo (markdown, se pega en el blog)</summary>{pegar(p["articulo_markdown"])}</details>')
    hecho.add("articulo_markdown")
    usa("post_anuncio_feed", "Post que anuncia el artículo")
    usa("cta_por_red", "CTA por red")
    usa("version_tiktok", "Versión TikTok")
    usa("tablero", "Tablero físico")
    usa("entrevista", "Preguntas de la entrevista")
    if p.get("prompt_imagenes"):
        o.append(f'<details class="prompt"><summary>Prompt de imagen para ChatGPT</summary>{pegar(p["prompt_imagenes"])}</details>')
    hecho.add("prompt_imagenes")
    if p.get("notas_produccion") and p.get("notas_produccion") != p.get("condicion"):
        o.append(f'<p class="nota">{e(p["notas_produccion"])}</p>')
    hecho.add("notas_produccion")
    for k, v in p.items():
        if k not in hecho and v not in (None, "", [], {}):
            o.append(rot(k.replace("_", " ")) + valor(v))
    return "\n".join(o)


class Mes:
    def __init__(self, mes):
        self.mes = mes
        self.nombre = MESES[mes[5:7]]
        self.cal = json.loads((MATRIZ / f"calendario-{self.nombre}.json").read_text(encoding="utf-8"))
        self.gui = {p["id"]: p for p in json.loads((MATRIZ / "guiones-completos.json").read_text(encoding="utf-8"))["piezas"]}
        self.semanas = []
        for g in self.cal["grupos"]:
            for x in g["calendario"]:
                if x.get("semana") and x["semana"] not in self.semanas:
                    self.semanas.append(x["semana"])
        self.semanas.sort(key=lambda s: int(re.search(r"\d+", s).group()))

    def num_semana(self, ent):
        s = ent.get("semana") or (self.gui.get(ent.get("id"), {}).get("semana"))
        return self.semanas.index(s) + 1 if s in self.semanas else 0

    def filtro(self, prefijo):
        o = [f'<div class="filtro" data-scope="{prefijo}"><button class="fbtn" data-sem="0" aria-pressed="true">Todas</button>']
        for i, s in enumerate(self.semanas, 1):
            corto = re.sub(r"Semana (\d+) \((.*)\)", r"S\1 · \2", s)
            o.append(f'<button class="fbtn" data-sem="{i}" aria-pressed="false">{e(corto)}</button>')
        return "".join(o) + "</div>"

    @staticmethod
    def avance():
        return ('<div class="avance"><span><b class="n">0</b> de <b class="tot">0</b> marcadas</span>'
                '<button type="button" class="reabrir">Reabrir todas</button></div>')

    # ───────────── pestañas ─────────────
    def tab_grupo(self, idx):
        g = self.cal["grupos"][idx]
        o = [f'<h2>{e(g["nombre"])}</h2>', f'<p class="intro">{e(g.get("descripcion", ""))}</p>']
        if g.get("reglas"):
            o.append('<ul class="reglas">' + "".join(f"<li>{e(r)}</li>" for r in g["reglas"]) + "</ul>")
        o.append(self.filtro(f"g{idx + 1}") + self.avance())
        for ent in g["calendario"]:
            p = self.gui.get(ent.get("id")) or {}
            titulo = p.get("titulo") or (ent.get("idea") or {}).get("titulo") or ent.get("titulo") or ""
            k = clave(f"g{idx + 1}", ent.get("fecha_iso") or ent["fecha"], titulo)
            chips = []
            if ent.get("intencion"):
                chips.append(f'<span class="tipo">{e(ent["intencion"])}</span>')
            if ent.get("producto") or p.get("producto"):
                chips.append(f'<span class="tipo">{e(ent.get("producto") or p.get("producto"))}</span>')
            if ent.get("destacada"):
                chips.append(f'<span class="tipo">Destacada {e(ent["destacada"])}</span>')
            if ent.get("cuenta") or p.get("cuenta"):
                chips.append(f'<span class="tipo">{e(ent.get("cuenta") or p.get("cuenta"))}</span>')
            o.append(f'<div class="pieza col" data-sem="{self.num_semana(ent)}" data-k="{k}">'
                     f'<div class="pieza-cab cab">{chk(k)}<span class="fecha">{e(ent["fecha"])}</span>'
                     f'<h3>{e(titulo)}</h3><span class="tipo">{e(ent.get("formato_publicacion") or p.get("formato") or "")}</span>'
                     + "".join(chips) + "</div>")
            linea = [x for x in (("CTA", ent.get("cta")), ("Redes", ", ".join(p.get("redes") or [])),
                                  ("Ángulo", p.get("angulo")), ("A quién", p.get("audiencia"))) if x[1]]
            if linea:
                o.append('<p class="cta-linea">' + " · ".join(f"<b>{e(a)}:</b> {e(str(b))}" for a, b in linea) + "</p>")
            if ent.get("nota"):
                o.append(f'<p class="nota">{e(ent["nota"])}</p>')
            if p:
                o.append(cuerpo_pieza(p))
            elif ent.get("idea"):
                o.append(rot("Qué se publica") + pegar(ent["idea"].get("desarrollo", "")))
            o.append("</div>")
        return "\n".join(o)

    def tab_correos(self):
        o = ["<h2>Correos del mes</h2>",
             '<p class="intro">A la lista propia. El Máster nunca lleva precio; ACERO puede llevar $225 solo aquí y en pauta.</p>',
             self.avance()]
        for c in self.cal.get("correos", []):
            p = self.gui.get(c.get("id")) or c
            k = clave("correo", c.get("fecha_iso", ""), c.get("nombre", ""))
            o.append(f'<div class="pieza col" data-k="{k}"><div class="pieza-cab cab">{chk(k)}'
                     f'<span class="fecha">{e(c["fecha"])}</span><h3>{e(c.get("nombre") or "")}</h3></div>')
            o.append(cuerpo_pieza(p) if c.get("id") in self.gui else valor({k2: v for k2, v in c.items() if k2 not in ("fecha", "nombre")}))
            o.append("</div>")
        return "\n".join(o)

    def tab_pauta(self):
        pub = self.cal.get("publicidad", {})
        o = ["<h2>Publicidad</h2>", f'<p class="intro">{e(pub.get("nota", ""))}</p>']
        if pub.get("indicaciones"):
            o.append('<div class="indic"><h3>Antes de subir nada</h3>')
            for k, v in pub["indicaciones"]:
                o.append(f"<p><b>{e(k)}.</b> {e(v)}</p>")
            o.append("</div>")
        o.append(self.avance())
        for c in pub.get("campanas", []):
            o.append(f'<h3 class="camp">{e(c["nombre"])}</h3>')
            for a in c["piezas"]:
                p = self.gui.get(a["id"], {})
                k = clave("ad", a["id"])
                o.append(f'<div class="ad col" data-k="{k}"><div class="ad-cab cab">{chk(k)}'
                         f'<span class="tipo">{e(a.get("formato") or "anuncio")}</span><h3>{e(a.get("titulo") or "")}</h3>'
                         f'<span class="precio-ad">{e(a.get("precio", ""))}</span></div>')
                if a.get("creativos_png"):
                    o.append(rot("Creativo listo para subir") + '<div class="creativos">' + "".join(
                        f'<a href="{e(Path(x).relative_to("matriz-viral/entregables").as_posix())}" target="_blank" rel="noopener">'
                        f'<img loading="lazy" alt="Creativo {e(Path(x).stem)}" src="{e(Path(x).relative_to("matriz-viral/entregables").as_posix())}"></a>'
                        for x in a["creativos_png"]) + "</div>")
                o.append(cuerpo_pieza(p))
                o.append("</div>")
        return "\n".join(o)

    def tab_resumen(self):
        c = self.cal
        o = ["<h2>Cómo se usa esto</h2>",
             '<p class="intro">Una pestaña por responsable, con el mismo enlace para todos. '
             'Lo que está en bloque con borde ámbar se copia y se pega tal cual. '
             'Cada ficha tiene una casilla: al marcarla la pieza se cierra, y la marca queda guardada en tu navegador.</p>']
        filas = [(g["nombre"].split(" — ")[0].split(" · ")[0] + " · " + g["nombre"].split(" · ")[1].split(" — ")[0],
                  f'{sum(1 for x in g["calendario"] if x.get("id"))} piezas', g.get("descripcion", "")) for g in c["grupos"]]
        filas.append(("Correos", f'{len(c.get("correos", []))} correos', "A la lista propia, uno por semana."))
        filas.append(("Publicidad", f'{sum(len(x["piezas"]) for x in c.get("publicidad", {}).get("campanas", []))} anuncios',
                      "Primero las 6 decisiones que corrigen septiembre; después los anuncios nuevos."))
        o.append(tabla(["Pestaña", "Cuánto", "Qué es"], filas))
        o.append("<h2>Las reglas que no se rompen</h2><ul class=\"reglas\">" + "".join(f"<li>{e(r)}</li>" for r in c["reglas_del_mes"]) + "</ul>")
        lm = c.get("lead_magnets", {})
        if lm:
            o.append("<h2>Lead magnets del mes</h2>")
            if lm.get("nota"):
                o.append(f'<p class="intro">{e(lm["nota"])}</p>')
            for x in lm.get("nuevo", []):
                o.append(f'<div class="lm-nuevo"><h4>{e(x["nombre"])} <span class="lm-pal">NUEVO · «{e(x["palabra"])}»</span></h4>'
                         + "".join(f"<p><b>{e(k.replace('_', ' '))}:</b> {valor_corto(v)}</p>" for k, v in x.items() if k not in ("nombre", "palabra")) + "</div>")
            if lm.get("respaldo"):
                o.append('<h3 class="camp">De respaldo (ya existen)</h3>' + valor(lm["respaldo"]))
            if lm.get("retirados"):
                o.append('<h3 class="camp">Retirados</h3>' + valor(lm["retirados"]))
            if lm.get("mapa_cta"):
                o.append('<h3 class="camp">Qué pieza pide cada palabra</h3>' + valor(lm["mapa_cta"]))
        if c.get("destacadas"):
            d = c["destacadas"]
            o.append(f"<h2>Destacadas del perfil · las actualiza {e(d.get('responsable', ''))}</h2>")
            o.append(f'<p class="intro">{e(d.get("nota", ""))}</p>')
            o.append(tabla(["Destacada", "Qué va", "Se agrega en octubre", "Qué se quita"],
                           [[x["destacada"], x["que_va"], ", ".join(x["agregar"]), x["quitar"]] for x in d["lista"]]))
        if c.get("checklist_tareas"):
            o.append("<h2>Checklist del mes</h2><ul class=\"e2e\">")
            for t in c["checklist_tareas"]:
                k = clave("tarea", t.get("tarea", ""))
                extra = " · ".join(str(t[x]) for x in ("responsable", "cuando", "desbloquea") if t.get(x))
                o.append(f'<li class="chkline">{chk(k)}<span><b>{e(t.get("tarea", ""))}</b>'
                         + (f'<br><small>{e(extra)}</small>' if extra else "") + "</span></li>")
            o.append("</ul>")
        if c.get("kpis_mensuales"):
            o.append("<h2>De dónde arrancamos</h2>" + valor(c["kpis_mensuales"]))
        return "\n".join(o)

    def tab_quien_compra(self):
        o = ["<h2>Quién compra y quién no</h2>"]
        md = MATRIZ / "COMPRADORES-VS-NO.md"
        if md.exists():
            o.append(markdown_a_html(md.read_text(encoding="utf-8"), saltar_h1=True))
        h = MATRIZ / "historico-2026.json"
        if h.exists():
            hist = json.loads(h.read_text(encoding="utf-8"))
            o.append("<h2>Lo publicado de julio a septiembre</h2>")
            o.append(f'<p class="intro">Métricas reales de Instagram (Meta Graph API), al {e(str(hist.get("metricas_al")))}. '
                     "Ninguna pieza del mes repite un id o un gancho de esta lista (historico-2026.json).</p>")
            o.append(tabla(["Mes", "Piezas", "Vistas (mediana)", "Comentarios (mediana)", "Guardados (mediana)", "Com./1.000"],
                           [[m, r["n"], r["vistas_mediana"], r["comentarios_mediana"], r["guardados_mediana"], r["comentarios_por_mil_mediana"]]
                            for m, r in hist["resumen_por_mes"].items()]))
            o.append('<h3 class="camp">Lo que más conversación trajo</h3>')
            o.append(tabla(["Fecha", "Gancho", "Vistas", "Comentarios", "Guardados"],
                           [[p["fecha"][:10], (p.get("hook") or "")[:90], p["views"], p["comentarios"], p["guardados"]]
                            for p in hist["mejores_por_comentarios"][:8]]))
        return "\n".join(o)

    def pestanas(self):
        t = [("resumen", "Resumen", self.tab_resumen)]
        for i, g in enumerate(self.cal["grupos"]):
            corto = g["nombre"].split(" — ")[0].replace("GRUPO", "G").split(" · ")
            t.append((f"g{i + 1}", f"{corto[0].strip()} · {corto[1].split(' (')[0].strip()}" if len(corto) > 1 else corto[0],
                      (lambda i=i: self.tab_grupo(i))))
        t.append(("correos", "Correos", self.tab_correos))
        t.append(("pauta", "Publicidad", self.tab_pauta))
        t.append(("compra", "Quién compra", self.tab_quien_compra))
        return t

    def artefacto(self):
        css, js = estilos_de_septiembre()
        js = js.replace("dma-matriz-sep-", f"dma-matriz-{self.mes}-")
        extra_css = ".creativos{display:flex;gap:12px;flex-wrap:wrap;margin:6px 0 10px}.creativos img{height:260px;width:auto;max-width:100%;border-radius:6px;border:1px solid var(--line)}.tipo{white-space:normal}.pegar,code,.nota,.cta-linea,td{overflow-wrap:anywhere}.pieza-cab h3{min-width:0}.lm-nuevo p{margin:6px 0 0}.chkline small{color:var(--ink-3)}details.prompt{margin-top:10px}details.prompt summary{cursor:pointer;font-family:var(--display);font-weight:700;font-size:13px;color:var(--amber-deep)}td code{font-size:12px;white-space:pre-wrap}"
        partes = [f"<title>Matriz {self.nombre.capitalize()} DMA</title>",
                  '<link rel="preconnect" href="https://fonts.googleapis.com">',
                  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
                  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;700;800;900&'
                  'family=Nunito:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap">',
                  f"<style>{css}{extra_css}</style>",
                  '<header><div class="wrap">',
                  f'<p class="eyebrow">Design Modeling Academy · {e(self.cal.get("subtitulo", "").split(" · ")[0])}</p>',
                  f"<h1>Matriz de {self.nombre.capitalize()}</h1>",
                  f'<p class="lede">{e(self.cal.get("resumen_cierre", ""))}</p>',
                  "</div></header>", '<nav><div class="wrap" role="tablist">']
        tabs = self.pestanas()
        for k, etq, _ in tabs:
            partes.append(f'<button data-t="{k}" role="tab" aria-selected="false">{e(etq)}</button>')
        partes.append('</div></nav><div class="wrap">')
        for k, _, fn in tabs:
            partes.append(f'<section id="tab-{k}" hidden>{fn()}</section>')
        partes.append(f'<footer>{e(self.cal.get("pie", ""))}<br>Generado con scripts/build_matriz_mes.py --mes {self.mes} el {date.today().isoformat()}.</footer></div>')
        partes.append(f"<script>{js}</script>")
        salida = ENTREGABLES / f"matriz-{self.nombre}-artefacto.html"
        salida.write_text("\n".join(partes), encoding="utf-8")
        return salida, len(tabs)

    def completo(self):
        def con(x):
            d = dict(x)
            if x.get("id") in self.gui:
                d["contenido"] = self.gui[x["id"]]
            return d
        c = self.cal
        datos = {
            "_meta": {
                "titulo": f"Matriz de contenido — Design Modeling Academy — {self.nombre} {self.mes[:4]}",
                "periodo": c.get("subtitulo", "").split(" · ")[0],
                "generado": date.today().isoformat(),
                "como_se_regenera": f"python3 matriz-viral/matriz/calendario-{self.nombre}.py && python3 scripts/build_matriz_mes.py --mes {self.mes}",
                "origen": f"calendario-{self.nombre}.json (orden) + guiones-completos.json (contenido de cada pieza)",
                "fuente_de_datos": "Métricas de Instagram por Meta Graph API (matriz.json, Action «Métricas semanales») y Apify para referentes; histórico en historico-2026.json; compradores en COMPRADORES-VS-NO.md.",
            },
            "reglas_del_mes": c["reglas_del_mes"],
            "checklist_tareas": c.get("checklist_tareas", []),
            "grupos": [{**{k: v for k, v in g.items() if k != "calendario"}, "calendario": [con(x) for x in g["calendario"]]}
                       for g in c["grupos"]],
            "publicidad": {**c.get("publicidad", {}),
                           "campanas": [{**cp, "piezas": [con(a) for a in cp["piezas"]]} for cp in c.get("publicidad", {}).get("campanas", [])]},
            "lead_magnets": c.get("lead_magnets", {}),
            "destacadas": c.get("destacadas", {}),
            "correos": [con(x) for x in c.get("correos", [])],
            "banco_reserva": [con({"id": i}) for i in c.get("banco_reserva", [])],
            "kpis_mensuales": c.get("kpis_mensuales", {}),
            "pendientes": c.get("pendientes", []),
            "artefactos": c.get("artefactos", {}),
        }
        salida = ENTREGABLES / f"matriz-{self.nombre}-{self.mes[:4]}-COMPLETA.json"
        salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        return salida, datos


def markdown_a_html(md, saltar_h1=False):
    """Markdown sencillo (títulos, tablas, listas, citas, negritas) a HTML."""
    def inline(t):
        t = e(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    o, lineas, i = [], md.splitlines(), 0
    while i < len(lineas):
        ln = lineas[i]
        if ln.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not re.match(r"^\|[\s\-|:]+\|$", lineas[i]):
                    filas.append([x.strip() for x in lineas[i].strip("|").split("|")])
                i += 1
            o.append('<div class="tabla-scroll"><table><thead><tr>' + "".join(f"<th>{inline(x)}</th>" for x in filas[0]) + "</tr></thead><tbody>"
                     + "".join("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in f) + "</tr>" for f in filas[1:]) + "</tbody></table></div>")
            continue
        m = re.match(r"^(#{1,3}) (.*)", ln)
        if m:
            if not (saltar_h1 and len(m.group(1)) == 1):
                o.append(f'<h{len(m.group(1)) + 1} class="camp">{inline(m.group(2))}</h{len(m.group(1)) + 1}>')
        elif re.match(r"^(\d+\.|-) ", ln):
            # Lista con subpuntos: las líneas sangradas («   - …» o un párrafo
            # sangrado) van dentro del punto anterior, no como puntos nuevos.
            tag = "ol" if ln[0].isdigit() else "ul"
            items = []
            while i < len(lineas):
                cur = lineas[i]
                if re.match(r"^(\d+\.|-) ", cur):
                    items.append({"txt": re.sub(r"^(\d+\.|-) ", "", cur), "sub": [], "par": []})
                elif items and re.match(r"^\s+(\d+\.|-) ", cur):
                    items[-1]["sub"].append(re.sub(r"^\s+(\d+\.|-) ", "", cur))
                elif items and cur.startswith("   ") and cur.strip():
                    items[-1]["par"].append(cur.strip())
                elif not cur.strip() and i + 1 < len(lineas) and (lineas[i + 1].startswith("   ") or re.match(r"^(\d+\.|-) ", lineas[i + 1])):
                    pass
                else:
                    break
                i += 1
            html_items = []
            for it in items:
                sub = ('<ul class="sub">' + "".join(f"<li>{inline(x)}</li>" for x in it["sub"]) + "</ul>") if it["sub"] else ""
                par = "".join(f'<p class="sub-p">{inline(x)}</p>' for x in it["par"])
                html_items.append(f"<li>{inline(it['txt'])}{sub}{par}</li>")
            o.append(f'<{tag} class="reglas">' + "".join(html_items) + f"</{tag}>")
            continue
        elif ln.startswith(">"):
            txt = []
            while i < len(lineas) and lineas[i].startswith(">"):
                txt.append(lineas[i].lstrip("> ").strip())
                i += 1
            o.append(f'<p class="nota">{"<br>".join(inline(x) for x in txt if x)}</p>')
            continue
        elif ln.strip():
            o.append(f'<p class="intro">{inline(ln)}</p>')
        i += 1
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", required=True, help="AAAA-MM")
    a = ap.parse_args()
    m = Mes(a.mes)
    art, n = m.artefacto()
    js, datos = m.completo()
    piezas = sum(len(g["calendario"]) for g in datos["grupos"])
    ads = sum(len(c["piezas"]) for c in datos["publicidad"].get("campanas", []))
    sin = [x["id"] for g in datos["grupos"] for x in g["calendario"] if x.get("id") and "contenido" not in x]
    print(f"OK → {art.relative_to(RAIZ)} ({art.stat().st_size / 1024:.0f} KB, {n} pestañas)")
    print(f"OK → {js.relative_to(RAIZ)} ({js.stat().st_size / 1024:.0f} KB) · {piezas} piezas en {len(datos['grupos'])} grupos · "
          f"{ads} anuncios · {len(datos['correos'])} correos")
    if sin:
        print("::warning::Piezas del calendario sin contenido en guiones-completos.json:", ", ".join(sin))


if __name__ == "__main__":
    main()
