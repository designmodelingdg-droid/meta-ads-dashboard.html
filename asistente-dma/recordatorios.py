"""
DMA Chief of Staff — Recordatorios proactivos por WhatsApp

Todo lo demás del asistente es reactivo: Dayana pregunta, él responde. Esto es
lo contrario — el bot escribe primero, sin que nadie le hable.

Qué manda:
  • 30 min antes de cada reunión → "En 30 min: sesión con Patricio"
  • A las 8:00 → lo que vence hoy (Google Tasks + ClickUp)
  • A las 18:00 → lo que quedó pendiente y vence hoy

## La ventana de 24 horas — leer antes de tocar este archivo

WhatsApp solo deja mandar texto libre si la persona te escribió en las últimas
24 h. Fuera de esa ventana, Meta rechaza el mensaje y **el recordatorio no
llega**. No es un error del código: es política de la plataforma.

Como Dayana usa el asistente a diario por voz, la ventana casi siempre está
abierta. Pero "casi siempre" no sirve para un recordatorio — el día que falle
es justo el día que se le pasa la reunión.

Por eso cada envío intenta texto libre y, si Meta lo rechaza, reintenta como
**plantilla aprobada** (`WA_TEMPLATE_RECORDATORIO`). Sin esa plantilla creada
en el Business Manager, los recordatorios son fiables solo dentro de la
ventana. Está explicado en GUIA-MONTAJE.md.
"""
from __future__ import annotations

import datetime
import json
import logging
import os

import pytz

log = logging.getLogger("dma-recordatorios")

TZ_EC = pytz.timezone("America/Guayaquil")

# Aviso ~30 min antes. El scheduler corre cada 15 min, así que la ventana mide
# exactamente 15: en cada tick el "faltan" de un evento baja 15 minutos, de modo
# que cae dentro de la banda una sola vez. Más ancha avisaría dos veces (lo
# atraparía el anti-duplicado, pero por los pelos); más angosta lo saltaría.
MINUTOS_ANTES = 30
VENTANA_MIN, VENTANA_MAX = 20, 35

ESTADO_FILE = os.getenv("RECORDATORIOS_FILE", "/tmp/dma_recordatorios.json")
TEMPLATE_FALLBACK = os.getenv("WA_TEMPLATE_RECORDATORIO", "")

DESTINO = os.getenv("ADMIN_PHONE", "593984372010")


# ── Estado (anti-duplicado) ───────────────────────────────────────────────────

def _estado() -> dict:
    """Qué se recordó ya hoy. Se reinicia solo al cambiar el día."""
    hoy = datetime.datetime.now(TZ_EC).strftime("%Y-%m-%d")
    try:
        with open(ESTADO_FILE) as f:
            data = json.load(f)
        if data.get("fecha") == hoy:
            return data
    except Exception:
        pass
    return {"fecha": hoy, "recordados": []}


