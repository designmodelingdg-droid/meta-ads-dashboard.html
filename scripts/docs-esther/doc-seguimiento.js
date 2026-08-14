const { d, p, pmix, h1, h2, h3, bullet, paso, enlace, codigo, aviso, tabla,
  portada, numeracion, seccion, PageBreak, Paragraph } = require('./comun');
const { Document, Packer } = d;
const fs = require('fs');

const RAW = 'https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/claude/remote-control-setup-GUe3f/matriz-viral/seguimiento';

const doc = new Document({
  creator: 'Design Modeling Academy',
  title: 'Montar el seguimiento por correo de los lead magnets',
  description: 'Paso a paso para crear los workflows de seguimiento en GoHighLevel',
  numbering: numeracion,
  sections: [seccion([

    ...portada(
      ['Seguimiento por correo', 'de los lead magnets'],
      'Montar los 3 workflows en GoHighLevel · paso a paso',
      '🟡  PRÓXIMA SEMANA',
      'CA7520',
      ['Para: Ester Alvarez', 'De: Dayana · Design Modeling Academy',
       'Fecha: 13 de agosto de 2026',
       'Tiempo estimado: 3–4 horas de montaje + 9 días de encendido escalonado']),

    new Paragraph({ children: [new PageBreak()] }),

    // ── EL PROBLEMA ────────────────────────────────────────────
    h1('Qué estamos resolviendo'),

    pmix(['Tenemos unos ', ['2.300 contactos'], ' que llegaron por nuestros recursos gratuitos (la calculadora de zapatas, el test de nivel BIM, los ebooks) y ', ['a ninguno se le está haciendo nada'], '.']),

    p('El flujo hoy termina cuando la persona descarga. No hay correo de bienvenida, no hay seguimiento, y la oportunidad se queda parada en el pipeline sin siguiente paso. Lo único que existe es la cadena de 3 mensajes directos del bot de Instagram, que se muere a las 24 horas porque Meta cierra la ventana.'),

    p('WhatsApp masivo está descartado: bloquean la línea. El correo es el puente.'),

    h2('Cómo queda la cadena completa'),
    codigo([
      'La persona comenta "ZAPATA" en Instagram',
      '   ↓  segundos',
      'El bot responde el comentario + le manda el enlace por DM',
      '   ↓  +3-4 horas',
      'DM 2',
      '   ↓  +1 día',
      'DM 3        ← aquí se cierra la ventana de 24h de Meta',
      '   ↓  +2 días',
      'CORREO 1  "Por si se te perdió entre los mensajes"',
      '   ↓',
      'Correos 2 al 7 · hasta el día 16',
    ]),

    p('Lo nuevo que vas a montar es todo lo que va del CORREO 1 en adelante.'),

    // ── DÓNDE ESTÁN ────────────────────────────────────────────
    h1('Dónde están los leads (no crees nada nuevo)'),

    p('Ya existen y ya están en un pipeline que funciona. Hay que engancharse a lo que hay:'),

    tabla(
      ['Qué', 'Dónde'],
      [
        ['Pipeline', 'INSTAGRAM – FACEBOOK  ·  qjXIsYXjqdWbge7bZCdT'],
        ['Etapa', 'NUEVO LEAD MAGNET  ·  eaa5097a-8317-4519-aae4-094471d8b26a'],
        ['Cuántos hay ahí', '334 oportunidades abiertas'],
      ], [26, 74]),

    h2('Qué hay exactamente en esa etapa'),

    tabla(
      ['Fuente', 'Cuántos', 'Nombre de la oportunidad', 'Va a'],
      [
        ['Bot Zapatas IG/FB', '106', 'Lead Zapatas - <usuario>', 'Secuencia A'],
        ['Calculadora de Zapatas - Registro', '78', 'nombre de la persona', 'Secuencia A'],
        ['contacto-instagram', '27', 'Lead Test BIM - <usuario>', 'Secuencia B'],
        ['Test Nivel  IG/FB', '10', 'Lead Test Nivel - <usuario>', 'Secuencia B'],
        ['(sin fuente)', '107', 'nombre de la persona', 'hay que mirarlos'],
      ], [34, 12, 33, 21]),

    new Paragraph({ children: [new PageBreak()] }),

    // ── LAS TRAMPAS ────────────────────────────────────────────
    h1('⚠️ Las cuatro trampas de este pipeline'),

    p('Cualquiera de estas rompe el montaje sin dar ningún error. Léelas antes de tocar nada.'),

    h3('1 · «Test Nivel  IG/FB» lleva DOS espacios'),
    p('Entre «Nivel» e «IG/FB» hay dos espacios, no uno. Un filtro escrito con un solo espacio no encuentra a nadie, y parece que no hay leads del test.'),
    pmix([['Solución: '], 'no filtres por esa fuente. Filtra por el nombre de la oportunidad.']),

    h3('2 · El test entró con dos nombres distintos'),
    p('27 se llaman «Lead Test BIM» y 10 «Lead Test Nivel». Si filtras por uno, pierdes los otros.'),
    pmix([['Solución: '], 'filtra por «contiene Test», a secas. Así entran los dos.']),

    h3('3 · 107 oportunidades no tienen fuente'),
    p('Es casi un tercio de la etapa. Si el filtro es solo por fuente, se quedan fuera.'),

    h3('4 · Unos 98 leads NO tienen correo'),
    pmix(['Entraron por el bot de Instagram y solo dejaron su usuario — por eso hay oportunidades llamadas «Lead Zapatas - Mauricio_granados74». De los 297 contactos de zapatas, solo ', ['199 tienen correo'], '.']),
    pmix([['Solución: '], 'un filtro de «¿tiene correo?» al principio de cada workflow. Sin eso se atascan dentro y no se ve.']),

    aviso('Estos 98 son dinero ya pagado.',
      ['Son leads que costaron pauta y hoy están muertos en el CRM porque nadie les pidió el correo. En el paso 3 hay un mensaje escrito para pedírselo. Recuperar aunque sea un tercio son unas 30 personas más, sin gastar un dólar.'], 'nota'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── LOS ARCHIVOS ───────────────────────────────────────────
    h1('Los archivos que necesitas'),

    p('Todo el texto de los correos está escrito. No hay que redactar nada.'),

    h3('La guía de montaje, clic a clic — empieza por aquí'),
    enlace(`${RAW}/MONTAJE-GHL.md`),
    h3('El contexto y las reglas'),
    enlace(`${RAW}/ESTRATEGIA.md`),
    h3('La plantilla de correo'),
    enlace(`${RAW}/plantilla-email.html`),
    h3('El texto de las tres secuencias'),
    enlace(`${RAW}/secuencia-A-zapatas-acero.md`),
    enlace(`${RAW}/secuencia-B-test-master.md`),
    enlace(`${RAW}/secuencia-C-reactivacion.md`),

    // ── PASO 0 ─────────────────────────────────────────────────
    h1('Paso 0 · Antes de tocar nada'),

    paso('Settings → Email Services: comprueba que SPF, DKIM y DMARC están en verde. Ya lo estaban, pero se mira igual.'),
    paso('Contacts → filtra por Email Status = Bounced o Unsubscribed y márcalos para excluirlos. Cada correo a una dirección muerta cuenta en contra.'),
    paso('Settings → Tags → crea estas siete etiquetas:'),
    codigo(['seq-zapatas-acero      seq-test-master      seq-reactivacion',
            'seq-completada         lead-caliente        email-frio',
            'respondio-correo       sin-correo-solo-dm']),
    paso('Opportunities → Pipelines: comprueba que existen estas etapas, en este orden: Nuevo lead → En nutrición → Interesado → Llamada agendada. Si tienen otro nombre NO las renombres (rompería reportes viejos): anota los nombres reales y usa esos.'),

    // ── PASO 1 ─────────────────────────────────────────────────
    h1('Paso 1 · Guardar la plantilla de correo'),

    paso('Marketing → Emails → New → Code / HTML Editor.'),
    paso('Pega el contenido completo de plantilla-email.html.'),
    paso('Guárdala con el nombre: DMA · Base secuencias'),
    paso('Comprueba que pesa menos de 102 KB.'),
    paso('Mándate una prueba y ábrela en Gmail DEL CELULAR. Es donde Gmail recorta y donde se ve si el botón sobrevive.'),

    aviso('No uses la plantilla de las campañas normales.',
      'La que usamos para los correos mensuales pesa unos 860 KB porque lleva las imágenes incrustadas. Gmail recorta cualquier correo que pase de 102 KB y se come justo el botón. Sirve para un envío suelto; no para una secuencia de 7 correos.', 'alerta'),

    p('Para cada correo: duplica esta plantilla y reemplaza solo el título, el cuerpo, el texto del botón, el enlace y la posdata. Nómbralos así para no perderte:'),
    codigo(['A1-web  A1-bot  A2  A3  A4  A5  A6  A7',
            'B1  B2-bajo  B2-alto  B2-neutro  B3  B4  B5',
            'C1  C2  C3']),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 2 ─────────────────────────────────────────────────
    h1('Paso 2 · Workflow A — Zapatas → Especialización en ACERO'),

    p('Automation → Workflows → New → Start from Scratch. Nómbralo: SEQ-A · Zapatas → ACERO'),

    h2('El disparador'),
    p('Opportunity Stage Changed → pipeline INSTAGRAM – FACEBOOK → etapa NUEVO LEAD MAGNET.'),
    pmix([['NO uses una etiqueta como disparador. '], 'No encontraría a nadie: estos leads no llevan etiqueta, llevan etapa de pipeline.']),

    h2('Los tres filtros, en este orden exacto'),

    h3('Filtro 1 · ¿Tiene correo?'),
    codigo(['If/Else:  Email  is not empty',
            '   → NO  →  Add tag "sin-correo-solo-dm"  →  FIN, no sigue',
            '   → SÍ  →  continúa']),

    h3('Filtro 2 · ¿Vino del bot o del formulario?'),
    codigo(['If/Else:  Opportunity Source  contains  "IG/FB"',
            '   → SÍ (vino del bot)        →  WAIT 2 días  →  correo A1-bot',
            '   → NO (vino del formulario) →  sin espera   →  correo A1-web']),
    p('Esto evita que la persona reciba el mensaje del bot y el correo diciendo lo mismo en el mismo minuto. A los 2 días la cadena del bot ya terminó y el correo entra justo cuando el bot se quedó sin poder escribir.'),

    h3('Filtro 3 · ¿Es de zapatas?'),
    codigo(['If/Else, cualquiera de estas (OR):',
            '   Opportunity Name    contains  "Zapatas"',
            '   Opportunity Source  contains  "Zapatas"',
            '   Contact Tag         is        lead-calculadora-zapatas',
            '   → SÍ  →  sigue la secuencia A',
            '   → NO  →  FIN (lo recoge el workflow B)']),

    h2('Los pasos de la secuencia'),

    tabla(
      ['#', 'Acción', 'Configuración'],
      [
        ['1', 'Add Tag', 'seq-zapatas-acero'],
        ['2', 'Update Opportunity', 'etapa → En nutrición'],
        ['3', 'Send Email', 'A1-bot o A1-web, según el filtro 2'],
        ['4', 'Wait', '2 días · entre 9:00 y 11:00 hora del contacto'],
        ['5', 'Send Email', 'A2 · el error #1 al dimensionar una zapata'],
        ['6', 'Wait', '2 días · misma franja'],
        ['7', 'Send Email', 'A3 · el puente'],
        ['8', 'Wait', '3 días'],
        ['9', 'Send Email', 'A4 · la oferta de ACERO'],
        ['10', 'Wait', '2 días'],
        ['11', 'Send Email', 'A5 · «no tengo tiempo»'],
        ['12', 'Wait', '3 días'],
        ['13', 'Send Email', 'A6 · testimonios'],
        ['14', 'Wait', '2 días'],
        ['15', 'Send Email', 'A7 · el cierre'],
        ['16', 'Add Tag', 'seq-completada'],
        ['17', 'Remove Tag', 'seq-zapatas-acero'],
      ], [7, 27, 66]),

    aviso('La franja horaria no es opcional.',
      'En cada «Wait» activa «esperar hasta una franja concreta» y pon 9:00–11:00. Sin eso los correos salen de madrugada y las aperturas se desploman.', 'alerta'),

    h2('Las cuatro salidas'),
    p('Se configuran en los ajustes del workflow (Goals / Events), no como pasos:'),

    tabla(
      ['Cuando pasa esto', 'El workflow hace'],
      [
        ['Responde un correo', 'Etiqueta respondio-correo → lo saca del workflow → avisa a Dayana'],
        ['Agenda una llamada', 'Mueve la oportunidad a «Llamada agendada» → lo saca'],
        ['Se da de baja', 'Lo saca del workflow'],
        ['Compra', 'Lo saca del workflow'],
      ], [32, 68]),

    p('Que responda es lo que queremos: ahí entra una persona.', { bold: true }),

    h2('La marca de «Interesado»'),
    p('En el correo A4, sobre el botón principal, añade la condición: si hace clic en el enlace → etiqueta lead-caliente + mueve la oportunidad a «Interesado».'),

    h2('Dos ajustes del workflow'),
    bullet('«Allow re-entry»: NO. Que nadie reciba la secuencia dos veces.'),
    bullet('«Stop on response»: SÍ.'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 3 ─────────────────────────────────────────────────
    h1('Paso 3 · Los que no tienen correo (unos 98)'),

    p('No es un caso raro: es un tercio de la etapa. A esos no se les puede mandar la secuencia porque no hay a dónde. Lo que sí se puede hacer, y hoy no se hace:'),

    paso('Quedan con la etiqueta sin-correo-solo-dm (la pone el filtro 1).'),
    paso('Se les manda un mensaje directo pidiendo el correo, si la ventana de 24 horas sigue abierta:'),
    codigo(['¡Hola! 👋 Te mandé la calculadora por aquí, pero se me queda',
            'corta la conversación por DM.',
            '',
            '¿Me pasas tu correo? Te mando el paso a paso completo de',
            'cómo usarla sin que se te pierda entre los mensajes, y de',
            'paso te llegan las herramientas nuevas cuando salen. Nada',
            'de spam. 🙌']),
    paso('Quien conteste con su correo: lo guardas en su ficha de contacto y entra a la secuencia A automáticamente (el filtro 1 deja de bloquearlo).'),

    // ── PASO 4 ─────────────────────────────────────────────────
    h1('Paso 4 · Workflow B — Test de Nivel → Máster'),

    p('Nómbralo: SEQ-B · Test de Nivel → Máster. Mismo disparador que el A: la etapa NUEVO LEAD MAGNET.'),

    h2('Los filtros'),
    codigo(['Filtro 1:  Email is not empty  →  NO: tag sin-correo-solo-dm y FIN',
            '',
            'Filtro 2, cualquiera de estas (OR):',
            '   Opportunity Name    contains  "Test"',
            '   Opportunity Source  contains  "Test Nivel"',
            '   Contact Tag         is        lead-test-nivel-bim',
            '   → SÍ  →  sigue la secuencia B',
            '   → NO  →  FIN']),

    h2('Los pasos'),

    tabla(
      ['#', 'Acción', 'Configuración'],
      [
        ['1', 'Add Tag', 'seq-test-master'],
        ['2', 'Update Opportunity', 'etapa → En nutrición'],
        ['3', 'Send Email', 'B1 · la entrega'],
        ['4', 'Wait', '2 días · 9:00–11:00'],
        ['5', 'If/Else', 'ver abajo: tres versiones del correo B2'],
        ['6', 'Wait', '3 días'],
        ['7', 'Send Email', 'B3 · el salto que más cuesta'],
        ['8', 'Wait', '3 días'],
        ['9', 'Send Email', 'B4 · microcredenciales'],
        ['10', 'Wait', '4 días'],
        ['11', 'Send Email', 'B5 · el cierre'],
        ['12', 'Add Tag', 'seq-completada'],
        ['13', 'Remove Tag', 'seq-test-master'],
      ], [7, 27, 66]),

    h2('El If/Else del paso 5'),
    p('Tres versiones del mismo correo, con distinta apertura. Están escritas en el archivo de la secuencia B:'),
    codigo(['¿Tiene etiqueta predijo-nivel-1 o predijo-nivel-2?  → B2-bajo',
            '¿Tiene etiqueta predijo-nivel-3 o predijo-nivel-4?  → B2-alto',
            'En cualquier otro caso                              → B2-neutro']),

    p('Interesado: clic en el botón del correo B3 → etiqueta lead-caliente + etapa «Interesado». Las salidas son las mismas cuatro del workflow A.'),

    aviso('En esta secuencia NO va el precio del Máster.',
      'Es una regla fija de la academia: el Máster nunca se cotiza por correo ni por chat. Se cierra siempre con una llamada. Si ves un precio del Máster en algún correo, es un error y hay que quitarlo. (El precio de la Especialización en ACERO sí va, en la secuencia A.)', 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 5 ─────────────────────────────────────────────────
    h1('Paso 5 · Workflow C — Reactivación de la lista dormida'),

    p('Son unos 2.000 contactos que llegaron por ebooks, guías y cursos gratuitos y llevan meses sin recibir nada.'),
    p('Nómbralo: SEQ-C · Reactivación lista dormida. Disparador: Tag Added → seq-reactivacion (esa etiqueta se pone a mano, en tandas).'),

    tabla(
      ['#', 'Acción', 'Configuración'],
      [
        ['1', 'Send Email', 'C1 · el hub de recursos'],
        ['2', 'Wait', '4 días · 9:00–11:00'],
        ['3', 'Send Email', 'C2 · el test como segmentador'],
        ['4', 'Wait', '4 días'],
        ['5', 'Send Email', 'C3 · cierre honesto'],
        ['6', 'Wait', '2 días'],
        ['7', 'If/Else', '¿abrió alguno de los tres?'],
        ['7a', '→ Sí', 'Add tag seq-completada'],
        ['7b', '→ No', 'Add tag email-frio + quitar de envíos'],
        ['8', 'Remove Tag', 'seq-reactivacion'],
      ], [7, 27, 66]),

    p('Salida extra, solo en este workflow: si le ponen la etiqueta lead-test-nivel-bim (o sea, hizo el test), sale de aquí. Pasa a la secuencia B y no debe recibir las dos.'),

    h2('Cómo cargar los contactos'),
    p('NO etiquetes los 2.000 de una vez. Contacts → filtra (ebook, guía, AI PRO, cursos, con correo válido) → ordena por fecha → añade la etiqueta seq-reactivacion así:'),

    tabla(
      ['Día', 'Cuántos'],
      [['1', '400'], ['2', '400'], ['3', '400'], ['4', '400'], ['5', 'los ~399 que queden']],
      [20, 80]),

    aviso('Por qué en tandas y no todos de golpe.',
      ['2.000 correos de una sentada a una lista que no recibe nada hace meses produce un pico de rebotes y de «marcar como spam» que los filtros leen como lista comprada. El dominio ya está calentado y funcionando — eso costó meses y se pierde en un día.',
       'Entre tanda y tanda mira el panel. Si los rebotes pasan del 2% o el spam del 0,1%, PARA y no cargues la siguiente.'], 'alerta'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 6 ─────────────────────────────────────────────────
    h1('Paso 6 · 🔑 Meter a los 334 que YA están ahí'),

    pmix([['Este es el punto de todo el montaje. '],
      'Los disparadores de arriba solo cogen a los que entren de ahora en adelante. Las 334 personas que llevan meses paradas en «NUEVO LEAD MAGNET» no se enrolan solas.']),

    p('Se hace desde el módulo de Oportunidades, no desde Contactos:'),

    paso('Opportunities → selecciona el pipeline INSTAGRAM – FACEBOOK.'),
    paso('Filtra por la etapa NUEVO LEAD MAGNET.'),
    paso('Primero los de zapatas: añade el filtro «Opportunity Name contiene Zapatas» O «Source contiene Zapatas» → selecciona todos → Add to Workflow → SEQ-A.'),
    paso('Después los del test: cambia el filtro a «Opportunity Name contiene Test» → selecciona todos → Add to Workflow → SEQ-B.'),
    paso('Los ~107 sin fuente son los que quedan al quitar los dos filtros anteriores. NO los metas a ciegas: ábrelos y mira de dónde vienen. Lo más probable es que sean del formulario de la calculadora, y entonces van a la A. Si no se puede saber, déjalos y pregúntale a Dayana.'),

    aviso('Cuenta antes de enrolar.',
      'Si un lead del test acaba en la secuencia de zapatas, recibe 7 correos sobre cimentaciones que no pidió. Eso no se puede deshacer.', 'alerta'),

    h2('También en tandas'),

    tabla(
      ['Día', 'Qué enrolar'],
      [
        ['1', '50 de zapatas — LOS MÁS RECIENTES PRIMERO'],
        ['2', 'mirar el panel; si está en verde, 100 más'],
        ['3', 'los ~34 restantes de zapatas'],
        ['4', 'los 37 del test, todos (son pocos)'],
      ], [15, 85]),

    p('Lo de «los más recientes primero» no es un detalle: quien descargó hace tres semanas abre el correo; quien descargó en mayo, no. Empezar por los que abren le enseña a Gmail que nuestros correos se leen, y eso protege todos los envíos siguientes.'),

    new Paragraph({ children: [new PageBreak()] }),

    // ── PASO 7 ─────────────────────────────────────────────────
    h1('Paso 7 · La prueba en seco (obligatoria)'),

    p('Antes de que esto toque a una sola persona real:'),

    paso('Duplica el workflow A y llámalo SEQ-A · PRUEBA.'),
    paso('Cambia TODOS los «Wait» a 2 minutos.'),
    paso('Mete el contacto de prueba: prueba+test@dgdesignmodeling.com'),
    paso('Mira llegar los 7 correos. En cada uno comprueba: que se ve bien en Gmail del celular, que el nombre sale bien (no vacío ni con llaves raras), que el botón lleva a donde debe, y que el enlace de baja funciona.'),
    paso('Comprueba que la oportunidad se movió de etapa sola.'),
    paso('Responde a uno de los correos y confirma que SALE del workflow.'),
    paso('Borra el workflow de prueba.'),

    // ── PASO 8 ─────────────────────────────────────────────────
    h1('Paso 8 · Encendido escalonado'),

    tabla(
      ['Cuándo', 'Qué'],
      [
        ['Día 1', 'Enciende SOLO la A (199 contactos)'],
        ['Día 3', 'Mira el panel. Si está en verde → enciende la B (26)'],
        ['Día 5', 'Si sigue verde → primera tanda de la C (400)'],
        ['Días 6-9', 'Una tanda diaria, mirando el panel cada día'],
      ], [18, 82]),

    h2('El panel: Marketing → Emails → Statistics'),

    tabla(
      ['Métrica', 'Meta', 'Si falla'],
      [
        ['Apertura', '≥ 25 %', 'reescribir los asuntos'],
        ['Clic', '≥ 3 %', 'el correo se lee pero no convence'],
        ['Rebote', '< 2 %', '🚨 parar y limpiar la lista'],
        ['Spam', '< 0,1 %', '🚨 PARAR TODO'],
        ['Baja', '< 0,5 %', 'normal en reactivación; vigilar'],
      ], [26, 20, 54]),

    // ── ERRORES ────────────────────────────────────────────────
    h1('Errores que ya conocemos'),

    bullet('Usar la plantilla pesada de las campañas. Gmail recorta a 102 KB y se come el botón.'),
    bullet('Dejar los «Wait» sin franja horaria. Salen de madrugada y la apertura se desploma.'),
    bullet('Dejar «re-entry» activado. La misma persona recibe la secuencia dos veces y se da de baja.'),
    bullet('Cargar los 2.000 de golpe. El dominio calentado se quema en un día.'),
    bullet('Prometer entrega por WhatsApp. Ese workflow no existe: todo se entrega por enlace, en el mismo correo.'),
    bullet('Mandar los 3 correos de la C a quien ya hizo el test. Por eso está la salida por etiqueta.'),
    bullet('Quitar el enlace de baja. Nunca. Es lo que protege el dominio.'),

    // ── CHECKLIST ──────────────────────────────────────────────
    h1('Lista de comprobación'),

    tabla(
      ['✓', 'Qué comprobar'],
      [
        ['☐', 'SPF, DKIM y DMARC en verde'],
        ['☐', 'Las 8 etiquetas creadas'],
        ['☐', 'Plantilla guardada y por debajo de 102 KB'],
        ['☐', 'Plantilla vista en Gmail del celular'],
        ['☐', 'Workflow A creado, con sus 3 filtros y sus 4 salidas'],
        ['☐', 'Workflow B creado, con el If/Else de los tres B2'],
        ['☐', 'Workflow C creado, con la salida por etiqueta del test'],
        ['☐', 'Todos los «Wait» con franja 9:00–11:00'],
        ['☐', '«Re-entry» desactivado en los tres'],
        ['☐', 'Prueba en seco hecha y workflow de prueba borrado'],
        ['☐', 'Los 334 enrolados, en tandas y contando antes'],
        ['☐', 'Panel revisado a las 48 horas'],
      ], [8, 92]),

    h1('Qué avisar cuando termines'),
    bullet('Qué workflows quedaron creados.'),
    bullet('Qué resultado dio la prueba en seco.'),
    bullet('Cuántas oportunidades enrolaste en cada secuencia.'),
    bullet('Cuántas quedaron con la etiqueta sin-correo-solo-dm.'),
    bullet('Cómo van rebotes y spam a las 48 horas.'),

    p('Si algo no cuadra, pregúntale a Dayana antes de improvisar. Un correo mal mandado a 300 personas no se puede recoger.', { bold: true }),

  ])],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/docs/2-Montar-seguimiento-por-correo-GHL.docx', b);
  console.log('OK doc seguimiento');
});
