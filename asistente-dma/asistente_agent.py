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

# El proveedor se elige igual que en claude_agent.py. Esto NO es opcional:
# si el bot corre con MODEL_PROVIDER=openrouter y el asistente llamara a
# Anthropic por su cuenta, usaría una cuenta distinta de la que paga el resto
# del bot — que fue exactamente el fallo de la primera versión.
#
# El adaptador de OpenRouter traduce tool use en ambos sentidos; sin eso el
# asistente no podría agendar ni crear tareas, solo conversar.
try:
    from config import ANTHROPIC_KEY
except ImportError:
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY") or os.getenv("ANTHROPIC_API_KEY", "")

PROVIDER = os.getenv("MODEL_PROVIDER", "anthropic").lower()

if PROVIDER == "openrouter":
    from openrouter_adapter import OpenRouterClient
    _client = OpenRouterClient()
    log.info(f"🧠 Asistente vía OpenRouter (modelo solicitado: {MODEL})")
else:
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

## CORREO — la superficie más delicada que tocas
Leer y buscar en su Gmail es reversible: hazlo directo.
Escribir NO. Ante la duda, `guardar_borrador`: queda listo en Gmail y ella lo
revisa. `enviar_correo` solo cuando pida explícitamente mandarlo, y aun así
primero con `confirmado: false` para que vea el texto exacto.
Un WhatsApp mal mandado se explica. Un correo mal mandado queda por escrito.

## REUNIONES
Fathom graba y resume sola sus reuniones de Zoom, Google Meet y Teams. Tú no
entras a ninguna reunión: lees lo que Fathom ya dejó hecho.
Si te pide las tareas de una reunión, saca el resumen y ofrécele pasarlas al
equipo con `crear_tarea_equipo` — pero pregunta a quién antes de asignar nada.

## DÓNDE VA CADA TAREA
Es la confusión más fácil de cometer, así que no la cometas:
- Tarea **de Dayana** → `crear_tarea` (Google Tasks, se sincroniza con su móvil).
- Tarea **para otra persona** → `crear_tarea_equipo` (ClickUp, donde trabaja el equipo).
Si dice "recuérdame" es de ella. Si dice un nombre, es para esa persona.

## CUANDO PREGUNTA POR DINERO
Hay dos fuentes y NO miden lo mismo. Preséntalas separadas, nunca sumadas:
- **Stripe** = dinero cobrado de verdad, con monto y fecha exactos.
- **CRM** = inscripciones que el equipo confirmó, incluidas las transferencias
  y los pagos en efectivo, que Stripe no ve.
Si Stripe dice 2 y el CRM dice 5, no te lo inventes ni lo cuadres: son 3 pagos
que entraron por fuera de Stripe. Dilo así.
Nunca des una cifra de facturación que no venga de una herramienta.

## CUANDO PREGUNTA POR CONTENIDO O POR PAUTA
Tienes la matriz: 148 reels reales con su eje y sus métricas, y 44 piezas ya
guionadas. Tres reglas al usarla:

1. **Mira lo que ya está escrito ANTES de proponer algo nuevo.** Si pide ideas
   de carrusel, `guiones_disponibles` primero. Inventar una pieza cuando ya hay
   doce escritas le hace perder el trabajo hecho.
2. **El alcance no es la venta.** La cuenta se viraliza con OBRA —construcción,
   humor de campo— que se lleva casi todo el alcance y trae público que mira
   pero no compra. Lo que vende el Máster es el NÚCLEO: BIM, modelado,
   coordinación, IA aplicada. Cuando te pregunte si algo funcionó, di las dos
   cosas: cuánto alcance tuvo Y de qué eje era.
3. **Nunca des una métrica de memoria.** Sale de `consultar_matriz` o no sale.

Para pauta, `retorno_real` cruza lo cobrado contra lo gastado. Ojo con la
diferencia: `ventas_resumen` dice cuánto entró; `retorno_real` dice contra qué.
Las reservas de ~$100 del Máster son anticipo, no venta cerrada: van aparte.
Y nunca sumes Stripe con el CRM — es la misma venta contada dos veces.

## CONTEXTO DEL NEGOCIO
Producto ancla: Máster Internacional en BIM Management e IA ($2,699.99 USD).
El CRM es GoHighLevel. Los anuncios son Meta Ads. El equipo trabaja en ClickUp.

