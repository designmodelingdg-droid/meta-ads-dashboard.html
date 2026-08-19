/**
 * Genera la guía de uso de la matriz de contenido, en Word.
 *
 *   node scripts/build_guia_matriz_docx.js
 *
 * POR QUÉ EXISTE
 *   El sistema de la matriz son cinco archivos encadenados y dos Actions. Eso
 *   se explica bien una vez en un chat y se olvida a la semana siguiente. Esta
 *   guía es la versión que se puede volver a abrir, imprimir y pasarle a quien
 *   entre nuevo al equipo.
 *
 *   Las cifras NO se escriben aquí: se leen de los mismos archivos que usa el
 *   generador del mes. Una guía con números viejos enseña mal.
 *
 * Requiere: npm i docx
 */
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,ShadingType,PageBreak,
Table,TableRow,TableCell,WidthType}=require('docx');
const fs=require('fs'), path=require('path');

const ROOT=path.resolve(__dirname,'..');
const NAVY="0E2438", ORANGE="C96A1C", GREY="5A6B7B", LIGHT="F4F7FA", BOX="F7F9FB";

const leer=rel=>{try{return JSON.parse(fs.readFileSync(path.join(ROOT,rel),'utf8'));}catch(e){return null;}};
const MATRIZ=leer('matriz-viral/matriz/matriz.json');
const GUI=leer('matriz-viral/matriz/guiones-completos.json');
const ADS=leer('matriz-viral/fuentes/ads-insights/por-campana.json');

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:140},
  children:[new TextRun({text:t,color:NAVY,bold:true})]});
const H2=t=>new Paragraph({spacing:{before:280,after:100},
  children:[new TextRun({text:t,color:ORANGE,bold:true,size:26})]});
const P=(t,o={})=>new Paragraph({spacing:{after:90},...o,
  children:[new TextRun({text:t,size:21,...(o.run||{})})]});
const bul=t=>new Paragraph({bullet:{level:0},spacing:{after:50},
  children:[new TextRun({text:t,size:21})]});
const note=t=>new Paragraph({spacing:{after:120},shading:{type:ShadingType.CLEAR,fill:LIGHT},
  border:{left:{style:BorderStyle.SINGLE,size:18,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:20,italics:true,color:GREY})]});
const code=t=>t.split('\n').map((l,i,a)=>new Paragraph({
  shading:{type:ShadingType.CLEAR,fill:BOX},spacing:{after:i===a.length-1?140:0},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"B9C6D3",space:8}},
  children:[new TextRun({text:l||" ",size:18,font:"Consolas"})]}));
const tbl=(head,rows,widths)=>new Table({columnWidths:widths,
  width:{size:widths.reduce((a,b)=>a+b),type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:"FFFFFF",size:18})]})]}))}),
    ...rows.map(r=>new TableRow({children:r.map((c,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},
      children:String(c).split('\n').map(line=>new Paragraph({
        children:[new TextRun({text:line,size:18})]}))}))}))]});

const b=[]; const push=(...x)=>x.flat().forEach(p=>b.push(p));

/* ── PORTADA ── */
push(new Paragraph({spacing:{after:40},
  children:[new TextRun({text:"DESIGN MODELING ACADEMY",color:ORANGE,bold:true,size:20})]}));
push(new Paragraph({heading:HeadingLevel.TITLE,spacing:{after:80},
  children:[new TextRun({text:"Cómo funciona la matriz de contenido",color:NAVY,bold:true})]}));
push(new Paragraph({spacing:{after:200},
  children:[new TextRun({text:"Guía de uso · qué es cada archivo, quién lo actualiza y cómo se saca el documento del mes",
    color:GREY,italics:true,size:22})]}));
push(P("Esta guía explica el sistema completo: de dónde salen los números, cómo se decide qué se publica cada día, y qué comando genera el Word que usa el equipo."));
push(note("Cómo pedirlo en el chat: escribe /matriz-mensual, o simplemente «vamos a generar la matriz». No hace falta abrir el repositorio ni acordarse de ningún comando."));

