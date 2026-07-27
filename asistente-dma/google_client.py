"""
DMA Chief of Staff — Cliente de Google (Calendar + Tasks + Docs)

El repo `dma-sales-assistant` NO tenía ninguna integración con Google. Este
módulo la agrega usando REST directo con `requests`, igual que `ghl_client.py`,
para no arrastrar el SDK pesado de Google.

Autenticación: OAuth de usuario con refresh token (NO service account). Google
Tasks y el calendario personal viven en la cuenta de Dayana; una service account
no puede verlos sin delegación de dominio, que requiere Google Workspace.

Variables de entorno necesarias:
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_REFRESH_TOKEN
    GOOGLE_CALENDAR_PRINCIPAL   (default: designmodelingdg@gmail.com)

Scopes que debe tener el refresh token:
    https://www.googleapis.com/auth/calendar
    https://www.googleapis.com/auth/tasks
    https://www.googleapis.com/auth/drive.file
"""
from __future__ import annotations

import datetime
import logging
import os
import threading

import requests

log = logging.getLogger("dma-google")

CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN", "")

CAL_PRINCIPAL = os.getenv("GOOGLE_CALENDAR_PRINCIPAL", "designmodelingdg@gmail.com")

TZ_NAME = "America/Guayaquil"

# ── Lista blanca de calendarios ───────────────────────────────────────────────
# La cuenta tiene ~90 calendarios y casi todos son de Google Classroom (uno por
# curso). Si el agente los lee todos, el panorama se vuelve ilegible y el gasto
# de tokens se dispara. Solo estos entran en "mi agenda"; los de Classroom se
# consultan aparte y solo cuando se pregunta explícitamente por clases.
CALENDARIOS_AGENDA = {
    CAL_PRINCIPAL:                                                  "Personal",
    "family09784735384594651010@group.calendar.google.com":          "Familia",
    "kjhu31dl7btp672hgultpjl2gg43qu4k@import.calendar.google.com":   "Plan de ventas",
    "classroom100141256514575030881@group.calendar.google.com":      "Máster BIM + IA",
    "36ciqljkv0uboujr1tk3ap9kk7232hj7@import.calendar.google.com":   "Design Modeling Academy",
    "23c35c09bab0183d3139337ceacaf20c9cb42beaa8dab18987d2cefd9cba22df@group.calendar.google.com": "Tareas Hubspot",
}

API_CAL   = "https://www.googleapis.com/calendar/v3"
API_TASKS = "https://tasks.googleapis.com/tasks/v1"
API_DRIVE = "https://www.googleapis.com/drive/v3"
API_UPLOAD = "https://www.googleapis.com/upload/drive/v3"

_token_cache: dict = {"access_token": "", "expira": None}
_token_lock = threading.Lock()


# ── Auth ──────────────────────────────────────────────────────────────────────

def _access_token() -> str:
    """
    Devuelve un access token válido, refrescándolo si está por vencer.

    Cachea en memoria del proceso. `railway.toml` fuerza `--workers 1`, así que
    hay un solo proceso y el caché es coherente. Con varios workers cada uno
    refrescaría por su cuenta — funcionaría igual, solo con llamadas de más.
    """
    with _token_lock:
        ahora = datetime.datetime.now(datetime.timezone.utc)
        expira = _token_cache.get("expira")
        if _token_cache.get("access_token") and expira and ahora < expira:
            return _token_cache["access_token"]

        if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
            raise RuntimeError(
                "Faltan credenciales de Google. Configura GOOGLE_CLIENT_ID, "
                "GOOGLE_CLIENT_SECRET y GOOGLE_REFRESH_TOKEN. "
                "Ver asistente-dma/GUIA-MONTAJE.md"
            )

        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id":     CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": REFRESH_TOKEN,
                "grant_type":    "refresh_token",
            },
            timeout=20,
        )
        if not r.ok:
            raise RuntimeError(f"No se pudo refrescar el token de Google: {r.status_code} {r.text[:200]}")

        data = r.json()
        _token_cache["access_token"] = data["access_token"]
        # 60 s de colchón para no usar un token que vence en el camino.
        _token_cache["expira"] = ahora + datetime.timedelta(seconds=data.get("expires_in", 3600) - 60)
        return _token_cache["access_token"]


