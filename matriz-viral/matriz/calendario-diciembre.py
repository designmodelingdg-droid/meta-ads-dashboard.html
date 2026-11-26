#!/usr/bin/env python3
"""Construye calendario-diciembre.json desde las piezas de guiones-completos.json.

    python3 matriz-viral/matriz/calendario-diciembre.py

Igual que octubre y noviembre: el calendario solo ORDENA piezas; el contenido vive en
guiones-completos.json (ids dic-* y ene-*). Diciembre va del martes 1 de diciembre de
2026 al miércoles 6 de enero de 2027. Los días del 1 al 6 de enero van en ESTE archivo
con su fecha real: scripts/verificar_matriz_mes.py y build_matriz_mes.py leen un
calendario por mes (calendario-<mes>.json) y el período cruza el cambio de año.

Método del mes (brief BIM 23-nov, BRIEF-DICIEMBRE-SINTOMATICO.md): problema primero,
dato técnico verificable y comparativo, y una pregunta que obliga a comentar. La palabra
del lead magnet solo cierra la pieza; el DM entrega una mini-solución y termina con una
pregunta que abre la conversación de venta.
"""
import datetime
import json
import pathlib
from collections import Counter

M = pathlib.Path(__file__).resolve().parent
G = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MES_CORTO = {12: "dic", 1: "ene"}


def etiqueta(f):
    d = datetime.date.fromisoformat(f)
    return f"{DIAS[d.weekday()]} {d.day} {MES_CORTO[d.month]}"


def pieza(pid):
    if pid not in G:
        raise SystemExit(f"FALTA en guiones-completos.json: {pid}")
    return G[pid]


# ───────────────────────── GRUPO 1 · FEED ─────────────────────────
# (fecha, id, intención para el verificador, intención del mes, nota)
# Intención del mes: problema / referencia / venta (60/20/20 pedido el 23-nov).
# El verificador cuenta «problema / solución / objeción-testimonio»: la referencia técnica
# comparativa se registra como «solución» y la venta como «objeción» o «testimonio».
FEED = [
    ("2026-12-01", "dic-sigues-modelando-carrusel", "problema", "problema",
     "Abre el mes. Síntoma del ingeniero empleado (banco del brief). Pregunta con número para no disparar NIVEL por error. + VENTA SUAVE: «comenta MÁSTER» para información."),
    ("2026-12-02", "dic-reedit-zapata-suelos-reel", "problema", "problema",
     "RE-EDICIÓN del ganador de noviembre (DfmwQgAjiDk, 81 comentarios) con gancho nuevo: «Copiaste la zapata del proyecto anterior». Única palabra en GHL."),
    ("2026-12-03", "dic-reedit-uniones-viga-columna-reel", "problema", "problema",
     "RE-EDICIÓN de la chuleta del 4-nov (DfU1jwSj6g6, 55 guardados) con gancho nuevo: «La viga pasó. La unión no.». + VENTA SUAVE: «comenta TEMARIO»."),
    ("2026-12-04", "dic-testimonio-acero-post", "testimonio", "venta",
     "Testimonio GUARDADO de Acero: reel del 23-oct (De2JwdYlfH9), «Ustedes han sido una gran solución». Palabra de venta TEMARIO (DM con el temario de Acero)."),
    ("2026-12-07", "dic-cuantia-aci-nec-carrusel", "solución", "referencia",
     "Referencia comparativa ACI 318-19 vs NEC (formato del ganador «El 1 % de cuantía», 152 comentarios). Regla 0."),
    ("2026-12-08", "dic-reedit-simbologia-niveles-reel", "problema", "problema",
     "RE-EDICIÓN del reel más comentado del año (DeubXmFlIDE, 603 comentarios) con gancho nuevo: «N+3,00 o N+2,95: ¿cuál vale?»."),
    ("2026-12-09", "dic-gabriel-memoria-devuelta-reel", "problema", "problema",
     "Gabriel a cámara (grabación G-01). Síntoma del calculista: «Te devolvieron la memoria y el cálculo estaba bien»."),
    ("2026-12-10", "dic-selfie-chatgpt-firma-reel", "problema", "problema",
     "REEL SELFIE (G-06a, Gabriel con el teléfono, sin protocolo). Síntoma: «el número de ChatGPT lleva tu firma». Semana de 5 piezas por el pedido de selfies."),
    ("2026-12-11", "dic-honorarios-revisiones-carrusel", "problema", "problema",
     "Síntoma del consultor independiente. Sale el viernes para no pegar 3 videos seguidos. + VENTA SUAVE: «comenta TEMARIO»."),
    ("2026-12-14", "dic-deflexiones-l360-carrusel", "solución", "referencia",
     "Referencia comparativa (IBC 2021, tabla 1604.3). Regla 0."),
    ("2026-12-15", "dic-gabriel-ratios-robot-reel", "problema", "problema",
     "Gabriel + pantalla de Robot (grabación G-02). Caso real de un alumno, sin nombre si no hay permiso. + VENTA SUAVE: «comenta TEMARIO»."),
    ("2026-12-16", "dic-ws-clip-niveles-duplicados-reel", "problema", "problema",
     "Clip del workshop (brief 4b). El único de los 4 con síntoma; falta subtitular y escuchar el audio."),
    ("2026-12-17", "dic-obj-tiempo-master-carrusel", "objeción", "venta",
     "Objeción real («no tengo tiempo», 3 de 5 compradores). Máster sin precio: «comenta MÁSTER» → WhatsApp para agendar. Cohorte de febrero."),
    ("2026-12-18", "dic-selfie-revit-no-bim-reel", "problema", "problema",
     "REEL SELFIE (G-06b). Síntoma: «Sabes Revit, pero no sabes BIM». NIVEL + VENTA SUAVE «comenta MÁSTER». Semana de 5 piezas por el pedido de selfies."),
    ("2026-12-21", "dic-doble-trabajo-autocad-excel-carrusel", "problema", "problema",
     "RITMO DE FIESTAS (2 por semana). Síntoma del contratista con AutoCAD + Excel."),
    ("2026-12-23", "dic-reedit-5-cimentaciones-reel", "solución", "referencia",
     "RE-EDICIÓN del 19-oct (Der2lsgjwu5, 103 comentarios) con gancho nuevo. Pieza de guardado antes de Navidad, sin venta."),
    ("2026-12-25", "dic-navidad-post", "comunidad", "saludo de marca",
     "FECHA ESPECIAL (Dayana, 23-nov): saludo de Navidad cálido, imagen DG 2026, SIN VENTA. Fuera de cuota."),
    ("2026-12-28", "dic-coordinar-sin-saber-carrusel", "problema", "problema",
     "RITMO DE FIESTAS. Síntoma del que le piden coordinar. + VENTA SUAVE: «comenta MÁSTER»."),
    ("2026-12-30", "dic-peso-varilla-post", "solución", "referencia",
     "Referencia guardable de Año Nuevo. Sale el 30 (sin venta el 31 y el 1)."),
    ("2026-12-31", "dic-fin-de-ano-post", "comunidad", "saludo de marca",
     "FECHA ESPECIAL (Dayana, 23-nov): cierre de año y propósito 2027, imagen DG 2026, sin venta dura (solo el test de NIVEL opcional). Fuera de cuota."),
    ("2027-01-04", "ene-obj-cursos-no-sirvieron-post", "objeción", "venta",
     "REGRESO. Objeción «ya hice cursos» → probar el módulo gratis (DIPLOMADO). El Diplomado BIM es grabado: «empiezas hoy». Cita guardada de Jorge Aguirre."),
    ("2027-01-05", "ene-selfie-acero-en-enero-reel", "objeción", "venta",
     "REEL SELFIE (G-06c). Objeción de tiempo: «En enero empiezo con acero… y ya es enero». Venta suave: «comenta TEMARIO»."),
    ("2027-01-06", "ene-testimonio-master-post", "testimonio", "venta",
     "Testimonio GUARDADO de Albino Piñeiro (egresado del Diplomado BIM; correo GHL «Seg 05 - Testimonios cierre»): el siguiente paso es el Máster, cohorte de febrero. Sin precio; «comenta MÁSTER»."),
]


