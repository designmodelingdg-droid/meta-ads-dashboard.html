# -*- coding: utf-8 -*-
"""Guiones completos de los reels de septiembre y prompts de imagen del feed.

Un reel sin guion no se graba: se improvisa, y el primer segundo se va en
«hola, bueno, hoy les traigo». En agosto un reel sin gancho hizo 198 vistas y
cero de todo. Aqui cada reel esta escrito segundo a segundo — que se ve, que
se dice y que texto va en pantalla — para poder grabarlo de corrido.

Regla del primer segundo: se abre con la FRONTERA (la afirmacion que incomoda
o el dato que sorprende), nunca con la invitacion. La presentacion, si hace
falta, va despues del gancho.

Todos los reels: 1080x1920 (9:16), 30 fps, subtitulos quemados en Montserrat
ExtraBold con la palabra clave en ambar #E8A04A (pipeline de edicion de la
casa). Duracion objetivo 30-45 s.
"""

REELS = [
 # ─────────────────────────────────────────────────────────────────────────
 # LOS CINCO REELS DE VALOR — todos nuevos, 8-sep-2026
 #
 # Los cinco anteriores se retiraron. Dos estaban ya publicados en agosto:
 #   · reel-valor6 «Revit me arrojó un error…»  = «le pedia a la ia dg.mp4»
 #   · reel-espejo «El salto que más cuesta»    = «modelas bien dg reel.mp4»
 #       (su gancho empezaba literalmente «Llevas tres años MODELANDO BIEN»)
 # Los otros tres se retiran con ellos porque la instrucción fue dejar cinco
 # completamente nuevos, no cuatro nuevos y uno heredado.
 #
 # La fórmula que se repite, porque es la que funcionó en agosto: se abre con
 # una FRONTERA —una afirmación que incomoda la práctica, nunca a la persona—
 # y se cierra con un recurso real que ya existe. Sin recurso detrás es
 # provocación; sin frontera es un folleto.
 #
 # Los cuatro con más comentarios del mes fueron de DATO DE CÁLCULO. Los cinco
 # llevan uno.
 # ─────────────────────────────────────────────────────────────────────────

 {"id": "reel-deriva", "fecha": "Miércoles 9", "titulo": "Cumple resistencia y el edificio es inhabitable",
  "estado": "POR GRABAR",
  "duracion": "35-40 s",
  "cta": "MEMORIA → guía + plantilla (recurso ya publicado)",
  "nota": "Sustituye a reel-valor6, que ya salió en agosto. El ángulo es el estado límite "
          "de servicio, que es la sección que más se olvida y la que el usuario del edificio "
          "nota primero. Incomoda sin acusar: el cálculo está bien, el documento no. "
          "⚠ PRODUCCIÓN: verificar el límite de deriva contra la edición vigente de la norma "
          "antes de grabar. Si hay duda, se dice «el límite que fija tu norma» sin cifra.",
  "guion": [
   ("0:00-0:04", "Primer plano, mirada directa. Sin intro.", "Tu estructura puede cumplir resistencia y aun así el edificio ser inhabitable.", "CUMPLE RESISTENCIA Y ES **INHABITABLE**"),
   ("0:04-0:11", "Plano medio.", "Porque resistencia y servicio son dos cosas distintas, y casi todo el mundo verifica solo la primera.", "RESISTENCIA Y **SERVICIO** NO SON LO MISMO"),
   ("0:11-0:20", "Pantalla: tabla de derivas de un modelo, columna de límite resaltada.", "La deriva de entrepiso no se cae, se siente. El tabique fisurado, la puerta que roza, el piso que vibra al caminar. Nada de eso sale en una verificación de resistencia.", "LA DERIVA NO SE CAE. SE **SIENTE**"),
   ("0:20-0:29", "Pantalla: modelo con deformación exagerada.", "Y es el error que más caro sale después de entregar, porque lo detecta el usuario del edificio y ya no hay nada que corregir en papel.", "LO DETECTA EL **USUARIO**, NO EL REVISOR"),
   ("0:29-0:38", "Vuelve a cámara, tono calmado.", "Si tu memoria no tiene una sección de limitación de daños, no está incompleta: está a medias. Comenta MEMORIA y te paso la estructura completa con la plantilla.", "COMENTA **MEMORIA**")]},

 {"id": "reel-duplicados", "fecha": "Miércoles 16", "titulo": "Tus planos están bien. Tu presupuesto está mal.",
  "estado": "POR GRABAR",
  "duracion": "35-40 s",
  "cta": "GUIA → Revit + ChatGPT (recurso ya publicado)",
  "nota": "El error invisible. Es el ángulo más fuerte de los cinco porque no da ningún "
          "mensaje en Revit: los planos salen perfectos y el cuadro cuenta el doble. "
          "Se descubre al presupuestar, que es cuando ya se cotizó.",
  "guion": [
   ("0:00-0:04", "Primer plano.", "Hay un error en Revit que no te avisa. Los planos salen bien y el presupuesto sale mal.", "UN ERROR QUE **NO TE AVISA**"),
   ("0:04-0:12", "Screen-record: dos elementos idénticos superpuestos, seleccionando uno y viendo que hay otro debajo.", "Son elementos duplicados exactamente en el mismo sitio. Un Ctrl+V de más, o pegar dos veces con Paste Aligned. Encima uno del otro, invisibles.", "DUPLICADOS EN EL **MISMO SITIO**"),
   ("0:12-0:20", "Pantalla: cuadro de cantidades, número resaltado.", "En los planos no se nota, porque uno tapa al otro. En el cuadro de cantidades sí: cuenta dos.", "EN EL CUADRO **CUENTA DOS**"),
   ("0:20-0:30", "Vuelve a cámara.", "Y esto no se descubre revisando. Se descubre cuando alguien presupuesta con ese número, que es cuando ya lo mandaste.", "SE DESCUBRE AL **PRESUPUESTAR**"),
   ("0:30-0:38", "Cierre.", "La comprobación es una sola: apunta la cantidad antes de borrar. Si después no bajó en el número exacto que borraste, pasó algo más. Comenta GUIA y te paso los diez errores de Revit que más tiempo te quitan.", "COMENTA **GUIA**")]},

 {"id": "reel-advertencias", "fecha": "Viernes 18", "titulo": "400 avisos sin leer",
  "estado": "POR GRABAR",
  "duracion": "30-35 s",
  "cta": "DYNAMO → pack de 5 scripts (recurso ya publicado)",
  "nota": "El dato que ordena la pieza es la frase del cierre, y es la más compartible de "
          "las cinco. El cuadro de advertencias de Revit no se puede ordenar ni filtrar ni "
          "pasarle a nadie: ese es justo el hueco que llena el script 01 del pack.",
  "guion": [
   ("0:00-0:05", "Primer plano.", "Un modelo con cuatrocientos avisos sin leer no es un modelo grande. Es un presupuesto con cuatrocientas sorpresas dentro.", "400 SORPRESAS **DENTRO**"),
   ("0:05-0:13", "Screen-record: abriendo Manage → Warnings, la lista larga.", "Este cuadro lo abre todo el mundo una vez, ve el número, lo cierra y sigue trabajando.", "SE ABRE UNA VEZ Y SE **CIERRA**"),
   ("0:13-0:22", "Pantalla: el cuadro, intentando ordenar sin poder.", "Y hay una razón: no se puede ordenar, no se puede filtrar y no se le puede pasar a nadie. Así no se revisa nada.", "NO SE ORDENA. NO SE **FILTRA**"),
   ("0:22-0:30", "Pantalla: el mismo contenido ya en una hoja ordenable.", "En una hoja sí. Ordenado por gravedad, con el ID de cada elemento culpable, y se lo puedes mandar a quien modeló.", "EN UNA HOJA **SÍ**"),
   ("0:30-0:36", "Cierre a cámara.", "Eso lo hace un script de veinte líneas. Comenta DYNAMO y te paso cinco, con el código explicado por dentro. Tres de ellos ni siquiera tocan tu modelo.", "COMENTA **DYNAMO**")]},

 {"id": "reel-cita-norma", "fecha": "Viernes 25", "titulo": "«Según la norma» no es una cita",
  "estado": "POR GRABAR",
  "duracion": "30-35 s",
  "cta": "MEMORIA → guía + plantilla (recurso ya publicado)",
  "nota": "El motivo de devolución más frecuente y el más fácil de evitar. Sirve para el que "
          "ya calcula bien y pierde la revisión en la redacción — que es el público exacto "
          "del recurso. NO se transcribe ninguna cifra normativa: se cita la norma por nombre "
          "y versión, nunca su contenido. Misma regla del tutor de IA.",
  "guion": [
   ("0:00-0:05", "Primer plano.", "Te devolvieron la memoria y no era el cálculo.", "NO ERA EL **CÁLCULO**"),
   ("0:05-0:13", "Plano medio.", "Una memoria no se devuelve porque el cálculo esté mal. Se devuelve porque el revisor no puede comprobar que esté bien. Son dos problemas distintos y solo uno es de ingeniería.", "SOLO UNO ES DE **INGENIERÍA**"),
   ("0:13-0:22", "Pantalla: dos frases comparadas, la de arriba tachada.", "«Según la normativa vigente» no es una cita. Sin el nombre completo y sin el año, nada de lo que cuelga de esa norma se puede reproducir.", "SIN VERSIÓN NO SE **REPRODUCE**"),
   ("0:22-0:30", "Vuelve a cámara.", "Y reproducir tu resultado es exactamente lo que el revisor va a intentar hacer.", "ES LO QUE VA A **INTENTAR**"),
   ("0:30-0:36", "Cierre.", "Escribe la memoria para alguien que quiere llegar a tu número y no puede llamarte. Comenta MEMORIA y te paso la estructura completa con la plantilla en Word.", "COMENTA **MEMORIA**")]},

 {"id": "reel-limite-ia", "fecha": "Miércoles 30", "titulo": "Lo que no hay que preguntarle a la IA",
  "estado": "POR GRABAR",
  "duracion": "35-40 s",
  "cta": "GUIA → Revit + ChatGPT (recurso ya publicado)",
  "nota": "Cierra el mes marcando el límite, y es la pieza que más nos diferencia: todo el "
          "mundo publica «10 prompts para Revit», nosotros publicamos dónde la IA deja de "
          "servir. Es lo que permite que una academia de ingeniería hable de IA sin quedar "
          "mal. Tono sereno, nunca alarmista.",
  "guion": [
   ("0:00-0:05", "Primer plano, tono tranquilo.", "Una inteligencia artificial no sabe cuándo no sabe.", "NO SABE CUÁNDO **NO SABE**"),
   ("0:05-0:13", "Plano medio.", "Cuando se equivoca, se equivoca con el mismo tono de seguridad con el que acierta. Y eso es justo lo que la hace peligrosa en un modelo que alguien va a firmar.", "SE EQUIVOCA CON EL MISMO **TONO**"),
   ("0:13-0:23", "Screen-record: una respuesta segura de sí misma en pantalla.", "Le pregunté qué sección poner. Me dio un número. Sonaba razonable. Pero no tiene mis cargas, ni mi norma, ni mi suelo — y ese número lleva mi firma, no la suya.", "ESE NÚMERO LLEVA **MI FIRMA**"),
   ("0:23-0:32", "Vuelve a cámara.", "Úsala para entender qué te está diciendo el programa y para buscar más rápido. No para decidir. La línea está justo ahí, y está más cerca de lo que parece.", "PARA ENTENDER, NO PARA **DECIDIR**"),
   ("0:32-0:40", "Cierre.", "Yo compruebo tres cosas antes de aplicar nada. Comenta GUIA y te paso los diez errores con su prompt, y la página donde explico esas tres comprobaciones.", "COMENTA **GUIA**")]},
]

