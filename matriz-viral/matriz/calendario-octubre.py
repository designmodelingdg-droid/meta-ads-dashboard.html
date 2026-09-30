#!/usr/bin/env python3
"""Construye calendario-octubre.json desde las piezas de guiones-completos.json.

    python3 matriz-viral/matriz/calendario-octubre.py

El calendario solo ORDENA piezas: el contenido de cada una vive en
guiones-completos.json (lo que lee la app de Daniela). Si una pieza cambia, se
corrige allí y se vuelve a correr esto. El Word, el artefacto y el JSON
completo salen de este calendario.
"""
import json
import pathlib

M = pathlib.Path(__file__).resolve().parent
G = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}

S1, S2, S3, S4 = "Semana 1 (5-11 oct)", "Semana 2 (12-18 oct)", "Semana 3 (19-25 oct)", "Semana 4 (26 oct-1 nov)"
SEM = {**{d: S1 for d in range(5, 12)}, **{d: S2 for d in range(12, 19)},
       **{d: S3 for d in range(19, 26)}, **{d: S4 for d in range(26, 32)}}
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def etiqueta(dia):
    import datetime
    return f"{DIAS[datetime.date(2026, 10, dia).weekday()]} {dia}"


def pieza(pid):
    if pid not in G:
        raise SystemExit(f"FALTA en guiones-completos.json: {pid}")
    return G[pid]


# ───────────────────────── GRUPO 1 · FEED ─────────────────────────
# (día, id, intención 50/20/30, producto, CTA, nota)
FEED = [
    (5,  "oct-tutor-dip-carrusel",             "solución",   "Diplomado", "Comenta DIPLOMADO (si no está montada: DM)", "Abre el lanzamiento del Tutor IA del Diplomado."),
    (7,  "oct-tutor-dip-reel",                 "solución",   "Diplomado", "Comenta DIPLOMADO / DM", "Reel de lanzamiento. Graba Gabriel."),
    (9,  "oct-dato-deriva-post",               "problema",   "Acero",     "Comenta ACERO", "Post con dato de cálculo verificable (el formato que más guarda la cuenta). En FB sale además oct-tutor-dip-post-fb."),
    (12, "oct-acusa-ia-calculo-carrusel",      "problema",   "Máster",    "Comenta NIVEL", "Acusación. Capturas reales de Revit/Robot."),
    (13, "oct-cotiza-reel",                    "problema",   "Cotizador", "Comenta COTIZA", "EXTRA lead magnet (martes). COTIZA se monta en OpenReply justo después de publicar."),
    (14, "oct-ranking-software-estructural-reel", "problema", "Máster",   "Comenta NIVEL", "Ranking con tablero físico. Graba Gabriel."),
    (15, "oct-cotiza-carrusel",                "solución",   "Cotizador", "Comenta COTIZA", "EXTRA lead magnet (jueves)."),
    (16, "oct-ang4-naves-rechazadas-post",     "problema",   "Acero",     "Comenta ACERO", "Ángulo 4 de compradores: los proyectos que rechazas."),
    (19, "oct-ranking-perfil-bim-carrusel",    "problema",   "Máster",    "Comenta NIVEL", "Ranking: ¿en qué fila estás?"),
    (20, "oct-obj-tiempo-reel",                "objeción",   "Máster",    "Comenta NIVEL", "Objeción de tiempo. Graba Gabriel."),
    (21, "oct-acusa-ia-calculo-reel",          "solución",   "Máster",    "Comenta NIVEL", "La IA ordena, tú decides. Graba Gabriel."),
    (22, "oct-obj-certificado-carrusel",       "objeción",   "Máster",    "Comenta NIVEL", "Objeción de certificado. Dayana confirma la lista de certificados antes de diseñar."),
    (23, "oct-ang3-bim-se-exige-post",         "problema",   "Máster",    "Comenta NIVEL", "Ángulo 3: BIM ya se exige."),
    (26, "oct-ang8-obra-software-carrusel",    "problema",   "Acero",     "Comenta ACERO", "Ángulo 8: de la obra al software. Filtra a quien quiere soldar."),
    (27, "oct-obj-cursos-youtube-reel",        "objeción",   "Acero",     "Comenta ACERO", "Objeción: muchos cursos, ninguno aplicable. Graba Gabriel."),
    (28, "oct-testimonio-acero-reel",          "testimonio", "Acero",     "Comenta ACERO", "Alumno real con permiso. Si el 21-oct no hay, sale la pieza de reserva descrita en la pieza."),
    (29, "oct-lm-acero-pandeo-lt-carrusel",    "problema",   "Acero",     "Comenta ACERO", "EXTRA lead magnet ACERO (el PROMO de recurso es lo que más comenta la cuenta: DM157, 159 comentarios)."),
    (30, "oct-obj-dinero-post",                "objeción",   "Máster",    "Comenta NIVEL", "Objeción de dinero sin precio: lo caro es el proyecto rechazado."),
]


