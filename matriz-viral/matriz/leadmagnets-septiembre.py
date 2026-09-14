# -*- coding: utf-8 -*-
"""Los tres recursos gratuitos de septiembre, desarrollados y con su montaje.

Por que existe este archivo aparte: en julio salio al aire un CTA que prometia
un recurso que no estaba montado, y los comentarios se quedaron sin respuesta.
La leccion no fue «hay que crear el recurso»: fue que el recurso y su embudo
son UNA sola entrega, y que mientras el bot no responda con el enlace, el
recurso no existe aunque el archivo este hecho.

El paso a paso de GoHighLevel sale del metodo probado con la Calculadora de
Zapatas (skill leadmagnet-app), no de la teoria.
"""

MEDIDA_FEED = "1080x1350 px (4:5)"
MEDIDA_CARR = "1080x1080 px (1:1)"
ESTILO = (" Estilo Design Modeling Academy: fondo azul marino #0E2438, acentos en ámbar #E8A04A, "
          "tipografía sans-serif de palo seco muy gruesa, composición limpia y con aire, sin stock "
          "corporativo ni gente sonriendo a cámara. El texto final se monta en Canva: la IA entrega "
          "el fondo y los elementos, no las letras.")

REGLA = ("Ningún CTA sale al aire sin su recurso VIVO y su disparador montado el día de la "
         "publicación. Si el recurso no llegó a tiempo NO se aplaza la pieza: se publica con el CTA "
         "de reemplazo. Prometer y no entregar cuesta más que cambiar la palabra.")

# ═══════════════ EL MONTAJE EN GHL — el mismo para los tres ═══════════════
PASOS_GHL = [
    ("1. El archivo, con URL propia y estable",
     "El PDF o el ZIP se sube y queda con una URL fija que no cambie nunca. Si mañana se "
     "reemplaza el archivo, se reemplaza en esa misma URL — porque esa dirección va a quedar "
     "escrita en correos, en DMs y en comentarios que siguen vivos meses después."),
    ("2. Embudo de dos páginas",
     "Página 1: la captura, con el formulario a la vista sin tener que bajar. Página 2: gracias, "
     "y ahí mismo el BOTÓN DE DESCARGA. El acceso es inmediato en pantalla. Nunca poner «te lo "
     "enviamos por correo» si no existe un workflow que lo envíe: es la promesa que más rápido se "
     "rompe."),
    ("3. Formulario nativo de GHL, no de terceros",
     "Nombre, correo, WhatsApp y una pregunta de perfil («¿en qué trabajas hoy?»). El formulario "
     "nativo mete el contacto directo al CRM sin costo por ejecución; el Inbound Webhook es "
     "prémium y cobra por cada envío. Al terminar, redirección automática a la página 2."),
    ("4. Etiquetas desde el primer segundo",
     "Cada contacto entra con dos etiquetas: una de tema (lead-revit-ia, lead-dynamo, "
     "lead-memoria-calculo) y una de origen (origen-bot-CHATGPT, origen-form, origen-comunidad). Sin "
     "la etiqueta de origen, a fin de mes no se puede decir qué recurso trajo a quién, y la "
     "pregunta de si el lead magnet sirvió se queda sin respuesta."),
    ("5. Bot de palabra clave en Instagram y Facebook — DOS ramas separadas",
     "Disparador de comentario filtrado por la palabra clave → respuesta pública → DM con el "
     "enlace. La acción de envío se configura POR SEPARADO para cada red: rama Instagram con DM "
     "de Instagram, rama Facebook con DM de Messenger. Nunca una sola acción compartida."),
    ("6. La respuesta pública lleva SIEMPRE el enlace",
     "No «te escribí al DM». El enlace visible en el comentario es la red de seguridad real: si el "
     "DM falla, la persona igual llega. Es gratis ponerlo y es lo único que salva la pieza cuando "
     "el canal falla en silencio."),
    ("7. Secuencia de correos, tres toques",
     "Correo 1 inmediato con el enlace otra vez (la gente cierra la página de gracias sin "
     "descargar). Correo 2 a las 48 h con un uso concreto del recurso. Correo 3 al día 5 con el "
     "puente al programa que le corresponde. La secuencia se enciende con la etiqueta de tema, no "
     "a mano."),
    ("8. Notificación interna al equipo",
     "Cada lead nuevo avisa al setter con el nombre del recurso y la respuesta de perfil. Un lead "
     "de memoria de cálculo no se trabaja igual que uno de Dynamo, y esa diferencia se pierde si "
     "todos caen en la misma bandeja sin etiqueta."),
    ("9. Prueba de punta a punta ANTES de publicar el post",
     "La prueba se hace comentando la palabra en Instagram Y en la copia de Facebook del mismo "
     "post. Es la única forma de detectar la falla de abajo antes de que la vean 3.000 personas."),
]

