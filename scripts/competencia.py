#!/usr/bin/env python3
"""
Radar de la competencia / del sector con la Graph API oficial de Meta.

Usa `business_discovery`, que permite leer datos PÚBLICOS de otras cuentas
business de Instagram: seguidores, y por publicación caption, likes,
comentarios, tipo y fecha. Gratis y sin límite de créditos.

Límite real: Meta NO entrega insights privados de cuentas ajenas (views,
alcance, guardados). Para eso solo hay estimación por scraping (Apify). Aquí
usamos likes+comentarios como señal de engagement, que sí es pública.

Uso:
    export META_TOKEN=EAA...
    python3 scripts/competencia.py                 # actualiza el radar
    python3 scripts/competencia.py --dry-run
    python3 scripts/competencia.py --add nuevacuenta
"""
import json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "matriz-viral", "matriz", "competencia.json")
BASE = "https://graph.facebook.com/v20.0"

TOKEN = os.environ.get("META_TOKEN", "").strip()
IG_ID = os.environ.get("META_IG_ID", "17841404048578200")

# Cuentas del sector a vigilar. Deben ser cuentas BUSINESS/CREATOR públicas de
# Instagram; si el handle no existe o es personal, Meta devuelve "Invalid user id"
# y el script simplemente la salta (no rompe).
# Para sumar una nueva: agrégala aquí, o pruébala antes con --add nombrecuenta
CUENTAS = ["bimpure", "arquitecturayempresa"]   # verificadas 2026-07-27
POR_CUENTA = 12


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        body = ""
        if hasattr(e, "read"):
            try: body = e.read().decode()[:160]
            except Exception: pass
        return {"error": {"message": f"{e} {body}"}}


def leer_cuenta(usuario):
    campos = (f"business_discovery.username({usuario})"
              "{username,followers_count,media_count,"
              f"media.limit({POR_CUENTA})"
              "{id,caption,like_count,comments_count,timestamp,media_product_type,permalink}}")
    d = api(IG_ID, fields=campos)
    if "error" in d:
        print(f"  ✗ @{usuario}: {d['error']['message'][:90]}")
        return None
    return d.get("business_discovery")


def main():
    if not TOKEN:
        print("ERROR: falta META_TOKEN en el entorno."); sys.exit(1)
    dry = "--dry-run" in sys.argv
    cuentas = list(CUENTAS)
    if "--add" in sys.argv:
        cuentas.append(sys.argv[sys.argv.index("--add") + 1])

    radar, total_posts = [], 0
    for u in cuentas:
        b = leer_cuenta(u)
        if not b: continue
        posts = []
        for m in (b.get("media", {}).get("data") or []):
            likes = m.get("like_count") or 0
            coms = m.get("comments_count") or 0
            posts.append({
                "id": m.get("id"), "fecha": (m.get("timestamp") or "")[:10],
                "tipo": {"REELS": "reel", "FEED": "post"}.get(m.get("media_product_type"), "post"),
                "titulo": (m.get("caption") or "").split("\n")[0][:90],
                "likes": likes, "comentarios": coms,
                "engagement": likes + coms, "url": m.get("permalink"),
            })
        posts.sort(key=lambda p: -p["engagement"])
        radar.append({
            "cuenta": b.get("username"), "seguidores": b.get("followers_count"),
            "publicaciones_totales": b.get("media_count"),
            "muestra": len(posts), "top": posts,
        })
        total_posts += len(posts)
        print(f"  ✓ @{b.get('username')}: {b.get('followers_count'):,} seguidores · {len(posts)} posts leídos")
        time.sleep(0.3)

    if not radar:
        print("No se pudo leer ninguna cuenta."); sys.exit(1)

    # Qué está funcionando en el sector ahora mismo
    todos = [(r["cuenta"], p) for r in radar for p in r["top"]]
    todos.sort(key=lambda x: -x[1]["engagement"])
    print(f"\n=== TOP del sector ({total_posts} posts de {len(radar)} cuentas) ===")
    for cuenta, p in todos[:8]:
        print(f"  {p['engagement']:>5} eng · {p['fecha']} · @{cuenta:22} {p['tipo']:5} {p['titulo'][:46]}")

    salida = {
        "generado": time.strftime("%Y-%m-%d"),
        "fuente": "Meta Graph API · business_discovery (datos públicos)",
        "nota": ("Meta no entrega insights privados de cuentas ajenas (views, alcance, "
                 "guardados). El engagement aquí es likes+comentarios, que sí es público."),
        "cuentas": radar,
        "top_sector": [{"cuenta": c, **p} for c, p in todos[:20]],
    }
    if dry:
        print("\n(--dry-run: no se escribió nada)"); return
    json.dump(salida, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n✓ {os.path.relpath(SALIDA, ROOT)} actualizado")


if __name__ == "__main__":
    main()