# ─────────────────────────────────────────────────────────────────────────────
# REELS PARA PAUTA — no son contenido de feed, son creativos de campaña
#
# Los pidió Dayana el 8-sep junto con la limpieza de los reels de valor. Se
# graban en la misma sesión pero se montan aparte: llevan CTA a landing, no a
# comentario, porque en pauta el comentario no se puede automatizar igual.
#
# En agosto el formulario trajo el lead a $0,46 contra $0,78 de WhatsApp, un 41%
# más barato. Los cuatro van a FORMULARIO.
#
# REGLA: ninguna pieza del Máster lleva precio. La de ACERO sí, porque el precio
# es el argumento: subió a $225 y la razón es el tutor.
# ─────────────────────────────────────────────────────────────────────────────

REELS_PAUTA = [
 {"id": "pauta-guia", "recurso": "Guía Revit + ChatGPT", "palabra": "GUIA",
  "estado": "POR GRABAR", "duracion": "20-25 s",
  "destino": "Formulario → landing guia-revit-ia",
  "nota": "El recurso ya está vivo y probado. Es el único de los tres que puede salir hoy.",
  "guion": [
   ("0:00-0:05", "Primer plano.", "Dos horas de foro para un error de Revit que se resuelve en dos minutos.", "2 HORAS PARA **2 MINUTOS**"),
   ("0:05-0:13", "Screen-record: el error, el prompt con contexto, la respuesta útil.", "Pero solo si le das cuatro datos: tu versión, tu disciplina, el mensaje literal y qué ya intentaste. Sin eso te responde lo que ya descartaste.", "CUATRO DATOS QUE LO **CAMBIAN TODO**"),
   ("0:13-0:20", "Vuelve a cámara.", "Diez errores, diez prompts, y la página que casi nadie escribe: cómo comprobar la respuesta antes de aplicarla.", "CÓMO **COMPROBARLA**"),
   ("0:20-0:25", "Cierre con la landing en pantalla.", "Es gratis y entras al instante. El enlace está aquí abajo.", "GRATIS · ACCESO **INMEDIATO**")]},

 {"id": "pauta-memoria", "recurso": "Memoria de cálculo + plantillas", "palabra": "MEMORIA",
  "estado": "BLOQUEADO — no sale hasta el visto bueno de Gabriel", "duracion": "20-25 s",
  "destino": "Formulario → landing memoria-calculo",
  "nota": "⚠ El recurso está publicado pero su CTA espera revisión académica. No se sube a "
          "pauta antes de eso: es el único que puede terminar dentro de un documento firmado.",
  "guion": [
   ("0:00-0:05", "Primer plano.", "Te devolvieron la memoria y no era el cálculo.", "NO ERA EL **CÁLCULO**"),
   ("0:05-0:13", "Pantalla: la estructura de secciones desplegándose.", "Se devuelve porque el revisor no puede comprobar que esté bien. Doce secciones, en orden, y los seis errores por los que vuelve a tu escritorio.", "12 SECCIONES · 6 **DEVOLUCIONES**"),
   ("0:13-0:20", "Pantalla: la plantilla de Word y la hoja de Excel.", "Con la plantilla en Word montada y la hoja de verificaciones en Excel. Para no armarla nunca más desde cero.", "PLANTILLA **EDITABLE**"),
   ("0:20-0:25", "Cierre.", "Gratis. El enlace está aquí abajo.", "GRATIS · ACCESO **INMEDIATO**")]},

 {"id": "pauta-dynamo", "recurso": "Pack starter de Dynamo", "palabra": "DYNAMO",
  "estado": "BLOQUEADO — no sale hasta correr los 5 scripts en Revit", "duracion": "20-25 s",
  "destino": "Formulario → landing pack-dynamo",
  "nota": "⚠ Los scripts están escritos y verificados en sintaxis y API, pero nadie los ha "
          "visto ejecutarse. No se promete en pauta lo que no se ha corrido.",
  "guion": [
   ("0:00-0:05", "Primer plano.", "Abriste Dynamo una vez, no supiste por dónde seguir, y lo cerraste.", "LO ABRISTE Y LO **CERRASTE**"),
   ("0:05-0:12", "Screen-record: pegando un script en un nodo de Python y ejecutándolo.", "La automatización en BIM no se atasca por falta de ideas. Se atasca en el primer script.", "SE ATASCA EN EL **PRIMERO**"),
   ("0:12-0:20", "Pantalla: los cinco scripts, tres marcados «solo lee».", "Aquí van cinco, comentados por dentro para que los cambies. Y tres de ellos ni siquiera tocan tu modelo: puedes correrlos hoy en un archivo vivo.", "TRES **SOLO LEEN**"),
   ("0:20-0:25", "Cierre.", "Gratis. El enlace está aquí abajo.", "GRATIS · ACCESO **INMEDIATO**")]},

 {"id": "pauta-acero-tutor", "recurso": "Especialización en Acero · $225 con tutor de IA", "palabra": "—",
  "estado": "BLOQUEADO — hasta que el tutor esté montado en los 4 cursos", "duracion": "25-30 s",
  "destino": "Formulario → landing de la Especialización",
  "nota": "Recoge el antiguo reel-tutor, que era bueno pero estaba colocado como pieza de "
          "feed. Funciona mejor en pauta: el tutor es la razón del precio nuevo, y eso es "
          "argumento de venta, no contenido de valor. ⚠ NO se graba ni se sube hasta que el "
          "tutor esté en la portada de los CUATRO cursos: si un alumno paga $225 y no lo "
          "encuentra, prometimos de más y ya cobrado.",
  "guion": [
   ("0:00-0:06", "Primer plano.", "Once de la noche, estudiando, y te trabas. ¿A quién le preguntas?", "¿A QUIÉN LE **PREGUNTAS**?"),
   ("0:06-0:15", "Screen-record: preguntándole al tutor y viendo la respuesta con la sesión y el minuto.", "Ahora la especialización te contesta. Responde con las clases del curso y te dice en qué sesión y en qué minuto está la respuesta.", "TE DICE SESIÓN Y **MINUTO**"),
   ("0:15-0:23", "Pantalla: el tutor diciendo que algo no está en el material.", "Y cuando algo no está en el material, te lo dice y te manda a la asesoría. No se lo inventa.", "CUANDO NO SABE, LO **DICE**"),
   ("0:23-0:30", "Cierre a cámara.", "Está incluido en la Especialización en Acero. El enlace está aquí abajo.", "**INCLUIDO** EN LA ESPECIALIZACIÓN")]},
]