INCIDENTE = ("El DM que falla en silencio — julio de 2026, unos 35 leads perdidos. Cuando el post "
             "nace en Instagram y aparece también en Facebook, mucha gente comenta en la copia de "
             "Facebook. Si la acción «enviar DM» está atada solo al canal de Instagram, el envío "
             "falla y el workflow igual marca el paso como ejecutado: el ID de quien comentó es de "
             "Facebook, no de Instagram. La respuesta pública sí sale siempre, y por eso nadie se "
             "da cuenta. Se arregla con los pasos 5, 6 y 9 — los tres, no uno.")

CHECKLIST = [
    "Comentar la palabra clave en Instagram → llega el DM con el enlace.",
    "Comentar la palabra clave en la copia de Facebook → llega el DM por Messenger.",
    "La respuesta pública automática incluye el enlace visible.",
    "El enlace abre la página de captura en teléfono, no solo en computador.",
    "Enviar el formulario → redirige solo a la página de gracias.",
    "El botón de descarga de la página de gracias entrega el archivo correcto.",
    "El contacto aparece en el CRM con sus dos etiquetas.",
    "Llega el correo 1 con el enlace.",
    "El setter recibe la notificación con el nombre del recurso.",
    "Borrar los contactos de prueba antes de publicar.",
]

