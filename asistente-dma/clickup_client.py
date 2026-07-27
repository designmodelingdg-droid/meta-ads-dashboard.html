"""
DMA Chief of Staff — Cliente de ClickUp (tareas para el equipo)

Google Tasks sirve para las tareas *de Dayana*, pero no puede asignarle nada a
otra persona: es una lista personal, no un gestor de equipo. Para "créale una
tarea a Ester" hace falta ClickUp, que es donde el equipo ya trabaja.

Los IDs de abajo salen del workspace real de DMA (4 espacios, 12 listas, 6
personas), leídos con el conector de ClickUp. Están escritos aquí a propósito:
resolverlos por nombre en cada llamada costaría 2-3 requests extra por tarea y
haría que el asistente se demore en responder una nota de voz.

Variable de entorno necesaria:
    CLICKUP_TOKEN   — token personal (Settings → Apps → API Token, empieza por pk_)
"""
from __future__ import annotations

import datetime
import logging
import os
import unicodedata

import requests

log = logging.getLogger("dma-clickup")

API = "https://api.clickup.com/api/v2"
TOKEN = os.getenv("CLICKUP_TOKEN", "")

# ── Equipo real de DMA en ClickUp ─────────────────────────────────────────────
# La clave es como Dayana los nombra en voz alta; los alias cubren lo que
# Whisper suele devolver (sin tildes, solo nombre de pila, apodos).
EQUIPO = {
    "dayana": {
        "id": "204092995", "email": "designmodelingdg@gmail.com",
        "nombre": "Dayana Calderón Brunetti",
        "alias": ["daya", "yo", "mi", "dayana calderon", "dayana brunetti"],
    },
    "ester": {
        "id": "204091388", "email": "asistencia.generaldg@gmail.com",
        "nombre": "Ester Álvarez",
        "alias": ["esther", "ester alvarez", "asistencia", "asistente general"],
    },
    "gabriel": {
        "id": "101130129", "email": "gabrielpantoja.ucab@gmail.com",
        "nombre": "Gabriel Pantoja Linares",
        "alias": ["gabo", "pantoja", "gabriel pantoja"],
    },
    "eber": {
        "id": "204179390", "email": "martinezeber61@gmail.com",
        "nombre": "Eber Martínez",
        "alias": ["heber", "eber martinez", "uruguay"],
    },
    "patricio": {
        "id": "101264643", "email": "patriciostagno@gmail.com",
        "nombre": "Patricio Stagno",
        "alias": ["pato", "patricio stagno", "stagno"],
    },
    "aylin": {
        "id": "101266192", "email": "aylin.taur@gmail.com",
        "nombre": "Aylin Tapia",
        "alias": ["aylin tapia", "ailin", "aylín"],
    },
}

# ── Listas reales del workspace ───────────────────────────────────────────────
LISTAS = {
    # Marketing + Diseño Gráfico
    "campañas meta":      "901712465678",
    "redes sociales":     "901712465691",
    "audiovisual":        "901712465701",
    "ideas campañas":     "901715052025",
    # Admin + Soporte al Cliente
    "documentación":      "901712465594",
    "soporte cliente":    "901715053233",
    # Tech + Bot
    "web dma":            "901714958252",
    "leadgods":           "901712465558",
    "gohighlevel":        "901712465356",
    "bots":               "901715055076",
    # Ventas + Asesores Comerciales
    "cursos":             "901712531927",
    "máster y diplomados": "901714227998",
}

# A dónde va una tarea cuando Dayana no dice la lista. Elegido por el área en la
# que cada persona trabaja de verdad, para que nada caiga en un cajón de sastre.
LISTA_POR_PERSONA = {
    "patricio": "audiovisual",
    "aylin":    "redes sociales",
    "ester":    "soporte cliente",
    "gabriel":  "gohighlevel",
    "eber":     "cursos",
    "dayana":   "ideas campañas",
}
LISTA_DEFAULT = "documentación"

PRIORIDADES = {"urgente": 1, "alta": 2, "normal": 3, "baja": 4}


def _headers() -> dict:
    if not TOKEN:
        raise RuntimeError(
            "Falta CLICKUP_TOKEN. Sácalo en ClickUp → Settings → Apps → "
            "Generate API Token. Ver asistente-dma/GUIA-MONTAJE.md"
        )
    return {"Authorization": TOKEN, "Content-Type": "application/json"}


def credenciales_ok() -> bool:
    """True si el token responde. Para el health check."""
    try:
        r = requests.get(f"{API}/user", headers=_headers(), timeout=15)
        return r.ok
    except Exception as e:
        log.warning(f"⚠️ ClickUp sin credenciales válidas: {e}")
        return False


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn").strip()


