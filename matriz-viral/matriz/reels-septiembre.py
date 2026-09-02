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
 {"id": "reel-valor6", "fecha": "Miércoles 9", "titulo": "Revit me arrojó un error y ChatGPT me ahorró 2 horas",
  "estado": "YA EDITADO — no hay que grabarlo",
  "duracion": "30 s",
  "cta": "GUÍA (⚠ confirmar palabra y que el recurso exista)",
  "nota": "El video está montado con el pipeline nuevo: silencios cortados, subtítulos, "
          "b-roll del comercial Revit+IA y fondo blueprint en los tramos a cámara. "
          "Lo único pendiente es confirmar la palabra clave del CTA antes de publicar.",
  "guion": [
   ("0:00-0:03", "Plano medio a cámara, fondo blueprint de Revit.", "Revit me arrojó un error, pero ChatGPT me ahorró dos horas de trabajo en buscar la solución.", "REVIT ME ARROJÓ UN **ERROR**"),
   ("0:03-0:09", "Captura de pantalla real del error en Revit.", "Me salió este error en Revit y, en vez de buscar en foros…", "ME SALIÓ ESTE ERROR EN **REVIT**"),
   ("0:09-0:16", "Screen-record: pegando el error en ChatGPT y escribiendo el contexto.", "…lo que hice es pegarlo en ChatGPT, darle un contexto para que me pueda dar la solución.", "ES PEGARLO EN **CHATGPT**"),
   ("0:16-0:20", "B-roll del modelo BIM resolviéndose.", "Una solución que me ahorra dos horas de trabajo.", "**2 HORAS** DE TRABAJO"),
   ("0:20-0:27", "Vuelve a cámara, fondo blueprint.", "Ojo: es importante que valides todo lo que hagas con la IA. Por eso, si te interesa, comenta GUÍA y te enseño cómo usarla.", "VALIDA TODO CON LA **IA**"),
   ("0:27-0:30", "Placa final con el logo DMA.", "—", "—")]},

 {"id": "reel-sobredimensionar", "fecha": "Miércoles 16", "titulo": "Sobredimensionar no es ir por el lado seguro",
  "estado": "POR GRABAR",
  "duracion": "35-40 s",
  "cta": "ACERO → las 5 verificaciones (recurso ya existe)",
  "nota": "Continuación del post #1 de la historia de la cuenta (14.334 vistas, 107 comentarios). "
          "El tema está validado: se repite la fórmula en video. Tono directo, sin agresividad — "
          "incomoda la práctica, no a la persona.",
  "guion": [
   ("0:00-0:04", "Primer plano, mirada directa a cámara. Sin intro.", "Sobredimensionar no te hace más seguro. Te hace más caro.", "SOBREDIMENSIONAR NO ES IR POR EL **LADO SEGURO**"),
   ("0:04-0:10", "Plano medio, gesticulando.", "Y lo peor: le estás trasladando tu inseguridad al presupuesto de tu cliente.", "LE TRASLADAS TU INSEGURIDAD AL **PRESUPUESTO**"),
   ("0:10-0:18", "Pantalla: dos secciones de viga comparadas.", "Primera señal de que una viga está sobrada: la eliges por costumbre, no por la verificación. Si siempre usas el mismo perfil «por si acaso», ahí está.", "SEÑAL 1: LA ELIGES POR **COSTUMBRE**"),
   ("0:18-0:26", "Pantalla: modelo con deflexión exagerada.", "Segunda: cumples resistencia con muchísimo margen pero nunca revisaste deflexión. Estás gastando acero en el criterio equivocado.", "SEÑAL 2: NUNCA REVISASTE **DEFLEXIÓN**"),
   ("0:26-0:34", "Vuelve a cámara.", "Y la tercera, la que más caro sale: revisas las conexiones al final. El nudo manda, y si lo dejas para el final, rediseñas todo.", "SEÑAL 3: EL **NUDO** VA AL FINAL"),
   ("0:34-0:40", "Cierre a cámara.", "Yo uso cinco verificaciones antes de firmar cualquier cosa. Comenta ACERO y te las paso, son gratis.", "COMENTA **ACERO**")]},

 {"id": "reel-coordinacion", "fecha": "Viernes 18", "titulo": "El choque que se paga dos veces",
  "estado": "POR GRABAR",
  "duracion": "30-35 s",
  "cta": "BIM → conversación hacia el módulo BIM Coordination",
  "nota": "Reemplaza a la pieza de «paquete Autodesk», que era venta blanda sin gancho. "
          "Este ángulo — el costo de detectar tarde — es el mismo que valida el módulo 2 "
          "de la nueva arquitectura.",
  "guion": [
   ("0:00-0:04", "A cámara, directo.", "Una interferencia detectada en el modelo cuesta una tarde. La misma, detectada en obra, cuesta miles.", "EN EL MODELO: UNA TARDE. EN OBRA: **MILES**"),
   ("0:04-0:12", "Screen-record: modelo 3D con dos disciplinas superpuestas.", "Esto es un ducto pasando por donde va una viga. En pantalla lo ves en dos segundos.", "AQUÍ SE VE EN **2 SEGUNDOS**"),
   ("0:12-0:20", "B-roll: foto/vídeo de obra.", "En obra lo ves cuando ya está montado. Y ahí no hay software: hay que romper, reprogramar y volver a pedir material.", "EN OBRA: ROMPER, REPROGRAMAR, **VOLVER A PEDIR**"),
   ("0:20-0:28", "Screen-record: detección de interferencias corriendo.", "Coordinar no es abrir los modelos juntos y mirar. Es tener un flujo: reglas, prioridades y un responsable por disciplina.", "COORDINAR ES UN **FLUJO**, NO UNA MIRADA"),
   ("0:28-0:35", "A cámara, cierre.", "Si en tu oficina los choques aparecen en obra, el problema no es el software. Comenta BIM y te cuento por dónde se arregla.", "COMENTA **BIM**")]},

 {"id": "reel-espejo", "fecha": "Viernes 25", "titulo": "El salto que más cuesta",
  "estado": "POR GRABAR",
  "duracion": "30 s",
  "cta": "RUTA (⚠ requiere disparador) o NIVEL como reemplazo",
  "nota": "La versión en video del carrusel de las 4 puertas. Tono personal y calmado, "
          "sin energía de vendedor: es una observación, no una arenga. Se puede grabar "
          "en una sola toma.",
  "guion": [
   ("0:00-0:05", "Plano medio, tono tranquilo.", "Llevas tres años modelando bien. Y sigues esperando a que alguien te diga qué modelar.", "LLEVAS 3 AÑOS MODELANDO BIEN"),
   ("0:05-0:12", "Gráfico en pantalla: los 4 peldaños.", "El recorrido tiene cuatro etapas: estructurar, coordinar, gestionar y automatizar.", "ESTRUCTURA · COORDINA · GESTIONA · **AUTOMATIZA**"),
   ("0:12-0:20", "Vuelve a cámara.", "Y el salto que más cuesta no es el último. Es el primero: dejar de ejecutar y empezar a decidir.", "EL SALTO MÁS DURO ES DEL **1 AL 2**"),
   ("0:20-0:26", "Gráfico: el peldaño 2 iluminado.", "Ese salto no es de software. Nadie se convierte en coordinador por aprender otro programa.", "NO ES DE **SOFTWARE**"),
   ("0:26-0:30", "Cierre a cámara.", "¿En qué peldaño estás tú? Comenta RUTA y te lo digo con tu caso.", "COMENTA **RUTA**")]},

 {"id": "reel-tutor", "fecha": "Miércoles 30", "titulo": "Tu especialización ahora te contesta",
  "estado": "POR GRABAR — CONDICIONADO al despliegue del tutor",
  "duracion": "35-40 s",
  "cta": "ACERO → temario + cómo funciona el tutor",
  "nota": "⚠ NO se graba ni se publica hasta que el tutor esté desplegado y probado. "
          "Es grabación de pantalla REAL: lo que se ve es lo que hace. Nada de simular "
          "una respuesta que el tutor no dio.",
  "guion": [
   ("0:00-0:05", "A cámara, de noche o luz cálida baja.", "Once de la noche, estudiando, y te trabas. ¿A quién le preguntas?", "11 DE LA NOCHE. ¿A QUIÉN LE **PREGUNTAS**?"),
   ("0:05-0:12", "Screen-record: escribiendo la pregunta en el tutor.", "En la Especialización en Acero, al programa. Le escribo como le escribiría a un profe.", "LE PREGUNTAS AL **PROGRAMA**"),
   ("0:12-0:22", "Screen-record: la respuesta apareciendo, con la cita de la sesión.", "Y me responde con el contenido de MI curso. Fíjate en esto: me dice en qué sesión está explicado, para que vuelva a la clase.", "TE DICE EN QUÉ **SESIÓN** ESTÁ"),
   ("0:22-0:30", "Screen-record: pregunta fuera del temario y su respuesta.", "Y si le pregunto algo que no está en las clases, me lo dice. No inventa. Eso para mí era la condición.", "SI NO ESTÁ, **TE LO DICE**"),
   ("0:30-0:38", "A cámara, cierre.", "Estudias a tu ritmo, pero ya no estudias solo. Comenta ACERO y te mando el temario.", "COMENTA **ACERO**")]},
]

# ── Prompts de imagen de las piezas del FEED ───────────────────────────
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
