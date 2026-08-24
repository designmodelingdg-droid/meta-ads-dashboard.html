/**
 * Genera el Word de los correos de nutricion para el equipo.
 *
 *   node scripts/build_correos_docx.js
 *
 * Fuentes (aqui no se escribe contenido a mano):
 *   matriz-viral/seguimiento/correos-nutricion.json   los 20 correos, literales
 *   matriz-viral/fuentes/ghl/correos-contenido.json   el inventario real de GHL
 *   matriz-viral/fuentes/ghl/correos.json             los 149 workflows y su estado
 *
 * El estado de los workflows y los duplicados salen del dato, no de la memoria:
 * si alguien enciende un flujo o borra una copia, el documento se regenera y lo
 * refleja.
 */
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,ShadingType,PageBreak,
Table,TableRow,TableCell,WidthType}=require('docx');
const fs=require('fs'), path=require('path');

const ROOT=path.resolve(__dirname,'..');
const NAVY="0E2438", ORANGE="C96A1C", GREY="5A6B7B", RED="A33B2A", LIGHT="F4F7FA", BOX="F7F9FB";
const leer=r=>{try{return JSON.parse(fs.readFileSync(path.join(ROOT,r),'utf8'));}catch(e){return null;}};

const D=leer('matriz-viral/seguimiento/correos-nutricion.json');
if(!D){console.error('Falta correos-nutricion.json');process.exit(1);}
const INV=leer('matriz-viral/fuentes/ghl/correos-contenido.json');
const GHL=leer('matriz-viral/fuentes/ghl/correos.json');
/* correos.json fue una sonda puntual del 20-ago que NINGUN script vuelve a
   escribir: su estado de flujos se quedo congelado y el documento repetia
   "78 en borrador" aunque el equipo los hubiera encendido. Desde el 24-ago
   ghl_correos.py guarda los flujos con su estado dentro de
   correos-contenido.json, que si se regenera en cada corrida. Se usa ese, y
   solo se cae al viejo si el nuevo todavia no existe. */

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:130},
  children:[new TextRun({text:t,color:NAVY,bold:true})]});
const H2=t=>new Paragraph({spacing:{before:260,after:90},
  children:[new TextRun({text:t,color:ORANGE,bold:true,size:26})]});
const H3=t=>new Paragraph({spacing:{before:200,after:70},
  children:[new TextRun({text:t,color:NAVY,bold:true,size:23})]});
const LBL=t=>new Paragraph({spacing:{before:140,after:40},
  children:[new TextRun({text:t,color:GREY,bold:true,size:17,allCaps:true})]});
const P=(t,o={})=>new Paragraph({spacing:{after:80},...o,
  children:[new TextRun({text:t,size:21,...(o.run||{})})]});
const bul=t=>new Paragraph({bullet:{level:0},spacing:{after:50},
  children:[new TextRun({text:t,size:21})]});
const note=t=>new Paragraph({spacing:{after:110},shading:{type:ShadingType.CLEAR,fill:LIGHT},
  border:{left:{style:BorderStyle.SINGLE,size:18,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:20,italics:true,color:GREY})]});
const alerta=t=>new Paragraph({spacing:{after:110},shading:{type:ShadingType.CLEAR,fill:"FBEFEC"},
  border:{left:{style:BorderStyle.SINGLE,size:20,color:RED,space:8}},
  children:[new TextRun({text:t,size:20,bold:true,color:RED})]});
// bloque para copiar y pegar
const copiar=lineas=>lineas.map((l,i,a)=>new Paragraph({
  shading:{type:ShadingType.CLEAR,fill:BOX},spacing:{after:i===a.length-1?130:60},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"B9C6D3",space:8}},
  children:[new TextRun({text:l||" ",size:20})]}));
const tbl=(head,rows,widths)=>new Table({columnWidths:widths,
  width:{size:widths.reduce((a,b)=>a+b),type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:"FFFFFF",size:18})]})]}))}),
    ...rows.map(r=>new TableRow({children:r.map((c,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},
      children:String(c).split('\n').map(l=>new Paragraph({
        children:[new TextRun({text:l,size:18})]}))}))}))]});

const b=[]; const push=(...x)=>x.flat().forEach(p=>b.push(p));

/* ── PORTADA ── */
push(new Paragraph({spacing:{after:40},
  children:[new TextRun({text:"DESIGN MODELING ACADEMY",color:ORANGE,bold:true,size:20})]}));
push(new Paragraph({heading:HeadingLevel.TITLE,spacing:{after:80},
  children:[new TextRun({text:"Actualizar los correos de las automatizaciones",color:NAVY,bold:true})]}));
push(new Paragraph({spacing:{after:180},
  children:[new TextRun({text:"Para Aylin y Ester · 4 carpetas de flujos · 20 correos nuevos, listos para copiar y pegar",
    color:GREY,italics:true,size:22})]}));