def _req(method: str, url: str, **kw) -> dict:
    """Llamada autenticada. Devuelve {} en 204 y lanza en error."""
    headers = kw.pop("headers", {})
    headers["Authorization"] = f"Bearer {_access_token()}"
    r = requests.request(method, url, headers=headers, timeout=kw.pop("timeout", 25), **kw)
    if not r.ok:
        raise RuntimeError(f"Google {method} {url.split('?')[0]} → {r.status_code}: {r.text[:250]}")
    if r.status_code == 204 or not r.content:
        return {}
    return r.json()


def credenciales_ok() -> bool:
    """True si el módulo puede autenticarse. Para el health check."""
    try:
        _access_token()
        return True
    except Exception as e:
        log.warning(f"⚠️ Google sin credenciales válidas: {e}")
        return False


# ── Helpers de fecha ──────────────────────────────────────────────────────────

def _rfc3339(dt: datetime.datetime) -> str:
    return dt.isoformat()


def _fmt_hora(iso: str) -> str:
    """'2026-07-28T16:00:00-05:00' → '16:00'. Evento de día completo → 'todo el día'."""
    if not iso:
        return "?"
    if len(iso) == 10:  # 'YYYY-MM-DD'
        return "todo el día"
    try:
        return datetime.datetime.fromisoformat(iso).strftime("%H:%M")
    except ValueError:
        return iso[11:16] or "?"


# ── Calendar ──────────────────────────────────────────────────────────────────

def listar_agenda(desde: datetime.datetime, hasta: datetime.datetime,
                  calendarios: dict | None = None) -> list[dict]:
    """
    Eventos de los calendarios de la lista blanca entre dos fechas,
    ordenados por hora de inicio.
    """
    cals = calendarios if calendarios is not None else CALENDARIOS_AGENDA
    eventos: list[dict] = []

    for cal_id, etiqueta in cals.items():
        try:
            data = _req(
                "GET", f"{API_CAL}/calendars/{requests.utils.quote(cal_id, safe='')}/events",
                params={
                    "timeMin":      _rfc3339(desde),
                    "timeMax":      _rfc3339(hasta),
                    "singleEvents": "true",
                    "orderBy":      "startTime",
                    "maxResults":   50,
                },
            )
        except Exception as e:
            # Un calendario roto no puede tumbar toda la agenda.
            log.warning(f"⚠️ No se pudo leer el calendario '{etiqueta}': {e}")
            continue

        for ev in data.get("items", []):
            if ev.get("status") == "cancelled":
                continue
            ini = ev.get("start", {})
            fin = ev.get("end", {})
            eventos.append({
                "id":          ev.get("id", ""),
                "calendario":  etiqueta,
                "calendar_id": cal_id,
                "titulo":      ev.get("summary", "(sin título)"),
                "inicio":      ini.get("dateTime") or ini.get("date", ""),
                "fin":         fin.get("dateTime") or fin.get("date", ""),
                "ubicacion":   ev.get("location", ""),
                "link":        ev.get("htmlLink", ""),
                "invitados":   [a.get("email", "") for a in ev.get("attendees", [])],
            })

    eventos.sort(key=lambda e: e["inicio"])
    return eventos


