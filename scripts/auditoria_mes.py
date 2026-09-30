#!/usr/bin/env python3
"""Auditoría de un mes: qué se publicó, qué pidió, quién respondió y qué pasó después.

    python3 scripts/auditoria_mes.py --mes 2026-09
      → matriz-viral/auditorias/AAAA-MM-auditoria-mes.json
      → matriz-viral/auditorias/AAAA-MM-auditoria-mes.md

Cruza, sin inventar nada, las fuentes que ya baja el repositorio:

  matriz/matriz.json                   cada publicación con vistas, comentarios,
                                       guardados y seguidores (Meta Graph API)
  fuentes/openreply/campanas.json      por campaña de palabra: post al que está
                                       atada, DM enviados, fallidos y clics limpios
  fuentes/ghl/embudo-leadmagnets.json  por recurso: bot → lead → acceso en GHL
  fuentes/historias/historias.json     cada frame de historia con alcance,
                                       respuestas y salidas
  fuentes/ads-insights/, ingresos/     pauta y dinero cobrado

Lo que la fuente no trae sale como null («s/d» en el .md). No lee ningún dato
personal: todo son cuentas.

Cómo se leen los veredictos (reglas fijas, a la vista en el .md):
  · conversación: comentarios por 1.000 vistas contra la mediana del mes;
  · palabra: si la publicación tenía campaña de OpenReply, cuántos DM salieron
    y cuántos fallaron; si una campaña falla más de lo que envía, es un fallo
    de montaje, no de contenido.
"""
import argparse
import json
import pathlib
import statistics as st
from collections import defaultdict

R = pathlib.Path(__file__).resolve().parent.parent
MV = R / "matriz-viral"
F = MV / "fuentes"