def fila_feed(dia, pid, intencion, producto, cta, nota):
    p = pieza(pid)
    return {"fecha": etiqueta(dia), "fecha_iso": f"2026-10-{dia:02d}", "semana": SEM[dia], "id": pid,
            "titulo": p.get("titulo"), "tipo": p.get("tipo"), "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
            "intencion": intencion, "producto": producto, "cta": cta, "estado": p.get("estado"), "nota": nota}


def filas_de(grupo_prefijo, extra=None):
    """Todas las piezas de octubre de un grupo, en orden de fecha."""
    out = []
    for p in G.values():
        if str(p.get("fecha_iso", "")).startswith("2026-10") and str(p.get("grupo", "")).startswith(grupo_prefijo):
            d = int(p["fecha_iso"][8:10])
            out.append({"fecha": etiqueta(d), "fecha_iso": p["fecha_iso"], "semana": SEM.get(d, S4), "id": p["id"],
                        "titulo": p.get("titulo"), "tipo": p.get("tipo"),
                        "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
                        "idea": {"titulo": p.get("titulo"), "formato": p.get("formato_detalle") or p.get("formato"),
                                 "desarrollo": p.get("hook") or ""},
                        **({"cuenta": p["cuenta"]} if p.get("cuenta") else {})})
    return sorted(out, key=lambda x: x["fecha_iso"])


def correos():
    out = []
    for p in G.values():
        if str(p.get("fecha_iso", "")).startswith("2026-10") and p.get("grupo") == "Correos":
            cuerpo = p.get("cuerpo")
            out.append({"fecha": f"{etiqueta(int(p['fecha_iso'][8:10]))} · {SEM.get(int(p['fecha_iso'][8:10]), S4).split(' (')[0]}",
                        "fecha_iso": p["fecha_iso"], "id": p["id"], "nombre": p.get("titulo"),
                        "asunto": p.get("asunto"), "preencabezado": p.get("preencabezado"),
                        "segmento": p.get("segmento"), "objetivo": p.get("hook") or "",
                        "cuerpo": "\n\n".join(cuerpo) if isinstance(cuerpo, list) else (cuerpo or ""),
                        "condicion": p.get("condicion") or ""})
    return sorted(out, key=lambda x: x["fecha_iso"])


def ficha_anuncio(pid, campana):
    p = pieza(pid)
    cfg = [["Botón", p.get("boton", "")], ["Público", p.get("publico_sugerido", "")], ["Qué medir", p.get("que_medir", "")]]
    if p.get("por_que"):
        cfg.append(["Por qué", p["por_que"]])
    guion = p.get("guion_video")
    pngs = sorted(str(x.relative_to(M.parent.parent)) for x in (M.parent / "entregables" / "pauta-octubre").glob(f"{pid}-*.png"))
    if pngs:
        cfg.append(["Creativo listo (4:5 y 9:16)", " · ".join(pngs)])
    return {"id": pid, "titulo": p.get("titulo"), "campana": campana,
            "precio": "$225 USD" if "Acero" in (p.get("producto") or campana) else "sin precio (regla del Máster)",
            "formato": p.get("formato_detalle") or "anuncio", "hook": p.get("hook"), "cuerpo": p.get("texto_principal"),
            "titular": p.get("titular"), "descripcion": p.get("descripcion"), "creativo": p.get("creativo"),
            **({"guion": guion} if guion else {}),
            "prompt": p.get("prompt_imagenes", ""), "cfg": cfg, "condicion": p.get("condicion", ""),
            **({"creativos_png": pngs} if pngs else {})}


ADS = {
    "ACERO · formulario (campaña [AGOSTO] ESPE.1 ACERO - FORM, geo-split)":
        ["oct-ang-ads-acero-a-naves", "oct-ang-ads-acero-b-obra-software", "oct-ang-ads-acero-c-otro-curso"],
    "ACERO · WhatsApp directo (se vuelve a encender, ~$390/mes)": ["oct-ang-ads-acero-wa-prueba"],
    "MÁSTER · una sola campaña ([14SEP] MASTER - FORM)":
        ["oct-ang-ads-master-a-revit-no-es-bim", "oct-ang-ads-master-b-concurso", "oct-ang-ads-master-c-trabajar-afuera", "oct-ang-ads-master-r-tiempo"],
    "DIPLOMADO · Tutor IA (desde el 12)": ["oct-tutor-dip-ads-a-rebobinar", "oct-tutor-dip-ads-b-minuto", "oct-tutor-dip-ads-c-no-inventa"],
}

