# -*- coding: utf-8 -*-
"""Las historias de septiembre, jornada por jornada.

Por que existe este archivo: la seccion de historias de la matriz decia «3-5
frames al dia» y una plantilla por dia de la semana. Eso no se puede ejecutar:
quien publica necesita saber QUE dice cada frame. Aqui esta cada jornada
escrita.

LA SEMANA ES UN ARCO, NO CINCO DIAS SUELTOS (revision del 11-sep)
-----------------------------------------------------------------
Hasta ahora cada dia se abria y se cerraba solo, y los cuatro frames eran
siempre relleno → valor → interaccion → venta. Funciona, pero no da ninguna
razon para volver mañana, y pedia una venta cada dia de los veinte.

Desde la semana 2 cada semana cuenta UNA historia, con el caso real de
Gabriel detras: una vivienda de dos pisos de hormigon armado, con
estructuras, arquitectura e instalaciones. Cada dia tiene un papel:

  ABRE EL BUCLE (lunes)    un hecho con numero y una promesa a fecha fija.
  LA PRUEBA (martes)       el material que demuestra lo de ayer.
  LA OBJECIÓN (miercoles)  la encuesta pregunta de quien es la culpa; lo que
                           contesten es el contenido del jueves.
  EL PAGO (jueves)         se cumple lo prometido el lunes, y ahi -solo ahi-
                           aparece la venta.
  EL CIERRE (viernes)      se remata y se suelta el recurso de la semana.

Dentro del dia siguen los cuatro roles, con uno nuevo: RECURSO, para cuando
lo que se pide es la palabra de un lead magnet y no una venta.

LOS FONDOS: TRES TIPOS Y UNA PROPORCION
---------------------------------------
  REAL · camara    ~40%  Gabriel, la obra, la memoria impresa, las varillas.
  REAL · pantalla  ~35%  Revit, el correo del revisor, el chat, el tutor.
  GENERADA         ~25%  solo lo que no se puede fotografiar.

La regla que importa: el mensaje principal de la semana NUNCA va sobre una
imagen generada. Va sobre material real, porque es lo que lo hace creible.
En los frames REAL el campo `prompt` no es un prompt: es la indicacion de
que hay que grabar.

CORRECCION DEL 25-SEP: el «caso real de Gabriel» (la vivienda de dos pisos,
la memoria devuelta, el correo del revisor) nunca se confirmo y no existe.
Las semanas 2 y 3 ya se publicaron asi; desde el viernes 25 las historias
vuelven al formato de agosto: cada dia cuelga de la pieza de feed de ese
dia y del recurso que pide, con sticker que abre un DM o lleva al recurso, y
solo con material que existe. No se vuelve a escribir un caso que no este
confirmado por escrito.

LOS NUMEROS ENTRE [] LOS CONFIRMA GABRIEL antes de grabar. La estructura
esta fija; las cifras no se inventan.

Reglas que se respetan en todas: nunca precio ni «inscribete» en historia
(el objetivo es que escriban), maximo 5 frames, y el primer frame no explica
nada — frena el dedo.

Todas las historias son 1080x1920 (9:16).
"""

MEDIDA = "1080x1920 px (9:16 vertical)"

# Estilo comun que se pega al final de CADA prompt de imagen de historia.
ESTILO = ("Estilo Design Modeling Academy: fondo azul marino #0E2438, acentos ambar #E8A04A, "
          "geometria blanca y limpia, estetica tecnica de ingenieria tipo Autodesk Revit, "
          "nada de ciencia ficcion. Composicion vertical con el 25% superior e inferior libres "
          "de elementos importantes (los tapa la interfaz de Instagram). Sin texto dentro de la "
          "imagen: el texto se pone con las herramientas de Instagram. " + MEDIDA + ".")

