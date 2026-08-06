"""
Ventas e ingresos — lo que el asistente no sabía responder.

Dayana le preguntó "¿cuántas ventas hicimos hoy?" y el asistente no tenía por
dónde mirar: sus 14 herramientas cubrían agenda, tareas y panorama, pero
ninguna tocaba el dinero.

## De dónde sale cada número

Hay dos fuentes y NO dicen lo mismo. Mezclarlas en un solo total sería mentir:

  STRIPE  — dinero cobrado de verdad. Monto exacto, fecha exacta, por cliente.
            Es la única fuente fiable para "¿cuánto facturamos?".
            No ve los pagos por transferencia ni los cobros en efectivo.

  GHL     — inscripciones. Cuenta las oportunidades que están en un stage
            "INSCRITO", que es donde el equipo mueve al cliente cuando confirma
            el pago, venga por donde venga. Cuenta personas, no dólares:
            el monetaryValue de la tarjeta lo escribe un humano y no siempre.

Por eso el resumen los muestra por separado y dice de dónde viene cada uno.
Si Stripe dice 2 y GHL dice 5, no es un bug: son 3 transferencias.

## Zona horaria

Todo se corta por días de Guayaquil, no UTC. "Hoy" a las 20:00 en Quito ya es
mañana en UTC, y sin esto las ventas de la noche saldrían en el día siguiente.
"""
from __future__ import annotations

import datetime
import logging

import pytz
import requests

from config import GHL_LOC, INSCRITO_STAGES, STRIPE_KEY

log = logging.getLogger("dma-assistant")

TZ_EC = pytz.timezone("America/Guayaquil")
STRIPE_API = "https://api.stripe.com/v1"
GHL_API = "https://services.leadconnectorhq.com"

MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


# ── Rango de fechas a partir de como se dice hablando ────────────────────────

def _hoy() -> datetime.date:
    return datetime.datetime.now(TZ_EC).date()


def rango_de(periodo: str = "hoy") -> tuple[datetime.date, datetime.date, str]:
    """
    "hoy" / "ayer" / "semana" / "mes" / "7 días" / "2026-07-20" -> (desde, hasta, etiqueta)

    Ambas fechas van INCLUIDAS. Se acepta lo que sale al dictar, no una sintaxis:
    el modelo pasa lo que oyó y aquí se interpreta.
    """
    p = (periodo or "hoy").strip().lower()
    hoy = _hoy()

    # Fecha suelta en ISO — el modelo la manda así cuando ella dice "el 20 de julio"
    try:
        d = datetime.date.fromisoformat(p)
        return d, d, f"{d.day} de {MESES_ES[d.month - 1]}"
    except ValueError:
        pass

    if p in ("hoy", "el día de hoy", "dia de hoy"):
        return hoy, hoy, "hoy"
    if p in ("ayer",):
        d = hoy - datetime.timedelta(days=1)
        return d, d, "ayer"
    if "semana pasada" in p:
        fin = hoy - datetime.timedelta(days=hoy.weekday() + 1)
        return fin - datetime.timedelta(days=6), fin, "la semana pasada"
    if "semana" in p:
        return hoy - datetime.timedelta(days=hoy.weekday()), hoy, "esta semana"
    if "mes pasado" in p:
        primero_este = hoy.replace(day=1)
        fin = primero_este - datetime.timedelta(days=1)
        return fin.replace(day=1), fin, f"{MESES_ES[fin.month - 1]}"
    if "mes" in p:
        return hoy.replace(day=1), hoy, f"{MESES_ES[hoy.month - 1]}"
    if p in ("año", "ano", "este año", "este ano"):
        return hoy.replace(month=1, day=1), hoy, str(hoy.year)

    # "7 días", "últimos 30 días", "15 dias"
    digitos = "".join(c for c in p if c.isdigit())
    if digitos:
        n = max(1, min(int(digitos), 365))
        return hoy - datetime.timedelta(days=n - 1), hoy, f"los últimos {n} días"

    return hoy, hoy, "hoy"


