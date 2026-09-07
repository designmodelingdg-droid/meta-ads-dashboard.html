/* Guía de montaje del Diagnóstico BIM del Máster, en Word para Ester y Aylin.
 * Se escribe desde el markdown para que las dos versiones no se separen.
 *   node scripts/build_test_master_docx.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle } = require('docx');
const ROOT=path.dirname(__dirname);
const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', RED='A33B2A', GREEN='1E7A55',
      WARN='FBF0DA', ALARM='F7E5E2', OK='E2F0E9', CODE='EEF2F6';

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:150},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:32,font:'Overpass'})]});
const H2=t=>new Paragraph({spacing:{before:270,after:100},
  children:[new TextRun({text:t,bold:true,color:ORANGE,size:25,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},children:trozos(t,o)});
const LI=t=>new Paragraph({bullet:{level:0},spacing:{after:70},children:trozos(t)});
const MONO=t=>new Paragraph({spacing:{before:100,after:130},
  shading:{type:ShadingType.CLEAR,fill:CODE},
  children:[new TextRun({text:t,size:18,font:'Consolas'})]});
const CAJA=(t,color,fill)=>new Paragraph({spacing:{before:150,after:170},
  shading:{type:ShadingType.CLEAR,fill},
  border:{left:{style:BorderStyle.SINGLE,size:20,color,space:10}},
  children:trozos(t,{color})});

/* **negrita** dentro del texto */
function trozos(t,o={}){
  const out=[]; const base={size:21,font:'Nunito',...(o.color?{color:o.color}:{}),...(o.run||{})};
  t.split(/(\*\*[^*]+\*\*)/).forEach(p=>{
    if(!p) return;
    const b=p.startsWith('**')&&p.endsWith('**');
    out.push(new TextRun({text:b?p.slice(2,-2):p,bold:b,...base}));
  });
  return out;
}
const celda=(t,{b=false,w=0,fill=null}={})=>new TableCell({width:{size:w,type:WidthType.DXA},
  ...(fill?{shading:{type:ShadingType.CLEAR,fill}}:{}),
  margins:{top:90,bottom:90,left:130,right:130},
  children:[new Paragraph({children:trozos(t,{run:{size:19}})})]});
const tabla=(head,filas,anchos)=>new Table({columnWidths:anchos,width:{size:9200,type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:anchos[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      margins:{top:90,bottom:90,left:130,right:130},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:'FFFFFF',size:19,font:'Overpass'})]})]}))}),
    ...filas.map(f=>new TableRow({children:f.map((c,i)=>celda(c,{w:anchos[i]}))}))]});

const h=[]; const push=(...x)=>h.push(...x);
const URL='https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-master-bim/';

push(new Paragraph({spacing:{after:60},children:[new TextRun({text:'DESIGN MODELING ACADEMY',
  bold:true,color:ORANGE,size:19,font:'Overpass',characterSpacing:60})]}));
push(new Paragraph({spacing:{after:120},children:[new TextRun({
  text:'Diagnóstico BIM del Máster',bold:true,color:NAVY,size:42,font:'Overpass'})]}));
push(P('Guía de montaje para Ester y Aylin · 7 de septiembre de 2026',{run:{color:GREY,italics:true}}));
push(P('El test ya está construido y probado. Lo que falta es conectarlo a GoHighLevel para que el resultado llegue al asesor antes de la llamada.'));
push(MONO(URL));

push(H1('Qué es esto, y en qué se diferencia del test que ya existe'));
push(P('Hay dos tests y **no son el mismo producto**.'));
push(tabla(['','Test de Nivel BIM (ya existe)','Diagnóstico del Máster (este)'],[
  ['Para quién','Cualquiera, recurso gratuito','Solo quien **ya agendó** una cita'],
  ['Cómo llega','Anuncio → landing → formulario','El closer lo manda por WhatsApp tras agendar'],
  ['Qué mide','Nivel BIM','Nivel BIM **+ base técnica**'],
  ['A dónde va el resultado','A ninguna parte: se queda en el navegador','**Al CRM, al contacto que lo hizo**'],
  ['Qué ve la persona al terminar','Su nivel y su ruta','**Nada: se lo da el asesor en la cita**'],
],[2000,3400,3800]));
push(CAJA('El test público calcula el nivel, se lo enseña a la persona y ahí muere: no manda el resultado a ningún sitio. Ese es el agujero que este cierra, y es la razón de que exista.',RED,ALARM));

