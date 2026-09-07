/* Plantilla de memoria de calculo, en Word y editable.
 * Las 13 secciones montadas, con el texto de apoyo dentro de cada una para
 * que el ingeniero borre y escriba encima.
 *   node scripts/build_memoria_plantilla.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
        PageBreak, TableOfContents } = require('docx');
const ROOT=path.dirname(__dirname);
const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', CODE='EEF2F6', WARN='FBF0DA';

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:380,after:140},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:28,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},alignment:o.center?AlignmentType.CENTER:undefined,
  children:[new TextRun({text:t,size:o.size||21,font:'Nunito',
    ...(o.color?{color:o.color}:{}),...(o.bold?{bold:true}:{}),...(o.italics?{italics:true}:{})})]});
/* La guia dentro de cada seccion: en gris y cursiva para que se vea que hay
   que borrarla. Si fuera del mismo color que el texto, se quedaria dentro de
   memorias entregadas — y eso ya pasa con las plantillas que circulan. */
const GUIA=t=>new Paragraph({spacing:{after:120},shading:{type:ShadingType.CLEAR,fill:CODE},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:19,font:'Nunito',color:GREY,italics:true})]});
const LI=t=>new Paragraph({bullet:{level:0},spacing:{after:60},
  children:[new TextRun({text:t,size:20,font:'Nunito',color:GREY,italics:true})]});
const RELLENA=()=>new Paragraph({spacing:{after:200},
  children:[new TextRun({text:'[ Escribe aquí ]',size:21,font:'Nunito',color:'B9C2CB'})]});

const celda=(t,{b=false,w=0,fill=null}={})=>new TableCell({width:{size:w,type:WidthType.DXA},
  ...(fill?{shading:{type:ShadingType.CLEAR,fill}}:{}),margins:{top:80,bottom:80,left:120,right:120},
  children:[new Paragraph({children:[new TextRun({text:t,bold:b,size:19,font:'Nunito'})]})]});
const tabla=(head,filas,anchos)=>new Table({columnWidths:anchos,width:{size:9200,type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:anchos[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      margins:{top:80,bottom:80,left:120,right:120},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:'FFFFFF',size:18,font:'Overpass'})]})]}))}),
    ...filas.map(f=>new TableRow({children:f.map((c,i)=>celda(c,{w:anchos[i]}))}))]});

const h=[];
// ── Portada ──────────────────────────────────────────────────────────────
h.push(new Paragraph({spacing:{before:1400,after:60},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:'MEMORIA DE CÁLCULO ESTRUCTURAL',bold:true,color:ORANGE,
    size:20,font:'Overpass',characterSpacing:80})]}));
h.push(new Paragraph({spacing:{after:400},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:'[ Nombre del proyecto ]',bold:true,color:NAVY,size:44,font:'Overpass'})]}));
h.push(tabla(['Campo','Contenido'],[
  ['Proyecto','[ nombre completo ]'],
  ['Ubicación','[ dirección, ciudad, país ]'],
  ['Promotor / cliente','[ nombre ]'],
  ['Autor de la memoria','[ nombre y número de registro profesional ]'],
  ['Fecha','[ dd/mm/aaaa ]'],
  ['Revisión','[ nº y motivo del cambio ]'],
],[3000,6200]));
h.push(GUIA('El número de revisión no es burocracia. Es lo que permite saber, dentro de seis meses, si el plano que está en obra corresponde a esta memoria o a la anterior. Cámbialo en cada emisión y anota el motivo.'));
h.push(new Paragraph({children:[new PageBreak()]}));