def _epoch(dia: datetime.date, fin_del_dia: bool = False) -> int:
    """Fecha de Guayaquil -> epoch UTC. Sin esto los cortes de día se corren 5 h."""
    t = datetime.time(23, 59, 59) if fin_del_dia else datetime.time(0, 0, 0)
    return int(TZ_EC.localize(datetime.datetime.combine(dia, t)).timestamp())


# ── Stripe: el dinero ────────────────────────────────────────────────────────

def cobros_stripe(desde: datetime.date, hasta: datetime.date) -> list[dict]:
    """
    Cobros con éxito entre las dos fechas (incluidas), ya netos de reembolsos.

    Devuelve [] si no hay clave configurada: el asistente prefiere decir
    "no puedo ver Stripe" a inventarse un cero.
    """
    if not STRIPE_KEY:
        log.warning("⚠️ ventas: STRIPE_SECRET_KEY sin configurar — sin datos de cobros.")
        return []

    salida: list[dict] = []
    starting_after = None
    for _ in range(10):          # tope duro: 1.000 cobros por consulta
        params = {
            "created[gte]": _epoch(desde),
            "created[lte]": _epoch(hasta, fin_del_dia=True),
            "limit": 100,
        }
        if starting_after:
            params["starting_after"] = starting_after
        try:
            r = requests.get(f"{STRIPE_API}/charges", auth=(STRIPE_KEY, ""),
                             params=params, timeout=20)
        except Exception as e:
            log.error(f"❌ ventas: Stripe no respondió — {e}")
            break
        if not r.ok:
            log.error(f"❌ ventas: Stripe {r.status_code} — {r.text[:200]}")
            break

        data = r.json()
        for ch in data.get("data", []):
            if ch.get("status") != "succeeded" or not ch.get("paid"):
                continue
            neto = (ch.get("amount") or 0) - (ch.get("amount_refunded") or 0)
            if neto <= 0:                     # reembolsado del todo
                continue
            bd = ch.get("billing_details") or {}
            salida.append({
                "monto": neto / 100.0,
                "moneda": (ch.get("currency") or "usd").upper(),
                "cliente": bd.get("name") or bd.get("email") or ch.get("receipt_email") or "Sin nombre",
                "email": bd.get("email") or ch.get("receipt_email") or "",
                "concepto": ch.get("description") or "",
                "fecha": datetime.datetime.fromtimestamp(ch.get("created", 0), TZ_EC).date(),
            })

        if not data.get("has_more"):
            break
        crudos = data.get("data") or []
        if not crudos:
            break
        starting_after = crudos[-1].get("id")

    return salida


# ── GHL: las inscripciones ───────────────────────────────────────────────────

def _headers_ghl() -> dict:
    import ghl_client as ghl
    return ghl.HEADERS


