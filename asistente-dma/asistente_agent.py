"""
DMA Chief of Staff — el cerebro del asistente ejecutivo

Por qué este módulo existe aparte de `claude_agent.py`:

`claude_agent.py` responde con prompt-y-respuesta y decide qué hacer con ~25
funciones `detect_*` escritas a mano. `handle_admin_command` (server.py) es una
cadena if/elif de comandos literales: "status", "pausa Carlos", "link 70".

Eso no puede servir para notas de voz. Nadie dicta "pausa Carlos" con la sintaxis
exacta; dicta *"oye, agéndame mañana a las 4 con Patricio y recuérdame llamar al
proveedor el viernes"* — dos intenciones, en desorden, con fechas relativas.

Ese es exactamente el problema que resuelve el tool-calling de la API de Claude.
Aquí hay un solo loop y una sola lista de herramientas: agregar una capacidad
nueva es agregar una entrada a TOOLS y una rama al dispatcher, no otro detect_*.
"""
from __future__ import annotations

import datetime
import json
import logging
import os

import anthropic
import pytz

import google_client as gcal
import panorama as pano

log = logging.getLogger("dma-asistente")

TZ_EC = pytz.timezone("America/Guayaquil")

MODEL = os.getenv("ASISTENTE_MODEL", "claude-sonnet-5")
MAX_VUELTAS = 8   # tope duro del loop: sin esto, un error repetido gira sin fin.

# Misma convención que claude_agent.py: la key vive en config.ANTHROPIC_KEY.
# El fallback a la variable de entorno permite importar este módulo suelto
# (para pruebas) sin arrastrar todo config.py.
try:
    from config import ANTHROPIC_KEY
except ImportError:
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY") or os.getenv("ANTHROPIC_API_KEY", "")

_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)


# ── System prompt ─────────────────────────────────────────────────────────────

def _system_prompt() -> str:
    ahora = datetime.datetime.now(TZ_EC)
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    return f"""Eres el Jefe de Gabinete de Dayana Calderón Brunetti, directora de
Design Modeling Academy (DMA), academia online de BIM, estructuras e IA para
ingenieros y arquitectos, con sede en Quito, Ecuador.

No eres un bot de atención al cliente. Trabajas PARA ella, no para sus clientes.
Ella te manda notas de voz mientras maneja, entre clases o saliendo de una
reunión. Tu trabajo es que nada se le caiga.

## AHORA MISMO
Es {dias[ahora.weekday()]} {ahora.strftime('%d/%m/%Y')}, {ahora.strftime('%H:%M')} en Ecuador (America/Guayaquil).
Usa esta fecha para resolver "mañana", "el viernes", "la próxima semana".
Nunca preguntes qué día es hoy.

## CÓMO TE HABLA
Te llegan transcripciones de audio. Vienen con errores: nombres mal escritos,
puntuación rara, frases cortadas. Interpreta la intención, no la letra.
Si dice "agéndame con patricio" y en DMA hay un Patricio, es él.
Una sola nota de voz puede traer VARIAS órdenes. Ejecútalas TODAS.

## CÓMO RESPONDES
Por WhatsApp. Corto y en seco:
- Confirma lo hecho en una línea por cosa: "✅ Agendado: Patricio, mañana 16:00."
- Sin preámbulos, sin "¡Claro que sí!", sin ofrecer ayuda extra al final.
- Español de Ecuador, tuteo. NUNCA voseo rioplatense: es "tienes", no "tenés";
  "puedes", no "podés"; "quieres", no "querés".
- Negrita de WhatsApp con *un asterisco*, nunca **dos**.

## AUTONOMÍA — la regla que no se rompe
Lo REVERSIBLE lo haces directo, sin preguntar: agendar, mover algo suyo, crear
tareas, tomar notas, leer cualquier cosa. Que te pida permiso para agendar sería
inútil.

Lo IRREVERSIBLE o lo que sale HACIA AFUERA se confirma ANTES: escribirle a un
lead o alumno, mover una oportunidad en el CRM, cualquier cosa con dinero.
Esas herramientas tienen un parámetro `confirmado`. La primera vez llámalas con
`confirmado: false`, muéstrale a Dayana exactamente qué se va a enviar y a quién,
y espera su "sí". Solo entonces vuelve a llamar con `confirmado: true`.

Una transcripción mal entendida que agenda algo se corrige en 5 segundos.
Una que le escribe a un cliente equivocado, no.

## LO QUE NO HACES
- No inventas datos. Si una herramienta falla, dilo: "No pude leer GHL".
- No cotizas ni negocias el Máster: eso es del bot de ventas, no tuyo.
- Si algo es ambiguo y es irreversible, pregunta. Si es reversible, elige la
  interpretación más probable, hazlo y dile cuál elegiste.

## CONTEXTO DEL NEGOCIO
Producto ancla: Máster Internacional en BIM Management e IA ($2,699.99 USD).
Equipo: Patricio (contenido/marketing), Ester Álvarez, Gabriel Pantoja,
Eber Martínez (Uruguay), Lisette (soporte técnico).
El CRM es GoHighLevel. Los anuncios son Meta Ads."""