def cargar(p, defecto=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return defecto


def por_mil(c, v):
    return round(c * 1000 / v, 2) if v and c is not None else None


def mediana(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(st.median(xs), 2) if xs else None


def codigo(url):
    partes = [x for x in (url or "").split("/") if x]
    return partes[-1] if partes else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", required=True)
    mes = ap.parse_args().mes

    matriz = cargar(MV / "matriz" / "matriz.json", {})
    orp = cargar(F / "openreply" / "campanas.json", {})
    emb = cargar(F / "ghl" / "embudo-leadmagnets.json", {})
    hist = cargar(F / "historias" / "historias.json", {})
    ads = cargar(F / "ads-insights" / "por-campana.json")
    ads_res = cargar(F / "ads-insights" / "resumen.json", {})
    ing = cargar(F / "ingresos" / "resumen.json", {})

    # ── campañas de OpenReply indexadas por el código del post ──
    camp_por_post = defaultdict(list)
    for c in orp.get("campanas", []):
        camp_por_post[codigo(c.get("post_url"))].append(c)

    # ── publicaciones del mes ──
    pubs = [r for r in matriz.get("reels", []) if (r.get("fecha") or "").startswith(mes)]
    med = mediana([por_mil(r.get("comentarios"), r.get("views")) for r in pubs])
    filas = []
    for r in sorted(pubs, key=lambda x: x["fecha"]):
        cps = camp_por_post.get(r.get("shortCode"), [])
        env = sum(c.get("enviados") or 0 for c in cps)
        fal = sum(c.get("fallidos") or 0 for c in cps)
        cli = sum(c.get("clics_limpios") or 0 for c in cps)
        cpm = por_mil(r.get("comentarios"), r.get("views"))
        if cpm is None:
            conv = "s/d"
        elif med and cpm >= med * 1.5:
            conv = "alta"
        elif med and cpm < med * 0.5:
            conv = "baja"
        else:
            conv = "media"
        lectura = []
        if cps:
            lectura.append(f"palabra {'/'.join(sorted({p for c in cps for p in c.get('palabras', [])}))}: {env} DM enviados, {cli} clics limpios")
            if fal > env:
                lectura.append(f"⚠ fallaron {fal} DM, más de los que salieron: montaje, no contenido")
            elif fal:
                lectura.append(f"{fal} DM fallidos")
        else:
            lectura.append("sin campaña de OpenReply atada a este post (la palabra, si la pedía, la contesta GHL o nadie)")
        filas.append({
            "fecha": r["fecha"], "id": r.get("id"), "tipo": r.get("tipo"), "eje": r.get("eje"),
            "gancho": (r.get("hook") or r.get("tema") or "")[:110], "url": r.get("url"),
            "vistas": r.get("views"), "alcance": r.get("alcance"), "comentarios": r.get("comentarios"),
            "guardados": r.get("guardados"), "compartidos": r.get("shares"), "seguidores": r.get("nuevos_seguidores"),
            "comentarios_por_mil": cpm, "conversacion": conv,
            "campanas_openreply": [c.get("nombre") for c in cps], "dm_enviados": env if cps else None,
            "dm_fallidos": fal if cps else None, "clics_limpios": cli if cps else None,
            "lectura": " · ".join(lectura),
        })

    # ── palabras: OpenReply + GHL ──
    palabras = {}
    for c in orp.get("campanas", []):
        for p in c.get("palabras", []):
            d = palabras.setdefault(p, {"palabra": p, "donde": set(), "campanas": [], "dm_enviados": 0, "dm_fallidos": 0, "clics_limpios": 0})
            d["donde"].add("OpenReply")
            d["campanas"].append(f'{c.get("nombre")} ({"activa" if c.get("activa") else "PAUSADA"})')
            d["dm_enviados"] += c.get("enviados") or 0
            d["dm_fallidos"] += c.get("fallidos") or 0
            d["clics_limpios"] += c.get("clics_limpios") or 0
    for p, w in (orp.get("workflows_ghl", {}).get("por_palabra") or {}).items():
        d = palabras.setdefault(p, {"palabra": p, "donde": set(), "campanas": [], "dm_enviados": 0, "dm_fallidos": 0, "clics_limpios": 0})
        if w.get("publicados"):
            d["donde"].add("GHL")
        if w.get("en_borrador"):
            d["campanas"].append("GHL en borrador: " + ", ".join(x["nombre"] for x in w["en_borrador"]))
    for p, e in (emb.get("embudos") or {}).items():
        d = palabras.setdefault(p, {"palabra": p, "donde": set(), "campanas": [], "dm_enviados": 0, "dm_fallidos": 0, "clics_limpios": 0})
        et = e.get("etapas", {})
        d["recurso"] = e.get("recurso")
        d["ghl_bot"] = (et.get("bot") or {}).get("total")
        d["ghl_lead"] = (et.get("lead") or {}).get("total")
        d["ghl_acceso"] = (et.get("acceso") or {}).get("total")
        d["ghl_bot_desde"] = (et.get("bot") or {}).get("tocados_desde")
    for d in palabras.values():
        d["donde"] = sorted(d["donde"])
        ok = d["dm_enviados"] + (d.get("ghl_bot") or 0)
        if d["dm_fallidos"] > d["dm_enviados"] and d["dm_fallidos"] >= 3:
            d["veredicto"] = "falla de montaje: falla más de lo que envía"
        elif ok == 0:
            d["veredicto"] = "no disparó en el mes"
        elif (d.get("ghl_lead") or 0) and d.get("ghl_acceso") == 0:
            d["veredicto"] = "capta pero nadie llega al acceso (revisar la etiqueta de acceso)"
        else:
            d["veredicto"] = "viva"

    # ── historias por día ──
    dias = defaultdict(list)
    for h in hist.get("historias", []):
        if (h.get("publicada") or "").startswith(mes):
            dias[h["publicada"][:10]].append(h)
    historias = []
    for d, hs in sorted(dias.items()):
        hs.sort(key=lambda x: x["publicada"])
        a0, a1 = hs[0].get("reach") or 0, hs[-1].get("reach") or 0
        historias.append({"dia": d, "frames": len(hs), "alcance_primero": a0, "alcance_ultimo": a1,
                          "retencion": round(a1 / a0, 2) if a0 else None,
                          "respuestas": sum(h.get("replies") or 0 for h in hs),
                          "visitas_perfil": sum(h.get("profile_visits") or 0 for h in hs),
                          "salidas": sum((h.get("navegacion") or {}).get("tap_exit", 0) for h in hs)})

    # ── pauta y dinero (lo que haya) ──
    pauta = None
    if isinstance(ads, dict):
        filas_ads = ads.get("filas") or ads.get("campanas") or []
    else:
        filas_ads = ads or []
    if filas_ads:
        pauta = {"ventana": ads_res.get("ventana"), "gasto_total": (ads_res.get("cortes") or {}).get("por-campana", {}).get("gasto"),
                 "campanas": filas_ads}

    salida = {
        "mes": mes, "generado_con": "scripts/auditoria_mes.py",
        "datos_al": {"matriz": matriz.get("actualizado"), "openreply": orp.get("generado"), "embudo": emb.get("generado"),
                     "historias": hist.get("generado"), "pauta": ads_res.get("generado"), "ingresos": ing.get("generado")},
        "reglas": {"conversacion": "comentarios por 1.000 vistas: alta ≥ 1,5 × mediana del mes; baja < 0,5 × mediana",
                   "palabra": "una campaña que falla más DM de los que envía es un fallo de montaje"},
        "mediana_comentarios_por_mil": med,
        "publicaciones": filas,
        "palabras": sorted(palabras.values(), key=lambda d: -(d["dm_enviados"] + (d.get("ghl_bot") or 0))),
        "motivos_de_fallo": orp.get("motivos_de_fallo", []),
        "historias": historias,
        "pauta": pauta,
        "ingresos": ing,
        "seguidores": orp.get("seguidores", []),
    }
    out = MV / "auditorias" / f"{mes}-auditoria-mes.json"
    out.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok → {out.relative_to(R)} · {len(filas)} publicaciones · {len(palabras)} palabras · {len(historias)} días de historias")


if __name__ == "__main__":
    main()
