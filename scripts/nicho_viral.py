#!/usr/bin/env python3
"""Que esta funcionando en el nicho de Revit + IA, fuera de nuestra cuenta.

Para que existe: para septiembre Dayana quiere apoyarse en «Revit conectado a
la IA». Antes de escribir dieciocho piezas sobre eso conviene mirar que forma
tiene lo que ya funciona ahi fuera — no para copiarlo, para saber contra que se
compite y que angulos estan gastados.

Que NO hace: no mide nuestro rendimiento. Eso vive en matriz.json y se cruza
aparte. Aqui solo se mira el nicho.

Disciplina de gasto, que es dinero de Dayana:
  - `maxTotalChargeUsd` es el tope DURO. Apify corta ahi aunque falten
    resultados. Es la unica proteccion que no depende de que yo acierte el
    precio por resultado, que Apify no publica.
  - `resultsLimit` acota ademas por cantidad.
  - Solo cuentas y contenido PUBLICO.

    APIFY_TOKEN=xxx python3 scripts/nicho_viral.py [--limite 40] [--tope 1.0]
"""
import argparse, json, os, sys, urllib.request, urllib.error
from datetime import date

ACTOR  = "apify~instagram-scraper"
SALIDA = "matriz-viral/fuentes/nicho-revit-ia.json"

# Las etiquetas del nicho concreto, no «arquitectura» en general: lo que se
# busca es el cruce Revit/BIM con IA, que es donde Dayana ve traccion.
ETIQUETAS = [
    "revit", "revittips", "bimmanager", "autodeskrevit",
    "iaparaarquitectos", "inteligenciaartificialarquitectura",
    "bimconia", "dynamorevit",
]

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()


def correr(limite, tope):
    payload = json.dumps({
        "directUrls": [f"https://www.instagram.com/explore/tags/{t}/" for t in ETIQUETAS],
        "resultsType": "posts",
        "resultsLimit": limite,
        "addParentData": False,
        "maxTotalChargeUsd": tope,      # ← el tope duro
    }).encode()
    url = (f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"
           f"?token={TOKEN}&maxTotalChargeUsd={tope}")
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=280) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Apify HTTP {e.code}: {e.read().decode()[:300]}")
        print("Sin datos. No se escribe nada — mejor vacio que inventado.")
        sys.exit(0)
    except Exception as e:
        print(f"Fallo de red con Apify: {e}. No se escribe nada.")
        sys.exit(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=40,
                    help="posts por etiqueta (por defecto 40)")
    ap.add_argument("--tope", type=float, default=1.0,
                    help="tope DURO de gasto en USD (por defecto 1.0)")
    op = ap.parse_args()

    if not TOKEN:
        print("ERROR: falta APIFY_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)

    print(f"  etiquetas : {len(ETIQUETAS)} · {', '.join(ETIQUETAS)}")
    print(f"  limite    : {op.limite} posts por etiqueta")
    print(f"  TOPE DURO : ${op.tope:.2f} — Apify corta ahi aunque falten datos")
    print()

    datos = correr(op.limite, op.tope)
    filas = [x for x in datos if isinstance(x, dict) and x.get("shortCode")]
    if not filas:
        print(f"No devolvio posts: {str(datos)[:200]}")
        sys.exit(0)

    def n(v): return v if isinstance(v, (int, float)) else 0

    piezas = []
    for p in filas:
        v = n(p.get("videoPlayCount"))
        eng = n(p.get("likesCount")) + n(p.get("commentsCount"))
        piezas.append({
            "shortCode": p["shortCode"],
            "url": p.get("url"),
            "tipo": p.get("type"),
            "fecha": (p.get("timestamp") or "")[:10],
            "vistas": v,
            "likes": n(p.get("likesCount")),
            "comentarios": n(p.get("commentsCount")),
            # comentarios por mil vistas: la senal de INTENCION, no de alcance.
            # Un reel de obra con dos millones de vistas y cero comentarios no
            # trae a nadie; uno de nicho con 2.000 vistas y 30 comentarios si.
            "coment_x1000": round(1000 * n(p.get("commentsCount")) / v, 2) if v else None,
            "engagement_pct": round(100 * eng / v, 2) if v else None,
            "duracion_s": n(p.get("videoDuration")) or None,
            "hook": (p.get("caption") or "").replace("\n", " ")[:180],
        })

    con_vistas = [x for x in piezas if x["vistas"]]
    con_vistas.sort(key=lambda x: x["coment_x1000"] or 0, reverse=True)

    res = {
        "generado": date.today().isoformat(),
        "etiquetas": ETIQUETAS,
        "tope_usd": op.tope,
        "limite_por_etiqueta": op.limite,
        "total": len(piezas),
        "nota": ("Contenido PUBLICO del nicho Revit + IA. Ordenado por comentarios "
                 "por cada mil vistas, que es intencion y no alcance. Las vistas "
                 "solas engañan: lo que mas vistas nos dio (OBRA) es lo que menos "
                 "comentarios trae por vista."),
        "piezas": piezas,
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"  {len(piezas)} piezas · {len(con_vistas)} con vistas")
    print(f"\n  TOP 12 por comentarios cada mil vistas:")
    for x in con_vistas[:12]:
        print(f"    {x['vistas']:>9,} v · {x['coment_x1000']:>6} c/1k · {x['hook'][:64]}")
    print(f"\n  guardado en {SALIDA}")


if __name__ == "__main__":
    main()
