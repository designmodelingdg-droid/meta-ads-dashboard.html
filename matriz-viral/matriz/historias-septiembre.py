# -*- coding: utf-8 -*-
"""Las historias de septiembre, jornada por jornada.

Por que existe este archivo: la seccion de historias de la matriz decia «3-5
frames al dia» y una plantilla por dia de la semana. Eso no se puede ejecutar:
quien publica necesita saber QUE dice cada frame. Aqui esta cada jornada
escrita.

Como esta armado cada dia — es un arco, no cuatro piezas sueltas:

  1. RELLENO      abre en humano. No vende nada, gana el derecho a lo demas.
  2. VALOR        el dato o la idea del dia. Es la razon de quedarse.
  3. INTERACCION  sticker que pide algo facil. Lo que responden se contesta
                  por DM, y ahi vive la conversion.
  4. VENTA        cierra pidiendo una PALABRA. Solo eso es automatizable: el
                  bot lo recoge igual que un comentario del feed.

Reglas que se respetan en todas: nunca precio ni «inscribete» en historia
(el objetivo es que escriban), maximo 5 frames, y el primer frame no explica
nada — frena el dedo.

Cada frame trae su PROMPT para generar la imagen en ChatGPT, con la medida.
Todas las historias son 1080x1920 (9:16).
"""

MEDIDA = "1080x1920 px (9:16 vertical)"

# Estilo comun que se pega al final de CADA prompt de imagen de historia.
ESTILO = ("Estilo Design Modeling Academy: fondo azul marino #0E2438, acentos ambar #E8A04A, "
          "geometria blanca y limpia, estetica tecnica de ingenieria tipo Autodesk Revit, "
          "nada de ciencia ficcion. Composicion vertical con el 25% superior e inferior libres "
          "de elementos importantes (los tapa la interfaz de Instagram). Sin texto dentro de la "
          "imagen: el texto se pone con las herramientas de Instagram. " + MEDIDA + ".")

