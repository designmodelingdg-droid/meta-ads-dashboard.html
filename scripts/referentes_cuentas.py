#!/usr/bin/env python3
"""Trae las publicaciones recientes de varias cuentas de referencia de Instagram, con
Apify y un tope DURO de gasto para toda la corrida.

    python3 scripts/referentes_cuentas.py matriz-viral/pedidos/referentes-cuentas.json

Pedido: {"cuentas": ["lexmrbim", ...], "por_cuenta": 30, "tope_usd": 1.0, "motivo": "..."}
Sale en matriz-viral/fuentes/referentes/cuentas-<AAAA-MM-DD>.json: por publicación,
la cuenta, el tipo, el texto (recortado), likes, comentarios, vistas, fecha y enlace.
No se guardan imágenes de terceros. Sin APIFY_TOKEN no hace nada; si Apify falla no
escribe nada (vacío antes que inventado). El token nunca se imprime.
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
R = pathlib.Path(__file__).resolve().parent.parent
SAL = R / "matriz-viral" / "fuentes" / "referentes"


def main():
    if not TOKEN:
        print("Sin APIFY_TOKEN: no se corre nada.")
        return
    pedido = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    cuentas = [c.lstrip("@").strip() for c in pedido["cuentas"] if c.strip()]
    por_cuenta = min(int(pedido.get("por_cuenta", 30)), 40)
    tope = min(float(pedido.get("tope_usd", 1.0)), 1.0)
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    salida_f = SAL / f"cuentas-{hoy}.json"
    if salida_f.exists() and not pedido.get("forzar"):
        print(f"Ya existe {salida_f.relative_to(R)}: no se vuelve a cobrar.")
        return
    entrada = {"directUrls": [f"https://www.instagram.com/{c}/" for c in cuentas],
               "resultsType": "posts", "resultsLimit": por_cuenta, "addParentData": False,
               "maxTotalChargeUsd": tope}
    url = ("https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items"
           f"?token={TOKEN}&maxTotalChargeUsd={tope}")
    req = urllib.request.Request(url, data=json.dumps(entrada).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=290) as r:
            items = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Apify HTTP {e.code}: {e.read().decode()[:300]}")
        return
    except Exception as e:  # noqa: BLE001
        print(f"Fallo de red con Apify: {e}")
        return
    filas = []
    for p in items or []:
        if p.get("error"):
            print(f"AVISO {p.get('inputUrl')}: {p.get('error')}")
            continue
        filas.append({
            "cuenta": p.get("ownerUsername"), "tipo": p.get("type"), "producto": p.get("productType"),
            "fecha": p.get("timestamp"), "url": p.get("url"),
            "texto": (p.get("caption") or "")[:600],
            "likes": p.get("likesCount"), "comentarios": p.get("commentsCount"),
            "vistas": p.get("videoViewCount") or p.get("videoPlayCount"),
            "duracion_s": p.get("videoDuration"),
        })
    if not filas:
        print("Sin datos. No se escribe nada.")
        return
    SAL.mkdir(parents=True, exist_ok=True)
    salida_f.write_text(json.dumps({
        "traido": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "fuente": "Apify · apify~instagram-scraper (perfiles públicos)",
        "motivo": pedido.get("motivo"), "cuentas": cuentas, "tope_usd": tope,
        "total": len(filas), "publicaciones": filas}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    por = {}
    for f in filas:
        por[f["cuenta"]] = por.get(f["cuenta"], 0) + 1
    print(f"Guardado {salida_f.relative_to(R)}: {len(filas)} publicaciones · {por}")


if __name__ == "__main__":
    main()
