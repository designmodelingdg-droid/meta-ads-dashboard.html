#!/usr/bin/env python3
"""Construye calendario-noviembre.json desde las piezas de guiones-completos.json.

    python3 matriz-viral/matriz/calendario-noviembre.py

Igual que octubre: el calendario solo ORDENA piezas; el contenido vive en
guiones-completos.json. Noviembre va del miércoles 28 de octubre (arranque del
workshop y Halloween, «semana 0») al lunes 30 de noviembre (Cyber Monday).
"""
import datetime
import json
import pathlib
from collections import Counter

M = pathlib.Path(__file__).resolve().parent
G = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
WS = "https://funnel.dgdesignmodeling.com/workshop-ia-revit-autodesk-registro"


def etiqueta(f):
    d = datetime.date.fromisoformat(f)
    return f"{DIAS[d.weekday()]} {d.day}" + (" oct" if d.month == 10 else "")


def pieza(pid):
    if pid not in G:
        raise SystemExit(f"FALTA en guiones-completos.json: {pid}")
    return G[pid]


# ───────────────────────── GRUPO 1 · FEED ─────────────────────────
# (fecha, id, intención 50/20/30, producto, CTA, nota)
FEED = [
    ("2026-10-31", "nov-ws-demo-reel", "solución", "Máster · workshop", "Comenta WORKSHOP",
     "Workshop · video 1. Se graba en la sesión de Daniela con Gabriel antes del jue 29-oct (PDF de grabaciones). Sale en el puente de Ecuador (31-oct al 3-nov) y en Halloween: el reel no lleva disfraz, el Halloween va en historias, correo y comunidades."),
    ("2026-11-02", "nov-muertos-habitos-carrusel", "problema", "Máster", "Comenta NIVEL",
     "EFEMÉRIDE: Día de Difuntos (Ecuador, Bolivia y Colombia) y Día de Muertos (México). Acusación con humor técnico."),
    ("2026-11-03", "nov-ws-5-preguntas-carrusel", "solución", "Máster · workshop", "Comenta WORKSHOP",
     "Workshop · carrusel W−14 (lo arma Daniela en la app). 3-nov: Independencia de Cuenca."),
    ("2026-11-04", "nov-chuleta-1-perfiles-acero-reel", "problema", "Acero", "Comenta ACERO",
     "SERIE CHULETA 1/4. El formato que se llevó octubre: 2 reels fuera de matriz = 44 % de las vistas y 71 % de los guardados del mes."),
    ("2026-11-05", "nov-ws-para-quien-reel", "objeción", "Máster · workshop", "Comenta WORKSHOP", "Workshop · video 2 (filtra a quien empieza de cero)."),
    ("2026-11-06", "nov-dato-recubrimiento-post", "problema", "Diplomado · Estructuras", "Comenta ZAPATA",
     "Dato de cálculo verificable (formato que más guarda). Sale con el blog del viernes."),
    ("2026-11-07", "nov-ia-revit-3-pasos-reel", "solución", "Máster · workshop", "Comenta WORKSHOP",
     "REFERENTE: adaptación del reel casi viral de @lexmrbim (98.570 vistas, 3.162 comentarios). Tutorial de 3 pasos con el celular sobre el monitor y recurso por palabra; DMA dice lo que el servidor oficial NO hace."),
    ("2026-11-09", "nov-peru-bim-obligatorio-carrusel", "problema", "Máster", "Comenta NIVEL",
     "TENDENCIA: BIM obligatorio en Perú desde el 14-ago-2026 (MEF). Va también a LinkedIn."),
    ("2026-11-10", "nov-chuleta-2-cerchas-reel", "problema", "Acero · Naves PRO", "Comenta ACERO",
     "SERIE CHULETA 2/4 · EFEMÉRIDE: Día Mundial de la Ciencia (UNESCO)."),
    ("2026-11-12", "nov-calidad-checklist-modelo-carrusel", "solución", "Máster", "Comenta NIVEL", "EFEMÉRIDE: World Quality Day."),
    ("2026-11-13", "nov-obj-master-bloques-post", "objeción", "Máster", "Comenta NIVEL",
     "Dar a conocer el Máster por bloques (Dayana, 23-oct). Sin precio. Sale con el blog del viernes."),
    ("2026-11-14", "nov-gabriel-error-modelos-reel", "problema", "Máster", "Comenta NIVEL", "Gabriel a cámara (más Gabriel, pedido de Dayana)."),
    ("2026-11-16", "nov-ws-horas-parametros-carrusel", "problema", "Máster · workshop", "Comenta WORKSHOP",
     "El día antes del workshop. 16-nov: descanso en México y festivo en Colombia; último día del Buen Fin (13-17)."),
    ("2026-11-17", "nov-chuleta-3-lod-reel", "problema", "Máster", "Comenta WORKSHOP", "SERIE CHULETA 3/4 · DÍA DEL WORKSHOP (8:00 PM Ecuador)."),
    ("2026-11-18", "nov-ws-donde-se-equivoco-carrusel", "solución", "Máster", "Comenta NIVEL", "Resumen del workshop con capturas reales de la grabación."),
    ("2026-11-19", "nov-nave-a-ojo-reel", "problema", "Acero", "Comenta ACERO",
     "REFERENTE: misma mecánica de @lexmrbim aplicada a Acero (3 verificaciones en pantalla y las otras 2 por la palabra)."),
    ("2026-11-20", "nov-acero-modulo-a-modulo-carrusel", "objeción", "Acero", "Comenta ACERO",
     "BLACK FRIDAY ECUADOR (20-nov, feriado). El feed explica el programa sin precio; la oferta va en historias, correo y pauta."),
    ("2026-11-21", "nov-ws-clip-demo-reel", "problema", "Máster", "Comenta NIVEL", "Clip del workshop (W+4)."),
    ("2026-11-23", "nov-master-que-bloque-carrusel", "problema", "Máster", "Comenta NIVEL", "Abre la Black Week. Máster por bloques sin precio."),
    ("2026-11-24", "nov-chuleta-4-uniones-reel", "problema", "Acero", "Comenta ACERO", "SERIE CHULETA 4/4."),
    ("2026-11-25", "nov-gabriel-no-compres-descuento-reel", "objeción", "Acero", "Comenta ACERO", "Gabriel a cámara: honestidad en la Black Week."),
    ("2026-11-27", "nov-bf-incluye-post", "objeción", "Acero · cursos", "Comenta ACERO", "BLACK FRIDAY. Sin precios en el feed: van en DM, correo y anuncio."),
]


