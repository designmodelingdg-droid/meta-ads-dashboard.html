/* Genera el Word de montaje del Tutor IA para Ester y Aylin.
 *
 * El contenido vive en tutor-acero/MONTAJE-GHL.md, que es lo que se versiona.
 * Esto solo lo viste con el formato de la casa: nadie mantiene dos textos.
 *
 *   node scripts/build_montaje_tutor_docx.js
 */
const fs = require('fs'), path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle, AlignmentType } = require('docx');

const NAVY = '0E2438', ORANGE = 'C96A1C', GREY = '5A6B7B', RED = 'A33B2A',
      CODE_BG = 'F2F5F8', WARN_BG = 'FBF0DA';

const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing:{before:320,after:140},
  children:[new TextRun({ text:t, bold:true, color:NAVY, size:32, font:'Overpass' })]});
const H2 = t => new Paragraph({ spacing:{before:260,after:100},
  children:[new TextRun({ text:t, bold:true, color:ORANGE, size:26, font:'Overpass' })]});
const P = (t,o={}) => new Paragraph({ spacing:{after:100},
  children:[new TextRun({ text:t, size:21, font:'Nunito', ...(o.run||{}) })], ...o });
const LI = t => new Paragraph({ bullet:{level:0}, spacing:{after:60},
  children:[new TextRun({ text:t, size:21, font:'Nunito' })]});
const NUM = (n,t) => new Paragraph({ spacing:{after:80}, indent:{left:280},
  children:[new TextRun({ text:n+'. ', bold:true, size:21, font:'Nunito', color:ORANGE }),
            new TextRun({ text:t, size:21, font:'Nunito' })]});
const CODE = txt => txt.split('\n').map((l,i,a) => new Paragraph({
  spacing:{before:i===0?100:0, after:i===a.length-1?140:0},
  shading:{type:ShadingType.CLEAR, fill:CODE_BG},
  border:{left:{style:BorderStyle.SINGLE, size:14, color:ORANGE, space:8}},
  children:[new TextRun({ text:l||' ', font:'Consolas', size:17 })]}));
const AVISO = txt => new Paragraph({ spacing:{before:140,after:140},
  shading:{type:ShadingType.CLEAR, fill:WARN_BG},
  border:{left:{style:BorderStyle.SINGLE, size:20, color:RED, space:10}},
  children:[new TextRun({ text:txt, size:21, font:'Nunito', bold:true, color:RED })]});
const celda = (t,{b=false,w=0}={}) => new TableCell({ width:{size:w,type:WidthType.DXA},
  margins:{top:80,bottom:80,left:120,right:120},
  children:[new Paragraph({ children:[new TextRun({ text:t, size:19, font:'Nunito', bold:b })]})]});
const tabla = (head, filas, anchos) => new Table({ columnWidths:anchos,
  width:{size:9200,type:WidthType.DXA},
  rows:[ new TableRow({ tableHeader:true, children: head.map((h,i)=>
           new TableCell({ width:{size:anchos[i],type:WidthType.DXA},
             shading:{type:ShadingType.CLEAR, fill:NAVY}, margins:{top:80,bottom:80,left:120,right:120},
             children:[new Paragraph({ children:[new TextRun({ text:h, bold:true, color:'FFFFFF', size:19, font:'Overpass' })]})]}))}),
         ...filas.map(f => new TableRow({ children: f.map((c,i)=>celda(c,{w:anchos[i]})) })) ]});

const URL = 'https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-acero/';
const hijos = [];
const push = (...x) => hijos.push(...x);

push(new Paragraph({ spacing:{after:60},
  children:[new TextRun({ text:'DESIGN MODELING ACADEMY', bold:true, color:ORANGE, size:19,
                          font:'Overpass', characterSpacing:60 })]}));
push(new Paragraph({ spacing:{after:120},
  children:[new TextRun({ text:'Montar el Tutor IA en GoHighLevel', bold:true, color:NAVY,
                          size:44, font:'Overpass' })]}));
push(P('Para Ester y Aylin · Especialización en Acero',{run:{color:GREY, italics:true}}));
push(P('Todo lo técnico ya está hecho y probado: el tutor está en línea, responde citando la sesión y el minuto, y las variables del servidor están puestas. Lo que falta es que aparezca dentro de los cursos.'));
push(AVISO('No hay que pegar código. El editor de cursos de GHL no permite insertar HTML en la lección, solo bloques con botón y enlace. Por eso el tutor va como un botón que abre su página, no incrustado dentro de la clase.'));
push(P('Esta es la dirección del tutor, la misma en todos los sitios:'));
push(...CODE(URL));

push(H1('Dónde va, y dónde NO'));
push(P('Va solo en los 4 cursos de la Especialización en Acero:'));
[['1','Análisis y Diseño Simplificado de Estructuras Complejas de Acero'],
 ['2','Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales'],
 ['3','Modelado BIM en Hormigón Armado y Acero Estructural'],
 ['4','Teoría y Cálculo de Uniones Metálicas en Edificaciones']].forEach(([n,t])=>push(NUM(n,t)));
push(AVISO('No va en la plantilla general ni en ningún curso del Máster. El tutor solo conoce esas cuatro clases: a un alumno del Máster le respondería «eso no está en el material» a todo, y sería peor que no tener botón.'));