def fila_feed(f, pid, intencion, intencion_dic, nota):
    p = pieza(pid)
    emb = p.get("embudo") or {}
    return {"fecha": etiqueta(f), "fecha_iso": f, "hora": p.get("fecha", f"{f}T15:00:00Z"), "semana": p.get("semana"), "id": pid,
            "titulo": p.get("titulo"), "tipo": p.get("tipo"), "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
            "redes": p.get("redes"), "intencion": intencion, "intencion_dic": intencion_dic, "producto": emb.get("producto_destino") or p.get("producto"),
            "cta": (p.get("cta") or {}).get("instagram", ""), "palabra": emb.get("palabra"), "canal_dm": emb.get("canal_dm"),
            "cta_info": (emb.get("cta_info") or {}).get("palabra"),
            "estado": p.get("estado"), "nota": nota, **({"fuera_de_cuota": True} if p.get("fuera_de_cuota") else {})}


def de_periodo(p):
    return p["id"].startswith(("dic-", "ene-")) and str(p.get("fecha_iso", "")) >= "2026-12-01"


def filas_de(grupo_prefijo):
    out = []
    for p in G.values():
        if de_periodo(p) and str(p.get("grupo", "")).startswith(grupo_prefijo):
            out.append({"fecha": etiqueta(p["fecha_iso"]), "fecha_iso": p["fecha_iso"], "hora": p.get("fecha"), "semana": p.get("semana"), "id": p["id"],
                        "titulo": p.get("titulo"), "tipo": p.get("tipo"), "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
                        "redes": p.get("redes"),
                        "idea": {"titulo": p.get("titulo"), "formato": p.get("formato_detalle") or p.get("formato"), "desarrollo": p.get("hook") or ""},
                        **({"cuenta": p["cuenta"]} if p.get("cuenta") else {}),
                        **({"gabriel_a_camara": True} if p.get("gabriel_a_camara") else {}),
                        **({"venta": True} if p.get("venta") else {}),
                        **({"destacada": p["destacada"]} if p.get("destacada") else {})})
    return sorted(out, key=lambda x: x["fecha_iso"])


def correos():
    out = []
    for p in G.values():
        if de_periodo(p) and p.get("grupo") == "Correos":
            cuerpo = p.get("cuerpo")
            out.append({"fecha": f"{etiqueta(p['fecha_iso'])} · {str(p.get('semana', '')).split(' (')[0]}", "fecha_iso": p["fecha_iso"], "id": p["id"],
                        "nombre": p.get("titulo"), "asunto": p.get("asunto"), "preencabezado": p.get("preencabezado"),
                        "segmento": p.get("segmento"), "objetivo": p.get("hook") or "",
                        "cuerpo": "\n\n".join(cuerpo) if isinstance(cuerpo, list) else (cuerpo or ""), "condicion": p.get("condicion") or ""})
    return sorted(out, key=lambda x: x["fecha_iso"])


def youtube_largos():
    out = []
    for p in sorted((p for p in G.values() if de_periodo(p) and str(p.get("grupo", "")).startswith("GRUPO 6")), key=lambda p: p["fecha_iso"]):
        y = p["youtube"]
        out.append({"fecha": etiqueta(p["fecha_iso"]), "fecha_iso": p["fecha_iso"], "id": p["id"], "titulo": y["titulo"],
                    "miniatura_texto": y["miniatura_texto"], "duracion": y["duracion_objetivo"], "descripcion": y["descripcion"],
                    "tramos": y["tramos_grabacion"]})
    return out


# ───────────────────────── GRABACIONES DE GABRIEL (antes del 8-dic) ─────────────────────────
def guion_de(pid):
    return [f"{t['tiempo']} · {t['voz']}" for t in pieza(pid).get("guion_reel", [])]


def selfie(pid):
    p = pieza(pid)
    return {"historia": pid, "fecha": etiqueta(p["fecha_iso"]), "texto": p["historias"][0]["texto"]}


