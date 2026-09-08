/* Plantilla de memoria de calculo, en Word y editable.
 *
 * La estructura NO es teorica: sale de una memoria real de Robot Structural
 * Analysis revisada por Gabriel (proyecto tipo, hormigon armado, NEC-SE-DS),
 * cruzada seccion por seccion en septiembre de 2026. Lo que cambio respecto a
 * la primera version esta anotado en cada sitio con "[cruce]".
 *
 *   node scripts/build_memoria_plantilla.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
        PageBreak } = require('docx');
const ROOT=path.dirname(__dirname);
const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', CODE='EEF2F6', WARN='FBF0DA';

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:380,after:140},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:28,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},alignment:o.center?AlignmentType.CENTER:undefined,
  children:[new TextRun({text:t,size:o.size||21,font:'Nunito',
    ...(o.color?{color:o.color}:{}),...(o.bold?{bold:true}:{}),...(o.italics?{italics:true}:{})})]});
/* La guia dentro de cada seccion va en gris y cursiva para que se vea que hay
   que borrarla. Si fuera del mismo color que el texto, se quedaria dentro de
   memorias entregadas — y eso ya pasa con las plantillas que circulan. */
const GUIA=t=>new Paragraph({spacing:{after:120},shading:{type:ShadingType.CLEAR,fill:CODE},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:19,font:'Nunito',color:GREY,italics:true})]});
const LI=t=>new Paragraph({bullet:{level:0},spacing:{after:60},
  children:[new TextRun({text:t,size:20,font:'Nunito',color:GREY,italics:true})]});
const RELLENA=()=>new Paragraph({spacing:{after:200},
  children:[new TextRun({text:'[ Escribe aquí ]',size:21,font:'Nunito',color:'B9C2CB'})]});
const FIG=t=>new Paragraph({spacing:{before:60,after:200},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:t,size:18,font:'Nunito',color:'B9C2CB',italics:true})]});

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
h.push(new Paragraph({spacing:{before:1200,after:60},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:'MEMORIA DE CÁLCULO ESTRUCTURAL',bold:true,color:ORANGE,
    size:20,font:'Overpass',characterSpacing:80})]}));
h.push(new Paragraph({spacing:{after:340},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:'[ Nombre del proyecto ]',bold:true,color:NAVY,size:44,font:'Overpass'})]}));
h.push(tabla(['Campo','Contenido'],[
  ['Proyecto','[ nombre completo ]'],
  ['Ubicación','[ parroquia, cantón, provincia ]'],
  ['Estructura','[ p. ej. Estructura de hormigón armado ]'],
  ['N.º de niveles','[ n ]'],
  ['Área total','[ m² ]'],
  ['Propietario','[ nombre ]'],
  ['Responsabilidad técnica','[ Ing. nombre — Registro Senescyt n.º ]'],
  ['Fecha','[ mes y año ]'],
  ['Revisión','[ n.º y motivo del cambio ]'],
],[3000,6200]));
h.push(GUIA('[cruce] El número de niveles y el área van en la portada. Son lo primero que mira un revisor para ubicarse, y evitan tener que buscarlos dentro. El registro profesional en Ecuador es el Registro Senescyt: ponlo con su número, no como «registro profesional».'));
h.push(GUIA('El número de revisión no es burocracia. Es lo que permite saber, dentro de seis meses, si el plano que está en obra corresponde a esta memoria o a la anterior. Cámbialo en cada emisión y anota el motivo.'));
h.push(new Paragraph({children:[new PageBreak()]}));

h.push(H1('Tabla de contenidos'));
h.push(GUIA('[cruce] Va siempre, y se actualiza antes de emitir. En Word: Referencias → Tabla de contenido. Una memoria de 40 páginas sin índice obliga al revisor a buscar, y lo que cuesta buscar se pregunta.'));
h.push(RELLENA());
h.push(new Paragraph({children:[new PageBreak()]}));

