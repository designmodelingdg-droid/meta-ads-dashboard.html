/* Paquete de montaje de los 3 lead magnets de septiembre, para Ester y Aylin.
 *
 * El texto vive aqui, no en los GUIA-MONTAJE.md. Si cambias uno de esos,
 * cambia tambien este archivo y vuelve a correrlo, o las versiones se separan.
 *
 *   node scripts/build_leadmagnets_docx.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
        PageBreak } = require('docx');
const ROOT=path.dirname(__dirname);
const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', RED='A33B2A', GREEN='1E7A55',
      WARN='FBF0DA', ALARM='F7E5E2', OK='E2F0E9', CODE='EEF2F6';

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:150},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:32,font:'Overpass'})]});
const H2=t=>new Paragraph({spacing:{before:270,after:100},
  children:[new TextRun({text:t,bold:true,color:ORANGE,size:25,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},children:trozos(t,o)});
const LI=t=>new Paragraph({bullet:{level:0},spacing:{after:70},children:trozos(t)});
const NUM=(n,t)=>new Paragraph({spacing:{after:70},indent:{left:340,hanging:340},
  children:[new TextRun({text:n+'. ',bold:true,color:NAVY,size:21,font:'Overpass'}),
            ...trozos(t)]});
const MONO=t=>new Paragraph({spacing:{before:100,after:130},
  shading:{type:ShadingType.CLEAR,fill:CODE},
  children:[new TextRun({text:t,size:17,font:'Consolas'})]});
const CAJA=(t,color,fill)=>new Paragraph({spacing:{before:150,after:170},
  shading:{type:ShadingType.CLEAR,fill},
  border:{left:{style:BorderStyle.SINGLE,size:20,color,space:10}},
  children:trozos(t,{color})});
const SALTO=()=>new Paragraph({children:[new PageBreak()]});

function trozos(t,o={}){
  const out=[]; const base={size:21,font:'Nunito',...(o.color?{color:o.color}:{}),...(o.run||{})};
  t.split(/(\*\*[^*]+\*\*)/).forEach(p=>{
    if(!p) return;
    const b=p.startsWith('**')&&p.endsWith('**');
    out.push(new TextRun({text:b?p.slice(2,-2):p,bold:b,...base}));
  });
  return out;
}
const celda=(t,{w=0,fill=null}={})=>new TableCell({width:{size:w,type:WidthType.DXA},
  ...(fill?{shading:{type:ShadingType.CLEAR,fill}}:{}),
  margins:{top:90,bottom:90,left:130,right:130},
  children:[new Paragraph({children:trozos(t,{run:{size:19}})})]});
const tabla=(head,filas,anchos)=>new Table({columnWidths:anchos,width:{size:9200,type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:anchos[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      margins:{top:90,bottom:90,left:130,right:130},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:'FFFFFF',size:19,font:'Overpass'})]})]}))}),
    ...filas.map(f=>new TableRow({children:f.map((c,i)=>celda(c,{w:anchos[i]}))}))]});

const BASE='https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/';
const h=[]; const push=(...x)=>h.push(...x);

/* ── Portada ────────────────────────────────────────────────────────────── */
push(new Paragraph({spacing:{after:60},children:[new TextRun({text:'DESIGN MODELING ACADEMY',
  bold:true,color:ORANGE,size:19,font:'Overpass',characterSpacing:60})]}));
push(new Paragraph({spacing:{after:120},children:[new TextRun({
  text:'Los 3 lead magnets de septiembre',bold:true,color:NAVY,size:42,font:'Overpass'})]}));
push(P('Paquete de montaje para Ester y Aylin · 7 de septiembre de 2026',{run:{color:GREY,italics:true}}));
push(P('Los tres recursos están construidos, publicados y probados de punta a punta. Lo que falta es conectarlos a GoHighLevel — y en dos de ellos, una verificación que no se puede hacer desde el repositorio.'));

push(H1('Los tres, de un vistazo'));
push(tabla(['Recurso','Palabra','Estado'],[
  ['Revit + ChatGPT: resuelve errores con IA','GUIA','**Listo.** Solo falta el montaje en GHL.'],
  ['Memoria de cálculo + plantillas','MEMORIA','**Listo.** Gabriel dio el visto bueno el 8-sep. Solo falta el montaje.'],
  ['Pack starter de Dynamo','DYNAMO','**Listo.** Los 5 scripts se corrieron en Revit el 8-sep. Solo falta el montaje.'],
],[4000,1400,3800]));
push(CAJA('El de Revit + ChatGPT es el urgente: hay un reel el miércoles 9 cuyo CTA ya lo promete. Ese es el que hay que montar primero.',ORANGE,WARN));