def grabaciones():
    yt = [p for p in G.values() if de_periodo(p) and str(p.get("grupo", "")).startswith("GRUPO 6")]
    return {
        "nota": "Todo lo que Gabriel tiene que grabar o capturar para que la matriz salga sin huecos. Fecha límite: lunes 7-dic (una sola sesión con Daniela), "
                "salvo la selfie del jue 3-dic, que se graba antes del mié 2-dic. Los reels SELFIE (G-06) se graban con el teléfono de Gabriel, en vertical, sin protocolo. Las 4 re-ediciones de reels ganadores NO necesitan grabación: el gancho nuevo va en texto sobre el video original. "
                "Regla 0: Gabriel confirma cada dato técnico antes de grabarlo, y cambia el ejemplo del «espejo» por su caso real si el del guion no le pasó.",
        "lista": [
            {"n": "G-01", "que": "Reel «Te devolvieron la memoria… y el cálculo estaba bien» (50-60 s, a cámara + 1 toma de pantalla de una memoria)",
             "pieza": "dic-gabriel-memoria-devuelta-reel", "sale": "mié 9-dic", "grabar_antes": "lun 7-dic", "guion": guion_de("dic-gabriel-memoria-devuelta-reel"),
             "notas": "Memoria impresa en la mano en el golpe. El tramo 0:03-0:15 es su caso real."},
            {"n": "G-02", "que": "Reel «Ratios de 1,4 en Robot: ¿sección o apoyos?» (50-60 s, a cámara + celular grabando el monitor con Robot)",
             "pieza": "dic-gabriel-ratios-robot-reel", "sale": "mar 15-dic", "grabar_antes": "lun 7-dic", "guion": guion_de("dic-gabriel-ratios-robot-reel"),
             "notas": "Pantalla real de Robot Structural Analysis: verificación de barras con ratios en rojo, apoyos, longitudes de pandeo y caso de viento. Sin nombre del alumno si no hay permiso (confirmar con Dayana)."},
            {"n": "G-03", "que": "4 selfies de 10-15 s para las historias de venta (vertical, luz natural, sin producción)",
             "pieza": ["dic-hist-1203", "dic-hist-1210", "dic-hist-1217", "ene-hist-0105"], "sale": "3, 10 y 17-dic y 5-ene",
             "grabar_antes": "mié 2-dic (la del 3) · lun 7-dic (las otras 3)",
             "guion": [selfie(i) for i in ["dic-hist-1203", "dic-hist-1210", "dic-hist-1217", "ene-hist-0105"]],
             "notas": "Una toma por selfie; si se traba, se repite entera. La del 5-ene no dice «Feliz año»: abre con el problema. "
                      "Se editan en /home/user/videos-dma/proyectos/historias-dma con la composición Story-vertical (selfie + subtítulos palabra por palabra)."},
            {"n": "G-04", "que": "Capturas reales de su equipo para 4 carruseles (no se graban, se exportan)",
             "pieza": ["dic-sigues-modelando-carrusel", "dic-doble-trabajo-autocad-excel-carrusel", "dic-coordinar-sin-saber-carrusel", "dic-gabriel-ratios-robot-reel"],
             "sale": "1, 21 y 28-dic", "grabar_antes": "lun 7-dic",
             "guion": ["Revit: modelo en gris (portada del 1-dic) y un muro seleccionado con su tabla de cantidades al lado (lámina 5 del 21-dic).",
                       "Navisworks: lista de resultados de Clash Detective con muchos choques y la misma lista agrupada por nivel y sistema (láminas 2 y 6 del 28-dic).",
                       "Robot: verificación de barras con ratios en rojo (reel del 15-dic)."],
             "notas": "Visuales = capturas reales (regla de la casa). Nada de imágenes de stock de software."},
            {"n": "G-05", "que": "Intro (20-30 s) y cierre (10-15 s) a cámara para los 4 videos largos de YouTube (horizontal 16:9)",
             "pieza": sorted(p["id"] for p in yt), "sale": "11 y 18-dic, 29-dic y 5-ene", "grabar_antes": "lun 7-dic",
             "guion": [{"video": p["id"], "intro": p["youtube"]["intro_gabriel"], "cierre": p["youtube"]["cierre_gabriel"]}
                       for p in sorted(yt, key=lambda x: x["fecha_iso"])],
             "notas": "Mismo fondo que la cámara del workshop para que empate con la grabación. Horizontal, no vertical."},
            {"n": "G-06", "que": "3 reels SELFIE de 25-35 s (Gabriel se graba con el teléfono, vertical, y empieza a hablar sin saludo: el problema va en la primera frase)",
             "pieza": ["dic-selfie-chatgpt-firma-reel", "dic-selfie-revit-no-bim-reel", "ene-selfie-acero-en-enero-reel"], "sale": "jue 10-dic, vie 18-dic y mar 5-ene",
             "grabar_antes": "lun 7-dic",
             "guion": [{"reel": i, "palabra_por_palabra": guion_de(i)} for i in ["dic-selfie-chatgpt-firma-reel", "dic-selfie-revit-no-bim-reel", "ene-selfie-acero-en-enero-reel"]],
             "notas": "Una sola toma por reel, sin trípode ni luz extra; si se traba, empieza de nuevo. Edición mínima: subtítulos de 1-2 palabras y logo (Story-vertical en historias-dma)."},
        ],
    }