def fila_feed(f, pid, intencion, producto, cta, nota):
    p = pieza(pid)
    return {"fecha": etiqueta(f), "fecha_iso": f, "semana": p.get("semana"), "id": pid,
            "titulo": p.get("titulo"), "tipo": p.get("tipo"), "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
            "intencion": intencion, "producto": producto, "cta": cta, "estado": p.get("estado"), "nota": nota}


def filas_de(grupo_prefijo):
    out = []
    for p in G.values():
        if p["id"].startswith("nov-") and str(p.get("grupo", "")).startswith(grupo_prefijo):
            out.append({"fecha": etiqueta(p["fecha_iso"]), "fecha_iso": p["fecha_iso"], "semana": p.get("semana"), "id": p["id"],
                        "titulo": p.get("titulo"), "tipo": p.get("tipo"),
                        "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
                        "idea": {"titulo": p.get("titulo"), "formato": p.get("formato_detalle") or p.get("formato"), "desarrollo": p.get("hook") or ""},
                        **({"cuenta": p["cuenta"]} if p.get("cuenta") else {}),
                        **({"gabriel_a_camara": True} if p.get("gabriel_a_camara") else {}),
                        **({"venta": True} if p.get("venta") else {})})
    return sorted(out, key=lambda x: x["fecha_iso"])


def correos():
    out = []
    for p in G.values():
        if p["id"].startswith("nov-") and p.get("grupo") == "Correos":
            cuerpo = p.get("cuerpo")
            out.append({"fecha": f"{etiqueta(p['fecha_iso'])} · {str(p.get('semana', '')).split(' (')[0]}", "fecha_iso": p["fecha_iso"], "id": p["id"],
                        "nombre": p.get("titulo"), "asunto": p.get("asunto"), "preencabezado": p.get("preencabezado"),
                        "segmento": p.get("segmento"), "objetivo": p.get("hook") or "",
                        "cuerpo": "\n\n".join(cuerpo) if isinstance(cuerpo, list) else (cuerpo or ""), "condicion": p.get("condicion") or ""})
    return sorted(out, key=lambda x: x["fecha_iso"])


def ficha_anuncio(pid, campana):
    p = pieza(pid)
    cfg = [["Botón", p.get("boton", "")], ["Público", p.get("publico_sugerido", "")], ["Qué medir", p.get("que_medir", "")]]
    return {"id": pid, "titulo": p.get("titulo"), "campana": campana,
            "precio": "precio de Black Friday (lo confirma Dayana)" if "Acero" in (p.get("producto") or "") or "Cursos" in (p.get("producto") or "")
            else "sin precio (regla del Máster)",
            "formato": p.get("formato_detalle") or "anuncio", "hook": p.get("hook"), "cuerpo": p.get("texto_principal"),
            "titular": p.get("titular"), "descripcion": p.get("descripcion"), "creativo": p.get("creativo"),
            "prompt": p.get("prompt_imagenes", ""), "cfg": cfg, "condicion": p.get("condicion", "")}


ADS = {
    "WORKSHOP · registro (2 al 16-nov, parte de los 59 USD del plan)": ["nov-ads-ws-demo", "nov-ads-ws-5-preguntas"],
    "ACERO · Black Friday (18 al 30-nov)": ["nov-ads-acero-bf"],
    "CURSOS DE BAJO COSTO · Halloween (30-oct al 1-nov) y Black Week": ["nov-ads-cursos-bf"],
    "MÁSTER · bono de Black Week (23 al 30-nov), sin precio": ["nov-ads-master-bono"],
}