# ═══════════════════════════ LOS TRES RECURSOS ═══════════════════════════
MAGNETS = [
  dict(
    id="lm-revit-chatgpt",
    nombre="Guía «Revit + ChatGPT: resuelve errores con IA»",
    palabra="CHATGPT",
    formato="PDF de 10-12 páginas",
    estado="POR CREAR — se necesita VIVO el lunes 8",
    cuando="Semana 1. CORREGIDO 9-sep: antes decía que el reel del miércoles 9 ya lo prometía — eso era del reparto viejo. El del Mié 9 es reel-deriva y pide MEMORIA. CHATGPT la piden el Mié 16 y el Mié 30, y el propio reel de lanzamiento del Mar 8.",
    promesa="Los 10 errores de Revit que más tiempo hacen perder, y el prompt exacto que los "
            "resuelve — con la advertencia de cuándo NO hacerle caso a la respuesta.",
    para_quien="Quien ya usa Revit todos los días y pierde tardes enteras buscando en foros.",
    por_que="El reel de duplicados del miercoles 16 y el del limite de la IA del miercoles 30 cuentan exactamente esto, y sus CTA apuntan aqui. El recurso no se inventa para llenar un hueco: existe porque ya hay piezas que lo piden.",
    contenido=[
        "Los 10 errores: qué dice Revit, qué significa de verdad y qué lo causa.",
        "El prompt exacto para cada uno, escrito para copiar y pegar, con el contexto que hay que "
        "darle a ChatGPT para que la respuesta sirva (versión, disciplina, qué se intentó ya).",
        "Cómo pegar el mensaje de error completo sin filtrar datos del cliente — se tapan nombres "
        "de proyecto y rutas antes de pegar nada.",
        "La página que más importa: CÓMO VERIFICAR LA RESPUESTA. Tres comprobaciones antes de "
        "aplicar lo que dijo la máquina en un modelo que alguien va a firmar.",
        "Qué NO preguntarle: dimensionamiento, cumplimiento de norma y cualquier decisión que "
        "termine en una firma.",
    ],
    produccion=[
        "Los 10 errores salen de casos reales, no de una lista de internet: se sacan del soporte "
        "de los cursos y de lo que pregunta la gente en la comunidad.",
        "Cada prompt se prueba antes de entrar a la guía. Si alguien lo copia y no da lo que "
        "promete, la guía deja de valer y de paso nos deja mal.",
        "Disclaimer educativo en la última página, igual que en la Calculadora de Zapatas.",
    ],
    ghl=[("Palabra clave", "CHATGPT"),
         ("Etiquetas", "lead-revit-ia · origen-bot-CHATGPT"),
         ("Pregunta de perfil", "¿Qué usas hoy para resolver un error de Revit?"),
         ("Entrega", "Botón de descarga en la página de gracias."),
         ("Puente", "Correo 3 lleva al módulo BIM + IA — sin precio, con «agenda una cita»."),
         ("Reemplazo si no llega", "El CTA cambia a MEMORIA, que está activa. GPT IA Pro sigue existiendo pero ya no tiene palabra: en blog va con enlace directo.")],
    posts=[dict(
        fecha="Mar 8", formato="REEL (grabar) — EXTRA de lanzamiento", red="Instagram + Facebook + TikTok",
        guion_en="reels-septiembre.py → REELS_LEADMAGNET → pauta-guia, con el CTA cambiado a "
                 "comentario en vez de formulario: se graba una vez y se monta dos veces.",
        hook="Llevo dos horas en un foro por un error que ChatGPT me resolvió en cuarenta segundos.",
        caption="Ese error de Revit que te frena la tarde casi siempre está mal explicado por el "
                "propio mensaje: dice una cosa y el problema es otra.\n\nJunté los 10 que más "
                "tiempo hacen perder, con el prompt exacto para cada uno. Y una página que importa "
                "más que las otras diez: cómo verificar la respuesta antes de meterla en un modelo "
                "que vas a firmar.\n\nEs gratis. Comenta CHATGPT y te llega.\n\n¿Cuál es el error de "
                "Revit que más veces te ha tocado buscar?",
        cta="Comenta CHATGPT",
        prompt="Imagen 1080x1350 px (4:5) para la portada del reel. Fondo azul marino #0E2438. Un "
               "cuadro de diálogo de error de software, dibujado en línea fina ámbar #E8A04A, "
               "flotando en el centro, con el texto ilegible a propósito — solo se lee la forma de "
               "la ventana y su icono de advertencia. Detrás, muy tenue, una retícula de planta de "
               "Revit. Sensación de estar trabado, no de catástrofe." + ESTILO
  ), dict(
        fecha="Jue 10", formato="CARRUSEL (7 slides) — EXTRA de lanzamiento",
        red="Instagram + Facebook + LinkedIn (PDF)",
        por_que="Segunda pieza del mismo recurso, dos días después del reel. El reel da alcance "
                "y el carrusel da guardados, que es donde vive este contenido: un error de Revit "
                "se guarda para cuando vuelva a pasar. Y son dos ventanas de comentarios para la "
                "misma palabra en vez de una.",
        hook="El mensaje de error de Revit casi nunca dice cuál es el problema.",
        slides=[
         "1 · EL MENSAJE DE ERROR TE ESTÁ DICIENDO OTRA COSA. Cinco de los diez que más tiempo "
         "hacen perder, y qué significan de verdad.",
         "2 · «No aparece en la vista» — y el elemento SÍ está. Es el que más tiempo hace perder "
         "de toda la lista, y casi nunca es un error: el elemento existe, pero la vista está "
         "configurada para no mostrarlo.",
         "3 · «Highlighted walls overlap». Dos muros ocupando el mismo espacio. Revit sigue "
         "trabajando, pero al calcular áreas de habitación va a ignorar uno de los dos — y el "
         "cuadro de áreas sale mal SIN AVISAR.",
         "4 · «There are identical instances in the same place». Dos elementos idénticos, uno "
         "exactamente encima del otro. Los planos se ven bien. El cuadro de cantidades cuenta "
         "el doble.",
         "5 · «Elements are joined but do not intersect». Siguen unidos, pero ya no se tocan: "
         "normalmente porque uno se movió después.",
         "6 · «The linked file could not be found». El vínculo apunta a una ruta que ya no "
         "existe. Alguien movió, renombró o guardó en otra carpeta.",
         "7 · Los diez, cada uno con su prompt. Y la página que importa más que las otras diez: "
         "cómo comprobar la respuesta antes de aplicarla. COMENTA CHATGPT."],
        caption="El error que te frena la tarde casi siempre está mal explicado por el propio "
                "mensaje: dice una cosa y el problema es otra.\n\n"
                "Los dos peores no dan ningún aviso. Dos muros superpuestos hacen que el cuadro "
                "de áreas salga mal sin decírtelo, y dos elementos idénticos encima hacen que el "
                "de cantidades cuente el doble. Los planos, mientras tanto, se ven perfectos.\n\n"
                "Junté los 10 que más tiempo hacen perder, con el prompt exacto para cada uno y "
                "cómo verificar la respuesta antes de meterla en un modelo que vas a firmar.\n\n"
                "Es gratis. Comenta CHATGPT y te llega.\n\n"
                "¿Cuál de los cinco te ha tocado más veces?",
        cta="Comenta CHATGPT",
        prompt="Siete imágenes de 1080x1080 px (1:1) de la misma familia, para carrusel. Fondo "
               "azul marino #0E2438. En cada una, un cuadro de diálogo de software dibujado en "
               "línea fina ámbar #E8A04A, siempre en la misma posición y a la misma escala, con "
               "el texto ilegible a propósito — solo se lee la forma de la ventana y su icono de "
               "advertencia. Lo que cambia de tarjeta a tarjeta es el fondo detrás del cuadro: "
               "una retícula de planta, dos muros solapados, dos objetos idénticos desfasados un "
               "milímetro, dos volúmenes que casi se tocan, y una carpeta vacía. Todo en línea "
               "blanca muy tenue. Sin texto legible en ninguna." + ESTILO),
  ]),
  dict(
    id="lm-dynamo-python",
    nombre="Pack starter de scripts Dynamo / Python para Revit",
    palabra="DYNAMO",
    formato="ZIP con 5 scripts comentados + guía de instalación en la propia página",
    estado="POR CREAR",
    cuando="Semana 3. Necesita más producción que los otros dos porque hay que probar cada script.",
    promesa="Cinco scripts que hacen en un clic lo que hoy haces a mano, con el código comentado "
            "línea por línea para que puedas cambiarlos.",
    para_quien="Quien ya modela bien y empieza a repetir tareas: renombrar, exportar, numerar, "
               "revisar parámetros.",
    por_que="Dynamo es el tema con mejor tasa de guardado de la cuenta y no tenemos ni un recurso "
            "propio sobre él. Guardar un post es la señal de «esto me sirve pero ahora no puedo»: "
            "es exactamente la gente que descarga un pack de scripts.",
    contenido=[
        "Script 01 — auditoría de advertencias del modelo a un CSV. SOLO LEE.",
        "Script 02 — elementos duplicados exactamente en el mismo sitio. SOLO LEE, no borra nada "
        "a propósito: la decisión de qué se borra es del que modela.",
        "Script 03 — renombrar vistas en lote, con buscar y reemplazar. MODIFICA EL MODELO.",
        "Script 04 — vistas que no están en ninguna hoja. SOLO LEE.",
        "Script 05 — rellenar un parámetro en lote. MODIFICA EL MODELO.",
        "La instalación va dentro de la propia guía («Cómo se instalan, 5 minutos»), no en un PDF "
        "aparte: son cinco pasos y abrir otro archivo para leerlos sobra.",
    ],
    produccion=[
        "Cada script se corre en un modelo de prueba antes de entrar al pack. Un script que falla "
        "en la máquina de otra persona hace más daño que no haber publicado nada.",
        "El comentario de cada línea es la mitad del valor: el pack enseña, no solo automatiza.",
        "Se dice la versión exacta de Revit y Dynamo con la que se probó. Sin eso, la mitad de los "
        "mensajes van a ser «a mí no me funciona».",
    ],
    ghl=[("Palabra clave", "DYNAMO"),
         ("Etiquetas", "lead-dynamo · origen-bot-DYNAMO"),
         ("Pregunta de perfil", "¿Qué tarea repites más veces al día en Revit?"),
         ("Entrega", "Botón de descarga del ZIP en la página de gracias."),
         ("Puente", "Correo 3 lleva al módulo BIM + IA — sin precio, con «agenda una cita»."),
         ("Reemplazo si no llega", "El CTA cambia a GPT IA Pro y el pack se corre a octubre.")],
    posts=[dict(
        fecha="Mar 22", formato="REEL (grabar) — EXTRA de lanzamiento",
        red="Instagram + Facebook + TikTok",
        guion_en="reels-septiembre.py → REELS_LEADMAGNET → pauta-dynamo, con el CTA "
                 "cambiado a comentario en vez de formulario: se graba una vez y se monta dos.",
        hook="Abriste Dynamo una vez, no supiste por dónde seguir, y lo cerraste.",
        caption="La automatización en BIM no se atasca por falta de ideas. Se atasca en el "
                "primer script: el que tienes que escribir tú, sin saber todavía qué hace cada "
                "nodo.\n\n"
                "Este pack es ese primer script hecho. Cinco, comentados línea por línea para "
                "que los cambies y no solo los ejecutes. Tres de ellos ni siquiera tocan tu "
                "modelo — solo leen — así que puedes correrlos hoy en un archivo vivo sin "
                "arriesgar nada.\n\n"
                "Con la instalación explicada en la propia guía y la versión exacta de Revit y Dynamo con la que los "
                "probamos.\n\n"
                "Es gratis. Comenta DYNAMO y te llega.\n\n"
                "¿Cuántas veces has abierto Dynamo y lo has vuelto a cerrar?",
        cta="Comenta DYNAMO",
        prompt="Imagen 1080x1350 px (4:5) para la portada del reel. Fondo azul marino #0E2438. "
               "Un grafo de nodos tipo Dynamo dibujado en línea fina ámbar #E8A04A: dos cajas "
               "conectadas por un solo cable curvo y limpio, muy pocas, con mucho aire "
               "alrededor. La idea es «el primero», no «muchos». Detrás, muy tenue, una retícula "
               "de planta. Sin texto legible dentro de los nodos." + ESTILO,
  ), dict(
        fecha="Jue 24", formato="CARRUSEL (6 slides) — EXTRA de lanzamiento",
        red="Instagram + Facebook + LinkedIn (PDF)",
        por_que="Segunda pieza del mismo recurso, dos días después del reel. Dynamo es el tema "
                "de mejor guardado de la cuenta y el carrusel es el formato que más se guarda: "
                "el reel trae el alcance y este se queda archivado. Dos ventanas de comentarios "
                "para la misma palabra.",
        slides=[
         "1 · CINCO TAREAS DE REVIT QUE NO DEBERÍAS SEGUIR HACIENDO A MANO.",
         "2 · Abrir el cuadro de advertencias, ver el número y cerrarlo. → Script 01: las saca "
         "todas a un CSV, ordenables y con el ID del elemento culpable.",
         "3 · Buscar a ojo por qué el cuadro de cantidades cuenta de más. → Script 02: te lista "
         "los elementos duplicados exactamente en el mismo sitio. No borra: decides tú.",
         "4 · Renombrar vistas una por una. → Script 03: buscar y reemplazar en lote.",
         "5 · Revisar qué vistas quedaron fuera de las hojas antes de entregar. → Script 04: te "
         "las lista. Y el Script 05 rellena un parámetro en lote.",
         "6 · Los cinco vienen comentados por dentro para que los cambies. TRES SOLO LEEN: los "
         "puedes correr hoy en un archivo vivo. COMENTA DYNAMO."],
        hook="Cinco tareas de Revit que no deberías seguir haciendo a mano.",
        caption="Si abres el cuadro de advertencias, ves el número y lo cierras; si renombras "
                "vistas una por una; o si revisas a ojo cuáles quedaron fuera de las hojas: eso "
                "ya lo hace un script.\n\nArmamos un pack con cinco, comentados línea por línea "
                "para que los puedas cambiar y no solo ejecutar. Tres de los cinco solo leen: los "
                "puedes correr hoy en un archivo vivo sin arriesgar nada.\n\nEs gratis. Comenta "
                "DYNAMO y te llega.\n\n¿Cuál de las cinco te quitaría más tiempo de encima?",
        cta="Comenta DYNAMO",
        prompt="Seis imágenes de 1080x1080 px (1:1) de la misma familia, para carrusel. Fondo azul "
               "marino #0E2438. Un grafo de nodos tipo Dynamo dibujado en línea fina ámbar #E8A04A "
               "— cajas conectadas por cables curvos — que en la primera tarjeta aparece enredado y "
               "en las siguientes se va ordenando hasta quedar en una sola línea limpia. Misma "
               "escala y mismo encuadre en las seis. Sin texto legible dentro de los nodos." + ESTILO),
  ]),
  dict(
    id="lm-memoria-calculo",
    nombre="Guía de memoria de cálculo + plantilla",
    palabra="MEMORIA",
    formato="PDF de la guía + plantilla editable (Word y Excel)",
    estado="POR CREAR — se define en la reunión de cierre del viernes 5",
    cuando="Semana 4 para el post de lanzamiento, PERO su palabra clave es la más urgente de las tres: reel-deriva la pide el Mié 9 y reel-cita-norma el Vie 25. El disparador MEMORIA tiene que estar vivo el 9, tres semanas antes de su propio lanzamiento.",
    promesa="La estructura completa de una memoria de cálculo que se sostiene ante revisión, con "
            "la plantilla para llenarla.",
    para_quien="El ingeniero que ya calcula bien pero improvisa el documento cada vez, y el que va "
               "a entregar a una entidad por primera vez.",
    por_que="Es el que pidió Dayana el 2-sep. Y encaja con lo que ya sabemos de la cuenta: los "
            "posts que revientan son los de dato de cálculo. Una memoria de cálculo es dato de "
            "cálculo convertido en documento — el mismo público, un paso más adelante.",
    contenido=[
        "Las secciones que toda memoria debe tener, en orden, y qué va en cada una.",
        "Qué se cita y cómo: normativa, hipótesis de carga, criterios adoptados y de dónde salen.",
        "Los SEIS errores por los que devuelven una memoria — y cómo se ve cada uno corregido. (Corregido 9-sep: aquí decía cinco; la guía publicada tiene seis y el reel también dice seis. El que mentía era este listado.)",
        "Plantilla editable en Word con la estructura montada, y hoja de Excel para el resumen de "
        "verificaciones.",
        "Ejemplo corto completo, de principio a fin, con números reales.",
    ],
    produccion=[
        "Este recurso lo revisa Gabriel antes de salir. Es el único de los tres que puede terminar "
        "dentro de un documento que alguien firma: si la estructura que proponemos está incompleta, "
        "el problema deja de ser de marketing.",
        "Disclaimer explícito: la plantilla es una guía de estructura, no reemplaza el criterio ni "
        "la responsabilidad del ingeniero que firma.",
        "La normativa se cita por nombre y versión, nunca se transcriben cifras: se remite a la "
        "norma vigente. Es la misma regla del tutor de IA.",
    ],
    ghl=[("Palabra clave", "MEMORIA"),
         ("Etiquetas", "lead-memoria-calculo · origen-bot-MEMORIA"),
         ("Pregunta de perfil", "¿Cada cuánto entregas memorias de cálculo?"),
         ("Entrega", "Página de gracias con dos botones: guía en PDF y plantilla editable."),
         ("Puente", "Correo 3 lleva a ACERO ($225 con el tutor de IA incluido, aquí el precio "
                    "SÍ va) o al módulo BIM "
                    "Professional según la respuesta de perfil."),
         ("Reemplazo si no llega", "El CTA cambia a las 5 Verificaciones de Acero, que ya existe.")],
    posts=[dict(
        fecha="Mar 29", formato="REEL (grabar) — EXTRA de lanzamiento",
        red="Instagram + Facebook + TikTok",
        guion_en="reels-septiembre.py → REELS_LEADMAGNET → pauta-memoria, con el CTA "
                 "cambiado a comentario en vez de formulario.",
        hook="Te devolvieron la memoria y no era el cálculo.",
        caption="Se devuelve porque el revisor no puede comprobar que esté bien. No es lo "
                "mismo.\n\n"
                "La guía trae las 12 secciones en orden y qué va en cada una, y los 6 errores "
                "por los que una memoria vuelve a tu escritorio. Los seis tienen algo en común, "
                "y está explicado.\n\n"
                "Con la plantilla en Word ya montada y la hoja de Excel para el resumen de "
                "verificaciones. Para no armarla nunca más desde cero.\n\n"
                "Es gratis. Comenta MEMORIA y te llega.\n\n"
                "¿Por qué te devolvieron la última que entregaste?",
        cta="Comenta MEMORIA",
        prompt="Imagen 1080x1350 px (4:5) para la portada del reel. Fondo azul marino #0E2438. "
               "Un índice de documento técnico dibujado en línea fina ámbar #E8A04A: doce "
               "renglones numerados, alineados, con el texto ilegible a propósito. Seis de ellos "
               "llevan una marca ámbar más gruesa al margen. Sobrio y ordenado, nada de sellos "
               "rojos. Sin texto legible." + ESTILO,
  ), dict(
        fecha="Jue 1 oct", formato="POST PLANO (1 imagen) — EXTRA de lanzamiento",
        red="Instagram + Facebook",
        por_que="Segunda pieza del mismo recurso, dos días después del reel. Va en post plano "
                "porque cumple la regla de la casa: lleva dato de cálculo verificable. Cierra "
                "el mes y deja la palabra MEMORIA pedida una vez más antes de octubre.",
        hook="Una memoria de cálculo no se devuelve por los números. Se devuelve por lo que no está escrito.",
        caption="Hipótesis que no se declararon. Criterios que se adoptaron y no se justificaron. "
                "Normativa citada sin versión.\n\nEl cálculo estaba bien. El documento no lo "
                "demostraba.\n\nArmamos la guía con la estructura completa de una memoria que se "
                "sostiene ante revisión, y la plantilla editable para llenarla.\n\nEs gratis. "
                "Comenta MEMORIA y te llega.\n\n¿Por qué te devolvieron la última que entregaste?",
        cta="Comenta MEMORIA",
        prompt="Imagen 1080x1350 px (4:5). Fondo azul marino #0E2438. Un documento técnico visto de "
               "frente y en perspectiva muy leve, dibujado en línea fina ámbar #E8A04A, con la "
               "silueta de párrafos y una tabla — el texto ilegible a propósito. Dos de sus "
               "secciones aparecen vacías, marcadas con un recuadro ámbar más grueso, como huecos. "
               "Sobrio, nada de sellos rojos ni de gestos de rechazo." + ESTILO),
  ]),
]