push(H2('Los enlaces'));
push(P('Cada recurso tiene dos direcciones: **la landing**, que es la que se reparte, y **el contenido**, que solo se abre después de registrarse. El `?acceso=dm2026` del final es el atajo para el equipo: sirve para revisar sin llenar el formulario, y no se reparte.'));

push(P('**1 · Revit + ChatGPT**'));
push(MONO(BASE+'guia-revit-ia/\n'+BASE+'guia-revit-ia/guia.html?acceso=dm2026'));
push(P('**2 · Memoria de cálculo**'));
push(MONO(BASE+'memoria-calculo/\n'+BASE+'memoria-calculo/guia.html?acceso=dm2026\n'+
          BASE+'memoria-calculo/Plantilla-Memoria-de-Calculo-DMA.docx\n'+
          BASE+'memoria-calculo/Resumen-Verificaciones-DMA.xlsx'));
push(P('**3 · Pack de Dynamo**'));
push(MONO(BASE+'pack-dynamo/\n'+BASE+'pack-dynamo/guia.html?acceso=dm2026\n'+
          BASE+'pack-dynamo/Pack-Dynamo-Starter-DMA.zip'));

/* ── Lo que falta ───────────────────────────────────────────────────────── */
push(SALTO());
push(H1('Ya no queda nada bloqueado'));
push(P('Los tres recursos están construidos, publicados y **desbloqueados**. Esto es lo que cambió el 8 de septiembre:'));
push(tabla(['Lo que faltaba','Estado'],[
  ['Que Gabriel revisara la estructura de la memoria de cálculo','**Hecho** — dio el visto bueno'],
  ['Correr los 5 scripts de Dynamo en Revit','**Hecho** — se corrieron'],
  ['Montarlos en GoHighLevel','**Es lo único que queda, y es esta guía**'],
],[5200,4000]));
push(CAJA('Los tres CTA pueden salir. Ya no hay que esperar a nadie: lo único entre estos recursos y las campañas es el montaje que viene a continuación.',GREEN,OK));

push(H2('Una sola cosa sigue esperando'));
push(P('El creativo de pauta de **ACERO con el tutor de IA** no se graba ni se sube hasta que el tutor esté montado en la portada de los **cuatro** cursos. Está confirmado en Estructuras; faltan Cerchas, Uniones y Modelado.'));
push(CAJA('Si un alumno paga $225 y no encuentra el tutor, prometimos de más y ya cobrado. Ese es el único bloqueo que queda vivo.',ORANGE,WARN));

/* ── El montaje común ───────────────────────────────────────────────────── */
push(SALTO());
push(H1('El montaje, paso a paso'));
push(P('Los tres se montan igual. Cambia la palabra clave, los campos del formulario y el correo 3. El resto es idéntico, así que se hace una vez y se repite.'));

push(H2('PASO 1 · El formulario nativo de GHL'));
push(P('GHL → **Sites → Forms → New Form**. Cuatro campos siempre: nombre, correo, WhatsApp y **una pregunta de perfil distinta en cada recurso** (están en las fichas de más adelante).'));
push(P('En **Settings → On Submit → Redirect URL**, la página de gracias del recurso con el token. Por ejemplo, para el de Revit:'));
push(MONO(BASE+'guia-revit-ia/gracias-agenda.html?acceso=dm2026'));
push(P('Publica el formulario, copia su URL y pégala en el archivo `index.html` del recurso, en la constante `GHL_FORM_IFRAME_URL`.'));
push(CAJA('Mientras no se pegue, la landing funciona y deja pasar a la gente, pero el contacto NO llega al CRM. Se ve un aviso naranja avisando de eso: es a propósito, es preferible un aviso visible a un lead que se pierde en silencio.',ORANGE,WARN));
push(P('**Por qué formulario nativo y no webhook:** el Inbound Webhook de GHL es prémium y cobra por ejecución. El nativo es gratis y el contacto entra igual.'));

push(H2('PASO 2 · Las dos etiquetas, desde el primer segundo'));
push(P('Workflow **Form Submitted → Add Tag**, siempre dos:'));
push(LI('**La de tema** (`lead-revit-ia`, `lead-memoria-calculo`, `lead-dynamo`) — es la que enciende la secuencia de correos.'));
push(LI('**La de origen** (`origen-bot-GUIA`, `origen-bot-MEMORIA`, `origen-bot-DYNAMO`).'));
push(P('Sin la etiqueta de origen, a fin de mes no se puede decir qué recurso trajo a quién — y la pregunta de si el lead magnet sirvió se queda sin respuesta.'));

