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
    (5,  "oct-tutor-dip-carrusel",             "solución",   "Diplomado", "Comenta DIPLOMADO (si no está montada: DM)", "Abre el lanzamiento del Tutor IA del Diplomado. AUDITORÍA SEP: los anuncios del tutor de Acero sacaron 0–2 comentarios; por eso esta pieza abre con el problema (buscar a ciegas en 133 h) y no con «ahora tiene tutor». Medir el martes 6: si queda por debajo de 2,66 comentarios por 1.000 vistas (mediana de septiembre), la pauta del tutor del 12 no se enciende sin cambiar el gancho."),
    (7,  "oct-ia-no-sabe-reel",                "problema",   "Máster",    "Comenta GUIA", "CAMBIO 5-oct (Dayana): reemplaza al reel del tutor, que no se grabó (pasa al banco de reserva). «Una IA no sabe cuándo no sabe», ya grabado. La palabra es GUIA: añadir el reel a la campaña «Guía Revit» de OpenReply. No se promociona en historias."),
    (8,  "oct-hola-soy-gabriel-carrusel",      "objeción",   "Máster",    "Comenta NIVEL", "Historia del creador (pedido de Dayana, 30-sep): estructura del carrusel de Juan Lombana «Si acabas de llegar: hola, soy Juan», con marca DMA y fotos reales de Gabriel. Responde la objeción de confianza («¿quién enseña?»). Se FIJA en el perfil: es la bienvenida de los que llegan con el dato del viernes 9. Gabriel confirma los 7 datos personales marcados."),
    (9,  "oct-dato-deriva-post",               "problema",   "Acero",     "Comenta ACERO", "Post con dato de cálculo verificable (el formato que más guarda la cuenta). El post de clases grabadas (oct-tutor-dip-post-fb) pasó al Mié 14."),
    (10, "oct-clase-chatgpt-seguidor-reel",    "problema",   "Máster",    "Comenta GUIA", "SÁBADOS DE CLASE REAL (8-oct, Dayana): fragmento de una clase del Máster BIM + IA sacado de Vimeo, ya editado (plantilla «Tres bandas»). No hay que grabar. GUIA: añadir el reel a la campaña «Guía Revit» de OpenReply."),
    (12, "oct-acusa-ia-calculo-carrusel",      "problema",   "Máster",    "Comenta NIVEL", "Acusación. Capturas reales de Revit/Robot."),
    (13, "oct-testimonio-acero-reel",          "testimonio", "Acero",     "Comenta ACERO", "CAMBIO 6-oct: pasa del Mié 28 al Mar 13 (intercambio con el reel de COTIZA). Alumno real con permiso por escrito; si no se consigue o no se puede grabar (Daniela de viaje), sale la pieza de reserva descrita en la pieza."),
    (14, "oct-tutor-dip-post-fb",              "solución",   "Diplomado", "Comenta DIPLOMADO (si no está montada: DM)", "CAMBIO 6-oct: el post de clases grabadas pasa del Vie 9 al Mié 14 y sale en Instagram y Facebook, porque el reel del ranking se movió al Vie 23."),
    (15, "oct-cotiza-carrusel",                "solución",   "Cotizador", "Comenta COTIZA", "EXTRA lead magnet (jueves)."),
    (16, "oct-ang4-naves-rechazadas-post",     "problema",   "Acero",     "Comenta ACERO", "Ángulo 4 de compradores: los proyectos que rechazas."),
    (17, "oct-clase-onefilter-reel",           "solución",   "Máster",    "Comenta NIVEL", "SÁBADOS DE CLASE REAL: tip de OneFilter (DiRoots) sacado de una clase del Máster, ya editado (estilo tutorial). «Gratis» solo para OneFilter; no decir que exportar a Excel es gratis."),
    (19, "oct-workshop-antes-ahora-carrusel",  "solución",   "Workshop → Máster", "Comenta WORKSHOP (si no está montada: DM)", "CAMBIO 8-oct (Dayana): carrusel del workshop del jue 22 con el formato «Antes / Ahora» del post de AECODE del 7-oct. Capturas REALES de Revit 2027 (Assistant y servidor MCP, de solo lectura). Reemplaza al carrusel del ranking, que pasa a reserva y vuelve si no hay capturas a tiempo."),
    (20, "oct-obj-tiempo-reel",                "objeción",   "Máster",    "Comenta NIVEL", "Objeción de tiempo. Graba Gabriel."),
    (21, "oct-acusa-ia-calculo-reel",          "solución",   "Máster",    "Comenta NIVEL", "La IA ordena, tú decides. Graba Gabriel."),
    (22, "oct-obj-certificado-carrusel",       "objeción",   "Máster",    "Comenta NIVEL", "Objeción de certificado. Dayana confirma la lista de certificados antes de diseñar."),
    (23, "oct-ranking-software-estructural-reel", "problema", "Máster",   "Comenta NIVEL", "CAMBIO 6-oct: pasa del Mié 14 al Vie 23. Ranking con tablero físico; se graba cuando vuelva Daniela."),
    (23, "oct-ang3-bim-se-exige-post",         "problema",   "Máster",    "Comenta NIVEL", "Ángulo 3: BIM ya se exige."),
    (24, "oct-clase-addin-no-piensa-reel",     "problema",   "Máster",    "Comenta GUIA", "SÁBADOS DE CLASE REAL: «los add-ins solo ejecutan, no piensan», de una clase del Máster, ya editado (pizarra + clase). GUIA: añadir el reel a la campaña «Guía Revit» de OpenReply."),
    (26, "oct-ang8-obra-software-carrusel",    "problema",   "Acero",     "Comenta ACERO", "Ángulo 8: de la obra al software. Filtra a quien quiere soldar."),
    (27, "oct-obj-cursos-youtube-reel",        "objeción",   "Acero",     "Comenta ACERO", "Objeción: muchos cursos, ninguno aplicable. Graba Gabriel."),
    (28, "oct-cotiza-reel",                    "problema",   "Cotizador", "Comenta COTIZA", "CAMBIO 6-oct: pasa del Mar 13 al Mié 28 (intercambio con el testimonio). COTIZA ya se lanzó el Mar 13 (comunidades y LinkedIn) y el Jue 15 (carrusel): este reel se suma a la campaña que exista. Se graba cuando vuelva Daniela."),
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
    if p.get("mensaje_bienvenida"):
        cfg.append(["Mensaje de bienvenida (WhatsApp)", p["mensaje_bienvenida"]])
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
    ["7 · Apagar las 3 campañas «[25AGOSTO] LEAD MAGNETS»",
     "Auditoría de septiembre (Meta, 31-ago al 29-sep): $77 gastados entre las tres, 0 leads de formulario y 7 conversaciones. Ese presupuesto pasa a ACERO. Si se quiere pauta para un recurso, se hace con el post del dato de cálculo (el mejor orgánico del año), no con los anuncios actuales."],
    ["8 · Reunión del 5-oct",
     "Se reactivan los anuncios de septiembre y se pausan todos los de enero a julio. No se suben anuncios NUEVOS de venta hasta probar los actuales, y Gabriel graba solo contenido de valor para el feed. Formulario de ACERO con preguntas que filtren a quien no tiene trabajo ni presupuesto. Ventas pone la fuente a cada oportunidad."],
    ["REGLA DE ORO", "El Máster no lleva precio en ninguna pieza. ACERO lleva $225 solo en pauta y en correo a la lista propia. Un texto por ángulo, en una sola campaña."],
]