DECISIONES_PAUTA = [
    ["Por qué hay que corregir antes de sumar anuncios",
     "Septiembre gastó lo mismo que agosto (~$1.150) y trajo −33 % de resultados en Meta, +50 % de costo por lead y −17 % de leads en GHL. La semana del 21-sep entraron 153 leads contra 230–380 lo normal (diagnóstico de Dayana, 30-sep)."],
    ["1 · Volver a encender ACERO por WhatsApp",
     "Junto al formulario, no en su lugar, con ~$390/mes como en agosto. «[JUL] ESPE.1 ACERO – WSP SMS» trajo 510 conversaciones a $0,77, y al apagarla los leads sin origen bajaron de 499 a 96. En julio-agosto el WhatsApp vendió 0,7 por cada 100 leads y el formulario 0,4. El texto es el ganador de la cuenta, con cierre «Escríbenos por WhatsApp», y el mensaje de bienvenida lleva el precio de $225 con Tutor de IA. Se mide por ventas a $225 a los 7 días."],
    ["2 · Pausar los anuncios cansados",
     "El 59 % de los leads de septiembre viene de anuncios de enero a julio, con frecuencia 2,74 en ACERO. En ACERO el presupuesto pasa a «ACERO 1» y «AceroAI1-1V04/V05/V06». En el Máster pasa a «MásterBloque1-1V05», el único anuncio de septiembre con venta en GHL ($400). Se retiran las copias de enero y mayo. Los anuncios nuevos de octubre entran como reemplazo, no como capa extra."],
    ["3 · Devolver presupuesto a ACERO",
     "En septiembre el Máster pasó de $420 a $700 y ACERO de $723 a $451. Un lead del Máster cuesta 2,8–3,6 $ en GHL y uno de ACERO 1–1,6 $."],
    ["4 · El Máster optimiza por UN evento de lead",
     "No por «Conversiones múltiples»: «[14SEP]» cuenta 212 resultados y GHL ve 83. Revisar por qué «[27AGO] TESTEO» no registra resultados y dejar el Máster en una sola campaña (el mismo texto corría en dos, el 34 % del gasto)."],
    ["5 · Publicar lo que ya está hecho",
     "Hay 26 borradores sin publicar, entre ellos «SEPTIEMBRE23» de ETABS + IDEA StatiCa. Se revisan y se publican los útiles antes de producir creativos nuevos."],
    ["6 · Filtros ya acordados (25-sep)",
     "Formulario de ACERO de «mayor intención», con la pregunta del precio de $225 y otra sobre qué software usa. El Máster agenda solo a quien dijo SÍ a los $500. Recordatorios de la cita a 24 h, 2 h y 15 min. Un solo enlace de pago de ACERO ($225)."],
    ["REGLA DE ORO", "El Máster no lleva precio en ninguna pieza. ACERO lleva $225 solo en pauta y en correo a la lista propia. Un texto por ángulo, en una sola campaña."],
]