def inscritos_ghl(desde: datetime.date, hasta: datetime.date,
                  max_paginas: int = 2) -> dict:
    """
    {producto: [nombres]} de quienes entraron a un stage INSCRITO en el rango.

    Se filtra por updatedAt en el cliente: la fecha de la tarjeta la pone GHL
    al moverla, que es justo el momento en que el equipo confirma el pago.

    max_paginas está a 2 (200 tarjetas por stage) a propósito: esto se dispara
    desde una nota de voz y tiene que contestar en segundos, no recorrer el CRM
    entero. Si un stage se llena más que eso, lo dice en el resumen.
    """
    desde_ms = _epoch(desde) * 1000
    hasta_ms = _epoch(hasta, fin_del_dia=True) * 1000

    por_producto: dict[str, list] = {}
    try:
        headers = _headers_ghl()
    except Exception as e:
        log.error(f"❌ ventas: sin cliente GHL — {e}")
        return {}

    # Varias claves apuntan al mismo stage (ESPECIALIZACIONES:ACERO, etc.);
    # se consulta cada stage una sola vez.
    vistos: set = set()
    for clave, info in INSCRITO_STAGES.items():
        stage_id = info.get("stage_id")
        if not stage_id or stage_id in vistos:
            continue
        vistos.add(stage_id)
        producto = clave.split(":")[0]

        starting = None
        starting_id = None
        for _ in range(max_paginas):
            params = {
                "location_id": GHL_LOC,
                "pipeline_id": info.get("pipeline_id"),
                "pipeline_stage_id": stage_id,
                "limit": 100,
            }
            if starting:
                params["startAfter"] = starting
                params["startAfterId"] = starting_id
            try:
                r = requests.get(f"{GHL_API}/opportunities/search",
                                 headers=headers, params=params, timeout=20)
                if not r.ok:
                    break
                data = r.json()
            except Exception as e:
                log.warning(f"⚠️ ventas: stage {stage_id} falló — {e}")
                break

            for o in data.get("opportunities", []):
                cuando = o.get("updatedAt") or o.get("createdAt") or ""
                ms = _a_ms(cuando)
                if ms is None or not (desde_ms <= ms <= hasta_ms):
                    continue
                c = o.get("contact") or {}
                nombre = (c.get("name") or o.get("name") or "Sin nombre").strip()
                por_producto.setdefault(producto, []).append(nombre)

            meta = data.get("meta", {}) or {}
            starting = meta.get("startAfter")
            starting_id = meta.get("startAfterId")
            if not starting or not meta.get("nextPage"):
                break

    return por_producto


def _a_ms(valor) -> int | None:
    """GHL devuelve la fecha como ISO ('2026-07-28T15:04:05.000Z') o como epoch ms."""
    if valor in (None, ""):
        return None
    if isinstance(valor, (int, float)):
        return int(valor)
    try:
        txt = str(valor).replace("Z", "+00:00")
        return int(datetime.datetime.fromisoformat(txt).timestamp() * 1000)
    except ValueError:
        return None


# ── Lo que ve el asistente ───────────────────────────────────────────────────

def _fmt(monto: float) -> str:
    return f"${monto:,.2f}"


def resumen_ventas(periodo: str = "hoy") -> str:
    """Cuánto se cobró y cuántos se inscribieron, con las dos fuentes separadas."""
    desde, hasta, etiqueta = rango_de(periodo)
    cobros = cobros_stripe(desde, hasta)
    lineas = [f"💰 Ventas — {etiqueta}"]

    if not STRIPE_KEY:
        lineas.append("\n⚠️ Stripe no está configurado, no puedo ver los cobros.")
    elif not cobros:
        lineas.append("\n💳 Stripe: ningún cobro en este periodo.")
    else:
        por_moneda: dict[str, float] = {}
        for c in cobros:
            por_moneda[c["moneda"]] = por_moneda.get(c["moneda"], 0) + c["monto"]
        totales = " · ".join(f"{_fmt(v)} {m}" for m, v in sorted(por_moneda.items()))
        lineas.append(f"\n💳 Stripe — {len(cobros)} cobro(s), {totales}")
        for c in sorted(cobros, key=lambda x: -x["monto"])[:12]:
            concepto = f" · {c['concepto']}" if c["concepto"] else ""
            lineas.append(f"  • {c['cliente']} — {_fmt(c['monto'])}{concepto}")
        if len(cobros) > 12:
            lineas.append(f"  … y {len(cobros) - 12} más")

    inscritos = inscritos_ghl(desde, hasta)
    total_ins = sum(len(v) for v in inscritos.values())
    if total_ins:
        lineas.append(f"\n🎓 Inscritos en el CRM — {total_ins}")
        for producto, gente in sorted(inscritos.items(), key=lambda x: -len(x[1])):
            lineas.append(f"  • {producto}: {len(gente)} — {', '.join(gente[:5])}"
                          + (" …" if len(gente) > 5 else ""))
    else:
        lineas.append("\n🎓 Inscritos en el CRM: ninguno movido a INSCRITO en este periodo.")

    lineas.append("\n_Stripe = dinero cobrado. CRM = inscripciones confirmadas por el "
                  "equipo (incluye transferencias). No tienen por qué coincidir._")
    return "\n".join(lineas)