push(H2('PASO 3 · El bot de la palabra clave, con DOS ramas'));
push(CAJA('ESTO ES LO QUE COSTÓ 35 LEADS EN JULIO. Configura la acción de envío POR SEPARADO para cada red: rama Instagram → DM de Instagram, rama Facebook → DM de Messenger. NUNCA una sola acción de DM compartida entre las dos.',RED,ALARM));
push(P('Cuando el post nace en Instagram y aparece también en Facebook, mucha gente comenta en la copia de Facebook. Si el envío está atado solo al canal de Instagram, **falla — y el workflow igual marca el paso como ejecutado**, porque el ID de quien comentó es de Facebook. La respuesta pública sí sale siempre, y por eso nadie se entera.'));
push(P('**La respuesta pública lleva SIEMPRE el enlace visible.** No «te escribí al DM». Es gratis ponerlo y es lo único que salva la pieza cuando el canal falla en silencio.'));

push(H2('PASO 4 · La secuencia de correos, tres toques'));
push(P('Se enciende con la etiqueta de tema, nunca a mano.'));
push(tabla(['','Cuándo','Qué dice'],[
  ['Correo 1','Inmediato','El enlace otra vez. Mucha gente cierra la página de gracias sin abrir nada.'],
  ['Correo 2','48 horas','Un uso concreto del recurso (está en la ficha de cada uno).'],
  ['Correo 3','Día 5','El puente al programa. **Cambia según el recurso** — ver fichas.'],
],[1200,1600,6400]));

push(H2('PASO 5 · Notificación interna al setter'));
push(P('Cada lead nuevo avisa con el nombre del recurso **y la respuesta de perfil**. Esa respuesta es la que dice cómo trabajar el lead, y se pierde si todos caen en la misma bandeja.'));

/* ── Fichas ─────────────────────────────────────────────────────────────── */
const FICHAS=[
 {n:'1', t:'Revit + ChatGPT: resuelve errores con IA', palabra:'GUIA',
  carpeta:'guia-revit-ia',
  tags:'lead-revit-ia · origen-bot-GUIA',
  pregunta:'¿Qué usas hoy para resolver un error de Revit?',
  opciones:'Busco en foros y Google · Le pregunto a un compañero · Ya uso ChatGPT o similar · Abro un ticket de soporte · Lo resuelvo probando hasta que sale',
  entrega:'Un botón: la guía en pantalla.',
  correo2:'El error 06 (elementos duplicados) y por qué se descubre al presupuestar, no antes.',
  correo3:'Módulo BIM + IA. **Sin precio**, con «agenda una cita».',
  publica:'Te dejo la guía aquí mismo 👇 los 10 errores de Revit con el prompt exacto para cada uno: [enlace]',
  ojo:'Es el urgente. El reel del miércoles 9 ya lo promete.',
  color:GREEN, fill:OK},
 {n:'2', t:'Memoria de cálculo + plantillas', palabra:'MEMORIA',
  carpeta:'memoria-calculo',
  tags:'lead-memoria-calculo · origen-bot-MEMORIA',
  pregunta:'¿Cada cuánto entregas memorias de cálculo?',
  opciones:'Varias al mes · Algunas al año · Voy a entregar la primera · Las reviso, no las escribo · Todavía no, pero quiero aprender',
  entrega:'Tres botones: la guía, la plantilla en Word y la hoja de Excel.',
  correo2:'El error 3 (hipótesis listadas, no justificadas) y por qué delata una memoria reciclada.',
  correo3:'**Depende del perfil.** «Varias al mes», «algunas al año» o «las reviso» → ACERO, $225 con el tutor de IA incluido, y **aquí el precio SÍ va**: es alguien que ya trabaja y $225 es una decisión pequeña. «Voy a entregar la primera» o «todavía no» → módulo BIM Professional, sin precio, con «agenda una cita».',
  publica:'Te la dejo aquí 👇 las 13 secciones de una memoria que se sostiene ante revisión, con la plantilla en Word y la hoja de verificaciones: [enlace]',
  ojo:'El CTA espera la revisión de Gabriel. Si llega la fecha sin revisar, la matriz ya tiene reemplazo: el CTA cambia a las 5 Verificaciones de Acero, que ya existe.',
  color:RED, fill:ALARM},
 {n:'3', t:'Pack starter de Dynamo', palabra:'DYNAMO',
  carpeta:'pack-dynamo',
  tags:'lead-dynamo · origen-bot-DYNAMO',
  pregunta:'¿Has usado Dynamo antes?',
  opciones:'Nunca lo he abierto · Lo abrí y me perdí · Uso scripts de otros · Escribo los míos · Automatizo para todo el equipo',
  entrega:'Dos botones: la guía de instalación y el ZIP con los 5 scripts.',
  correo2:'El script 02 y por qué los duplicados no se ven hasta que alguien presupuesta.',
  correo3:'Módulo BIM + IA. **Sin precio**, con «agenda una cita».',
  publica:'Te dejo el pack aquí 👇 cinco scripts de Dynamo comentados por dentro, tres de ellos solo leen y no tocan tu modelo: [enlace]',
  ojo:'El CTA espera a que alguien corra los cinco scripts en Revit. «Nunca lo he abierto» y «automatizo para todo el equipo» son dos conversaciones distintas: al primero se le vende el módulo completo, al segundo le sobra la mitad.',
  color:RED, fill:ALARM},
];