// ── Las 13 secciones ─────────────────────────────────────────────────────
const SEC = [
 ['1. Objeto y alcance',
  ['Di qué se calcula en este documento y —tan importante— qué NO se calcula aquí.',
   'La mayoría de discusiones con el revisor nacen en esta sección. Si la cimentación va en documento aparte, dilo aquí: si no, el revisor asume que falta.'], null],
 ['2. Normativa aplicable',
  ['Una norma por fila, con su nombre completo, su versión y su año. Nunca «la norma vigente» a secas dentro del cuerpo.',
   'Sin la versión, nada de lo que cuelga de esa norma se puede reproducir — y reproducirlo es exactamente lo que el revisor va a intentar.'],
  [['Norma (nombre completo)','Versión / año','Para qué se usa en este proyecto'],
   [['[ p. ej. NEC-SE-DS «Peligro sísmico y diseño sismorresistente» ]','[ año ]','[ verificaciones sísmicas, sección 11 ]'],
    ['[ ]','[ ]','[ ]'],['[ ]','[ ]','[ ]'],['[ ]','[ ]','[ ]']],
   [4200,1600,3400]]],
 ['3. Descripción del sistema estructural',
  ['Tipología, luces principales, número de niveles, sistema de resistencia a fuerzas laterales y juntas estructurales.',
   'Escríbelo como si el lector no hubiera visto los planos, porque la mitad de las veces los mira después de leer esto.'], null],
 ['4. Materiales y propiedades',
  ['Cada material con sus resistencias características, módulos y coeficientes, y la referencia de dónde sale cada valor.',
   'Un valor de resistencia sin la norma o el ensayo que lo respalda es una afirmación, no un dato.'],
  [['Material','Propiedad','Valor adoptado','Procedencia (norma o ensayo)'],
   [['[ hormigón / acero / … ]','[ f\'c, fy, E… ]','[ valor y unidad ]','[ norma, artículo o nº de ensayo ]'],
    ['[ ]','[ ]','[ ]','[ ]'],['[ ]','[ ]','[ ]','[ ]']],
   [2200,2200,2200,2600]]],
 ['5. Acciones consideradas',
  ['Cada carga con su valor Y su origen. «Sobrecarga de uso 200 kg/m²» está incompleto; con la categoría de uso y el artículo de la norma, está completo.'],
  [['Acción','Valor','Unidad','Origen (norma, artículo o criterio)'],
   [['Carga permanente','[ ]','[ ]','[ ]'],
    ['Sobrecarga de uso','[ ]','[ ]','[ categoría de uso, norma y artículo ]'],
    ['Viento','[ ]','[ ]','[ ]'],['Sismo','[ ]','[ ]','[ ]'],
    ['[ acción particular del proyecto ]','[ ]','[ ]','[ ]']],
   [2600,1500,1300,3800]]],
 ['6. Hipótesis y justificación',
  ['Por qué esas cargas y no otras. Qué se supuso sobre el terreno, sobre el uso y sobre lo que hará el edificio en 50 años.',
   'ESTA ES LA SECCIÓN QUE SEPARA UNA MEMORIA QUE SE DEFIENDE DE UNA QUE SE DEVUELVE. Es también la única que no se puede copiar del proyecto anterior — y justo por eso revela si la memoria se escribió o se recicló.'], null],
 ['7. Combinaciones de carga',
  ['Todas las combinaciones usadas, con sus coeficientes y su referencia normativa.',
   'Si las generó el software automáticamente, dilo y di cuál. El revisor necesita saber si las revisó una persona.'],
  [['Nº','Combinación','Referencia normativa'],
   [['1','[ p. ej. 1,2D + 1,6L ]','[ norma y artículo ]'],['2','[ ]','[ ]'],['3','[ ]','[ ]'],['4','[ ]','[ ]']],
   [800,4600,3800]]],
 ['8. Criterios de modelización',
  ['Software y versión, tipo de análisis, condiciones de apoyo — y qué se simplificó.',
   'Lo que más peso tiene aquí es lo que simplificaste. Toda simplificación es legítima si está declarada y justificada; ninguna lo es si el revisor la descubre solo al comparar con los planos.'],
  [['Aspecto','Qué se adoptó en este proyecto'],
   [['Software y versión','[ ]'],['Tipo de análisis','[ lineal / no lineal, estático / dinámico ]'],
    ['Condiciones de apoyo','[ ]'],['Simplificaciones declaradas','[ cuáles, y por qué son del lado de la seguridad ]']],
   [3000,6200]]],
 ['9. Análisis y resultados',
  ['Los valores que gobiernan cada verificación, no el listado completo del programa.',
   'Un anexo de 300 páginas del software no es un resultado: es un volcado. Lo que va en el cuerpo son los valores que mandan.'], null],
 ['10. Verificaciones · Estados límite últimos (ELU)',
  ['Resistencia, estabilidad y pandeo. Cada verificación con su solicitación, su resistencia y su ratio.',
   'Usa la hoja de Excel que acompaña a esta plantilla para el resumen, y trae aquí la tabla ya resuelta.'], null],
 ['11. Verificaciones · Estados límite de servicio (ELS)',
  ['Deflexiones, derivas de entrepiso, vibraciones y fisuración.',
   'ES LA SECCIÓN QUE MÁS SE OLVIDA Y LA QUE EL USUARIO DEL EDIFICIO NOTA PRIMERO. Una estructura puede cumplir resistencia y aun así ser inhabitable — y ese error se detecta cuando ya no hay nada que corregir en papel.'], null],
 ['12. Cimentación y terreno',
  ['Capacidad portante adoptada y de dónde sale, asientos previstos y tipo de cimentación.',
   'Si no hay estudio geotécnico, hay que decirlo y decir qué se supuso. Nunca dar un valor de capacidad portante sin decir su procedencia.'], null],
 ['13. Conclusiones y anexos',
  ['La declaración de cumplimiento CON LAS CONDICIONES bajo las que cumple, y los anexos referenciados desde el cuerpo.',
   '«Cumple» a secas no dice nada. «Cumple bajo las hipótesis de la sección 6 y con los materiales de la sección 4» sí dice algo, y además te protege.'], null],
];