DECISIONES_PAUTA = [
    ["De dónde sale (análisis del 23-oct, Meta 23-sep → 22-oct)",
     "$1.090,76 gastados, 1.097 leads (683 de formulario + 414 de WhatsApp), CPL $0,99. El Máster [29SEP] es el mejor: $0,75 en 30 días y $0,60 en los últimos 7."],
    ["1 · Apagar lo que no trae nada",
     "El conjunto «Resto» de ACERO WSP ($15,83, 0 leads, frecuencia 59,5), las dos campañas LEAD MAGNETS de clics ($59, 0 leads) y ACERO TEST GANCHOS ($1,62)."],
    ["2 · Concentrar el Máster en [29SEP]", "Y reactivar «MÁSTER CITA» ($0,63) solo si GHL confirma que esos leads agendan."],
    ["3 · Workshop: registro del 2 al 16-nov",
     "Hoy no hay ningún anuncio del workshop. Los 59 USD del plan van a quien interactuó con la cuenta: las chuletas de octubre alcanzaron unas 55.000 cuentas (puede contar a la misma persona dos veces). Medir registros reales en GHL el 3 y el 10-nov."],
    ["4 · Black Friday", "Acero y cursos de bajo costo con precio de Black Friday del 18 al 30-nov (acceso anticipado 18-22). Máster: solo el bono, sin precio. Un solo enlace de pago por producto."],
    ["5 · Ecuador y las elecciones", "Concentrar la pauta de Ecuador del 18 al 26 y bajarla del 27 al 29 (silencio electoral y elecciones seccionales del dom 29-nov)."],
    ["REGLA DE ORO", "El Máster no lleva precio en ninguna pieza. Los precios de Black Friday van solo en pauta, correo y DM. La oferta cierra el lun 30-nov a las 23:59 (Ecuador) y NO se reabre."],
]

EFEMERIDES = [
    ["Sáb 31-oct", "Halloween · Día Mundial de las Ciudades (ONU) · inicio del puente en Ecuador (31-oct al 3-nov)", "Halloween flash de cursos de bajo costo (cupón SUSTO)"],
    ["Lun 2-nov", "Día de Difuntos: feriado en Ecuador, Bolivia, Colombia y 9 comunidades de España · Día de Muertos (México, no es feriado de ley)", "Carrusel «Aquí descansan» (acusación con humor técnico)"],
    ["Mar 3-nov", "Independencia de Cuenca (feriado en Ecuador) · Cyber Wow Perú (2-5 nov) · CyberMonday Argentina (2-4 nov)", "Carrusel del workshop"],
    ["Dom 8-nov", "Día Mundial del Urbanismo", "Se cubre el lun 9 con Perú BIM (obra pública)"],
    ["Mar 10-nov", "Día Mundial de la Ciencia (UNESCO)", "Chuleta 2: tipos de cercha"],
    ["Jue 12-nov", "World Quality Day (semana CQI 9-13 nov)", "Carrusel del checklist de calidad del modelo"],
    ["13-17 nov", "Buen Fin en México (termina el día del workshop) · lun 16 descanso en México y festivo en Colombia", "«Tu Buen Fin es gratis: workshop el martes»"],
    ["Lun 16-nov", "Ecuador: pago del décimo tercer sueldo del sector público", "Último empujón del workshop"],
    ["Mar 17-nov", "WORKSHOP · 8:00 PM Ecuador", "Recordatorios ya hechos (PR #137)"],
    ["Vie 20-nov", "Ecuador: día libre (Decreto 507) y Black Friday ecuatoriano, adelantado por las elecciones", "Acceso anticipado: historias y correo solo a Ecuador"],
    ["Lun 23-nov", "Argentina: feriado de la Soberanía Nacional", "Abre la Black Week"],
    ["Jue 26 · Vie 27 · Lun 30-nov", "Thanksgiving · Black Friday (Chile: BF del 27 al 30) · Cyber Monday", "Pico de venta y cierre definitivo el 30 a las 23:59"],
    ["27-29 nov", "Ecuador: silencio electoral; elecciones seccionales el dom 29", "Bajar la pauta en Ecuador"],
]

ESTRATEGIA_COMERCIAL = {
    "nota": "Actualizado el 23-oct (Dayana): las decisiones de precio y de cómo se nombra cada oferta las toma ESTER. Los números de abajo son solo la propuesta de partida. La promo la recibe únicamente quien responde o escribe al WhatsApp: la página vieja no se toca (dejará de servir cuando salga la nueva) y cada oferta tiene su mini landing, que se manda solo por WhatsApp. Principios que siguen: escasez real (fecha y hora de cierre, no se reabre), bonos antes que descuentos grandes en lo caro, el Máster nunca con precio.",
    "reglas": [
        "Ninguna pieza pública (feed, historias, comunidades, LinkedIn, blog, anuncios ni correos) lleva el precio de la oferta ni enlaza la página vieja de pago.",
        "Las piezas dicen que HAY oferta, hasta cuándo y cómo pedirla: responder la historia, escribir la palabra por WhatsApp (SUSTO, LISTA, BLACK) o responder el correo.",
        "Por WhatsApp una persona manda el precio y la mini landing de esa oferta. Una mini landing por oferta (SUSTO · cursos; BLACK · Acero; BLACK · cursos); no se publica ni se enlaza en abierto.",
        "Los anuncios de Halloween y Black Friday llevan el botón «Enviar mensaje» y van a WhatsApp, no a la página.",
        "El Máster no lleva precio en ningún lado: en la Black Week va con bono y se habla en llamada.",
        "Ester decide: el precio final, si el descuento se dice en % o en $, si la mini landing muestra el precio normal tachado, los bonos y si entran los Diplomados.",
    ],
    "ventanas": [
        ["Halloween flash", "vie 30-oct 00:00 → dom 1-nov 23:59 (Ecuador)", "Propuesta: cursos de bajo costo (~$26,99) a $19,99 con el cupón SUSTO", "Historias 31-oct y 1-nov, comunidades 30-oct, correos 30-oct y 1-nov, anuncio corto → todo termina en WhatsApp (SUSTO)"],
        ["Calentamiento + workshop", "2 → 17 nov", "Sin oferta: valor (chuletas, dato, Perú BIM, calidad) y registro al workshop", "Feed, historias, comunidades, correos 2, 10 y 15-nov, pauta de registro"],
        ["Acceso anticipado", "mié 18 → dom 22-nov", "Para registrados al workshop, compradores de cursos y Ecuador (su Black Friday es el 20)", "Historias 18 y 20, correos 18 y 20, comunidades 18 → WhatsApp (LISTA)"],
        ["Black Week", "lun 23 → lun 30-nov 23:59", "Propuesta: Acero con Tutor IA $179 (normal $225) · sin Tutor $159 · pack de 3 cursos de bajo costo $49 · Diplomados −15 a −20 % o bono · Máster: «Bono Black» (Acero con Tutor IA + Naves PRO) al empezar un bloque, solo en llamada", "Historias casi diarias, correos 23, 25, 27 y 30, comunidades 23, 27 y 30, pauta → WhatsApp (BLACK)"],
    ],
    "falta_para_decidir": [
        "Ester: precios finales, bonos y cómo se nombran. Halloween antes del jue 29-oct; Black Friday antes del lun 16-nov.",
        "Ester: las 3 mini landings, los cupones en GHL y el enlace de WhatsApp con cada palabra ya escrita (SUSTO, LISTA, BLACK), que reemplaza los corchetes de las piezas.",
        "Ester y Aylin: las plantillas de respuesta por WhatsApp con el precio y la mini landing de cada oferta.",
        "Dayana: el corte de Stripe y PayPal de noviembre de 2025 (no hay dato del Black Friday pasado; en GHL solo existe el formulario «Registro BlackFriday 2025»).",
    ],
}