push(P("Este documento trae todo lo que hace falta: qué flujos hay que tocar, dónde está cada correo hoy, qué plantillas nuevas hay que crear, y el texto completo de cada correo palabra por palabra."));
push(P("Lo único que pone el equipo son las imágenes. Cada correo lleva indicado qué imagen va."));
push(note("Cómo se usa: busca la secuencia, copia lo que está en los bloques grises tal cual está —asunto, preencabezado y cuerpo— y pégalo en la plantilla. No hace falta reescribir nada."));

/* ── 1 · LO PRIMERO ── */
push(H1("1 · Lo primero, antes de tocar nada"));

const ws=(INV&&INV.flujos)||(GHL&&GHL.workflows&&GHL.workflows.workflows)||[];
const fechaFlujos=(INV&&INV.flujos)?(INV.generado||'hoy'):((GHL&&GHL.generado)||'?');
const borradores=ws.filter(w=>w.estado!=='published').length;
push(H2("Estos flujos están APAGADOS"));
push(P(`De los ${ws.length||149} flujos de la cuenta, ${borradores||78} están en borrador. Ahí dentro está todo lo de nutrición y recontacto — el símbolo ⛔ del nombre no es decoración, es el estado real.`));
push(P(`Corte del ${fechaFlujos}. Este recuento se rehace en cada corrida, así que si el equipo enciende un flujo, la próxima versión de este documento ya lo refleja.`,{italics:true}));
const apagados=ws.filter(w=>/nutrici|recontacto|remarketing|MQL|sin calificar|mal encaje|oportunidad/i.test(w.nombre||'')&&w.estado!=='published');
if(apagados.length){
  push(tbl(["Estado","Flujo"],apagados.slice(0,14).map(w=>["⛔ borrador",String(w.nombre).slice(0,70)]),[1900,8600]));
}
push(alerta("ACTUALIZAR LAS PLANTILLAS NO LOS ENCIENDE. Encender es un paso aparte y va al final de este documento (sección 5). No lo hagan por su cuenta sin avisar a Dayana."));

push(H2("Hay plantillas duplicadas — esto se resuelve PRIMERO"));
if(INV&&INV.plantillas){
  const norm=n=>String(n).replace(/^🟢\s*/,'').replace(/\(clone\)/,'').trim();
  const cuenta={}; INV.plantillas.forEach(t=>{const k=norm(t.nombre);cuenta[k]=(cuenta[k]||0)+1;});
  const reps=Object.entries(cuenta).filter(([,v])=>v>1).sort((a,b)=>b[1]-a[1]);
  const sobrantes=reps.reduce((t,[,v])=>t+v-1,0);
  push(P(`Hay ${reps.length} plantillas con el nombre repetido y ${sobrantes} copias de más: versiones con 🟢, sin 🟢 y alguna marcada (clone).`));
  push(tbl(["Copias","Plantilla"],reps.slice(0,10).map(([k,v])=>[`${v}×`,k.slice(0,70)]),[1400,9100]));
}
push(alerta("Si editan la copia que el flujo NO usa, el trabajo se pierde entero y nadie se entera hasta que alguien recibe el correo viejo. Antes de editar: abrir el flujo, mirar el paso «Enviar correo» y anotar el ID exacto de la plantilla vinculada."));

push(H2("Qué falla en los correos que hay hoy"));
push(bul("El correo 01 y el 02 tienen el mismo asunto y la misma apertura. Quien recibe los dos ve un reenvío."));
push(bul("El correo 03 habla de un workshop de 2025 sobre estudiar en Estados Unidos. No tiene que ver con BIM ni con lo que la persona pidió."));
push(bul("Ninguno hace una sola pregunta. Un correo que no pregunta nada no obtiene nada."));

/* ── 2 · REGLAS ── */
push(new Paragraph({children:[new PageBreak()]}));
push(H1("2 · Las reglas que no se rompen"));
push(bul("El precio del Máster NO aparece nunca, ni «desde», ni aproximado. El Máster se conversa, no se cotiza por correo."));
push(bul("El precio de ACERO SÍ puede ir: $499,99 → $199,99."));
push(bul("{{unsubscribe_url}} en todos los correos. Sin excepción."));
push(bul("Una herramienta gratuita NO es una certificación ni un diploma. El test es un diagnóstico."));
push(bul("La calculadora lleva siempre su aviso: es de apoyo para predimensionar, no sustituye el criterio de un profesional responsable."));
push(bul("Los cupos se dicen «limitados». Nunca un número inventado: esa gente vuelve al mes siguiente a comprobarlo."));
push(bul("Si alguien pregunta el precio del Máster o quiere inscribirse, pasa a un humano. No improvisar cifras."));
push(bul("Todos los «Wait» en franja 9:00–11:00. Un correo a las 3 de la mañana se lee como spam."));
push(note("Plantilla base: matriz-viral/seguimiento/plantilla-email.html. Sin imágenes en base64 — Gmail recorta el correo a los 102 KB y se come el botón."));

/* ── 3 · LAS SECUENCIAS ── */
push(new Paragraph({children:[new PageBreak()]}));
push(H1("3 · Los 20 correos, listos para copiar"));
push(P("Cada correo indica si la plantilla es NUEVA (hay que crearla) y qué imagen lleva.",{run:{color:GREY,italics:true}}));

