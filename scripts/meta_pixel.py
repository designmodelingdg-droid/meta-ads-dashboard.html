#!/usr/bin/env python3
"""Baja el estado real del pixel y de la Conversions API de Meta.

Por qué existe: la auditoria tecnica de la cuenta (24-ago-2026) solo pudo
evaluar 14 de 50 checks. Los 36 que faltaron son los de Pixel/CAPI, que pesan
el 30% del score, y no estaban porque `ads_insights.py` baja la API de
Insights, que trae rendimiento de anuncios y nada del pixel.

Esto lo cierra. Corre dentro del Action, que es donde vive META_TOKEN.

Todo lo que pide esta verificado contra la documentacion oficial de Meta
(Marketing API > AdsPixel y su edge /stats), no supuesto:

  - Campos del nodo AdsPixel: id, name, creation_time, last_fired_time,
    data_use_setting, enable_automatic_matching, first_party_cookie_status,
    is_unavailable, owner_business.
  - Edge /stats con `aggregation`, que admite entre otros: event,
    event_source, match_keys, device_type, browser_type, host.
  - `aggregation=event_source` separa WEB_ONLY de SERVER_ONLY. Esa es la
    unica forma fiable de saber por API si la CAPI esta mandando eventos:
    si SERVER_ONLY viene en cero, CAPI no esta desplegada.

LO QUE ESTO **NO** DA, Y CONVIENE NO PROMETERLO:
  El Event Match Quality (EMQ), el numero del 1 al 10 que se ve en Events
  Manager, NO esta expuesto como campo en la Marketing API. Lo que si se
  puede bajar es `aggregation=match_keys`, que dice QUE parametros de
  emparejamiento se estan enviando (email, telefono, nombre, IP, fbc, fbp...).
  Eso es el INSUMO del EMQ, no el EMQ. El informe lo dice asi y no llama EMQ
  a algo que no lo es.

Sin PII: solo se guardan conteos agregados. Ningun evento individual, ningun
correo, ningun telefono.

Uso:
    META_TOKEN=EAA... python3 scripts/meta_pixel.py
    META_TOKEN=EAA... python3 scripts/meta_pixel.py --dias 30
"""

import argparse
import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v20.0"
CUENTA = "act_1159622151150228"          # la misma que usa ads_insights.py
SALIDA = pathlib.Path("matriz-viral/fuentes/meta-pixel")

TOKEN = os.environ.get("META_TOKEN", "").strip()

# Las agregaciones que sirven para auditar, con lo que responde cada una.
AGREGACIONES = {
    "event": "cuantos eventos de cada tipo llegaron",
    "event_source": "WEB_ONLY vs SERVER_ONLY — asi se detecta si la CAPI vive",
    "match_keys": "que parametros de emparejamiento se envian (insumo del EMQ)",
    "device_type": "reparto por dispositivo",
    "browser_type": "reparto por navegador",
}


def pedir(ruta, params=None):
    """Una llamada a la Graph API. Devuelve (datos, error_legible)."""
    p = dict(params or {})
    p["access_token"] = TOKEN
    url = f"{API}/{ruta.lstrip('/')}?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": "DMA-auditoria/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:400]
        # El token nunca se escribe en el log ni en el JSON de salida.
        return None, f"HTTP {e.code}: {cuerpo}"
    except Exception as e:                                  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=30,
                    help="ventana de estadisticas del pixel (por defecto 30)")
    args = ap.parse_args()

    if not TOKEN:
        print("::error::Falta META_TOKEN. Este script corre dentro del Action, "
              "que es donde vive el secreto.", file=sys.stderr)
        return 1

    hoy = datetime.date.today()
    # La ventana termina AYER a proposito: el dia sin cerrar da cifras cortas.
    # Es el mismo criterio de ads_insights.py y el error que se le senalo a la
    # agencia el 3-ago-2026.
    hasta = hoy - datetime.timedelta(days=1)
    desde = hasta - datetime.timedelta(days=args.dias - 1)

    salida = {
        "generado": hoy.isoformat(),
        "ventana": {"desde": desde.isoformat(), "hasta": hasta.isoformat()},
        "fuente": "Meta Marketing API — nodo AdsPixel y su edge /stats",
        "nota_emq": ("El EMQ de Events Manager no esta expuesto en la Marketing "
                     "API. Lo que hay aqui es match_keys, que es el insumo del "
                     "EMQ, no el EMQ. No confundirlos en el informe."),
        "pixeles": [],
        "fallos": [],
    }

    # 1 — que pixeles cuelgan de la cuenta
    campos = ("id,name,creation_time,last_fired_time,data_use_setting,"
              "enable_automatic_matching,first_party_cookie_status,"
              "is_unavailable,owner_business")
    datos, err = pedir(f"{CUENTA}/adspixels", {"fields": campos, "limit": 50})
    if err:
        salida["fallos"].append({"paso": "listar pixeles", "detalle": err})
        SALIDA.mkdir(parents=True, exist_ok=True)
        (SALIDA / "pixel.json").write_text(
            json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"No se pudieron listar los pixeles: {err}", file=sys.stderr)
        return 1

    pixeles = datos.get("data", [])
    print(f"Pixeles en la cuenta: {len(pixeles)}")

    # 2 — por cada pixel, las agregaciones que permiten auditar
    for px in pixeles:
        pid = px.get("id")
        registro = {"config": px, "stats": {}}
        print(f"\n  pixel {pid} · {px.get('name')}")
        print(f"    ultimo disparo: {px.get('last_fired_time') or 's/d'}")

        for agg, para_que in AGREGACIONES.items():
            d, e = pedir(f"{pid}/stats", {
                "aggregation": agg,
                "start_time": desde.isoformat(),
                "end_time": hasta.isoformat(),
            })
            if e:
                registro["stats"][agg] = {"error": e, "para_que": para_que}
                salida["fallos"].append(
                    {"paso": f"stats {agg} de {pid}", "detalle": e})
                print(f"    {agg:16} FALLO — {e[:70]}")
                continue
            filas = d.get("data", [])
            registro["stats"][agg] = {"para_que": para_que, "filas": filas}
            print(f"    {agg:16} ok ({len(filas)} filas)")

        # 3 — la lectura que importa: hay eventos de servidor o no
        fuente = registro["stats"].get("event_source", {}).get("filas") or []
        blob = json.dumps(fuente).upper()
        registro["capi_detectada"] = "SERVER_ONLY" in blob
        registro["nota_capi"] = (
            "Hay eventos SERVER_ONLY: la Conversions API esta enviando."
            if registro["capi_detectada"] else
            "No aparecen eventos SERVER_ONLY en la ventana. Si el pixel si "
            "dispara, la CAPI no esta desplegada — es el check M02, critico, "
            "y Meta cifra la perdida de datos sin el en 30-40%."
        )
        print(f"    -> CAPI: {'SI' if registro['capi_detectada'] else 'NO detectada'}")

        salida["pixeles"].append(registro)

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / "pixel.json"
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    print(f"\nEscrito {destino} — {len(salida['pixeles'])} pixel(es), "
          f"{len(salida['fallos'])} fallo(s).")
    # Un fallo parcial no rompe la corrida: queda anotado en el JSON.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