# ───────────────────── FORMATOS EN PRUEBA (se revisan cada mes) ─────────────────────
# Cada pieza: id de guiones-completos y, cuando ya salió, su shortCode de Instagram.
# whatsapp_14d y ventas_14d los llena Ester desde GHL a los 14 días de publicada.
FORMATOS_PRUEBA = {
    "nota": "Pedido de Dayana (23-oct): los formatos nuevos se prueban y se revisan cada mes. Un formato entra fijo a la matriz solo si genera las tres cosas: interés, interacción y ventas. Que tenga vistas no basta. Lo calcula scripts/formatos_prueba.py --mes 2026-11 contra la mediana de reels de los 90 días anteriores.",
    "criterios": [
        ["Interés", "Vistas a los 7 días ≥ 1,5 veces la mediana de reels de 90 días", "matriz.json (Graph API, lunes y viernes)"],
        ["Interacción", "(comentarios + guardados + compartidos) por 1.000 vistas ≥ 2 veces la mediana, y comentarios por 1.000 ≥ la mediana", "matriz.json"],
        ["Venta", "≥ 10 personas escriben la palabra o llegan al WhatsApp en 14 días, y al menos 1 venta atribuida a la pieza", "GHL (etiqueta origen-bot-<palabra>) + Ester marca la fuente de la venta"],
    ],
    "decision": [
        "3 de 3 en al menos 2 piezas → entra FIJO a la matriz (mínimo 1 por semana).",
        "2 de 3 → se repite una vez más el mes siguiente con otro tema; si vuelve a quedarse en 2, entra solo como formato de alcance (sin cuota fija).",
        "0 o 1 de 3 en 2 piezas → sale de la matriz.",
        "Nunca se decide con una sola pieza ni con piezas de menos de 7 días.",
    ],
    "formatos": [
        {"formato": "Chuleta visual sin voz (lista que se arma en pantalla)",
         "plantilla": "vimeo-clips/editados/pizarra/ (simbologia-niveles.mp4; variante isométrica: uniones-acero-hormigon.mp4)",
         "estado": "Probado en interés e interacción. Falta probar que vende.",
         "piezas": [{"id": "simbologia-niveles (fuera de matriz)", "shortCode": "DeubXmFlIDE"},
                    {"id": "oct-uniones-acero-hormigon-reel"}, {"id": "nov-chuleta-1-perfiles-acero-reel"},
                    {"id": "nov-chuleta-3-lod-reel"}, {"id": "nov-chuleta-4-uniones-reel"}],
         "que_falta_saber": "Si las vistas y los guardados se convierten en DMs de ACERO y en ventas, o solo en guardados."},
        {"formato": "Pizarra dibujada con voz de Gabriel por IA (estilo 9)",
         "plantilla": "video-recursos/plantillas/pizarra-dibujada",
         "estado": "1 pieza buena (cimentaciones). Falta una segunda pieza y probar venta.",
         "piezas": [{"id": "cimentaciones (fuera de matriz)", "shortCode": "Der2lsgjwu5"},
                    {"id": "oct-ia-reemplazar-ingeniero-reel"}, {"id": "nov-chuleta-2-cerchas-reel"}],
         "que_falta_saber": "«¿La IA te va a reemplazar?» dio 0 comentarios en julio. Esta versión acusa 4 hábitos concretos, que es el patrón que sí funciona. Si no pasa la mediana, la chuleta 2 dice si falló el tema o el formato."},
        {"formato": "Gabriel + motion cromado (estilo 10)",
         "plantilla": "video-recursos/plantillas/gabriel-motion-cromado",
         "estado": "Nuevo: todavía sin pieza publicada.",
         "piezas": [{"id": "nov-gabriel-no-compres-descuento-reel"}],
         "control": "nov-gabriel-error-modelos-reel (Gabriel a cámara sin motion, 14-nov)",
         "que_falta_saber": "Si el motion suma vistas y comentarios frente a Gabriel a cámara solo."},
    ],
    "revisiones": ["lun 9-nov: las piezas de octubre (uniones, IA, chuleta 1) ya tienen 7 días", "lun 30-nov: cierre del mes y decisión para diciembre"],
}