/* ── 1 · EL SISTEMA ── */
push(H1("1 · El sistema, en cinco piezas"));
push(P("Cada una alimenta a la siguiente. Entender esta cadena es entender la matriz entera:"));
push(...code(
"  matriz.json              lo que PASÓ\n"+
"       ↓                   métricas reales de Meta, pieza por pieza\n"+
"  patrones-de-viralidad    por qué pasó\n"+
"       ↓                   qué formato y qué eje funcionan\n"+
"  guiones-completos.json   qué vamos a publicar\n"+
"       ↓                   cada pieza escrita palabra por palabra\n"+
"  calendario-<mes>.json    cuándo y dónde\n"+
"       ↓                   qué pieza, qué día, en qué red\n"+
"  build_matriz_docx.js     el entregable\n"+
"                           → el Word del mes"));

push(tbl(["Archivo","Qué guarda","Estado hoy"],[
 ["matriz.json","Cada publicación con sus métricas reales, su eje y su estructura",
  MATRIZ?`${MATRIZ.total_reels} piezas · refrescado ${MATRIZ.actualizado||MATRIZ.generado}`:"no disponible"],
 ["patrones-de-viralidad.md","El análisis: qué funciona y por qué","se revisa cada semana"],
 ["guiones-completos.json","El contenido escrito de cada pieza, con CTA por red",
  GUI?`${GUI.total||GUI.piezas.length} piezas listas`:"no disponible"],
 ["calendario-<mes>.json","El orden de publicación del mes","uno por mes"],
 ["fuentes/ads-insights/","Gasto, leads y CPL reales de las campañas",
  ADS?`${(ADS.filas||[]).length} campañas · ventana ${(ADS.ventana||{}).desde||'—'} → ${(ADS.ventana||{}).hasta||'—'}`:"no disponible"],
],[3000,5000,3400]));

push(note("REGLA DE ORO: nada se escribe a mano en el Word. Si un dato está mal, se corrige en su archivo y se vuelve a generar. Lo que se edite directamente en el Word se pierde en la siguiente corrida."));

/* ── 2 · QUIÉN ACTUALIZA QUÉ ── */
push(H1("2 · Quién actualiza cada cosa"));
push(P("La mitad del sistema se mantiene solo. Conviene saber qué mitad:"));
push(tbl(["Qué","Quién","Cada cuánto"],[
 ["matriz.json (métricas orgánicas)","Action «Métricas semanales», por la Graph API de Meta","lunes y viernes"],
 ["fuentes/ads-insights/ (pauta)","La misma Action","lunes y viernes"],
 ["fuentes/ingresos/ (Stripe + PayPal)","La misma Action","lunes y viernes"],
 ["guiones-completos.json","A mano, cuando se escribe contenido nuevo","según haga falta"],
 ["calendario-<mes>.json","El skill matriz-mensual","una vez al mes"],
 ["El eje de cada pieza nueva","A mano: ninguna API lo sabe","cada semana"],
],[4200,4900,2300]));
push(note("Si la matriz lleva más de una semana sin refrescarse, se corre a mano en Actions → Métricas semanales → Run workflow. El documento avisa de la fecha del dato en cada sección."));

/* ── 3 · DÓNDE LO VE EL EQUIPO ── */
push(H1("3 · Dónde lo ve el equipo"));
push(P("Al fusionar los cambios, la Action «publish-matriz» deja el calendario y los guiones en una dirección pública. No hay que mandarle archivos a nadie:"));
push(...code("https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/matriz.json"));
push(bul("Patricio lee siempre la última versión en ese enlace."));
push(bul("El asistente de WhatsApp lee esa misma fuente, así que nunca se contradicen."));
push(bul("Si alguien dice que ve datos viejos, lo primero es comprobar que la Action corrió — no volver a exportar nada."));

/* ── 4 · CÓMO SE DECIDE EL MES ── */
push(new Paragraph({children:[new PageBreak()]}));
push(H1("4 · Cómo se decide qué se publica cada día"));
push(P("Estas reglas no son de estilo: salen del análisis de las publicaciones reales de la cuenta."));
push(bul("Ritmo: 3-4 piezas por semana, 18 al mes. Más que eso no se sostiene."));
push(bul("Mínimo 60% de núcleo (BIM · IA · modelado · acero). Cero obra en el calendario."));
push(bul("Los carruseles abren semana: es el formato de mejor engagement."));
push(bul("Los reels se agrupan en dos días de grabación, no repartidos por todo el mes."));
push(bul("Un slot de venta por semana, los jueves, en historias. Nunca más de uno."));
push(bul("Un blog por semana, el sábado, anunciado con un post que lleva el enlace."));
push(bul("No se repite una pieza ya usada otro mes."));

