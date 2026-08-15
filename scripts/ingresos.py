#!/usr/bin/env python3
"""
Baja los INGRESOS REALES de Stripe y PayPal y los deja en el repo.

POR QUÉ EXISTE
    Hasta ahora el retorno se medía contra las oportunidades "ganadas" del CRM.
    Eso tiene dos problemas conocidos: alguien puede marcar ganada una
    oportunidad que no se cobró, y las reservas de $100 del Máster aparecen
    como venta cuando son un anticipo.

    Stripe y PayPal son la única fuente que no opina: ahí está el dinero que
    de verdad entró. Cruzar eso con el gasto de Meta da el retorno honesto.

    Corre DENTRO de GitHub Actions, donde las credenciales viven cifradas como
    secretos del repo. Los datos se commitean; las credenciales nunca salen.

SECRETOS QUE NECESITA
    STRIPE_SECRET_KEY
    CLIEND_ID_PAYPAL      (sí, con la 'D' — es como está creado el secreto)
    SECRET_KEY_PAYPAL

USO
    python3 scripts/ingresos.py --dias 30
"""
import base64, json, os, sys, time, urllib.request, urllib.parse, urllib.error, argparse
from datetime import date, datetime, timedelta

SALIDA = "matriz-viral/fuentes/ingresos"


def http(url, cab=None, datos=None, metodo="GET"):
    r = urllib.request.Request(url, data=datos, headers=cab or {}, method=metodo)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.load(resp)


# ── STRIPE ─────────────────────────────────────────────────────────
def stripe(desde, hasta):
    clave = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not clave:
        return {"error": "falta STRIPE_SECRET_KEY"}
    cab = {"Authorization": f"Bearer {clave}"}
    ini = int(datetime.combine(desde, datetime.min.time()).timestamp())
    fin = int(datetime.combine(hasta, datetime.max.time()).timestamp())

    cargos, sig, vueltas = [], None, 0
    while vueltas < 20:
        p = {"limit": 100, "created[gte]": ini, "created[lte]": fin}
        if sig:
            p["starting_after"] = sig
        try:
            d = http(f"https://api.stripe.com/v1/charges?{urllib.parse.urlencode(p)}", cab)
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}", "detalle": e.read().decode()[:200]}
        cargos += d.get("data", [])
        if not d.get("has_more"):
            break
        sig = d["data"][-1]["id"]
        vueltas += 1
        time.sleep(0.25)

    # Solo lo cobrado de verdad, y descontando reembolsos
    ok = [c for c in cargos if c.get("paid") and c.get("status") == "succeeded"]
    filas = [{
        "id": c["id"],
        "fecha": datetime.utcfromtimestamp(c["created"]).date().isoformat(),
        "bruto": c["amount"] / 100,
        "reembolsado": c.get("amount_refunded", 0) / 100,
        "neto": (c["amount"] - c.get("amount_refunded", 0)) / 100,
        "moneda": (c.get("currency") or "").upper(),
        "correo": (c.get("billing_details") or {}).get("email") or c.get("receipt_email"),
        "descripcion": c.get("description"),
    } for c in ok]
    return {"cobros": len(filas),
            "neto": round(sum(f["neto"] for f in filas), 2),
            "reembolsado": round(sum(f["reembolsado"] for f in filas), 2),
            "filas": filas}


# ── PAYPAL ─────────────────────────────────────────────────────────
def paypal(desde, hasta):
    cid = os.environ.get("CLIEND_ID_PAYPAL", "").strip() or os.environ.get("CLIENT_ID_PAYPAL", "").strip()
    sec = os.environ.get("SECRET_KEY_PAYPAL", "").strip()
    if not (cid and sec):
        return {"error": "faltan CLIEND_ID_PAYPAL / SECRET_KEY_PAYPAL"}

    base = "https://api-m.paypal.com"
    auth = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    try:
        tok = http(f"{base}/v1/oauth2/token",
                   {"Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"},
                   b"grant_type=client_credentials", "POST")["access_token"]
    except urllib.error.HTTPError as e:
        return {"error": f"login HTTP {e.code}", "detalle": e.read().decode()[:200]}

    cab = {"Authorization": f"Bearer {tok}"}
    filas = []
    # La búsqueda de transacciones de PayPal admite 31 días por petición
    tramo_ini = desde
    while tramo_ini <= hasta:
        tramo_fin = min(tramo_ini + timedelta(days=30), hasta)
        pagina = 1
        while pagina <= 20:
            p = {"start_date": f"{tramo_ini}T00:00:00-0000",
                 "end_date": f"{tramo_fin}T23:59:59-0000",
                 "fields": "transaction_info,payer_info",
                 "page_size": 100, "page": pagina}
            try:
                d = http(f"{base}/v1/reporting/transactions?{urllib.parse.urlencode(p)}", cab)
            except urllib.error.HTTPError as e:
                return {"error": f"HTTP {e.code}", "detalle": e.read().decode()[:200],
                        "filas": filas}
            for t in d.get("transaction_details", []):
                ti = t.get("transaction_info", {}) or {}
                monto = float((ti.get("transaction_amount") or {}).get("value") or 0)
                if monto <= 0:          # deja fuera reembolsos y comisiones
                    continue
                filas.append({
                    "id": ti.get("transaction_id"),
                    "fecha": (ti.get("transaction_initiation_date") or "")[:10],
                    "neto": monto,
                    "moneda": (ti.get("transaction_amount") or {}).get("currency_code"),
                    "correo": ((t.get("payer_info") or {}).get("email_address")),
                    "descripcion": ti.get("transaction_subject") or ti.get("transaction_note"),
                })
            if pagina >= int(d.get("total_pages") or 1):
                break
            pagina += 1
            time.sleep(0.3)
        tramo_ini = tramo_fin + timedelta(days=1)

    return {"cobros": len(filas), "neto": round(sum(f["neto"] for f in filas), 2), "filas": filas}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=30)
    a = ap.parse_args()

    hasta = date.today() - timedelta(days=1)   # nunca hoy: día sin cerrar = cifras cortas
    desde = hasta - timedelta(days=a.dias - 1)
    os.makedirs(SALIDA, exist_ok=True)

    resumen = {"generado": date.today().isoformat(),
               "ventana": {"desde": desde.isoformat(), "hasta": hasta.isoformat()},
               "nota": ("Ingresos REALMENTE cobrados. Es la unica fuente que no opina: "
                        "el CRM puede tener oportunidades marcadas ganadas que no se "
                        "cobraron, y las reservas de $100 del Master no son venta completa."),
               "fuentes": {}}

    for nombre, fn in (("stripe", stripe), ("paypal", paypal)):
        try:
            r = fn(desde, hasta)
        except Exception as e:
            r = {"error": str(e)[:200]}
        json.dump({"generado": resumen["generado"], "ventana": resumen["ventana"], **r},
                  open(f"{SALIDA}/{nombre}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        if "error" in r:
            print(f"  {nombre}: ERROR · {r['error']}", file=sys.stderr)
            resumen["fuentes"][nombre] = {"error": r["error"]}
        else:
            print(f"  {nombre}: {r['cobros']} cobros · ${r['neto']:,.2f}")
            resumen["fuentes"][nombre] = {"cobros": r["cobros"], "neto": r["neto"]}

    total = sum(f.get("neto", 0) for f in resumen["fuentes"].values())
    resumen["total_neto"] = round(total, 2)
    json.dump(resumen, open(f"{SALIDA}/resumen.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nVentana {desde} → {hasta} · total cobrado ${total:,.2f}")


if __name__ == "__main__":
    main()