DESTACADAS = [
    {"destacada": "🔩 ACERO", "que_va": "Chuletas de acero, Gabriel sobre el orden del diseño, acceso anticipado y Black Week de Acero.",
     "agregar": ["nov-hist-1104", "nov-hist-1105", "nov-hist-1111", "nov-hist-1118", "nov-hist-1120", "nov-hist-1123", "nov-hist-1124", "nov-hist-1125", "nov-hist-1127", "nov-hist-1130"],
     "quitar": "El 1-dic: todos los frames con precio, cuenta regresiva o «Black Friday» (vencidos)."},
    {"destacada": "🎯 BIM + IA", "que_va": "Máster por bloques, workshop, Perú BIM, checklist de calidad y preguntas sobre la IA.",
     "agregar": ["nov-hist-1102", "nov-hist-1103", "nov-hist-1109", "nov-hist-1112", "nov-hist-1113", "nov-hist-1116", "nov-hist-1117", "nov-hist-1119", "nov-hist-1126"],
     "quitar": "Después del 17-nov, los frames de cuenta regresiva y registro del workshop (dejar solo el resumen del 19)."},
    {"destacada": "🎁 HERRAMIENTAS", "que_va": "Recursos gratis (zapatas, 5 verificaciones, test de nivel) y cursos de bajo costo.",
     "agregar": ["nov-hist-1031", "nov-hist-1101", "nov-hist-1106", "nov-hist-1110"],
     "quitar": "El 2-nov: los frames del cupón SUSTO (vencido)."},
    {"destacada": "👥 COMUNIDAD", "que_va": "Detrás de cámara de la grabación con Daniela y del workshop.", "agregar": [], "quitar": "Recaps de más de 3 meses."},
    {"destacada": "⭐ ALUMNOS", "que_va": "Testimonios reales con permiso.", "agregar": [], "quitar": "Nada, salvo que un alumno retire su permiso."},
]
DESTACADA_DE = {i: d["destacada"] for d in DESTACADAS for i in d["agregar"]}