SEMANAS = [
 {"n": 1, "rango": "Lun 7 – Vie 11 de septiembre",
  "hilo": "El error que cuesta plata (ACERO)",
  "porque": "Arranca el mes con lo que mejor funciono en agosto: el dato de calculo verificable. "
            "El hilo de la semana lleva del error tipico al recurso gratuito de las 5 verificaciones.",
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
     {"rol": "VENTA", "texto": "Mañana te muestro exactamente cómo se lo pregunté. Si no quieres esperar, respóndeme GUÍA.",
      "sticker": "RESPONDER CON PALABRA: «GUÍA». ⚠ Solo si el recurso ya existe; si no, cambiar a «GPT».",
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
     {"rol": "VENTA", "texto": "Ojo: la IA acelera, el criterio es tuyo. Eso es justo lo que enseñamos en el módulo BIM + IA. Respóndeme RUTA y te digo si es el tuyo.",
      "sticker": "RESPONDER CON PALABRA: «RUTA». ⚠ Requiere el disparador montado.",
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

   {"dia": "Viernes 11", "titulo": "El dato del mes: la cuantía mínima",
    "historias": [
     {"rol": "RELLENO", "texto": "Respondo las preguntas de ayer. La primera me la hacen mucho.",
      "sticker": "Ninguno.",
      "prompt": "Pantalla de teléfono con varias burbujas de mensajes entrantes (sin texto legible), sobre un escritorio con planos. " + ESTILO},
     {"rol": "VALOR", "texto": "«¿Con qué cuantía arranco una columna?» El código dice 1% del área bruta. En una 30×30 son 9 cm². 4Ø18 cumplen. 4Ø16 NO.",
      "sticker": "Ninguno.",
      "prompt": "Sección transversal de una columna cuadrada de hormigón dibujada técnicamente, con 4 varillas en las esquinas, cotas limpias, sobre fondo azul marino. Estilo pizarra técnica. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Sabías el dato?",
      "sticker": "QUIZ con respuesta correcta: «¿4Ø16 cumplen en una 30×30?» Sí / No. Los que fallan reciben DM con la explicación — es el lead más calificado de la semana.",
      "prompt": "Dos secciones de columna lado a lado, una con marca de verificación verde y otra con marca ámbar de advertencia. Sin texto. " + ESTILO},
     {"rol": "VENTA", "texto": "Revisar esto a mano en cada elemento es lento. Tenemos una herramienta con las 5 verificaciones que usamos nosotros — es gratis. Respóndeme ACERO.",
      "sticker": "RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Lista de cinco casillas de verificación estilizadas sobre fondo azul, todas marcadas en ámbar, junto a la silueta de una viga metálica. " + ESTILO}]},
  ]},

 {"n": 2, "rango": "Lun 14 – Vie 18 de septiembre",
  "hilo": "Coordinar y automatizar (BIM + IA)",
  "porque": "La semana sube un nivel: del cálculo puntual a la coordinación del proyecto. "
            "Prepara el terreno para el carrusel de las 4 puertas de la semana 3.",
  "dias": [
   {"dia": "Lunes 14", "titulo": "Coordinación: el choque que se paga dos veces",
    "historias": [
     {"rol": "RELLENO", "texto": "Historia real de obra (sin nombres): una viga y un ducto que no se hablaban.",
      "sticker": "Ninguno.",
      "prompt": "Foto de obra en construcción, estructura metálica vista desde abajo con instalaciones pasando entre vigas. Luz natural, realista. " + ESTILO},
     {"rol": "VALOR", "texto": "Detectado en el modelo: una tarde de trabajo. Detectado en obra: reprogramar, romper y volver a pedir material.",
      "sticker": "Ninguno.",
      "prompt": "Comparación visual en dos columnas: a la izquierda un modelo 3D con una alerta ámbar pequeña; a la derecha una obra real con una zona demolida. Sin texto. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Cuándo detectas tú las interferencias?",
      "sticker": "ENCUESTA: «En el modelo» / «En obra 😅». A los segundos se les manda el carrusel de hoy por DM.",
      "prompt": "Línea de tiempo horizontal de un proyecto con dos puntos marcados: uno temprano en ámbar, uno tardío en rojo apagado. Minimalista. " + ESTILO},
     {"rol": "VENTA", "texto": "Coordinar disciplinas es un oficio, y se aprende. Respóndeme BIM y te cuento cómo lo enseñamos.",
      "sticker": "RESPONDER CON PALABRA: «BIM».",
      "prompt": "Tres modelos superpuestos en capas separadas (arquitectura, estructura, instalaciones) en explosión vertical, cada capa en un tono distinto. " + ESTILO}]},

   {"dia": "Martes 15", "titulo": "Comunidad y blog",
    "historias": [
     {"rol": "RELLENO", "texto": "Nuestra comunidad de WhatsApp ya está a tope de gente que pregunta cosas buenísimas.",
      "sticker": "Ninguno.",
      "prompt": "Ilustración de red de puntos conectados formando la silueta de un edificio, sobre azul marino, con algunos nodos brillando en ámbar. " + ESTILO},
     {"rol": "VALOR", "texto": "Del blog del sábado: la IA en arquitectura no te quita el trabajo. Te quita las tareas que odias del trabajo.",
      "sticker": "Ninguno.",
      "prompt": "Escritorio dividido: una mitad con papeles y tareas repetitivas apiladas, la otra despejada con una sola maqueta bien resuelta. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Qué tarea te quitarías hoy mismo?",
      "sticker": "CAJA DE PREGUNTAS abierta.",
      "prompt": "Manos apartando una pila de documentos para dejar ver un modelo 3D limpio debajo. Gesto de despejar. " + ESTILO},
     {"rol": "VENTA", "texto": "Si tu respuesta es «documentación» o «cantidades», eso ya se automatiza. Respóndeme IA.",
      "sticker": "RESPONDER CON PALABRA: «IA».",
      "prompt": "Tabla de cantidades estilizada generándose sola desde un modelo 3D, con líneas de datos fluyendo en ámbar. " + ESTILO}]},

   {"dia": "Miércoles 16", "titulo": "Sobredimensionar no es ir por lo seguro",
    "historias": [
     {"rol": "RELLENO", "texto": "Esta frase levantó ampolla la última vez que la dije. La repito igual.",
      "sticker": "Ninguno.",
      "prompt": "Retrato de perfil de un ingeniero mirando un plano con expresión seria, luz lateral dramática pero sobria. " + ESTILO},
     {"rol": "VALOR", "texto": "Sobredimensionar no te hace más seguro. Te hace más caro — y le traslada tu inseguridad al presupuesto del cliente.",
      "sticker": "Ninguno.",
      "prompt": "Dos vigas idénticas en sección, una notablemente más robusta que la otra, con una etiqueta de costo estilizada (símbolo, no texto) más grande en la robusta. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Te ha pasado que revisas un diseño ajeno y está sobrado?",
      "sticker": "ENCUESTA: «Siempre» / «Casi nunca».",
      "prompt": "Lupa sobre un plano estructural, con algunos elementos resaltados en ámbar. Estilo técnico limpio. " + ESTILO},
     {"rol": "VENTA", "texto": "El reel completo está en el feed. Y si quieres las 5 verificaciones que uso antes de firmar: respóndeme ACERO.",
      "sticker": "ENLACE al reel + RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Sello o timbre de aprobación de ingeniero sobre un plano, en ámbar, con la estructura al fondo. " + ESTILO}]},

   {"dia": "Jueves 17", "titulo": "VENTA · La objeción del tiempo",
    "historias": [
     {"rol": "RELLENO", "texto": "«Me interesa, pero no tengo tiempo.» Me lo escribieron tres veces esta semana.",
      "sticker": "Ninguno.",
      "prompt": "Agenda de papel abierta con la semana llena de anotaciones, junto a un teléfono y un casco de obra. Realista, cálido. " + ESTILO},
     {"rol": "VALOR", "texto": "Es 100% asincrónico. No hay horario al que llegar tarde, y el acceso no caduca. Avanzas el sábado a las 11 de la noche si quieres.",
      "sticker": "Ninguno.",
      "prompt": "Reloj mostrando una hora nocturna junto a una pantalla encendida con una clase en reproducción, en una habitación en penumbra. Íntimo. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Ese era tu freno?",
      "sticker": "ENCUESTA: «Sí, era eso» / «El mío es otro». A los segundos se les pregunta cuál por DM.",
      "prompt": "Candado abriéndose estilizado sobre fondo azul, con una ruta de puntos continuando después de él en ámbar. " + ESTILO},
     {"rol": "VENTA", "texto": "Si quieres el temario completo y ver si te cuadra, respóndeme ACERO.",
      "sticker": "RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Documento de temario estilizado en perspectiva, con capítulos como bloques apilados, sobre fondo azul marino. " + ESTILO}]},

   {"dia": "Viernes 18", "titulo": "Cierre de semana + recurso",
    "historias": [
     {"rol": "RELLENO", "texto": "Resumen de la semana en 10 segundos, por si te perdiste algo.",
      "sticker": "Ninguno.",
      "prompt": "Mosaico de tres miniaturas verticales en fila sobre fondo azul marino, como un resumen visual de publicaciones. " + ESTILO},
     {"rol": "VALOR", "texto": "Lo más comentado: que detectar un choque tarde cuesta más que el error en sí.",
      "sticker": "Ninguno.",
      "prompt": "Gráfico de barras ascendente muy simple donde la última barra, en ámbar, es desproporcionadamente alta. Representa el costo creciente. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Qué quieres que tratemos la semana que viene?",
      "sticker": "CAJA DE PREGUNTAS. Lo que más se repita entra a la matriz de octubre.",
      "prompt": "Buzón de sugerencias estilizado en línea fina, con sobres entrando, sobre fondo azul. " + ESTILO},
     {"rol": "VENTA", "texto": "Mañana sale el comparativo ETABS vs SAP2000 en el blog. Y si aún no tienes la calculadora de zapatas: respóndeme ZAPATA, es gratis.",
      "sticker": "CUENTA REGRESIVA al blog + RESPONDER CON PALABRA: «ZAPATA».",
      "prompt": "Calculadora técnica junto a un croquis de zapata aislada con sus cotas, sobre superficie de trabajo azul. " + ESTILO}]},
  ]},

 {"n": 3, "rango": "Lun 21 – Vie 25 de septiembre",
  "hilo": "¿En qué etapa estás? (las 4 puertas del Máster)",
  "porque": "La semana del lanzamiento de la nueva arquitectura. Todo el hilo lleva al "
            "diagnostico: el objetivo es que la gente se ubique en una etapa y escriba.",
  "dias": [
   {"dia": "Lunes 21", "titulo": "Los errores que delatan la etapa",
    "historias": [
     {"rol": "RELLENO", "texto": "Llevo años revisando modelos ajenos. Los errores se repiten tanto que ya sé en qué etapa está cada quien.",
      "sticker": "Ninguno.",
      "prompt": "Pila de planos revisados con marcas de corrección en ámbar, vista cenital, sobre mesa de trabajo. " + ESTILO},
     {"rol": "VALOR", "texto": "El error #1 de quien empieza: modelar sin decidir antes los estándares. Se ve bonito y no sirve para coordinar.",
      "sticker": "Ninguno.",
      "prompt": "Dos modelos 3D idénticos por fuera, uno con estructura interna ordenada por capas y otro con las capas mezcladas y caóticas. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Tu oficina tiene un BEP escrito?",
      "sticker": "ENCUESTA: «Sí» / «¿Un qué?». Los segundos son el público exacto del módulo 1.",
      "prompt": "Documento de protocolo estilizado con una portada limpia y pestañas laterales, sobre fondo azul marino. " + ESTILO},
     {"rol": "VENTA", "texto": "Mañana te explico las 4 etapas por las que pasa todo el mundo. Y por qué casi nadie empieza donde cree.",
      "sticker": "CUENTA REGRESIVA al carrusel del miércoles.",
      "prompt": "Escalera de cuatro peldaños en isométrico sobre fondo azul, con una figura pequeña en el primer peldaño y el cuarto iluminado en ámbar. " + ESTILO}]},

   {"dia": "Martes 22", "titulo": "Mitos de la automatización",
    "historias": [
     {"rol": "RELLENO", "texto": "Tres cosas que me dicen sobre automatizar y que son mentira. Van rápido.",
      "sticker": "Ninguno.",
      "prompt": "Tres burbujas de diálogo vacías en cascada sobre fondo azul marino, la última tachada en ámbar. " + ESTILO},
     {"rol": "VALOR", "texto": "«Hay que saber programar.» No: hay que saber QUÉ automatizar. La parte difícil es identificar la tarea, no escribir el script.",
      "sticker": "Ninguno.",
      "prompt": "Diagrama de nodos tipo programación visual conectados con líneas limpias, muy ordenado, sobre fondo azul. Estilo Dynamo. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Has automatizado algo alguna vez, aunque sea pequeño?",
      "sticker": "ENCUESTA: «Sí» / «Nunca». A los «nunca» se les manda por dónde empezar.",
      "prompt": "Engranaje pequeño moviendo uno grande, línea fina en ámbar sobre azul. Metáfora de esfuerzo mínimo, efecto grande. " + ESTILO},
     {"rol": "VENTA", "texto": "El módulo BIM + IA es exactamente esto, con proyectos reales. Respóndeme RUTA y te digo si te toca ese o uno antes.",
      "sticker": "RESPONDER CON PALABRA: «RUTA».",
      "prompt": "Cerebro estilizado hecho de circuitos conectado a un modelo de edificio, ambos en línea fina blanca con acentos ámbar. " + ESTILO}]},

   {"dia": "Miércoles 23", "titulo": "LAS 4 PUERTAS (la pieza del mes)",
    "historias": [
     {"rol": "RELLENO", "texto": "Hoy publicamos algo que llevábamos meses ordenando. Reorganizamos toda la formación.",
      "sticker": "Ninguno.",
      "prompt": "Plano arquitectónico de una planta con cuatro accesos marcados en ámbar, vista cenital, estilo blueprint sobre azul marino. " + ESTILO},
     {"rol": "VALOR", "texto": "«Quiero aprender BIM» es como decir «quiero aprender medicina». Depende de dónde estés parado. Por eso ahora hay 4 puertas: Estructura, Coordina, Gestiona, Automatiza.",
      "sticker": "Ninguno.",
      "prompt": "Cuatro puertas arquitectónicas en fila, cada una con un ícono distinto encima (checklist, cubos, gráfica, circuito), la retícula del suelo en perspectiva. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Cuál dirías que es la tuya?",
      "sticker": "QUIZ de 4 opciones (sin respuesta correcta): Estructura / Coordina / Gestiona / Automatiza. Es el sticker más importante del mes: cada respuesta es un lead calificado.",
      "prompt": "Las mismas cuatro puertas vistas de frente en composición simétrica, numeradas visualmente por altura creciente. " + ESTILO},
     {"rol": "VENTA", "texto": "Cada puerta entrega su propia microcredencial avalada internacionalmente. Respóndeme RUTA y te digo cuál te toca con tu caso.",
      "sticker": "ENLACE al carrusel + RESPONDER CON PALABRA: «RUTA».",
      "prompt": "Sello o medalla de certificación estilizada en ámbar sobre fondo azul, sobria y profesional, sin texto. " + ESTILO}]},

   {"dia": "Jueves 24", "titulo": "VENTA · El espejo",
    "historias": [
     {"rol": "RELLENO", "texto": "Ayer alguien me respondió: «llevo 3 años modelando bien y sigo en lo mismo».",
      "sticker": "Ninguno.",
      "prompt": "Persona de espaldas frente a una ventana grande de oficina mirando la ciudad, luz de tarde. Reflexivo, no triste. " + ESTILO},
     {"rol": "VALOR", "texto": "Modelar bien te hace indispensable en la tarea. Decidir te hace indispensable en el proyecto. El salto no es de software: es de rol.",
      "sticker": "Ninguno.",
      "prompt": "Dos siluetas: una frente a una pantalla ejecutando, otra frente a un equipo señalando un plano en una mesa. Contraste de rol. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿En qué peldaño estás hoy, de verdad?",
      "sticker": "QUIZ: Modelador / Coordinador / BIM Manager / BIM + IA.",
      "prompt": "Cuatro peldaños ascendentes con etiquetas visuales (herramienta, engranajes, gráfica, circuito), el segundo iluminado. " + ESTILO},
     {"rol": "VENTA", "texto": "Hay un test de 20 preguntas que te lo dice sin adornos. Respóndeme NIVEL y te lo mando.",
      "sticker": "RESPONDER CON PALABRA: «NIVEL».",
      "prompt": "Cuestionario estilizado en pantalla de teléfono con barra de progreso en ámbar, sin texto legible. " + ESTILO}]},

   {"dia": "Viernes 25", "titulo": "El espejo en video",
    "historias": [
     {"rol": "RELLENO", "texto": "Grabé este en una sola toma. Sale de una conversación real de esta semana.",
      "sticker": "Ninguno.",
      "prompt": "Set casero de grabación con luz suave y una silla vacía frente a la cámara, listo para grabar. " + ESTILO},
     {"rol": "VALOR", "texto": "El reel de hoy: por qué el salto que más cuesta es del 1 al 2, y no tiene nada que ver con aprender otro programa.",
      "sticker": "ENLACE al reel.",
      "prompt": "Salto visual entre dos plataformas separadas por un vacío, con una figura a punto de cruzar, en línea fina sobre azul. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Qué te frena a ti para dar ese salto?",
      "sticker": "CAJA DE PREGUNTAS.",
      "prompt": "Puente incompleto sobre fondo azul marino, con las últimas piezas flotando a punto de encajar en ámbar. " + ESTILO},
     {"rol": "VENTA", "texto": "Mañana en el blog: cómo elegir software de estructuras sin casarte con una marca. Y si quieres ubicarte primero, respóndeme NIVEL.",
      "sticker": "CUENTA REGRESIVA al blog + RESPONDER CON PALABRA: «NIVEL».",
      "prompt": "Tres logos genéricos de software representados como formas abstractas en una balanza, sin marcas reales. " + ESTILO}]},
  ]},

 {"n": 4, "rango": "Lun 28 de septiembre – Vie 2 de octubre",
  "hilo": "Nunca estudias solo (el tutor de IA) + cierre",
  "porque": "Cierra el mes con el diferenciador nuevo de ACERO y deja la cuenta caliente "
            "para octubre. TODA la semana depende de que el tutor este desplegado.",
  "dias": [
   {"dia": "Lunes 28", "titulo": "La duda de las 11 de la noche",
    "historias": [
     {"rol": "RELLENO", "texto": "El punto débil de estudiar por tu cuenta siempre fue el mismo, y no es la falta de ganas.",
      "sticker": "Ninguno.",
      "prompt": "Habitación en penumbra con una sola lámpara encendida sobre un escritorio con apuntes y una pantalla. Sensación de estudio nocturno. " + ESTILO},
     {"rol": "VALOR", "texto": "Es la duda que aparece a las 11 de la noche, cuando no hay a quién preguntarle. Se responde tres días después, o nunca.",
      "sticker": "Ninguno.",
      "prompt": "Signo de interrogación formado por líneas de un plano técnico, flotando en un espacio oscuro azul marino. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Te ha pasado abandonar un curso por quedarte trabado?",
      "sticker": "ENCUESTA: «Sí, más de una vez» / «Nunca».",
      "prompt": "Barra de progreso de un curso detenida a la mitad, en tonos apagados con el tramo restante en gris. " + ESTILO},
     {"rol": "VENTA", "texto": "Eso se acabó en la Especialización en Acero. Te lo muestro mañana. Respóndeme ACERO si no quieres esperar.",
      "sticker": "CUENTA REGRESIVA + RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Burbuja de chat iluminada en ámbar en medio de una habitación oscura, como una respuesta que llega de noche. " + ESTILO}]},

   {"dia": "Martes 29", "titulo": "Cómo funciona el tutor",
    "historias": [
     {"rol": "RELLENO", "texto": "Llevamos semanas construyendo esto y hoy por fin lo puedo enseñar.",
      "sticker": "Ninguno.",
      "prompt": "Pantalla de computadora mostrando una interfaz de chat limpia y profesional, vista en ángulo, en un escritorio ordenado. " + ESTILO},
     {"rol": "VALOR", "texto": "Un tutor de IA entrenado SOLO con las clases del programa: los 4 cursos, más de 40 sesiones. Le preguntas normal y te responde con el contenido de tu curso, diciéndote en qué sesión está.",
      "sticker": "Ninguno.",
      "prompt": "Esquema de cuatro bloques de curso conectados por líneas a un núcleo central luminoso en ámbar. Representa entrenamiento con material propio. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Qué le preguntarías primero?",
      "sticker": "CAJA DE PREGUNTAS. Las mejores se prueban EN VIVO mañana con el tutor.",
      "prompt": "Teclado con las manos escribiendo una pregunta, pantalla desenfocada al fondo con una interfaz de chat. " + ESTILO},
     {"rol": "VENTA", "texto": "Y lo más importante: si algo NO está en las clases, te lo dice. No inventa. Respóndeme ACERO para el temario completo.",
      "sticker": "RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Icono de escudo o verificación en ámbar sobre fondo azul, sobrio, junto a un pequeño ícono de libro cerrado. Representa honestidad. " + ESTILO}]},

   {"dia": "Miércoles 30", "titulo": "El tutor, en vivo",
    "historias": [
     {"rol": "RELLENO", "texto": "Le hice las preguntas que me mandaron ayer. Grabé la pantalla sin cortes.",
      "sticker": "Ninguno.",
      "prompt": "Grabación de pantalla en curso indicada por un punto rojo discreto, mostrando una interfaz de chat técnica. " + ESTILO},
     {"rol": "VALOR", "texto": "Mira cómo responde una pregunta de verdad — y cómo cita la sesión exacta para que vuelvas a la clase.",
      "sticker": "ENLACE al reel del feed.",
      "prompt": "Respuesta de chat estructurada con una cita destacada al pie en ámbar, estilo interfaz limpia. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Confiarías en una IA para resolver dudas técnicas?",
      "sticker": "ENCUESTA: «Sí, si cita la fuente» / «Prefiero un humano». Ambas respuestas abren conversación.",
      "prompt": "Dos íconos enfrentados en equilibrio: un circuito y un casco de ingeniero, unidos por una línea ámbar. " + ESTILO},
     {"rol": "VENTA", "texto": "No reemplaza a los instructores: les quita las preguntas repetidas para que las tutorías se usen en lo difícil. Respóndeme ACERO.",
      "sticker": "RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Dos capas de soporte representadas como dos anillos concéntricos, el interior en ámbar (humano) y el exterior en blanco (IA). " + ESTILO}]},

   {"dia": "Jueves 1 de octubre", "titulo": "VENTA · Últimos cupos",
    "historias": [
     {"rol": "RELLENO", "texto": "Cierro la cohorte esta semana. Ya sabes lo que hay dentro, así que voy directo.",
      "sticker": "Ninguno.",
      "prompt": "Puerta de acceso entreabierta con luz cálida saliendo, en un pasillo de estética arquitectónica limpia. " + ESTILO},
     {"rol": "VALOR", "texto": "4 cursos, más de 40 sesiones, 100% asincrónico, acceso que no caduca, tutor de IA incluido y microcredencial al terminar.",
      "sticker": "Ninguno.",
      "prompt": "Cinco íconos en fila vertical representando: cursos, video, reloj infinito, chat, medalla. Línea fina, ámbar sobre azul. " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Alguna duda antes de decidir?",
      "sticker": "CAJA DE PREGUNTAS — se contestan TODAS hoy mismo por DM.",
      "prompt": "Mano sosteniendo un teléfono con una conversación abierta, ambiente cálido de oficina. " + ESTILO},
     {"rol": "VENTA", "texto": "Quedan [CUPOS REALES]. Respóndeme ACERO y lo vemos con tu caso concreto.",
      "sticker": "CUENTA REGRESIVA al cierre + RESPONDER CON PALABRA: «ACERO».",
      "prompt": "Estructura metálica terminada al atardecer, silueta limpia contra el cielo. Aspiracional pero real. " + ESTILO}]},

   {"dia": "Viernes 2 de octubre", "titulo": "Cierre de mes",
    "historias": [
     {"rol": "RELLENO", "texto": "Se acaba septiembre. Hicimos más de lo que teníamos planeado, la verdad.",
      "sticker": "Ninguno.",
      "prompt": "Calendario de pared con el mes terminando, junto a una taza y un cuaderno con notas. Cálido, cotidiano. " + ESTILO},
     {"rol": "VALOR", "texto": "El dato del mes, por si te lo perdiste: el peso de una varilla es Ø²/162 kg/m. Una Ø12 de 12 m pesa 10,7 kg. Sirve para estimar acero en visita, sin planilla.",
      "sticker": "Ninguno.",
      "prompt": "Varillas de acero corrugado apiladas vistas en sección, con una fórmula esquematizada en líneas al lado (sin texto). " + ESTILO},
     {"rol": "INTERACCIÓN", "texto": "¿Qué quieres que hagamos en octubre?",
      "sticker": "CAJA DE PREGUNTAS. Lo que más se repita entra a la matriz.",
      "prompt": "Hoja en blanco sobre mesa de trabajo con un lápiz al lado, esperando ser escrita. Metáfora del mes nuevo. " + ESTILO},
     {"rol": "VENTA", "texto": "Y si este mes te quedaste con ganas de empezar: respóndeme RUTA y arrancamos octubre sabiendo por dónde.",
      "sticker": "RESPONDER CON PALABRA: «RUTA».",
      "prompt": "Camino de retícula azul que se aleja hacia el horizonte con cuatro hitos marcados en ámbar. " + ESTILO}]},
  ]},
]
