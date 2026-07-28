"""
Gmail para el asistente — leer, buscar, responder y enviar.

Reutiliza el OAuth de `google_client`: mismo client_id, mismo refresh token, un
solo consentimiento. Va en un módulo aparte porque Gmail es la superficie más
delicada del asistente — aquí un error no descoloca una agenda, le escribe a un
cliente— y conviene que se lea de un vistazo.

## ⚠️ Hace falta re-autorizar

El refresh token actual se emitió para calendar + tasks + drive.file. Gmail NO
estaba, y Google no amplía scopes de un token ya emitido: hay que rehacer el
consentimiento añadiendo

    https://www.googleapis.com/auth/gmail.modify

y pegar el GOOGLE_REFRESH_TOKEN nuevo en Render. Hasta entonces estas funciones
devuelven un aviso claro en vez de fallar con un 403 críptico.

`gmail.modify` cubre leer, buscar, etiquetar, guardar borradores y enviar. No
cubre borrar definitivamente, a propósito: el asistente no tiene por qué poder
vaciar la papelera de nadie.

## Qué se confirma y qué no

Leer y buscar son reversibles: directo.
Guardar un borrador es reversible: directo.
ENVIAR sale hacia afuera y no se puede deshacer: exige confirmado=true, y eso
se verifica aquí además de pedirse en el prompt.
"""
from __future__ import annotations

import base64
import logging
from email.message import EmailMessage

import google_client as gc

log = logging.getLogger("dma-google")

API_GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"

SCOPE_GMAIL = "https://www.googleapis.com/auth/gmail.modify"

_AVISO_SCOPE = (
    "Gmail todavía no está autorizado. El permiso de Google que tiene el "
    "asistente cubre calendario, tareas y Drive, pero no el correo. Hay que "
    "volver a autorizar añadiendo el scope de Gmail y pegar el refresh token "
    "nuevo en Render (ver asistente-dma/GUIA-MONTAJE.md)."
)


def _es_falta_de_scope(e: Exception) -> bool:
    """Un 403 con 'insufficient' o 'ACCESS_TOKEN_SCOPE' = el token no cubre Gmail."""
    t = str(e)
    return ("403" in t and ("insufficient" in t.lower() or "scope" in t.lower())) or "401" in t


def _get(ruta: str, **kw) -> dict:
    return gc._req("GET", f"{API_GMAIL}{ruta}", **kw)


def _post(ruta: str, **kw) -> dict:
    return gc._req("POST", f"{API_GMAIL}{ruta}", **kw)


# ── Lectura ───────────────────────────────────────────────────────────────────

def _cabecera(payload: dict, nombre: str) -> str:
    for h in (payload.get("headers") or []):
        if (h.get("name") or "").lower() == nombre.lower():
            return h.get("value", "")
    return ""


def _decodificar(data: str) -> str:
    """base64url de Gmail -> texto. Gmail omite el relleno."""
    if not data:
        return ""
    faltan = (-len(data)) % 4
    try:
        return base64.urlsafe_b64decode(data + "=" * faltan).decode("utf-8", errors="replace")
    except Exception:
        return ""


def _cuerpo(payload: dict) -> str:
    """
    Saca el texto del mensaje. Un correo real es un árbol MIME: multipart
    /alternative con texto y HTML, a veces anidado dentro de multipart/mixed
    por los adjuntos. Se recorre entero y se prefiere text/plain; el HTML solo
    entra si no hay alternativa, y se limpia por encima.
    """
    if not payload:
        return ""

    planos: list[str] = []
    htmls: list[str] = []

    def recorrer(parte: dict) -> None:
        mime = parte.get("mimeType", "")
        cuerpo = parte.get("body", {}) or {}
        if mime == "text/plain" and cuerpo.get("data"):
            planos.append(_decodificar(cuerpo["data"]))
        elif mime == "text/html" and cuerpo.get("data"):
            htmls.append(_decodificar(cuerpo["data"]))
        for hijo in (parte.get("parts") or []):
            recorrer(hijo)

    recorrer(payload)

    if planos:
        return "\n".join(planos).strip()
    if htmls:
        import re
        txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", "\n".join(htmls), flags=re.S | re.I)
        txt = re.sub(r"<br\s*/?>|</p>", "\n", txt, flags=re.I)
        txt = re.sub(r"<[^>]+>", " ", txt)
        txt = (txt.replace("&nbsp;", " ").replace("&amp;", "&")
                  .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
        return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]{2,}", " ", txt)).strip()
    return ""


def buscar_correos(consulta: str = "is:unread", limite: int = 10) -> str:
    """
    Busca con la sintaxis de Gmail y devuelve la lista con remitente y asunto.

    `consulta` es literalmente lo que se escribiría en la caja de búsqueda:
      is:unread · from:ester · newer_than:2d · has:attachment · in:inbox
    """
    limite = max(1, min(int(limite or 10), 25))
    try:
        lista = _get("/messages", params={"q": consulta or "is:unread",
                                          "maxResults": limite})
    except Exception as e:
        if _es_falta_de_scope(e):
            return _AVISO_SCOPE
        return f"No pude buscar en Gmail: {e}"

    ids = [m["id"] for m in (lista.get("messages") or [])]
    if not ids:
        return f"Ningún correo para «{consulta}»."

    filas = []
    for mid in ids:
        try:
            m = _get(f"/messages/{mid}", params={
                "format": "metadata",
                "metadataHeaders": ["From", "Subject", "Date"],
            })
        except Exception:
            continue
        p = m.get("payload", {}) or {}
        etiquetas = m.get("labelIds") or []
        filas.append({
            "id":      mid,
            "de":      _cabecera(p, "From"),
            "asunto":  _cabecera(p, "Subject") or "(sin asunto)",
            "fecha":   _cabecera(p, "Date"),
            "no_leido": "UNREAD" in etiquetas,
            "resumen": (m.get("snippet") or "")[:160],
        })

    lineas = [f"📧 {len(filas)} correo(s) — «{consulta}»\n"]
    for f in filas:
        marca = "🔵" if f["no_leido"] else "  "
        lineas.append(f"{marca} *{f['asunto']}*\n   de: {f['de']}\n   {f['resumen']}\n   id: {f['id']}")
    return "\n".join(lineas)