def crear_evento(titulo: str, inicio_iso: str, fin_iso: str, descripcion: str = "",
                 ubicacion: str = "", invitados: list[str] | None = None,
                 calendar_id: str = "") -> dict:
    """Crea un evento. Por defecto en el calendario personal."""
    cal = calendar_id or CAL_PRINCIPAL
    cuerpo = {
        "summary": titulo,
        "start":   {"dateTime": inicio_iso, "timeZone": TZ_NAME},
        "end":     {"dateTime": fin_iso,    "timeZone": TZ_NAME},
    }
    if descripcion:
        cuerpo["description"] = descripcion
    if ubicacion:
        cuerpo["location"] = ubicacion
    if invitados:
        cuerpo["attendees"] = [{"email": e} for e in invitados]

    ev = _req(
        "POST", f"{API_CAL}/calendars/{requests.utils.quote(cal, safe='')}/events",
        params={"sendUpdates": "all" if invitados else "none"},
        json=cuerpo,
    )
    return {"id": ev.get("id", ""), "link": ev.get("htmlLink", ""), "titulo": titulo}


def mover_evento(event_id: str, inicio_iso: str, fin_iso: str, calendar_id: str = "") -> dict:
    """Cambia la hora de un evento existente."""
    cal = calendar_id or CAL_PRINCIPAL
    ev = _req(
        "PATCH",
        f"{API_CAL}/calendars/{requests.utils.quote(cal, safe='')}/events/{event_id}",
        params={"sendUpdates": "all"},
        json={
            "start": {"dateTime": inicio_iso, "timeZone": TZ_NAME},
            "end":   {"dateTime": fin_iso,    "timeZone": TZ_NAME},
        },
    )
    return {"id": ev.get("id", ""), "link": ev.get("htmlLink", ""),
            "titulo": ev.get("summary", "")}


def buscar_hueco(duracion_min: int, desde: datetime.datetime, hasta: datetime.datetime,
                 hora_min: int = 9, hora_max: int = 19) -> list[str]:
    """
    Huecos libres de `duracion_min` minutos, respetando horario laboral.

    Usa freeBusy sobre los calendarios de la lista blanca — así una clase de
    Classroom no bloquea un hueco, pero una reunión real sí.
    """
    ocupado = _req(
        "POST", f"{API_CAL}/freeBusy",
        json={
            "timeMin": _rfc3339(desde),
            "timeMax": _rfc3339(hasta),
            "timeZone": TZ_NAME,
            "items": [{"id": c} for c in CALENDARIOS_AGENDA],
        },
    )

    bloques: list[tuple[datetime.datetime, datetime.datetime]] = []
    for cal in ocupado.get("calendars", {}).values():
        for b in cal.get("busy", []):
            bloques.append((
                datetime.datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
                datetime.datetime.fromisoformat(b["end"].replace("Z", "+00:00")),
            ))
    bloques.sort()

    huecos: list[str] = []
    dur = datetime.timedelta(minutes=duracion_min)
    cursor = desde

    while cursor + dur <= hasta and len(huecos) < 8:
        fin_prop = cursor + dur
        # Fuera de horario laboral → salta a las hora_min del día siguiente.
        if cursor.hour < hora_min or fin_prop.hour > hora_max or fin_prop.day != cursor.day:
            cursor = (cursor + datetime.timedelta(days=1)).replace(
                hour=hora_min, minute=0, second=0, microsecond=0)
            continue
        # Fin de semana → salta al lunes.
        if cursor.weekday() >= 5:
            cursor = (cursor + datetime.timedelta(days=7 - cursor.weekday())).replace(
                hour=hora_min, minute=0, second=0, microsecond=0)
            continue

        choca = any(ini < fin_prop and cursor < fin for ini, fin in bloques)
        if choca:
            cursor += datetime.timedelta(minutes=30)
        else:
            huecos.append(cursor.isoformat())
            cursor += datetime.timedelta(minutes=60)

    return huecos


# ── Tasks ─────────────────────────────────────────────────────────────────────

_lista_default: str = ""


def _tasklist_id() -> str:
    """ID de la lista de tareas por defecto (la primera de la cuenta)."""
    global _lista_default
    if _lista_default:
        return _lista_default
    data = _req("GET", f"{API_TASKS}/users/@me/lists", params={"maxResults": 10})
    items = data.get("items", [])
    if not items:
        raise RuntimeError("La cuenta de Google no tiene ninguna lista de tareas.")
    _lista_default = items[0]["id"]
    return _lista_default