# Lo que hay que grabar. Todo el mes se sostiene con estas tomas: se hacen en
# una sola sesion y sirven para las 16 jornadas. Lo demas son capturas que ya
# existen o imagenes que ya estan generadas en el banco.
GRABACION = {
  "nota": "6 bloques de cámara y 5 grabaciones de pantalla, para 16 jornadas. Sin "
          "esto, la mitad de las historias no se pueden publicar tal como están "
          "escritas.",
  "camara": [
    "Gabriel caminando por la obra de la casa con el plano en la mano — 20 s, sin hablar.",
    "Gabriel en el escritorio, de perfil, mirando el monitor — 15 s.",
    "Gabriel hablando a cámara, plano medio, fondo de oficina — 3 tomas de 15 s.",
    "La memoria de cálculo impresa sobre la mesa: pasar una hoja y cerrarla.",
    "Varillas apiladas en obra, plano corto con luz natural.",
    "El cronómetro del teléfono corriendo sobre el escritorio.",
  ],
  "pantalla": [
    "El modelo de la casa girando despacio en Revit — 8 s.",
    "La losa de la planta alta seleccionada, con su cantidad en propiedades; "
    "y los dos modelos superpuestos encendiendo y apagando uno.",
    "El panel de avisos de Revit abriéndose, con el contador visible, y el scroll por la lista.",
    "El script de Dynamo corriendo de principio a fin, SIN CORTES — es la prueba, no se edita.",
    "El tutor contestando una pregunta real, con la cita de norma visible.",
  ],
  "ojo": "Las capturas de DM y del correo del revisor van con los nombres tapados.",
}