Equipo (así los nombra ella, así los reconoces):
- Ester Álvarez — asistencia general y soporte al cliente
- Patricio Stagno — contenido y producción audiovisual
- Gabriel Pantoja — GoHighLevel y configuración técnica
- Aylin Tapia — redes sociales
- Eber Martínez — cursos y especializaciones (Uruguay)
- Lisette — soporte técnico (no está en ClickUp)"""


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
                "invitados":   {"type": "array", "items": {"type": "string"}, "description": "A quién invitar. Puedes poner el NOMBRE tal como se dictó ('Ester', 'Patricio') — el correo se resuelve solo desde el equipo. Solo si Dayana los mencionó."},
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

    # ── Tareas del equipo (ClickUp) ──
    {
        "name": "crear_tarea_equipo",
        "description": (
            "Crea una tarea en ClickUp y se la asigna a alguien del EQUIPO. "
            "Úsalo cuando la tarea es para OTRA persona: 'créale una tarea a "
            "Ester', 'que Patricio grabe el reel', 'asígnale esto a Gabriel'. "
            "Para tareas de la propia Dayana usa crear_tarea (Google Tasks). "
            "Equipo: Dayana, Ester, Gabriel, Eber, Patricio, Aylin. "
            "Reversible: hazlo directo, sin pedir permiso."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo":      {"type": "string", "description": "Qué hay que hacer, en imperativo."},
                "para":        {"type": "string", "description": "Nombre o correo de la persona. Acepta el nombre tal como se dictó."},
                "descripcion": {"type": "string", "description": "Detalle o contexto que haya dictado."},
                "vence":       {"type": "string", "description": "Fecha límite YYYY-MM-DD."},
                "prioridad":   {"type": "string", "enum": ["urgente", "alta", "normal", "baja"]},
                "lista":       {"type": "string", "description": "Lista de ClickUp. Omítela y se elige la del área de esa persona."},
            },
            "required": ["titulo", "para"],
        },
    },
    {
        "name": "ver_tareas_equipo",
        "description": (
            "Consulta las tareas de ClickUp de alguien del equipo. Para "
            "'¿qué tiene pendiente Ester?', '¿en qué va Patricio?'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "quien": {"type": "string", "description": "Nombre o correo. Omítelo para ver las de todos."},
            },
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

    # ── Ventas y dinero ──
    {
        "name": "ventas_resumen",
        "description": (
            "Cuánto se cobró y cuántos se inscribieron en un periodo. Úsalo para "
            "'¿cuántas ventas hicimos hoy?', '¿cuánto facturamos esta semana?', "
            "'¿cómo va el mes?'. Devuelve DOS fuentes separadas: Stripe (dinero "
            "cobrado de verdad) y el CRM (inscripciones, que incluyen "
            "transferencias). No las sumes ni las presentes como una sola cifra: "
            "si no coinciden es porque miden cosas distintas."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "periodo": {
                    "type": "string",
                    "description": ("Como lo dijo ella: 'hoy', 'ayer', 'esta semana', "
                                    "'semana pasada', 'este mes', 'mes pasado', "
                                    "'últimos 7 días', o una fecha 'AAAA-MM-DD'."),
                },
            },
        },
    },
    {
        "name": "ingresos_por_cliente",
        "description": (
            "Cuánto pagó CADA cliente en un periodo, de mayor a menor, juntando "
            "las cuotas de una misma persona. Para '¿cuánto me ha pagado cada "
            "cliente esta semana?'. Solo ve Stripe."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "periodo": {"type": "string", "description": "Igual que en ventas_resumen. Por defecto 'semana'."},
            },
        },
    },
    {
        "name": "ventas_por_dia",
        "description": (
            "Serie diaria de cobros, para ver la tendencia: qué días entra dinero "
            "y qué días no. Para 'dame las ventas día por día' o '¿cómo viene la "
            "semana?'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dias": {"type": "integer", "description": "Cuántos días hacia atrás, contando hoy. Por defecto 7."},
            },
        },
    },
    {
        "name": "progreso_alumno",
        "description": (
            "Cuánto ha avanzado un alumno en su curso: porcentaje, fecha de "
            "inicio, último acceso y número de sesiones. Para '¿cómo va Fulano "
            "en el máster?' o '¿ha entrado a la plataforma?'. Sale del último "
            "snapshot académico, no es tiempo real."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string", "description": "Nombre del alumno."},
                "email":  {"type": "string", "description": "Su correo, si lo sabes (más fiable)."},
            },
        },
    },

    # ── Correo ──
    {
        "name": "buscar_correos",
        "description": (
            "Busca en el Gmail de Dayana con la sintaxis de Gmail y devuelve "
            "remitente, asunto y un resumen de cada uno, con su id. Ejemplos de "
            "consulta: 'is:unread', 'from:ester', 'newer_than:2d', "
            "'has:attachment', 'is:unread newer_than:1d'. Para '¿qué correos "
            "tengo?' usa 'is:unread'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "consulta": {"type": "string", "description": "Consulta en sintaxis de Gmail."},
                "limite":   {"type": "integer", "description": "Cuántos traer, máximo 25. Por defecto 10."},
            },
        },
    },
    {
        "name": "leer_correo",
        "description": (
            "Abre un correo entero por su id y devuelve cabeceras y texto. "
            "El id sale de buscar_correos — llama a esa primero."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"mensaje_id": {"type": "string"}},
            "required": ["mensaje_id"],
        },
    },
    {
        "name": "guardar_borrador",
        "description": (
            "Escribe el correo y lo deja en Borradores SIN enviarlo. Reversible: "
            "no pide confirmación. Es lo que hay que usar cuando ella dice "
            "'prepárame una respuesta' o cuando no está claro si quiere mandarlo ya."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "para":           {"type": "string", "description": "Destinatario. Puede ir vacío si es respuesta."},
                "asunto":         {"type": "string"},
                "texto":          {"type": "string", "description": "Cuerpo del correo."},
                "responder_a_id": {"type": "string", "description": "Id del correo al que responde, para que quede en el mismo hilo."},
            },
            "required": ["texto"],
        },
    },
    {
        "name": "enviar_correo",
        "description": (
            "Envía un correo de verdad, a nombre de Dayana. IRREVERSIBLE y sale "
            "hacia afuera: llama primero con confirmado=false para que ella vea "
            "destinatario, asunto y texto exactos, y solo con su 'sí' explícito "
            "vuelve a llamar con confirmado=true. Si dudas entre esto y un "
            "borrador, haz el borrador."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "para":           {"type": "string", "description": "Destinatario. Vacío si es respuesta y sale del original."},
                "asunto":         {"type": "string"},
                "texto":          {"type": "string"},
                "responder_a_id": {"type": "string", "description": "Id del correo al que responde."},
                "confirmado":     {"type": "boolean", "description": "false para previsualizar, true solo tras el OK de Dayana."},
            },
            "required": ["texto", "confirmado"],
        },
    },

    # ── Reuniones ──
    {
        "name": "ultimas_reuniones",
        "description": (
            "Lista las reuniones que grabó Fathom (Zoom, Google Meet y Teams): "
            "título, fecha, con quién y el enlace. Para '¿qué reuniones tuve "
            "esta semana?'. No trae el resumen — para eso usa resumen_reunion."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dias":   {"type": "integer", "description": "Hacia atrás. Por defecto 7."},
                "limite": {"type": "integer", "description": "Cuántas. Por defecto 10."},
            },
        },
    },
    {
        "name": "resumen_reunion",
        "description": (
            "El resumen de una reunión y las tareas que salieron de ella. "
            "'busqueda' es lo que ella diría: el nombre de alguien que estuvo, "
            "un trozo del título, o vacío para la última. Si salen varias "
            "candidatas te las devuelve para que preguntes cuál — no elijas al "
            "azar. Las tareas que devuelve se pueden pasar al equipo con "
            "crear_tarea_equipo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "busqueda": {"type": "string", "description": "Persona, título o fecha. Vacío = la última."},
                "dias":     {"type": "integer", "description": "Ventana de búsqueda hacia atrás. Por defecto 14."},
            },
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

    # ── Marketing y contenido ──
    {
        "name": "consultar_matriz",
        "description": (
            "La matriz de contenido: 148 reels reales con sus métricas y su eje. "
            "Con que='diagnostico' dice qué eje se lleva el alcance y cuál se "
            "lleva la venta — para '¿cómo va mi contenido?'. Con que='mejores' "
            "trae las piezas que más rindieron con su hook — para '¿qué reel "
            "funcionó mejor?' o '¿qué me conviene repetir?'. Es la misma fuente "
            "que ve Patricio, así que nunca se contradicen."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "que":     {"type": "string", "enum": ["diagnostico", "mejores"],
                            "description": "diagnostico = el reparto por eje. mejores = el top de piezas."},
                "cuantas": {"type": "integer", "description": "Cuántas piezas traer si que='mejores'. Por defecto 5."},
                "eje":     {"type": "string", "description": "Filtrar por eje: NÚCLEO-IA, NÚCLEO-BIM, OBRA, PROMO, COMUNIDAD."},
            },
        },
    },
    {
        "name": "guiones_disponibles",
        "description": (
            "Qué contenido ya está escrito y esperando publicación: 44 piezas "
            "con hook, slides, caption y CTA por red. Para '¿qué toca publicar?', "
            "'¿tengo algo de carrusel?' o '¿qué hay listo de IA?'. SIEMPRE mira "
            "aquí antes de proponer contenido nuevo — puede que ya esté escrito."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "formato": {"type": "string", "description": "carrusel, reel, post, blog, anuncio, historia o youtube."},
                "eje":     {"type": "string", "description": "NÚCLEO-IA, NÚCLEO-BIM, OBRA, PROMO o COMUNIDAD."},
            },
        },
    },
    {
        "name": "ver_guion",
        "description": (
            "Trae un guion completo por su id: hook, slides una por una, caption "
            "y la CTA de cada red. Para 'pásame el guion de X'. Si no sabes el id, "
            "llama antes a guiones_disponibles."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "El id del guion, o parte de su título."},
            },
            "required": ["id"],
        },
    },
    {
        "name": "retorno_real",
        "description": (
            "Cruza lo COBRADO en Stripe contra lo GASTADO en pauta, y dice "
            "cuánto volvió por cada dólar. Para '¿la pauta se paga sola?', "
            "'¿cuánto volvió este mes?' o '¿vale la pena la campaña?'. Separa "
            "las reservas de ~$100 del Máster, que son anticipo y no venta "
            "cerrada. Distinto de ventas_resumen: aquel dice cuánto entró, "
            "este dice contra qué."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dias": {"type": "integer", "description": "Ventana hacia atrás. Por defecto 30, máximo 90."},
            },
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


def _resolver_invitados(invitados) -> tuple[list, list]:
    """
    'Ester' → 'asistencia.generaldg@gmail.com'.

    El modelo recibe nombres dictados, no correos: nadie dice "agéndame con
    asistencia.generaldg arroba gmail". Sin esta resolución, Google rechaza el
    invitado y el evento entero falla con "correo no válido" — que es justo lo
    que pasó la primera vez que Dayana dictó "agéndame con Ester".

    Los correos del equipo ya están en clickup_client.EQUIPO, así que se
    reutilizan en vez de mantener una segunda lista que se desincronice.

    Devuelve (correos_resueltos, nombres_sin_correo). Un nombre desconocido NO
    tumba el evento: se agenda igual y se avisa a quién no se pudo invitar.
    """
    correos, desconocidos = [], []
    for quien in (invitados or []):
        q = (quien or "").strip()
        if not q:
            continue
        if "@" in q:                      # ya es un correo
            correos.append(q)
            continue
        try:
            import clickup_client as cu
            persona = cu.resolver_persona(q)
        except Exception:
            persona = None
        if persona and persona.get("email"):
            correos.append(persona["email"])
        else:
            desconocidos.append(q)
    return correos, desconocidos


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
            invitados, sin_correo = _resolver_invitados(args.get("invitados"))
            ev = gcal.crear_evento(
                titulo=args["titulo"],
                inicio_iso=args["inicio"],
                fin_iso=args["fin"],
                descripcion=args.get("descripcion", ""),
                ubicacion=args.get("ubicacion", ""),
                invitados=invitados or None,
            )
            resp = f"Evento creado: {ev['titulo']} — {ev['link']}"
            if invitados:
                resp += f" (invitados: {', '.join(invitados)})"
            if sin_correo:
                # El evento SÍ se creó. Se avisa de a quién no se pudo invitar,
                # en vez de fallar entero: agendar es lo que ella pidió.
                resp += (f". No se pudo invitar a {', '.join(sin_correo)} — "
                         f"no tengo su correo, pero el evento quedó agendado.")
            return resp

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

        # ── Tareas del equipo (ClickUp) ──
        if nombre == "crear_tarea_equipo":
            import clickup_client as cu
            persona = cu.resolver_persona(args["para"])
            if not persona:
                return (f"No reconocí a '{args['para']}' en el equipo. "
                        f"Estas son las personas disponibles:\n{cu.listar_equipo()}")
            t = cu.crear_tarea(
                titulo=args["titulo"],
                para=args["para"],
                descripcion=args.get("descripcion", ""),
                vence=args.get("vence", ""),
                prioridad=args.get("prioridad", ""),
                lista=args.get("lista", ""),
            )
            venc = f", vence {t['vence']}" if t["vence"] else ""
            return (f"Tarea creada para {t['para']} en la lista '{t['lista']}'{venc}: "
                    f"{t['titulo']} — {t['link']}")

        if nombre == "ver_tareas_equipo":
            import clickup_client as cu
            tareas = cu.tareas_de(args.get("quien", ""))
            if not tareas:
                return "Sin tareas abiertas para esa persona."
            return json.dumps(tareas[:25], ensure_ascii=False)

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

        # ── Ventas ──
        if nombre == "ventas_resumen":
            import ventas
            return ventas.resumen_ventas(args.get("periodo") or "hoy")

        if nombre == "ingresos_por_cliente":
            import ventas
            return ventas.ingresos_por_cliente(args.get("periodo") or "semana")

        if nombre == "ventas_por_dia":
            import ventas
            return ventas.ventas_por_dia(args.get("dias") or 7)

        if nombre == "progreso_alumno":
            import academico_progreso as acp
            info = acp.get_alumno_progress(email=args.get("email", ""),
                                           nombre=args.get("nombre", ""))
            if not info:
                return ("No encontré a esa persona en el snapshot académico. "
                        "Puede que no esté inscrita o que el snapshot esté viejo.")
            return json.dumps(info, ensure_ascii=False)

        # ── Correo ──
        if nombre == "buscar_correos":
            import gmail_client as gm
            return gm.buscar_correos(args.get("consulta") or "is:unread",
                                     args.get("limite") or 10)

        if nombre == "leer_correo":
            import gmail_client as gm
            return gm.leer_correo(args.get("mensaje_id", ""))

        if nombre == "guardar_borrador":
            import gmail_client as gm
            return gm.guardar_borrador(
                para=args.get("para", ""),
                asunto=args.get("asunto", ""),
                texto=args.get("texto", ""),
                responder_a_id=args.get("responder_a_id", ""),
            )

        if nombre == "enviar_correo":
            import gmail_client as gm
            # La guardia vive aquí además de en el prompt: si el modelo se
            # inventa confirmado=true, esto no lo salva — pero si simplemente
            # lo olvida, sí. Es la misma política que enviar_mensaje_a_contacto.
            return gm.enviar_correo(
                para=args.get("para", ""),
                asunto=args.get("asunto", ""),
                texto=args.get("texto", ""),
                confirmado=bool(args.get("confirmado")),
                responder_a_id=args.get("responder_a_id", ""),
            )

        # ── Reuniones ──
        if nombre == "ultimas_reuniones":
            import fathom_client as fa
            return fa.ultimas_reuniones(args.get("dias") or 7, args.get("limite") or 10)

        if nombre == "resumen_reunion":
            import fathom_client as fa
            return fa.resumen_reunion(args.get("busqueda") or "", args.get("dias") or 14)

        # ── Marketing ──
        if nombre == "consultar_matriz":
            import marketing as mk
            if (args.get("que") or "diagnostico") == "mejores":
                return mk.mejores_piezas(args.get("cuantas") or 5, args.get("eje") or "")
            return mk.diagnostico()

        if nombre == "guiones_disponibles":
            import marketing as mk
            return mk.guiones(args.get("formato") or "", args.get("eje") or "")

        if nombre == "ver_guion":
            import marketing as mk
            return mk.guion(args.get("id") or "")

        if nombre == "retorno_real":
            import marketing as mk
            return mk.retorno_real(args.get("dias") or 30)

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