def crear_tarea(titulo: str, notas: str = "", vence_iso: str = "") -> dict:
    """Crea una tarea en Google Tasks. `vence_iso` en formato YYYY-MM-DD."""
    cuerpo = {"title": titulo}
    if notas:
        cuerpo["notes"] = notas
    if vence_iso:
        # Google Tasks ignora la hora del due date, pero exige RFC3339 completo.
        cuerpo["due"] = f"{vence_iso[:10]}T00:00:00.000Z"

    t = _req("POST", f"{API_TASKS}/lists/{_tasklist_id()}/tasks", json=cuerpo)
    return {"id": t.get("id", ""), "titulo": titulo, "vence": vence_iso}


def listar_tareas(incluir_completadas: bool = False) -> list[dict]:
    data = _req(
        "GET", f"{API_TASKS}/lists/{_tasklist_id()}/tasks",
        params={
            "showCompleted": "true" if incluir_completadas else "false",
            "maxResults": 100,
        },
    )
    tareas = [{
        "id":      t.get("id", ""),
        "titulo":  t.get("title", ""),
        "notas":   t.get("notes", ""),
        "vence":   (t.get("due") or "")[:10],
        "estado":  t.get("status", ""),
    } for t in data.get("items", []) if t.get("title")]

    # Las que tienen fecha primero y por vencimiento; las sueltas al final.
    tareas.sort(key=lambda t: t["vence"] or "9999-12-31")
    return tareas


def completar_tarea(task_id: str) -> dict:
    t = _req("PATCH", f"{API_TASKS}/lists/{_tasklist_id()}/tasks/{task_id}",
             json={"status": "completed"})
    return {"id": t.get("id", ""), "titulo": t.get("title", "")}


def tareas_vencidas(hoy: datetime.date) -> list[dict]:
    """Tareas pendientes cuya fecha ya pasó o es hoy. Para el brief matutino."""
    limite = hoy.isoformat()
    return [t for t in listar_tareas() if t["vence"] and t["vence"] <= limite]


# ── Notas (Google Docs vía Drive) ─────────────────────────────────────────────

CARPETA_NOTAS_ID = os.getenv("GOOGLE_CARPETA_NOTAS", "")


def crear_nota(titulo: str, contenido: str) -> dict:
    """
    Crea un Google Doc con el contenido de la nota.

    Sube texto plano y deja que Drive lo convierta a Google Doc — así se evita
    el batchUpdate de la API de Docs, que necesitaría un scope extra.
    """
    metadata = {"name": titulo, "mimeType": "application/vnd.google-apps.document"}
    if CARPETA_NOTAS_ID:
        metadata["parents"] = [CARPETA_NOTAS_ID]

    import json as _json
    boundary = "dma-nota-boundary"
    cuerpo = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{_json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        "Content-Type: text/plain; charset=UTF-8\r\n\r\n"
        f"{contenido}\r\n"
        f"--{boundary}--"
    ).encode("utf-8")

    doc = _req(
        "POST", f"{API_UPLOAD}/files",
        params={"uploadType": "multipart", "fields": "id,name,webViewLink"},
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
        data=cuerpo,
    )
    return {"id": doc.get("id", ""), "titulo": doc.get("name", titulo),
            "link": doc.get("webViewLink", "")}


def buscar_notas(texto: str, limite: int = 10) -> list[dict]:
    """Busca notas por texto en el nombre o el contenido."""
    q = f"fullText contains '{texto.replace(chr(39), '')}' and mimeType='application/vnd.google-apps.document' and trashed=false"
    data = _req("GET", f"{API_DRIVE}/files",
                params={"q": q, "pageSize": limite,
                        "fields": "files(id,name,webViewLink,modifiedTime)"})
    return [{"id": f["id"], "titulo": f["name"], "link": f.get("webViewLink", ""),
             "modificado": f.get("modifiedTime", "")[:10]} for f in data.get("files", [])]