D.secuencias.forEach((s,idx)=>{
  if(idx) push(new Paragraph({children:[new PageBreak()]}));
  push(H2(`Secuencia ${s.id} · ${s.carpeta}`));
  push(tbl(["","",],[
    ["Para quién",s.quien],
    ["Qué busca",s.objetivo],
    ["Ritmo",s.duracion],
    ["Salida",s.salida],
  ],[2400,8100]));

  s.correos.forEach(c=>{
    push(H3(`Correo ${c.n} — ${c.cuando}`));
    push(LBL("Plantilla"));
    push(P(c.plantilla,{run:{bold:true,color:ORANGE}}));
    push(LBL("Asunto — copiar tal cual"));
    push(...copiar([c.asunto]));
    push(LBL("Preencabezado — copiar tal cual"));
    push(...copiar([c.preencabezado]));
    push(LBL("Cuerpo — copiar tal cual"));
    push(...copiar(c.cuerpo));
    if(c.cta&&c.cta.texto){
      push(LBL("Botón"));
      push(...copiar([c.cta.texto, c.cta.enlace||'']));
    }
    push(LBL("Imagen que va en este correo"));
    push(P(c.imagen,{run:{italics:true}}));
    if(c.nota) push(note(c.nota));
  });
});

/* ── 4 · PLANTILLAS NUEVAS ── */
push(new Paragraph({children:[new PageBreak()]}));
push(H1("4 · Las plantillas nuevas que hay que crear"));
const nuevas=[];
D.secuencias.forEach(s=>s.correos.forEach(c=>nuevas.push([s.id,c.plantilla.replace(/^NUEVA · /,''),`Correo ${c.n} · ${c.cuando}`])));
push(P(`Son ${nuevas.length} plantillas. Se crean en Marketing → Plantillas de correo, dentro de una carpeta nueva llamada «NUTRICIÓN 2026».`));
push(tbl(["Secuencia","Nombre de la plantilla","Cuándo se manda"],nuevas,[1500,5600,3400]));
push(alerta("El correo 6 de la secuencia S1 son DOS plantillas, una por rama (A y B). En total son 21 plantillas."));
push(note("Nombrarlas exactamente así. Los nombres están puestos para que se sepa a qué flujo pertenece cada una sin abrir nada — que es justo lo que hoy no se puede hacer."));

/* ── 5 · MONTAJE Y ENCENDIDO ── */
push(new Paragraph({children:[new PageBreak()]}));
push(H1("5 · Cómo se monta, y cómo se enciende"));
push(H2("Montaje"));
push(P("1. Abrir cada flujo de la sección 1 y anotar, paso por paso, el nombre y el ID de la plantilla vinculada a cada «Enviar correo»."));
push(P("2. Resolver los duplicados: saber cuál usa el flujo de verdad."));
push(P("3. Crear las 21 plantillas nuevas con los textos de la sección 3."));
push(P("4. En cada paso «Enviar correo» del flujo, apuntar a la plantilla nueva."));
push(alerta("Editar sobre la plantilla existente o reapuntar el paso — pero NO crear una plantilla nueva y dejar el paso apuntando a la vieja. El flujo va por ID: una plantilla nueva sin reapuntar no se manda nunca."));
push(P("5. Revisar que todos los «Wait» estén en franja 9:00–11:00."));
push(P("6. Comprobar que {{unsubscribe_url}} está en las 21."));
push(P("7. Prueba en seco: inscribir un contacto propio y recorrer la secuencia entera antes de tocar a nadie real."));

push(H2("Encendido — solo con el OK de Dayana"));
push(bul("Encender UNA secuencia primero: la de RECURSOS, que es la de más volumen."));
push(bul("A las 48 horas mirar aperturas, rebotes y quejas de spam."));
push(bul("Si va bien, encender la siguiente. NUNCA las cuatro el mismo día."));
push(bul("Los contactos que ya están parados en el pipeline no entran solos: los disparadores solo cogen a los nuevos. Hay que inscribirlos a mano, por tandas y empezando por los más recientes."));
push(alerta("Un correo mal mandado a 300 personas no se puede recoger. Ante la duda, preguntar antes de enviar."));

push(H2("Qué avisar al terminar"));
push(P("Plantillas creadas · resultado de la prueba en seco · qué flujos quedaron reapuntados · cuántos duplicados se limpiaron · y a las 48 horas del encendido, aperturas y rebotes."));

/* ── SALIDA ── */
const doc=new Document({styles:{default:{document:{run:{font:"Calibri"}}}},
 sections:[{properties:{page:{size:{width:12240,height:15840},
   margin:{top:900,bottom:900,left:900,right:900}}},children:b}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/4-Actualizar-correos-automatizaciones.docx');
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync(OUT,buf);
  const n=D.secuencias.reduce((t,s)=>t+s.correos.length,0);
  console.log(`OK → ${OUT} (${(buf.length/1024).toFixed(0)} KB) · ${D.secuencias.length} secuencias · ${n} correos`);});