# ───────────────────────── EMBUDO ─────────────────────────
def embudo_mes():
    filas = []
    for f, pid, *_ in FEED:
        e = pieza(pid).get("embudo") or {}
        if not e:
            continue
        filas.append({"fecha": etiqueta(f), "id": pid, "palabra": e.get("palabra"), "lead_magnet": e.get("lead_magnet"),
                      "producto_destino": e.get("producto_destino"), "canal_dm": e.get("canal_dm"),
                      "cta_info": (e.get("cta_info") or {}).get("palabra")})
    por_palabra = Counter(x["palabra"] for x in filas)
    return {
        "nota": "Pedido de Dayana (23-nov): pieza de problema → «Comenta PALABRA» → DM automático con la mini-solución (lead magnet) → el DM termina con una PREGUNTA que abre la conversación → "
                "el bot de ventas toma la conversación y lleva al producto que resuelve el problema completo. Cada pieza del feed trae su bloque `embudo` en guiones-completos.json "
                "(palabra, lead_magnet, enlace, dm_texto con [ENLACE], producto_destino, canal_dm). No hay lead magnet nuevo este mes.",
        "canales": "ZAPATA se queda en GHL. Todas las demás palabras van por OpenReply (decisión del 23-nov). NIVEL y MEMORIA ya salen SOLO por OpenReply: Dayana apagó su disparador en GHL (23-nov). "
                   "Para las demás, al montar cada campaña en OpenReply se apaga su disparador de comentario en GHL (una palabra, una automatización).",
        "venta_suave": "Pedido de Dayana (23-nov): 3 piezas del Máster y 3 de Acero cierran además con «Si quieres más información de nuestro Máster por bloques, comenta MÁSTER» / "
                       "«Si quieres más información de la Especialización en Acero, comenta TEMARIO». MÁSTER lleva a WhatsApp (" + "https://wa.me/593984372010" + ") para agendar, sin precio; TEMARIO, al temario de Acero.",
        "palabras": [
            {"palabra": "ZAPATA", "lead_magnet": "Calculadora de zapatas", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-calculadora-zapatas-form", "producto": "Diplomado de Cálculo Estructural", "canal": "GHL"},
            {"palabra": "ACERO", "lead_magnet": "5 verificaciones de una nave", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-verificacion-acero-form", "producto": "Especialización en Acero con Tutor IA", "canal": "OpenReply"},
            {"palabra": "MEMORIA", "lead_magnet": "Memoria de cálculo verificable", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-memoria-calculo-form", "producto": "Diplomado de Cálculo Estructural", "canal": "OpenReply"},
            {"palabra": "COTIZA", "lead_magnet": "Cotizador de honorarios", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form", "producto": "Especialización en Acero con Tutor IA", "canal": "OpenReply"},
            {"palabra": "NIVEL", "lead_magnet": "Test de nivel BIM", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-test-nivel-bim-form", "producto": "Máster por bloques (agendar, nunca precio)", "canal": "OpenReply"},
            {"palabra": "BIM", "lead_magnet": "Curso introductorio BIM", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-curso-introductorio-bim-form", "producto": "Máster · Bloque 1 (agendar)", "canal": "OpenReply"},
            {"palabra": "DIPLOMADO", "lead_magnet": "Primer módulo del Diplomado BIM", "enlace": "https://funnel.dgdesignmodeling.com/acceso-gratis-modulo-diplomado-bim-form", "producto": "Diplomado BIM", "canal": "OpenReply"},
            {"palabra": "TEMARIO", "lead_magnet": "Temario de Acero (venta, no recurso)", "enlace": "https://drive.google.com/file/d/1K0cRiCofWt__tw-Yge21nJ2Wg25EpHlC/view?usp=sharing", "producto": "Especialización en Acero con Tutor IA", "canal": "OpenReply → persona / WhatsApp"},
            {"palabra": "MÁSTER", "lead_magnet": "Información + cita de 20 minutos por WhatsApp (venta)", "enlace": "https://wa.me/593984372010", "producto": "Máster por bloques (cohorte de febrero)", "canal": "OpenReply → WhatsApp"},
        ],
        "no_se_usan_en_dic": "DYNAMO y NAVISWORKS siguen vivas pero no entran este mes: ninguna pieza del feed tiene un síntoma de esos recursos (y el verificador todavía no las tiene en su lista viva).",
        "por_pieza": filas,
        "conteo": dict(por_palabra),
    }


DESTACADAS = [
    {"destacada": "🎯 BIM + IA", "que_va": "Síntomas del Máster (el que modela, coordinar, niveles) y las ventas del Máster.",
     "agregar": ["dic-hist-1201", "dic-hist-1208", "dic-hist-1210", "dic-hist-1216", "dic-hist-1221", "dic-hist-1228", "ene-hist-0104", "ene-hist-0105"],
     "quitar": "El mar 1-dic, antes de publicar: todo lo de Black Friday, combo y cuenta regresiva (vencido)."},
    {"destacada": "🔩 ACERO", "que_va": "Uniones, deflexiones, ratios y la venta de Acero del 3-dic.",
     "agregar": ["dic-hist-1203", "dic-hist-1214", "dic-hist-1215"], "quitar": "Frames de noviembre con precio o con el combo."},
    {"destacada": "🎁 HERRAMIENTAS", "que_va": "Recursos gratis (zapatas, memoria, cotizador) y el quiz de la varilla.",
     "agregar": ["dic-hist-1202", "dic-hist-1207", "dic-hist-1209", "dic-hist-1211", "dic-hist-1217", "dic-hist-1223", "dic-hist-1229"], "quitar": "Nada."},
    {"destacada": "👥 COMUNIDAD", "que_va": "Cajas de preguntas, encuestas y el horario de fiestas.",
     "agregar": ["dic-hist-1218", "dic-hist-1222", "dic-hist-1230"], "quitar": "El horario de fiestas, el 4-ene."},
    {"destacada": "⭐ ALUMNOS", "que_va": "Testimonios reales con permiso.", "agregar": ["dic-hist-1204", "ene-hist-0106"], "quitar": "Nada, salvo que un alumno retire su permiso."},
]

PENDIENTES = [
    "OFERTA DE DICIEMBRE: la pasa Dayana después. Slot reservado: historia de venta del jue 17-dic y correo del mié 16-dic (si la oferta es de otro producto, la historia cambia de producto). En público solo porcentajes; precio por WhatsApp.",
    "Oferta de enero (historia del 5-ene y correo del 5-ene): la pasa Dayana si la hay.",
    "Precio vigente de Acero en diciembre para el equipo comercial (el $225 era «todo noviembre»). En público no se dice (confirmar con Dayana).",
    "Testimonio de Acero (4-dic): Daniela confirma en el reel del 23-oct (De2JwdYlfH9) que el alumno dice «Ustedes han sido una gran solución»; si no, usa otra frase textual del mismo video.",
    "Palabra de venta ESTRUCTURAS para la historia del jue 17-dic: la contesta una persona, como NAVES en noviembre (confirmar con Dayana o cambiar por la que prefiera).",
    "Permiso para contar el caso del alumno de los ratios de 1,4 (reel del 15-dic) y caso real de Gabriel para el reel de la memoria (confirmar con Dayana / Gabriel).",
    "Horario de atención del equipo del 24 al 25-dic y del 31-dic al 1-ene (historia del 18-dic) (confirmar con Dayana).",
]

CHECKLIST = [
    {"tarea": "Limpiar las destacadas antes de publicar el mar 1-dic: quitar Black Friday, combo, cuenta regresiva y todo lo que tenga % o precio de noviembre.", "desbloquea": "Que nadie pida una oferta vencida", "cuando": "lun 30-nov noche / mar 1-dic temprano", "para": "Daniela"},
    {"tarea": "Montar en OpenReply las campañas de comentario de ACERO, COTIZA, BIM, DIPLOMADO, TEMARIO y MÁSTER con el `dm_texto` de cada pieza (enlace real en [ENLACE] y la pregunta final) y apagar su disparador en GHL; NIVEL y MEMORIA ya están solo en OpenReply (23-nov): actualizar sus textos con los DM de diciembre. ZAPATA se queda en GHL. Probar cada una con una cuenta ajena (IG y FB).", "desbloquea": "El embudo de las piezas del feed", "cuando": "antes del mar 1-dic", "para": "Dayana (campañas OpenReply) · Ester (prueba)"},
    {"tarea": "Que el bot de ventas tome la conversación cuando la persona contesta la pregunta del DM, y que pase TEMARIO, MÁSTER y ESTRUCTURAS a una persona.", "desbloquea": "Que la pregunta del DM termine en una cita o una venta", "cuando": "antes del mar 1-dic", "para": "Patricio · Ester"},
    {"tarea": "Sesión de grabación con Gabriel y Daniela (lista «Grabaciones de Gabriel»: G-01 a G-06, con los 3 reels selfie). La selfie del 3-dic, antes del mié 2-dic.", "desbloquea": "Reels del 9 y 15-dic, 3 reels selfie (10 y 18-dic, 5-ene), 4 historias de venta y los 4 videos largos de YouTube", "cuando": "lun 7-dic (selfie del 3: mié 2-dic)", "para": "Gabriel · Daniela"},
    {"tarea": "Re-editar los 4 reels ganadores con el gancho y el cierre nuevos (zapata 2-dic, uniones 3-dic, simbología 8-dic, 5 cimentaciones 23-dic). Sin grabar: texto sobre el video original y lámina de cierre con la pregunta.", "desbloquea": "4 de los 7 reels del período", "cuando": "2 días antes de cada fecha", "para": "Daniela"},
    {"tarea": "Clip del workshop del 16-dic: subtitular, escuchar el audio completo y cambiar el cierre a la pregunta + NIVEL. Los otros 3 clips quedan en reserva.", "desbloquea": "Reel del 16-dic", "cuando": "antes del lun 14-dic", "para": "Daniela"},
    {"tarea": "Editar los 4 videos largos de YouTube (16:9, 2-5 min) con la intro y el cierre de Gabriel; miniatura con el texto de cada ficha. El 4.º se publica solo si en la grabación hay un error real de la IA.", "desbloquea": "YouTube 11 y 18-dic, 29-dic y 5-ene", "cuando": "2 días antes de cada fecha", "para": "Daniela"},
    {"tarea": "Gabriel revisa los datos técnicos (regla 0): cuantías ACI/NEC del 7-dic, deflexiones IBC del 14-dic, pesos de varilla del 30-dic, quizzes de historias y los 4 blogs.", "desbloquea": "Que nada de lo que se publica sea inexacto", "cuando": "antes del lun 7-dic", "para": "Gabriel"},
    {"tarea": "Testimonios GUARDADOS (no hay nuevos): sacar el fotograma y la frase del reel de Acero del 23-oct (De2JwdYlfH9) y los videos de Albino Piñeiro, Luis Fernández y Jorge Aguirre de la página de testimonios para el 4-dic, 17-dic, 4-ene, 5-ene y 6-ene.", "desbloquea": "3 piezas de venta y 3 historias de venta", "cuando": "antes del mié 2-dic", "para": "Daniela"},
    {"tarea": "Editar las historias con Gabriel en /home/user/videos-dma/proyectos/historias-dma: selfies en Story-vertical y explicaciones con RutaMaster, RutaAcero, RutaDiplomado y AnatomyConexion (campo `produccion` de cada historia).", "desbloquea": "Las historias con Gabriel y las de venta", "cuando": "2 días antes de cada fecha", "para": "Daniela"},
    {"tarea": "Diseñar los 2 posts de fecha especial con imagen de marca DG 2026 (Navidad 25-dic y cierre de año 31-dic) y programarlos: el equipo no está esos días.", "desbloquea": "Las 2 fechas especiales", "cuando": "antes del vie 18-dic", "para": "Daniela"},
    {"tarea": "Cada lunes: cuántos comentaron cada palabra, cuántos recibieron el DM, cuántos contestaron la pregunta y cuántos agendaron o compraron en 14 días (OpenReply + GHL).", "desbloquea": "Saber qué pregunta del DM abre conversación y cuál no", "cuando": "lunes 7, 14, 21 y 28-dic y 4-ene", "para": "Ester · Dayana"},
    {"tarea": "Guardar las historias en su destacada cada viernes (4, 11 y 18-dic) y el 30-dic y 6-ene.", "desbloquea": "Destacadas al día", "cuando": "viernes", "para": "Daniela"},
    {"tarea": "Publicar los 4 blogs de los sábados 5, 12 y 19-dic y 2-ene con su post de anuncio (el 26-dic no hay blog).", "desbloquea": "G3 del período", "cuando": "sábados", "para": "Equipo de contenido"},
]


def main():
    feed = [fila_feed(*f) for f in FEED]
    cuota = [x for x in feed if not x.get("fuera_de_cuota")]
    fmt = Counter("reel" if "REEL" in (x["formato_publicacion"] or "").upper() else
                  "carrusel" if "CARRUSEL" in (x["formato_publicacion"] or "").upper() else "post" for x in cuota)
    inten = Counter(x["intencion_dic"] for x in cuota)
    hist = filas_de("GRUPO 5")
    ventas = sum(1 for x in hist if x.get("venta"))
    gab = sum(1 for x in hist if x.get("gabriel_a_camara"))
    yt = youtube_largos()
    n = len(cuota)
    cal = {
        "mes": "2026-12",
        "subtitulo": "Del martes 1 de diciembre de 2026 al miércoles 6 de enero de 2027 · contenido sintomático: problema primero, dato comparativo y pregunta que obliga a comentar · ritmo normal hasta el 19-dic y de fiestas del 20-dic al 6-ene",
        "periodo": {"desde": "2026-12-01", "hasta": "2027-01-06",
                    "nota_enero": "Los días 1 a 6 de enero van en este archivo con su fecha real (ids ene-*): las herramientas del mes (verificar_matriz_mes.py, build_matriz_mes.py) leen un calendario por mes y este período cruza el año."},
        "ventas_por_semana_max": 1,
        "automatizacion_confirmada": {"NIVEL": "OpenReply (disparador apagado en GHL, Dayana 23-nov)", "MEMORIA": "OpenReply (disparador apagado en GHL, Dayana 23-nov)"},
        "reglas_del_mes": [
            f"LO QUE DIJERON LOS DATOS (matriz.json, Meta Graph API, 20-nov): noviembre bajó a 2.877 vistas, 7,3 comentarios y 14 guardados por pieza, contra 7.632 / 36,2 / 213,9 de octubre. "
            "Ganaron los PROBLEMAS técnicos concretos: «La misma zapata no se comporta igual en arcilla, arena, limo, grava…» (81 comentarios), «Zapatas en arena suelta, pilotes cortos o hasta el estrato» (34), "
            "«6 formas de unir una viga de acero a una columna» (55 guardados) y el post «40 mm.»; y los históricos «Simbología de niveles en planos» (603 comentarios), «5 tipos de cimentación» (103), «El 1 % de cuantía» (152) e «Hipótesis que no se declararon…» (48). "
            "Perdieron (0-2 comentarios): efemérides, promos directas, piezas del workshop / IA en Revit sin problema y explicaciones planas (LOD 100-500, tipos de cercha).",
            "LAS 3 LLAVES DE CADA PIEZA: 1) abre con un error concreto que el ingeniero reconoce y que le cuesta plata o prestigio (acusar un hábito / síntoma); 2) da un dato técnico verificable y comparativo que se guarda; "
            "3) termina con una pregunta que obliga a comentar («¿Cuál usas tú?», «Dinos el número»). La palabra del lead magnet solo es el CTA de cierre, nunca el tema.",
            f"FEED: {n} piezas en cuota + {len(feed) - n} saludos de marca fuera de cuota (Navidad 25-dic y cierre de año 31-dic) · formato {fmt['reel']} reels / {fmt['carrusel']} carruseles / {fmt['post']} posts · intención {inten['problema']} problema / {inten['referencia']} referencia técnica comparativa / {inten['venta']} venta-testimonio-objeción "
            f"({round(100 * inten['problema'] / n)} / {round(100 * inten['referencia'] / n)} / {round(100 * inten['venta'] / n)} %). Pedido: ~60/20/20; el verificador (50/20/30 ± 10) no deja pasar de 60 % de problema. Las semanas del 7 y del 14-dic llevan 5 piezas por los reels selfie que pidió Dayana.",
            "EMBUDO: pieza de problema → «Comenta PALABRA» → DM automático con la mini-solución → el DM termina con una pregunta que abre la conversación → el bot de ventas lleva al producto. "
            "ZAPATA en GHL; el resto en OpenReply (NIVEL y MEMORIA ya solo en OpenReply). VENTA SUAVE: 3 piezas del Máster y 3 de Acero suman «si quieres más información… comenta MÁSTER / TEMARIO». Ningún lead magnet nuevo este mes.",
            "VIDEO: 4 reels ganadores re-editados con un gancho de problema nuevo (zapata y suelos, uniones viga-columna, simbología de niveles, 5 cimentaciones), 1 clip del workshop con síntoma, 2 reels nuevos de Gabriel, 3 reels SELFIE (Gabriel con el teléfono, sin protocolo) "
            f"y {len(yt)} videos LARGOS de YouTube (2-5 min, no Shorts) con lo mejor del workshop del 17-nov. Lo que hay que grabar está en «Grabaciones de Gabriel» (antes del 8-dic).",
            "RITMO: del 1 al 19-dic, 4 piezas de feed por semana (los carruseles abren la semana, los reels van juntos), historias de lunes a viernes con UNA venta el jueves, LinkedIn y correo semanales y blog el sábado. "
            "Del 20-dic al 6-ene, 2 piezas de feed por semana (más los 2 saludos de marca), historias livianas (1-2 frames) y NADA de venta el 24, 25 y 31-dic ni el 1-ene. Sin historias el 24, 25, 31 y 1.",
            "EFEMÉRIDES: solo dos saludos de marca pedidos por Dayana, Navidad (25-dic) y cierre de año (31-dic), con imagen DG 2026, sin venta y fuera de cuota. Ninguna pieza de contenido usa una efeméride como tema (en noviembre dieron 0-2 comentarios).",
            "SIN PROMOS INVENTADAS: el Black Friday terminó el 30-nov. La OFERTA DE DICIEMBRE está pendiente (la pasa Dayana): su slot es la historia del jue 17-dic y el correo del 16-dic. Máster: próxima cohorte en FEBRERO de 2027. Diplomado BIM: grabado, empiezas hoy. "
            "El Máster nunca lleva precio; si Dayana define una promo, va solo en porcentajes y por WhatsApp.",
            "LAS PIEZAS DE VENTA NO USAN PALABRAS DE LEAD MAGNET (Dayana, 30-oct): TEMARIO (Acero), MÁSTER (agendar), ESTRUCTURAS (Diplomado de Cálculo, historia del 17) y DIPLOMADO (módulo gratis para probar antes de pagar).",
            "Visuales = capturas reales de Revit, Robot y Navisworks y cámara de Gabriel. Nada técnico se publica sin que Gabriel lo revise (regla 0). Cero OBRA. Ningún id ni gancho repetido.",
        ],
        "checklist_tareas": CHECKLIST,
        "efemerides": [
            ["Dom 6-dic", "Fundación de Quito (local, cae en domingo)", "No entra como contenido."],
            ["Mar 8-dic", "Inmaculada Concepción: feriado en Colombia, Perú, Argentina y Chile (no en Ecuador)", "Historias normales; el reel del día sale igual."],
            ["Jue 24 · Vie 25-dic", "Nochebuena y Navidad", "Solo el post de saludo de Navidad (vie 25, programado). Sin historias y sin venta."],
            ["Jue 31-dic · Vie 1-ene", "Fin de año y Año Nuevo", "Solo el post de cierre de año (jue 31, programado). Sin historias y sin venta dura."],
            ["Mié 6-ene", "Reyes (en Colombia el feriado pasa al lun 11-ene)", "No entra como contenido."],
        ],
        "estrategia_comercial": {
            "slot_oferta_diciembre": {"estado": "PENDIENTE: la pasa Dayana", "donde": ["dic-hist-1217 (historia de venta, jue 17-dic)", "dic-correo-1216-acero (correo, mié 16-dic)"], "regla": "En público solo porcentajes; precio y mini landing por WhatsApp. Ester decide precio y nombre."},
            "nota": "Diciembre todavía no tiene oferta (pendiente). Se vende por conversación: cada pieza de problema abre un DM con pregunta, y el bot y el equipo llevan al producto. Una venta por semana en historias (jueves 3, 10 y 17-dic y mar 5-ene).",
            "reglas": [
                "Ningún precio en público. El Máster, nunca (cohorte de febrero, se invita a agendar por WhatsApp https://wa.me/593984372010); Acero, tampoco este mes.",
                "Si Dayana define una oferta de diciembre o enero, la nombra y le pone precio Ester; va solo por WhatsApp con su mini landing y en público solo con porcentajes.",
                "Sin venta el 24, 25 y 31-dic ni el 1-ene, en ningún canal.",
                "Quien contesta la pregunta del DM con un problema real pasa a una persona en menos de 30 minutos en horario laboral.",
            ],
        },
        "publicidad": {
            "nota": "Esta matriz no abre campañas nuevas ni inventa ofertas. Propuesta para revisar con Dayana y Olympus (confirmar con Dayana): pautar como anuncio de interacción la re-edición de «Simbología de niveles» (8-dic) y la de la zapata (2-dic), que ya probaron que conversan, con su palabra clave.",
            "campanas": [],
            "indicaciones": [["Pauta de diciembre", "(confirmar con Dayana / Olympus): presupuesto, campañas activas y si se pautan las re-ediciones ganadoras."]],
        },
        "embudo": embudo_mes(),
        "grabaciones_gabriel": grabaciones(),
        "youtube_largos": {"nota": "Videos normales de YouTube (16:9, 2-5 minutos), NO Shorts, hechos con lo mejor del workshop IA conectada a Revit (17-nov). Título que abre con un problema, descripción con capítulos y el test de nivel, y texto de miniatura corto.",
                           "videos": yt},
        "grupos": [
            {"n": 1, "nombre": "GRUPO 1 · Feed principal — Instagram, Facebook, LinkedIn, Threads (imágenes) · Instagram, Facebook, TikTok, YouTube Shorts, LinkedIn (reels)",
             "descripcion": f"{n} piezas en cuota + 2 saludos de marca: 4-5 por semana del 1 al 19-dic y 2 por semana del 20-dic al 6-ene. 10:00 Ecuador (15:00 UTC). Cada pieza trae su bloque `embudo`.",
             "reglas": ["Problema primero, dato comparativo y pregunta que obliga a comentar; la palabra solo cierra.",
                        "Las piezas de venta usan TEMARIO, MÁSTER o DIPLOMADO, nunca ACERO, NIVEL, ZAPATA, MEMORIA ni COTIZA.", "Venta suave: «Si quieres más información de nuestro Máster por bloques, comenta MÁSTER» / «…de la Especialización en Acero, comenta TEMARIO» como segunda línea de cierre.",
                        "En TikTok, YouTube Shorts, LinkedIn y Threads, sin palabra clave: pregunta abierta."],
             "calendario": feed},
            {"n": 2, "nombre": "GRUPO 2 · Comunidades — WhatsApp, canal de IG, grupos de FB, comunidad de YouTube, comunidades GHL",
             "descripcion": "Un post completo por semana, el mismo en todos los canales, con el enlace directo al recurso.",
             "reglas": ["Si hay regalo, el enlace va directo en el post. Nada de «respóndeme X». Sin hashtags.", "Sin precio y sin oferta (no hay oferta definida)."],
             "calendario": filas_de("GRUPO 2")},
            {"n": 3, "nombre": "GRUPO 3 · Blog de Design Modeling Academy",
             "descripcion": "Un artículo los sábados 5, 12 y 19-dic y 2-ene (el 26-dic no hay), con su post de anuncio.", "reglas": ["El CTA del blog es el recurso gratis de su tema, nunca genérico."],
             "calendario": filas_de("GRUPO 3")},
            {"n": 4, "nombre": "GRUPO 4 · LinkedIn — Design Modeling Academy",
             "descripcion": "Una publicación de texto por semana en la página de Design Modeling Academy, tono formal, sin hashtags; publica Daniela.",
             "reglas": ["NUNCA «comenta la palabra»: pregunta abierta al final.", "El enlace va dentro del post.", "No sale el mismo día que su pieza base del feed."],
             "calendario": filas_de("GRUPO 4")},
            {"n": 5, "nombre": "GRUPO 5 · Historias de Instagram (y Facebook stories)",
             "descripcion": f"Lunes a viernes, 09:00 Ecuador (14:00 UTC). {len(hist)} días: 3-4 frames hasta el 18-dic y 1-2 frames en fiestas. {ventas} de venta (una por semana) y {gab} con Gabriel a cámara. Sin historias el 24, 25 y 31-dic ni el 1-ene.",
             "reglas": ["Cada historia dice en `produccion` qué composición de /home/user/videos-dma/proyectos/historias-dma usar (RutaMaster, RutaAcero, RutaDiplomado, AnatomyConexion, Story, Faltan) o qué selfie de Gabriel.",
                        "DÍAS DE VENTA, en 3 tiempos: 1) curiosidad, 2) prueba REAL, 3) «Respóndeme X si estás cansado de… y de…».",
                        "DÍAS DE VALOR: 1) curiosidad, 2) el dato o el tip (quiz o encuesta), 3) «Respóndeme X y te mando [recurso gratis]».",
                        "Fiestas: 1-2 frames, sin venta.", "Precio nunca en la historia.", "Máximo 4 frames."],
             "calendario": hist},
            {"n": 6, "nombre": "GRUPO 6 · YouTube — videos largos (2-5 min, no Shorts)",
             "descripcion": f"{len(yt)} videos con lo mejor del workshop del 17-nov, con intro y cierre de Gabriel.",
             "reglas": ["Título que abre con el problema.", "En la descripción: capítulos y el enlace al test de nivel.", "Lo que se usó en el workshop, dicho así: un servidor MCP de código abierto sobre pyRevit y NonicaTab AI Connector. No decir «Revit» ni «servidor MCP de Autodesk»."],
             "calendario": filas_de("GRUPO 6")},
        ],
        "lead_magnets": {
            "nota": "No hay lead magnet nuevo en diciembre. Se usan los que existen, cada uno con su producto. DYNAMO y NAVISWORKS siguen vivas pero no entran este mes.",
            "nuevo": [],
            "respaldo": [{"nombre": x["lead_magnet"], "palabra": x["palabra"], "por_que": f"Lleva a {x['producto']} · {x['canal']}"} for x in embudo_mes()["palabras"][:7]],
            "mapa_cta": [{"palabra": k, "fecha": ", ".join(r["fecha"] for r in embudo_mes()["por_pieza"] if r["palabra"] == k),
                          "producto": next(r["producto_destino"] for r in embudo_mes()["por_pieza"] if r["palabra"] == k)} for k in embudo_mes()["conteo"] if k],
        },
        "destacadas": {"responsable": "Daniela", "nota": "Se limpian antes del mar 1-dic (todo lo de noviembre con precio, combo o Black Friday) y se alimentan cada viernes.", "lista": DESTACADAS},
        "correos_nota": "Un correo por semana a la lista propia: 2, 9 y 16-dic (valor con recurso), 22 y 29-dic (valor de fiestas, sin venta) y 5-ene (venta blanda del Máster: test + agendar, sin precio).",
        "piezas": [], "pauta": [],
        "banco_reserva": [i for i in ["dic-ws-clip-muros-reel", "dic-ws-clip-niveles-reel", "dic-ws-clip-conexion-reel"] if i in G],
        "correos": correos(),
        "auditoria_previa": {"mes": "2026-11", "resumen": "Noviembre (al 20-nov, matriz.json): 2.877 vistas, 7,3 comentarios y 14 guardados por pieza (octubre: 7.632 / 36,2 / 213,9). Lo que conversó: problemas técnicos concretos de cimentaciones y acero. Lo que no: efemérides, promos directas, workshop/IA en Revit sin problema y explicaciones planas."},
        "kpis_mensuales": {
            "nota": "De dónde arranca diciembre (matriz.json, Meta Graph API, actualizado el 20-nov).",
            "por_pieza": {"octubre": {"vistas": 7632, "comentarios": 36.2, "guardados": 213.9}, "noviembre": {"vistas": 2877, "comentarios": 7.3, "guardados": 14.1}},
            "metas_diciembre": ["Comentarios por pieza del feed: volver por encima de 20 (mitad del camino a octubre).",
                                "Cada palabra: cuántos contestan la pregunta del DM (nueva medición del embudo, cada lunes).",
                                "Re-ediciones: cada una por encima de la mediana de reels de 90 días."],
        },
        "pendientes": PENDIENTES,
        "resumen_cierre": f"Diciembre-enero: {n} piezas de feed ({inten['problema']} de problema, {inten['referencia']} de referencia comparativa y {inten['venta']} de venta), 4 re-ediciones de reels ganadores, 2 reels nuevos de Gabriel, 1 clip del workshop, "
                          f"3 reels selfie, 2 saludos de marca (Navidad y 31-dic), {len(yt)} videos largos de YouTube, {len(hist)} días de historias ({ventas} de venta, {gab} con Gabriel), {len(filas_de('GRUPO 2'))} posts de comunidades, {len(filas_de('GRUPO 4'))} de LinkedIn, {len(filas_de('GRUPO 3'))} blogs y {len(correos())} correos. Cada pieza del feed trae su embudo completo. Sin promos inventadas.",
        "pie": "Design Modeling Academy · Matriz de contenido diciembre 2026 (1 dic – 6 ene 2027) · métricas reales de Meta Graph API (matriz.json, 20-nov) y brief de contenido sintomático.",
    }
    json.dump(cal, open(M / "calendario-diciembre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok ·", n, "feed ·", dict(fmt), dict(inten), "·", sum(len(g["calendario"]) for g in cal["grupos"]), "entradas")


if __name__ == "__main__":
    main()