SEMANAS = [
 {"n": 1, "rango": "Lun 7 – Vie 11 de septiembre",
  "hilo": "El error que cuesta plata (ACERO)",
  "porque": "Arranca el mes con lo que mejor funcionó en agosto: el dato de cálculo verificable. "
            "El hilo de la semana lleva del error típico al recurso gratuito de las 5 verificaciones.",
  "dias": [
   {"dia": "Lunes 7", "titulo": "El arranque: tres señales",
    "historias": [
     {"rol": "RELLENO", "texto": "Lunes. Café, y una pregunta que me hizo un alumno el viernes y no me dejó dormir.",
      "sticker": "Ninguno.",
      "prompt": "Escritorio de ingeniero visto desde arriba al amanecer: taza de café, cuaderno con un croquis de pórtico metálico a mano alzada, lápiz, y la esquina de un teclado. Luz cálida de mañana entrando de lado. " + ESTILO},
     {"rol": "VALOR", "texto": "«¿Por qué mi oficina va tan lenta si todos sabemos Revit?» Porque saber el software no es tener flujo. Hoy publicamos las 3 señales de que tu oficina ya necesita BIM + IA.",
      "sticker": "Ninguno.",
      "prompt": "Diagrama limpio de tres iconos en columna sobre fondo azul marino: un reloj con flecha circular (tareas repetidas), dos modelos superpuestos con un choque marcado en ámbar, y dos barras de tiempo de distinta longitud. Estilo línea fina, muy legible en móvil. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Cuál te pasa a ti?",
      "sticker": "ENCUESTA de 2 opciones: «Repito tareas» / «Choques en obra». A quien vote se le contesta por DM.",
      "prompt": "Split vertical de dos mitades: arriba un profesional repitiendo la misma tarea (tres pantallas iguales en fila), abajo una foto de obra con una interferencia marcada en ámbar. Sin texto. " + ESTILO},
     {"rol": "VENTA", "texto": "Si te pasan las dos, no te falta gente: te falta flujo. Respóndeme BIM y te digo por dónde se empieza.",
      "sticker": "RESPONDER CON PALABRA: «BIM» → lo agarra el bot.",
      "prompt": "Modelo BIM blanco de un edificio pequeño flotando sobre una retícula azul, con líneas de coordinación conectando sus partes en ámbar. Espacio limpio en el centro-bajo para escribir encima. " + ESTILO}]},

   {"dia": "Martes 8", "titulo": "Detrás de cámaras + el error de Revit",
    "historias": [
     {"rol": "RELLENO", "texto": "Hoy grabamos. Así se ve esto por dentro (spoiler: menos glamuroso de lo que parece).",
      "sticker": "Ninguno.",
      "prompt": "Detrás de cámaras de una grabación casera profesional: trípode con teléfono, aro de luz encendido, pantalla de computadora al fondo con un modelo 3D, cables ordenados. Ambiente real de oficina, no de estudio. " + ESTILO},
     {"rol": "VALOR", "texto": "Mañana sale el reel del error de Revit que me costó dos horas… hasta que le pedí ayuda a la IA con el contexto correcto.",
      "sticker": "Ninguno.",
      "prompt": "Primer plano de una pantalla con un cuadro de diálogo de error de software genérico en tonos oscuros, desenfocado al fondo un modelo 3D. Sensación de bloqueo. Sin texto legible en la pantalla. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Cuánto tiempo pierdes al mes buscando soluciones a errores del software?",
      "sticker": "QUIZ de 3 opciones: «menos de 2 h» / «2 a 5 h» / «más de 5 h». Los que marquen más de 5 reciben DM.",
      "prompt": "Reloj de arena estilizado sobre fondo azul marino, con la arena cayendo convertida en pequeños iconos de engranaje y código. Minimalista, línea fina. " + ESTILO},
     {"rol": "VENTA", "texto": "Mañana te muestro exactamente cómo se lo pregunté. Si no quieres esperar, respóndeme CHATGPT.",
      "sticker": "RESPONDER CON PALABRA: «CHATGPT».",
      "prompt": "Burbuja de chat de IA sobre fondo azul, con una respuesta técnica esquematizada en líneas (sin texto real), y un pequeño ícono de Revit-like en la esquina. " + ESTILO}]},

   {"dia": "Miércoles 9", "titulo": "El reel del día: Revit + ChatGPT",
    "historias": [
     {"rol": "RELLENO", "texto": "Ya está arriba. 30 segundos, y creo que es de lo más útil que hemos publicado.",
      "sticker": "Ninguno.",
      "prompt": "Teléfono en mano mostrando un reel en reproducción (pantalla vertical con un modelo BIM), fondo de oficina desenfocado. " + ESTILO},
     {"rol": "VALOR", "texto": "La clave no fue «preguntarle a la IA». Fue darle el CONTEXTO: qué versión, qué estaba haciendo, y el mensaje de error completo.",
      "sticker": "Ninguno.",
      "prompt": "Esquema de tres cajas conectadas por flechas ámbar sobre azul marino: una caja con un ícono de documento, otra con un ícono de engranaje, otra con un ícono de check. Representa contexto → proceso → solución. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Le pides ayuda a la IA en tus proyectos?",
      "sticker": "ENCUESTA: «Todos los días» / «No me fío». A los que no se fían se les contesta con el criterio de validación.",
      "prompt": "Balanza de dos platos sobre fondo azul: en un plato un chip/circuito, en el otro un casco de ingeniero. Equilibrada. Línea fina, elegante. " + ESTILO},
     {"rol": "VENTA", "texto": "Ojo: la IA acelera, el criterio es tuyo. Eso es justo lo que enseñamos en el módulo BIM + IA. Respóndeme NIVEL y el test te dice si ese módulo es el tuyo.",
      "sticker": "RESPONDER CON PALABRA: «NIVEL».",
      "prompt": "Cuatro puertas alineadas en perspectiva sobre suelo de retícula azul; la cuarta está iluminada en ámbar. Estilo arquitectónico limpio. " + ESTILO}]},

   {"dia": "Jueves 10", "titulo": "VENTA · Cupos de ACERO",
    "historias": [
     {"rol": "RELLENO", "texto": "Pregunta honesta que me llegó ayer: «¿esto sirve si ya llevo años trabajando?»",
      "sticker": "Ninguno.",
      "prompt": "Manos de un profesional con experiencia sobre un plano estructural impreso, con un escalímetro al lado. Detalle cálido, cercano. " + ESTILO},
     {"rol": "VALOR", "texto": "Sirve más, de hecho. Los que llevan años saben dónde les duele — y vienen a cerrar esa brecha concreta, no a aprender de cero.",
      "sticker": "Ninguno.",
      "prompt": "Dos siluetas de perfil frente a un modelo estructural: una mira una pieza suelta, la otra mira el conjunto completo. Representa mirada de detalle vs. mirada de sistema. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Cuál es tu punto flojo hoy?",
      "sticker": "CAJA DE PREGUNTAS: «¿Qué parte del diseño en acero te frena?». Las mejores se contestan mañana.",
      "prompt": "Estructura metálica en isométrico con una de sus conexiones destacada en ámbar y el resto en blanco tenue. " + ESTILO},
     {"rol": "VENTA", "texto": "Abrimos cohorte de la Especialización en Acero. Quedan [CUPOS REALES]. Respóndeme ACERO y te mando el temario.",
      "sticker": "CUENTA REGRESIVA al cierre + RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Perfil de acero tipo I en primer plano con profundidad de campo, sobre fondo azul marino con retícula técnica tenue. Iluminación de estudio. " + ESTILO}]},

   {"dia": "Viernes 11", "titulo": "Cierra la guía y abre el caso",
    "papel": "CIERRA Y ABRE EL BUCLE",
    "historias": [
     {"rol": "RELLENO", "texto": "[446] personas abrieron la guía esta semana.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar la pantalla de la analítica con el número de aperturas, sin retocar. Que se vea que es un panel de verdad."},
     {"rol": "VALOR", "texto": "La número 06 fue la que más me escribieron: elementos duplicados.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el schedule de Revit bajando por las filas repetidas. Marcar dos o tres en ámbar al editar."},
     {"rol": "INTERACCIÓN", "texto": "¿Te ha pasado que el presupuesto no cuadra con el modelo?",
      "sticker": "ENCUESTA de 2 opciones: «Sí, más de una vez» / «Nunca lo he revisado».",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel de espaldas frente al monitor, medio cuerpo, luz lateral. 10 segundos, sin hablar."},
     {"rol": "CIERRE", "texto": "El lunes les cuento lo que ese error costó en una casa de dos pisos.",
      "sticker": "CUENTA REGRESIVA al lunes 9:00.",
      "fondo": "GENERADA",
      "prompt": "Perfil de acero tipo I en primer plano con profundidad de campo, sobre fondo azul marino con retícula técnica tenue. Iluminación de estudio. " + ESTILO}]},
  ]},

 {"n": 2, "rango": "Lun 14 – Vie 18 de septiembre",
  "hilo": "Dos modelos, la misma losa",
  "porque": "El caso real de Gabriel: una vivienda de dos pisos de hormigón armado con estructuras, "
            "arquitectura e instalaciones. Tres disciplinas en un proyecto pequeño es justo donde se "
            "ven los cruces, y es el tamaño de proyecto que la audiencia reconoce como suyo. El lunes "
            "se promete una cifra y el jueves se paga: ese es el bucle.",
  "dias": [
   {"dia": "Lunes 14", "titulo": "El presupuesto que no cuadraba",
    "papel": "ABRE EL BUCLE",
    "historias": [
     {"rol": "RELLENO", "texto": "Una vivienda de dos pisos. Nada complicado: estructuras, arquitectura e instalaciones.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel en la obra de la casa, con el plano impreso en la mano. 20 segundos caminando, sin hablar."},
     {"rol": "VALOR", "texto": "El presupuesto de hormigón salió [$2.400] por encima. Y nadie calculó mal.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el modelo de la casa girando despacio en Revit, 8 segundos."},
     {"rol": "INTERACCIÓN", "texto": "¿Te ha pasado que el presupuesto no cuadra con el modelo?",
      "sticker": "ENCUESTA: «Sí, más de una vez» / «Nunca lo he revisado». A quien vote se le contesta por DM.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel en el escritorio, de perfil, mirando el monitor."},
     {"rol": "CIERRE", "texto": "El jueves les enseño dónde estaban esos [$2.400].",
      "sticker": "CUENTA REGRESIVA al jueves.",
      "fondo": "GENERADA",
      "prompt": "Dos siluetas de perfil frente a un modelo estructural: una mira una pieza suelta, la otra el conjunto completo. " + ESTILO}]},

   {"dia": "Martes 15", "titulo": "La prueba: la losa contada dos veces",
    "papel": "LA PRUEBA",
    "historias": [
     {"rol": "RELLENO", "texto": "Me pidieron la prueba. Aquí está, sin editar.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel encogiendose de hombros frente al monitor, plano corto."},
     {"rol": "VALOR", "texto": "La losa de la planta alta: [18 m³] de hormigón.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar la losa seleccionada en Revit con su cantidad visible en las propiedades."},
     {"rol": "VALOR", "texto": "Estaba en el modelo de estructuras. Y otra vez en el de arquitectura.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar los dos modelos superpuestos, encendiendo y apagando uno para que se vea la repetición."},
     {"rol": "INTERACCIÓN", "texto": "¿Qué duda tienes de esto? Mañana contesto en cámara.",
      "sticker": "CAJA DE PREGUNTAS. Solo se pone si mañana se contesta de verdad.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel mirando a cámara, plano medio, fondo de oficina desenfocado."}]},

   {"dia": "Miércoles 16", "titulo": "¿De quién es la culpa?",
    "papel": "LA OBJECIÓN",
    "historias": [
     {"rol": "RELLENO", "texto": "Ayer preguntaron lo mismo tres veces: ¿de quién es la culpa?",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel en el escritorio leyendo los mensajes en el teléfono."},
     {"rol": "VALOR", "texto": "Del de estructuras, dicen unos. Del de arquitectura, dicen otros.",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Dos siluetas de perfil frente a un modelo estructural: una mira una pieza suelta, la otra el conjunto completo. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "Yo creo que de ninguno de los dos. Voten.",
      "sticker": "ENCUESTA: «Del de estructuras» / «Del de arquitectura». El resultado se usa mañana.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el modelo federado con las dos disciplinas en colores distintos."},
     {"rol": "CIERRE", "texto": "Hoy salió el reel completo: tus planos están bien, tu presupuesto está mal.",
      "sticker": "ENLACE al reel.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del reel publicado en el perfil."}]},

   {"dia": "Jueves 17", "titulo": "VENTA · Dónde estaban los $2.400",
    "papel": "EL PAGO DEL BUCLE",
    "historias": [
     {"rol": "RELLENO", "texto": "Prometí enseñarles dónde estaban los [$2.400]. Aquí está.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el schedule y el presupuesto lado a lado, señalando la fila que se repite."},
     {"rol": "VALOR", "texto": "Ganó «del de arquitectura» con [61%]. Es la respuesta cómoda.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del resultado de la encuesta de ayer, tal cual."},
     {"rol": "VALOR", "texto": "La verdad: nadie revisó el cruce. En el proceso no existe ese paso.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel en la obra, plano medio, hablando a cámara."},
     {"rol": "VENTA", "texto": "En una casa son [$2.400]. En lo que haces tú, multiplícalo. Respóndeme ACERO y te mando el temario.",
      "sticker": "RESPONDER CON PALABRA: «ACERO» → lo agarra el bot.",
      "fondo": "GENERADA",
      "prompt": "Perfil de acero tipo I en primer plano con profundidad de campo, sobre fondo azul marino con retícula técnica tenue. Iluminación de estudio. " + ESTILO}]},

   {"dia": "Viernes 18", "titulo": "Los avisos que nadie lee",
    "papel": "EL CIERRE",
    "historias": [
     {"rol": "RELLENO", "texto": "Abrí el modelo de la casa y tenía [127] avisos sin leer.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el panel de avisos de Revit abriendose, con el contador visible."},
     {"rol": "VALOR", "texto": "Ninguno impedía trabajar. Por eso llevaban meses ahí.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el scroll por la lista de avisos, despacio."},
     {"rol": "INTERACCIÓN", "texto": "¿Cuántos tiene tu modelo ahora mismo? Ábrelo y mira.",
      "sticker": "ENCUESTA: «Menos de 50» / «Prefiero no saber».",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel señalando la pantalla, plano corto."},
     {"rol": "CIERRE", "texto": "Hoy sale el reel con los avisos que sí importan.",
      "sticker": "ENLACE al reel.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del reel publicado."}]},
  ]},

 {"n": 3, "rango": "Lun 21 – Vie 25 de septiembre",
  "hilo": "34 ventanas, una por una",
  "porque": "Sigue la misma casa. El lunes se cronometra una tarea real y se promete hacerla en "
            "segundos; el martes se paga con el Pack de Dynamo. El jueves el hilo sube de nivel: "
            "de automatizar una tarea a las cuatro etapas del Master.",
  "dias": [
   {"dia": "Lunes 21", "titulo": "Le puse cronómetro",
    "papel": "ABRE EL BUCLE",
    "historias": [
     {"rol": "RELLENO", "texto": "Le puse cronómetro a lo último que hice en la casa de dos pisos.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "El cronómetro del teléfono corriendo sobre el escritorio, junto al teclado."},
     {"rol": "VALOR", "texto": "Numerar [34] puertas y ventanas. Una por una. [41] minutos.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar acelerado el renombrado manual, que se vea la repetición."},
     {"rol": "INTERACCIÓN", "texto": "¿Cuánto tardas tú en eso?",
      "sticker": "ENCUESTA: «Menos de 10 min» / «Prefiero no contarlo».",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel de perfil frente al monitor."},
     {"rol": "CIERRE", "texto": "Mañana lo hago delante de ustedes en [40] segundos.",
      "sticker": "CUENTA REGRESIVA al martes.",
      "fondo": "GENERADA",
      "prompt": "Reloj de arena técnico sobre fondo azul marino, con la arena cayendo en ámbar. " + ESTILO}]},

   {"dia": "Martes 22", "titulo": "40 segundos, sin tocar el teclado",
    "papel": "LA PRUEBA · lanzamiento del Pack de Dynamo",
    "historias": [
     {"rol": "RELLENO", "texto": "[40] segundos. Sin tocar el teclado.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el script corriendo de principio a fin, sin cortes. Es la prueba: no se edita."},
     {"rol": "VALOR", "texto": "Es un script de Dynamo. Yo no sé programar y lo uso igual.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel encogiendose de hombros, medio sonriendo."},
     {"rol": "VALOR", "texto": "Son cinco. Los regalo hoy.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "La carpeta con los cinco archivos, vista de explorador."},
     {"rol": "RECURSO", "texto": "Responde DYNAMO y te los mando.",
      "sticker": "RESPONDER CON PALABRA: «DYNAMO».",
      "fondo": "GENERADA",
      "prompt": "Cinco piezas metálicas idénticas alineándose solas sobre una retícula azul, la última encajando en ámbar. " + ESTILO}]},

   {"dia": "Miércoles 23", "titulo": "«Eso es para programadores»",
    "papel": "LA OBJECIÓN",
    "historias": [
     {"rol": "RELLENO", "texto": "Ayer me escribieron tres veces lo mismo: «eso es para programadores».",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Capturas de los tres DM, con los nombres tapados."},
     {"rol": "VALOR", "texto": "Abrir un script y darle play no es programar. Es abrir un archivo.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el doble clic en el archivo y el play, cuatro segundos."},
     {"rol": "INTERACCIÓN", "texto": "¿Has abierto Dynamo alguna vez?",
      "sticker": "QUIZ de 3: «Nunca» / «Lo abrí y me perdí» / «Lo uso». A quien marque «me perdí» se le contesta.",
      "fondo": "REAL · pantalla",
      "prompt": "La interfaz de Dynamo abierta, con un script sencillo a la vista."},
     {"rol": "RECURSO", "texto": "Si marcaste «me perdí»: el pack trae la guía de instalación. Responde DYNAMO.",
      "sticker": "RESPONDER CON PALABRA: «DYNAMO».",
      "fondo": "REAL · pantalla",
      "prompt": "La primera página de la guía de instalación en pantalla."}]},

   {"dia": "Jueves 24", "titulo": "VENTA · El espejo: las cuatro puertas",
    "papel": "EL PAGO DEL BUCLE",
    "historias": [
     {"rol": "RELLENO", "texto": "Los que automatizan no son más inteligentes. Van un nivel más arriba.",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Cuatro puertas alineadas en perspectiva sobre suelo de retícula azul; la cuarta está iluminada en ámbar. " + ESTILO},
     {"rol": "VALOR", "texto": "Modelador. Coordinador. BIM Manager. Especialista BIM + IA.",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Las mismas cuatro puertas, con la cuarta encendida y las tres primeras en blanco tenue. " + ESTILO},
     {"rol": "VALOR", "texto": "La mayoría se queda en la primera porque nadie le dijo que había cuatro.",
      "sticker": "Ninguno.",
      "fondo": "REAL · cámara",
      "prompt": "Gabriel hablando a cámara, plano medio."},
     {"rol": "VENTA", "texto": "Hay un test de 20 preguntas que te dice en cuál estás. Gratis, 5 minutos. Responde NIVEL.",
      "sticker": "RESPONDER CON PALABRA: «NIVEL».",
      "fondo": "REAL · pantalla",
      "prompt": "El test abierto en el teléfono, con la barra de progreso a medias."}]},

   # REESCRITA el 25-sep (pedido de Dayana). La version anterior de este
   # viernes y de toda la semana 4 contaba «la memoria que me devolvieron» de
   # una vivienda de dos pisos: ese caso NUNCA se confirmo, y las historias
   # pedian grabar una memoria impresa y un correo de revisor que no existen.
   # Ahora cada dia cuelga de la pieza de feed de ese dia y del recurso que la
   # pieza pide, como en agosto, y solo usa material que ya existe: la guia
   # publicada, la plantilla Word, la NEC-SE-DS, el tutor y los posts del dia.
   {"dia": "Viernes 25", "titulo": "«Según la norma» no es una cita",
    "papel": "PIEZA DEL DÍA · reel-cita-norma → MEMORIA",
    "historias": [
     {"rol": "RELLENO", "texto": "¿Cuántas veces has escrito «según la norma» en una memoria?",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Hoja de documento técnico en primer plano, en perspectiva leve, con un renglón resaltado en ámbar y el resto del texto ilegible a propósito. " + ESTILO},
     {"rol": "VALOR", "texto": "Así lo devuelve el revisor: «Se aplica la normativa sismorresistente vigente».\nAsí lo aprueba: «NEC-SE-DS, Peligro sísmico y diseño sismorresistente, versión 2015».",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la guía publicada (memoria-calculo/guia.html), bloque «Devolución 2 · Normativa citada sin versión», con las dos cajas «Como se ve mal» y «Como se ve corregido» visibles."},
     {"rol": "INTERACCIÓN", "texto": "¿Tú pones la versión de la norma?",
      "sticker": "ENCUESTA: «Siempre» / «Casi nunca». A quien marque «Casi nunca» se le escribe por DM con el enlace de la guía.",
      "fondo": "GENERADA",
      "prompt": "Dos columnas limpias sobre azul marino: a la izquierda una etiqueta de documento sin fecha, a la derecha la misma etiqueta con un sello de año en ámbar. Línea fina. " + ESTILO},
     {"rol": "RECURSO", "texto": "Es uno de los 6 motivos por los que devuelven una memoria. Los 6, con el ejemplo corregido y la plantilla en Word, están en la guía gratis. Respóndeme MEMORIA y te la mando.",
      "sticker": "RESPONDER CON PALABRA: «MEMORIA» → la contesta el workflow de GHL (montado 25-sep). Opcional, de respaldo: ENLACE a funnel.dgdesignmodeling.com/acceso-gratis-memoria-calculo-form («Guía gratis»).",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la guía: la lista «Las seis devoluciones» completa."}]},
  ]},

 {"n": 4, "rango": "Lun 28 de septiembre – Vie 2 de octubre",
  "hilo": "La memoria de cálculo, con la guía real (y el tutor del Acero)",
  "porque": "Reescrita el 25-sep. Cada día sale de la pieza de feed del día y del recurso que pide. "
            "Todo lo que se muestra existe: la guía de memoria de cálculo publicada, su plantilla Word, "
            "la NEC-SE-DS, el tutor de IA del Acero y los posts del día. Nada de casos sin confirmar.",
  "dias": [
   {"dia": "Lunes 28", "titulo": "El tutor de IA del Acero, funcionando",
    "papel": "PIEZA DEL DÍA · carrusel sep-acero-agente-ia",
    "historias": [
     {"rol": "RELLENO", "texto": "Estudias de noche, te trabas en una lección y no hay a quién preguntarle.",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Escritorio de noche con la pantalla encendida mostrando un modelo de estructura metálica, lámpara cálida, sin personas. " + ESTILO},
     {"rol": "VALOR", "texto": "Los alumnos del Acero ahora le preguntan al Tutor de IA. Responde con las clases del curso y te dice en qué lección y en qué minuto está.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Grabar el tutor del Acero (burbuja «IA» dentro del curso) respondiendo una pregunta real de conexiones, con la línea de FUENTES (lección y minuto) visible."},
     {"rol": "INTERACCIÓN", "texto": "¿Qué haces cuando te trabas en una clase?",
      "sticker": "ENCUESTA: «Busco en YouTube» / «Espero a preguntar». A todos los que voten se les escribe por DM.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del carrusel del día publicado."},
     {"rol": "VENTA", "texto": "Viene incluido en la Especialización en Acero. Escríbenos y te mandamos el temario.",
      "sticker": "ENLACE al WhatsApp del bot de ventas (el mismo número de la campaña de WhatsApp del Acero). Sin precio en la historia.",
      "fondo": "REAL · pantalla",
      "prompt": "La respuesta del tutor con la captura de la clase debajo."}]},

   {"dia": "Martes 29", "titulo": "Sale la guía de memoria de cálculo",
    "papel": "PIEZA DEL DÍA · reel pauta-memoria (lanzamiento)",
    "historias": [
     {"rol": "RELLENO", "texto": "Te devolvieron la memoria y no era el cálculo.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del reel del día publicado."},
     {"rol": "INTERACCIÓN", "texto": "¿Cuál crees que es el motivo más frecuente de devolución?",
      "sticker": "QUIZ de 3: «Un error de cálculo» / «Norma citada sin versión» / «Falta un plano». La correcta es «Norma citada sin versión».",
      "fondo": "GENERADA",
      "prompt": "Tres tarjetas en columna sobre azul marino, la del medio con borde ámbar. Sin texto. " + ESTILO},
     {"rol": "VALOR", "texto": "Ninguno de los 6 motivos es un error de cálculo. Los 6 son de escritura, y se arreglan releyendo.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la guía: el índice de «Las 12 secciones», bajando despacio."},
     {"rol": "RECURSO", "texto": "Guía + plantilla en Word + Excel de verificaciones. Gratis. Respóndeme MEMORIA y te la mando.",
      "sticker": "RESPONDER CON PALABRA: «MEMORIA» → la contesta el workflow de GHL. Opcional, de respaldo: ENLACE a funnel.dgdesignmodeling.com/acceso-gratis-memoria-calculo-form («Guía gratis»).",
      "fondo": "REAL · pantalla",
      "prompt": "El Word de la plantilla (Plantilla-Memoria-de-Calculo-DMA.docx) abierto, bajando por el índice."}]},

   {"dia": "Miércoles 30", "titulo": "El error que cuesta más caro",
    "papel": "SIN PIEZA DE FEED · valor de la guía + caja de preguntas",
    "historias": [
     {"rol": "RELLENO", "texto": "La estructura no se cae. Y aun así el edificio es inhabitable.",
      "sticker": "Ninguno.",
      "fondo": "GENERADA",
      "prompt": "Losa de entrepiso vista de perfil con una deflexión exagerada marcada con una línea ámbar punteada. Línea fina, técnica. " + ESTILO},
     {"rol": "VALOR", "texto": "Es el motivo de devolución número 5: la memoria verifica resistencia, pero no deflexión, deriva ni vibración.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la guía: «Devolución 5 · Faltan los estados límite de servicio», con el ejemplo mal y corregido."},
     {"rol": "INTERACCIÓN", "texto": "¿Qué parte de la memoria te cuesta más escribir?",
      "sticker": "CAJA DE PREGUNTAS. Las 2 o 3 mejores se contestan el jueves en historias.",
      "fondo": "GENERADA",
      "prompt": "Índice de documento técnico con doce renglones en línea fina y uno resaltado en ámbar. Sin texto legible. " + ESTILO}]},

   {"dia": "Jueves 1 de octubre", "titulo": "Respuestas + la guía una vez más",
    "papel": "PIEZA DEL DÍA · post lm-memoria-calculo-feed",
    "historias": [
     {"rol": "VALOR", "texto": "Respuesta a sus preguntas de ayer (1 frame por pregunta, máximo 2).",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "La pregunta real de la caja de ayer, sin nombre, y debajo la respuesta escrita con la herramienta de texto de Instagram. Si no llegaron preguntas, este frame no se publica."},
     {"rol": "VALOR", "texto": "Hoy en el feed: por qué una memoria no se devuelve por los números.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del post del día publicado."},
     {"rol": "RECURSO", "texto": "Si todavía no tienes la guía, respóndeme MEMORIA y te la mando.",
      "sticker": "RESPONDER CON PALABRA: «MEMORIA» → la contesta el workflow de GHL. Opcional, de respaldo: ENLACE a funnel.dgdesignmodeling.com/acceso-gratis-memoria-calculo-form («Guía gratis»).",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la guía: «Lo que los seis tienen en común»."}]},

   {"dia": "Viernes 2 de octubre", "titulo": "¿Cuánto pesa una varilla Ø12 de 12 m?",
    "papel": "PIEZA DEL DÍA · post del peso de la varilla → ACERO",
    "historias": [
     {"rol": "INTERACCIÓN", "texto": "Sin tabla: ¿cuánto pesa una varilla Ø12 de 12 metros?",
      "sticker": "QUIZ de 3: «8,5 kg» / «10,7 kg» / «13,3 kg». La correcta es 10,7 kg.",
      "fondo": "GENERADA",
      "prompt": "Una varilla corrugada en horizontal con una cota de «12 m» y su sección circular al lado, trazo blanco sobre azul marino. " + ESTILO},
     {"rol": "VALOR", "texto": "Peso (kg/m) = Ø² ÷ 162, con Ø en mm.\nØ12 → 144 ÷ 162 = 0,888 kg/m → × 12 m = 10,7 kg.",
      "sticker": "Ninguno.",
      "fondo": "REAL · pantalla",
      "prompt": "Captura del post del día publicado (la imagen con la fórmula)."},
     {"rol": "RECURSO", "texto": "Es una de las verificaciones rápidas del acero. Las 5 están en la herramienta gratis.",
      "sticker": "ENLACE: funnel.dgdesignmodeling.com/acceso-gratis-verificacion-acero-form («Herramienta gratis»).",
      "fondo": "REAL · pantalla",
      "prompt": "Captura de la herramienta de las 5 verificaciones abierta."}]},
  ]},
]
