#!/usr/bin/env python3
"""
Baja los datos REALES de las campañas de Meta y los deja en el repo.

POR QUÉ EXISTE
    Cada viernes llega el reporte de la agencia y la regla es que ninguna
    cifra se da por buena sin verificarla contra Meta. Hasta ahora eso
    dependía de que Dayana pasara el META_TOKEN a mano en cada sesión, y
    cuando no lo hacía, la auditoría se quedaba sin contrastar (pasó el
    14-ago: se auditó el reporte solo contra sí mismo).

    Este script corre DENTRO de GitHub Actions, donde el token ya vive
    cifrado como secreto del repo. Baja los datos, los commitea, y a partir
    de ahí cualquiera los lee sin necesitar credencial ninguna.

    El token nunca sale de GitHub. Los datos sí.

QUÉ BAJA
    Tres cortes de la misma ventana, que son los tres que hacen falta para
    auditar el reporte:
      1. por campaña   → el total y el desglose que el reporte suele resumir
      2. por adset     → donde vive el geo-split, que el reporte nunca abre
      3. por día       → destapa si el reporte se generó antes de cerrar el
                         último día (el error del 3-ago: $11 reportados
                         contra $32,67 reales)

USO
    META_TOKEN=EAA... python3 scripts/ads_insights.py
    META_TOKEN=EAA... python3 scripts/ads_insights.py --dias 7
"""
import json, os, sys, time, urllib.request, urllib.parse, urllib.error, argparse
from datetime import date, timedelta

TOKEN = os.environ.get("META_TOKEN", "").strip()
CUENTA = "act_1159622151150228"
API = "https://graph.facebook.com/v20.0"
SALIDA = "matriz-viral/fuentes/ads-insights"

CAMPOS = ("campaign_name,adset_name,spend,impressions,reach,frequency,clicks,ctr,cpc,"
          "objective,actions,action_values,purchase_roas,cost_per_action_type")


def pedir(ruta, params):
    params = {**params, "access_token": TOKEN}
    url = f"{API}/{ruta}?{urllib.parse.urlencode(params)}"
    filas, vueltas = [], 0
    while url and vueltas < 25:
        with urllib.request.urlopen(url, timeout=90) as r:
            d = json.load(r)
        filas += d.get("data", [])
        url = (d.get("paging") or {}).get("next")
        vueltas += 1
        if url:
            time.sleep(0.3)
    return filas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=30, help="ventana hacia atrás (por defecto 30)")
    a = ap.parse_args()

    if not TOKEN:
        print("ERROR: falta META_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)

    # La ventana termina AYER, nunca hoy: un día sin cerrar da cifras cortas
    # y es exactamente el error que se le señaló a la agencia el 3-ago.
    hasta = date.today() - timedelta(days=1)
    desde = hasta - timedelta(days=a.dias - 1)
    rango = json.dumps({"since": desde.isoformat(), "until": hasta.isoformat()})

    cortes = {
        "por-campana": {"level": "campaign", "fields": CAMPOS, "time_range": rango},
        "por-adset":   {"level": "adset",    "fields": CAMPOS, "time_range": rango},
        "por-dia":     {"level": "campaign", "fields": CAMPOS, "time_range": rango,
                        "time_increment": 1},
        "por-pais":    {"level": "campaign", "fields": CAMPOS, "time_range": rango,
                        "breakdowns": "country"},
    }

    os.makedirs(SALIDA, exist_ok=True)
    resumen = {"generado": date.today().isoformat(),
               "ventana": {"desde": desde.isoformat(), "hasta": hasta.isoformat()},
               "nota": ("La ventana termina AYER a proposito: un dia sin cerrar da cifras "
                        "cortas. Es el error que se le senalo a la agencia el 3-ago-2026."),
               "cortes": {}}

    for nombre, params in cortes.items():
        try:
            filas = pedir(f"{CUENTA}/insights", params)
        except urllib.error.HTTPError as e:
            detalle = e.read().decode()[:200]
            print(f"  {nombre}: ERROR {e.code} · {detalle}", file=sys.stderr)
            resumen["cortes"][nombre] = {"error": f"{e.code}", "detalle": detalle}
            continue
        ruta = f"{SALIDA}/{nombre}.json"
        json.dump({"generado": resumen["generado"], "ventana": resumen["ventana"],
                   "filas": filas}, open(ruta, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        gasto = sum(float(f.get("spend") or 0) for f in filas)
        resumen["cortes"][nombre] = {"filas": len(filas), "gasto": round(gasto, 2)}
        print(f"  {nombre}: {len(filas)} filas · ${gasto:,.2f}")
        time.sleep(0.4)

    json.dump(resumen, open(f"{SALIDA}/resumen.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nVentana {desde} → {hasta}. Datos en {SALIDA}/")


if __name__ == "__main__":
    main()