BASE_FEED = ("Estilo Design Modeling Academy: fondo azul marino #0E2438, acento ámbar #E8A04A, "
             "texto blanco, tipografía sans muy gruesa, estética técnica de ingeniería limpia "
             "(referencia Autodesk Revit), sin fotos de stock genéricas, sin ciencia ficción. "
             "Firma abajo a la izquierda «DG · @design_modeling_dg». "
             "NO escribas texto dentro de la imagen salvo donde se indique — el texto lo monta diseño.")

FEED_PROMPTS = {
 "ago-3-senales-bim-ia": ("CARRUSEL · 6 slides · 1080x1350 px (4:5)",
   "Portada: tres iconos grandes en columna sobre azul marino — un reloj con flecha circular, dos modelos "
   "superpuestos con un choque en ámbar, y dos barras de tiempo desiguales. Slides interiores: un icono por "
   "slide, número 01/02/03 gigante en ámbar a la izquierda, espacio limpio a la derecha para el texto. "
   "Slide de cierre: fondo ámbar invertido con espacio central limpio. " + BASE_FEED),
 "sep-dato-cuantia-minima": ("POST PLANO · 1 imagen · 1080x1350 px (4:5)",
   "Estilo pizarra técnica: fondo azul marino, trazo blanco tipo tiza. Sección transversal de una columna "
   "cuadrada de 30x30 dibujada técnicamente con 4 varillas en las esquinas y cotas limpias. A la derecha, "
   "espacio para el cálculo escrito paso a paso. Una marca de verificación verde y una de advertencia ámbar. "
   "El dibujo ocupa el 70% del lienzo y debe leerse en un teléfono. " + BASE_FEED),
 "ago-navisworks-coordinacion": ("CARRUSEL · 7 slides · 1080x1350 px (4:5)",
   "Portada: tres modelos superpuestos en capas separadas verticalmente (arquitectura, estructura, "
   "instalaciones), cada capa en un tono distinto, con una interferencia marcada en ámbar. Interiores: "
   "un paso del flujo de coordinación por slide, con diagramas de línea fina. " + BASE_FEED),
 "ago-errores-modelar-revit": ("CARRUSEL · 8 slides · 1080x1350 px (4:5)",
   "Portada: modelo 3D con varias zonas marcadas con círculos ámbar de error. Interiores: cada slide muestra "
   "UN error a la izquierda (en rojo apagado) y su corrección a la derecha (en verde), formato antes/después "
   "muy legible. " + BASE_FEED),
 "sep-carrusel-4-puertas": ("CARRUSEL · 8 slides · 1080x1350 px (4:5)",
   "Portada: cuatro puertas arquitectónicas en fila sobre suelo de retícula en perspectiva, una iluminada en "
   "ámbar. Slides 2-5: una puerta por slide, con su icono encima (checklist, cubos ensamblándose, gráfica con "
   "signo de dólar, cerebro-circuito) y la frase del profesional entre comillas grandes. Slide 6: las cuatro "
   "puertas conectadas por una flecha que termina en un birrete. Cierre: fondo ámbar invertido. " + BASE_FEED),
 "sep-acero-agente-ia": ("CARRUSEL · 6 slides · 1080x1350 px (4:5)",
   "Motivo: burbujas de chat de interfaz limpia sobre azul marino. Portada: una burbuja con una pregunta "
   "técnica a medio escribir y un cursor. Slide 3: usar la CAPTURA REAL del tutor respondiendo, nunca una "
   "recreación. Slide 4: split con «chatbot genérico» tachado y «tutor del curso» en ámbar. " + BASE_FEED),
 "post-varilla": ("POST PLANO · 1 imagen · 1080x1350 px (4:5)",
   "Estilo pizarra técnica sobre azul marino: varillas de acero corrugado vistas en sección y en perspectiva, "
   "con la fórmula del peso esquematizada en grande al centro y espacio para el cálculo debajo. Una varilla "
   "destacada en ámbar. " + BASE_FEED),
}