CHECKLIST = [
    {"tarea": "Revisar el post del 21-oct (DexigJZl5mA): su caption abre con el texto del carrusel cancelado del workshop, que decía «Jueves 22 de octubre». Si quedó la fecha vieja, editarlo.", "desbloquea": "Que nadie llegue al workshop con la fecha equivocada", "cuando": "ya", "para": "Daniela"},
    {"tarea": "WORKSHOP: montar y probar la palabra en GHL con una cuenta ajena (IG y FB), y confirmar que solo GHL la contesta.", "desbloquea": "Reel del 31-oct y todo el feed del workshop", "cuando": "antes del vie 30-oct", "para": "Ester"},
    {"tarea": "Grabar en UNA sesión con Daniela: demo y «para quién es» del workshop, el reel «conectar la IA a Revit en 3 pasos» y «tu nave a ojo» (celular sobre el monitor, como el referente), el reel «el error que más veo», el reel «no compres por el descuento» y los selfies de Gabriel para historias (3, 5, 10, 12, 16, 18, 23 y 27-nov). Lista de pantallas en grabaciones-pantalla-gabriel.pdf.", "desbloquea": "6 reels y 8 historias con Gabriel a cámara", "cuando": "antes del jue 29-oct (lo del workshop) y del vie 13-nov (el resto)", "para": "Gabriel y Daniela"},
    {"tarea": "Editar las 4 chuletas (perfiles de acero, cerchas, LOD, uniones) con los formatos de los reels del 19 y 20-oct que funcionaron: la 1, la 3 y la 4 como «Simbología de niveles» (lista visual sin voz) y la 2 como «5 tipos de cimentación» (pizarra con voz). Gabriel revisa cada lámina técnica antes de publicar.", "desbloquea": "La serie que se llevó octubre", "cuando": "una por semana, 2 días antes", "para": "Daniela / Dayana"},
    {"tarea": "Auditar el disparador de NIVEL: 110 disparos en 3 días contra 9 tests terminados (análisis del 23-oct). Comprobar si responde a cualquier comentario con la palabra «nivel» y avisar al setter.", "desbloquea": "Las 8 piezas que piden NIVEL", "cuando": "antes del lun 2-nov", "para": "Ester / Patricio"},
    {"tarea": "Decidir precios, bonos y cómo se nombra cada oferta de Halloween y Black Friday (propuesta en la pestaña Resumen). La promo va SOLO por WhatsApp: no se cambia la página vieja. Crear los cupones, las 3 mini landings (SUSTO; BLACK · Acero; BLACK · cursos) y el enlace de WhatsApp con cada palabra ya escrita, y ponerlo donde las piezas dicen [enlace de WhatsApp…].", "desbloquea": "Halloween (30-oct) y Black Week (18-nov)", "cuando": "Halloween antes del jue 29-oct; Black Friday antes del lun 16-nov", "para": "Ester (decide y crea)"},
    {"tarea": "Respuestas a las palabras de historias, correos y comunidades (SUSTO, LISTA, BLACK, NAVES, NIVEL, ACERO, ZAPATA): las contesta una persona; las de oferta pasan a WhatsApp, donde va el precio y la mini landing. Dejar plantillas listas en la bandeja.", "desbloquea": "Que las historias de venta conviertan", "cuando": "antes del 30-oct", "para": "Ester y Aylin"},
    {"tarea": "Publicar los 2 reels de prueba ya editados («6 uniones acero-hormigón» y «¿La IA te va a reemplazar?») antes del 31-oct, y anotar su enlace para la revisión de formatos.", "desbloquea": "La revisión de formatos del 9-nov", "cuando": "antes del sáb 31-oct", "para": "Daniela"},
    {"tarea": "Producir la chuleta 2 (cerchas) en estilo 9, pizarra con voz, y «no compres por el descuento» en estilo 10, motion cromado. Son las piezas de prueba de formato del mes.", "desbloquea": "Comparar formatos con el mismo tipo de tema", "cuando": "2 días antes de cada fecha", "para": "Daniela / Dayana"},
    {"tarea": "Revisión de formatos en prueba: correr scripts/formatos_prueba.py --mes 2026-11 y anotar en el calendario, por pieza, cuántos llegaron al WhatsApp y cuántas ventas salieron en 14 días (GHL).", "desbloquea": "Qué formato entra fijo en diciembre", "cuando": "lun 9-nov y lun 30-nov", "para": "Ester (datos de GHL) · Dayana (decide)"},
    {"tarea": "Confirmar con Dayana los nombres de los 4 bloques del Máster y qué certificación da cada uno, y los nombres de los 4 módulos de Acero.", "desbloquea": "Post del 13, carrusel del 20 y del 23-nov", "cuando": "antes del lun 9-nov", "para": "Dayana"},
    {"tarea": "Pedir el corte de Stripe y PayPal de noviembre de 2025 (no hay dato del Black Friday pasado).", "desbloquea": "La meta de Black Friday", "cuando": "antes del 10-nov", "para": "Dayana"},
    {"tarea": "Pauta: apagar «Resto» de ACERO WSP, las 2 campañas LEAD MAGNETS y ACERO TEST GANCHOS; subir la campaña de registro del workshop (2 al 16-nov).", "desbloquea": "Leads más baratos y registros al workshop", "cuando": "lun 2-nov", "para": "Olympus"},
    {"tarea": "La guía de regalo «conectar la IA a tu Revit» (la promete la landing y el mensaje del 16-nov) tiene que existir antes del workshop. Definir quién la hace.", "desbloquea": "Promesa del workshop", "cuando": "antes del lun 16-nov", "para": "Dayana (asigna)"},
    {"tarea": "Cada viernes, guardar las historias de la semana en su destacada; el 2-nov quitar SUSTO y el 1-dic quitar todo lo de Black Friday.", "desbloquea": "Destacadas al día", "cuando": "viernes 6, 13, 20 y 27", "para": "Daniela"},
    {"tarea": "Publicar los 4 blogs (6, 13, 20 y 27) con su post de anuncio.", "desbloquea": "G3 del mes", "cuando": "cada viernes", "para": "equipo de contenido"},
]