push(H1('Las 20 preguntas, en dos ejes'));
push(P('**Eje A · Nivel BIM (14 preguntas).** Cuatro bloques que corresponden a los cuatro módulos: Modelador (4), Coordinador (4), BIM Manager 4D-5D (3), Especialista BIM+IA (3). Un bloque se domina con el 70% de su puntaje.'));
push(P('**Eje B · Base técnica (6 preguntas).** Tres de cálculo y diseño estructural, tres de arquitectura y edificación. Se considera base real con 6 de 9.'));
push(CAJA('Esto último es lo nuevo, y es lo que más cambia la llamada: al que predimensiona una zapata no se le vende igual que al que resuelve un programa arquitectónico, aunque los dos sean Coordinadores BIM.',ORANGE,WARN));
push(H2('Una regla que conviene entender antes de leer un resultado'));
push(P('El nivel es el **último bloque dominado sin saltos**. Si alguien domina Modelador y BIM Manager pero no Coordinador, el test dice **Modelador**, no BIM Manager, y añade que tiene conocimiento disperso por encima de su nivel.'));
push(P('Es a propósito: decirle al asesor que tiene delante a un BIM Manager cuando le falta la coordinación entera hace que pierda la llamada en los primeros dos minutos.'));

push(H1('El resultado se entrega EN LA LLAMADA, no en la pantalla'));
push(P('Esta es la decisión que más define el test, y conviene que todo el equipo la diga igual.'));
push(P('Al terminar, la persona **no ve su nivel ni su perfil**. Ve que el diagnóstico está completo, que ya tenemos su perfil, y que su asesor se lo entrega en la cita.'));
push(P('**Por qué.** Si al terminar le decimos «eres Coordinador BIM», la cita pasa a ser opcional: ya tiene lo que vino a buscar. Guardando el resultado, la llamada deja de ser una presentación de ventas y pasa a ser el sitio donde recoge algo que ya es suyo y todavía no ha visto.'));
push(CAJA('En agosto la asistencia a citas fue del 46,3% contra un objetivo del 80%. Este es uno de los pocos resortes que la mueven sin gastar un dólar más.',GREEN,OK));
push(H2('Si preguntan por WhatsApp antes de la cita'));
push(P('No se manda el resultado por escrito. Respuesta sugerida:'));
push(CAJA('Ya tengo tu perfil aquí delante. Te lo explico en la llamada porque tiene matices —hay cosas que dominas por encima de tu nivel y huecos que se cierran más rápido de lo que parece— y por escrito se malinterpreta. En cinco minutos de llamada lo tienes claro.',NAVY,CODE));

push(H1('PASO 1 · Crear los campos personalizados'));
push(P('GHL → **Settings → Custom Fields → Add Field**. Seis campos, todos sobre el objeto **Contact**.'));
push(tabla(['Nombre del campo','Clave (exacta)','Tipo'],[
  ['Nivel BIM','nivel_bim','Texto de una línea'],
  ['Perfil técnico','perfil_tecnico','Texto de una línea'],
  ['Módulo recomendado','modulo_recomendado','Texto de una línea'],
  ['Código de diagnóstico','codigo_diagnostico','Texto de una línea'],
  ['Detalle del diagnóstico','detalle_diagnostico','**Texto largo**'],
  ['Puntajes por bloque','puntajes_bloques','Texto de una línea'],
],[3200,3200,2800]));
push(CAJA('La clave es lo que importa, no el nombre visible. Si GHL genera una clave distinta al guardar (a veces le pone un prefijo), hay que copiar la que quedó y pegarla en app.html, en el bloque CFG.CAMPOS.',ORANGE,WARN));

