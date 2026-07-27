"""
DMA Chief of Staff — Panorama de la empresa

Un solo agregador que junta agenda, tareas, comercial, ads y académico.
Alimenta tanto la pregunta "¿cómo vamos?" como el brief de las 7 de la mañana.

Regla de diseño: este módulo NO reimplementa nada. Compone lo que ya existe en
`dma-sales-assistant` — sobre todo `daily_report._build_report()`, que ya arma
el corte comercial del día. Cada bloque va en su propio try: si Meta Ads se cae,
el resto del panorama igual sale.
"""
from __future__ import annotations

import datetime
import logging

import pytz

import google_client as gcal

log = logging.getLogger("dma-panorama")

TZ_EC = pytz.timezone("America/Guayaquil")


def _hoy() -> datetime.datetime:
    return datetime.datetime.now(TZ_EC)


# ── Bloques ───────────────────────────────────────────────────────────────────

def bloque_agenda(dias: int = 1) -> str:
    """Agenda de hoy (o de los próximos N días) desde los calendarios en lista blanca."""
    ahora = _hoy()
    desde = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    hasta = desde + datetime.timedelta(days=dias)

    eventos = gcal.listar_agenda(desde, hasta)
    if not eventos:
        return "📅 *Agenda*\nNada agendado."

    lineas = ["📅 *Agenda*"]
    dia_actual = ""
    for ev in eventos:
        dia = ev["inicio"][:10]
        if dias > 1 and dia != dia_actual:
            dia_actual = dia
            lineas.append(f"\n_{dia}_")
        hora = gcal._fmt_hora(ev["inicio"])
        etiqueta = f" · {ev['calendario']}" if ev["calendario"] != "Personal" else ""
        lineas.append(f"• {hora} — {ev['titulo']}{etiqueta}")
    return "\n".join(lineas)


def bloque_tareas() -> str:
    """Tareas vencidas o que vencen hoy."""
    pendientes = gcal.tareas_vencidas(_hoy().date())
    if not pendientes:
        return "✅ *Tareas*\nSin pendientes vencidos."

    hoy_str = _hoy().date().isoformat()
    lineas = ["📋 *Tareas*"]
    for t in pendientes[:12]:
        marca = "🔴" if t["vence"] < hoy_str else "🟡"
        lineas.append(f"{marca} {t['titulo']}")
    if len(pendientes) > 12:
        lineas.append(f"…y {len(pendientes) - 12} más.")
    return "\n".join(lineas)


def bloque_comercial() -> str:
    """
    Corte comercial del día. Reutiliza el reporte que `daily_report` ya construye
    en vez de volver a consultar y clasificar las conversaciones de GHL.
    """
    try:
        import daily_report
        return daily_report._build_report()
    except Exception as e:
        log.warning(f"⚠️ Panorama comercial no disponible: {e}")
        return "💼 *Comercial*\nNo se pudo leer GHL en este momento."


def bloque_ads(dias: int = 7) -> str:
    try:
        import meta_ads
        return f"📊 *Meta Ads ({dias}d)*\n{meta_ads.resumen_campanas(dias)}"
    except Exception as e:
        log.warning(f"⚠️ Meta Ads no disponible: {e}")
        return "📊 *Meta Ads*\nNo se pudo leer la cuenta de anuncios."


def bloque_academico() -> str:
    try:
        import academico_progreso
        return f"🎓 *Académico*\n{academico_progreso.resumen_snapshot()}"
    except Exception as e:
        log.warning(f"⚠️ Académico no disponible: {e}")
        return "🎓 *Académico*\nSin snapshot de progreso disponible."


# ── Composición ───────────────────────────────────────────────────────────────

BLOQUES = {
    "agenda":    lambda: bloque_agenda(1),
    "tareas":    bloque_tareas,
    "comercial": bloque_comercial,
    "ads":       lambda: bloque_ads(7),
    "academico": bloque_academico,
}


def panorama(secciones: list[str] | None = None) -> str:
    """
    Panorama completo o parcial.

    `secciones` acepta cualquier clave de BLOQUES. Sin argumento devuelve todo.
    El agente pide solo lo que la pregunta necesita — preguntar "¿qué tengo hoy?"
    no debería costar una lectura completa de GHL ni de Meta Ads.
    """
    pedidas = secciones or list(BLOQUES)
    partes = []
    for nombre in pedidas:
        fn = BLOQUES.get(nombre)
        if not fn:
            continue
        try:
            partes.append(fn())
        except Exception as e:
            log.error(f"❌ Bloque '{nombre}' falló: {e}")
            partes.append(f"⚠️ El bloque '{nombre}' falló y se omitió.")
    return "\n\n".join(partes)


def brief_matutino() -> str:
    """Lo que llega por WhatsApp a las 7:00 EC."""
    ahora = _hoy()
    MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    cabecera = f"☀️ *Buenos días, Dayana*\n_{ahora.day} de {MESES[ahora.month - 1]}_"
    return f"{cabecera}\n\n{panorama(['agenda', 'tareas', 'comercial'])}"