# ── Herramientas ──────────────────────────────────────────────────────────────

TOOLS = [
    # ── Agenda ──
    {
        "name": "ver_agenda",
        "description": (
            "Consulta la agenda de Dayana. Úsalo para '¿qué tengo hoy?', "
            "'¿estoy libre el jueves?', '¿a qué hora es la reunión?'. "
            "Solo lee los calendarios reales de trabajo y familia; los ~90 "
            "calendarios de Google Classroom quedan fuera a propósito."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "desde": {"type": "string", "description": "Fecha inicial YYYY-MM-DD. Por defecto hoy."},
                "dias":  {"type": "integer", "description": "Cuántos días mirar desde esa fecha. Por defecto 1."},
            },
        },
    },
    {
        "name": "crear_evento",
        "description": (
            "Agenda un evento en el calendario de Dayana. Acción reversible: "
            "hazlo directo, sin pedir permiso. Si ella no dice cuánto dura, "
            "asume 1 hora."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo":      {"type": "string", "description": "Título del evento, claro y corto."},
                "inicio":      {"type": "string", "description": "Inicio en ISO 8601 con offset de Ecuador, ej: 2026-07-28T16:00:00-05:00"},
                "fin":         {"type": "string", "description": "Fin en ISO 8601 con offset. Si no se sabe, inicio + 1 hora."},
                "descripcion": {"type": "string"},
                "ubicacion":   {"type": "string", "description": "Lugar o link de la reunión."},
                "invitados":   {"type": "array", "items": {"type": "string"}, "description": "Correos a invitar. Solo si Dayana los dictó."},
            },
            "required": ["titulo", "inicio", "fin"],
        },
    },
    {
        "name": "mover_evento",
        "description": "Cambia la hora de un evento existente. Busca primero con ver_agenda para obtener su id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id":    {"type": "string"},
                "calendar_id": {"type": "string", "description": "El calendar_id que devolvió ver_agenda."},
                "inicio":      {"type": "string", "description": "Nuevo inicio ISO 8601 con offset."},
                "fin":         {"type": "string", "description": "Nuevo fin ISO 8601 con offset."},
            },
            "required": ["event_id", "inicio", "fin"],
        },
    },
    {
        "name": "buscar_hueco",
        "description": (
            "Encuentra huecos libres para una reunión. Úsalo cuando diga "
            "'búscame un espacio', 'cuándo puedo', 'agéndalo cuando esté libre'. "
            "Respeta horario laboral y salta fines de semana."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "duracion_min":  {"type": "integer", "description": "Duración en minutos. Por defecto 60."},
                "dentro_de_dias": {"type": "integer", "description": "Ventana de búsqueda en días. Por defecto 7."},
            },
        },
    },

    # ── Tareas y notas ──
    {
        "name": "crear_tarea",
        "description": (
            "Crea una tarea en Google Tasks. Para 'recuérdame…', 'anota que tengo "
            "que…', 'no me dejes olvidar…'. Reversible: hazlo directo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {"type": "string", "description": "Qué hay que hacer, en imperativo. Ej: 'Llamar al proveedor de hosting'."},
                "vence":  {"type": "string", "description": "Fecha límite YYYY-MM-DD. Omite si no la dijo."},
                "notas":  {"type": "string", "description": "Detalle extra que haya dictado."},
            },
            "required": ["titulo"],
        },
    },
    {
        "name": "ver_tareas",
        "description": "Lista las tareas pendientes de Dayana, las vencidas primero.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "completar_tarea",
        "description": "Marca una tarea como hecha. Usa ver_tareas antes para obtener el id.",
        "input_schema": {
            "type": "object",
            "properties": {"task_id": {"type": "string"}},
            "required": ["task_id"],
        },
    },
    {
        "name": "crear_nota",
        "description": (
            "Guarda una nota como Google Doc. Para cuando dicta una idea larga, "
            "las conclusiones de una reunión o un borrador. Transcribe la idea "
            "completa y ordenada, no un resumen de una línea."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo":    {"type": "string", "description": "Título descriptivo con fecha si aplica."},
                "contenido": {"type": "string", "description": "El contenido de la nota, ya ordenado y legible."},
            },
            "required": ["titulo", "contenido"],
        },
    },
    {
        "name": "buscar_nota",
        "description": "Busca entre las notas guardadas por texto.",
        "input_schema": {
            "type": "object",
            "properties": {"texto": {"type": "string"}},
            "required": ["texto"],
        },
    },

    # ── Panorama ──
    {
        "name": "panorama_empresa",
        "description": (
            "El estado de la empresa. Pide SOLO las secciones que la pregunta "
            "necesita — cada sección cuesta una consulta a un sistema distinto. "
            "'¿cómo vamos?' → comercial. '¿cómo van los anuncios?' → ads."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "secciones": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["agenda", "tareas", "comercial", "ads", "academico"]},
                    "description": "Secciones a incluir. Omite para traer todo (es caro).",
                },
            },
        },
    },
    {
        "name": "buscar_contacto",
        "description": (
            "Busca una persona en GoHighLevel por nombre y devuelve su estado: "
            "etiquetas, oportunidad, última conversación."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"nombre": {"type": "string"}},
            "required": ["nombre"],
        },
    },

    # ── Acción hacia afuera (requiere confirmación) ──
    {
        "name": "enviar_mensaje_a_contacto",
        "description": (
            "Envía un WhatsApp a un contacto de GHL a nombre de DMA. "
            "IRREVERSIBLE: llama primero con confirmado=false para que Dayana "
            "vea el texto exacto y el destinatario. Solo con su 'sí' explícito "
            "vuelve a llamar con confirmado=true."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre":     {"type": "string", "description": "Nombre del contacto en GHL."},
                "mensaje":    {"type": "string", "description": "Texto exacto a enviar."},
                "confirmado": {"type": "boolean", "description": "false para previsualizar, true solo tras el OK de Dayana."},
            },
            "required": ["nombre", "mensaje", "confirmado"],
        },
    },
]