LEAD_MAGNETS = {
    "nota": "Octubre sale con UN lead magnet nuevo (COTIZA) y ninguno más. Los de respaldo ya existen y funcionan. Si en la semana 2 uno no genera DM, se reemplaza por otro de esta lista, no por uno nuevo.",
    "nuevo": [{"nombre": "Cotizador de Honorarios Estructurales", "palabra": "COTIZA",
               "estado": "Funnel en GHL montado y probado por Dayana (30-sep). OpenReply se monta justo después de publicar el reel del 13 y el carrusel del 15. Falta volver a pegar ghl-landing.html con el formulario nativo.",
               "piezas": ["oct-cotiza-reel", "oct-cotiza-historias", "oct-cotiza-carrusel", "oct-blog-cobrar-diseno-estructural"],
               "puente": "Especialización en Acero / Diplomado en Estructuras (secuencia de correo S5)"}],
    "respaldo": [
        {"nombre": "Calculadora de Zapatas", "palabra": "ZAPATA", "por_que": "El que más leads trajo (162 etiquetados) y alimenta ACERO."},
        {"nombre": "5 verificaciones en acero", "palabra": "ACERO", "por_que": "Su post DM157 es el mejor PROMO de la cuenta (159 comentarios, 356 guardados). CTA de todas las piezas de ACERO."},
        {"nombre": "Test de Nivel BIM", "palabra": "NIVEL", "por_que": "Puerta al Máster y CTA de todas sus piezas. Poco uso hasta ahora: se mide en octubre."},
        {"nombre": "Memoria de cálculo", "palabra": "MEMORIA", "por_que": "Vivo, 23 leads. Se usa solo si una pieza de cálculo lo pide."},
    ],
    "retirados": [{"nombre": "Guía Revit + ChatGPT", "palabra": "CHATGPT", "por_que": "No tiene campaña ni workflow que conteste: nadie recibe nada. Fuera de los CTA hasta que se vuelva a montar."}],
    "mapa_cta": [
        {"palabra": "NIVEL", "fecha": "Lun 12, Mié 14, Lun 19, Mar 20, Mié 21, Jue 22, Vie 23, Vie 30", "producto": "Máster"},
        {"palabra": "ACERO", "fecha": "Vie 9, Vie 16, Lun 26, Mar 27, Mié 28, Jue 29", "producto": "Acero"},
        {"palabra": "COTIZA", "fecha": "Mar 13, Jue 15 (+ historias Mar 13 y blog Sáb 17)", "producto": "Cotizador → Acero/Diplomado"},
        {"palabra": "DIPLOMADO", "fecha": "Lun 5, Mié 7 (lanzamiento del tutor)", "producto": "Diplomado · montar antes del 5 o CTA a DM"},
    ],
}

CHECKLIST = [
    {"tarea": "Volver a pegar cotizador-honorarios/ghl-landing.html en la página 1 del funnel (trae el formulario nativo). Quitar del formulario la línea «Te la enviamos también al correo» y poner Ecuador como país por defecto. Borrar el contacto «Prueba Cotizador».", "desbloquea": "Que los leads de COTIZA entren a su workflow y no al de Zapatas", "cuando": "antes del 13-oct", "para": "Ester y Aylin"},
    {"tarea": "Gabriel revisa las horas de ejemplo del cotizador (app.html, ENTREGABLES).", "desbloquea": "Reel del Mar 13 y carrusel del Jue 15", "cuando": "antes del 12-oct", "para": "Gabriel"},
    {"tarea": "Día de grabación 1: reels del 13, 14, 20 y 21 (+ tablero físico del ranking).", "desbloquea": "Semanas 2 y 3 del feed", "cuando": "Jue 8-oct", "para": "Gabriel"},
    {"tarea": "Día de grabación 2: reels del 27 y 28 (testimonio o pieza de reserva) + capturas de Robot para el carrusel del 29.", "desbloquea": "Semana 4 del feed", "cuando": "Jue 22-oct", "para": "Gabriel"},
    {"tarea": "Conseguir un alumno de ACERO con permiso por escrito para el testimonio.", "desbloquea": "Reel del Mié 28", "cuando": "antes del 21-oct", "para": "Dayana / soporte"},
    {"tarea": "Confirmar la lista exacta de certificados del Máster y pasar los escaneos oficiales.", "desbloquea": "Carrusel del Jue 22", "cuando": "antes del 19-oct", "para": "Dayana"},
    {"tarea": "Montar la palabra DIPLOMADO (o dejar el CTA en DM).", "desbloquea": "Lanzamiento del tutor 5–9 oct", "cuando": "antes del 5-oct", "para": "Patricio"},
    {"tarea": "Crear la campaña COTIZA en OpenReply atada al post justo después de publicar, y la de Facebook en GHL; probar con una cuenta ajena.", "desbloquea": "Que el comentario COTIZA reciba el DM", "cuando": "13 y 15-oct, al publicar", "para": "Patricio"},
    {"tarea": "Pauta: aplicar las 6 decisiones de la sección de publicidad (WhatsApp de ACERO, pausar anuncios cansados, presupuesto, optimización del Máster, borradores, filtros).", "desbloquea": "Que la pauta vuelva a traer compradores", "cuando": "semana del 5-oct", "para": "Olympus"},
    {"tarea": "Subir los anuncios nuevos de octubre como reemplazo de los cansados.", "desbloquea": "Pauta de las semanas 3 y 4", "cuando": "Lun 19-oct (tutor: Lun 12)", "para": "Olympus"},
    {"tarea": "Montar la secuencia de correo S5 · SEGUIMIENTO COTIZADOR (matriz-viral/seguimiento/correos-nutricion.json).", "desbloquea": "Seguimiento de los leads del cotizador", "cuando": "antes del 13-oct", "para": "Ester y Aylin"},
    {"tarea": "Publicar los 3 blogs (17, 24 y 31) con su post de anuncio.", "desbloquea": "G3 del mes", "cuando": "cada sábado", "para": "equipo de contenido"},
]