// ── Las secciones ────────────────────────────────────────────────────────
const SEC = [
 ['1. Objetivo y alcance',
  ['Di qué se calcula en este documento, CON QUÉ SOFTWARE Y VERSIÓN, y de qué estudios externos parte —el de mecánica de suelos, sobre todo, con el nombre de quién lo hizo.',
   '[cruce] Nombrar aquí el estudio de suelos y su autor es mejor que dejarlo para la sección de cimentación: el revisor sabe desde la primera página qué es tuyo y qué viene de un tercero.',
   'Di también qué NO se calcula aquí. Si la cimentación va en documento aparte, dilo: si no, el revisor asume que falta.'], null],

 ['2. Proceso de cálculo',
  ['La cadena que lleva de la ubicación al sistema estructural, en este orden: dónde está el proyecto → qué nivel de amenaza sísmica le corresponde → qué uso tendrá → qué coeficiente de importancia le asigna la norma → qué sistema estructural se adoptó.',
   '[cruce] Esta sección no estaba en la primera versión y es la que más rápido orienta al revisor. Cada eslabón lleva su referencia: «según la Tabla X de la NEC-SE-DS», no «según la norma».',
   'Cierra diciendo si el diseño se ajustó a criterios del cliente o a la propuesta arquitectónica, y en qué.'], null],

 ['3. Análisis y diseño estructural',
  ['Por qué se usó el método que se usó (elementos finitos, análisis dinámico) y con qué programa.',
   'Y la tabla de elementos: qué es cada miembro y con qué sección entró al modelo.'],
  [['Miembro','Descripción y sección'],
   [['Sistema de losas','[ p. ej. losa aligerada en dos direcciones, e = 20 cm ]'],
    ['Columnas','[ material y sección ]'],
    ['Vigas principales (X)','[ material y sección ]'],
    ['Vigas principales (Y)','[ material y sección ]'],
    ['Vigas banda / nervios','[ material y sección ]'],
    ['[ otro ]','[ ]']],
   [3000,6200]]],

 ['4. Marco teórico — normas aplicadas',
  ['Una norma por fila, con su nombre completo, su versión y su año. Nunca «la norma vigente» a secas dentro del cuerpo.',
   'Sin la versión, nada de lo que cuelga de esa norma se puede reproducir — y reproducirlo es exactamente lo que el revisor va a intentar.'],
  [['Norma (nombre completo)','Versión / año','Para qué se usa aquí'],
   [['[ p. ej. NEC-SE-DS «Peligro sísmico y diseño sismorresistente» ]','[ año ]','[ análisis sísmico, sección 8 ]'],
    ['[ p. ej. NEC-SE-HM «Estructuras de hormigón armado» ]','[ año ]','[ ]'],
    ['[ p. ej. NEC «Cargas no sísmicas» ]','[ año ]','[ ]'],
    ['[ p. ej. ACI 318 ]','[ edición ]','[ ]']],
   [4200,1600,3400]]],

 ['5. Parámetros asumidos',
  ['Materiales con sus resistencias, y las secciones adoptadas por tipo de elemento.',
   'Un valor de resistencia sin la norma o el ensayo que lo respalda es una afirmación, no un dato.'],
  [['Material o elemento','Propiedad','Valor adoptado','Procedencia'],
   [['Hormigón',"f'c",'[ kg/cm² ]','[ norma o ensayo ]'],
    ['Acero de refuerzo','fy','[ kg/cm² ]','[ p. ej. ASTM A615 Gr.60 ]'],
    ['[ elemento ]','Sección','[ cm × cm ]','[ criterio adoptado ]'],
    ['[ ]','[ ]','[ ]','[ ]']],
   [2400,1800,2200,2800]]],

 ['6. Análisis de cargas',
  ['Cargas muertas, vivas y efectos sísmicos. Cada carga con su valor Y su origen: «sobrecarga de uso 200 kg/m²» está incompleto; con la categoría de uso y el artículo de la norma, está completo.',
   'En los efectos sísmicos van: zona sísmica, valor Z, caracterización del peligro, tipo de suelo, coeficientes Fa, Fd y Fs, períodos To y Tc, y el factor R con su justificación de irregularidades (φP y φE).'],
  [['Acción / parámetro','Valor','Unidad','Origen (norma, artículo o criterio)'],
   [['Peso propio','[ ]','[ ]','[ calculado por el programa ]'],
    ['Sobrecarga permanente','[ ]','kg/m²','[ norma y tabla ]'],
    ['Carga viva','[ ]','kg/m²','[ ocupación, norma y tabla ]'],
    ['Zona sísmica','[ ]','—','[ mapa de la norma ]'],
    ['Z','[ ]','g','[ ]'],
    ['Tipo de suelo','[ ]','—','[ estudio de suelos ]'],
    ['Fa / Fd / Fs','[ ]','—','[ ]'],
    ['R','[ ]','—','[ tabla y sistema estructural ]']],
   [2800,1400,1200,3800]]],

 ['7. Cálculo del cortante basal',
  ['La tabla completa de coeficientes y el cortante que resulta.',
   '[cruce] Esta sección no estaba en la primera versión y en Ecuador es obligada: el revisor la busca por su nombre. Si va escondida dentro de «resultados», parece que falta.',
   'OJO con la fila «tipo de estructura»: Ct y α dependen de ella, y es donde más se cuela un valor del proyecto anterior.'],
  [['Parámetro','Nomenclatura','Valor'],
   [['Coeficiente de importancia','I','[ ]'],
    ['Tipo de estructura','—','[ descríbelo tal como lo pide la tabla de la norma ]'],
    ['Coeficiente del tipo de edificio','Ct','[ ]'],
    ['Exponente','α','[ ]'],
    ['Altura de la edificación','hn','[ m ]'],
    ['Período de vibración','Ta','[ s ]'],
    ['Aceleración espectral','Sa','[ g ]'],
    ['Cortante basal','V','[ ]']],
   [4400,1800,3000]]],

 ['8. Análisis modal',
  ['Los períodos de los primeros modos y la participación de masas acumulada.',
   '[cruce] Tampoco estaba, y es lo que justifica que el modelo dinámico sea válido. Si la participación de masas no llega al mínimo que pide la norma, el análisis no vale por muchos resultados que salgan después.'],
  [['Modo','Período (s)','Participación X (%)','Participación Y (%)'],
   [['1','[ ]','[ ]','[ ]'],['2','[ ]','[ ]','[ ]'],['3','[ ]','[ ]','[ ]'],
    ['Acumulada','—','[ ]','[ ]']],
   [1600,2400,2600,2600]]],

 ['9. Combinaciones de carga',
  ['Todas las combinaciones usadas, con su referencia normativa. Y di CUÁL resultó crítica y en qué dirección.',
   'Si las generó el software automáticamente, dilo y di cuál. El revisor necesita saber si las revisó una persona.'],
  [['N.º','Combinación','Referencia normativa'],
   [['1','[ p. ej. 1,2D + 1,6L ]','[ norma y artículo ]'],['2','[ ]','[ ]'],
    ['3','[ ]','[ ]'],['Crítica','[ cuál y en qué dirección ]','[ ]']],
   [900,4500,3800]]],

 ['10. Verificación de secciones y resultados',
  ['Elemento por elemento, empezando por el más crítico: solicitación, resistencia y ratio.',
   '[cruce] Cierra CADA elemento con una conclusión concreta y accionable —«todas las vigas en dirección Y se dimensionan 30×40, con 4 varillas de 16 mm; el resto va en planos»—. Así lo hace la memoria de referencia, y es lo que convierte una tabla en una instrucción.',
   'Usa la hoja de Excel que acompaña a esta plantilla y trae aquí la tabla ya resuelta.'], null],

 ['11. Limitación de daños',
  ['Las derivas de piso en ambas direcciones, elásticas e inelásticas, contra el límite de la norma.',
   '[cruce] Este es el nombre que usa la NEC y el que busca un revisor ecuatoriano. En la primera versión se llamaba «estados límite de servicio», que es correcto en general pero no es como se titula aquí.',
   'ES LA SECCIÓN QUE MÁS SE OLVIDA Y LA QUE EL USUARIO DEL EDIFICIO NOTA PRIMERO. Una estructura puede cumplir resistencia y aun así ser inhabitable.'],
  [['Dirección','Deriva elástica','R','Deriva inelástica','Límite','Observación'],
   [['X','[ ]','[ ]','[ % ]','[ % ]','[ Cumple / No cumple ]'],
    ['Y','[ ]','[ ]','[ % ]','[ % ]','[ Cumple / No cumple ]']],
   [1500,1700,700,1800,1500,2000]]],

 ['12. Conclusiones',
  ['La declaración de cumplimiento CON LAS CONDICIONES bajo las que cumple: qué secciones, qué espectro, qué hipótesis.',
   '«Cumple» a secas no dice nada. «Cumple bajo las hipótesis de la sección 6 y con los materiales de la sección 5» sí dice algo, y además te protege.',
   'Cierra con la firma y el Registro Senescyt.'], null],
];