def leer_correo(mensaje_id: str) -> str:
    """El correo entero: cabeceras y cuerpo en texto."""
    if not mensaje_id:
        return "Falta el id del correo. Búscalo primero con buscar_correos."
    try:
        m = _get(f"/messages/{mensaje_id}", params={"format": "full"})
    except Exception as e:
        if _es_falta_de_scope(e):
            return _AVISO_SCOPE
        return f"No pude leer ese correo: {e}"

    p = m.get("payload", {}) or {}
    cuerpo = _cuerpo(p)
    if len(cuerpo) > 6000:
        cuerpo = cuerpo[:6000] + "\n\n[…recortado]"
    return "\n".join([
        f"De: {_cabecera(p, 'From')}",
        f"Para: {_cabecera(p, 'To')}",
        f"Asunto: {_cabecera(p, 'Subject')}",
        f"Fecha: {_cabecera(p, 'Date')}",
        f"id: {mensaje_id}",
        "",
        cuerpo or "(sin texto legible)",
    ])


# ── Escritura ─────────────────────────────────────────────────────────────────

def _mime(para: str, asunto: str, texto: str,
          responde_a: dict | None = None) -> dict:
    msg = EmailMessage()
    msg["To"] = para
    msg["Subject"] = asunto
    msg.set_content(texto)
    if responde_a:
        # Sin estas dos cabeceras el cliente de correo del otro abre un hilo
        # nuevo y la respuesta aparece suelta, fuera de la conversación.
        mid = responde_a.get("message_id")
        if mid:
            msg["In-Reply-To"] = mid
            msg["References"] = mid
    crudo = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    cuerpo = {"raw": crudo}
    if responde_a and responde_a.get("thread_id"):
        cuerpo["threadId"] = responde_a["thread_id"]
    return cuerpo


def _datos_para_responder(mensaje_id: str) -> tuple[dict, str, str]:
    """(contexto_hilo, destinatario, asunto_con_Re) del mensaje al que se responde."""
    m = _get(f"/messages/{mensaje_id}", params={
        "format": "metadata",
        "metadataHeaders": ["From", "Subject", "Message-ID", "Reply-To"],
    })
    p = m.get("payload", {}) or {}
    destino = _cabecera(p, "Reply-To") or _cabecera(p, "From")
    asunto = _cabecera(p, "Subject") or ""
    if not asunto.lower().startswith("re:"):
        asunto = f"Re: {asunto}"
    ctx = {"thread_id": m.get("threadId", ""), "message_id": _cabecera(p, "Message-ID")}
    return ctx, destino, asunto


def guardar_borrador(para: str, asunto: str, texto: str,
                     responder_a_id: str = "") -> str:
    """Deja el correo escrito en Borradores. Reversible: no pide confirmación."""
    try:
        ctx = None
        if responder_a_id:
            ctx, destino, asunto_re = _datos_para_responder(responder_a_id)
            para = para or destino
            asunto = asunto or asunto_re
        d = _post("/drafts", json={"message": _mime(para, asunto, texto, ctx)})
    except Exception as e:
        if _es_falta_de_scope(e):
            return _AVISO_SCOPE
        return f"No pude guardar el borrador: {e}"
    log.info(f"📝 Borrador guardado para {para}: {asunto[:50]}")
    return (f"✅ Borrador guardado (no enviado).\nPara: {para}\nAsunto: {asunto}\n"
            f"Está en Borradores de Gmail para revisarlo antes de mandarlo.")


def enviar_correo(para: str, asunto: str, texto: str,
                  confirmado: bool = False, responder_a_id: str = "") -> str:
    """
    Envía. IRREVERSIBLE.

    Con confirmado=False no toca Gmail: devuelve la previsualización exacta.
    La comprobación está aquí y no solo en el prompt — fiarse de que el modelo
    siempre ponga el flag es fiarse de que nunca se equivoque.
    """
    if not confirmado:
        return ("PENDIENTE DE CONFIRMACIÓN — no se envió nada todavía.\n"
                f"Para: {para or '(el remitente del correo original)'}\n"
                f"Asunto: {asunto or '(Re: del original)'}\n"
                f"Texto:\n{texto}\n\n"
                "Muéstraselo tal cual a Dayana y pídele que confirme.")

    try:
        ctx = None
        if responder_a_id:
            ctx, destino, asunto_re = _datos_para_responder(responder_a_id)
            para = para or destino
            asunto = asunto or asunto_re
        if not para:
            return "No sé a quién enviarlo. Falta el destinatario. No se envió nada."
        _post("/messages/send", json=_mime(para, asunto, texto, ctx))
    except Exception as e:
        if _es_falta_de_scope(e):
            return _AVISO_SCOPE
        return f"No pude enviar el correo: {e}"

    log.info(f"📤 Asistente envió correo a {para}: {asunto[:50]}")
    return f"✅ Correo enviado a {para}\nAsunto: {asunto}"


def credenciales_ok() -> bool:
    """Para /asistente-diag: ¿el token cubre Gmail?"""
    try:
        _get("/profile")
        return True
    except Exception:
        return False
