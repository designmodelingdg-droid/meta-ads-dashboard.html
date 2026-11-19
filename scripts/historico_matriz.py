#!/usr/bin/env python3
"""Histórico de la matriz: lo planificado y lo publicado, con su resultado real.

Junta en un solo archivo lo que antes estaba repartido por meses:

  · lo PUBLICADO, con las métricas de Instagram que trae matriz.json
    (Meta Graph API, refrescadas por la Action «Métricas semanales»);
  · lo PLANIFICADO en cada matriz: julio (carpetas guiones/2026-07-*),
    agosto (calendario-agosto.json) y septiembre (calendario-septiembre.json);
  · la lista de piezas y ganchos YA USADOS, que la matriz de cada mes nuevo
    tiene que respetar (ninguna pieza se repite).

    python3 scripts/historico_matriz.py
      → matriz-viral/matriz/historico-2026.json
      → matriz-viral/matriz/HISTORICO-JUL-SEP.md

No inventa nada: lo que matriz.json no trae sale como null («s/d» en el .md).
"""
import json
import pathlib
import re
import statistics as st
import unicodedata

M = pathlib.Path("matriz-viral/matriz")
G = pathlib.Path("matriz-viral/guiones")
MESES = {"07": "julio", "08": "agosto", "09": "septiembre"}


