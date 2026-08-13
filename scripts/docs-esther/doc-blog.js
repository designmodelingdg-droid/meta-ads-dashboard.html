const { d, p, pmix, h1, h2, h3, bullet, paso, enlace, codigo, aviso, tabla,
  portada, numeracion, seccion, PageBreak, Paragraph } = require('./comun');
const { Document, Packer } = d;
const fs = require('fs');

const IMG = 'https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/recursos/img';
const RAW = 'https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/claude/remote-control-setup-GUe3f';

const doc = new Document({
  creator: 'Design Modeling Academy',
  title: 'Publicar el articulo de IA en Revit',
  description: 'Paso a paso para publicar el articulo del blog y actualizar el hub de recursos',
  numbering: numeracion,
  sections: [seccion([

    ...portada(
      ['Publicar el artículo', '«La IA de Revit, paso a paso»'],
      'Blog + hub de recursos · paso a paso completo',
      '🔴  URGENTE',
      'B3261E',
      ['Para: Esther', 'De: Dayana · Design Modeling Academy',
       'Fecha: 13 de agosto de 2026',
       'Tiempo estimado: 20–30 minutos']),

    new Paragraph({ children: [new PageBreak()] }),

    // ── POR QUÉ ────────────────────────────────────────────────
    h1('Por qué esto es urgente'),

    p('El lunes 4 de agosto publicamos un carrusel sobre las funciones de IA de Revit. Ese post cierra prometiendo, textualmente:'),
    codigo(['«Comenta BIM o IA y te mando cómo activarlas paso a paso.»']),
    pmix(['Ese paso a paso ', ['no existía'], '. Hay gente que ya comentó esperándolo, y todavía no ha recibido nada.']),

    p('Hay un segundo motivo, más delicado. Al ir a escribir ese paso a paso lo verificamos contra la documentación oficial de Autodesk, y las tres funciones que prometía el carrusel no resistieron la comprobación:'),

    tabla(
      ['Lo que decía el post', 'La realidad'],
      [
        ['«Autodesk AI Assist genera detalles constructivos»', 'No existe. Ninguna función así en Revit.'],
        ['«Detecta y RESUELVE los choques»', 'Interference Check los detecta. Resolverlos, no.'],
        ['«Le das los m² y te da 3 layouts»', 'Existe (Generative Design), pero no funciona así y exige AEC Collection.'],
      ], [50, 50]),

    p('Y Autodesk dice, textual: «A partir de la versión Revit 2026, no hay funciones impulsadas por IA». Lo que sí es IA de verdad —el Autodesk Assistant— solo está en Revit 2027.', { after: 200 }),

    aviso('Lo importante: no hay que borrar el post.',
      ['El post tiene alcance y comentarios, y borrarlo se nota más que corregirlo. El artículo que vas a publicar es más honesto que el post, y eso juega a nuestro favor: vendemos formación técnica, y la credibilidad es el producto.',
       'El artículo ya está escrito y verificado, con las 7 fuentes de Autodesk enlazadas. No hay que redactar ni decidir nada — solo publicarlo.'], 'nota'),

    // ── LO QUE YA ESTÁ HECHO ───────────────────────────────────
    h1('Lo que ya está hecho (no lo rehagas)'),

    tabla(
      ['Qué', 'Estado'],
      [
        ['El artículo completo, en HTML', '✅ Listo para pegar'],
        ['Las 4 imágenes, con el texto en español dentro', '✅ Generadas y alojadas'],
        ['La tarjeta del hub de recursos, en primer lugar', '✅ En el archivo regenerado'],
        ['El guion del carrusel corregido en la matriz', '✅ Hecho'],
        ['El texto de los DM de respuesta', '✅ Al final de este documento'],
      ], [70, 30]),

    aviso('Las imágenes NO hay que subirlas a ningún lado.',
      'Ya están alojadas de forma permanente y el artículo las trae puestas en su sitio. No hace falta descargarlas, ni subirlas a la biblioteca de GHL, ni pasarlas por Canva: el texto ya va dentro de cada imagen y está bien escrito.', 'nota'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 1 ─────────────────────────────────────────────────
    h1('Paso 1 · Publicar el artículo en el blog'),

    h2('1.1 · Abre el archivo con el artículo'),
    p('Es un archivo HTML. Ábrelo con el Bloc de notas, TextEdit o el navegador — cualquier cosa que muestre el texto:'),
    enlace(`${RAW}/matriz-viral/guiones/blog-ia-revit-LISTO-PARA-PEGAR.html`),
    p('Selecciona todo (Ctrl+A o Cmd+A) y copia. Es un solo bloque, no hay que armar nada.'),

    h2('1.2 · Crea la entrada'),
    paso('En GoHighLevel, entra a Sites → Blogs → New Post.'),
    paso('Cambia el editor a modo HTML o «Code». Esto es importante: si lo pegas en el modo visual normal, el HTML se ve como texto plano con las etiquetas a la vista.'),
    paso('Pega todo lo que copiaste.'),

    h2('1.3 · Rellena los campos, exactamente así'),

    tabla(
      ['Campo', 'Qué poner'],
      [
        ['Título', 'La IA de Revit, paso a paso: qué trae de verdad y cómo activarlo'],
        ['URL / slug', 'ia-en-revit-paso-a-paso-como-activarla'],
        ['Meta descripción', 'Qué funciones de IA trae Revit realmente, en qué versión, y el paso a paso para activarlas. Sin humo: también lo que no hace.'],
        ['Categoría', 'BIM + IA'],
        ['Autor', 'Design Modeling Academy'],
      ], [26, 74]),

    aviso('El slug tiene que ser EXACTO.',
      ['Escríbelo tal cual: ia-en-revit-paso-a-paso-como-activarla',
       'La tarjeta del hub de recursos y los mensajes automáticos de Instagram ya apuntan a esa dirección. Si el slug cambia aunque sea una letra, esos enlaces quedan rotos y la gente llega a una página que no existe.'], 'alerta'),

    h2('1.4 · La imagen destacada'),
    p('En «Featured image» / imagen destacada, pega esta dirección:'),
    enlace(`${IMG}/ia-revit-portada.png`),
    p('Si el campo solo acepta subir un archivo, abre esa dirección en el navegador, guarda la imagen y súbela.'),

    h2('1.5 · Publica y guarda la dirección'),
    paso('Dale a Publicar.'),
    paso('Abre el post ya publicado y comprueba tres cosas: que se ven las 4 imágenes, que los títulos salen como títulos (no como texto suelto), y que los enlaces de Autodesk abren en pestaña nueva.'),
    paso('Copia la dirección final. Debería ser: funnel.dgdesignmodeling.com/post/ia-en-revit-paso-a-paso-como-activarla'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 2 ─────────────────────────────────────────────────
    h1('Paso 2 · Actualizar el hub de recursos'),

    p('El artículo tiene que aparecer el PRIMERO de la sección «Del blog». La persona que llega desde el mensaje de Instagram tiene que verlo de entrada, sin buscar.'),
    p('Ya está hecho en el archivo — solo hay que pegarlo:'),

    paso('Abre este archivo y copia todo su contenido:'),
    enlace(`${RAW}/recursos/ghl-recursos.html`),
    paso('En GoHighLevel: Sites → la página /recursos → el bloque de Custom Code.'),
    paso('Borra lo que hay dentro y pega lo nuevo. Guarda y publica.'),

    aviso('Cómo comprobar que quedó bien',
      ['Abre funnel.dgdesignmodeling.com/recursos en el celular.',
       'En la sección «Del blog» tienen que salir 4 tarjetas, y la PRIMERA debe ser «La IA de Revit, paso a paso». Al tocarla, tiene que abrir el artículo que acabas de publicar.',
       'Si la tarjeta no aparece, casi siempre es porque el bloque de Custom Code quedó a medias: vuelve a pegarlo completo.'], 'nota'),

    // ── PASO 3 ─────────────────────────────────────────────────
    h1('Paso 3 · Responder a los que ya comentaron'),

    p('Esta es la parte que cierra el círculo. Hay gente esperando desde el 4 de agosto.'),

    h2('3.1 · En la publicación del 4 de agosto'),
    bullet('Responde a cada comentario con el enlace del artículo.'),
    bullet('Fija un comentario nuestro con este texto:'),
    codigo(['Ampliamos esto en el blog con el paso a paso real y una',
            'aclaración importante sobre en qué versión de Revit está',
            'cada función → [enlace del artículo]']),
    bullet('NO borres el post ni los comentarios.'),

    h2('3.2 · El mensaje directo (DM) para quien comentó «BIM» o «IA»'),
    p('Este es el mensaje que se les debe enviar. Reemplaza [ENLACE] por la dirección del artículo:'),

    codigo([
      '¡Hola! 👋 Aquí está lo que te prometí: el paso a paso',
      'completo de las funciones de IA de Revit 👇',
      '',
      '📄 [ENLACE]',
      '',
      'Te aviso de algo antes de que lo abras, porque en el post no',
      'cabía: Autodesk dice en su propia documentación que HASTA',
      'REVIT 2026 no hay funciones de IA. Lo que existe llegó con',
      'la 2027.',
      '',
      'En el artículo está el paso a paso real de lo que sí funciona',
      '(con las fuentes de Autodesk enlazadas) y también lo que Revit',
      'todavía NO hace, aunque se diga por ahí.',
      '',
      'Y si te sirve, aquí están todas nuestras herramientas gratis',
      'en un solo sitio — calculadora de zapatas, test de nivel BIM,',
      'ebooks y más:',
      '🎁 https://funnel.dgdesignmodeling.com/recursos',
    ]),

    p('Y este otro, entre 3 y 4 horas después:'),

    codigo([
      '¿Alcanzaste a leerlo? 😄',
      '',
      'Te hago la pregunta que me interesa de verdad: ¿en qué versión',
      'de Revit estás trabajando?',
      '',
      'Te lo pregunto porque es lo que decide qué puedes usar hoy y',
      'qué no. Y según lo que me digas, te apunto por dónde empezar. 👇',
    ]),

    aviso('El segundo mensaje tiene que salir dentro de las 24 horas.',
      'Instagram y Facebook solo dejan escribirle a una persona durante las 24 horas siguientes a que ella nos escribió. Pasado ese plazo el mensaje no se entrega. Por eso va a las 3–4 horas y no al día siguiente.', 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PENDIENTE ──────────────────────────────────────────────
    h1('Lo único que queda pendiente'),

    p('Dentro del artículo, en la sección del Autodesk Assistant, falta una captura de pantalla del panel abierto en Revit 2027.'),

    pmix([['Esa imagen no se puede generar con IA, y es a propósito: '],
      'es lo único del artículo que la gente va a intentar reproducir en su pantalla. Una interfaz inventada sería exactamente el error que este artículo viene a corregir.']),

    bullet('Si alguien del equipo tiene Revit 2027: que tome dos capturas — el icono del Assistant en la barra de título, y el panel abierto con el Tech Preview encendido en Settings.'),
    bullet('Si nadie lo tiene: el artículo funciona perfectamente sin esa captura. Se publica igual y se añade después.'),

    p('No esperes por esto para publicar.', { bold: true }),

    // ── CHECKLIST ──────────────────────────────────────────────
    h1('Lista de comprobación final'),

    tabla(
      ['✓', 'Qué comprobar'],
      [
        ['☐', 'El artículo está publicado y el slug es exactamente ia-en-revit-paso-a-paso-como-activarla'],
        ['☐', 'Se ven las 4 imágenes dentro del artículo'],
        ['☐', 'La imagen destacada aparece al compartir el enlace por WhatsApp'],
        ['☐', 'En /recursos, «La IA de Revit» es la PRIMERA tarjeta de «Del blog»'],
        ['☐', 'Esa tarjeta abre el artículo'],
        ['☐', 'Se respondieron los comentarios del post del 4 de agosto'],
        ['☐', 'Hay un comentario fijado con el enlace'],
        ['☐', 'Se enviaron los DM a quienes comentaron BIM o IA'],
      ], [8, 92]),

    h1('Si algo no cuadra'),
    p('Escríbele a Dayana antes de improvisar. Es preferible que el artículo salga un día después a que salga con un dato técnico mal: todo el valor de esta pieza es que lo que dice se puede verificar.'),

  ])],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/docs/1-URGENTE-Publicar-articulo-IA-Revit.docx', b);
  console.log('OK doc blog');
});
