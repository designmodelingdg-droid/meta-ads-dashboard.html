"""
Canal privado del asistente — WhatsApp Cloud API, sin pasar por GHL.

## El problema que resuelve

Hoy el asistente vive dentro del número del bot, que es un canal de GHL. Eso
significa que TODA la conversación con el asistente —la agenda, el correo, las
cifras de facturación, los resúmenes de reuniones— queda registrada como una
conversación más de GHL, visible para cualquiera del equipo con acceso al CRM.

No es un fallo de configuración: es lo que hace la integración. Conectas un
número a GHL y todo lo que pasa por él se vuelve un registro de GHL. No existe
un "esta conversación no la guardes".

La única forma real de que el asistente sea privado es que no pase por ahí.
Este módulo es esa vía: un número aparte, conectado directamente a la API de
Meta, del que GHL no sabe nada.

    Hoy:    Dayana → número del bot → GHL → server → asistente → GHL → Dayana
                                       ↑ todo el equipo lee esto

    Aquí:   Dayana → número privado → Meta → server → asistente → Meta → Dayana
                                       ↑ nadie más que ella

## Qué hace falta para encenderlo

    WA_TOKEN             token del System User con whatsapp_business_messaging
    WA_PHONE_NUMBER_ID   id del número privado (lo da Meta en API Setup)
    WA_VERIFY_TOKEN      cadena que tú inventas; Meta la repite al verificar
    WA_APP_SECRET        clave secreta de la app de Meta, para validar la firma

Mientras falten, este módulo no hace nada: el webhook responde 200 y descarta.
El bot de ventas sigue igual, porque no comparte ni una línea de este flujo.

## Por qué se valida la firma

Este endpoint es público: cualquiera en internet puede hacerle POST. Sin
comprobar la firma de Meta, bastaría con conocer la URL para inyectar mensajes
haciéndose pasar por Dayana — y el asistente puede leer su correo y mandar
mensajes a clientes. La comprobación es barata y aquí no es opcional.
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import os
import time

log = logging.getLogger("dma-asistente-wa")

VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "dma-wa-verify-2026")
APP_SECRET = os.getenv("WA_APP_SECRET", "")

# Ids de mensaje ya atendidos. Meta reintenta el webhook si tardas en responder,
# y sin esto una nota de voz se procesaría —y se cobraría— dos veces.
_VISTOS: dict = {}
_TTL_VISTOS = 600

# Historial por teléfono, para que "sí, mándalo" sepa a qué se refiere.
# En memoria: el Procfile fuerza --workers 1. Perderlo en un redeploy no cuesta
# nada, es contexto de charla.
_HISTORIAL: dict = {}


def activo() -> bool:
    """¿Está configurado el canal privado? Si no, este módulo no interviene."""
    from config import WA_TOKEN, WA_PHONE_NUMBER_ID
    return bool(WA_TOKEN and WA_PHONE_NUMBER_ID)


# ── Seguridad ────────────────────────────────────────────────────────────────

def firma_valida(cuerpo: bytes, cabecera: str) -> bool:
    """
    Comprueba el X-Hub-Signature-256 que manda Meta.

    Sin APP_SECRET configurado devuelve False y el webhook rechaza todo: es
    preferible que el canal no funcione a que funcione sin autenticar.
    """
    if not APP_SECRET:
        log.error("🔑 FALTA WA_APP_SECRET — no puedo validar la firma de Meta, "
                  "rechazo el webhook. Ponla en Render → Environment.")
        return False
    if not cabecera or not cabecera.startswith("sha256="):
        return False
    esperado = hmac.new(APP_SECRET.encode(), cuerpo, hashlib.sha256).hexdigest()
    # compare_digest y no ==: comparar cadenas con == filtra información por el
    # tiempo que tarda en fallar.
    return hmac.compare_digest(esperado, cabecera.split("=", 1)[1])


def _ya_visto(mensaje_id: str) -> bool:
    if not mensaje_id:
        return False
    ahora = time.time()
    for k, t in list(_VISTOS.items()):
        if ahora - t > _TTL_VISTOS:
            _VISTOS.pop(k, None)
    if mensaje_id in _VISTOS:
        return True
    _VISTOS[mensaje_id] = ahora
    return False


# ── Lectura del payload de Meta ──────────────────────────────────────────────

def extraer_mensajes(payload: dict) -> list[dict]:
    """
    Saca los mensajes entrantes del payload de Meta.

    La forma es profunda y variable —entry[] → changes[] → value.messages[]— y
    muchas notificaciones no traen mensajes en absoluto (acuses de entrega, de
    lectura). Devolver una lista vacía en esos casos es lo correcto.
    """
    salida: list[dict] = []
    for entry in (payload.get("entry") or []):
        for cambio in (entry.get("changes") or []):
            valor = cambio.get("value") or {}
            for m in (valor.get("messages") or []):
                salida.append(m)
    return salida


def texto_del_mensaje(m: dict) -> str:
    """
    Texto de un mensaje, transcribiendo si es nota de voz.

    Devuelve "" para lo que el asistente no sabe atender (una ubicación, un
    sticker), y eso hace que se ignore en silencio en vez de contestar
    cualquier cosa.
    """
    tipo = m.get("type", "")

    if tipo == "text":
        return ((m.get("text") or {}).get("body") or "").strip()

    if tipo in ("audio", "voice"):
        media_id = (m.get(tipo) or {}).get("id", "")
        if not media_id:
            return ""
        try:
            import whatsapp_cloud as wa
            import media_handler as media
            datos = wa.download_media(media_id)
            if not datos:
                log.warning("⚠️ No se pudo bajar la nota de voz de Meta.")
                return ""
            # A diferencia del flujo por GHL, aquí NO se antepone "[Nota de voz]:".
            # Esa marca fue justo lo que rompió el disparador la primera vez, y
            # en este canal no aporta nada: todo lo que llega es para el asistente.
            return media.transcribe_bytes(datos, ".ogg")
        except Exception as e:
            log.error(f"❌ Error transcribiendo nota de voz: {e}")
            return ""

    log.info(f"↩️ Tipo de mensaje ignorado en el canal privado: {tipo}")
    return ""


# ── Flujo ────────────────────────────────────────────────────────────────────

def verificar(mode: str, token: str, challenge: str) -> tuple[str, int]:
    """Responde al saludo de verificación que Meta hace UNA vez, al conectar."""
    if mode == "subscribe" and token == VERIFY_TOKEN:
        log.info("✅ Webhook privado verificado por Meta.")
        return challenge, 200
    log.warning("⚠️ Verificación de webhook rechazada: el token no coincide.")
    return "forbidden", 403


def procesar(payload: dict, autorizado) -> int:
    """
    Atiende un webhook ya validado. Devuelve cuántos mensajes se procesaron.

    `autorizado` es la función que decide si ese teléfono puede usar el
    asistente. Se recibe como parámetro en vez de importarla para no crear una
    dependencia circular con server.py.
    """
    if not activo():
        return 0

    import whatsapp_cloud as wa

    atendidos = 0
    for m in extraer_mensajes(payload):
        mid = m.get("id", "")
        de = m.get("from", "")

        if _ya_visto(mid):
            continue

        # Un número no autorizado no recibe ni un "no puedo atenderte": este
        # número no se publica en ninguna parte, así que quien escriba sin estar
        # en la lista o se equivocó o está probando. En ambos casos, silencio.
        if not autorizado(de):
            log.warning(f"🚫 Mensaje al canal privado desde un número no autorizado: {de[:6]}…")
            continue

        texto = texto_del_mensaje(m)
        if not texto:
            continue

        log.info(f"🔒 Asistente (canal privado) ← {texto[:80]}")
        try:
            import asistente_agent
            respuesta, historial = asistente_agent.responder(
                texto, historial=_HISTORIAL.get(de))
            _HISTORIAL[de] = historial[-12:]
        except Exception as e:
            log.error(f"❌ El asistente falló en el canal privado: {e}", exc_info=True)
            # Aquí solo escribe Dayana, así que se le dice QUÉ falló. Un "no pude
            # procesar" mudo obliga a ir a los logs de Render para saber si fue
            # la clave, la red o el modelo.
            respuesta = (f"❌ Falló procesando: \"{texto[:40]}\"\n\n"
                         f"Motivo: {type(e).__name__}: {str(e)[:180]}")

        try:
            wa.send_text(de, respuesta)
            atendidos += 1
        except Exception as e:
            log.error(f"❌ No pude responder por el canal privado: {e}")

    return atendidos


def diagnostico() -> dict:
    """Para /asistente-diag: si el canal privado está montado y con qué falta."""
    from config import WA_TOKEN, WA_PHONE_NUMBER_ID
    return {
        "activo": activo(),
        "falta": [n for n, v in (("WA_TOKEN", WA_TOKEN),
                                 ("WA_PHONE_NUMBER_ID", WA_PHONE_NUMBER_ID),
                                 ("WA_APP_SECRET", APP_SECRET)) if not v],
        "verify_token_por_defecto": VERIFY_TOKEN == "dma-wa-verify-2026",
    }