def resolver_persona(quien: str) -> dict | None:
    """
    'Ester', 'esther', 'asistencia.generaldg@gmail.com' → la ficha del equipo.

    Tolerante a propósito: viene de una transcripción de voz, donde los nombres
    llegan sin tilde y a veces mal escritos.
    """
    if not quien:
        return None
    q = _sin_tildes(quien)

    for clave, p in EQUIPO.items():
        if q == p["email"].lower():
            return p
        if q == clave or q == _sin_tildes(p["nombre"]):
            return p
        if any(q == _sin_tildes(a) for a in p["alias"]):
            return p

    # Coincidencia parcial: "créale una tarea a gabriel pantoja linares".
    for clave, p in EQUIPO.items():
        if clave in q or q in _sin_tildes(p["nombre"]):
            return p
        if any(_sin_tildes(a) in q for a in p["alias"]):
            return p
    return None


def resolver_lista(nombre: str, persona_clave: str = "") -> str:
    """Nombre de lista → id. Si no se dice ninguna, va a la del área de la persona."""
    if nombre:
        n = _sin_tildes(nombre)
        for etiqueta, lid in LISTAS.items():
            if n == _sin_tildes(etiqueta) or n in _sin_tildes(etiqueta):
                return lid
    if persona_clave:
        return LISTAS[LISTA_POR_PERSONA.get(persona_clave, LISTA_DEFAULT)]
    return LISTAS[LISTA_DEFAULT]


def crear_tarea(titulo: str, para: str = "", descripcion: str = "",
                vence: str = "", prioridad: str = "", lista: str = "") -> dict:
    """
    Crea una tarea en ClickUp y se la asigna a alguien del equipo.

    `vence` en YYYY-MM-DD. ClickUp espera epoch en milisegundos.
    """
    persona = resolver_persona(para) if para else None
    clave = next((k for k, v in EQUIPO.items() if persona and v["id"] == persona["id"]), "")

    cuerpo: dict = {"name": titulo}
    if descripcion:
        cuerpo["description"] = descripcion
    if persona:
        cuerpo["assignees"] = [int(persona["id"])]
    if prioridad:
        p = PRIORIDADES.get(_sin_tildes(prioridad))
        if p:
            cuerpo["priority"] = p
    if vence:
        try:
            d = datetime.date.fromisoformat(vence[:10])
            # Vence al final del día, no a medianoche: una tarea "para el viernes"
            # no está atrasada el viernes a las 9 de la mañana.
            cuerpo["due_date"] = int(datetime.datetime(
                d.year, d.month, d.day, 23, 59).timestamp() * 1000)
            cuerpo["due_date_time"] = True
        except ValueError:
            log.warning(f"⚠️ Fecha inválida ignorada: {vence}")

    list_id = resolver_lista(lista, clave)
    r = requests.post(f"{API}/list/{list_id}/task", headers=_headers(),
                      json=cuerpo, timeout=25)
    if not r.ok:
        raise RuntimeError(f"ClickUp no pudo crear la tarea: {r.status_code} {r.text[:200]}")

    t = r.json()
    etiqueta_lista = next((k for k, v in LISTAS.items() if v == list_id), list_id)
    return {
        "id":     t.get("id", ""),
        "titulo": t.get("name", titulo),
        "link":   t.get("url", ""),
        "para":   persona["nombre"] if persona else "sin asignar",
        "email":  persona["email"] if persona else "",
        "lista":  etiqueta_lista,
        "vence":  vence,
    }


def tareas_de(quien: str = "", solo_abiertas: bool = True) -> list[dict]:
    """Tareas asignadas a alguien, en todas las listas del workspace."""
    persona = resolver_persona(quien) if quien else None
    encontradas: list[dict] = []

    # Se comprueba el token una vez y no doce: sin esto, un token ausente
    # ensucia el log con un aviso idéntico por cada lista del workspace.
    if not TOKEN:
        log.warning("⚠️ ClickUp sin CLICKUP_TOKEN; se omiten las tareas del equipo.")
        return []

    for etiqueta, list_id in LISTAS.items():
        params: dict = {"subtasks": "true"}
        if solo_abiertas:
            params["include_closed"] = "false"
        if persona:
            params["assignees[]"] = persona["id"]
        try:
            r = requests.get(f"{API}/list/{list_id}/task", headers=_headers(),
                             params=params, timeout=20)
            if not r.ok:
                continue
            for t in r.json().get("tasks", []):
                vence = ""
                if t.get("due_date"):
                    vence = datetime.datetime.fromtimestamp(
                        int(t["due_date"]) / 1000).strftime("%Y-%m-%d")
                encontradas.append({
                    "id":     t.get("id", ""),
                    "titulo": t.get("name", ""),
                    "lista":  etiqueta,
                    "estado": (t.get("status") or {}).get("status", ""),
                    "vence":  vence,
                    "link":   t.get("url", ""),
                    "para":   ", ".join(a.get("username") or a.get("email", "")
                                        for a in t.get("assignees", [])),
                })
        except Exception as e:
            log.warning(f"⚠️ No se pudo leer la lista '{etiqueta}': {e}")

    encontradas.sort(key=lambda t: t["vence"] or "9999-12-31")
    return encontradas


def listar_equipo() -> str:
    """A quién se le puede asignar. Para cuando el nombre dictado no resuelve."""
    return "\n".join(f"• {p['nombre']} ({p['email']})" for p in EQUIPO.values())