SEC.forEach(([t,guias,tb])=>{
  h.push(H1(t));
  guias.forEach(g=>h.push(GUIA(g)));
  if(tb) h.push(tabla(tb[0],tb[1],tb[2]));
  h.push(RELLENA());
});

// ── Cierre ───────────────────────────────────────────────────────────────
h.push(new Paragraph({children:[new PageBreak()]}));
h.push(H1('Antes de emitir: la relectura'));
h.push(P('Léela una vez más con una sola pregunta en la cabeza:',{color:GREY}));
h.push(new Paragraph({spacing:{before:120,after:160},shading:{type:ShadingType.CLEAR,fill:WARN},
  children:[new TextRun({text:'¿Podría alguien llegar a estos números partiendo solo de lo que está escrito aquí, sin llamarme?',
    bold:true,size:23,font:'Overpass',color:'7A4A10'})]}));
h.push(P('Si la respuesta es sí, la memoria está completa. Si necesita llamarte, todavía no lo está — y ese hueco es exactamente lo que el revisor va a encontrar.',{color:GREY}));
h.push(H1('Comprobación final'));
[ 'Cada norma citada lleva su versión y su año.',
  'Cada carga lleva su origen, no solo su valor.',
  'Las simplificaciones del modelo están declaradas.',
  'Están las verificaciones de servicio, no solo las de resistencia.',
  'Cada número del cuerpo se puede rastrear hasta una carga y una combinación.',
  'El número de revisión y su motivo están actualizados.',
].forEach(x=>h.push(LI(x)));

h.push(new Paragraph({spacing:{before:400},
  children:[new TextRun({text:'Plantilla de estructura documental de Design Modeling Academy. No es un método de cálculo ni una norma, y no sustituye el criterio ni la responsabilidad del ingeniero que firma la memoria. La normativa aplicable, sus versiones vigentes y todos los valores de diseño los determina el profesional responsable del proyecto.',
    size:17,font:'Nunito',color:GREY,italics:true})]}));

const doc=new Document({styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:1000,bottom:1000,left:1000,right:1000}}},children:h}]});
const OUT=path.join(ROOT,'memoria-calculo/Plantilla-Memoria-de-Calculo-DMA.docx');
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);
  console.log(`OK → ${OUT} (${(b.length/1024).toFixed(0)} KB) · ${SEC.length} secciones`);});