def norm(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


def mediana(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(st.median(xs), 1) if xs else None


def por_mil(p):
    v, c = p.get("views"), p.get("comentarios")
    return round(c * 1000 / v, 2) if v and c is not None else None


def resumen(grupo):
    return {
        "n": len(grupo),
        "vistas_mediana": mediana([p.get("views") for p in grupo]),
        "comentarios_mediana": mediana([p.get("comentarios") for p in grupo]),
        "guardados_mediana": mediana([p.get("guardados") for p in grupo]),
        "comentarios_por_mil_mediana": mediana([por_mil(p) for p in grupo]),
    }


def agrupar(pubs, clave):
    out = {}
    for p in pubs:
        out.setdefault(p.get(clave) or "sin clasificar", []).append(p)
    return {k: resumen(v) for k, v in sorted(out.items(), key=lambda kv: -len(kv[1]))}


def main():
    matriz = json.load(open(M / "matriz.json", encoding="utf-8"))
    guiones = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}

    # ---------- publicado (jul-sep) ----------
    pubs = []
    for r in matriz["reels"]:
        f = r.get("fecha") or ""
        if f[:7] not in ("2026-07", "2026-08", "2026-09"):
            continue
        pubs.append({
            "id": r.get("id"), "fecha": f, "mes": MESES[f[5:7]], "tipo": r.get("tipo"),
            "eje": r.get("eje"), "hook": r.get("hook") or r.get("tema"), "url": r.get("url"),
            "views": r.get("views"), "alcance": r.get("alcance"), "likes": r.get("likes"),
            "comentarios": r.get("comentarios"), "guardados": r.get("guardados"),
            "shares": r.get("shares"), "nuevos_seguidores": r.get("nuevos_seguidores"),
            "comentarios_por_mil": None, "lectura": r.get("nota"),
        })
        pubs[-1]["comentarios_por_mil"] = por_mil(pubs[-1])

    # ---------- planificado ----------
    plan = []
    for d in sorted(G.glob("2026-07-*")):
        slug = d.name.split("_", 1)[-1]
        plan.append({"mes": "julio", "id": f"jul-{slug}", "fecha": d.name[:10], "origen": f"guiones/{d.name}",
                     "titulo": slug.replace("-", " "), "formato": None})
    ago = json.load(open(M / "calendario-agosto.json", encoding="utf-8"))
    for p in ago.get("piezas", []):
        g = guiones.get(p["id"], {})
        plan.append({"mes": "agosto", "id": p["id"], "fecha": p.get("fecha"), "origen": "calendario-agosto.json",
                     "titulo": g.get("titulo"), "hook": g.get("hook"), "formato": p.get("formato_publicacion")})
    sep = json.load(open(M / "calendario-septiembre.json", encoding="utf-8"))
    for gr in sep.get("grupos", []):
        for e in gr.get("calendario", []):
            if not e.get("id"):
                continue
            g = guiones.get(e["id"], {})
            plan.append({"mes": "septiembre", "grupo": gr.get("nombre", "")[:40], "id": e["id"], "fecha": e.get("fecha"),
                         "origen": "calendario-septiembre.json", "titulo": g.get("titulo"), "hook": g.get("hook"),
                         "formato": e.get("formato_publicacion")})

    usados_ids = sorted({p["id"] for p in plan if p.get("id")})
    usados_hooks = sorted({p["hook"] for p in pubs + plan if p.get("hook")})

    orden = [p for p in pubs if p["comentarios"] is not None]
    mejores = sorted(orden, key=lambda p: -(p["comentarios"] or 0))[:12]
    peores = sorted([p for p in orden if (p["views"] or 0) >= 500],
                    key=lambda p: ((p["comentarios"] or 0), (p["guardados"] or 0)))[:12]

    salida = {
        "generado_con": "scripts/historico_matriz.py",
        "fuente_metricas": matriz.get("actualizado_fuente") or "matriz.json",
        "metricas_al": matriz.get("actualizado"),
        "regla": "Ninguna pieza de un mes nuevo repite un id de usados_ids ni un gancho de usados_hooks.",
        "resumen_por_mes": {m: resumen([p for p in pubs if p["mes"] == m]) for m in MESES.values()},
        "por_eje": agrupar(pubs, "eje"),
        "por_tipo": agrupar(pubs, "tipo"),
        "mejores_por_comentarios": mejores,
        "peores_con_alcance": peores,
        "publicado": pubs,
        "planificado": plan,
        "usados_ids": usados_ids,
        "usados_hooks": usados_hooks,
    }
    json.dump(salida, open(M / "historico-2026.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def s(x):
        if x is None:
            return "s/d"
        if isinstance(x, float) and x.is_integer():
            x = int(x)
        if isinstance(x, int):
            return f"{x:,}".replace(",", ".")
        if isinstance(x, float):
            return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(x)
    L = ["# Histórico julio–septiembre 2026", "",
         f"Generado por `scripts/historico_matriz.py` desde `matriz.json` (métricas de Instagram, {salida['fuente_metricas']}, al {s(salida['metricas_al'])}) y las matrices de cada mes. No se edita a mano.", "",
         "## Resumen por mes (publicado)", "", "| Mes | Piezas | Vistas (mediana) | Comentarios (mediana) | Guardados (mediana) | Comentarios por 1.000 vistas |", "|---|---|---|---|---|---|"]
    for m, r in salida["resumen_por_mes"].items():
        L.append(f"| {m} | {r['n']} | {s(r['vistas_mediana'])} | {s(r['comentarios_mediana'])} | {s(r['guardados_mediana'])} | {s(r['comentarios_por_mil_mediana'])} |")
    for titulo, clave in (("Por eje", "por_eje"), ("Por formato", "por_tipo")):
        L += ["", f"## {titulo}", "", "| | Piezas | Vistas | Comentarios | Guardados | Com./1.000 |", "|---|---|---|---|---|---|"]
        for k, r in salida[clave].items():
            L.append(f"| {k} | {r['n']} | {s(r['vistas_mediana'])} | {s(r['comentarios_mediana'])} | {s(r['guardados_mediana'])} | {s(r['comentarios_por_mil_mediana'])} |")
    L += ["", "## Lo que más conversación trajo", "", "| Fecha | Id | Eje | Gancho | Vistas | Comentarios | Guardados |", "|---|---|---|---|---|---|---|"]
    for p in mejores:
        L.append(f"| {p['fecha']} | {p['id']} | {s(p['eje'])} | {(p['hook'] or '')[:70]} | {s(p['views'])} | {s(p['comentarios'])} | {s(p['guardados'])} |")
    L += ["", "## Lo que tuvo alcance y no trajo conversación (≥ 500 vistas)", "", "| Fecha | Id | Eje | Gancho | Vistas | Comentarios | Guardados |", "|---|---|---|---|---|---|---|"]
    for p in peores:
        L.append(f"| {p['fecha']} | {p['id']} | {s(p['eje'])} | {(p['hook'] or '')[:70]} | {s(p['views'])} | {s(p['comentarios'])} | {s(p['guardados'])} |")
    L += ["", "## Planificado por mes", ""]
    for m in MESES.values():
        L.append(f"- **{m}**: {sum(1 for p in plan if p['mes'] == m)} piezas en la matriz.")
    L += ["", f"Ids ya usados: {len(usados_ids)} · ganchos ya usados: {len(usados_hooks)}. Están en `historico-2026.json` y la comprobación de la matriz nueva los lee.", ""]
    (M / "HISTORICO-JUL-SEP.md").write_text("\n".join(L), encoding="utf-8")
    print("ok ·", len(pubs), "publicadas ·", len(plan), "planificadas")


def ya_usado(hook, historico, umbral=0.8):
    """True si un gancho nuevo se parece demasiado a uno ya usado (palabras en común)."""
    a = set(norm(hook))
    if not a:
        return False
    for h in historico["usados_hooks"]:
        b = set(norm(h))
        if b and len(a & b) / min(len(a), len(b)) >= umbral:
            return True
    return False


if __name__ == "__main__":
    main()