# ── Dispatcher ────────────────────────────────────────────────────────────────

def _ahora() -> datetime.datetime:
    return datetime.datetime.now(TZ_EC)


def _parse_dia(fecha: str) -> datetime.datetime:
    base = _ahora().replace(hour=0, minute=0, second=0, microsecond=0)
    if not fecha:
        return base
    try:
        d = datetime.date.fromisoformat(fecha[:10])
        return TZ_EC.localize(datetime.datetime(d.year, d.month, d.day))
    except ValueError:
        return base


def ejecutar_tool(nombre: str, args: dict) -> str:
    """
    Ejecuta una herramienta y devuelve texto para el modelo.

    Nunca lanza: un fallo se devuelve como texto para que el agente pueda
    contárselo a Dayana en vez de romper la conversación entera.
    """
    try:
        # ── Agenda ──
        if nombre == "ver_agenda":
            desde = _parse_dia(args.get("desde", ""))
            dias = max(1, int(args.get("dias", 1)))
            eventos = gcal.listar_agenda(desde, desde + datetime.timedelta(days=dias))
            if not eventos:
                return "Sin eventos en ese rango."
            return json.dumps(eventos, ensure_ascii=False)

        if nombre == "crear_evento":
            ev = gcal.crear_evento(
                titulo=args["titulo"],
                inicio_iso=args["inicio"],
                fin_iso=args["fin"],
                descripcion=args.get("descripcion", ""),
                ubicacion=args.get("ubicacion", ""),
                invitados=args.get("invitados") or None,
            )
            return f"Evento creado: {ev['titulo']} — {ev['link']}"

        if nombre == "mover_evento":
            ev = gcal.mover_evento(
                event_id=args["event_id"],
                inicio_iso=args["inicio"],
                fin_iso=args["fin"],
                calendar_id=args.get("calendar_id", ""),
            )
            return f"Evento movido: {ev['titulo']}"

        if nombre == "buscar_hueco":
            dur = int(args.get("duracion_min", 60))
            dias = int(args.get("dentro_de_dias", 7))
            desde = _ahora() + datetime.timedelta(hours=1)
            huecos = gcal.buscar_hueco(dur, desde, desde + datetime.timedelta(days=dias))
            return json.dumps(huecos) if huecos else "No hay huecos libres en esa ventana."

        # ── Tareas y notas ──
        if nombre == "crear_tarea":
            t = gcal.crear_tarea(args["titulo"], args.get("notas", ""), args.get("vence", ""))
            return f"Tarea creada: {t['titulo']}" + (f" (vence {t['vence']})" if t["vence"] else "")

        if nombre == "ver_tareas":
            tareas = gcal.listar_tareas()
            return json.dumps(tareas, ensure_ascii=False) if tareas else "Sin tareas pendientes."

        if nombre == "completar_tarea":
            t = gcal.completar_tarea(args["task_id"])
            return f"Tarea completada: {t['titulo']}"

        if nombre == "crear_nota":
            n = gcal.crear_nota(args["titulo"], args["contenido"])
            return f"Nota guardada: {n['titulo']} — {n['link']}"

        if nombre == "buscar_nota":
            notas = gcal.buscar_notas(args["texto"])
            return json.dumps(notas, ensure_ascii=False) if notas else "No encontré notas con ese texto."

        # ── Panorama ──
        if nombre == "panorama_empresa":
            return pano.panorama(args.get("secciones") or None)

        if nombre == "buscar_contacto":
            import ghl_client as ghl
            c = ghl.search_contact_by_name(args["nombre"])
            if not c or not c.get("id"):
                return f"No encontré a '{args['nombre']}' en GHL."
            cid = c["id"]
            resumen = {
                "id":       cid,
                "nombre":   f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                "telefono": c.get("phone", ""),
                "email":    c.get("email", ""),
                "tags":     c.get("tags", []),
            }
            try:
                op = ghl.get_opportunity_by_contact(cid)
                if op:
                    resumen["oportunidad"] = {
                        "nombre": op.get("name", ""),
                        "etapa":  op.get("pipelineStageId", ""),
                        "valor":  op.get("monetaryValue", 0),
                    }
            except Exception:
                pass
            return json.dumps(resumen, ensure_ascii=False)

        # ── Irreversible ──
        if nombre == "enviar_mensaje_a_contacto":
            destino = args["nombre"]
            texto = args["mensaje"]

            # La previsualización se resuelve ANTES de tocar GHL: pedir
            # confirmación nunca debe poder fallar por un problema del CRM.
            if not args.get("confirmado"):
                return (
                    "PENDIENTE DE CONFIRMACIÓN — no se envió nada todavía. "
                    f"Muéstrale a Dayana que se enviaría a '{destino}' el texto: "
                    f"\"{texto}\" y pídele que confirme."
                )

            import ghl_client as ghl
            c = ghl.search_contact_by_name(destino)
            if not c or not c.get("id"):
                return f"No encontré a '{destino}' en GHL. No se envió nada."
            cid = c["id"]
            conv_id = ghl.get_conversation_by_contact(cid)
            if not conv_id:
                return f"'{destino}' no tiene conversación activa en GHL. No se envió nada."
            ghl.send_message(conv_id, texto, contact_id=cid)
            log.info(f"📤 Asistente envió mensaje a {destino}: {texto[:60]}")
            return f"Mensaje enviado a {c.get('firstName', destino)}."

        return f"Herramienta desconocida: {nombre}"

    except Exception as e:
        log.error(f"❌ Tool '{nombre}' falló: {e}")
        return f"ERROR ejecutando {nombre}: {e}"


