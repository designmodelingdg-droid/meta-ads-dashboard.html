/* GUÍA OPERATIVA · HISTORIAS DE INSTAGRAM — versión completa y corregida.
   Reemplaza al PDF del 13-ago. Mismo formato, con tres cosas nuevas:
   el jueves de venta, las secuencias de venta frame por frame, y la regla
   de que el sticker que convierte tiene que ser automatizable. */
const { d, p, pmix, h1, h2, h3, bullet, paso, enlace, codigo, aviso, tabla,
  portada, numeracion, seccion, PageBreak, Paragraph, TextRun, NAVY, NARANJA, ANCHO } = require('./comun');
const { Document, Packer, ShadingType, BorderStyle, WidthType, Table, TableRow, TableCell } = d;
const fs = require('fs');

// ── Cabecera de cada día ───────────────────────────────────────────
const dia = (fecha, titulo, meta) => new Table({
  columnWidths: [ANCHO],
  width: { size: ANCHO, type: WidthType.DXA },
  borders: { top:{style:BorderStyle.NONE}, bottom:{style:BorderStyle.NONE},
    left:{style:BorderStyle.NONE}, right:{style:BorderStyle.NONE},
    insideHorizontal:{style:BorderStyle.NONE}, insideVertical:{style:BorderStyle.NONE} },
  rows: [new TableRow({ children: [new TableCell({
    width: { size: ANCHO, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: NAVY },
    margins: { top: 150, bottom: 150, left: 200, right: 200 },
    children: [
      new Paragraph({ spacing:{after:50}, children:[new TextRun({
        text: fecha.toUpperCase(), bold:true, size:20, color:'E8A04A', characterSpacing:50, font:'Calibri' })] }),
      new Paragraph({ spacing:{after:60}, children:[new TextRun({
        text: titulo, bold:true, size:26, color:'FFFFFF', font:'Calibri' })] }),
      new Paragraph({ children:[new TextRun({
        text: meta, size:17, color:'9FB3C4', font:'Calibri' })] }),
    ],
  })] })],
});

// ── Tabla de frames ────────────────────────────────────────────────
const frames = (filas) => tabla(
  ['#', 'QUÉ SE VE', 'TEXTO EN PANTALLA', 'STICKER', 'QUÉ HACES DESPUÉS'],
  filas, [4, 21, 27, 26, 22]);

const SIN = 'Ninguno.';
const NADA = '— nada, este frame no convierte';