def _marcar(clave: str) -> None:
    data = _estado()
    if clave not in data["recordados"]:
        data["recordados"].append(clave)
    try:
        with open(ESTADO_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        log.warning(f"⚠️ No se pudo guardar el estado de recordatorios: {e}")


def _ya_recordado(clave: str) -> bool:
    return clave in _estado()["recordados"]


# ── Envío ─────────────────────────────────────────────────────────────────────

def _enviar(texto: str) -> bool:
    """
    Manda el recordatorio. Texto libre primero; si Meta lo rechaza por la
    ventana de 24 h, reintenta como plantilla.
    """
    try:
        import whatsapp_cloud as wa
    except ImportError:
        log.error("❌ whatsapp_cloud no disponible; no se envía el recordatorio.")
        return False

    r = wa.send_text(DESTINO, texto)
    if not r.get("error"):
        return True

    log.warning(f"⚠️ Texto libre rechazado (probable ventana de 24 h): {str(r['error'])[:120]}")

    if not TEMPLATE_FALLBACK:
        log.error("❌ Recordatorio NO entregado y no hay WA_TEMPLATE_RECORDATORIO configurada.")
        return False

    try:
        # La plantilla debe tener un parámetro {{1}} donde va el texto.
        # WhatsApp no acepta saltos de línea dentro de un parámetro de plantilla.
        plano = texto.replace("\n", " · ").replace("*", "")
        r2 = wa.send_template(DESTINO, TEMPLATE_FALLBACK, lang="es", body_params=[plano])
        if r2.get("error"):
            log.error(f"❌ La plantilla también falló: {str(r2['error'])[:120]}")
            return False
        return True
    except Exception as e:
        log.error(f"❌ Fallback a plantilla falló: {e}")
        return False


# ── Recordatorio de reuniones ─────────────────────────────────────────────────

def revisar_eventos_proximos() -> int:
    """Avisa de los eventos que empiezan en ~30 min. Devuelve cuántos avisó."""
    import google_client as gcal

    ahora = datetime.datetime.now(TZ_EC)
    desde = ahora + datetime.timedelta(minutes=VENTANA_MIN)
    hasta = ahora + datetime.timedelta(minutes=VENTANA_MAX)

    try:
        eventos = gcal.listar_agenda(desde, hasta)
    except Exception as e:
        log.error(f"❌ No se pudo leer la agenda para recordatorios: {e}")
        return 0

    enviados = 0
    for ev in eventos:
        # Los eventos de día completo no tienen hora; recordarlos "en 30 min"
        # no significa nada.
        if len(ev["inicio"]) == 10:
            continue

        clave = f"ev:{ev['id']}"
        if _ya_recordado(clave):
            continue

        try:
            inicio = datetime.datetime.fromisoformat(ev["inicio"])
            faltan = int((inicio - ahora).total_seconds() / 60)
        except ValueError:
            faltan = MINUTOS_ANTES

        partes = [f"⏰ *En {faltan} min:* {ev['titulo']}"]
        if ev.get("ubicacion"):
            partes.append(f"📍 {ev['ubicacion']}")
        if ev.get("invitados"):
            partes.append("👥 " + ", ".join(ev["invitados"][:4]))

        if _enviar("\n".join(partes)):
            _marcar(clave)
            enviados += 1
            log.info(f"⏰ Recordado: {ev['titulo']} ({faltan} min)")

    return enviados


# ── Resumen de pendientes ─────────────────────────────────────────────────────

def _pendientes_de_hoy() -> list[str]:
    """Lo que vence hoy, juntando Google Tasks y ClickUp."""
    hoy = datetime.datetime.now(TZ_EC).date()
    lineas: list[str] = []

    try:
        import google_client as gcal
        for t in gcal.tareas_vencidas(hoy):
            marca = "🔴" if t["vence"] < hoy.isoformat() else "🟡"
            lineas.append(f"{marca} {t['titulo']}")
    except Exception as e:
        log.warning(f"⚠️ Google Tasks no disponible para el resumen: {e}")

    try:
        import clickup_client as cu
        for t in cu.tareas_de("dayana"):
            if t["vence"] and t["vence"] <= hoy.isoformat():
                marca = "🔴" if t["vence"] < hoy.isoformat() else "🟡"
                lineas.append(f"{marca} {t['titulo']} · _{t['lista']}_")
    except Exception as e:
        log.warning(f"⚠️ ClickUp no disponible para el resumen: {e}")

    return lineas


def resumen_manana() -> bool:
    """8:00 — la agenda del día y lo que vence."""
    if _ya_recordado("resumen:manana"):
        return False

    try:
        import panorama
        texto = panorama.brief_matutino()
    except Exception as e:
        log.error(f"❌ No se pudo armar el brief matutino: {e}")
        return False

    if _enviar(texto):
        _marcar("resumen:manana")
        return True
    return False


def resumen_tarde() -> bool:
    """18:00 — solo lo que sigue pendiente y vencía hoy. Silencio si no hay nada."""
    if _ya_recordado("resumen:tarde"):
        return False

    pendientes = _pendientes_de_hoy()
    if not pendientes:
        _marcar("resumen:tarde")   # nada que decir tampoco es un fallo
        return False

    texto = ("🌆 *Cierre del día*\nEsto vencía hoy y sigue abierto:\n\n"
             + "\n".join(pendientes[:10]))
    if _enviar(texto):
        _marcar("resumen:tarde")
        return True
    return False


# ── Registro en el scheduler ──────────────────────────────────────────────────

def registrar_jobs(scheduler) -> None:
    """
    Engancha los tres trabajos al APScheduler que server.py ya tiene levantado.

    `replace_existing` evita jobs duplicados si el módulo se recarga.
    """
    scheduler.add_job(revisar_eventos_proximos, "interval", minutes=15,
                      id="recordatorio_eventos", replace_existing=True)
    scheduler.add_job(resumen_manana, "cron", hour=8, minute=0, timezone=TZ_EC,
                      id="recordatorio_manana", replace_existing=True)
    scheduler.add_job(resumen_tarde, "cron", hour=18, minute=0, timezone=TZ_EC,
                      id="recordatorio_tarde", replace_existing=True)
    log.info("⏰ Recordatorios registrados: eventos c/15min, resumen 8:00 y 18:00")
