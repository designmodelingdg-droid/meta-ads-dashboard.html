const { d, p, pmix, h1, h2, h3, bullet, paso, enlace, codigo, aviso, tabla,
  portada, numeracion, seccion, PageBreak, Paragraph } = require('./comun');
const { Document, Packer } = d;
const fs = require('fs');

const doc = new Document({
  creator: 'Design Modeling Academy',
  title: 'Historias que venden',
  description: 'Estrategia de venta por historias de Instagram, sin depender de responder a mano',
  numbering: numeracion,
  sections: [seccion([

    ...portada(
      ['Historias que venden'],
      'Lo que le faltaba a la estrategia de historias',
      '🟠  ESTRATEGIA',
      'CA7520',
      ['Design Modeling Academy', 'Complemento de la Guía Operativa · Agosto 2026',
       'Fecha: 14 de agosto de 2026']),

    new Paragraph({ children: [new PageBreak()] }),

    // ── 1 ──────────────────────────────────────────────────────
    h1('De dónde sale esto'),

    p('Dayana revisó las historias del mes y dijo: «en todas las historias no hay de ventas por ningún lado».'),
    p('Se auditó la Guía Operativa de Historias de agosto contra la matriz de contenido. La conclusión es mixta, y conviene decirla completa.'),

    h2('Donde la impresión NO da en el blanco'),

    p('La guía sí tiene venta, solo que no está en la historia: está en el mensaje directo. Es su propia regla de oro:'),
    codigo(['«El sticker es la conversión. Todo el que responde el sticker',
            'recibe un DM. Ahí es donde se cierra — nunca en la historia.»']),
    pmix(['Y la regla 3 —«nunca precio ni inscríbete»— ', ['está bien y no se toca'],
      '. Coincide con la regla permanente de la academia: el Máster no se cotiza por contenido ni por chat. De las 15 secuencias, 13 llevan instrucción de DM.']),
    p('O sea: el diseño es correcto. El problema es otro.'),

    h2('Donde da de lleno: cuatro huecos medidos'),

    h3('1 · La semana tipo no tiene ni un slot de venta'),
    tabla(
      ['Día', 'Qué se publica', 'Función'],
      [
        ['Lunes', 'pieza del día', 'educativo'],
        ['Martes', 'detrás de cámara', 'cercanía'],
        ['Miércoles', 'pieza del día', 'educativo'],
        ['Jueves', 'caja de preguntas', 'conversación'],
        ['Viernes', 'pieza del día + republicar', 'educativo'],
        ['Sábado', 'testimonio «sin vender»', 'prueba social'],
        ['Domingo', 'nada', '—'],
      ], [16, 52, 32]),
    pmix([['Cero de siete. '], 'Y el sábado, que es el día natural para vender, lo prohíbe expresamente. Nadie está diseñando el momento de la oferta.']),

    h3('2 · La guía dice «mándales DM» 15 veces y no trae ni un guion'),
    p('Este es el hueco grande. Todo el paso donde vive la conversión depende de improvisar, uno por uno, cada tarde. En la práctica eso se hace tres días y se abandona.'),
    pmix(['La conversión no está rota: ', ['está sin construir'], '.']),

    h3('3 · ACERO es el 20 % de las historias, siendo el producto que más convierte'),
    tabla(['Producto', 'Secuencias en agosto'],
      [['Máster BIM + IA', '12'], ['Especialización en ACERO', '3']], [60, 40]),
    p('ACERO trae leads a $0,45–$0,61 y cierra más rápido. Está infrarrepresentado justo en el canal más directo.'),

    h3('4 · La cuenta regresiva se gasta anunciando un video'),
    p('La propia guía la llama «el sticker más subestimado». Es el único que crea urgencia sin decir un precio — o sea, el único que puede vender sin romper la regla 3.'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── 2 · EL ARREGLO DE FONDO ────────────────────────────────
    h1('🔑 «No me da tiempo de responder»'),

    p('Dayana, 14-ago: «chévere por DM, pero si no me da tiempo de estar respondiendo en las historias nos jodemos».'),

    aviso('Tiene razón, y es el punto que hunde la estrategia entera.',
      'Un plan que exige responder a mano todos los días se hace tres días y se abandona. Y entonces las historias vuelven a ser solo alcance. No es falta de disciplina: es un diseño que pide trabajo manual diario.', 'alerta'),

    h2('Por qué pasa: no todos los stickers se pueden automatizar'),

    tabla(
      ['Sticker', '¿Dónde cae la respuesta?', '¿Automatizable?'],
      [
        ['Encuesta', 'solo en el panel de la historia', '❌ No — hay que escribir a mano'],
        ['Quiz', 'solo en el panel', '❌ No'],
        ['Deslizador', 'solo en el panel', '❌ No'],
        ['Caja de preguntas', 'solo en el panel', '❌ No'],
        ['Responder a la historia', 'LLEGA A LA BANDEJA DE MENSAJES', '✅ SÍ — lo agarra el bot'],
        ['Enlace', 'no hay respuesta, va directo', '✅ Cero trabajo'],
        ['Cuenta regresiva', 'avisa sola', '✅ Cero trabajo'],
      ], [24, 40, 36]),

    pmix(['Ahí está el problema: ', ['la guía apoya toda la conversión en los cuatro stickers que NO se pueden automatizar'], '.']),

    h2('El arreglo: mover el CTA a lo que sí se automatiza'),

    p('Es exactamente lo que ya funciona en el feed. Ahí el CTA no es un sticker: es «comenta ACERO», y el bot lo recoge. Está probado — comentario → DM → registro en el CRM en 3 minutos, medido dos veces.'),
    p('En historias el equivalente es:'),
    codigo(['«Responde esta historia con la palabra ACERO y te lo mando»']),
    pmix(['La persona escribe. Eso ', ['cae en la bandeja de mensajes'],
      '. El bot lo lee, detecta la palabra y dispara la secuencia sola. Tú no tocas nada.']),

    aviso('La regla nueva',
      ['El sticker que convierte tiene que ser automatizable.',
       'Encuestas, quiz y deslizadores se quedan — son buenísimos para alcance y para que el algoritmo empuje la historia — pero dejan de ser el paso de conversión. Nadie tiene la obligación de responderlos uno por uno.',
       'El frame que convierte pide responder con una palabra.'], 'nota'),

    h2('Cómo queda cada secuencia'),
    tabla(
      ['Frames', 'Función', 'Sticker', 'Trabajo tuyo'],
      [
        ['1 al 3', 'valor, enganche, alcance', 'encuesta / quiz', 'ninguno'],
        ['último', 'CONVERSIÓN', '«responde con [PALABRA]»', 'ninguno — lo agarra el bot'],
      ], [12, 30, 28, 30]),

    h2('Las palabras por producto'),
    tabla(
      ['Palabra', 'A dónde lleva', 'Estado del bot'],
      [
        ['ACERO', 'Especialización en Acero', 'ya existe en el feed'],
        ['BIM / IA', 'Máster', 'ya existe'],
        ['ZAPATA', 'Calculadora', 'ya existe y probado'],
        ['NIVEL', 'Test de Nivel BIM', 'HAY QUE CREARLO'],
        ['CUPO', 'Aviso de cupos de ACERO', 'HAY QUE CREARLO'],
      ], [18, 46, 36]),

    aviso('Lo único que hay que montar',
      ['Que el workflow del bot dispare también con MENSAJES DIRECTOS, no solo con comentarios. En GoHighLevel es el mismo workflow con un disparador más: Instagram DM / Facebook Message → contiene la palabra.',
       'Hay que confirmarlo en la cuenta ANTES de anunciarlo en una historia. Si el bot no está montado, la historia promete algo que no llega.'], 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── 3 · LA SEMANA ──────────────────────────────────────────
    h1('La semana tipo corregida'),

    tabla(
      ['Día', 'Qué se publica', 'Cambio'],
      [
        ['Lunes', 'pieza del día', '—'],
        ['Martes', 'detrás de cámara', '—'],
        ['Miércoles', 'pieza del día', '—'],
        ['JUEVES', 'SECUENCIA DE VENTA (rotan las 3 de abajo)', '🆕 nuevo'],
        ['Viernes', 'pieza del día + republicar respuestas', '—'],
        ['Sábado', 'testimonio + sticker de intención', 'ajustado'],
        ['Domingo', 'nada', '—'],
      ], [16, 60, 24]),

    p('El sábado deja de ser «sin vender». Sigue sin llevar precio, pero el sticker cambia de «¿Te ves aquí?» a uno que separe al curioso del interesado.'),

    // ── 4 · LAS SECUENCIAS ─────────────────────────────────────
    h1('Las tres secuencias de venta'),
    p('Rotan cada jueves. Ninguna dice un precio. Ninguna dice «inscríbete».'),

    h2('🔩 VENTA A · La objeción (ACERO)'),
    p('Se usa cuando la gente ya vio contenido técnico de acero y no ha escrito.'),
    tabla(
      ['#', 'Qué se ve', 'Texto en pantalla', 'Sticker'],
      [
        ['1', 'Tú a cámara, sin producción', '«Me escribieron esto la semana pasada:»', 'ninguno'],
        ['2', 'Captura real de un DM, tapando el nombre', '«Me interesa, pero no tengo tiempo»', 'ninguno'],
        ['3', 'Texto sobre azul', '«Es 100 % asincrónico. No hay horario al que llegar tarde. El acceso no caduca.»', 'ENCUESTA: «¿Ese era tu freno?» → Sí / El mío es otro'],
        ['4', 'Tú a cámara', '«Si quieres el temario completo, respóndeme con la palabra ACERO.»', '«Responde con ACERO» → lo agarra el bot'],
      ], [5, 22, 41, 32]),

    h2('🎯 VENTA B · El espejo (Máster)'),
    p('Que la persona se reconozca en el problema antes de que le hables del producto.'),
    tabla(
      ['#', 'Qué se ve', 'Texto en pantalla', 'Sticker'],
      [
        ['1', 'Texto sobre azul', '«Llevas 3 años modelando bien. Y sigues esperando a que te digan qué modelar.»', 'ninguno'],
        ['2', 'Los 4 niveles en pantalla', '«Modelador → Coordinador → BIM Manager → BIM + IA»', 'QUIZ: «¿Dónde crees que estás?»'],
        ['3', 'Texto sobre azul', '«El salto que más cuesta es del 1 al 2. Y no es de software: es dejar de ejecutar y empezar a decidir.»', 'ninguno'],
        ['4', 'Captura del test', '«Hay un test de 20 preguntas que te lo dice sin adornos.»', 'ENLACE al test + «o responde NIVEL»'],
      ], [5, 22, 41, 32]),
    pmix([['Cierra al test, no al Máster. '], 'Quien hace el test entra a la secuencia de correo y se vende solo. La historia no tiene que cerrar la venta.']),

    h2('⏳ VENTA C · Los cupos (ACERO)'),
    p('Una vez al mes. Es la única que crea urgencia, y la crea con lo que es verdad.'),
    tabla(
      ['#', 'Qué se ve', 'Texto en pantalla', 'Sticker'],
      [
        ['1', 'Los 4 logos: Robot · Advance Steel · Revit · certificaciones', '«4 programas. 4 meses. A tu ritmo.»', 'ninguno'],
        ['2', 'El número enorme sobre azul', '«Esta cohorte son 10 cupos. Quedan 8.»', 'CUENTA REGRESIVA al cierre de inscripciones'],
        ['3', 'Tú a cámara', '«Si quieres el detalle, respóndeme con la palabra CUPO.»', '«Responde con CUPO» → lo agarra el bot'],
      ], [5, 26, 37, 32]),

    aviso('Las dos reglas duras de esta secuencia',
      ['1) El número tiene que ser el de verdad. 10 cupos, 2 vendidos, quedan 8 (confirmado el 14-ago). Se actualiza cada vez que se publica. Esta gente vuelve al mes siguiente: un contador falso se descubre solo, y con él se cae la credibilidad — que es lo único que vende un programa de $199 por internet.',
       '2) La cuenta regresiva va al CIERRE de inscripciones de esta cohorte, no a la apertura. La cohorte abre todos los meses, así que «abre pronto» no aprieta nada. Lo que aprieta es que estos 8 cupos se acaban.'], 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── 5 · DM ─────────────────────────────────────────────────
    h1('Los DM, para cuando sí respondas a mano'),

    p('Con el arreglo de arriba ya no hace falta responder para que la estrategia funcione. Pero cuando tengas tiempo y quieras escribirle a alguien, estos son los guiones. Se copian, se les cambia el nombre y se mandan.'),

    aviso('Las tres reglas del DM',
      ['1) Siempre con el nombre de la persona. Un DM sin nombre se lee como bot.',
       '2) Nunca precio del Máster. Si preguntan cuánto cuesta, se pasa a llamada. El precio de ACERO sí se puede decir.',
       '3) Una pregunta al final, siempre. Un DM que no pregunta se muere ahí.'], 'nota'),

    h3('DM 1 · Votó la opción «que le falta algo» en una encuesta'),
    p('Ej.: «Ni sabía», «Me ha pasado», «Nunca», «Team a mano». Acaba de admitir un hueco.'),
    codigo(['¡Hola [NOMBRE]! Vi que votaste «[SU RESPUESTA]» en la historia 👀',
            '',
            'Te cuento en corto por qué importa: [UNA FRASE con la',
            'consecuencia real del hueco que admitió].',
            '',
            '¿Te pasa seguido o fue una vez?']),

    h3('DM 2 · Falló un quiz'),
    p('El lead más calificado, según la propia guía: se equivocó en un dato técnico y lo sabe.'),
    codigo(['¡Hola [NOMBRE]! El quiz de la historia tenía trampa 😄 la',
            'respuesta era [RESPUESTA] y casi todo el mundo falló, así',
            'que no eres tú.',
            '',
            'Te explico por qué: [2 O 3 LÍNEAS, técnicas de verdad].',
            '',
            '¿En qué tipo de proyecto te estás encontrando esto?']),
    pmix([['Nunca hagas sentir tonto a nadie. '], '«Casi todo el mundo falló» es lo que convierte la vergüenza en curiosidad.']),

    h3('DM 3 · Escribió en la caja de preguntas'),
    codigo(['¡Hola [NOMBRE]! Me preguntaste «[SU PREGUNTA]».',
            '',
            '[RESPUESTA REAL, útil, sin vender nada. Que se note que le',
            'dedicaste tiempo.]',
            '',
            '¿Te sirve así o quieres que lo aterrice a tu caso?']),
    pmix(['Ese ', ['«¿lo aterrizo a tu caso?»'], ' es la puerta. Quien dice que sí está pidiendo una conversación de venta sin saberlo.']),

    h3('DM 4 · Respondió a una historia de venta'),
    codigo(['¡Hola [NOMBRE]! Gracias por responder 🙌',
            '',
            'Antes de contarte nada: ¿en qué estás trabajando ahora y qué',
            'te gustaría poder hacer que hoy no puedes?',
            '',
            'Te lo pregunto porque según lo que me digas te sirve una cosa',
            'u otra — y a veces la respuesta es que todavía no es tu',
            'momento. Prefiero decírtelo a venderte algo que no necesitas.']),

    h3('DM 5 · Preguntó el precio'),
    codigo(['¡Hola [NOMBRE]! Te lo cuento con calma en 30 minutos, que así',
            'te digo también si te conviene o no según dónde estés 👇',
            '',
            'https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe',
            '',
            'Si prefieres por aquí, dime primero en qué estás trabajando.']),
    pmix([['Excepción — ACERO: '], 'ahí el precio SÍ se puede decir por DM ($499,99 → $199,99), porque es un producto de decisión rápida. El Máster no: siempre llamada.']),

    // ── 6 · MEDIR ──────────────────────────────────────────────
    h1('Qué se mide'),
    p('La guía ya lo dice bien: no son las vistas, son las respuestas y los DM. Una historia con 300 vistas y 12 respuestas vale más que una de 3.000 y ninguna.'),
    p('Se añade una sola columna, porque es la que dice si esto sirvió:'),
    tabla(
      ['Semana', 'Respuestas con palabra clave', 'Entraron al bot', 'Llamadas agendadas'],
      [['', '', '', ''], ['', '', '', ''], ['', '', '', '']], [16, 34, 25, 25]),
    pmix([['«Respuestas con palabra clave» es la columna nueva. '],
      'Es la que mide si el cambio de mecánica funcionó, y no depende de que nadie se acuerde de anotar nada: sale del CRM.']),

    h1('Lo que hay que decidir'),
    tabla(['Qué', 'Quién'],
      [
        ['Aprobar el jueves como slot de venta', 'Dayana'],
        ['Montar el disparador de DM en el bot (palabras NIVEL y CUPO)', 'Equipo técnico'],
        ['Confirmar los cupos que quedan cada vez que se publique', 'Dayana'],
        ['Autorización de un alumno para el testimonio del sábado', 'Dayana'],
      ], [72, 28]),

    p('Sin el disparador de DM montado, la secuencia de cupos NO se publica: prometería algo que no llega.', { bold: true }),

  ])],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/home/user/meta-ads-dashboard.html/matriz-viral/entregables/3-Historias-que-venden.docx', b);
  console.log('OK doc historias');
});
