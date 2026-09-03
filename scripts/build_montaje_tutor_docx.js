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
push(P('Son dos montajes distintos y uno depende del otro: primero las variables, después lo que se ve. El PASO 0 ya está hecho por Dayana y verificado — el tutor responde. Podéis empezar directamente por el PASO 1.'));
push(P('La página del tutor ya está publicada y lista. No hay que editar código en ningún momento:'));
push(...CODE(URL));

push(H1('PASO 1 · La lección dentro de los 4 cursos de ACERO'));
push(P('Va solo en estos cuatro cursos. En ningún otro: el tutor únicamente conoce estas clases, y en un curso del Máster respondería «eso no está en el material» a todo.'));
[['1','Análisis y Diseño Simplificado de Estructuras Complejas de Acero'],
 ['2','Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales'],
 ['3','Modelado BIM en Hormigón Armado y Acero Estructural'],
 ['4','Teoría y Cálculo de Uniones Metálicas en Edificaciones']].forEach(([n,t])=>push(NUM(n,t)));

push(H2('En cada uno de los 4 cursos'));
push(NUM('1','Entrar al curso → Categorías / Módulos.'));
push(NUM('2','Crear una lección AL PRINCIPIO, la primera de todas, llamada: Tutor IA — pregúntale a tus clases'));
push(NUM('3','En el cuerpo de la lección insertar un bloque de código personalizado (Custom Code / HTML) y pegar esto tal cual:'));
push(...CODE(`<iframe
  src="${URL}"
  style="width:100%;height:720px;border:0;border-radius:12px;display:block"
  title="Tutor IA · Especialización en Acero"
  loading="lazy"></iframe>`));
push(NUM('4','Guardar y publicar la lección.'));
push(AVISO('Que el bloque quede a ancho completo y sin relleno lateral. Si el editor deja margen a los lados, el chat sale estrecho y se lee mal en el teléfono.'));
push(H2('Comprobar antes de darlo por hecho'));
push(P('Abrir la lección COMO ALUMNO (no desde el editor) y hacer una pregunta de verdad, por ejemplo «¿qué es el pandeo?». Tiene que responder y terminar citando la clase y el minuto exactos.'));

push(H1('PASO 2 · El botón en la plantilla'));
push(P('Este sí es global: aparece en todos los cursos. Por eso el texto del botón dice que es solo de Acero, para que un alumno del Máster lo entienda antes de hacer clic y no después de preguntar.'));
push(P('Lo monta Dayana. Se incluye aquí para que sepáis que existe y por qué.'));

push(H1('Lo que hay que saber cuando pregunten'));
push(P('No hay que activar a nadie.',{run:{bold:true}}));
push(P('No se emite nada por alumno. Quien entra al área de miembros ya está autenticado por GoHighLevel, y con eso basta: un alumno que se matricula el martes tiene tutor el martes.'));
push(P('El tutor solo conoce esos 4 cursos.',{run:{bold:true}}));
push(P('Si alguien le pregunta por hormigón armado o por BIM 4D, responderá que no está en el material y mandará a la asesoría. Es a propósito, no es un fallo.'));
push(P('Nunca da cifras de norma ni precios.',{run:{bold:true}}));
push(P('Ante «¿cuántos MPa es la fluencia del A36?» remite a la norma vigente en vez de dictar el número, porque las transcripciones automáticas deforman las cifras. Está probado: 17 casos, con las trampas repetidas 3 veces cada una.'));
push(P('Hay dos topes al día.',{run:{bold:true}}));
push(P('20 preguntas por navegador y 600 en todo el servicio. Si un alumno agota las suyas, el mensaje le dice que mañana se reinician y le ofrece la asesoría.'));

push(H1('Si algo falla, en este orden'));
push(tabla(['Qué se ve','Qué significa y qué hacer'],[
  ['La página no carga', 'Abrir ' + URL + ' directamente en el navegador. Si tampoco carga, avisar a Dayana.'],
  ['«Token inválido»', 'Falta la variable TOKEN_PAGINA en Render o no coincide. Es de Dayana.'],
  ['No responde nada', 'Suele ser el dominio: falta añadirlo en CORS_ORIGENES. Es de Dayana.'],
  ['«Alcanzaste tus preguntas de hoy»', 'No es un fallo: es el tope diario funcionando.'],
  ['«Eso no está en el material»', 'Tampoco es un fallo. La pregunta es de un curso que el tutor no conoce.'],
], [2600, 6600]));

const doc = new Document({ creator:'Design Modeling Academy',
  title:'Montar el Tutor IA en GoHighLevel',
  styles:{ default:{ document:{ run:{ font:'Nunito', size:21 } } } },
  sections:[{ properties:{ page:{ margin:{ top:1000, bottom:1000, left:1000, right:1000 } } },
              children:hijos }] });

const OUT = path.resolve(__dirname,'..','matriz-viral','entregables','Montar-Tutor-IA-en-GHL-Ester-Aylin.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b);
  console.log(`OK → ${path.relative(path.resolve(__dirname,'..'), OUT)} (${(b.length/1024).toFixed(0)} KB)`); });