// ═══════════════════════════════════════════════════════════════════
const doc = new Document({
  creator: 'Design Modeling Academy',
  title: 'Guía Operativa · Historias de Instagram',
  description: 'Historias de Instagram — guía completa frame por frame, con el jueves de venta',
  numbering: numeracion,
  sections: [seccion([

    ...portada(
      ['Historias de Instagram'],
      'Guía operativa completa · frame por frame',
      '📖  GUÍA OPERATIVA',
      'CA7520',
      ['Responsable de ejecución: Dayana Calderón',
       'Frecuencia: diaria · lunes a sábado',
       'Redes: Instagram + Facebook (la misma historia)',
       'Versión: 14 de agosto de 2026 — reemplaza a la del 13-ago']),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ QUÉ CAMBIÓ ══
    h1('Qué cambió respecto a la versión anterior'),

    p('Al revisar el mes se vio que las historias no vendían por ningún lado. La auditoría dio tres cosas concretas:'),
    bullet('La semana tipo tenía 0 slots de venta de 7 días, y el sábado lo prohibía expresamente.'),
    bullet('El documento decía «mándales DM» quince veces y no traía ni un guion escrito.'),
    bullet('Toda la conversión se apoyaba en los cuatro stickers que NO se pueden automatizar, y por eso no daba tiempo de responder.'),

    p('Esta versión corrige las tres. Lo que NO cambia: nunca precio ni «inscríbete» en pantalla, y el Máster sigue sin cotizarse.'),

    // ══ 01 REGLAS ══
    h1('01 · Las reglas que no se rompen'),

    h3('1 · El sticker que CONVIERTE tiene que ser automatizable'),
    pmix([['Esta es la regla nueva y la más importante. '],
      'Encuestas, quiz y deslizadores se quedan —son buenísimos para alcance— pero dejan de ser el paso de conversión. El frame que cierra pide responder con una palabra clave.']),

    h3('2 · Todo el que responde con la palabra entra al bot'),
    p('Ya no hay que escribirle a nadie a mano para que esto funcione. El bot lo recoge, manda el DM y lo registra en el CRM.'),

    h3('3 · Nunca precio ni «inscríbete»'),
    p('El objetivo de la historia es que te escriban, no que compren desde ahí.'),

    h3('4 · Máximo 5 frames por secuencia'),
    p('A partir del sexto se cae la mitad de la audiencia.'),

    h3('5 · El primer frame no explica'),
    p('Frena el dedo. La explicación empieza en el segundo frame.'),

    h3('6 · Guardar las buenas en DESTACADAS'),
    p('Por tema: ACERO · BIM+IA · Herramientas · Comunidad · Alumnos. Son la portada del perfil.'),

    h3('7 · Publicar también en Facebook'),
    p('Es la mitad del alcance real de la cuenta. No es opcional, y no como repost automático.'),

    aviso('Cómo encaja con el embudo',
      ['En el feed el CTA es «comenta ACERO / BIM / IA» y lo recoge el bot.',
       'En historias el CTA es «responde con ACERO / BIM / IA / NIVEL / CUPO» y lo recoge el MISMO bot.',
       'Es el mismo camino y la misma automatización: palabra → DM → conversación → venta.'], 'nota'),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 02 STICKERS ══
    h1('02 · Qué sticker usar, y cuál te obliga a trabajar'),

    p('Esta tabla es la que explica por qué antes no daba tiempo. Los cuatro primeros stickers solo viven en el panel de la historia: para aprovecharlos hay que mirarlos y escribir a mano, uno por uno.'),

    tabla(
      ['Sticker', 'Qué te da', '¿Se automatiza?', 'Para qué usarlo ahora'],
      [
        ['Encuesta (2 opciones)', 'volumen de respuestas', '❌ No', 'ALCANCE. El algoritmo empuja la historia. No hay que responderla.'],
        ['Quiz', 'los que fallan', '❌ No', 'ALCANCE + el dato técnico que sorprende. Opcional responder.'],
        ['Deslizador', 'participación fácil', '❌ No', 'Calentar la cuenta. Poco valor, cero obligación.'],
        ['Caja de preguntas', 'conversación real', '❌ No', 'Material para contenido. Se lee cuando haya tiempo.'],
        ['RESPONDER CON PALABRA', 'el lead, en el CRM', '✅ SÍ', '👉 ESTE ES EL QUE CONVIERTE. Va en el último frame.'],
        ['Enlace', 'tráfico directo', '✅ Sí', 'Al blog, al test, al post. Cero trabajo.'],
        ['Cuenta regresiva', 'recordatorio automático', '✅ Sí', 'Cierre de inscripciones. Avisa sola.'],
      ], [20, 20, 14, 46]),

    aviso('Lo que hay que montar antes de usar las palabras nuevas',
      ['El bot ya responde a COMENTARIOS con ACERO, BIM, IA y ZAPATA. Falta que responda también a MENSAJES DIRECTOS, y crear las palabras NIVEL y CUPO.',
       'En GoHighLevel es el mismo workflow con un disparador más: Instagram DM / Facebook Message → contiene la palabra.',
       'Hasta que esté montado, NO se publica una historia que prometa algo por palabra clave: prometería algo que no llega.'], 'alerta'),

    // ══ SEMANA TIPO ══
    h1('La semana tipo'),
    p('Esto se publica siempre, haya o no pieza de feed ese día.'),

    tabla(
      ['Día', 'Qué se publica', 'Sticker'],
      [
        ['Lunes', 'Secuencia de la pieza del día (3–5 frames)', 'el que traiga la pieza'],
        ['Martes', 'Detrás de cámara: qué estás grabando o modelando. Sin producción.', 'ninguno o encuesta simple'],
        ['Miércoles', 'Secuencia de la pieza del día', 'el que traiga la pieza'],
        ['JUEVES 🆕', 'SECUENCIA DE VENTA — rotan las 3 de la sección 05', 'responder con palabra'],
        ['Viernes', 'Secuencia de la pieza del día + republicar respuestas', 'enlace al post'],
        ['Sábado', 'Testimonio o avance de un alumno (con permiso)', 'encuesta + «responde NIVEL»'],
        ['Domingo', 'Nada, o una sola de cierre. Descansar también es estrategia.', '—'],
      ], [14, 56, 30]),

    pmix([['El sábado deja de ser «sin vender». '], 'Sigue sin llevar precio, pero cierra con palabra clave para separar al curioso del interesado.']),

    h1('Destacadas del perfil'),
    p('Las buenas secuencias no se pierden a las 24 horas: se guardan. Son la portada del perfil para quien te descubre.'),
    tabla(['Destacada', 'Qué va dentro'],
      [
        ['ACERO', 'Conexiones, verificaciones y sobredimensionamiento.'],
        ['BIM + IA', 'Revit con IA, coordinación, criterio.'],
        ['HERRAMIENTAS', 'La calculadora y las que vengan.'],
        ['COMUNIDAD', 'Recaps y conversaciones.'],
        ['ALUMNOS', 'Testimonios y casos.'],
      ], [26, 74]),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 03 CALENDARIO ══
    h1('03 · Calendario del mes'),
    p('Los días con secuencia escrita están desarrollados frame por frame en las secciones 04 y 05. Los que no aparecen se cubren con la semana tipo.'),

    tabla(
      ['Fecha', 'Pieza del día', 'Frames', 'Sección'],
      [
        ['Lun 4', '3 cosas que tu Revit ya hace con IA — CORREGIDA', '5', '04'],
        ['Mié 6', '5 errores al usar IA en proyectos BIM', '4', '04'],
        ['JUE 7', 'VENTA A · La objeción (ACERO)', '4', '05'],
        ['Vie 8', 'Calculadora de Zapatas (lead magnet)', '5', '04'],
        ['Sáb 9', 'Diálogo Arqui vs Inge (humor)', '3', '04'],
        ['Lun 11', 'Le pedí a la IA que coordinara un modelo BIM', '4', '04'],
        ['Mié 13', 'De modelador a BIM Manager', '3', '04'],
        ['JUE 14', 'VENTA B · El espejo (Máster)', '4', '05'],
        ['Vie 15', 'IA en BIM: qué automatizar y qué NUNCA delegar', '3', '04'],
        ['Sáb 16', 'Esto lo hizo una IA en 10 segundos (mito del render)', '4', '04'],
        ['Lun 18', '¿Qué hace un BIM Manager que la IA nunca podrá?', '4', '04'],
        ['Mié 20', 'El error #1 al diseñar conexiones en acero', '4', '04'],
        ['JUE 21', 'VENTA C · Los cupos (ACERO)', '3', '05'],
        ['Sáb 23', 'Acero: 5 verificaciones que no puedes saltarte', '3', '04'],
        ['Sáb 23', 'Cómo activar la IA de Revit — video largo', '3', '04'],
        ['Lun 25', 'Coordinador BIM vs. el que sigue modelando a mano', '3', '04'],
        ['Mié 27', '3 señales de que tu estructura está sobredimensionada', '4', '04'],
        ['JUE 28', 'VENTA A otra vez (o la que mejor funcione)', '4', '05'],
        ['Vie 29', 'Comunidad: recap del mes + invitación', '3', '04'],
      ], [11, 56, 12, 21]),

    p('Los días 22, 30 y 31 siguen pendientes de definir la pieza. Hasta que se cierren, se cubren con la semana tipo. No se deja el día sin historia.'),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 04 SECUENCIAS DEL MES ══
    h1('04 · Las secuencias, frame por frame'),
    p('Cada bloque es un día. Se graba y se publica en orden. La columna «Sticker» es la que convierte; «Qué haces después» dice si tienes que hacer algo o no.'),

    // ─ LUNES 4 ─
    dia('Lunes 4', '3 cosas que tu Revit ya hace con IA', 'Carrusel · IA · Máster BIM + IA · 5 frames'),
    aviso('⚠️ Esta secuencia se corrigió el 11-ago',
      ['La versión anterior prometía 3 funciones que no existen. Autodesk dice, textual, que hasta Revit 2026 NO hay funciones de IA — el Autodesk Assistant llegó en la 2027.',
       'Los frames de abajo ya están corregidos. NO uses la versión vieja.'], 'alerta'),
    frames([
      ['1','Grabación de pantalla de Revit, moviéndote por el menú. 3 segundos, sin decir nada.','Revit ya tiene IA. Pero solo si estás en la versión correcta.',SIN,NADA],
      ['2','Texto grande sobre azul. «2026» tachado, «2027» en naranja.','Hasta Revit 2026 no hay funciones de IA. Lo que existe llegó en la 2027.','ENCUESTA: «¿En qué versión estás?» → 2026 o antes / 2027','Nada. Es alcance — el dato sorprende y la gente vota.'],
      ['3','Captura real del panel del Autodesk Assistant abierto.','Le escribes en lenguaje normal y crea láminas, tablas y plantas.',SIN,NADA],
      ['4','Texto sobre azul.','Ninguna te da el proyecto. Te da el borrador. El criterio lo pones tú.',SIN,NADA],
      ['5','Captura del artículo del blog.','El paso a paso completo, con las fuentes de Autodesk.','ENLACE al artículo + «o responde IA y te lo mando»','Nada — el enlace es directo y la palabra la agarra el bot.'],
    ]),

    // ─ MIÉRCOLES 6 ─
    dia('Miércoles 6', '5 errores al usar IA en tus proyectos BIM', 'Carrusel · IA · Máster BIM + IA · 4 frames'),
    frames([
      ['1','Texto grande sobre azul, sin adornos.','5 errores al usar IA en BIM. El #3 te cuesta el proyecto.',SIN,NADA],
      ['2','Pantalla partida: un chat de IA a la izquierda, un plano a la derecha.','El #1: confiar en la primera respuesta.','ENCUESTA: «Me ha pasado» / «Siempre reviso»','Nada. Si tienes tiempo, escríbele a los del «Me ha pasado».'],
      ['3','Portada de una norma con un naranja encima.','El #3: no revisar contra la norma. La IA no sabe qué norma aplica en tu país.','QUIZ: «¿La IA conoce tu norma local?» Sí / No / Depende (respuesta: No)','Nada. Opcional: DM a los que fallaron.'],
      ['4','Captura del carrusel.','Los 5 están en el post. ¿Cuál has cometido?','ENLACE al post + «responde IA»','Nada — lo agarra el bot.'],
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // ─ VIERNES 8 ─
    dia('Viernes 8', 'Calculadora de Zapatas', 'Lead magnet · Carrusel + post · 5 frames'),
    frames([
      ['1','Tu celular en la mano con la calculadora abierta. Vertical, sin edición.','Dimensioné una zapata en 2 minutos. Desde el celular.',SIN,NADA],
      ['2','Grabación de pantalla real: metes carga y esfuerzo del suelo, sale el resultado.','Metes la carga. Metes el esfuerzo del suelo. Y listo.',SIN,'Nada. Que se vea funcionando — eso fue lo que la hizo el post #1 del mes.'],
      ['3','Fondo azul, texto grande.','Es gratis. ¿La quieres?','👉 «Responde ZAPATA y te la mando»','Nada — el bot manda el enlace solo. ESTE es el frame que convierte.'],
      ['4','Captura del post publicado.','También está en el post','ENLACE al post + «Comenta ZAPATA»','Nada — los que comentan entran al bot.'],
      ['5','Captura de los comentarios pidiéndola (prueba social real).','Ayer la pidieron 37 personas.','ENLACE al post','Solo se publica si los comentarios existen de verdad. NUNCA inventar el número.'],
    ]),

    // ─ SÁBADO 9 ─
    dia('Sábado 9', 'Diálogo Arqui vs Inge sobre la IA', 'Reel de humor · 3 frames'),
    frames([
      ['1','El reel recortado: solo el remate del chiste.','—A ti te reemplaza cualquier plantilla de Pinterest',SIN,NADA],
      ['2','Fondo azul, texto centrado.','El chiste tiene fondo: la IA no reemplaza al que tiene criterio. Reemplaza al que no lo tiene.','ENCUESTA: «Team arqui» / «Team inge»','Nada. La encuesta de bando es la que más votos saca: sirve para alcance.'],
      ['3','Captura del reel publicado.','¿De qué lado estás?','ENLACE al reel',NADA],
    ]),

    // ─ LUNES 11 ─
    dia('Lunes 11', 'Le pedí a la IA que coordinara un modelo BIM', 'Reel 32s · IA · Máster · 4 frames'),
    frames([
      ['1','Pantalla del modelo con el choque resaltado.','Le pedí a la IA que coordinara un modelo.',SIN,NADA],
      ['2','El acierto en pantalla.','Encontró un choque que a mí se me pasó.',SIN,NADA],
      ['3','El fallo en pantalla, marcado en naranja.','Y marcó como crítico algo que en obra se resuelve solo.','ENCUESTA: «¿Confiarías en ella?» Sí / No / Solo revisando','Nada. Los de «Solo revisando» son el perfil exacto del Máster — si tienes tiempo, escríbeles.'],
      ['4','Tú a cámara.','Te ahorra horas. No te ahorra el criterio.','👉 «Responde IA y te mando el análisis completo»','Nada — lo agarra el bot.'],
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // ─ MIÉRCOLES 13 ─
    dia('Miércoles 13', 'De modelador a BIM Manager', 'Reel 30s · Venta · Máster · 3 frames'),
    frames([
      ['1','Texto sobre azul.','Modelas bien. Pero no despegas a BIM Manager.',SIN,NADA],
      ['2','Las 3 habilidades numeradas.','01 Coordinar · 02 Gestionar · 03 IA aplicada','ENCUESTA: «¿Cuál te falta?» Coordinar / Gestionar / IA','Nada. La respuesta te dice qué le sirve a cada uno.'],
      ['3','Tú a cámara, tono directo pero sin vender.','Las 3 se aprenden. Ninguna se aprende sola.','👉 «Responde NIVEL y te mando el test que te dice dónde estás»','Nada. Nada de precio ni de «inscríbete»: el objetivo es que escriban.'],
    ]),

    // ─ VIERNES 15 ─
    dia('Viernes 15', 'IA en BIM: qué automatizar y qué NUNCA delegar', 'Blog + LinkedIn + post IG · 3 frames'),
    frames([
      ['1','Fondo azul, texto grande.','¿Qué SÍ le delegarías a una IA en tu proyecto?','CAJA DE PREGUNTAS abierta','Nada obligatorio. Las respuestas son material para el próximo contenido: guárdalas.'],
      ['2','Dos columnas: AUTOMATIZA / NO DELEGUES.','Automatiza: cantidades, documentación, choques. No delegues: norma, prioridad, la firma.','DESLIZADOR: «¿Cuánto de tu trabajo automatizarías?» 0-100%','Nada. El deslizador es el de más participación: úsalo para alcance.'],
      ['3','Captura del artículo del blog.','La guía completa está en el blog.','ENLACE al blog','Nada — el enlace va directo.'],
    ]),

    // ─ SÁBADO 16 ─
    dia('Sábado 16', 'Esto lo hizo una IA en 10 segundos', 'Mito del render · Carrusel · 4 frames'),
    frames([
      ['1','El render final a pantalla completa. Sin texto los primeros 2 segundos.','(nada)',SIN,NADA],
      ['2','El mismo render.','¿Cuánto crees que tomó esto?','QUIZ: «4 horas» / «1 hora» / «10 segundos» (respuesta: 10 segundos)','Nada. El quiz con respuesta sorprendente es el que más se comparte.'],
      ['3','Foto del boceto a mano al lado del render.','Partí de esto.',SIN,NADA],
      ['4','Texto sobre azul.','La IA no diseñó. Solo me quitó las horas de renderizar.','ENCUESTA: «¿Lo usarías en tus entregas?» Sí / No me atrevo','Nada. Si tienes tiempo, pregunta a los de «No me atrevo» por qué: ahí sale la objeción real.'],
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // ─ LUNES 18 ─
    dia('Lunes 18', '¿Qué hace un BIM Manager que la IA nunca podrá?', 'Carrusel · IA · Máster · 4 frames'),
    frames([
      ['1','Texto sobre azul.','¿Qué hace un BIM Manager que la IA nunca podrá?','CAJA DE PREGUNTAS: «Dime tú primero»','Nada obligatorio. Preguntar ANTES de dar la respuesta duplica las respuestas.'],
      ['2','Las 3 en pantalla.','Prioriza. Negocia. Responde.',SIN,NADA],
      ['3','Una firma manuscrita en naranja sobre el azul.','La IA no firma nada.','ENCUESTA: «¿De acuerdo?» Sí / No del todo','Nada. Los de «No del todo» son buena puerta de entrada si tienes tiempo.'],
      ['4','Republicación de 2-3 respuestas de la caja del frame 1.','Esto me respondieron ustedes','ENLACE al carrusel','Republicar respuestas hace que la gente participe la próxima vez.'],
    ]),

    // ─ MIÉRCOLES 20 ─
    dia('Miércoles 20', 'El error #1 al diseñar conexiones en acero', 'Post plano · ACERO · Especialización · 4 frames'),
    frames([
      ['1','Foto o esquema del nudo dibujado como empotrado en el modelo.','Tu modelo dice que esta conexión toma momento.',SIN,NADA],
      ['2','El detalle real de taller: dos ángulos al alma.','Y en obra se construye así.','QUIZ: «¿Esta conexión toma momento?» Sí / No (respuesta: No)','Nada. Frame clave para ACERO: si tienes tiempo, DM a los que fallan.'],
      ['3','Texto sobre azul.','El momento se va al vano. Las derivas no son las que calculaste.','ENCUESTA: «¿Defines la conexión antes o después de analizar?»','Nada. Los de «Después» son exactamente el error del post.'],
      ['4','Captura del post.','Los 3 pasos para evitarlo, en el post.','👉 «Responde ACERO y te mando la guía» + ENLACE','Nada — lo agarra el bot de la Especialización.'],
    ]),

    // ─ SÁBADO 23 a ─
    dia('Sábado 23', 'Acero: 5 verificaciones que no puedes saltarte', 'Blog + LinkedIn + post IG · 3 frames'),
    frames([
      ['1','Texto sobre azul.','El perfil «pasa» por resistencia. Y el diseño está mal igual.',SIN,NADA],
      ['2','Las 5 verificaciones listadas.','Pandeo local · Lateral-torsional · Derivas y P-Δ · Conexiones · Placa base','ENCUESTA: «¿Cuál revisas siempre?»','Nada. La que menos voten es tu próximo tema de contenido: la historia también es investigación.'],
      ['3','Captura del artículo.','La guía completa está en el blog.','👉 «Responde ACERO» + ENLACE al blog','Nada — lo agarra el bot.'],
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // ─ SÁBADO 23 b ─
    dia('Sábado 23', 'Cómo activar la IA de Revit — video largo', 'YouTube + Short · 3 frames'),
    frames([
      ['1','Grabación tuya montando el video. Detrás de cámara, sin producción.','Grabando el paso a paso completo.',SIN,'Nada. El detrás de cámara sube la cercanía y no cuesta nada.'],
      ['2','La miniatura del video.','Sale hoy. ¿Lo quieres ver?','CUENTA REGRESIVA a la hora de publicación','Nada — los que la activan reciben aviso solos. Es el sticker más subestimado.'],
      ['3','Fragmento del video: el momento del choque.','Este es el minuto que más te va a servir.','ENLACE al video',NADA],
    ]),

    // ─ LUNES 25 ─
    dia('Lunes 25', 'Coordinador BIM vs. el que sigue modelando a mano', 'Reel 15s · BIM · 3 frames'),
    frames([
      ['1','El reel recortado: solo el POV del que modela a mano.','Tres días para un detalle.',SIN,NADA],
      ['2','El corte al coordinador BIM.','20 minutos.','ENCUESTA: «Team a mano» / «Team BIM+IA»','Nada. Si tienes tiempo, pregunta a los de «Team a mano» qué los frena: es oro para el mes siguiente.'],
      ['3','Captura del reel.','Modelar a mano en 2026 es usar ábaco teniendo Excel.','ENLACE al reel',NADA],
    ]),

    // ─ MIÉRCOLES 27 ─
    dia('Miércoles 27', '3 señales de que tu estructura de acero está sobredimensionada', 'Carrusel · ACERO · 4 frames'),
    frames([
      ['1','Esquema de pórtico con todos los perfiles iguales.','Si usas el mismo perfil en toda la estructura, no estás siendo conservador.',SIN,NADA],
      ['2','Tabla de ratios D/C con valores en 0.4 resaltados.','Estás pagando acero de más.','ENCUESTA: «¿Revisas ratio D/C elemento por elemento?» Siempre / A veces / Nunca','Nada. «A veces» y «Nunca» son leads directos de ACERO.'],
      ['3','Íconos: soldadura · montaje · cimentación, con «+$».','El exceso no se queda en el perfil. Lo paga el cliente 3 veces.',SIN,NADA],
      ['4','Captura del carrusel.','Las 3 señales, en el post.','👉 «Responde ACERO» + ENLACE','Nada — lo agarra el bot.'],
    ]),

    // ─ VIERNES 29 ─
    dia('Viernes 29', 'Comunidad: recap del mes + invitación', 'Post · Comunidad · 3 frames'),
    frames([
      ['1','Collage de capturas reales de la comunidad (con permiso).','Esto pasó este mes adentro',SIN,NADA],
      ['2','Captura de una duda resuelta.','Una pregunta que respondimos entre todos.','ENCUESTA: «¿Te sirve este tipo de comunidad?» Sí / Cuéntame más','Nada obligatorio.'],
      ['3','Texto sobre azul.','No es un grupo de anuncios. Es donde se conversa de verdad.','👉 «Responde COMUNIDAD y te mando la invitación»','Nada — lo agarra el bot. Nunca invitar en masa.'],
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 05 VENTA ══
    h1('05 · Las secuencias de VENTA (los jueves)'),
    p('Rotan cada jueves. Ninguna dice un precio. Ninguna dice «inscríbete». Las tres cierran con palabra clave, así que ninguna te obliga a responder a mano.'),

    dia('Jueves · Venta A', 'La objeción — ACERO', 'Se usa cuando ya vieron contenido técnico de acero y no han escrito · 4 frames'),
    frames([
      ['1','Tú a cámara, sin producción.','Me escribieron esto la semana pasada:',SIN,NADA],
      ['2','Captura real de un DM, tapando el nombre.','«Me interesa, pero no tengo tiempo»',SIN,'Tiene que ser un DM real. Si no tienes uno, no inventes la captura: usa texto sobre azul.'],
      ['3','Texto sobre azul.','Es 100% asincrónico. No hay horario al que llegar tarde. El acceso no caduca.','ENCUESTA: «¿Ese era tu freno?» → Sí / El mío es otro','Nada. Los de «El mío es otro» son material: si tienes tiempo, pregúntales.'],
      ['4','Tú a cámara.','Si quieres el temario completo, respóndeme con la palabra ACERO.','👉 «Responde ACERO»','Nada — el bot manda el temario y lo registra. ESTE frame es el que convierte.'],
    ]),

    dia('Jueves · Venta B', 'El espejo — Máster', 'Que se reconozca en el problema antes de hablarle del producto · 4 frames'),
    frames([
      ['1','Texto sobre azul.','Llevas 3 años modelando bien. Y sigues esperando a que te digan qué modelar.',SIN,NADA],
      ['2','Los 4 niveles en pantalla.','Modelador → Coordinador → BIM Manager → BIM + IA','QUIZ: «¿Dónde crees que estás?» (sin respuesta correcta)','Nada. Solo alcance.'],
      ['3','Texto sobre azul.','El salto que más cuesta es del 1 al 2. Y no es de software: es dejar de ejecutar y empezar a decidir.',SIN,NADA],
      ['4','Captura del test.','Hay un test de 20 preguntas que te lo dice sin adornos.','ENLACE al test + 👉 «o responde NIVEL»','Nada. Quien hace el test entra a la secuencia de correo y se vende solo.'],
    ]),

    aviso('Por qué la B cierra al test y no al Máster',
      'Porque el Máster no se cierra en una historia ni en un DM: se cierra en una llamada. El test hace el trabajo intermedio — la persona descubre sola qué le falta, y a partir de ahí la secuencia de correo la acompaña. Tú no tienes que convencer a nadie.', 'nota'),

    dia('Jueves · Venta C', 'Los cupos — ACERO', 'UNA VEZ AL MES · 3 frames'),
    frames([
      ['1','Los 4 logos: Robot · Advance Steel · Revit · certificaciones.','4 programas. 4 meses. A tu ritmo.',SIN,NADA],
      ['2','El número enorme sobre azul.','Esta cohorte son 10 cupos. Quedan 8.','CUENTA REGRESIVA al cierre de inscripciones','Nada — avisa sola a quien la active.'],
      ['3','Tú a cámara.','Si quieres el detalle, respóndeme con la palabra CUPO.','👉 «Responde CUPO»','Nada — lo agarra el bot.'],
    ]),

    aviso('Las dos reglas duras de la secuencia C',
      ['1) El número tiene que ser el de verdad. Hoy son 10 cupos por cohorte y quedan 8 (14-ago-2026). Se actualiza cada vez que se publica. Esta gente vuelve al mes siguiente: si ve el mismo contador, se acabó la credibilidad — y la credibilidad es lo único que vende un programa de $199 por internet.',
       '2) La cuenta regresiva va al CIERRE de inscripciones de esta cohorte, NO a la apertura. La cohorte abre todos los meses, así que «abre pronto» no aprieta nada. Lo que aprieta es que estos 8 cupos se acaban.',
       '3) NO se publica hasta que el bot tenga montada la palabra CUPO.'], 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 06 DM ══
    h1('06 · Los DM, para cuando quieras responder a mano'),
    p('Con las palabras clave montadas ya no hace falta responder para que esto funcione. Pero cuando tengas tiempo y quieras escribirle a alguien, aquí están los guiones. Se copian, se cambia el nombre y se mandan.'),

    aviso('Las tres reglas del DM',
      ['1) Siempre con el nombre de la persona. Un DM sin nombre se lee como bot.',
       '2) Nunca el precio del Máster. Si preguntan, se pasa a llamada. El de ACERO sí se puede decir.',
       '3) Una pregunta al final, siempre. Un DM que no pregunta se muere ahí.'], 'nota'),

    h3('DM 1 · Votó la opción «que le falta algo» en una encuesta'),
    codigo(['¡Hola [NOMBRE]! Vi que votaste «[SU RESPUESTA]» en la historia 👀',
            '',
            'Te cuento en corto por qué importa: [UNA FRASE con la',
            'consecuencia real del hueco que admitió].',
            '',
            '¿Te pasa seguido o fue una vez?']),

    h3('DM 2 · Falló un quiz'),
    codigo(['¡Hola [NOMBRE]! El quiz de la historia tenía trampa 😄 la',
            'respuesta era [RESPUESTA] y casi todo el mundo falló, así',
            'que no eres tú.',
            '',
            'Te explico por qué: [2 O 3 LÍNEAS, técnicas de verdad].',
            '',
            '¿En qué tipo de proyecto te estás encontrando esto?']),
    pmix([['Nunca hagas sentir tonto a nadie. '], '«Casi todo el mundo falló» convierte la vergüenza en curiosidad.']),

    h3('DM 3 · Escribió en la caja de preguntas'),
    codigo(['¡Hola [NOMBRE]! Me preguntaste «[SU PREGUNTA]».',
            '',
            '[RESPUESTA REAL, útil, sin vender nada.]',
            '',
            '¿Te sirve así o quieres que lo aterrice a tu caso?']),
    pmix(['Ese ', ['«¿lo aterrizo a tu caso?»'], ' es la puerta: quien dice que sí está pidiendo una conversación de venta sin saberlo.']),

    h3('DM 4 · Respondió a una historia de venta'),
    codigo(['¡Hola [NOMBRE]! Gracias por responder 🙌',
            '',
            'Antes de contarte nada: ¿en qué estás trabajando ahora y qué',
            'te gustaría poder hacer que hoy no puedes?',
            '',
            'Según lo que me digas te sirve una cosa u otra — y a veces la',
            'respuesta es que todavía no es tu momento. Prefiero decírtelo',
            'a venderte algo que no necesitas.']),

    h3('DM 5 · Preguntó el precio'),
    codigo(['¡Hola [NOMBRE]! Te lo cuento con calma en 30 minutos, que así',
            'te digo también si te conviene o no según dónde estés 👇',
            '',
            'https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe',
            '',
            'Si prefieres por aquí, dime primero en qué estás trabajando.']),
    pmix([['Excepción — ACERO: '], 'ahí el precio SÍ se dice por DM ($499,99 → $199,99), porque es decisión rápida. El Máster no: siempre llamada.']),

    new Paragraph({ children: [new PageBreak()] }),

    // ══ 07 CHECKLIST ══
    h1('07 · Tu día, ahora'),

    p('Esto es lo que cambia de verdad respecto a la versión anterior. Antes había que revisar stickers y escribir DM todas las tardes. Ahora no.'),

    tabla(
      ['Cuándo', 'Qué haces', '¿Obligatorio?'],
      [
        ['Mañana', 'Grabar y publicar la secuencia del día en el orden escrito. Verificar que el último frame lleve la palabra clave.', 'SÍ'],
        ['Justo después', 'Publicar la misma secuencia en Facebook. No como repost automático.', 'SÍ'],
        ['Cuando puedas', 'Mirar las respuestas de encuestas y quiz. Son para aprender, no para responder.', 'no'],
        ['Cuando puedas', 'Escribirle a quien votó «lo que le falta». Es un extra, no el motor.', 'no'],
        ['Noche', 'Guardar en DESTACADAS la secuencia si funcionó.', 'SÍ'],
        ['Viernes', 'Republicar las 3 mejores respuestas de la caja del jueves.', 'si hubo'],
      ], [16, 62, 22]),

    aviso('Lo que hace el bot solo, sin ti',
      ['Todo el que responde con ACERO, BIM, IA, ZAPATA, NIVEL, CUPO o COMUNIDAD recibe su DM, entra al CRM y arranca su secuencia de correo. A cualquier hora, también los domingos.',
       'Esa es la diferencia entre una estrategia que se sostiene y una que dura tres días.'], 'nota'),

    h1('Lo único que se mide'),
    p('No son las vistas. Una historia con 300 vistas y 12 respuestas vale más que una de 3.000 y ninguna.'),
    tabla(
      ['Semana', 'Respuestas con palabra clave', 'Entraron al bot', 'Llamadas agendadas'],
      [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']], [16, 34, 25, 25]),
    pmix([['«Respuestas con palabra clave» es la columna nueva'],
      ' y no depende de que nadie anote nada: sale del CRM.']),

    h1('Lo que hay que montar antes de arrancar'),
    tabla(['Qué', 'Quién', 'Bloquea a'],
      [
        ['Disparador de DM en el bot (Instagram/Facebook Message)', 'Equipo técnico', 'TODAS las secuencias'],
        ['Palabras nuevas: NIVEL, CUPO, COMUNIDAD', 'Equipo técnico', 'Venta B, Venta C, Vie 29'],
        ['Confirmar cupos restantes cada vez que se publique la C', 'Dayana', 'Venta C'],
        ['Autorización de un alumno para el testimonio del sábado', 'Dayana', 'sábados'],
      ], [52, 24, 24]),

    p('Sin el disparador de DM montado, ninguna secuencia se publica con palabra clave: prometería algo que no llega. Mientras tanto, se cierra con enlace.', { bold: true }),

  ])],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/home/user/meta-ads-dashboard.html/matriz-viral/entregables/3-Historias-Instagram-GUIA-COMPLETA.docx', b);
  console.log('OK guía completa');
});
