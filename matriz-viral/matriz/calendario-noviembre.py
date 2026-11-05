#!/usr/bin/env python3
"""Construye calendario-noviembre.json desde las piezas de guiones-completos.json.

    python3 matriz-viral/matriz/calendario-noviembre.py

Igual que octubre: el calendario solo ORDENA piezas; el contenido vive en
guiones-completos.json. Noviembre va del miércoles 28 de octubre (arranque del
workshop y Halloween, «semana 0») al lunes 30 de noviembre. Desde el 9-nov
(Dayana, 3 y 4-nov): combo del mes (9 al 26) y Black Friday (4-nov, reunión de cierre):
del vie 27 al lun 30, con Cyber Monday, para todos los países.
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
    ("2026-11-04", "nov-valor-6-uniones-viga-columna-reel", "problema", "Acero", "Comenta ACERO",
     "Chuleta visual ya editada (6 uniones viga de acero–columna de hormigón; en octubre se anotó como oct-uniones-acero-hormigon-reel y no se subió). Abre la semana de acero (Dayana, 30-oct)."),
    ("2026-11-05", "nov-ws-para-quien-reel", "objeción", "Máster · workshop", "Comenta WORKSHOP", "Workshop · video 2 (filtra a quien empieza de cero)."),
    ("2026-11-06", "nov-dato-recubrimiento-post", "problema", "Diplomado · Estructuras", "Comenta ZAPATA",
     "Dato de cálculo verificable (formato que más guarda). Sale con el blog del viernes."),
    ("2026-11-09", "nov-combo-diplomado-50-post", "objeción", "Especializaciones · Diplomados", "Comenta COMBO",
     "COMBO DEL MES (Dayana, 3-nov): «Un diplomado completo por $50» con la compra de una especialización. Solo 10 cupos. Es la única pieza del feed con precio (el gancho de $50); no muestra el precio de la especialización."),
    ("2026-11-07", "nov-valor-sismo-cimentaciones-reel", "problema", "Diplomado · Estructuras", "Comenta ZAPATA",
     "Video de valor pendiente de octubre (Drive de Dayana, 30-oct): ya está editado. Entra en lugar del reel «IA + Revit en 3 pasos», que es justo lo que se hace en el workshop y pasa al 28-nov como clip."),
    ("2026-11-09", "nov-peru-bim-obligatorio-carrusel", "problema", "Máster", "Comenta NIVEL",
     "TENDENCIA: BIM obligatorio en Perú desde el 14-ago-2026 (MEF). Va también a LinkedIn."),
    ("2026-11-10", "nov-chuleta-2-cerchas-reel", "problema", "Acero · Naves PRO", "Comenta ACERO",
     "SERIE CHULETA 1/4 · EFEMÉRIDE: Día Mundial de la Ciencia (UNESCO)."),
    ("2026-11-11", "nov-valor-5-suelos-zapata-reel", "problema", "Diplomado · Estructuras", "Comenta ZAPATA",
     "Video de valor pendiente de octubre. Título igual al del video: «5 pisos sobre una zapata»."),
    ("2026-11-12", "nov-calidad-checklist-modelo-carrusel", "solución", "Máster", "Comenta NIVEL", "EFEMÉRIDE: World Quality Day."),
    ("2026-11-13", "nov-obj-master-bloques-post", "objeción", "Máster", "Comenta NIVEL",
     "Dar a conocer el Máster por bloques (Dayana, 23-oct). Sin precio. Sale con el blog del viernes."),
    ("2026-11-14", "nov-gabriel-error-modelos-reel", "problema", "Máster", "Comenta NIVEL", "Gabriel a cámara (más Gabriel, pedido de Dayana)."),
    ("2026-11-16", "nov-ws-horas-parametros-carrusel", "problema", "Máster · workshop", "Comenta WORKSHOP",
     "El día antes del workshop. 16-nov: descanso en México y festivo en Colombia; último día del Buen Fin (13-17)."),
    ("2026-11-17", "nov-chuleta-3-lod-reel", "problema", "Máster", "Comenta WORKSHOP", "SERIE CHULETA 2/4 · DÍA DEL WORKSHOP (8:00 PM Ecuador)."),
    ("2026-11-18", "nov-ws-donde-se-equivoco-carrusel", "solución", "Máster", "Comenta NIVEL", "Resumen del workshop con capturas reales de la grabación."),
    ("2026-11-19", "nov-nave-a-ojo-reel", "problema", "Acero", "Comenta ACERO",
     "REFERENTE: misma mecánica de @lexmrbim aplicada a Acero (3 verificaciones en pantalla y las otras 2 por la palabra)."),
    ("2026-11-20", "nov-acero-modulo-a-modulo-carrusel", "objeción", "Acero", "Comenta TEMARIO",
     "Semana del combo (últimos cupos, hasta el jue 26). El feed explica el programa sin precio. El 20 ya no es Black Friday (reunión del 4-nov)."),
    ("2026-11-21", "nov-ws-clip-demo-reel", "problema", "Máster", "Comenta NIVEL", "Clip del workshop (W+4)."),
    ("2026-11-23", "nov-master-que-bloque-carrusel", "problema", "Máster", "Comenta NIVEL", "Semana del Black Friday (vie 27 → lun 30) y últimos días del combo (hasta el jue 26). Máster por bloques sin precio hasta el 27."),
    ("2026-11-24", "nov-chuleta-4-uniones-reel", "problema", "Acero", "Comenta ACERO", "SERIE CHULETA 3/4."),
    ("2026-11-25", "nov-gabriel-no-compres-descuento-reel", "objeción", "Acero", "Comenta TEMARIO", "Gabriel a cámara: honestidad en la semana del Black Friday."),
    ("2026-11-26", "nov-valor-grava-zapata-reel", "problema", "Diplomado · Estructuras", "Comenta ZAPATA",
     "Video de valor pendiente de octubre: un respiro de valor antes del Black Friday."),
    ("2026-11-27", "nov-bf-incluye-post", "objeción", "Acero · cursos", "Comenta BLACK", "BLACK FRIDAY · arranca hoy y va hasta el lun 30 (Cyber Monday), todos los países. Con precios (Dayana, 4-nov): tachado, precio de hoy y %, Máster por bloques incluido."),
    ("2026-11-28", "nov-ia-revit-3-pasos-reel", "solución", "Máster", "Comenta NIVEL",
     "CLIP DESTACADO DEL WORKSHOP (W+11): se corta de la grabación del 17-nov el momento de los 3 pasos. Antes estaba el 7-nov; se movió porque mostrarlo antes del workshop le quitaba sentido (Dayana, 30-oct)."),
    ("2026-11-30", "nov-chuleta-1-perfiles-acero-reel", "problema", "Acero", "Comenta ACERO",
     "SERIE CHULETA 4/4: cierra la serie. Estaba el 4-nov; pasó aquí para que ese día salga el video ya editado de las 6 uniones (Dayana, 30-oct)."),
]


def fila_feed(f, pid, intencion, producto, cta, nota):
    p = pieza(pid)
    return {"fecha": etiqueta(f), "fecha_iso": f, "semana": p.get("semana"), "id": pid,
            "titulo": p.get("titulo"), "tipo": p.get("tipo"), "formato_publicacion": p.get("formato_detalle") or p.get("formato"),
            "intencion": intencion, "producto": producto, "cta": cta, "estado": p.get("estado"), "nota": nota,
            **({"fuera_de_cuota": True} if pid in FUERA_DE_CUOTA else {})}


# Videos de valor que quedaron editados en octubre sin subir (Drive de Dayana, 30-oct).
# Se publican en noviembre, pero no cuentan en el reparto 40/40/20 ni 50/20/30 del mes:
# son 4 reels de «problema» que no se planificaron con esas cuotas.
FUERA_DE_CUOTA = {"nov-valor-sismo-cimentaciones-reel", "nov-valor-5-suelos-zapata-reel",
                  "nov-valor-grava-zapata-reel", "nov-valor-6-uniones-viga-columna-reel"}


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
    if p.get("banda_fija"):
        cfg.append(["Banda fija (todo el video)", p["banda_fija"]])
    if p.get("variantes_gancho"):
        cfg.append(["Variantes de gancho", " · ".join(p["variantes_gancho"])])
    if p.get("guion"):
        cfg.append(["Guion del video", " | ".join(f"{t[0]}: {t[2]} [{t[3]}]" for t in p["guion"])])
    return {"id": pid, "titulo": p.get("titulo"), "campana": campana,
            "precio": "sin precio: solo el % (Black Friday, Dayana 4-nov); el precio lo da el closer" if (p.get("producto") or "").startswith("Máster") and "Black" in campana
            else "sin precio (regla del Máster)" if (p.get("producto") or "").startswith("Máster")
            else "visible: especialización $225 + diplomado de Estructuras o Arquitectura por $50" if "Diplomados" in (p.get("producto") or "") and "Especializaciones" in (p.get("producto") or "")
            else "solo porcentajes, sin precios (Dayana, 4-nov): el precio exacto se da por WhatsApp" if "Todos" in (p.get("producto") or "")
            else "sin precio",

            "formato": p.get("formato_detalle") or "anuncio", "hook": p.get("hook"), "cuerpo": p.get("texto_principal"),
            "titular": p.get("titular"), "descripcion": p.get("descripcion"), "creativo": p.get("creativo"),
            "prompt": p.get("prompt_imagenes", ""), "cfg": cfg, "condicion": p.get("condicion", "")}


ADS = {
    "WORKSHOP · registro (2 al 16-nov, parte de los 59 USD del plan)": ["nov-ads-ws-demo", "nov-ads-ws-5-preguntas", "nov-ads-ws-taller-gratis"],
    "COMBO DEL MES · Especialización + Diplomado por $50 (9 al 26-nov) · campaña NUEVA (ACERO FORM + COMBO)": ["nov-ads-acero-bf"],
    "BLACK FRIDAY · todos los programas, del vie 27 al lun 30 (Cyber Monday), todos los países": ["nov-ads-cursos-bf"],
    "MÁSTER · −25 % en el bloque, solo del 27 al 30, con el precio de cada bloque (se pauta desde el jue 26)": ["nov-ads-master-bono"],
    "MÁSTER · la ruta en 4 bloques (siempre activa desde el 2-nov), sin precio": ["nov-ads-master-ruta"],
    "COLECCIÓN AUTODESK CON IA · cómo funciona (2 al 22-nov), sin precio": ["nov-ads-coleccion-ruta"],
    "ESPECIALIZACIONES · cómo funcionan (2 al 17-nov), sin precio": ["nov-ads-especializaciones-ruta"],
    "ACERO · la especialización en video (2 al 17-nov), sin precio": ["nov-ads-acero-ruta"],
    "DIPLOMADO CÁLCULO ESTRUCTURAL · en video (2 al 22-nov), sin precio": ["nov-ads-diplomado-calculo-ruta"],
}

DECISIONES_PAUTA = [
    ["De dónde sale (análisis del 23-oct, Meta 23-sep → 22-oct)",
     "$1.090,76 gastados, 1.097 leads (683 de formulario + 414 de WhatsApp), CPL $0,99. El Máster [29SEP] es el mejor: $0,75 en 30 días y $0,60 en los últimos 7."],
    ["1 · Apagar lo que no trae nada",
     "El conjunto «Resto» de ACERO WSP ($15,83, 0 leads, frecuencia 59,5), las dos campañas LEAD MAGNETS de clics ($59, 0 leads) y ACERO TEST GANCHOS ($1,62)."],
    ["2 · Concentrar el Máster en [29SEP]", "Y reactivar «MÁSTER CITA» ($0,63) solo si GHL confirma que esos leads agendan."],
    ["3 · Workshop: registro del 2 al 16-nov",
     "Hoy no hay ningún anuncio del workshop. Los 59 USD del plan van a quien interactuó con la cuenta: las chuletas de octubre alcanzaron unas 55.000 cuentas (puede contar a la misma persona dos veces). Medir registros reales en GHL el 3 y el 10-nov."],
    ["4 · Combo y Black Friday (3-nov, Dayana)", "Del 9 al 26-nov, o hasta llenar los 10 cupos: campaña nueva «ACERO FORM + COMBO» con anuncio propio («Un diplomado completo por $50» —Estructuras o Arquitectura, a elección— con una especialización a $225), en video de Gabriel e imagen, con botón a WhatsApp; se financia con lo que se apaga de lead magnets. Black Friday del vie 27 00:00 al lun 30 23:59, todos los países (reunión del 4-nov): cursos BIM −50 %, especializaciones −40 %, diplomados −40 %, Máster −25 % en el bloque; SOLO PORCENTAJES, sin precios (Dayana, 4-nov). Campaña NUEVA «BLACKFRIDAY + CYBERMONDAY» y con presupuesto propio (Patricio, 4-nov), separada de las del Máster y Acero; los anuncios del Black Friday se suben unos días antes del 27. Un solo enlace de pago por producto."],
    ["5 · Países (Olympus, 4-nov)", "Ecuador es el 14 % de la audiencia y más de la mitad de las ventas; México, el 33 % y casi sin ventas. Olympus lo revisa en los primeros días del mes y propone un cambio gradual, para no reiniciar el aprendizaje. Presupuesto del Máster: no se sube ni se baja este mes; Acero sigue con WhatsApp + formulario."],
    ["6 · Lead magnets", "Cierre de octubre (3-nov): las campañas de visitas al perfil gastaron $58 sin leads (3.063 visitas a $0,019). Acordado con Olympus el 2-nov: se deciden el lun 9-nov con los UTM, y les pedimos optimizarlas a vistas de la página de destino con el píxel en las landings. Si siguen sin traer leads, se apagan y ese dinero pasa al combo y a pautar la chuleta ganadora («Simbología de niveles», 79.800 vistas) con su palabra clave."],
    ["7 · Acero a $225", "Todo noviembre a $225 (Dayana, 3-nov). Los anuncios de Acero dicen $225 o no dicen precio; ninguno dice $199,99. Solo el Black Friday baja el precio."],
    ["8 · Anuncios que convierten (Taller Lap)", "Los anuncios del combo y del Black Friday siguen la fórmula de los anuncios con 293-432 días activos (EDICION-GANADORA-NICHO.md): Gabriel a cámara, la oferta en una banda fija abajo todo el video (el combo con «$50»; el Black Friday solo con %), prueba en pantalla, 30-45 s y 3-4 variantes que solo cambian el gancho. Se apagan las variantes que no rinden a los 3-4 días."],
    ["REGLA DE ORO", "El Black Friday se dice SOLO en porcentajes, sin ningún precio exacto, para generar intriga (Dayana, 4-nov); el precio lo da el equipo por WhatsApp o en la llamada. El Máster nunca lleva precio en público. El combo dice «$50» en anuncio, correo, historias, comunidades y en su post del feed. El combo cierra el jue 26 a las 23:59 y el Black Friday va del vie 27 00:00 al lun 30 23:59 (hora de Ecuador): no se reabre."],
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
    ["Vie 20-nov", "Ecuador: día libre (Decreto 507)", "Combo: últimos cupos y aviso del Black Friday del 27 al 30 (ya no hay Black Friday ese día, reunión del 4-nov)"],
    ["Lun 23-nov", "Argentina: feriado de la Soberanía Nacional", "Aviso del Black Friday del viernes y últimos días del combo"],
    ["Jue 26 · Vie 27-nov", "Thanksgiving · Black Friday", "Cierra el combo (jue 26, 23:59) · arranca el Black Friday (vie 27, 00:00)"],
    ["Lun 30-nov", "Cyber Monday", "Último día del Black Friday (cierra a las 23:59) · la chuleta de perfiles de acero cierra la serie en el feed"],
    ["Dom 29-nov", "Ecuador: elecciones seccionales", "El Black Friday sigue para todos (decisión del 4-nov); Olympus vigila el rendimiento en Ecuador"],
]

# Qué hay que actualizar en cada canal para el combo, el workshop y el Black Friday
# (pedido de Dayana, 3-nov). Web revisada el 3-nov: academia-web (vercel).
ACTUALIZAR_POR_CANAL = {
    "nota": "Regla de Dayana (4-nov): toda oferta (combo, Black Friday o la que venga) se actualiza en TODOS los canales, sin dejar ninguno por fuera, y se quita de todos al terminar. Primero va la app de DG, módulo por módulo, en el orden del menú; después, lo que vive fuera de la app. Precios tomados de la web el 3-nov: Acero $225 (tachado $464,99), las demás especializaciones $199,99, diplomados desde $499,99 y el Máster por bloques en $750 / $750 / $600 / $900. El Black Friday se publica SOLO con porcentajes (cursos BIM −50 %, especializaciones −40 %, diplomados −40 %, Máster −25 %): los precios exactos están solo en la pestaña Equipo comercial (Dayana, 4-nov). Combo (9 al 26): el diplomado de Estructuras o de Arquitectura, a elección, por $50 con una especialización; 10 cupos.",
    "filas": [
        ["App · Estrategia mensual", "Sincronizar la matriz de noviembre (después de mezclar el PR #166, que corrige las fechas). Volver a sincronizar cada vez que cambie la matriz: solo actualiza los borradores y no toca lo aprobado.", "hoy · cada cambio", "Ester"],
        ["App · Generador y Copiloto", "Todo lo que se genere en noviembre sale con las ofertas vigentes. Antes de aprobar, revisar que no aparezca Acero a $199,99, la «Black Week», el «Cyber Monday» ni el Máster con precio fuera del Black Friday.", "todo el mes", "Daniela · Ester"],
        ["App · Calendario (feed e historias)", "Aprobar cada pieza en su fecha. Combo: post del lun 9 e historias del 10, 18, 20, 23 y 25. Black Friday: historias del 23 (aviso), 26 (Máster con precio), 27 (arranca) y 30 (último día, Cyber Monday), más el post del 27. Destacadas: quitar el combo el 27 y el Black Friday el mar 1-dic.", "según el calendario", "Ester (aprueba) · Daniela (sube las artes)"],
        ["App · Blog & SEO", "Los artículos del 6, 13, 20 y 27 son de valor, sin precio en el texto. Lo que se agrega:\n• Del 9 al 26, un recuadro al final del artículo: «Este mes, el diplomado por $50 con tu especialización (10 cupos) → WhatsApp COMBO».\n• Del 27 al 30, el recuadro del Black Friday con sus porcentajes (sin precios) y la palabra BLACK.\n• El mar 1-dic se quitan los recuadros de todos los artículos, también de los anteriores.", "lun 9 · vie 27 · mar 1-dic", "Daniela"],
        ["App · Comunidades (GHL)", "El mismo post en la comunidad de GHL:\n• 9: combo\n• 13: Máster por bloques\n• 16 y 17: workshop\n• 18: gracias + combo\n• 23: aviso del Black Friday\n• 27: arranca el Black Friday (solo %)\n• 30: último día (Cyber Monday)", "según el calendario", "Daniela"],
        ["App · Campañas (OpenReply)", "Crear las campañas COMBO (lun 9) y BLACK (lun 16) con la respuesta y la mini landing de cada una:\n• COMBO solo vive en OpenReply.\n• MEMORIA sale de las campañas donde está repetida.\n• Las respuestas de ACERO dicen $225, nunca $199,99.\n• BLACK se apaga el mar 1-dic a las 00:00.", "lun 9 · lun 16 · mar 1-dic", "Ester · Daniela"],
        ["App · Ofertas y eventos (webs)", "Cargar con fecha de inicio y fin, para que aparezcan y se quiten solas:\n• Oferta «Combo de noviembre» (diplomado de Estructuras o Arquitectura por $50 con una especialización): 9 al 26-nov, en la página de inicio y en la de eventos.\n• Oferta «Black Friday»: del vie 27 al lun 30, solo con el % de cada programa (sin precio ni precio nuevo).\n• Workshop del 17: pasa a «Ya terminó» el 18.\nSe revisa en la web de la academia; la web de la consultoría no lleva estas ofertas.", "lun 9 · jue 26 · mié 18", "Daniela (carga) · Ester (aprueba)"],
        ["App · Correo", "Correos de noviembre (Dayana, 4-nov):\n• 30-oct y 1-nov: Halloween\n• 2: workshop\n• 9: lanzamiento del combo + preguntas frecuentes\n• 27: arranca el Black Friday (solo %)\n• 30: último día (Cyber Monday, solo %)\nSe eliminaron los del 10, 15, 18, 23 y 25. El correo «Novedades del mes» lleva el combo y la fecha del Black Friday. Apagar en GHL las automatizaciones viejas (Black Week 2025 y Acero a $199,99).", "cada fecha", "Ester · Aylin"],
        ["App · Tareas del equipo", "Cargar como tareas, con responsable y fecha, todas las filas de este cuadro y el checklist del mes. Un anuncio fijo con los precios vigentes, que se cambia el 27 y se quita el 28.", "hoy", "Ester"],
        ["App · Grabaciones", "Grabar en 2 minutos cómo se ofrece el combo por WhatsApp, para que el equipo comercial lo vea antes del lun 9.", "jue 5", "Dayana · Gabriel"],
        ["App · Setter, Reuniones ventas y Resumen de citas", "Guion de llamada:\n• A todo lead de especializaciones se le ofrece el combo y se le dice cuántos cupos quedan.\n• Máster: precio de bloque normal hasta el 26; del 27 al 30 (todos los países), el precio del Black Friday.\n• Del lun 23 al jue 26, recontacto uno a uno antes del Black Friday (lista y guiones en la pestaña Equipo comercial).\n• En el resumen de citas, revisar que nadie ofrezca Acero a $199,99.", "lun 9 · lun 23 · jue 26", "Ester · Sandra · Franklin · Eber"],
        ["App · Métricas y KPIs", "Seguimiento semanal de los cupos del combo (meta 10), las ventas del Black Friday por país y la meta de $10.000.", "cada lunes", "Ester"],
        ["Bot de WhatsApp", "Mensaje a Patricio programado para el jue 5:\n• Combo para todo el que pregunte por una especialización (10 cupos).\n• Acero a $225.\n• Black Friday: solo los %; el precio exacto lo da una persona.\n• COMBO y BLACK pasan a una persona.\nEster avisa cuando se llenan los cupos.", "jue 5", "Patricio"],
        ["Grupos de WhatsApp (envíos programados)", "Grupo del workshop: 6, 9, 12, 13 y 16, ya programados; el 17 se programa con el enlace del Zoom.\nComunidad 1, Comunidad 2 y Clientes:\n• workshop el 10 y el 16, ya programados;\n• falta programar el combo (lun 9) y el Black Friday (23 y 27).", "lun 9 · lun 23 · vie 27", "Claude (programa) · Dayana (aprueba)"],
        ["Comunidades fuera de la app (canal de IG, grupos de FB, comunidad de YouTube)", "El mismo post que en la comunidad de GHL, el mismo día.", "según el calendario", "Daniela"],
        ["GHL (CRM)", "Etiqueta combo-nov para contar cupos. Mini landings COMBO y BLACK, que se mandan solo por WhatsApp. Los enlaces de pago del Black Friday se apagan a las 23:59.", "lun 9 · lun 16", "Ester"],
        ["Meta Ads", "Anuncios: el combo con «$50» y el Black Friday solo con %:\n• Combo: campaña NUEVA con presupuesto propio y 4 variantes, lun 9 (Patricio, 4-nov).\n• Black Friday: los anuncios se suben unos días antes; jue 26 (agendar Máster) y del vie 27 al lun 30.\nApagar lo que no rinda a los 3-4 días. Decidir los lead magnets el lun 9.", "lun 9 · lun 9 · jue 26 · lun 30", "Olympus"],
        ["LinkedIn (3 cuentas)", "Sin ofertas ni precios: es contenido de valor. No se publica el Black Friday.", "según el calendario", "Daniela"],
        ["Al terminar (mar 1-dic)", "Quitar el Black Friday y el combo de:\n• la web (Ofertas y eventos)\n• el blog\n• las destacadas\n• el bot\n• OpenReply\n• el anuncio fijo de Tareas\n• Meta Ads\nAcero vuelve a $225 y el Máster vuelve a ir sin precio.", "mar 1-dic", "Ester (revisa) · todos"],
    ],
}

ESTRATEGIA_COMERCIAL = {
    "nota": "Actualizado el 3-nov (Dayana, en el cierre de octubre): corre el COMBO (Especialización a precio normal + Diplomado de Estructuras o Arquitectura por $50, del 9 al 26; Dayana, 4-nov) y el Black Friday tiene descuento en TODOS los programas, incluido el Máster (−25 % en el bloque). En público solo van los porcentajes (Dayana, 4-nov). FECHAS DE LA REUNIÓN DEL 4-NOV: del vie 27 00:00 al lun 30 23:59 (Cyber Monday incluido), para todos los países; se elimina el día solo de Ecuador del 20. Se quitan el acceso anticipado (LISTA) y la Black Week del 23. Nota anterior (23-oct): las decisiones de precio y de cómo se nombra cada oferta las toma ESTER. Los números de abajo son solo la propuesta de partida. La promo la recibe únicamente quien responde o escribe al WhatsApp: la página vieja no se toca (dejará de servir cuando salga la nueva) y cada oferta tiene su mini landing, que se manda solo por WhatsApp. Principios que siguen: escasez real (fecha y hora de cierre, no se reabre), bonos antes que descuentos grandes en lo caro, el Máster sin precio en público.",
    "reglas": [
        "Ninguna pieza pública enlaza la página vieja de pago. BLACK FRIDAY SOLO CON PORCENTAJES (Dayana, 4-nov): en anuncios, feed, historias, correos, comunidades, web y blog van el % y las fechas, nunca el precio final; la intriga lleva a escribir BLACK. Los precios exactos solo los tiene el equipo comercial (pestaña Equipo comercial).",
        "Las piezas dicen que HAY oferta, hasta cuándo y cómo pedirla: responder la historia, escribir la palabra por WhatsApp (SUSTO, COMBO, BLACK) o responder el correo.",
        "Excepción del combo (3-nov): el «diplomado por $50» SÍ se dice en anuncio, correo, historias, comunidades y en UNA publicación del feed (lun 9, «Un diplomado completo por $50»), porque es el gancho. El post del Black Friday (vie 27) lleva solo porcentajes (Dayana, 4-nov). El resto del feed sigue sin precios.",
        "GUION DE WHATSAPP (Dayana, 3-nov): a TODO el que llega preguntando por una especialización se le ofrece el combo, lo atienda el bot o una persona: «Si te inscribes en la especialización a su precio normal, por solo $50 más te llevas el diplomado completo. Es solo este mes y quedan [X] de 10 cupos». Sandra lleva la cuenta de cupos con la etiqueta combo-nov.",
        "10 CUPOS REALES: el combo tiene un tope de 10 en el mes. Al llegar a 10 se apaga el anuncio, se avisa en historias «cupos agotados» y el bot deja de ofrecerlo. Nunca se reabre ni se inventan cupos.",
        "Por WhatsApp una persona manda el precio y la mini landing de esa oferta. Una mini landing por oferta (SUSTO · cursos; COMBO · especialización + diplomado; BLACK · todos los programas); no se publica ni se enlaza en abierto.",
        "Los anuncios de Halloween y Black Friday llevan el botón «Enviar mensaje» y van a WhatsApp, no a la página.",
        "El Máster no lleva precio, salvo en el Black Friday (del 27 al 30): esos días se dice el precio de cada bloque con su tachado y el −25 % (Dayana, 3-nov). Fuera de esas fechas, el precio se da en la llamada.",
        "ACERO SE VENDE A $225 TODO NOVIEMBRE (Dayana, 3-nov): en octubre ninguna venta pagó los $225 (se vendió a $199,99 por PayPal). Nadie ofrece $199,99 ni descuentos sueltos; la única excepción es el Black Friday (27 al 30).",
        "El combo y el Black Friday no se suman (propuesta; lo decide Ester): el combo cierra el jue 26 a las 23:59 y el Black Friday empieza el vie 27 a las 00:00.",
        "Ester decide: el precio final, si el descuento se dice en % o en $, si la mini landing muestra el precio normal tachado, los bonos y si entran los Diplomados.",
    ],
    "ventanas": [
        ["Halloween flash", "vie 30-oct 00:00 → dom 1-nov 23:59 (Ecuador)", "Propuesta: cursos de bajo costo (~$26,99) a $19,99 con el cupón SUSTO", "Historias 31-oct y 1-nov, comunidades 30-oct, correos 30-oct y 1-nov, anuncio corto → todo termina en WhatsApp (SUSTO)"],
        ["Calentamiento + workshop", "2 → 17 nov", "Sin oferta: valor (chuletas, dato, Perú BIM, calidad) y registro al workshop", "Feed, historias, comunidades, correo del 2-nov, pauta de registro y mensajes al grupo del workshop"],
        ["Combo del mes", "lun 9 → jue 26-nov 23:59 · SOLO 10 CUPOS", "Un Diplomado completo por $50 (Estructuras o Arquitectura, a elección) con la compra de una Especialización a precio normal ($225). La llave es SOLO una especialización (con un curso de $27 el diplomado saldría en $77). Tope: 10 cupos en el mes; al llenarse se cierra aunque no sea el 26 (Dayana, 3-nov)", "Publicación del feed, correo y comunidades el 9-nov; historias 10, 18, 20, 23 y 25; anuncio propio en video de Gabriel e imagen → WhatsApp (COMBO). Por WhatsApp se le ofrece a TODO el que pregunta por una especialización"],
                ["Recontacto uno a uno", "lun 23 → jue 26-nov", "Setter y closers llaman o escriben, uno por uno, a los leads del Máster, de especializaciones y de diplomados que no compraron, para contarles el Black Friday antes de que empiece y reservarles el descuento (aquí sí se da el precio exacto, uno a uno)", "WhatsApp y llamada (lista en la pestaña Equipo comercial)"],
        ["Black Friday", "vie 27 00:00 → lun 30 23:59 (Cyber Monday)", "Cursos BIM −50 % · especializaciones −40 % · diplomados −40 % · Máster −25 % en el bloque. En público SOLO porcentajes (Dayana, 4-nov). Todos los países. Máster: se pauta y se agenda desde el jue 26", "Aviso 23 (historia y comunidades), Máster 26 (historia), arranque 27 (feed, historia, correo, comunidades, anuncios) y último día 30 (historia, correo, comunidades) → WhatsApp (BLACK)"],
    ],
    "falta_para_decidir": [
        "Ester: qué diplomados entran al combo y su precio de referencia. Los $50 cubren el certificado (Dayana, 3-nov). Todo montado antes del lun 9-nov con Daniela.",
        "Ester: los % finales del Black Friday y si el combo se suma o no. Antes del lun 16-nov.",
        "Ester: las mini landings (COMBO; BLACK), los cupones en GHL y el enlace de WhatsApp con cada palabra ya escrita, que reemplaza los corchetes de las piezas.",
        "Ester y Aylin: las plantillas de respuesta por WhatsApp con el precio y la mini landing de cada oferta.",
        "Dayana: el corte de Stripe y PayPal de noviembre de 2025 (no hay dato del Black Friday pasado; en GHL solo existe el formulario «Registro BlackFriday 2025»).",
    ],
}

# ───────────────────── EQUIPO COMERCIAL (pedido de Dayana tras la reunión del 4-nov) ─────────────────────
EQUIPO_COMERCIAL = {
    "nota": "Para Sandra, Eber, Franklin, Ester, Aylin y Patricio. Qué se vende en noviembre, a qué precio, cómo se presenta y a quién hay que volver a llamar antes del Black Friday. Sale de la reunión de cierre y apertura del 4-nov (Fathom). Meta del mes: $10.000. Los precios exactos del Black Friday están abajo y son solo para el equipo: en público van solo los porcentajes.",
    "quien": [
        ["Sandra", "Setter y ventas de cursos y del combo (nueva en el equipo)", "Llama a cada lead nuevo en menos de 30 minutos, agenda las citas del Máster con doble confirmación y se las pasa a Eber y Franklin. Vende cursos y especializaciones por WhatsApp, ofrece el combo a todo el que pregunta por una especialización y lleva la cuenta de los 10 cupos (etiqueta combo-nov). En el recontacto del Black Friday llama a los leads de especializaciones y a los compradores de cursos.", "10 combos (unos 3 por semana) · 12 citas por semana con Franklin · asistencia del 50 % o más"],
        ["Franklin", "Setter y closer", "Agenda con Sandra y cierra bloques del Máster. Después del workshop (17-nov) llama a los asistentes. En el recontacto llama a los registrados al workshop que no compraron.", "12 citas por semana (con Sandra) · 1 bloque del Máster por semana (con Eber)"],
        ["Eber", "Closer del Máster y de diplomados", "Hace las llamadas de 20 minutos del Máster. Si la persona no entra al Máster, ofrece el diplomado (downsell) o el combo. En el recontacto llama a los leads del Máster y de diplomados que no cerraron.", "1 bloque del Máster por semana · 4 reuniones realizadas por semana"],
        ["Ester", "CRM, avisos y precios", "Confirma los precios del Black Friday (antes del lun 16), monta las mini landings COMBO y BLACK, los enlaces de pago, los avisos de lead nuevo a Sandra y Franklin, y saca la lista del recontacto en GHL (vie 20).", "Pipeline limpio · 0 citas sin estado"],
        ["Aylin", "Apoyo en WhatsApp", "Apoya a Sandra con las respuestas a COMBO, BLACK y TEMARIO y con las plantillas.", "Nadie espera más de 30 minutos"],
        ["Patricio (Olympus)", "Bot de ventas y pauta", "Actualiza el bot con el combo (9 al 26), Acero a $225 y el Black Friday del 27 al 30 (solo %). Monta la campaña nueva del combo y la del Black Friday.", "Que el bot nunca dé un precio viejo"],
    ],
    "campanas": [
        ["MASTER FORM", "Continúa igual", "Todo el mes", "Leads del Máster por formulario → cita de 20 minutos"],
        ["ACERO FORM", "Continúa igual", "Todo el mes", "Leads de Acero por formulario y WhatsApp → Especialización a $225"],
        ["WORKSHOP", "Continúa igual", "Hasta el mar 17-nov", "Registro al workshop gratis → después, cita del Máster"],
        ["ACERO FORM + COMBO", "NUEVA", "lun 9 → jue 26-nov", "Upsell: +$50 USD y se lleva el diplomado de Estructuras o el de Arquitectura, a su elección. 10 cupos"],
        ["BLACKFRIDAY + CYBERMONDAY", "NUEVA", "vie 27 → lun 30-nov", "50 % off cursos BIM · 40 % off especializaciones · 40 % off diplomados · 25 % off en bloques del Máster"],
    ],
    "precios_black_friday": [
        ["Cursos BIM (todos; suben al precio original de $154,99 y sobre él va el −50 %)", "$154,99", "−50 %", "$77,49"],
        ["Especialización en Acero con Tutor IA", "$225", "−40 %", "$135"],
        ["Otras especializaciones", "$199,99", "−40 %", "$119,99"],
        ["Diplomado de Estructuras", "$500", "−40 %", "$300"],
        ["Diplomado de Arquitectura", "$400", "−40 %", "$240"],
        ["Máster · BIM Professional", "$750", "−25 %", "$562,50"],
        ["Máster · BIM Coordination", "$750", "−25 %", "$562,50"],
        ["Máster · BIM Management", "$600", "−25 %", "$450"],
        ["Máster · BIM + IA", "$900", "−25 %", "$675"],
    ],
    "nota_precios": "Estos precios son SOLO para el equipo comercial (Dayana, 4-nov). En público (anuncios, feed, historias, correos, comunidades, web y blog) el Black Friday se dice solo con porcentajes, para generar intriga: el precio exacto se da por WhatsApp o en la llamada, cuando la persona escribe BLACK o agenda.",
    "que_vender": [
        ["Máster BIM + IA por bloques", "BIM Professional $750 · BIM Coordination $750 · BIM Management $600 · BIM + IA $900", "−25 % en el bloque", "Leads del formulario del Máster (NIVEL) y registrados al workshop", "Siempre en una llamada de 20 minutos: qué hace hoy, qué quiere lograr, cuánto puede invertir → qué bloque le toca. El precio no se da por chat; del 27 al 30 se dice el precio con descuento en la llamada."],
        ["Diplomados", "Estructuras $500 · Arquitectura $400", "−40 %", "Quien no entra al Máster (downsell) y quien pregunta por un diplomado", "Se ofrece cuando el Máster no encaja por presupuesto o tiempo. Del 9 al 26 entra en el combo."],
        ["Combo del mes (lun 9 → jue 26)", "Especialización a precio normal + $50 → diplomado de Estructuras o de Arquitectura, a elección. Solo 10 cupos", "No se suma: el combo cierra el jue 26", "Todo el que pregunta por una especialización", "«Por solo $50 más te llevas el diplomado completo de Estructuras o de Arquitectura, el que elijas. Es solo este mes y quedan X de 10 cupos.» Un curso NO activa el combo."],
        ["Especialización en Acero con Tutor IA", "$225 todo noviembre (nunca $199,99)", "−40 %", "Leads de Acero (WhatsApp y formulario) y quien descargó la guía ACERO", "Se vende el tutor de IA: dudas resueltas a cualquier hora mientras cursas. Con el combo, sube a diplomado."],
        ["Otras especializaciones", "$199,99", "−40 %", "Quien pregunta por otra especialización", "Igual que Acero: se ofrece el combo."],
        ["Cursos BIM", "Precio original $154,99 (Dayana, 4-nov: todos los cursos suben a ese precio y sobre él se aplica el descuento)", "−50 % sobre $154,99 = $77,49", "Compradores de cursos y quien quiere una herramienta concreta", "Después de la compra, ofrecer subir a especialización (y al combo)."],
        ["Workshop gratis (mar 17-nov, 8:00 PM Ecuador)", "Gratis", "—", "Registrados al workshop", "Sirve para vender el Máster: del 18 al 20 se llama a los asistentes para la cita de 20 minutos."],
    ],
    "guiones": [
        ["Lead nuevo (setter, en menos de 30 minutos)", "Sandra · Franklin", "Hola [nombre], soy Sandra de Design Modeling Academy 👋 Vi que nos dejaste tus datos hace un ratito por el Máster BIM + IA. ¿Tienes 2 minutos ahora para una llamada corta y te cuento cómo funciona por bloques?\n→ En la llamada: qué hace hoy y qué quiere lograr → agendar los 20 minutos con Eber o Franklin → confirmar la cita el mismo día y 1 hora antes."],
        ["Preguntan por una especialización (WhatsApp)", "Sandra · Aylin · bot", "¡Hola [nombre]! La Especialización en Acero con Tutor IA está en $225: son 4 cursos, el certificado y un tutor de IA que te resuelve dudas mientras cursas.\nY este mes tenemos algo especial: si te inscribes en la especialización a su precio normal, por solo $50 más te llevas el diplomado completo de Estructuras o de Arquitectura, el que elijas. Es solo este mes (del 9 al 26) y quedan [X] de 10 cupos. ¿Te paso el enlace?"],
        ["«¿Y si mejor espero al Black Friday?»", "Sandra · Eber", "Depende de lo que quieras llevarte. Si es solo la especialización, en el Black Friday tiene −40 % (Acero queda en $135). Pero si quieres la especialización y el diplomado, el combo te deja los dos en $275; en el Black Friday, por separado, serían $375 con Arquitectura ($135 + $240) o $435 con Estructuras ($135 + $300). El combo cierra el jueves 26 o cuando se llenen los 10 cupos.\n(Este guion es solo para la conversación uno a uno: en público el Black Friday va sin precios.)"],
        ["Llamada del Máster (closer)", "Eber · Franklin", "1) Diagnóstico: qué hace hoy, qué quiere lograr en 6 meses, cuánto tiempo tiene a la semana y cuánto puede invertir.\n2) Recomendación: el bloque que le toca (BIM Professional si empieza; Coordination si ya modela; Management si lidera; BIM + IA si ya coordina).\n3) Precio del bloque y forma de pago.\n4) Si no entra: diplomado (downsell) o el combo si buscaba una especialización.\n5) Marcar el resultado en el CRM al colgar."],
        ["Máster en la semana del Black Friday", "Eber · Franklin", "Del viernes 27 al lunes 30 el bloque con el que empieces tiene −25 %: BIM Professional y BIM Coordination quedan en $562,50 (antes $750), BIM Management en $450 (antes $600) y BIM + IA en $675 (antes $900). Si agendamos el jueves 26, te dejo el precio reservado para el viernes."],
    ],
    "recontacto": {
        "nota": "Lo pidió Dayana el 4-nov: antes del Black Friday hay que volver a contactar UNO A UNO a todos los que preguntaron por el Máster, una especialización o un diplomado y no compraron, explicarles el descuento y ver si quieren entrar este mes. No es un envío masivo: cada persona recibe un mensaje con su nombre y su programa, y después una llamada si responde.",
        "pasos": [
            ["vie 20-nov", "Ester saca la lista en GHL (etiqueta bf-recontacto) con los 6 grupos de abajo, sin duplicados y sin los que ya compraron, y la reparte.", "Ester"],
            ["lun 23 → jue 26-nov", "Mensaje uno a uno por WhatsApp con el guion de abajo; si responde, llamada. A los del Máster, cita de 20 minutos el jue 26 para reservar el precio.", "Sandra · Franklin · Eber"],
            ["cada día", "Marcar el resultado en el CRM: reservado · interesado · no por ahora · sin respuesta.", "quien llamó"],
            ["vie 27 a primera hora", "Mandar el enlace de pago a todos los «reservados» e «interesados».", "Sandra · Eber"],
            ["lun 30 (Cyber Monday)", "Último aviso a los «interesados» que no pagaron: cierra a las 23:59.", "Sandra · Franklin · Eber"],
        ],
        "segmentos": [
            ["Leads del Máster sin cerrar (pipelines Máster High Ticket y Máster BIM + IA, últimos 90 días, incluidos los no show)", "El bloque con −25 % (desde $450)", "Eber · Franklin"],
            ["Registrados al workshop que no compraron (incluidos los 198 detenidos de un workshop anterior)", "Cita del Máster con el −25 %", "Franklin"],
            ["Leads de diplomados y downsells que no cerraron (pipeline Diplomados)", "Diplomados desde $299,99", "Eber"],
            ["Leads de Acero y de especializaciones que no compraron (pipelines Especializaciones y Olympus Cursos Lowcost)", "Acero $135 · otras $119,99", "Sandra"],
            ["Compradores de cursos (Halloween, Naves PRO)", "Subir a especialización: Acero $135", "Sandra"],
            ["Alumnos del Máster que dejaron de pagar su cuota (3)", "Caso por caso: retomar con el bloque siguiente con −25 %", "Eber (con Ester)"],
        ],
        "mensaje": "Hola [nombre], ¿cómo vas? 👋 Hace un tiempo nos escribiste por [programa] y quería avisarte antes que a nadie: del viernes 27 al lunes 30 tenemos el Black Friday de Design Modeling Academy, y [programa] tiene [−40 % / −50 % / −25 % en el bloque]. ¿Quieres que te cuente cuánto te queda y te reserve el descuento? El viernes a primera hora te mando el enlace.\n(Si responde, aquí sí se le da el precio exacto de la tabla de precios del Black Friday.)",
    },
    "bot": {
        "nota": "Cómo responde el bot de ventas en noviembre (Patricio lo actualiza el jue 5 con el mensaje del grupo de Soporte TECH). El bot informa y deriva: las ventas de combo, Black Friday y Máster las cierra una persona.",
        "filas": [
            ["Preguntan por una especialización", "Da el precio ($225 Acero, $199,99 las demás) y, del 9 al 26, ofrece el combo: diplomado de Estructuras o Arquitectura por $50 más, 10 cupos.", "Si quiere el combo, pasa a Sandra."],
            ["Escriben COMBO o BLACK", "No vende: pasa la conversación a una persona.", "Sandra (o Aylin) responde con la mini landing."],
            ["Preguntan por el Máster", "No da precio; ofrece agendar 20 minutos. Del 27 al 30 dice que hay −25 % en el bloque; el precio lo da el closer.", "Eber o Franklin hacen la llamada."],
            ["Preguntan por Acero a $199,99", "Responde que este mes está en $225 (con tutor de IA) y ofrece el combo; del 27 al 30 tiene −40 % (el precio exacto lo da una persona).", "Sandra."],
            ["Se llenan los 10 cupos del combo", "Deja de ofrecerlo.", "Sandra avisa a Patricio por el grupo de Soporte TECH."],
            ["Del vie 27 al lun 30", "Dice SOLO los porcentajes (cursos BIM −50 %, especializaciones −40 %, diplomados −40 %, Máster −25 %), nunca el precio final.", "Pasa a una persona (Sandra), que da el precio exacto y el enlace."],
            ["mar 1-dic", "Vuelve a los precios normales y el Máster vuelve a ir sin precio.", "Patricio lo actualiza el lun 30 por la noche."],
        ],
    },
    "reglas": [
        "Todo se marca en el CRM: cita asistida, no asistió, reagendó, ganada o perdida. Sin eso, Meta no aprende y no sabemos dónde se pierde la venta (Patricio, 4-nov).",
        "Ningún lead espera más de 30 minutos. Hoy el promedio es de 5 horas y por ahí se pierde la mayoría.",
        "Pipeline limpio: quien no compra pasa a su etapa o se cierra. Nada se acumula en el pipeline del Máster.",
        "Acero a $225 todo el mes. Sin $199,99 ni descuentos sueltos; la única excepción es el Black Friday.",
        "El combo solo se activa con una especialización (un curso no cuenta), tiene 10 cupos y no se suma con el Black Friday.",
        "Pagos fallidos: se llama en menos de 24 horas.",
    ],
    "fechas": [
        ["lun 9", "Arranca el combo (10 cupos, campaña ACERO FORM + COMBO) · se decide la prueba del formulario del Máster · artes nuevas de pauta"],
        ["mar 17", "Workshop, 8:00 PM Ecuador · del 18 al 20 se llama a los asistentes"],
        ["vie 20", "Ester entrega la lista del recontacto"],
        ["lun 23 → jue 26", "Recontacto uno a uno · el jue 26 a las 23:59 cierra el combo"],
        ["vie 27 → lun 30", "Black Friday para todos los países (cierra el lun 30 a las 23:59)"],
        ["mar 1-dic", "Todo vuelve a precio normal"],
    ],
}

# ───────────────────── PLAN DE PAUTA DE OLYMPUS (Patricio, 5-nov) ─────────────────────
PLAN_PAUTA = {
    "titulo": "Plan de pauta de Olympus · 5-nov al 5-dic",
    "url": "https://claude.ai/artifact/3XFVXrFSSwcT7WqQsEcqJ9",
    "nota": "Lo compartió Patricio en Estrategia General el 5-nov. Tope del mes: USD 1.200 (USD 1.125 proyectados + USD 75 de reserva). Se juzga por citas y ventas, no por costo por lead. Desde aquí se le hace seguimiento cada lunes.",
    "presupuesto": [
        ["Máster (formulario + prueba)", "USD 11", "31 días", "USD 341"],
        ["Acero (WhatsApp + formulario)", "USD 15", "31 días", "USD 465"],
        ["Workshop (saldo)", "—", "hasta el 17-nov", "USD 29"],
        ["Lead magnets", "USD 2", "hasta el lun 9", "USD 10"],
        ["Combo (campaña nueva)", "USD 10", "lun 9 → jue 26", "USD 180"],
        ["Black Friday", "USD 20", "jue 26 → lun 30", "USD 100"],
        ["Reserva para lo que venda", "—", "—", "USD 75"],
    ],
    "seguimiento": [
        ["dom 8", "Fabián revisa si la asistencia llega a Meta y si los compradores están excluidos; deja armada la campaña del combo sin publicar", "Fabián", "pendiente"],
        ["dom 8", "Marcar las 13 citas de octubre sin resultado", "Eber · Franklin · Sandra", "pendiente"],
        ["jue 5", "Grabar el video del combo con Gabriel", "Dayana · Gabriel", "pendiente"],
        ["lun 9", "Las 7 acciones: pausar ACERO 1 WhatsApp (EC y MX), MX Acero WSP $5,50 → $4,50, EC $4,00 → $4,80, sumar OCT V1 y V2 a Acero WSP, sumar Bloques V2 y el video de la ruta al Máster FORM y crear la campaña del combo ($10 al día)", "Fabián", "pendiente"],
        ["lun 9", "Decidir la prueba del formulario del Máster (gana con 3 citas) y los lead magnets (si los UTM no traen leads, sus $2 al día pasan al combo)", "Olympus · Dayana", "pendiente"],
        ["lun 9", "Entregar las 3 artes nuevas («El que calcula, decide», «Modelar bonito no consigue proyectos», «Sabes más comandos. Nadie te pone a cargo.»)", "Ester · Daniela", "pendiente"],
        ["jue 12", "Revisar el combo", "Fabián", "pendiente"],
        ["lun 16", "Subir las artes nuevas, aplicar las reglas de apagado, decidir ACERO 1 en formulario y el segundo paso de México a Ecuador. Si el combo lleva menos de 3 ventas, se cambia el creativo (no la oferta)", "Fabián · Olympus", "pendiente"],
        ["lun 16", "Confirmar los precios del Black Friday (los porcentajes ya están: cursos −50 %, especializaciones −40 %, diplomados −40 %, Máster −25 %)", "Ester", "pendiente"],
        ["17 al 22", "Cerrar la campaña del workshop y dejar listos los anuncios del Black Friday (solo con %)", "Fabián", "pendiente"],
        ["jue 26", "Cerrar el combo a las 23:59 y activar el Máster del Black Friday", "Fabián", "pendiente"],
        ["27 al 30", "Revisar cada día y mover presupuesto a lo que venda", "Fabián", "pendiente"],
        ["1 al 5-dic", "Apagar las promos, volver a la pauta normal e informe final con propuesta para diciembre (sáb 5)", "Fabián · Olympus", "pendiente"],
    ],
    "reglas": [
        ["Acero WhatsApp", "Gasta USD 10 y cada conversación cuesta más de USD 1,50", "Trae una compra: se queda aunque sea más caro"],
        ["Máster", "Gasta USD 35 sin ninguna cita", "Consigue citas a USD 13 o menos, con asistencia"],
        ["Combo", "Llega a 10 cupos: se apaga el mismo día", "3 combos al lun 16: recibe parte de la reserva"],
    ],
    "ajustes": [
        "Black Friday: el plan dice «Máster sin precio, salvo Black Friday» y «usa los precios de la matriz». Desde el 4-nov (Dayana) el Black Friday va SOLO con porcentajes en todos los anuncios, Máster incluido: ningún precio exacto.",
        "Diplomados del combo: ya está decidido (Dayana, 4-nov): el de Estructuras o el de Arquitectura, a elección. Ester no tiene que confirmarlo.",
        "Proyección de cursos en Black Friday: el plan usa $13,49. Ahora los cursos suben a su precio original de $154,99 y el −50 % los deja en $77,49, así que esa línea de la proyección queda corta.",
        "Diplomados en Black Friday: el plan usa $300 (Estructuras). Arquitectura queda en $240.",
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
                    {"id": "nov-valor-6-uniones-viga-columna-reel"}, {"id": "nov-chuleta-1-perfiles-acero-reel"},
                    {"id": "nov-chuleta-3-lod-reel"}, {"id": "nov-chuleta-4-uniones-reel"}],
         "que_falta_saber": "Si las vistas y los guardados se convierten en DMs de ACERO y en ventas, o solo en guardados."},
        {"formato": "Pizarra dibujada con voz de Gabriel por IA (estilo 9)",
         "plantilla": "video-recursos/plantillas/pizarra-dibujada",
         "estado": "1 pieza buena (cimentaciones). Falta una segunda pieza y probar venta.",
         "piezas": [{"id": "cimentaciones (fuera de matriz)", "shortCode": "Der2lsgjwu5"},
                    {"id": "oct-ia-reemplazar-ingeniero-reel"}, {"id": "nov-chuleta-2-cerchas-reel"}],
         "que_falta_saber": "«¿La IA te va a reemplazar?» dio 0 comentarios en julio. Esta versión acusa 4 hábitos concretos, que es el patrón que sí funciona. Si no pasa la mediana, la chuleta de cerchas dice si falló el tema o el formato."},
        {"formato": "Gabriel + motion cromado (estilo 10)",
         "plantilla": "video-recursos/plantillas/gabriel-motion-cromado",
         "estado": "Nuevo: todavía sin pieza publicada.",
         "piezas": [{"id": "nov-gabriel-no-compres-descuento-reel"}],
         "control": "nov-gabriel-error-modelos-reel (Gabriel a cámara sin motion, 14-nov)",
         "que_falta_saber": "Si el motion suma vistas y comentarios frente a Gabriel a cámara solo."},
    ],
    "revisiones": ["lun 9-nov: la de IA de octubre; las 6 uniones (4-nov) llevan 5 días, lectura preliminar (la regla pide 7)", "lun 30-nov: cierre del mes y decisión para diciembre"],
}

DESTACADAS = [
    {"destacada": "🔩 ACERO", "que_va": "Chuletas de acero, Gabriel sobre el orden del diseño, el combo del mes y el Black Friday.",
     "agregar": ["nov-hist-1104", "nov-hist-1105", "nov-hist-1110", "nov-hist-1111", "nov-hist-1118", "nov-hist-1120", "nov-hist-1123", "nov-hist-1124", "nov-hist-1125", "nov-hist-1127", "nov-hist-1130"],
     "quitar": "El vie 27 a medianoche: los frames del combo. El mar 1-dic: todo lo que tenga % de Black Friday o cuenta regresiva (vencido)."},
    {"destacada": "🎯 BIM + IA", "que_va": "Máster por bloques, workshop, Perú BIM, checklist de calidad y preguntas sobre la IA.",
     "agregar": ["nov-hist-1109", "nov-hist-1112", "nov-hist-1113", "nov-hist-1116", "nov-hist-1117", "nov-hist-1119", "nov-hist-1126"],
     "quitar": "Después del 17-nov, los frames de cuenta regresiva y registro del workshop (dejar solo el resumen del 19)."},
    {"destacada": "🎁 HERRAMIENTAS", "que_va": "Recursos gratis (zapatas, 5 verificaciones, test de nivel) y cursos de bajo costo.",
     "agregar": ["nov-hist-1031", "nov-hist-1101", "nov-hist-1106"],
     "quitar": "El 2-nov: los frames del cupón SUSTO (vencido)."},
    {"destacada": "👥 COMUNIDAD", "que_va": "Detrás de cámara de la grabación con Daniela y del workshop.", "agregar": [], "quitar": "Recaps de más de 3 meses."},
    {"destacada": "⭐ ALUMNOS", "que_va": "Testimonios reales con permiso.", "agregar": [], "quitar": "Nada, salvo que un alumno retire su permiso."},
]
DESTACADA_DE = {i: d["destacada"] for d in DESTACADAS for i in d["agregar"]}

CHECKLIST = [
    {"tarea": "REUNIÓN DEL 4-NOV · Marcar en el CRM el resultado de las 13 citas de octubre sin estado (asistió / no asistió / reagendó). Meta guarda la atribución unos 14 días: si no se marcan ya, la API de conversiones pierde ese dato (Patricio).", "desbloquea": "Que Meta optimice por citas reales y saber si la asistencia bajó o solo falta registrarla", "cuando": "esta semana", "para": "Eber · Franklin · Sandra"},
    {"tarea": "REUNIÓN DEL 4-NOV · Llamar a cada lead nuevo en menos de 30 minutos (hoy se tarda 5 horas en promedio). Al llegar el aviso de «formulario calificado», se llama de una vez. Ester confirma que el aviso le llega a Franklin y a Sandra.", "desbloquea": "La asistencia a citas (meta: 50 % o más)", "cuando": "todo el mes", "para": "Sandra · Franklin · Eber · Ester (avisos)"},
    {"tarea": "REUNIÓN DEL 4-NOV · Medir los recordatorios automáticos de cita (activos desde el 30-oct: el mismo día, 1 hora y 15 minutos antes, y reagendar a quien faltó). Cada lunes: citas, asistencias y no show.", "desbloquea": "Saber si basta con automatizar o hace falta seguimiento extra", "cuando": "cada lunes", "para": "Olympus · Ester"},
    {"tarea": "REUNIÓN DEL 4-NOV · Nuevas artes de pauta para refrescar los anuncios (fatiga), con los ganchos que funcionaron en octubre («Si todavía…», bloque 1 del Máster, Acero con Tutor IA y la imagen «Tu próximo caso no se aprende en un tutorial»).", "desbloquea": "Anuncios nuevos (no hay desde el 22-oct)", "cuando": "lun 9-nov", "para": "Ester · Daniela"},
    {"tarea": "REUNIÓN DEL 4-NOV · Coordinar los videos nuevos de Acero y del Máster para la pauta de noviembre, cuando regrese Daniela.", "desbloquea": "Pauta del Máster y de Acero con creativos nuevos", "cuando": "semana del 9-nov", "para": "Dayana · Gabriel · Daniela"},
    {"tarea": "PRECIO DE LOS CURSOS PARA EL BLACK FRIDAY (Dayana, 4-nov): todos los cursos BIM suben a su precio original de $154,99 (web, fichas y enlaces de pago) y sobre ese precio se aplica el −50 % ($77,49) del vie 27 al lun 30. El mar 1-dic se revisa el precio de los cursos.", "desbloquea": "Que el −50 % de los cursos sea real y coincida con lo que se cobra", "cuando": "antes del jue 26-nov", "para": "Ester"},
    {"tarea": "REUNIÓN DEL 4-NOV · RECONTACTO UNO A UNO antes del Black Friday: llamar o escribir a cada lead del Máster, de especializaciones y de diplomados que no compró (lista y guion en la pestaña Equipo comercial), contarle el precio del Black Friday y reservarle el cupo para el 27.", "desbloquea": "Que los que ya conocen el programa entren este mes", "cuando": "lun 23 → jue 26-nov (y seguimiento del 27 al 30)", "para": "Sandra · Franklin · Eber"},
    {"tarea": "Revisar el post del 21-oct (DexigJZl5mA): su caption abre con el texto del carrusel cancelado del workshop, que decía «Jueves 22 de octubre». Si quedó la fecha vieja, editarlo.", "desbloquea": "Que nadie llegue al workshop con la fecha equivocada", "cuando": "ya", "para": "Daniela"},
    {"tarea": "WORKSHOP: montar y probar la palabra en GHL con una cuenta ajena (IG y FB), y confirmar que solo GHL la contesta.", "desbloquea": "Reel del 31-oct y todo el feed del workshop", "cuando": "antes del vie 30-oct", "para": "Ester"},
    {"tarea": "Grabar en UNA sesión con Daniela: demo y «para quién es» del workshop, «tu nave a ojo» (celular sobre el monitor, como el referente), el reel «el error que más veo», el reel «no compres por el descuento» y los selfies de Gabriel para historias (3, 5, 10, 12, 16, 18, 23 y 27-nov). Lista de pantallas en grabaciones-pantalla-gabriel.pdf.", "desbloquea": "6 reels y 8 historias con Gabriel a cámara", "cuando": "antes del jue 29-oct (lo del workshop) y del vie 13-nov (el resto)", "para": "Gabriel y Daniela"},
    {"tarea": "Editar las 4 chuletas (cerchas 10-nov, LOD 17-nov, uniones 24-nov y perfiles de acero 30-nov) con los formatos de los reels del 19 y 20-oct que funcionaron: LOD, uniones y perfiles como «Simbología de niveles» (lista visual sin voz) y cerchas como «5 tipos de cimentación» (pizarra con voz). El 4-nov sale el video ya editado de las 6 uniones viga-columna. Gabriel revisa cada lámina técnica antes de publicar.", "desbloquea": "La serie que se llevó octubre", "cuando": "una por semana, 2 días antes", "para": "Daniela / Dayana"},
    {"tarea": "Auditar el disparador de NIVEL: 110 disparos en 3 días contra 9 tests terminados (análisis del 23-oct). Comprobar si responde a cualquier comentario con la palabra «nivel» y avisar al setter.", "desbloquea": "Las 8 piezas que piden NIVEL", "cuando": "antes del lun 2-nov", "para": "Ester / Patricio"},
    {"tarea": "CUPOS Y GUION DEL COMBO (reunión del 4-nov): Sandra lleva la cuenta de los 10 cupos (etiqueta combo-nov) y avisa al equipo y a Patricio al llegar a 10. Sandra (con el apoyo de Aylin) ofrece el combo a todo el que pregunta por una especialización por WhatsApp, con el guion de la pestaña Equipo comercial. Meta: unos 3 cupos por semana.", "desbloquea": "Que el combo se venda en cada conversación de especialización", "cuando": "desde el lun 9-nov", "para": "Sandra · Aylin"},
    {"tarea": "COMBO DEL MES (3-nov): Entran el diplomado de Estructuras y el de Arquitectura, a elección del alumno (Dayana, 4-nov; los $50 cubren el certificado). Ester y Daniela montan la mini landing COMBO, el enlace de WhatsApp con «COMBO» ya escrito, la etiqueta combo-nov en GHL y la campaña COMBO en OpenReply (una sola automatización: si va en OpenReply, no se monta también en GHL). Ponerlo donde las piezas dicen [enlace de WhatsApp…].", "desbloquea": "El correo, las comunidades y el anuncio del lun 9-nov", "cuando": "todo montado el vie 6-nov", "para": "Ester y Daniela"},
    {"tarea": "BLACK FRIDAY del vie 27 al lun 30 (reunión del 4-nov): confirmar los % y precios (cursos −50 %, especializaciones y diplomados −40 %, Máster −25 % en el bloque), la mini landing BLACK y los enlaces de pago que se apagan el lun 30 a las 23:59.", "desbloquea": "Las piezas del 23, 26, 27 y 30-nov", "cuando": "antes del lun 16-nov", "para": "Ester (decide y crea)"},
    {"tarea": "Grabar con Gabriel el anuncio del combo («Un diplomado completo por $50…», 15 s, 9:16 y 4:5) y los selfies del 10, 23 y 27-nov con los textos nuevos del combo y del Black Friday (27 al 30).", "desbloquea": "Anuncio del combo y 3 historias con Gabriel", "cuando": "jue 5-nov", "para": "Dayana y Gabriel"},
    {"tarea": "Actualizar la información del bot de ventas: combo del mes, Acero a $225 todo noviembre, Black Friday del vie 27 al lun 30 con precios (Máster incluido) y que COMBO y BLACK pasen a una persona. Se le pide por el grupo de Soporte TECH el jue 5.", "desbloquea": "Que el bot no dé precios viejos", "cuando": "jue 5-nov", "para": "Patricio"},
    {"tarea": "Respuestas a las palabras de historias, correos y comunidades (SUSTO, COMBO, BLACK, NAVES, TEMARIO, MÁSTER, NIVEL, ACERO, ZAPATA): las contesta una persona; las de oferta pasan a WhatsApp, donde va el precio y la mini landing. Dejar plantillas listas en la bandeja.", "desbloquea": "Que las historias de venta conviertan", "cuando": "antes del 30-oct", "para": "Ester y Aylin"},
    {"tarea": "Publicar los 2 reels de prueba ya editados («6 uniones acero-hormigón» y «¿La IA te va a reemplazar?») antes del 31-oct, y anotar su enlace para la revisión de formatos.", "desbloquea": "La revisión de formatos del 9-nov", "cuando": "antes del sáb 31-oct", "para": "Daniela"},
    {"tarea": "Producir la chuleta 2 (cerchas) en estilo 9, pizarra con voz, y «no compres por el descuento» en estilo 10, motion cromado. Son las piezas de prueba de formato del mes.", "desbloquea": "Comparar formatos con el mismo tipo de tema", "cuando": "2 días antes de cada fecha", "para": "Daniela / Dayana"},
    {"tarea": "Revisión de formatos en prueba: correr scripts/formatos_prueba.py --mes 2026-11 y anotar en el calendario, por pieza, cuántos llegaron al WhatsApp y cuántas ventas salieron en 14 días (GHL).", "desbloquea": "Qué formato entra fijo en diciembre", "cuando": "lun 9-nov y lun 30-nov", "para": "Ester (datos de GHL) · Dayana (decide)"},
    {"tarea": "Confirmar con Dayana los nombres de los 4 bloques del Máster y qué certificación da cada uno, y los nombres de los 4 módulos de Acero.", "desbloquea": "Post del 13, carrusel del 20 y del 23-nov", "cuando": "antes del lun 9-nov", "para": "Dayana"},
    {"tarea": "Pedir el corte de Stripe y PayPal de noviembre de 2025 (no hay dato del Black Friday pasado).", "desbloquea": "La meta de Black Friday", "cuando": "antes del 10-nov", "para": "Dayana"},
    {"tarea": "Pauta: apagar «Resto» de ACERO WSP, las 2 campañas LEAD MAGNETS y ACERO TEST GANCHOS; subir la campaña de registro del workshop (2 al 16-nov).", "desbloquea": "Leads más baratos y registros al workshop", "cuando": "lun 2-nov", "para": "Olympus"},
    {"tarea": "Pauta del combo (6 al 26-nov, campaña nueva con presupuesto propio) y del Black Friday (vie 27 al lun 30, todos los países; Máster desde el jue 26; anuncios subidos unos días antes). Decidir el lun 9-nov si sigue la prueba del formulario de calificación del Máster, por citas y costo por cita.", "desbloquea": "Las ventas del combo y del Black Friday", "cuando": "lun 9, jue 26 y lun 30-nov", "para": "Olympus"},
    {"tarea": "La guía de regalo «conectar la IA a tu Revit» (la promete la landing y el mensaje del 16-nov) tiene que existir antes del workshop. Definir quién la hace.", "desbloquea": "Promesa del workshop", "cuando": "antes del lun 16-nov", "para": "Dayana (asigna)"},
    {"tarea": "Juntar las pruebas reales para las historias de venta (frame 2): 3 o 4 mensajes de alumnos con permiso o con el nombre tapado, el testimonio del alumno de Acero, una nave en SAP2000 de Naves PRO, un reporte de interferencias de Navisworks y una captura del Tutor IA de Acero.", "desbloquea": "Las 12 historias de venta en 3 tiempos", "cuando": "antes del lun 2-nov", "para": "Daniela / Ester"},
    {"tarea": "Gabriel confirma lo que dice a cámara en las historias de venta («me tomó años…», «he visto a muchos ingenieros…») y revisa los datos técnicos de las historias de valor (perfiles, recubrimiento ACI, cerchas, uniones).", "desbloquea": "Que nada de lo que se publica sea inexacto", "cuando": "antes de la sesión de grabación", "para": "Gabriel"},
    {"tarea": "Cada viernes, guardar las historias de la semana en su destacada; el 2-nov quitar SUSTO, el 27 el combo y el mar 1-dic todo lo de Black Friday.", "desbloquea": "Destacadas al día", "cuando": "viernes 6, 13, 20 y 27", "para": "Daniela"},
    {"tarea": "Publicar los 4 blogs (6, 13, 20 y 27) con su post de anuncio.", "desbloquea": "G3 del mes", "cuando": "cada viernes", "para": "equipo de contenido"},
]


def main():
    feed = [fila_feed(*f) for f in FEED]
    cuota = [x for x in feed if not x.get("fuera_de_cuota")]
    fmt = Counter("reel" if "REEL" in (x["formato_publicacion"] or "").upper() else
                  "carrusel" if "CARRUSEL" in (x["formato_publicacion"] or "").upper() else "post" for x in cuota)
    inten = Counter("objeción/testimonio" if x["intencion"] in ("objeción", "testimonio") else x["intencion"] for x in cuota)
    hist = filas_de("GRUPO 5")
    ventas = sum(1 for x in hist if x.get("venta"))
    gab = sum(1 for x in hist if x.get("gabriel_a_camara"))
    cal = {
        "mes": "2026-11",
        "subtitulo": "Del miércoles 28 de octubre al lunes 30 de noviembre · Halloween, workshop del 17-nov, combo del mes (9 al 26) y Black Friday del 27 al 30 (con Cyber Monday) · escrita para vender Máster por bloques y Especialización en ACERO",
        "ventas_por_semana_max": 4,
        "reglas_del_mes": [
            "LO QUE APRENDIMOS EN OCTUBRE (análisis del 23-oct): dos reels que NO estaban en la matriz —«Simbología de niveles en planos ¿Cuál usas más?» (57.230 vistas, 220 comentarios, 2.455 guardados, 705 compartidos, el más compartido de la cuenta) y «5 tipos de cimentación» (8.598 vistas, 7,33 comentarios por 1.000)— se llevaron el 44 % de las vistas y el 71 % de los guardados del mes. Por eso noviembre abre la SERIE CHULETA: 4 reels, uno por semana.",
            "REFERENTES (Graph API, 23-oct; Apify sin crédito este mes): el reel DeGtyhfoXar de @lexmrbim («Conecta Revit + IA paso a paso») sacó 98.570 vistas y 3.162 comentarios. Su mediana de reels (5.224) es casi la nuestra (5.306): lo que lo separa es que CADA tutorial termina en un recurso por palabra (reels con palabra: 14 comentarios por 1.000; sin palabra: 0). Se adapta en dos reels (7 y 19-nov). @aecode.ai: lo que le funciona son carruseles comparativos con un problema de obra en el gancho.",
            "LO QUE NO FUNCIONÓ: los anuncios de producto sueltos en el feed (tutor, certificado, carrusel del workshop: 0 comentarios) y los reels de opinión sobre la IA y los clips de clase de los sábados (936 a 1.177 vistas, 0 a 2 comentarios). Cada producto entra detrás de un problema o de un dato. El workshop no tuvo registros porque todavía no se había promocionado: no hay anuncio y ninguna historia lo mencionaba.",
            f"FEED: {len(cuota)} piezas + {len(feed) - len(cuota)} videos de valor pendientes de octubre (fuera de cuota, ya editados) · formato {fmt['reel']} reels / {fmt['carrusel']} carruseles / {fmt['post']} posts · intención {inten['problema']} problema / {inten['solución']} solución / {inten['objeción/testimonio']} objeción.",
            "EFEMÉRIDES Y TENDENCIAS ENTRAN AL CALENDARIO (pedido de Dayana, 23-oct): Día de Difuntos y de Muertos, Día de la Ciencia, World Quality Day, Buen Fin, Black Friday (27-nov) y Cyber Monday (30-nov), y la tendencia del sector: BIM obligatorio en Perú. Tabla completa en la pestaña Resumen.",
            f"HISTORIAS CON MÁS VENTA Y CON GABRIEL (Dayana, 23-oct): {ventas} historias de venta en el mes (2 por semana hasta el workshop; después, el combo y el Black Friday) y Gabriel a cámara en {gab} días (al menos 2 por semana), grabadas en una sola sesión con Daniela.",
            "DAR A CONOCER LOS PROGRAMAS: el Máster por bloques (BIM Professional · Coordination · Management · BIM + IA) y la Especialización en Acero se explican con piezas propias (13, 20 y 23-nov), siempre desde el problema y sin precio en el feed.",
            "PALABRAS DE COMENTARIO: NIVEL (Máster), ACERO, ZAPATA y WORKSHOP (hasta el 17-nov). En historias, las respuestas (SUSTO, NAVES, COMBO, BLACK) llegan por DM y las contesta una persona. No hay lead magnet nuevo este mes.",
            "LAS PIEZAS DE VENTA NO USAN PALABRAS DE LEAD MAGNET (Dayana, 30-oct): ACERO, NIVEL y ZAPATA disparan la automatización del recurso gratis (ACERO manda la guía de las 5 verificaciones). Para pedir la información de un curso: TEMARIO (Especialización en Acero), MÁSTER, NAVES; para las ofertas: SUSTO, COMBO y BLACK. Las piezas de valor siguen con la palabra de su recurso.",
            "COMBO Y BLACK FRIDAY (Dayana, 3-nov, cierre de octubre): del lun 9 al jue 26 corre el combo (Especialización a precio normal $225 + Diplomado de Estructuras o Arquitectura por $50; la llave es SOLO una especialización; solo 10 cupos en el mes; anuncio propio en video e imagen, una publicación del feed y se ofrece por WhatsApp a todo el que pregunta por una especialización). Black Friday en todos los programas del vie 27 al lun 30, todos los países (reunión del 4-nov; propuesta: cursos −50 %, especializaciones y diplomados −40 %, Máster −25 % en el bloque; en público solo los %, Dayana 4-nov). Se quitan el acceso anticipado, la Black Week y el día solo de Ecuador. Los números los confirma Ester.",
            "ACERO A $225 SÍ O SÍ (Dayana, 3-nov): la Especialización en Acero con Tutor IA se vende a $225 todo noviembre, sin $199,99 ni descuentos sueltos (en octubre ninguna venta pagó los $225). La única excepción es el Black Friday (27 al 30).",
            "LA PROMO SOLO POR WHATSAPP (Dayana, 23-oct): ninguna pieza pública lleva el precio de la oferta ni enlaza la página vieja (excepciones del 3 y 4-nov: el «diplomado por $50» del combo se dice en anuncio, correo, historias, comunidades y una publicación del feed; el Black Friday muestra sus precios en anuncios, el post del feed, historias, correo, comunidades, la web (Ofertas y eventos) y el recuadro del blog). Quien responde o escribe al WhatsApp recibe el precio y la mini landing de su oferta. Ester decide los precios y cómo se nombran. El Máster no lleva precio salvo en el Black Friday. Toda oferta cierra a la hora dicha (Ecuador) y NO se reabre.",
            "FORMATOS EN PRUEBA: chuleta visual sin voz, pizarra con voz de Gabriel (estilo 9) y Gabriel con motion cromado (estilo 10). Se revisan el 9 y el 30-nov. Un formato entra fijo solo si genera interés, interacción y ventas (pestaña Resumen).",
            "Visuales = capturas reales de Revit/Robot/Navisworks y cámara de Gabriel. Nada técnico se publica sin que Gabriel lo revise (regla 0).",
            "Mínimo 60 % en el NÚCLEO. Cero OBRA. Ninguna pieza repite un id o un gancho ya usado.",
        ],
        "checklist_tareas": CHECKLIST,
        "efemerides": EFEMERIDES,
        "estrategia_comercial": ESTRATEGIA_COMERCIAL,
        "actualizar_por_canal": ACTUALIZAR_POR_CANAL,
        "equipo_comercial": EQUIPO_COMERCIAL,
        "plan_pauta": PLAN_PAUTA,
        "formatos_prueba": FORMATOS_PRUEBA,
        "publicidad": {
            "nota": "Primero se apaga lo que no trae nada; después entran la campaña de registro del workshop y las de Black Friday.",
            "campanas": [{"nombre": k, "piezas": [ficha_anuncio(i, k) for i in v]} for k, v in ADS.items()],
            "indicaciones": DECISIONES_PAUTA,
        },
        "grupos": [
            {"n": 1, "nombre": "GRUPO 1 · Feed principal — Instagram, Facebook, TikTok, YouTube Shorts",
             "descripcion": "4-5 piezas por semana. La serie Chuleta sale martes o miércoles; el workshop ocupa su carrusel y sus dos videos; el Black Friday (vie 27) lleva sus precios en el post del feed.",
             "reglas": ["Cada pieza lleva el CTA de su producto: Máster → NIVEL; ACERO → ACERO; concreto → ZAPATA; workshop → WORKSHOP (hasta el 17).",
                        "Si la pieza VENDE la especialización (no regala un recurso), la palabra es TEMARIO; el combo, COMBO; el Black Friday, BLACK. ACERO entrega la guía gratis, no la información del curso.",
                        "En TikTok y YouTube Shorts, sin palabra clave: pregunta abierta."],
             "calendario": feed},
            {"n": 2, "nombre": "GRUPO 2 · Comunidades — WhatsApp, canal de IG, grupos de FB, comunidad de YouTube, comunidades GHL",
             "descripcion": "Un solo post completo, el mismo en todos los canales: 6 del workshop (plan), Halloween, Acero, Máster por bloques, 2 del combo y 2 del Black Friday.",
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
             "reglas": ["DÍAS DE VENTA, en 3 tiempos: 1) curiosidad (la pieza que falta), 2) prueba REAL con captura, 3) «Respóndeme X si estás cansado de… y de…».", "DÍAS DE VALOR, en 3 tiempos: 1) curiosidad, 2) el dato o el tip, 3) «Respóndeme X y te mando [recurso gratis]» o el enlace del workshop.", "La apertura del frame 1 no se repite: cada historia arranca distinto.", "La prueba nunca se inventa: mensajes de alumnos (nombre tapado si no hay permiso), modelos o resultados reales.", "Precio nunca en la historia: va por DM o WhatsApp, con la mini landing de la oferta.", "Máximo 4 frames.", "Las respuestas llegan como DM: se contestan a mano el mismo día.", "SIN HISTORIAS sábados, domingos ni feriados (lunes 2 y martes 3 de noviembre). Si hay una promo el fin de semana, va UN solo frame programado: repost del post o el arte, con su «Respóndeme X» solo si la palabra la contesta una automatización."],
             "calendario": [{**x, **({"destacada": DESTACADA_DE[x["id"]]} if x["id"] in DESTACADA_DE else {})} for x in hist]},
        ],
        "lead_magnets": {
            "nota": "Noviembre NO lanza lead magnet nuevo (análisis del 23-oct): ZAPATA, ACERO y MEMORIA están vivas, COTIZA no arrancó (9 contactos al bot) y OpenReply no envía nada desde el 10-oct.",
            "plan_noviembre": {
                "problema": "Cierre de octubre (3-nov): la gente sí pide los recursos, pero se pierde en el camino y nadie le ofrece el paso siguiente. NIVEL: 708 lo pidieron (169 en la última semana, por la chuleta) y 59 terminaron el test (8 %). ACERO: 244 la pidieron y 66 recibieron la guía (27 %). ZAPATA: 230 y 164 (71 %). La pauta de lead magnets (visitas al perfil) gastó $58 en octubre y dejó 1 conversación.",
                "acciones": [
                    ["Pauta", "Olympus optimiza a vistas de la página de destino con el píxel en las landings. El lun 9-nov se decide con los UTM: si no trae leads, se apaga y ese dinero va a pautar la chuleta ganadora con su palabra clave.", "Olympus", "lun 9-nov"],
                    ["Arreglar la entrega", "Probar NIVEL y ACERO con una cuenta ajena (IG y FB) y encontrar en qué paso se cae la gente (link, formulario, test, correo).", "Ester", "esta semana"],
                    ["Segundo paso", "Un mensaje por DM de Instagram a las 23 horas (dentro de la ventana de 24 horas, sin riesgo de bloqueo de WhatsApp; reunión del 4-nov) a cada persona que pidió un recurso, con la oferta del mes: ACERO y ZAPATA → combo (especialización + diplomado por $50); NIVEL → cita del Máster; MEMORIA → diplomado.", "Ester y Aylin", "desde el lun 9-nov"],
                    ["Ordenar", "Una palabra, una sola automatización: MEMORIA está en 3 campañas de OpenReply a la vez, GUIA en 2 y BIM/IA en 2. Se retiran COTIZA y DYNAMO, que no traen gente.", "Ester", "esta semana"],
                    ["Medir", "Cada lunes: cuántos piden, cuántos reciben, cuántos conversan y cuántos compran en 14 días (embudo-leadmagnets.json + GHL).", "Ester · Dayana", "cada lunes"],
                ],
            },
            "nuevo": [],
            "respaldo": [{"nombre": "5 verificaciones en acero", "palabra": "ACERO", "por_que": "CTA de las chuletas de acero y de Acero."},
                         {"nombre": "Test de Nivel BIM", "palabra": "NIVEL", "por_que": "Puerta al Máster. Auditar el disparador antes del 2-nov."},
                         {"nombre": "Calculadora de Zapatas", "palabra": "ZAPATA", "por_que": "Subió de 181 a 214 etiquetados tras las chuletas de octubre."}],
            "mapa_cta": [{"palabra": "WORKSHOP", "fecha": "31-oct, 3, 5, 16 y 17-nov", "producto": "Registro al workshop"},
                         {"palabra": "NIVEL", "fecha": "2, 9, 12, 13, 14, 18, 21, 23 y 28-nov", "producto": "Máster"},
                         {"palabra": "ACERO", "fecha": "4, 10, 19, 24 y 30-nov", "producto": "Guía de las 5 verificaciones (lead magnet)"},
                         {"palabra": "TEMARIO", "fecha": "historia del 5-nov, 20 y 25-nov", "producto": "Información de la Especialización en Acero (venta)"},
                         {"palabra": "COMBO", "fecha": "9-nov (feed, correo y comunidades), historias 10, 18, 20, 23 y 25-nov", "producto": "Combo del mes: especialización + diplomado por $50 (venta)"},
                         {"palabra": "BLACK", "fecha": "23, 26, 27 y 30-nov (feed, historias, correo, comunidades)", "producto": "Black Friday del 27 al 30 (venta)"},
                         {"palabra": "ZAPATA", "fecha": "6, 7, 11 y 26-nov", "producto": "Calculadora de zapatas"}],
        },
        "destacadas": {"responsable": "Daniela", "nota": "Se alimentan cada viernes; lo vencido (SUSTO, cuenta regresiva del workshop, Black Friday) se quita al día siguiente de cerrar.", "lista": DESTACADAS},
        "correos_nota": "A la lista propia (Dayana, 4-nov): Halloween (2), workshop (2-nov), combo (lun 9, lanzamiento + preguntas) y Black Friday (27 y 30, solo con %). Se eliminaron los del 10, 15, 18, 23 y 25.",
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
        "resumen_cierre": f"Noviembre: {len(feed)} piezas de feed con la serie Chuleta (el formato que se llevó octubre), el workshop del 17 con todas sus piezas, Halloween, el combo del mes y el Black Friday del 27 al 30 (con Cyber Monday), {len(hist)} días de historias ({ventas} de venta, {gab} con Gabriel a cámara), comunidades, LinkedIn, 4 blogs, {len(correos())} correos y la pauta.",
        "pie": "Design Modeling Academy · Matriz de contenido noviembre 2026 (28 oct – 30 nov) · métricas reales de Meta Graph API, análisis de referentes con Apify y efemérides verificadas con fuente.",
    }
    json.dump(cal, open(M / "calendario-noviembre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok ·", len(feed), "feed ·", dict(fmt), dict(inten), "·", sum(len(g["calendario"]) for g in cal["grupos"]), "entradas")


if __name__ == "__main__":
    main()