SEC.forEach(([t,guias,tb])=>{
  h.push(H1(t));
  guias.forEach(g=>h.push(GUIA(g)));
  if(tb) h.push(tabla(tb[0],tb[1],tb[2]));
  h.push(RELLENA());
  h.push(FIG('Figura N.º [ n ] — [ descripción ]'));
});

// ── Convencion de figuras y tablas ───────────────────────────────────────
h.push(new Paragraph({children:[new PageBreak()]}));
h.push(H1('Figuras y tablas: la convención'));
h.push(GUIA('[cruce] La memoria de referencia se apoya en 48 figuras —capturas del modelo, secciones, espectros, derivas—. Sin ellas el texto no se sostiene, y con ellas mal numeradas el revisor se pierde.'));
h.push(P('Tres reglas, y las tres se rompen solas cuando se copia de un proyecto anterior:'));
[ 'Numeración CORRELATIVA y sin repetir. En la memoria de referencia hay siete números de figura usados dos veces y un salto del 16 al 19: pasa al insertar figuras nuevas y no renumerar.',
  'Cada figura y cada tabla se CITA desde el texto antes de aparecer. Una figura que nadie menciona es una figura que nadie mira.',
  'El pie dice qué se está viendo Y de dónde sale: «Figura N.º 7 — Columnas en 3D, Robot Structural Analysis 2019».',
].forEach(x=>h.push(LI(x)));