def main():
    feed = [fila_feed(*f) for f in FEED]
    from collections import Counter
    fmt = Counter("reel" if "REEL" in (x["formato_publicacion"] or "").upper() else
                  "carrusel" if "CARRUSEL" in (x["formato_publicacion"] or "").upper() else "post" for x in feed)
    inten = Counter("objeción/testimonio" if x["intencion"] in ("objeción", "testimonio") else x["intencion"] for x in feed)
    cal = {
        "mes": "2026-10",
        "subtitulo": "Del lunes 5 al domingo 1 de noviembre · calendarios por grupo, misma información adaptada a cada canal · escrita para vender Máster y Especialización en ACERO",
        "reglas_del_mes": [
            "REGLA DE ORO: todos los grupos comparten la misma información la misma semana, adaptada a cada canal. El feed del lunes alimenta comunidades, historias, LinkedIn y el correo de la semana.",
            f"FEED: {len(feed)} piezas · formato {fmt['reel']} reels / {fmt['carrusel']} carruseles / {fmt['post']} posts (40/40/20) · intención {inten['problema']} problema / {inten['solución']} solución / {inten['objeción/testimonio']} objeción o testimonio (50/20/30, del análisis de compradores del 29-sep).",
            "A QUIÉN LE HABLAMOS: cada pieza nombra a un perfil comprador de COMPRADORES-VS-NO.md. Si no le habla a ninguno, no entra.",
            "EL PATRÓN: acusar un hábito concreto (8,61 comentarios por 1.000 vistas contra 0,54) o dar un dato de cálculo verificable (DM168: 130 comentarios, 611 guardados). Nada de «la IA te va a reemplazar» (0 comentarios en julio).",
            "POST PLANO = SOLO CON DATO VERIFICABLE, con su fuente en las notas de producción.",
            "Mínimo 60 % en el NÚCLEO (BIM / IA / modelado / acero). Cero OBRA.",
            "NINGUNA pieza repite un id o un gancho ya usado (historico-2026.json).",
            "PALABRAS DE COMENTARIO — SOLO ESTAS: NIVEL (Máster), ACERO, ZAPATA, MEMORIA, COTIZA (nueva) y DIPLOMADO (lanzamiento del tutor, si está montada). CHATGPT queda fuera: no tiene quien conteste. BIM e IA siguen siendo el bot de ventas del Máster.",
            "UNA venta por semana, el jueves, en historias: 8 tutor · 15 objeción de ACERO · 22 espejo del Máster · 29 ACERO por dentro.",
            "EL MÁSTER NUNCA LLEVA PRECIO. ACERO lleva $225 solo en pauta y en correo a la lista propia.",
            "Visuales = capturas reales de Revit/Robot y cámara de Gabriel. Imagen con IA solo con aprobación y costo a la vista.",
            "Reels de menos de 30 s (en esta cuenta rinden más del doble que los de 30–60 s).",
        ],
        "checklist_tareas": CHECKLIST,
        "publicidad": {
            "nota": "Primero se corrige lo que hace perder leads (6 decisiones); después los anuncios nuevos reemplazan a los cansados. Fichas completas por anuncio abajo.",
            "campanas": [{"nombre": k, "piezas": [ficha_anuncio(i, k) for i in v]} for k, v in ADS.items()],
            "indicaciones": DECISIONES_PAUTA,
        },
        "grupos": [
            {"n": 1, "nombre": "GRUPO 1 · Feed principal — Instagram, Facebook, TikTok, YouTube Shorts",
             "descripcion": "Lun/Mié/Vie base + martes y jueves de lead magnet. Guion completo de cada pieza en guiones-completos.json (la app lo muestra por id).",
             "reglas": ["Cada pieza lleva el CTA de su producto: Máster → NIVEL; ACERO → ACERO; Cotizador → COTIZA.",
                        "En TikTok y YouTube Shorts, sin palabra clave: pregunta abierta."],
             "calendario": feed},
            {"n": 2, "nombre": "GRUPO 2 · Comunidades — WhatsApp, canal de IG, grupos de FB, comunidad de YouTube, comunidades GHL",
             "descripcion": "Martes, jueves y viernes. Comparten la pieza de la semana con contexto y una pregunta. Sin hashtags.",
             "reglas": ["Nunca un enlace suelto: contexto + pregunta.", "Canales de difusión: el recurso va con su enlace directo.", "Comunidades de WhatsApp/GHL: se puede pedir «respóndeme NIVEL / ACERO / COTIZA», pero ahí no hay bot: una persona del equipo contesta a mano con el enlace el mismo día.", "Grupos de Facebook y comunidad de YouTube: solo la pregunta, sin enlace."],
             "calendario": filas_de("GRUPO 2")},
            {"n": 3, "nombre": "GRUPO 3 · Blog de Design Modeling Academy",
             "descripcion": "Un artículo por semana, siempre sábado, con CTA a una campaña o a un recurso. El post de anuncio sale el mismo sábado.",
             "reglas": ["El CTA del blog nunca es genérico."],
             "calendario": filas_de("GRUPO 3")},
            {"n": 4, "nombre": "GRUPO 4 · LinkedIn — Design Modeling Academy · Design Modeling DG · Gabriel Pantoja",
             "descripcion": "Lun/Mié/Vie + texto de Gabriel los martes. Solo PDF, video horizontal o texto.",
             "reglas": ["NUNCA «comenta la palabra»: pregunta abierta y enlace en el primer comentario."],
             "calendario": filas_de("GRUPO 4")},
            {"n": 5, "nombre": "GRUPO 5 · Historias de Instagram (y Facebook stories)",
             "descripcion": "Lunes a viernes, 3–5 frames. Cada día abre la puerta a la pieza del feed; los jueves 15, 22 y 29 son el único slot de venta de la semana.",
             "reglas": ["El sticker es el CTA.", "Nunca precio ni «inscríbete».", "Máximo 5 frames.", "Las respuestas llegan como DM: se contestan a mano."],
             "calendario": filas_de("GRUPO 5")},
        ],
        "lead_magnets": LEAD_MAGNETS,
        "piezas": [],
        "pauta": [],
        "banco_reserva": [i for i in ["ago-derivas-deformaciones", "ago-tip-revit-ia", "ago-revit-ia-futuro"] if i in G],
        "correos": correos(),
        "kpis_mensuales": {
            "nota": "De dónde arranca octubre (septiembre, del 1 al 27, sin los 403 contactos cargados a mano). Fuente: diagnóstico de Dayana del 30-sep sobre Meta y GHL; cobros en fuentes/ingresos/.",
            "gasto_meta": {"agosto": 1144, "septiembre": 1151},
            "resultados_meta": {"agosto": 1177, "septiembre": 789},
            "costo_por_resultado": {"agosto": 0.97, "septiembre": 1.46},
            "leads_ghl": {"agosto": 1016, "septiembre": 844},
            "cobrado_neto_26ago_24sep": 7486.81,
            "metas_octubre": ["Leads en GHL de vuelta a ≥ 230 por semana", "Ventas de ACERO a $225 atribuibles a WhatsApp o formulario, medidas por semana", "Máster: todos los agendados con SÍ a los $500; asistencia > 50 %", "COTIZA: DM y leads etiquetados lead-cotizador"],
        },
        "pendientes": ["El detalle operativo está en checklist_tareas, con responsable.",
                       "Qué funciona y de dónde sale: HISTORICO-JUL-SEP.md y COMPRADORES-VS-NO.md."],
        "resumen_cierre": f"Octubre por grupos: {len(feed)} piezas de feed escritas para vender Máster y ACERO, 1 lead magnet nuevo (COTIZA) y 4 de respaldo, historias diarias con 1 venta por semana, comunidades, 4 blogs, LinkedIn en 3 cuentas, correos semanales y una pauta que primero corrige lo que hizo perder leads en septiembre.",
        "pie": "Design Modeling Academy · Matriz de contenido octubre 2026 (5 oct – 1 nov) · construida sobre la matriz viral (métricas reales de Instagram vía Meta Graph API), el histórico jul-sep y el análisis de quién compra y quién no.",
        "artefactos": {"nota": "Se completan al generar el Word y el artefacto de octubre."},
    }
    json.dump(cal, open(M / "calendario-octubre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok ·", len(feed), "feed ·", dict(fmt), dict(inten), "·", sum(len(g["calendario"]) for g in cal["grupos"]), "entradas")


if __name__ == "__main__":
    main()