LEAD_MAGNETS = {
    "nota": "Octubre sale con UN lead magnet nuevo (COTIZA) y ninguno más. Los de respaldo ya existen y funcionan. Si en la semana 2 uno no genera DM, se reemplaza por otro de esta lista, no por uno nuevo.",
    "nuevo": [{"nombre": "Cotizador de Honorarios Estructurales", "palabra": "COTIZA",
               "estado": "Funnel en GHL montado y probado por Dayana (30-sep). Entra en el workflow de recursos de Ester (rama COTIZADOR: acceso-cotizador-honorarios, correo de acceso, comunidad y oportunidad en NUEVO LEAD MAGNET) y en su workflow propio (lead-cotizador, aviso interno, membresía y secuencia S5). OpenReply se monta al publicar el carrusel del Jue 15 (el reel pasó al Mié 28, cambio del 6-oct). Falta volver a pegar ghl-landing.html con el formulario nativo.",
               "piezas": ["oct-cotiza-carrusel", "oct-blog-cobrar-diseno-estructural", "oct-cotiza-reel", "oct-cotiza-historias"],
               "puente": "Especialización en Acero / Diplomado en Estructuras (secuencia de correo S5)"}],
    "respaldo": [
        {"nombre": "Calculadora de Zapatas", "palabra": "ZAPATA", "por_que": "El que más leads trajo (162 etiquetados) y alimenta ACERO. El que mejor convierte: 169 al bot → 151 con acceso (89 %)."},
        {"nombre": "5 verificaciones en acero", "palabra": "ACERO", "por_que": "Su post DM157 es el mejor PROMO de la cuenta (159 comentarios, 356 guardados). CTA de todas las piezas de ACERO. Auditoría: 174 leads y 43 con acceso (25 %). El flujo funciona (revisado el 30-sep): es gente que no llena el formulario. Tarea para subir ese 25 % en el checklist."},
        {"nombre": "Test de Nivel BIM", "palabra": "NIVEL", "por_que": "Puerta al Máster y CTA de todas sus piezas. El flujo funciona (revisado el 30-sep); el acceso se marca con acceso-nivelbim. En septiembre casi nadie la pidió (2 al bot): octubre es la primera prueba de volumen."},
        {"nombre": "Memoria de cálculo", "palabra": "MEMORIA", "por_que": "Vivo: 34 al bot → 33 con acceso. Se usa solo si una pieza de cálculo lo pide. ⚠ Hoy lo escuchan 3 automatizaciones: dejar una sola antes de usarlo."},
    ],
    "retirados": [{"nombre": "Pack de 5 scripts de Dynamo", "palabra": "DYNAMO", "por_que": "Auditoría de septiembre: su reel sacó 0 comentarios y OpenReply falla 4 de 4 porque GHL también contesta. El recurso sigue en /recursos; la palabra sale de los CTA."},
                  {"nombre": "Guía Revit + ChatGPT", "palabra": "CHATGPT", "por_que": "No tiene campaña ni workflow que conteste: nadie recibe nada. La guía se pide con GUIA (OpenReply), que es la palabra que usa el reel del Mié 7."}],
    "mapa_cta": [
        {"palabra": "NIVEL", "fecha": "Jue 8 (historia del creador), Lun 12, Mar 20, Mié 21, Jue 22, Vie 23 (ranking y post), Vie 30", "producto": "Máster"},
        {"palabra": "ACERO", "fecha": "Vie 9, Mar 13 (testimonio), Vie 16, Lun 26, Mar 27, Jue 29", "producto": "Acero"},
        {"palabra": "COTIZA", "fecha": "Mar 13 (comunidades y LinkedIn), Jue 15 (carrusel), Sáb 17 (blog), Mié 28 (reel e historias)", "producto": "Cotizador → Acero/Diplomado"},
        {"palabra": "DIPLOMADO", "fecha": "Lun 5 (lanzamiento del tutor) y Mié 14 (post de clases grabadas)", "producto": "Diplomado · montar antes del 5 o CTA a DM"},
        {"palabra": "GUIA", "fecha": "Mié 7 (reel «Una IA no sabe cuándo no sabe», cambio del 5-oct)", "producto": "Guía Revit + ChatGPT (OpenReply, campaña «Guía Revit») → Máster"},
        {"palabra": "WORKSHOP", "fecha": "Lun 19 (carrusel «Antes / ahora» e historias con cuenta regresiva)", "producto": "Workshop Revit + IA del jue 22-oct → cita de ruta del Máster · la contesta GHL con el enlace de la landing; montar antes del 19 o CTA a DM"},
    ],
}