def main():
    feed = [fila_feed(*f) for f in FEED]
    fmt = Counter("reel" if "REEL" in (x["formato_publicacion"] or "").upper() else
                  "carrusel" if "CARRUSEL" in (x["formato_publicacion"] or "").upper() else "post" for x in feed)
    inten = Counter("objeción/testimonio" if x["intencion"] in ("objeción", "testimonio") else x["intencion"] for x in feed)
    hist = filas_de("GRUPO 5")
    ventas = sum(1 for x in hist if x.get("venta"))
    gab = sum(1 for x in hist if x.get("gabriel_a_camara"))
    cal = {
        "mes": "2026-11",
        "subtitulo": "Del miércoles 28 de octubre al lunes 30 de noviembre · Halloween, workshop del 17-nov y Black Friday · escrita para vender Máster por bloques y Especialización en ACERO",
        "ventas_por_semana_max": 4,
        "reglas_del_mes": [
            "LO QUE APRENDIMOS EN OCTUBRE (análisis del 23-oct): dos reels que NO estaban en la matriz —«Simbología de niveles en planos ¿Cuál usas más?» (57.230 vistas, 220 comentarios, 2.455 guardados, 705 compartidos, el más compartido de la cuenta) y «5 tipos de cimentación» (8.598 vistas, 7,33 comentarios por 1.000)— se llevaron el 44 % de las vistas y el 71 % de los guardados del mes. Por eso noviembre abre la SERIE CHULETA: 4 reels, uno por semana.",
            "REFERENTES (Graph API, 23-oct; Apify sin crédito este mes): el reel DeGtyhfoXar de @lexmrbim («Conecta Revit + IA paso a paso») sacó 98.570 vistas y 3.162 comentarios. Su mediana de reels (5.224) es casi la nuestra (5.306): lo que lo separa es que CADA tutorial termina en un recurso por palabra (reels con palabra: 14 comentarios por 1.000; sin palabra: 0). Se adapta en dos reels (7 y 19-nov). @aecode.ai: lo que le funciona son carruseles comparativos con un problema de obra en el gancho.",
            "LO QUE NO FUNCIONÓ: los anuncios de producto sueltos en el feed (tutor, certificado, carrusel del workshop: 0 comentarios) y los reels de opinión sobre la IA y los clips de clase de los sábados (936 a 1.177 vistas, 0 a 2 comentarios). Cada producto entra detrás de un problema o de un dato. El workshop no tuvo registros porque todavía no se había promocionado: no hay anuncio y ninguna historia lo mencionaba.",
            f"FEED: {len(feed)} piezas · formato {fmt['reel']} reels / {fmt['carrusel']} carruseles / {fmt['post']} posts · intención {inten['problema']} problema / {inten['solución']} solución / {inten['objeción/testimonio']} objeción.",
            "EFEMÉRIDES Y TENDENCIAS ENTRAN AL CALENDARIO (pedido de Dayana, 23-oct): Día de Difuntos y de Muertos, Día de la Ciencia, World Quality Day, Buen Fin, Black Friday de Ecuador (20-nov) e internacional (27-nov), Cyber Monday, y la tendencia del sector: BIM obligatorio en Perú. Tabla completa en la pestaña Resumen.",
            f"HISTORIAS CON MÁS VENTA Y CON GABRIEL (Dayana, 23-oct): {ventas} historias de venta en el mes (2 por semana hasta el workshop, más en la Black Week) y Gabriel a cámara en {gab} días (al menos 2 por semana), grabadas en una sola sesión con Daniela.",
            "DAR A CONOCER LOS PROGRAMAS: el Máster por bloques (BIM Professional · Coordination · Management · BIM + IA) y la Especialización en Acero se explican con piezas propias (13, 20 y 23-nov), siempre desde el problema y sin precio en el feed.",
            "PALABRAS DE COMENTARIO: NIVEL (Máster), ACERO, ZAPATA y WORKSHOP (hasta el 17-nov). En historias, las respuestas (SUSTO, NAVES, LISTA, BLACK) llegan por DM y las contesta una persona. No hay lead magnet nuevo este mes.",
            "LA PROMO SOLO POR WHATSAPP (Dayana, 23-oct): ninguna pieza pública lleva el precio de la oferta ni enlaza la página vieja. Quien responde o escribe al WhatsApp recibe el precio y la mini landing de su oferta. Ester decide los precios y cómo se nombran. El Máster nunca lleva precio. Toda oferta cierra a la hora dicha (Ecuador) y NO se reabre.",
            "FORMATOS EN PRUEBA: chuleta visual sin voz, pizarra con voz de Gabriel (estilo 9) y Gabriel con motion cromado (estilo 10). Se revisan el 9 y el 30-nov. Un formato entra fijo solo si genera interés, interacción y ventas (pestaña Resumen).",
            "Visuales = capturas reales de Revit/Robot/Navisworks y cámara de Gabriel. Nada técnico se publica sin que Gabriel lo revise (regla 0).",
            "Mínimo 60 % en el NÚCLEO. Cero OBRA. Ninguna pieza repite un id o un gancho ya usado.",
        ],
        "checklist_tareas": CHECKLIST,
        "efemerides": EFEMERIDES,
        "estrategia_comercial": ESTRATEGIA_COMERCIAL,
        "formatos_prueba": FORMATOS_PRUEBA,
        "publicidad": {
            "nota": "Primero se apaga lo que no trae nada; después entran la campaña de registro del workshop y las de Black Friday.",
            "campanas": [{"nombre": k, "piezas": [ficha_anuncio(i, k) for i in v]} for k, v in ADS.items()],
            "indicaciones": DECISIONES_PAUTA,
        },
        "grupos": [
            {"n": 1, "nombre": "GRUPO 1 · Feed principal — Instagram, Facebook, TikTok, YouTube Shorts",
             "descripcion": "4-5 piezas por semana. La serie Chuleta sale martes o miércoles; el workshop ocupa su carrusel y sus dos videos; la Black Week va sin precios en el feed.",
             "reglas": ["Cada pieza lleva el CTA de su producto: Máster → NIVEL; ACERO → ACERO; concreto → ZAPATA; workshop → WORKSHOP (hasta el 17).",
                        "En TikTok y YouTube Shorts, sin palabra clave: pregunta abierta."],
             "calendario": feed},
            {"n": 2, "nombre": "GRUPO 2 · Comunidades — WhatsApp, canal de IG, grupos de FB, comunidad de YouTube, comunidades GHL",
             "descripcion": "Un solo post completo, el mismo en todos los canales: 6 del workshop (plan), Halloween, Acero, Máster por bloques y 4 de Black Friday.",
             "reglas": ["Si hay regalo o registro, el enlace va directo en el post. Nada de «respóndeme X». Sin hashtags.", "Si es oferta, el único enlace es el de WhatsApp con la palabra ya escrita. Nunca el precio ni la página vieja."],
             "calendario": filas_de("GRUPO 2")},
            {"n": 3, "nombre": "GRUPO 3 · Blog de Design Modeling Academy",
             "descripcion": "Un artículo cada viernes (6, 13, 20 y 27) con su post de anuncio.", "reglas": ["El CTA del blog nunca es genérico."],
             "calendario": filas_de("GRUPO 3")},
            {"n": 4, "nombre": "GRUPO 4 · LinkedIn — Design Modeling Academy",
             "descripcion": "Solo la página de Design Modeling Academy, 2 por semana, tono formal, sin hashtags; publica Daniela.",
             "reglas": ["NUNCA «comenta la palabra»: pregunta abierta al final.", "El enlace va dentro del post."],
             "calendario": filas_de("GRUPO 4")},
            {"n": 5, "nombre": "GRUPO 5 · Historias de Instagram (y Facebook stories)",
             "descripcion": f"Lunes a viernes (y Halloween), 3-4 frames. {ventas} días de venta y {gab} con Gabriel a cámara.",
             "reglas": ["El sticker es el CTA.", "Precio nunca en la historia: va por DM o WhatsApp, con la mini landing de la oferta.", "Máximo 4 frames.", "Las respuestas llegan como DM: se contestan a mano."],
             "calendario": [{**x, **({"destacada": DESTACADA_DE[x["id"]]} if x["id"] in DESTACADA_DE else {})} for x in hist]},
        ],
        "lead_magnets": {
            "nota": "Noviembre NO lanza lead magnet nuevo (análisis del 23-oct): ZAPATA, ACERO y MEMORIA están vivas, COTIZA no arrancó (9 contactos al bot) y OpenReply no envía nada desde el 10-oct.",
            "nuevo": [],
            "respaldo": [{"nombre": "5 verificaciones en acero", "palabra": "ACERO", "por_que": "CTA de las chuletas de acero y de Acero."},
                         {"nombre": "Test de Nivel BIM", "palabra": "NIVEL", "por_que": "Puerta al Máster. Auditar el disparador antes del 2-nov."},
                         {"nombre": "Calculadora de Zapatas", "palabra": "ZAPATA", "por_que": "Subió de 181 a 214 etiquetados tras las chuletas de octubre."}],
            "mapa_cta": [{"palabra": "WORKSHOP", "fecha": "31-oct, 3, 5, 7, 16 y 17-nov", "producto": "Registro al workshop"},
                         {"palabra": "NIVEL", "fecha": "2, 9, 12, 13, 14, 18, 21 y 23-nov", "producto": "Máster"},
                         {"palabra": "ACERO", "fecha": "4, 10, 19, 20, 24, 25 y 27-nov", "producto": "Acero"},
                         {"palabra": "ZAPATA", "fecha": "6-nov", "producto": "Calculadora de zapatas"}],
        },
        "destacadas": {"responsable": "Daniela", "nota": "Se alimentan cada viernes; lo vencido (SUSTO, cuenta regresiva del workshop, Black Friday) se quita al día siguiente de cerrar.", "lista": DESTACADAS},
        "correos_nota": "A la lista propia: Halloween (2), workshop (3) y Black Friday (6).",
        "piezas": [], "pauta": [],
        "banco_reserva": [i for i in ["oct-tutor-dip-reel", "ago-tip-revit-ia"] if i in G],
        "correos": correos(),
        "auditoria_previa": {"mes": "2026-10", "artefacto": "https://github.com/designmodelingdg-droid/meta-ads-dashboard.html/blob/claude/remote-control-setup-GUe3f/matriz-viral/auditorias/2026-10-resultados.md", "archivos": ["matriz-viral/auditorias/2026-10-resultados.md"],
                             "resumen": "Octubre (1-22): 148.263 vistas en IG, 540 comentarios en IG y 251 en FB. Lo que funcionó: las 2 chuletas fuera de matriz y los posts de acusación o dato (cita de obra 12,10 comentarios por 1.000; MEMORIA 9,50; pandeo 5,21; COTIZA 5,08). Lo que no: anuncios de producto en el feed y reels de opinión."},
        "kpis_mensuales": {
            "nota": "De dónde arranca noviembre. Fuentes: matriz.json (Meta Graph API, 23-oct), ads-insights (23-sep → 22-oct) y fuentes/ingresos (1 al 22-oct). Lo cobrado por consultoría NO es ingreso de la Academy (Dayana, 23-oct).",
            "pauta_30_dias": {"gasto": 1090.76, "leads": 1097, "cpl": 0.99},
            "cobrado_academy_1_22_oct": 4016.82,
            "metas_noviembre": ["Registros al workshop: la meta la fija Dayana (no hay base histórica). Se mide el 3 y el 10-nov.",
                                "Black Friday: la meta se fija con el corte de nov-2025 (pendiente).",
                                "Chuletas: cada una por encima de la mediana de 90 días (2.437 vistas)."],
        },
        "pendientes": ["Precios y bonos: los confirma Dayana.", "Nombres de bloques y módulos: los confirma Dayana."],
        "resumen_cierre": f"Noviembre: {len(feed)} piezas de feed con la serie Chuleta (el formato que se llevó octubre), el workshop del 17 con todas sus piezas, Halloween y Black Friday con fechas por país, {len(hist)} días de historias ({ventas} de venta, {gab} con Gabriel a cámara), comunidades, LinkedIn, 4 blogs, {len(correos())} correos y la pauta.",
        "pie": "Design Modeling Academy · Matriz de contenido noviembre 2026 (28 oct – 30 nov) · métricas reales de Meta Graph API, análisis de referentes con Apify y efemérides verificadas con fuente.",
    }
    json.dump(cal, open(M / "calendario-noviembre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok ·", len(feed), "feed ·", dict(fmt), dict(inten), "·", sum(len(g["calendario"]) for g in cal["grupos"]), "entradas")


if __name__ == "__main__":
    main()
