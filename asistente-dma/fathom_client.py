"""
Fathom — resúmenes y tareas de las reuniones.

## Lo que ya funcionaba y no hacía falta construir

Dayana pidió "que pueda entrar a las reuniones con Fathom y Zoom". Mirando su
cuenta, Fathom YA entra solo: de sus últimas 10 reuniones grabadas hay de Zoom,
de Google Meet y de Microsoft Teams, todas con resumen y tareas ya extraídas.

Así que no hace falta ninguna integración con Zoom, ni que el bot "entre" a
nada. Quien entra es el notetaker de Fathom, por su propia conexión con el
calendario. Lo único que faltaba era que el asistente pudiera LEER lo que
Fathom ya produjo — que es esto.

Si alguna reunión no aparece, se arregla en la configuración de Fathom
(que se una a todas las reuniones del calendario), no en este código.

## Credencial

    FATHOM_API_KEY   → en Render

Se saca en Fathom → Settings → Integrations → API. La API es de plan de pago;
si la clave no está o no tiene permiso, cada función lo dice en una línea en
vez de fallar en silencio.

## Nota sobre el contrato de la API

El entorno donde se construyó esto no tiene salida hacia api.fathom.ai, así que
las rutas y los nombres de campo NO se pudieron probar contra el servicio real:
salen de la documentación y de la forma de los datos que devuelve el conector
de Fathom sobre la misma cuenta. Por eso la lectura de cada campo es tolerante
(`_campo()` prueba varios nombres) y `credenciales_ok()` devuelve el error
literal de Fathom, para que /asistente-diag diga la verdad desde producción en
vez de obligar a adivinar.
"""
from __future__ import annotations

import datetime
import logging
import os

import requests

log = logging.getLogger("dma-assistant")

API = "https://api.fathom.ai/external/v1"
API_KEY = os.getenv("FATHOM_API_KEY", "")

_SIN_CLAVE = ("Fathom no está configurado. Falta FATHOM_API_KEY en Render "
              "(se saca en Fathom → Settings → Integrations → API).")


def _campo(d: dict, *claves, defecto=""):
    """Devuelve el primer campo que exista. La API ha ido renombrando algunos."""
    for k in claves:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return defecto


def _get(ruta: str, params: dict | None = None) -> dict:
    r = requests.get(f"{API}{ruta}", headers={"X-Api-Key": API_KEY,
                                              "Accept": "application/json"},
                     params=params or {}, timeout=30)
    if not r.ok:
        raise RuntimeError(f"Fathom {r.status_code}: {r.text[:250]}")
    return r.json()


def _reuniones(dias: int = 7, limite: int = 10, con_resumen: bool = False,
               con_tareas: bool = False, con_transcripcion: bool = False) -> list[dict]:
    desde = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(days=max(1, min(int(dias or 7), 180))))
    params = {
        "created_after": desde.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "include_summary": "true" if con_resumen else "false",
        "include_action_items": "true" if con_tareas else "false",
        "include_transcript": "true" if con_transcripcion else "false",
    }
    items: list[dict] = []
    cursor = None
    for _ in range(5):                      # tope: ~50 reuniones
        if cursor:
            params["cursor"] = cursor
        data = _get("/meetings", params)
        items.extend(data.get("items") or data.get("meetings") or [])
        cursor = data.get("next_cursor") or (data.get("meta") or {}).get("next_cursor")
        if not cursor or len(items) >= limite:
            break
    return items[:limite]


def _fecha(m: dict) -> str:
    crudo = str(_campo(m, "scheduled_start_time", "recording_start_time",
                       "created_at", "started_at"))
    try:
        d = datetime.datetime.fromisoformat(crudo.replace("Z", "+00:00"))
        return d.strftime("%d/%m/%Y")
    except ValueError:
        return crudo[:10]


def _titulo(m: dict) -> str:
    return str(_campo(m, "meeting_title", "title", defecto="Reunión sin título"))


def _gente(m: dict) -> list[str]:
    nombres = []
    for inv in (_campo(m, "calendar_invitees", "invitees", defecto=[]) or []):
        if isinstance(inv, dict):
            nombres.append(str(_campo(inv, "name", "display_name", "email", defecto="")))
        elif inv:
            nombres.append(str(inv))
    return [n for n in nombres if n]