def ingresos_por_cliente(periodo: str = "semana") -> str:
    """Cuánto pagó cada cliente en el periodo, de mayor a menor."""
    desde, hasta, etiqueta = rango_de(periodo)
    cobros = cobros_stripe(desde, hasta)
    if not STRIPE_KEY:
        return "⚠️ Stripe no está configurado, no puedo ver los ingresos por cliente."
    if not cobros:
        return f"💰 Ingresos por cliente — {etiqueta}\n\nNingún cobro en este periodo."

    agrupado: dict[str, dict] = {}
    for c in cobros:
        clave = (c["email"] or c["cliente"]).lower()
        item = agrupado.setdefault(clave, {"nombre": c["cliente"], "email": c["email"],
                                           "total": 0.0, "pagos": 0, "conceptos": set()})
        item["total"] += c["monto"]
        item["pagos"] += 1
        if c["concepto"]:
            item["conceptos"].add(c["concepto"])

    total = sum(v["total"] for v in agrupado.values())
    lineas = [f"💰 Ingresos por cliente — {etiqueta}",
              f"{len(agrupado)} cliente(s) · {_fmt(total)} en total\n"]
    for v in sorted(agrupado.values(), key=lambda x: -x["total"]):
        cuotas = f" ({v['pagos']} pagos)" if v["pagos"] > 1 else ""
        que = f" · {', '.join(sorted(v['conceptos']))}" if v["conceptos"] else ""
        lineas.append(f"• {v['nombre']} — {_fmt(v['total'])}{cuotas}{que}")
    return "\n".join(lineas)


def ventas_por_dia(dias: int = 7) -> str:
    """Serie diaria: para ver si la semana va de subida o de bajada."""
    dias = max(1, min(int(dias or 7), 90))
    hasta = _hoy()
    desde = hasta - datetime.timedelta(days=dias - 1)
    cobros = cobros_stripe(desde, hasta)
    if not STRIPE_KEY:
        return "⚠️ Stripe no está configurado, no puedo ver las ventas por día."

    por_dia: dict[datetime.date, list] = {}
    for c in cobros:
        por_dia.setdefault(c["fecha"], []).append(c["monto"])

    total = sum(c["monto"] for c in cobros)
    lineas = [f"📈 Ventas por día — últimos {dias} días",
              f"Total: {_fmt(total)} en {len(cobros)} cobro(s)\n"]
    d = desde
    while d <= hasta:
        montos = por_dia.get(d, [])
        etiqueta = f"{DIAS_ES[d.weekday()][:3]} {d.day:02d}/{d.month:02d}"
        if montos:
            lineas.append(f"  {etiqueta} — {_fmt(sum(montos))} ({len(montos)})")
        else:
            lineas.append(f"  {etiqueta} — —")
        d += datetime.timedelta(days=1)
    return "\n".join(lineas)


def credenciales_ok() -> dict:
    """Para /asistente-diag: qué fuente de ventas está viva."""
    out = {"stripe": False, "ghl": False}
    if STRIPE_KEY:
        try:
            r = requests.get(f"{STRIPE_API}/charges", auth=(STRIPE_KEY, ""),
                             params={"limit": 1}, timeout=10)
            out["stripe"] = r.ok
        except Exception:
            pass
    try:
        r = requests.get(f"{GHL_API}/opportunities/search", headers=_headers_ghl(),
                         params={"location_id": GHL_LOC, "limit": 1}, timeout=10)
        out["ghl"] = r.ok
    except Exception:
        pass
    return out