# ── Loop del agente ───────────────────────────────────────────────────────────

def responder(texto: str, historial: list[dict] | None = None) -> tuple[str, list[dict]]:
    """
    Procesa un mensaje de Dayana (texto ya transcrito si venía en audio).

    Devuelve (respuesta_para_whatsapp, historial_actualizado). El historial se
    devuelve para que quien llame lo guarde y lo reinyecte en el siguiente turno
    — así "sí, mándalo" sabe a qué se refiere.
    """
    mensajes: list[dict] = list(historial or [])
    mensajes.append({"role": "user", "content": texto})

    for vuelta in range(MAX_VUELTAS):
        resp = _client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=_system_prompt(),
            tools=TOOLS,
            messages=mensajes,
        )
        mensajes.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            texto_final = "".join(b.text for b in resp.content if b.type == "text").strip()
            return texto_final or "Listo.", mensajes

        resultados = []
        for bloque in resp.content:
            if bloque.type != "tool_use":
                continue
            log.info(f"🔧 {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)[:120]})")
            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,
                "content": ejecutar_tool(bloque.name, bloque.input),
            })
        mensajes.append({"role": "user", "content": resultados})

    log.warning(f"⚠️ Loop cortado tras {MAX_VUELTAS} vueltas.")
    return ("Me enredé procesando eso y preferí parar antes de hacer algo a medias. "
            "¿Me lo dices de nuevo, más corto?"), mensajes