push(H1('Los pasos, en cada uno de los 4 cursos'));
push(NUM('1','Abrir el curso → Editar → en el selector Páginas elegir PRODUCTO (la portada del curso, la que ve el alumno al entrar).'));
push(NUM('2','Añadir un Custom Block en el cuerpo, arriba del todo o justo debajo del video de presentación.'));
push(NUM('3','Rellenar los campos del bloque exactamente así:'));
push(tabla(['Campo del bloque','Qué poner'],[
  ['Imagen','tarjeta-tutor.png (va adjunta con estas instrucciones)'],
  ['Heading','Tutor IA · pregúntale a tus clases'],
  ['Contenido','Resuelve tus dudas con las clases de tus 4 cursos. Te dice en qué sesión y en qué minuto está la respuesta — y si algo no está en el material, te lo dice en vez de inventarlo.'],
  ['Button Text','Abrir el Tutor IA'],
  ['Tipo de botón','Solid Button'],
  ['Relleno del botón','#0E2438'],
  ['Borde del botón','#E8A04A'],
  ['Button Text (color)','#FFFFFF'],
  ['Ir a la URL','La dirección de arriba, pegada completa'],
], [2400, 6600]));
push(NUM('4','Guardar cambios.'));
push(NUM('5','Repetir en los otros tres cursos.'));
push(H2('Si además se quiere dentro de las lecciones'));
push(P('Con el mismo Custom Block, en Páginas → Lección, para que el alumno lo tenga a mano mientras estudia sin volver a la portada. Es opcional: con la portada del curso ya se cumple.'));

push(H1('Comprobar antes de darlo por hecho'));
push(P('Abrir el curso COMO ALUMNO, no desde el editor. Pulsar el botón y hacer una pregunta de verdad, por ejemplo: ¿Qué es el pandeo?'));
push(P('Tiene que responder y terminar citando la clase y el minuto, así:'));
push(...CODE('El pandeo es un fenómeno de inestabilidad que ocurre en\nelementos estructurales…\n\nFUENTES: [221121 Sesión N°1-Acero-DM.mp4 · min 112:09]'));
push(AVISO('Avisar a Dayana cuando los 4 estén hechos: hasta que estén, la campaña de publicidad de ACERO no puede salir.'));
push(H2('Por qué eso último importa'));
push(P('El precio de la Especialización sube de $200 a $225 justamente porque incluye el tutor. Si la campaña sale antes de que el tutor esté montado, un alumno paga los $225 y no lo encuentra. Por eso el orden es: primero estos 4 cursos, después la publicidad.'));

push(H1('Lo que hay que saber cuando pregunten'));
push(P('No hay que activar a nadie.',{run:{bold:true}}));
push(P('No se emite ninguna clave por alumno. Quien entra al área de miembros ya está identificado por GoHighLevel, y con eso basta: un alumno que se matricula el martes tiene tutor el martes.'));
push(P('El tutor solo conoce esos 4 cursos.',{run:{bold:true}}));
push(P('Si le preguntan por hormigón armado o por BIM 4D, dirá que no está en el material y mandará a la asesoría. Es a propósito.'));
push(P('Nunca da cifras de norma ni precios.',{run:{bold:true}}));
push(P('Ante «¿cuántos MPa es la fluencia del A36?» remite a la norma vigente en vez de dictar el número, porque las transcripciones automáticas deforman las cifras. Está probado: 17 casos, con las trampas repetidas 3 veces cada una.'));
push(P('Hay dos topes al día.',{run:{bold:true}}));
push(P('20 preguntas por navegador y 600 en todo el servicio. Si un alumno agota las suyas, el mensaje le dice que mañana se reinician y le ofrece la asesoría.'));
push(P('El botón abre en otra pestaña.',{run:{bold:true}}));
push(P('Es a propósito: el alumno consulta y vuelve a su clase sin perder dónde iba.'));

push(H1('Si algo falla, en este orden'));
push(tabla(['Qué se ve','Qué significa'],[
  ['La página no carga', 'Abrir la dirección directamente en el navegador. Si tampoco carga, avisar a Dayana.'],
  ['«Token inválido»', 'Suele ser que el servidor estaba reiniciándose. Esperar dos minutos y recargar con Ctrl+Shift+R. Si sigue, es de Dayana.'],
  ['No responde nada', 'Problema de permisos del dominio. Es de Dayana.'],
  ['«Alcanzaste tus preguntas de hoy»', 'No es un fallo: es el tope diario funcionando.'],
  ['«Eso no está en el material»', 'Tampoco es un fallo. La pregunta es de un tema que el tutor no conoce.'],
], [2600, 6600]));

const doc = new Document({ creator:'Design Modeling Academy',
  title:'Montar el Tutor IA en GoHighLevel',
  styles:{ default:{ document:{ run:{ font:'Nunito', size:21 } } } },
  sections:[{ properties:{ page:{ margin:{ top:1000, bottom:1000, left:1000, right:1000 } } },
              children:hijos }] });

const OUT = path.resolve(__dirname,'..','matriz-viral','entregables','Montar-Tutor-IA-en-GHL-Ester-Aylin.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b);
  console.log(`OK → ${path.relative(path.resolve(__dirname,'..'), OUT)} (${(b.length/1024).toFixed(0)} KB)`); });