push(H2("Por qué el núcleo y no la obra"));
if(MATRIZ&&MATRIZ.reels&&MATRIZ.reels.length){
  const R=MATRIZ.reels, tv=R.reduce((t,r)=>t+(r.views||0),0);
  const eje={}; R.forEach(r=>{const e=r.eje||'sin clasificar';
    eje[e]=eje[e]||{p:0,v:0}; eje[e].p++; eje[e].v+=r.views||0;});
  push(tbl(["Eje","% de las piezas","% del alcance"],
    Object.entries(eje).sort((a,b)=>b[1].v-a[1].v).map(([e,d])=>
      [e,(100*d.p/R.length).toFixed(0)+"%",(tv?(100*d.v/tv).toFixed(1):"0")+"%"]),
    [4600,3300,3500]));
  push(note("El alcance de OBRA no compra: quien compra el Máster es quien modela desde la computadora. El formato viral funciona; lo que hay que mover es el tema."));
}else{
  push(P("(La matriz no está disponible para calcular el reparto por eje.)",{run:{italics:true,color:GREY}}));
}

/* ── 5 · SACAR EL DOCUMENTO ── */
push(H1("5 · Sacar el documento del mes"));
push(P("En el chat basta con pedirlo. Por dentro, esto es lo que corre:"));
push(...code("npm i docx                                    # solo la primera vez\n"+
             "node scripts/build_matriz_docx.js --mes 2026-09"));
push(P("Sin --mes coge el calendario más reciente. El archivo sale en matriz-viral/entregables/."));
push(H2("Las diez secciones del Word"));
push(tbl(["#","Sección","De dónde sale"],[
 ["1","Las reglas del mes","del calendario del mes"],
 ["2","Los CTA del mes","fijo, por producto"],
 ["3","Qué está trayendo clientes (pauta real)","fuentes/ads-insights + ingresos"],
 ["4","Cómo va el contenido","matriz.json"],
 ["5","Calendario de un vistazo","del calendario del mes"],
 ["6","Desarrollo completo, pieza por pieza","guiones-completos.json"],
 ["7","Historias","guiones-completos.json"],
 ["8","Venta y pauta (copy de anuncios)","guiones-completos.json"],
 ["9","Banco de reserva","del calendario del mes"],
 ["10","Resumen y checklist","calculado"],
],[700,5200,5500]));
push(note("Las secciones 3 y 4 se recalculan en cada corrida, por eso no envejecen. Si falta una fuente, el documento lo dice en rojo en vez de rellenar el hueco: un documento que no avisa de lo que le falta se lee como completo."));

/* ── 6 · REGLAS ── */
push(H1("6 · Reglas que no se rompen"));
push(bul("Nada se escribe a mano en el Word. Se corrige el origen y se regenera."));
push(bul("Una pieza sin id en guiones-completos.json no entra al calendario: antes hay que escribirla."));
push(bul("El precio del Máster no aparece en ninguna pieza. El de ACERO sí puede ir en correo a lista propia y en DM."));
push(bul("El número de cupos se actualiza cada vez que se publica. Nunca se inventa: esa gente vuelve al mes siguiente a comprobarlo."));
push(bul("Toda afirmación técnica sobre un software se verifica en la documentación oficial ANTES de publicar."));
push(bul("Las historias de venta no se publican hasta que el disparador de DM del bot esté montado para su palabra clave."));
push(bul("Si falta un dato, se dice. No se rellena de memoria."));

/* ── SALIDA ── */
const doc=new Document({styles:{default:{document:{run:{font:"Calibri"}}}},
 sections:[{properties:{page:{size:{width:12240,height:15840},
   margin:{top:900,bottom:900,left:900,right:900}}},children:b}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/Guia-Matriz-de-Contenido-DMA.docx');
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync(OUT,buf);
  console.log(`OK → ${OUT} (${(buf.length/1024).toFixed(0)} KB)`);});