# ───────────────────────── DESTACADAS (las actualiza Daniela) ─────────────────────────
# Las cinco de siempre. Cada historia de octubre dice en cuál se guarda (columna
# «destacada» del Grupo 5). Lo que se QUITA sale de la auditoría de septiembre:
# CHATGPT no la contesta nadie y DYNAMO falla en OpenReply.
DESTACADAS = [
    {"destacada": "🔩 ACERO", "que_va": "Verificaciones, conexiones, casos de obra al software y la venta de los jueves de Acero.",
     "agregar": ["oct-hist-1009", "oct-hist-1015", "oct-hist-1016", "oct-hist-1026", "oct-hist-1029"],
     "quitar": "Frames con fechas o cupos ya vencidos, y cualquier frame que muestre precio."},
    {"destacada": "🎯 BIM + IA", "que_va": "Máster, test de nivel, ranking de software, el tutor de IA del Diplomado.",
     "agregar": ["oct-hist-1005", "oct-hist-1007", "oct-tutor-dip-historias", "oct-hist-1012", "oct-hist-1019", "oct-hist-1022", "oct-hist-1023", "oct-hist-1030"],
     "quitar": "Frames que piden comentar CHATGPT (nadie la contesta) y los que prometen funciones de IA en Revit que no existen."},
    {"destacada": "🎁 HERRAMIENTAS", "que_va": "Los recursos gratis: cotizador, calculadora de zapatas, memoria de cálculo, 5 verificaciones, test de nivel.",
     "agregar": ["oct-cotiza-historias"],
     "quitar": "Frames que piden DYNAMO o CHATGPT: se cambian por un sticker de enlace a /recursos o se borran."},
    {"destacada": "👥 COMUNIDAD", "que_va": "Detrás de cámara y las preguntas de la comunidad.",
     "agregar": ["oct-hist-1006", "oct-hist-1020", "oct-hist-1027"],
     "quitar": "Recaps de más de 3 meses."},
    {"destacada": "⭐ ALUMNOS", "que_va": "Testimonios reales con permiso.",
     "agregar": ["oct-hist-1028 (solo si sale el testimonio real; si sale la reserva, va a ACERO)"],
     "quitar": "Nada, salvo que un alumno retire su permiso."},
]
DESTACADA_DE = {i.split(" ")[0]: d["destacada"] for d in DESTACADAS for i in d["agregar"]}


