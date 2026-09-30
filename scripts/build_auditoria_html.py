#!/usr/bin/env python3
"""Página de la auditoría de un mes, para compartir con el equipo.

    python3 scripts/auditoria_mes.py --mes 2026-09        # primero, los datos
    python3 scripts/build_auditoria_html.py --mes 2026-09
      → matriz-viral/entregables/auditoria-<mes>.html

Lee `auditorias/<mes>-auditoria-mes.json` (los números) y
`auditorias/<mes>-hallazgos.md` (la lectura, escrita a mano). Usa el mismo
estilo que el artefacto de la matriz.
"""
import argparse
import html
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / "scripts"))
from build_matriz_mes import estilos_de_septiembre, markdown_a_html, MESES  # noqa: E402

e = html.escape


def n(x, dec=0):
    if x is None:
        return "s/d"
    if isinstance(x, float) and not x.is_integer():
        return f"{x:,.{dec or 1}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{int(x):,}".replace(",", ".")


def tabla(cab, filas, clase=""):
    return ('<div class="tabla-scroll"><table class="' + clase + '"><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in cab)
            + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
            + "</tbody></table></div>")


CHIP = {"alta": "ok", "media": "mid", "baja": "bad", "s/d": "mid"}


def chip(txt, tono):
    return f'<span class="chip {tono}">{e(txt)}</span>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", required=True)
    mes = ap.parse_args().mes
    nombre = MESES[mes[5:7]]
    a = json.loads((R / "matriz-viral" / "auditorias" / f"{mes}-auditoria-mes.json").read_text(encoding="utf-8"))
    md = (R / "matriz-viral" / "auditorias" / f"{mes}-hallazgos.md").read_text(encoding="utf-8")
    css, _ = estilos_de_septiembre()
    css += """
.chip{display:inline-block;font:700 11.5px/1.45 var(--display);letter-spacing:.02em;padding:2px 9px;border-radius:10px;white-space:normal}
ul.sub{margin:6px 0 4px;padding-left:20px;list-style:disc}ul.sub li{margin-bottom:3px;font-size:14.5px}p.sub-p{margin:8px 0 2px;font-size:14.5px}
.chip.ok{background:var(--ok-bg);color:var(--ok)}.chip.bad{background:var(--stop-bg);color:var(--stop)}.chip.mid{background:var(--wait-bg);color:var(--amber-deep)}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.hallazgos h2.camp,.hallazgos h3.camp{color:var(--ink);font-size:21px;margin-top:30px}
.hallazgos ol.reglas li,.hallazgos ul.reglas li{color:var(--ink);font-size:15px}
section{padding-top:8px}.fuente{font-size:13px;color:var(--ink-3)}
td a{color:var(--amber-deep)}
"""
    o = [f"<title>Auditoría {nombre.capitalize()} DMA</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;700;800;900&family=Nunito:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap">',
         f"<style>{css}</style>",
         '<header><div class="wrap">',
         f'<p class="eyebrow">Design Modeling Academy · auditoría de {nombre} {mes[:4]}</p>',
         f"<h1>¿Funcionó {nombre}?</h1>",
         '<p class="lede">Cada publicación con su palabra, los DM que salieron, los clics reales y los leads en GHL; los recursos del mes, las historias, la pauta y lo cobrado.</p>',
         '</div></header><div class="wrap">']

    o.append('<section class="hallazgos">' + markdown_a_html(md, saltar_h1=True) + "</section>")

    # publicaciones
    filas = []
    for p in a["publicaciones"]:
        filas.append([e(p["fecha"][5:]), f'<a href="{e(p["url"] or "#")}" target="_blank" rel="noopener">{e(p["id"])}</a>', e(p["tipo"] or ""),
                      e(p["gancho"][:80]), f'<span class="num">{n(p["vistas"])}</span>', n(p["comentarios"]), n(p["guardados"]),
                      n(p["seguidores"]), n(p["comentarios_por_mil"], 1), chip(p["conversacion"], CHIP.get(p["conversacion"], "mid")),
                      n(p["dm_enviados"]), n(p["dm_fallidos"]), n(p["clics_limpios"]), e(p["lectura"])])
    o.append(f'<section><h2>Cada publicación del mes</h2><p class="intro">Conversación = comentarios por 1.000 vistas contra la mediana del mes '
             f'({n(a["mediana_comentarios_por_mil"], 2)}): alta ≥ 1,5 veces la mediana, baja &lt; 0,5 veces. DM y clics salen de la campaña de OpenReply atada a ese post; '
             f'si la palabra la contesta GHL, sale en la tabla de palabras.</p>'
             + tabla(["Fecha", "Post", "Tipo", "Gancho", "Vistas", "Com.", "Guard.", "Seg.", "Com./1.000", "Conversación", "DM", "DM fallidos", "Clics", "Lectura"], filas)
             + "</section>")

    # plan contra publicado
    filas = [[e(p["fecha"][5:]), e(p["id"] or "—"), e((p["titulo"] or "")[:70]), e(p["formato"] or ""), e(", ".join(p["publicado_ese_dia"]) or "—"), e(p["estado"])]
             for p in a.get("plan_contra_publicado", [])]
    o.append('<section><h2>Lo planificado contra lo publicado</h2><p class="intro">Por fecha. Que haya publicación ese día no garantiza que sea la pieza del plan: '
             'la columna «Tema» de arriba lo confirma.</p>' + tabla(["Fecha", "Pieza del plan", "Título", "Formato", "Publicado ese día", "Estado"], filas)
             + f'<p class="fuente">Publicado fuera del plan: {e(", ".join(a.get("publicado_fuera_de_plan", [])) or "nada")}.</p></section>')

    # palabras
    filas = []
    for w in a["palabras"]:
        tono = "ok" if w["veredicto"] == "viva" else ("bad" if "falla" in w["veredicto"] or "no disparó" in w["veredicto"] else "mid")
        filas.append([f'<b>{e(w["palabra"])}</b>', e(" + ".join(w["donde"])), e(w.get("recurso") or ""), n(w["dm_enviados"]), n(w["dm_fallidos"]),
                      n(w["clics_limpios"]), n(w.get("ghl_bot")), n(w.get("ghl_lead")), n(w.get("ghl_acceso")), chip(w["veredicto"], tono)])
    o.append('<section><h2>Cada palabra y su embudo</h2><p class="intro">OpenReply cuenta DM y clics limpios (sin bots desde el 15-sep). '
             'GHL cuenta contactos con la etiqueta del bot, del lead y del acceso; son totales acumulados, no solo del mes.</p>'
             + tabla(["Palabra", "Dónde vive", "Recurso", "DM", "DM fallidos", "Clics", "GHL bot", "GHL lead", "GHL acceso", "Veredicto"], filas) + "</section>")

    # historias
    filas = [[e(h["dia"][5:]), n(h["frames"]), n(h["alcance_primero"]), n(h["alcance_ultimo"]),
              f'{round((h["retencion"] or 0) * 100)} %' if h["retencion"] is not None else "s/d", n(h["respuestas"]), n(h["visitas_perfil"]), n(h["salidas"])]
             for h in a["historias"]]
    o.append('<section><h2>Historias</h2><p class="intro">Solo los días que se alcanzaron a leer: la API las borra a las 24 h, y la lectura automática '
             'empezó el 22-sep y estuvo parada del 27 al 30-sep.</p>'
             + tabla(["Día", "Frames", "Alcance 1.º", "Alcance último", "Retención", "Respuestas", "Visitas al perfil", "Salidas"], filas) + "</section>")

    # pauta
    if a.get("pauta"):
        filas = []
        for c in a["pauta"]["campanas"]:
            ac = {x["action_type"]: float(x["value"]) for x in c.get("actions", [])}
            lead = ac.get("lead", 0)
            msg = ac.get("onsite_conversion.messaging_conversation_started_7d", 0)
            gasto = float(c["spend"])
            res = lead + msg if "ACERO - FORM" not in c["campaign_name"] else lead
            filas.append([e(c["campaign_name"]), f'${n(gasto)}', n(lead), n(msg), f'${n(round(gasto / res, 2), 2)}' if res else "—",
                          n(float(c.get("frequency") or 0), 2)])
        v = a["pauta"]["ventana"]
        o.append(f'<section><h2>Pauta</h2><p class="intro">Meta Ads del {e(v["desde"])} al {e(v["hasta"])}: ${n(a["pauta"]["gasto_total"])} en total. '
                 'Costo por resultado según Meta; el diagnóstico con GHL es el de Dayana del 30-sep (en la matriz de octubre).</p>'
                 + tabla(["Campaña", "Gasto", "Leads", "Conversaciones", "Costo por resultado", "Frecuencia"], filas) + "</section>")
    ing = a.get("ingresos") or {}
    if ing.get("total_neto"):
        f = ing.get("fuentes", {})
        o.append(f'<section><h2>Lo cobrado</h2><p class="intro">Del {e(ing["ventana"]["desde"])} al {e(ing["ventana"]["hasta"])}: '
                 f'<b>${n(ing["total_neto"], 2)}</b> netos (Stripe ${n(f.get("stripe", {}).get("neto"), 2)} en {n(f.get("stripe", {}).get("cobros"))} cobros · '
                 f'PayPal ${n(f.get("paypal", {}).get("neto"), 2)} en {n(f.get("paypal", {}).get("cobros"))}). Incluye cuotas de contratos vigentes: '
                 'recurrente no es captación.</p></section>')
    d = a["datos_al"]
    o.append(f'<footer>Datos al {e(d.get("matriz") or "")} · OpenReply {e(d.get("openreply") or "")} · embudo {e(d.get("embudo") or "")}. '
             f'Generado con scripts/auditoria_mes.py y scripts/build_auditoria_html.py --mes {e(mes)}. Sin datos personales.</footer></div>')
    out = R / "matriz-viral" / "entregables" / f"auditoria-{nombre}-{mes[:4]}.html"
    out.write_text("\n".join(o), encoding="utf-8")
    print(f"ok → {out.relative_to(R)} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