// ── Relectura ────────────────────────────────────────────────────────────
h.push(H1('Antes de emitir: la relectura'));
h.push(P('Léela una vez más con una sola pregunta en la cabeza:',{color:GREY}));
h.push(new Paragraph({spacing:{before:120,after:160},shading:{type:ShadingType.CLEAR,fill:WARN},
  children:[new TextRun({text:'¿Podría alguien llegar a estos números partiendo solo de lo que está escrito aquí, sin llamarme?',
    bold:true,size:23,font:'Overpass',color:'7A4A10'})]}));
h.push(P('Si la respuesta es sí, la memoria está completa. Si necesita llamarte, todavía no lo está — y ese hueco es exactamente lo que el revisor va a encontrar.',{color:GREY}));

h.push(H1('Comprobación final'));
h.push(P('Los cuatro primeros puntos salen de errores encontrados en una memoria real. No son hipotéticos.',{color:GREY,italics:true}));
[ 'EL MATERIAL ES EL MISMO EN TODO EL DOCUMENTO. Si la estructura es de hormigón, que no quede ni una frase hablando de perfiles de acero — ni en el objetivo, ni en las conclusiones.',
  'EL SOFTWARE ES EL MISMO EN TODO EL DOCUMENTO, pies de tabla incluidos.',
  'EL TIPO DE SUELO COINCIDE entre el texto, la tabla de coeficientes y la tabla del cortante basal.',
  'LA UBICACIÓN ES CORRECTA: cantón y provincia, verificados.',
  'Cada norma citada lleva su versión y su año.',
  'Cada carga lleva su origen, no solo su valor.',
  'Las figuras van correlativas y todas están citadas desde el texto.',
  'Está la sección de limitación de daños, no solo las de resistencia.',
  'Cada número del cuerpo se puede rastrear hasta una carga y una combinación.',
  'El número de revisión y su motivo están actualizados.',
].forEach(x=>h.push(LI(x)));

h.push(new Paragraph({spacing:{before:400},
  children:[new TextRun({text:'Plantilla de estructura documental de Design Modeling Academy. Su estructura se cruzó contra una memoria real de proyecto tipo revisada por el equipo académico. No es un método de cálculo ni una norma, y no sustituye el criterio ni la responsabilidad del ingeniero que firma la memoria. La normativa aplicable, sus versiones vigentes y todos los valores de diseño los determina el profesional responsable del proyecto.',
    size:17,font:'Nunito',color:GREY,italics:true})]}));

const doc=new Document({styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:1000,bottom:1000,left:1000,right:1000}}},children:h}]});
const OUT=path.join(ROOT,'memoria-calculo/Plantilla-Memoria-de-Calculo-DMA.docx');
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);
  console.log(`OK → ${OUT} (${(b.length/1024).toFixed(0)} KB) · ${SEC.length} secciones`);});