CHECKLIST = [
    {"tarea": "WORKSHOP: montar en GHL el disparador de la palabra WORKSHOP (Instagram y Facebook) con el enlace de la landing de registro del workshop, y probarlo desde una cuenta ajena.", "desbloquea": "El carrusel del Lun 19 y sus historias (si no está, el CTA pasa a «Escríbenos por DM»)", "cuando": "antes del 19-oct", "para": "Patricio · Ester y Aylin"},
    {"tarea": "Capturas reales del carrusel «Antes / ahora» desde Revit 2027: panel del Autodesk Assistant respondiendo, Claude Desktop conectado por el MCP respondiendo con datos del modelo, una tabla de planificación filtrada a mano, láminas hechas a mano y el Assistant creando una lámina. Modelo de DMA o del Diplomado, sin datos de clientes.", "desbloquea": "El carrusel del Lun 19 (sin capturas vuelve el ranking)", "cuando": "antes del 16-oct (puede salir del ensayo del jue 15)", "para": "Gabriel"},
    {"tarea": "DECIDIDO (Dayana, 30-sep): las palabras con embudo las contesta GHL. Pausar en OpenReply las campañas MEMORIA VERIFICABLE, MEMORIA VERIFICABLE copy, MEMORIA DE CÁLCULO, PACK DYNAMO, 5 ERRORES REVIT (BIM/IA) y CHECKLIST NAVISWORKS (BIM/IA). OpenReply queda para las palabras sueltas (TUTORIAL, GUIA, PARTE) y para COTIZA en Instagram; COTIZA en Facebook la contesta GHL.", "desbloquea": "Que los DM de MEMORIA, DYNAMO y BIM/IA no fallen («no eres el dueño de la conversación»)", "cuando": "antes del lunes 5", "para": "Dayana (OpenReply)"},
    {"tarea": "ACERO: subir el 25 % que llega al acceso. El flujo funciona (revisado en GHL el 30-sep): la caída es de gente que recibe el DM y no llena el formulario, y el DM de Instagram solo se entrega dentro de las 24 h del comentario. Acortar el formulario de la landing de las 5 verificaciones y sumar un recordatorio (correo o WhatsApp) a quien tiene lead-acero-verificaciones sin acceso-verificacion.", "desbloquea": "Las 6 piezas de octubre que piden ACERO (la primera el Vie 9)", "cuando": "antes del 9-oct", "para": "Ester y Aylin"},
    {"tarea": "Quitar de GHL la duplicidad de accesos: «✅ OLD Acceso y Descarga PDF Recursos Gratis» sigue publicado (61 inscritos) junto al NEW y puede mandar el acceso dos veces. Comprobar y despublicar el OLD si ya no lo usa nada.", "desbloquea": "Que nadie reciba dos correos de acceso", "cuando": "antes del lunes 5", "para": "Ester y Aylin"},
    {"tarea": "Llenar los 7 datos personales del carrusel «Si acabas de llegar: hola, soy Gabriel» (edad, familia, fan de, origen, el momento del cambio, año de fundación y número REAL de alumnos) y juntar las fotos reales: clase, obra, época de AutoCAD/Excel.", "desbloquea": "El carrusel del Jue 8, que se fija en el perfil", "cuando": "antes del 6-oct", "para": "Gabriel"},
    {"tarea": "Apagar las 3 campañas «[25AGOSTO] LEAD MAGNETS» y pasar ese presupuesto a ACERO.", "desbloquea": "$77 al mes que hoy no traen leads", "cuando": "antes del lunes 5", "para": "Olympus"},
    {"tarea": "Confirmar que las tareas automáticas del repositorio volvieron solas (historias cada 4 h a los :17; métricas lunes y viernes). Estuvieron paradas del 27 al 30-sep por la suspensión de GitHub.", "desbloquea": "Que la auditoría de octubre tenga las historias de todos los días", "cuando": "1-oct", "para": "Dayana"},
    {"tarea": "Limpiar las 5 destacadas del perfil: quitar los frames que piden CHATGPT o DYNAMO, los que tienen fechas, cupos o precios vencidos, y revisar que las portadas sigan iguales y legibles.", "desbloquea": "Que quien llega nuevo al perfil no pida un recurso que nadie contesta", "cuando": "antes del lunes 5", "para": "Daniela"},
    {"tarea": "Cada viernes, guardar en su destacada las historias de la semana (columna «Destacada» del Grupo 5 y bloque «destacadas» del calendario).", "desbloquea": "Destacadas al día sin una jornada de limpieza a fin de mes", "cuando": "viernes 9, 16, 23 y 30", "para": "Daniela"},
    {"tarea": "Cotizador: borrar los contactos de prueba («Prueba Cotizador E2E» y «Prueba Cotizador»), revisar por qué el contacto de prueba figura con 12 productos de membresía (¿la oferta o la Comunidad Design Premium dan de más?) y mirar el botón y el enlace de la plantilla «Acceso Pack Dynamo_01». La landing con formulario nativo y la prueba de punta a punta ya están HECHAS (30-sep).", "desbloquea": "Que el cotizador dé solo lo que promete", "cuando": "antes del 13-oct", "para": "Dayana"},
    {"tarea": "Gabriel revisa las horas de ejemplo del cotizador (app.html, ENTREGABLES).", "desbloquea": "Reel del Mar 13 y carrusel del Jue 15", "cuando": "antes del 12-oct", "para": "Gabriel"},
    {"tarea": "PAUSA DE GRABACIÓN (6-oct): Daniela viaja y no se graban videos nuevos hasta que vuelva. Quedan por grabar: testimonio o su reserva (Mar 13), reels del 20 y 21, ranking (Vie 23, con tablero físico), reel del 27 y reel de COTIZA (Mié 28). Si al volver no da el tiempo, se reemplazan por piezas que no necesiten cámara.", "desbloquea": "Semanas 2 a 4 del feed", "cuando": "cuando vuelva Daniela", "para": "Gabriel y Daniela"},
    {"tarea": "Día de grabación 2: reels del 27 y 28 (testimonio o pieza de reserva) + capturas de Robot para el carrusel del 29.", "desbloquea": "Semana 4 del feed", "cuando": "Jue 22-oct", "para": "Gabriel"},
    {"tarea": "Conseguir un alumno de ACERO con permiso por escrito para el testimonio.", "desbloquea": "Reel del Mié 28", "cuando": "antes del 21-oct", "para": "Dayana / soporte"},
    {"tarea": "Confirmar la lista exacta de certificados del Máster y pasar los escaneos oficiales.", "desbloquea": "Carrusel del Jue 22", "cuando": "antes del 19-oct", "para": "Dayana"},
    {"tarea": "Montar la palabra DIPLOMADO (o dejar el CTA en DM).", "desbloquea": "Lanzamiento del tutor 5–9 oct", "cuando": "antes del 5-oct", "para": "Patricio"},
    {"tarea": "Crear la campaña COTIZA en OpenReply atada al carrusel del Jue 15 al publicarlo (y la de Facebook en GHL); probar con una cuenta ajena. El Mié 28 se le añade el reel.", "desbloquea": "Que el comentario COTIZA reciba el DM", "cuando": "15-oct al publicar, y 28-oct", "para": "Dayana (las campañas de OpenReply las hace ella)"},
    {"tarea": "Pauta: aplicar las 6 decisiones de la sección de publicidad (WhatsApp de ACERO, pausar anuncios cansados, presupuesto, optimización del Máster, borradores, filtros).", "desbloquea": "Que la pauta vuelva a traer compradores", "cuando": "semana del 5-oct", "para": "Olympus"},
    {"tarea": "Subir los anuncios nuevos de octubre como reemplazo de los cansados, SOLO después de probar los de septiembre (reunión del 5-oct). Los del tutor esperan al reel, que no está grabado.", "desbloquea": "Pauta de las semanas 3 y 4", "cuando": "Lun 19-oct", "para": "Olympus"},
    {"tarea": "Añadir el reel del Mié 7 («Una IA no sabe cuándo no sabe») a la campaña «Guía Revit» de OpenReply (palabra GUIA, dispara también por DM) y comprobar que solo esa campaña lo escucha.", "desbloquea": "Que el comentario GUIA del reel reciba la guía", "cuando": "Mié 7, al publicar", "para": "Dayana (OpenReply)"},
    {"tarea": "Revisión semanal del 5-oct: cada post con dato de cálculo cierra con una palabra de recurso (el de la fórmula del acero sacó 91 guardados y solo 10 comentarios).", "desbloquea": "Que los datos verificables también traigan leads", "cuando": "todo octubre", "para": "equipo de contenido"},
    {"tarea": "Revisión semanal del 5-oct: comprobar que los comentarios de Facebook reciben el DM del recurso. El post de MEMORIA del 1-oct sacó 192 comentarios en Facebook contra 32 en Instagram.", "desbloquea": "Que la conversación de Facebook llegue al bot", "cuando": "semana del 5-oct", "para": "Patricio / Dayana"},
    {"tarea": "Reunión del 5-oct: historias de 4 frames como máximo por día (ya aplicado en la matriz).", "desbloquea": "Retención de las historias por encima del 60 %", "cuando": "desde el Lun 5", "para": "Daniela"},
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
            "PALABRAS DE COMENTARIO — SOLO ESTAS: NIVEL (Máster), ACERO, ZAPATA, MEMORIA, COTIZA (nueva), DIPLOMADO (lanzamiento del tutor, si está montada) y GUIA (reel del Mié 7, cambio del 5-oct; la contesta OpenReply). CHATGPT queda fuera: no tiene quien conteste. BIM e IA siguen siendo el bot de ventas del Máster.",
            "UNA PALABRA, UNA AUTOMATIZACIÓN (auditoría de septiembre: MEMORIA con dos campañas de OpenReply y un workflow de GHL, 30 DM fallidos; DYNAMO, 4 de 4). DECIDIDO por Dayana el 30-sep: las palabras con embudo (ZAPATA, ACERO, NIVEL, MEMORIA, DYNAMO y BIM/IA, el bot de ventas) las contesta GHL; OpenReply queda para las palabras sueltas (TUTORIAL, GUIA, PARTE) y para COTIZA en Instagram. Las campañas de OpenReply las hace Dayana.",
            "BIM e IA NUNCA como palabra de un recurso: son el bot de ventas del Máster (el checklist de Navisworks falló 3 de 5).",
            "DYNAMO fuera de los CTA de octubre: 0 comentarios en su reel y falla en OpenReply.",
            "LOS DOS FORMATOS GANADORES DE SEPTIEMBRE se repiten: el dato de cálculo verificable (cuantía mínima: 44.589 vistas, 146 comentarios, 163 seguidores) y el tutorial paso a paso con palabra (plano 2D → BIM: 99 comentarios, 47 DM). Anunciar un producto («ahora tiene X») nunca va solo: siempre detrás de un problema.",
            "CAMBIOS DEL 8-OCT: el Lun 19 sale el carrusel del workshop «Antes / ahora: Revit con IA» (formato del post de AECODE del 7-oct que le gustó a Dayana, CTA WORKSHOP); el carrusel del ranking pasa a reserva y las historias del 19 promocionan el workshop con cuenta regresiva.",
            "CAMBIOS DEL 6-OCT: Daniela viaja y no se graban videos nuevos hasta que vuelva. El Mié 7 sale el reel de valor 5 de septiembre («Una IA no sabe cuándo no sabe»). Testimonio de Acero al Mar 13 y reel de COTIZA al Mié 28; ranking al Vie 23; post de clases grabadas al Mié 14. Las historias de la semana 1 se corren un día y ninguna promociona un reel que no sale ese día.",
            "CAMBIOS DEL 5-OCT (revisión semanal, auditoría orgánica de septiembre y reunión de cierre): historias de 4 frames como máximo; cada dato de cálculo cierra con palabra de recurso; los posts del recurso se cuidan también en Facebook (192 comentarios del post de MEMORIA); el reel del tutor queda aplazado hasta que se grabe y en su lugar sale «Una IA no sabe cuándo no sabe», que no se promociona en historias.",
            "UNA venta por semana, el jueves, en historias: 8 tutor · 15 objeción de ACERO · 22 espejo del Máster · 29 ACERO por dentro.",
            "EL MÁSTER NUNCA LLEVA PRECIO. ACERO lleva $225 solo en pauta y en correo a la lista propia.",
            "Visuales = capturas reales de Revit/Robot y cámara de Gabriel. Imagen con IA solo con aprobación y costo a la vista.",
            "Reels de menos de 30 s (en esta cuenta rinden más del doble que los de 30–60 s).",
        ],
        "checklist_tareas": CHECKLIST,
        "publicidad": {
            "nota": "Primero se corrige lo que hace perder leads (7 decisiones: las 6 del diagnóstico de Dayana y la de la auditoría de septiembre); después los anuncios nuevos reemplazan a los cansados. Fichas completas por anuncio abajo.",
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
             "descripcion": "Lunes a viernes, 3–4 frames. Cada día abre la puerta a la pieza del feed; los jueves 15, 22 y 29 son el único slot de venta de la semana.",
             "reglas": ["El sticker es el CTA.", "Nunca precio ni «inscríbete».", "Máximo 4 frames (auditoría orgánica de septiembre y reunión del 5-oct).", "Las respuestas llegan como DM: se contestan a mano.", "Cada historia dice en qué destacada se guarda. Daniela las guarda cada viernes (ver «destacadas»)."],
             "calendario": [{**x, **({"destacada": DESTACADA_DE[x["id"]]} if x["id"] in DESTACADA_DE else {})} for x in filas_de("GRUPO 5")]},
        ],
        "lead_magnets": LEAD_MAGNETS,
        "destacadas": {"responsable": "Daniela", "nota": "Las cinco de siempre. Se limpian antes del lunes 5 y se alimentan cada viernes con las historias de la semana.", "lista": DESTACADAS},
        "piezas": [],
        "pauta": [],
        "banco_reserva": [i for i in ["oct-ranking-perfil-bim-carrusel", "oct-tutor-dip-reel", "ago-derivas-deformaciones", "ago-tip-revit-ia", "ago-revit-ia-futuro"] if i in G],
        "correos": correos(),
        "auditoria_previa": {"mes": "2026-09", "artefacto": "https://claude.ai/artifact/BNSfUg4TDFQjibVyN4ATt8",
                             "archivos": ["matriz-viral/auditorias/2026-09-hallazgos.md", "matriz-viral/auditorias/2026-09-auditoria-mes.json"],
                             "resumen": "Funcionó: el dato de cálculo verificable y el tutorial paso a paso con palabra. No funcionó: los anuncios del tutor, Dynamo, el carrusel de las 4 puertas y las campañas de pauta de lead magnets. Roto: MEMORIA y DYNAMO con dos automatizaciones. ACERO funciona pero el 75 % no llena el formulario. NIVEL funciona: el «0 accesos» era un error de medición, corregido el 30-sep."},
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
        "artefactos": {"artefacto": "https://claude.ai/artifact/6Q8f77WzYEqSMExS1h9Mx3", "pages": "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/entregables/matriz-octubre-artefacto.html", "json_app": "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/entregables/matriz-octubre-2026-COMPLETA.json", "word": "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/entregables/Matriz-Contenido-Octubre-2026-DMA.docx"},
    }
    json.dump(cal, open(M / "calendario-octubre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok ·", len(feed), "feed ·", dict(fmt), dict(inten), "·", sum(len(g["calendario"]) for g in cal["grupos"]), "entradas")


if __name__ == "__main__":
    main()
