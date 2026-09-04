/* Propuesta de nombres de cursos con el agente de IA dentro.
 *   node scripts/build_nombres_cursos_docx.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle } = require('docx');
const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', RED='A33B2A',
      LIGHT='F4F7FA', WARN='FBF0DA';
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:140},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:32,font:'Overpass'})]});
const H2=t=>new Paragraph({spacing:{before:260,after:100},
  children:[new TextRun({text:t,bold:true,color:ORANGE,size:25,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},
  children:[new TextRun({text:t,size:21,font:'Nunito',...(o.run||{})})]});
const AVISO=t=>new Paragraph({spacing:{before:140,after:140},
  shading:{type:ShadingType.CLEAR,fill:WARN},
  border:{left:{style:BorderStyle.SINGLE,size:20,color:RED,space:10}},
  children:[new TextRun({text:t,size:21,font:'Nunito',bold:true,color:RED})]});
const celda=(t,{b=false,w=0,fill=null}={})=>new TableCell({width:{size:w,type:WidthType.DXA},
  ...(fill?{shading:{type:ShadingType.CLEAR,fill}}:{}),
  margins:{top:90,bottom:90,left:130,right:130},
  children:[new Paragraph({children:[new TextRun({text:t,size:19,font:'Nunito',bold:b})]})]});
const tabla=(head,filas,anchos)=>new Table({columnWidths:anchos,width:{size:9200,type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:anchos[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      margins:{top:90,bottom:90,left:130,right:130},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:'FFFFFF',size:19,font:'Overpass'})]})]}))}),
    ...filas.map(f=>new TableRow({children:f.map((c,i)=>celda(c,{w:anchos[i]}))}))]});

const h=[]; const push=(...x)=>h.push(...x);
push(new Paragraph({spacing:{after:60},children:[new TextRun({text:'DESIGN MODELING ACADEMY',
  bold:true,color:ORANGE,size:19,font:'Overpass',characterSpacing:60})]}));
push(new Paragraph({spacing:{after:120},children:[new TextRun({
  text:'Nombres de los cursos con el agente de IA',bold:true,color:NAVY,size:42,font:'Overpass'})]}));
push(P('Propuesta para revisar · 3 de septiembre de 2026',{run:{color:GREY,italics:true}}));

push(P('Ahora que la Especialización en Acero incluye el tutor de IA, los nombres de los cursos pueden decirlo. Pero solo donde sea verdad, y hoy es verdad en cuatro cursos, no en todos.'));

push(H1('La regla antes que la lista'));
push(P('Un nombre que dice «con IA» es una promesa. El alumno la lee al comprar y la busca al entrar; si no la encuentra, el nombre deja de vender y empieza a costar. Por eso la propuesta separa lo que ya se puede renombrar de lo que primero hay que construir.'));
push(AVISO('El tutor solo conoce los 4 cursos de la Especialización en Acero: son las 135 horas que están indexadas. Cualquier otro curso que se renombre con «IA» estaría prometiendo algo que todavía no existe.'));

push(H1('Grupo 1 · Se pueden renombrar hoy'));
push(P('Los cuatro cursos de la Especialización en Acero. El tutor ya responde con sus clases.'));
push(tabla(['Nombre actual','Nombre propuesto'],[
 ['Análisis y Diseño Simplificado de Estructuras Complejas de Acero',
  'Estructuras Complejas de Acero · con Tutor IA'],
 ['Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales',
  'Cerchas y Naves Industriales · con Tutor IA'],
 ['Modelado BIM en Hormigón Armado y Acero Estructural',
  'Modelado BIM en Hormigón y Acero · con Tutor IA'],
 ['Teoría y Cálculo de Uniones Metálicas en Edificaciones',
  'Uniones Metálicas en Edificaciones · con Tutor IA'],
],[4300,4700]));
push(H2('Por qué así y no de otra forma'));
push(P('Se acortan. Los nombres actuales tienen entre 45 y 63 caracteres y en la portada del área de miembros llegan cortados. «Análisis y Diseño Simplificado de…» no dice nada; «Estructuras Complejas de Acero» sí.'));
push(P('El sufijo va siempre igual y siempre al final. «· con Tutor IA» detrás del nombre, no dentro. Así se lee la materia primero —que es lo que el alumno busca— y se ve de un golpe qué cursos ya lo tienen y cuáles no.'));
push(P('No se dice «con Inteligencia Artificial». Es más largo, suena a folleto y además promete más de lo que hay: no es que el curso sea de IA, es que trae un tutor de IA encima. Tutor es la palabra exacta.'));

push(H1('Grupo 2 · La Especialización'));
push(tabla(['Nombre actual','Nombre propuesto'],[
 ['Especialización en Acero','Especialización en Acero · con Tutor IA incluido'],
],[4300,4700]));
push(P('«Incluido» hace un trabajo que no hace ninguna otra palabra: es lo que evita que alguien pregunte si el tutor se paga aparte. Y ese es justo el argumento que sostiene el precio de $225.'));

push(H1('Grupo 3 · Naves Industriales (el curso suelto de $27)'));
push(P('Nombre actual: «OFF Naves Industriales PRO 30 Horas en SAP2000».'));
push(P('Aquí hay una decisión antes que un nombre, y no la puedo tomar yo.'));
push(P('El contenido de naves SÍ está indexado —son 1.302 bloques del curso de Cerchas y Naves—, así que técnicamente el tutor podría responder a un alumno de este curso. Pero le respondería también con material de los otros tres cursos, que esa persona no compró. Hay que decidir si eso es un problema o un regalo.'));
push(tabla(['Si se decide…','El nombre sería'],[
 ['Que el tutor responda solo con el material de naves','Naves Industriales en SAP2000 · con Tutor IA'],
 ['Que no lleve tutor por ahora','Naves Industriales PRO en SAP2000 (30 horas)'],
],[4300,4700]));
push(P('En los dos casos se quita el «OFF» del principio: es una marca interna de descuento y en la tienda se lee como parte del nombre del curso.',{run:{italics:true}}));
push(P('La primera opción es un día de trabajo: el servicio ya sabe filtrar por curso, solo hay que decirle cuál. La segunda es gratis y honesta.'));

push(H1('Grupo 4 · El Máster y lo demás'));
push(P('Los cuatro módulos del Máster, el Diplomado y el Curso Introductorio NO se renombran todavía.'));
push(P('Sus clases no están transcritas ni indexadas, así que el tutor no las conoce. Renombrarlos con «IA» hoy sería vender algo que no se puede entregar — y el Máster ya tiene su propio argumento de IA, que son las microcredenciales y la DMA Engineering Suite. Mezclarlo con «tutor de IA» confunde dos cosas distintas.'));
push(P('Lo que falta para poder hacerlo no es programación: es transcribir esos cursos y sumarlos al corpus, igual que se hizo con estos cuatro. Es trabajo de datos, y se puede planificar para octubre.'));

push(H1('Un detalle que salió al preparar esto'));
push(P('Buscando los nombres reales en el repositorio aparecieron, para el mismo producto, variantes como «Diplomado», «DIPLOMADO BIM», «Diplomado Arquitectos Ingenieros 4.0», «DIPLOMADO - NO SE USA» y «Diplomado (Nueva Comunidad)».'));
push(P('No es un problema del tutor, pero sí de esta lista: si el mismo curso se llama de tres formas según dónde se mire, cualquier renombrado va a dejar sitios sin actualizar. Vale la pena fijar un nombre oficial por producto antes de tocar nada, aunque sea en una hoja.'));

push(H1('Qué hace falta decidir'));
push(tabla(['Decisión','Quién'],[
 ['Aprobar o corregir los nombres del Grupo 1','Dayana'],
 ['Naves Industriales: ¿con tutor filtrado o sin tutor por ahora?','Dayana y Gabriel'],
 ['Fijar un nombre oficial por producto y dónde vive esa lista','Dayana'],
 ['¿Se transcriben los cursos del Máster para octubre?','Dayana y Gabriel'],
],[6400,2600]));

const doc=new Document({creator:'Design Modeling Academy',
  title:'Nombres de los cursos con el agente de IA',
  styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:1000,bottom:1000,left:1000,right:1000}}},children:h}]});
const OUT=path.resolve(__dirname,'..','matriz-viral','entregables','Nombres-de-Cursos-con-IA.docx');
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);
  console.log(`OK → ${path.relative(path.resolve(__dirname,'..'),OUT)} (${(b.length/1024).toFixed(0)} KB)`);});