push(H1('PASO 2 · Crear el formulario que recibe el resultado'));
push(P('GHL → **Sites → Forms → New Form**. Nómbralo «Diagnóstico BIM Máster».'));
push(P('Añade los seis campos del paso 1, **todos ocultos**: la persona ya terminó el test, este formulario solo transporta el dato al CRM.'));
push(P('Publica el formulario y copia su enlace, que se ve así:'));
push(MONO('https://api.leadconnectorhq.com/widget/form/AbC123XyZ'));
push(P('Pégalo en **app.html**, en CFG.FORM_GHL, reemplazando PEGAR_ID_DEL_FORMULARIO.'));
push(CAJA('Mientras no se pegue, el test funciona y calcula bien, pero muestra un aviso naranja diciendo que falta conectarlo. Es a propósito: es preferible un aviso visible a un resultado que se pierde en silencio.',ORANGE,WARN));
push(P('**Por qué formulario nativo y no webhook:** el webhook de GHL es prémium y cobra por ejecución. El nativo es gratis y el dato entra igual.'));

push(H1('PASO 3 · Cómo manda el link el closer'));
push(P('El link tiene que llevar identificado al contacto, o el resultado no se puede pegar a nadie. En la plantilla de WhatsApp de GHL:'));
push(MONO(URL+'?cid={{contact.id}}&nombre={{contact.first_name}}&email={{contact.email}}'));
push(P('Mensaje sugerido, después de agendar:'));
push(CAJA('Listo [nombre], ya quedó tu cita para el [día] a las [hora].\n\nAntes de la llamada, te paso un diagnóstico de 5 minutos: 20 preguntas sobre lo que sabes hacer en un proyecto. Lo reviso antes de hablar contigo, así no gastamos la cita en que me expliques desde cero por dónde vas.\n\n[link]',NAVY,CODE));

push(H1('PASO 4 · Dónde lo lee el asesor'));
push(P('En la ficha del contacto, en los campos personalizados. El que se lee de un vistazo es **detalle_diagnostico**, que termina con una línea así:'));
push(MONO('PARA EL ASESOR: Domina hasta Coordinador, viene de cálculo\nestructural. Entrar por BIM Management · GESTIONA.'));
push(P('Esa frase es el resumen operativo: nivel, de dónde viene y por dónde entrar. Todo lo demás es el respaldo por si la conversación lo pide.'));
push(P('**Recomendado:** añadir esos campos a la vista de la oportunidad en el pipeline de High Tickets, para verlos sin abrir el contacto.'));

push(H1('Comprobar antes de darlo por hecho'));
push(P('No basta con que el test cargue. Hay que verificar que **el dato llega**:'));
push(LI('Abre el link **con un cid real** de un contacto de prueba tuyo.'));
push(LI('Responde las 20 preguntas de cualquier forma.'));
push(LI('Al terminar debe decir «Listo. Tu asesor ya lo tiene.»'));
push(LI('**Abre ese contacto en el CRM** y comprueba que los seis campos se llenaron.'));
push(CAJA('El paso 4 es el que de verdad importa. Los pasos 1 a 3 pueden salir bien y el dato no haber llegado.',RED,ALARM));
push(H2('Si los campos llegan vacíos'));
push(P('Quiere decir que el formulario no está tomando los valores de la dirección. Dos cosas que revisar, en este orden:'));
push(LI('**Que las claves coincidan** exactamente entre CFG.CAMPOS y las claves reales en el CRM. Es la causa más frecuente.'));
push(LI('**Que el formulario acepte prellenado por URL.** Si tu versión de GHL no lo hace, la alternativa es el webhook prémium: se activa en el formulario y se pega su URL en CFG.FORM_GHL. Cuesta por ejecución, pero funciona igual.'));
push(P('Mientras tanto, el test siempre muestra un **código de diagnóstico** —por ejemplo B2-EST-57— que el asesor puede pedir y apuntar a mano. No es la solución, es el paracaídas.'));

push(H1('Lo que hay que saber cuando pregunten'));
push(P('**No sustituye a la llamada, la prepara.** El test calcula el nivel, el perfil técnico y el módulo por el que debería entrar. Todo eso lo entrega el asesor.'));
push(P('**Nunca dice precios.** Ni del Máster, ni de los módulos, ni de la ruta.'));
push(P('**Funciona sin el cid.** Si alguien abre el link suelto, el test corre igual y muestra el código; simplemente el resultado no se pega a ningún contacto.'));

const doc=new Document({styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:900,bottom:900,left:900,right:900}}},children:h}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/Diagnostico-BIM-Master-Montaje-GHL.docx');
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);
  console.log(`OK → ${OUT} (${(b.length/1024).toFixed(0)} KB)`);});