def _texto_resumen(m: dict) -> str:
    s = _campo(m, "default_summary", "summary", defecto="")
    if isinstance(s, dict):
        return str(_campo(s, "markdown_formatted", "text", "content", defecto=""))
    return str(s or "")


def _tareas(m: dict) -> list[str]:
    salida = []
    for a in (_campo(m, "action_items", "actionItems", defecto=[]) or []):
        if isinstance(a, dict):
            desc = str(_campo(a, "description", "text", "title", defecto="")).strip()
            quien = _campo(a, "assignee", "assigned_to", defecto="")
            if isinstance(quien, dict):
                quien = _campo(quien, "name", "display_name", "email", defecto="")
            salida.append(f"{desc} — {quien}" if quien else desc)
        elif a:
            salida.append(str(a))
    return [s for s in salida if s]


# ── Lo que ve el asistente ───────────────────────────────────────────────────

def ultimas_reuniones(dias: int = 7, limite: int = 10) -> str:
    """Qué reuniones se grabaron, con quién y cuándo. Sin resumen: es la lista."""
    if not API_KEY:
        return _SIN_CLAVE
    try:
        ms = _reuniones(dias=dias, limite=limite)
    except Exception as e:
        return f"No pude leer Fathom: {e}"
    if not ms:
        return f"No hay reuniones grabadas en los últimos {dias} días."

    lineas = [f"🎥 {len(ms)} reunión(es) — últimos {dias} días\n"]
    for m in ms:
        gente = _gente(m)
        con = f" · con {', '.join(gente[:4])}" + (" …" if len(gente) > 4 else "") if gente else ""
        lineas.append(f"• *{_titulo(m)}* — {_fecha(m)}{con}\n  {_campo(m, 'url', 'share_url')}")
    return "\n".join(lineas)


def resumen_reunion(busqueda: str = "", dias: int = 14) -> str:
    """
    Resumen y tareas de una reunión.

    `busqueda` es lo que ella diría: un nombre de persona, un trozo del título,
    o nada para la última. Si encajan varias, las lista para que elija en vez
    de adivinar y resumir la equivocada.
    """
    if not API_KEY:
        return _SIN_CLAVE
    try:
        ms = _reuniones(dias=dias, limite=25, con_resumen=True, con_tareas=True)
    except Exception as e:
        return f"No pude leer Fathom: {e}"
    if not ms:
        return f"No hay reuniones grabadas en los últimos {dias} días."

    q = (busqueda or "").strip().lower()
    if q:
        candidatas = [m for m in ms
                      if q in _titulo(m).lower()
                      or any(q in g.lower() for g in _gente(m))
                      or q in _fecha(m)]
        if not candidatas:
            return (f"No encontré ninguna reunión que cuadre con «{busqueda}» en los "
                    f"últimos {dias} días. Las que hay:\n\n"
                    + "\n".join(f"• {_titulo(m)} — {_fecha(m)}" for m in ms[:8]))
        if len(candidatas) > 1:
            return ("Hay varias que cuadran, dime cuál:\n\n"
                    + "\n".join(f"• {_titulo(m)} — {_fecha(m)}"
                                f" · con {', '.join(_gente(m)[:3]) or 'sin invitados'}"
                                for m in candidatas[:8]))
        m = candidatas[0]
    else:
        m = ms[0]

    resumen = _texto_resumen(m)
    if len(resumen) > 4000:
        resumen = resumen[:4000] + "\n[…recortado]"

    partes = [f"🎥 *{_titulo(m)}* — {_fecha(m)}"]
    gente = _gente(m)
    if gente:
        partes.append(f"Con: {', '.join(gente)}")
    partes.append(f"{_campo(m, 'url', 'share_url')}\n")
    partes.append(resumen or "(Fathom no generó resumen para esta reunión)")

    tareas = _tareas(m)
    if tareas:
        partes.append("\n📌 Tareas que salieron:")
        partes.extend(f"  • {t}" for t in tareas)
    return "\n".join(partes)


def credenciales_ok() -> dict:
    """Para /asistente-diag: ¿la clave sirve? Y si no, el error literal."""
    if not API_KEY:
        return {"ok": False, "detalle": "FATHOM_API_KEY sin configurar"}
    try:
        _get("/meetings", {"include_summary": "false"})
        return {"ok": True, "detalle": ""}
    except Exception as e:
        return {"ok": False, "detalle": str(e)[:200]}