push(SALTO());
push(H1('Ficha de cada recurso'));
push(P('Lo que cambia entre uno y otro. Todo lo demás está en el apartado anterior.'));

FICHAS.forEach(f=>{
  push(H2(f.n+' · '+f.t));
  push(tabla(['Campo','Valor'],[
    ['Palabra clave', '**'+f.palabra+'**'],
    ['Etiquetas', f.tags],
    ['Pregunta de perfil', f.pregunta],
    ['Opciones del desplegable', f.opciones],
    ['Qué entrega la página de gracias', f.entrega],
    ['Correo 2 (48 h)', f.correo2],
    ['Correo 3 (día 5)', f.correo3],
  ],[2600,6600]));
  push(P('**Redirect URL del formulario:**'));
  push(MONO(BASE+f.carpeta+'/gracias-agenda.html?acceso=dm2026'));
  push(P('**Respuesta pública del bot** (con el enlace visible, siempre):'));
  push(CAJA(f.publica,NAVY,CODE));
  push(CAJA(f.ojo,f.color,f.fill));
});

/* ── Checklist ──────────────────────────────────────────────────────────── */
push(SALTO());
push(H1('Comprobar antes de publicar el CTA'));
push(P('Diez puntos por recurso. No basta con que la landing cargue: hay que verificar que **el dato llega** y que **el archivo se entrega**.'));
[ 'Comentar la palabra clave **en Instagram** → llega el DM con el enlace.',
  'Comentar la palabra clave **en la copia de Facebook** → llega el DM por Messenger.',
  'La respuesta pública automática incluye el enlace visible.',
  'El enlace abre la landing **en teléfono**, no solo en computador.',
  'Enviar el formulario → redirige solo a la página de gracias.',
  'El botón de la página de gracias abre el contenido **sin pedir registro**.',
  'Los botones de descarga entregan el archivo correcto (Word, Excel, ZIP).',
  'El contacto aparece en el CRM con sus **dos** etiquetas.',
  'Llega el correo 1 con el enlace.',
  'Borrar los contactos de prueba antes de publicar.',
].forEach((x,i)=>push(NUM(i+1,x)));
push(CAJA('El punto 2 es el que se salta todo el mundo, y es justo el que falló en julio. Probar solo en Instagram no detecta nada.',RED,ALARM));

push(H2('Si el candado no se abre'));
push(P('El contenido se desbloquea con `?acceso=dm2026`, que además queda guardado en ese navegador. Si alguien dice que le pide registro habiendo llenado el formulario, casi siempre es que abrió el enlace en otro dispositivo. Se le manda el enlace con el token y entra.'));

push(H2('Si los contactos no llegan al CRM'));
push(P('Quiere decir que falta pegar la URL del formulario nativo en `GHL_FORM_IFRAME_URL`, o que las claves no coinciden. Es la causa más frecuente, y con diferencia.'));

/* ── Qué no promete ─────────────────────────────────────────────────────── */
push(H1('Lo que NO prometen, y conviene decir igual'));
push(P('Los tres recursos están escritos con un límite explícito dentro. No es un adorno legal: es lo que permite que una academia de ingeniería los reparta sin quedar mal.'));
push(tabla(['Recurso','El límite, dicho en voz alta'],[
  ['Revit + ChatGPT','No reemplaza saber Revit. La IA es buena para entender qué te está diciendo el programa y para ordenar por dónde buscar. Es mala para decidir. No dimensiona, no verifica norma y no firma nada — hay una página entera sobre esto.'],
  ['Memoria de cálculo','No calcula nada. Es estructura documental. Ninguna cifra normativa se transcribe: se remite siempre a la norma vigente. El Excel calcula un ratio y marca CUMPLE / NO CUMPLE, y nada más: el límite lo escribe el usuario.'],
  ['Pack de Dynamo','Se entregan tal cual, para aprender y adaptar. Hay que probarlos en una copia antes de usarlos en producción. Tres solo leen; los dos que escriben traen simulacro.'],
],[2400,6800]));
push(CAJA('Si alguien pregunta por WhatsApp «¿esto me resuelve los cálculos?», la respuesta es no — y decirlo bien nos suma. Es la diferencia entre una academia de ingeniería y un vendedor de plantillas.',GREEN,OK));

const doc=new Document({styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:900,bottom:900,left:900,right:900}}},children:h}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/Lead-Magnets-Septiembre-Montaje-GHL.docx');
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);
  console.log(`OK → ${OUT} (${(b.length/1024).toFixed(0)} KB)`);});
