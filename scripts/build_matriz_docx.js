const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,ShadingType,PageBreak,
Table,TableRow,TableCell,WidthType,AlignmentType}=require('docx');
const fs=require('fs');
const NAVY="0E2438", ORANGE="C96A1C", GREY="5A6B7B", GREEN="1E7B4F", RED="A33B2A";

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:120},
  children:[new TextRun({text:t,color:NAVY,bold:true})]});
const H2=t=>new Paragraph({spacing:{before:240,after:90},
  children:[new TextRun({text:t,color:ORANGE,bold:true,size:24})]});
const H3=t=>new Paragraph({spacing:{before:180,after:70},
  children:[new TextRun({text:t,color:NAVY,bold:true,size:22})]});
const P=(t,o={})=>new Paragraph({spacing:{after:80},...o,
  children:[new TextRun({text:t,size:21,...(o.run||{})})]});
const note=t=>new Paragraph({spacing:{after:80},shading:{type:ShadingType.CLEAR,fill:"F4F7FA"},
  border:{left:{style:BorderStyle.SINGLE,size:18,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:20,italics:true,color:GREY})]});
const bul=t=>new Paragraph({bullet:{level:0},spacing:{after:40},
  children:[new TextRun({text:t,size:21})]});
const cap=lines=>lines.map((l,i)=>new Paragraph({
  shading:{type:ShadingType.CLEAR,fill:"F7F9FB"},spacing:{after:i===lines.length-1?140:0},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"B9C6D3",space:8}},
  children:[new TextRun({text:l||" ",size:19,font:"Consolas"})]}));
const W=[1300,2400,1500,4500];
const tbl=(head,rows,widths=W)=>new Table({columnWidths:widths,width:{size:widths.reduce((a,b)=>a+b),type:WidthType.DXA},
  rows:[new TableRow({children:head.map((h,i)=>new TableCell({width:{size:widths[i],type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR,fill:NAVY},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:"FFFFFF",size:18})]})]}))}),
    ...rows.map(r=>new TableRow({children:r.map((c,i)=>new TableCell({width:{size:widths[i],type:WidthType.DXA},
      children:[new Paragraph({children:[new TextRun({text:String(c),size:18})]})]}))}))]});

let b=[];
// PORTADA
b.push(new Paragraph({spacing:{after:40},children:[new TextRun({text:"DESIGN MODELING ACADEMY",color:ORANGE,bold:true,size:20})]}));
b.push(new Paragraph({heading:HeadingLevel.TITLE,spacing:{after:80},
  children:[new TextRun({text:"Matriz de Contenido — Agosto 2026",color:NAVY,bold:true})]}));
b.push(P("Incluye los reels pendientes de julio. Todo el contenido desglosado por formato y red, separando CONTENIDO DE VALOR (orgánico) de VENTA / PAUTA (ads).",{run:{color:GREY,italics:true}}));
b.push(P("Construido sobre la matriz viral: solo se repiten los patrones que YA demostraron funcionar con datos reales.",{run:{color:GREY,italics:true}}));

// 1. REGLAS
b.push(H1("1 · Las reglas (probadas con tus datos)"));
b.push(H2("Lo que SÍ funciona"));
b.push(bul("Ángulo ganador: «la IA te da velocidad, el CRITERIO es tuyo» — 8.5% de engagement en 2 piezas."));
b.push(bul("Herramientas gratuitas (lead magnets): el post de la calculadora fue el 70% del alcance del mes."));
b.push(bul("Cerrar SIEMPRE con pregunta directa + CTA de comentar. Sin pregunta = 0 comentarios (comprobado 3 veces)."));
b.push(bul("El humor va en REEL, nunca en post plano (meme estático: 1,321 views vs 4,700+ en video)."));
b.push(bul("Publicar también en FACEBOOK: 9,103 de 11,193 views del post ganador vinieron de ahí."));
b.push(H2("Lo que NO funciona"));
b.push(bul("Promo de curso pura sin gancho: «3 FAQ SAP2000» tuvo 5,195 views y CERO comentarios y guardados."));
b.push(bul("Hooks tipo trivia: «Los maestros del BIM» fue el peor del mes (538 views, 0 de todo)."));
b.push(bul("Contenido de obra/construcción: da millones de views pero atrae público que NO compra."));
b.push(note("Regla de oro del mes: ≥60% del contenido debe ser NÚCLEO (BIM · IA · modelado · acero), no obra."));

// 2. CTAs
b.push(H1("2 · Los CTA de este mes"));
b.push(P("Este mes todo apunta a dos productos. Cada pieza lleva el CTA que le corresponde:"));
b.push(tbl(["Producto","Palabra clave","Formato del CTA","Cuándo usarlo"],[
 ["Especialización en ACERO","ACERO","«Comenta ACERO y te mando la info»","Piezas de estructuras, acero, cálculo, conexiones"],
 ["Máster BIM + IA","BIM o IA","«Comenta BIM o IA y te cuento cómo»","Piezas de BIM, Revit, coordinación, IA aplicada"],
],[2100,1200,3000,3400]));
b.push(note("En LinkedIn NO se usa «comenta la palabra» — ahí va una pregunta abierta o «escríbeme por DM». En TikTok: «link en bio»."));

// 3. LO QUE DICEN LAS CAMPAÑAS
b.push(new Paragraph({children:[new PageBreak()]}));
b.push(H1("3 · Qué está trayendo clientes (campañas reales, últimos 30 días)"));
b.push(P("Datos de tu cuenta publicitaria: $1,474 invertidos · 1,873 leads · CPL promedio $0.79."));
b.push(tbl(["Leads","Campaña","CPL","Lectura"],[
 ["582","ESPE.1 ACERO – WhatsApp","$0.61","ACERO es tu mejor producto en volumen"],
 ["535","MÁSTER – Formulario V2","$0.71","El Máster convierte bien y sostenido"],
 ["486","ACERO geo-split – WSP+SMS","$0.45","EL MEJOR CPL de todos. Segmentar por zona funciona"],
 ["125","MÁSTER BIM+IA – WSP API","$0.51","CPL excelente. Escalable"],
 ["1","Curso SAP2000 – LANDING","$164.64","❌ Las landings NO funcionan para pauta"],
 ["0","Tráfico al perfil – IG","—","CTR 15% pero cero leads. No genera negocio"],
],[900,3200,1100,4500]));
b.push(H2("Las 3 conclusiones para la pauta"));
b.push(bul("WhatsApp gana siempre. Todos los ganadores van a WSP; las landings destruyen el CPL ($164 vs $0.45)."));
b.push(bul("ACERO es tu caballo de batalla: 1,068 leads combinados con el CPL más bajo. Merece más contenido orgánico que lo alimente."));
b.push(bul("Los anuncios ganadores son IMÁGENES simples (el top: «IMG2» con 558 leads y CPL $0.58), no producciones complejas."));
b.push(note("Acción: replicar el formato «IMG2» (imagen simple + copy directo + WhatsApp) para los nuevos anuncios de ACERO y Máster."));

// 4. JULIO PENDIENTE
b.push(new Paragraph({children:[new PageBreak()]}));
b.push(H1("4 · Pendientes de julio (3 piezas)"));
b.push(P("Estas ya tienen guion completo. Se publican primero, en formato estático (no requieren grabar video).",{run:{color:GREY}}));

b.push(H3("J1 · Mito render IA — CARRUSEL (7 slides) · 🎯 VALOR"));
b.push(P("Hook: «Esto parece un render de 4 horas. Lo hizo una IA en 10 segundos.»"));
b.push(bul("Slides: 1) hook · 2) el boceto a mano · 3) le describí el estilo · 4) el render en 10 seg · 5) sin modelar ni V-Ray · 6) la IA NO diseñó, el criterio es tuyo · 7) CTA"));
b.push(P("CTA: «¿Quieres dominar la IA aplicada a BIM? Comenta BIM o IA.»",{run:{bold:true}}));
b.push(P("Redes: Instagram + Facebook · LinkedIn (post de texto: «Renderizar me tomaba 4h; una IA lo hizo en 10 seg») · TikTok"));

b.push(H3("J2 · Diálogo Arqui vs Inge — REEL · 🎯 VALOR"));
b.push(P("Hook: «—La IA me va a quitar el trabajo. —A ti te reemplaza cualquier plantilla de Pinterest.»"));
b.push(P("Va en VIDEO (el meme estático ya se probó y rindió mal). Ritmo ping-pong, sin pausas, subtítulos quemados.",{run:{color:RED}}));
b.push(P("CTA: «¿De qué lado estás? Comenta BIM o IA.»",{run:{bold:true}}));
b.push(P("Redes: Instagram + TikTok (el humor es nativo ahí) · LinkedIn con tono reflexivo"));

b.push(H3("J3 · 3 cosas que tu Revit ya hace con IA — CARRUSEL (6 slides) · 🎯 VALOR"));
b.push(P("Hook: «Tu Revit ya tiene IA adentro. Y probablemente nunca la activaste.»"));
b.push(bul("01 Genera detalles constructivos · 02 Detecta y resuelve choques · 03 Propone distribución en planta · Cierre: te dan el borrador, tú pones el criterio"));
b.push(P("CTA: «¿Cuál no conocías? Comenta BIM o IA y te mando cómo activarlas.»",{run:{bold:true}}));
b.push(P("Redes: Instagram + Facebook · LinkedIn (carrusel PDF) · YouTube (video largo: «Cómo activar la IA de Revit paso a paso»)"));

module.exports={b,H1,H2,H3,P,note,bul,cap,tbl,new_page:()=>new Paragraph({children:[new PageBreak()]}),
  Document,Packer,Paragraph,TextRun,HeadingLevel,NAVY,ORANGE,GREY,GREEN,RED,fs};

// ============ AGOSTO ============
b.push(new Paragraph({children:[new PageBreak()]}));
b.push(H1("5 · AGOSTO — Contenido de VALOR (orgánico)"));
b.push(P("Estas piezas NO venden directo: generan conversación, guardados y autoridad. El CTA abre el DM; la venta se cierra después.",{run:{color:GREY}}));

const valor=[
 ["S1 · Lun 4","CARRUSEL · IG+FB","🎯 BIM+IA",
  "Tu Revit ya tiene IA adentro: 3 funciones que no activaste",
  "«¿Cuál no conocías? Comenta BIM o IA»","LinkedIn: carrusel PDF · YouTube: video largo paso a paso"],
 ["S1 · Mié 6","CARRUSEL · IG+FB","🎯 BIM+IA",
  "5 errores al usar IA en tus proyectos BIM (el #3 te cuesta el proyecto)",
  "«¿Cuál has cometido? Comenta BIM o IA»","LinkedIn: documento PDF, CTA pregunta abierta"],
 ["S1 · Sáb 9","REEL · IG+TikTok","🎯 Humor BIM+IA",
  "Diálogo Arqui vs Inge sobre la IA",
  "«¿De qué lado estás? Comenta BIM o IA»","TikTok con audio en tendencia"],
 ["S2 · Lun 11","REEL · IG+TikTok+FB","🎯 BIM+IA",
  "Le pedí a la IA que coordinara un modelo BIM. Mira dónde falló",
  "«Comenta BIM o IA y te cuento mi flujo»","YouTube Short · LinkedIn post de texto"],
 ["S2 · Sáb 16","CARRUSEL · IG+FB","🎯 BIM+IA",
  "Esto parece un render de 4h. Lo hizo una IA en 10 segundos",
  "«¿Lo usarías en tus entregas? Comenta BIM o IA»","TikTok · LinkedIn"],
 ["S3 · Lun 18","CARRUSEL · IG+FB","🎯 Criterio",
  "¿Qué hace un BIM Manager que la IA nunca podrá? (prioriza · negocia · responde)",
  "«¿De acuerdo? Comenta BIM o IA»","LinkedIn: el mejor formato para este tema"],
 ["S3 · Mié 20","POST · IG+FB","🎯 ACERO",
  "El error #1 al diseñar conexiones en acero (y cómo evitarlo)",
  "«Comenta ACERO y te mando la guía»","TikTok: versión rápida"],
 ["S4 · Lun 25","REEL · IG+TikTok","🎯 Humor BIM",
  "Coordinador BIM vs. el que sigue modelando a mano",
  "«¿Team a mano o team BIM+IA? Comenta BIM o IA»","TikTok nativo"],
 ["S4 · Mié 27","CARRUSEL · IG+FB","🎯 ACERO",
  "3 señales de que tu estructura de acero está sobredimensionada",
  "«¿Cuántas te pasan? Comenta ACERO»","LinkedIn: documento"],
];
b.push(tbl(["Fecha","Formato","Eje","Tema / Hook","CTA","Otras redes"],
  valor.map(v=>[v[0],v[1],v[2],v[3],v[4],v[5]]),[1100,1500,1200,3400,2100,2400]));

b.push(H2("Detalle de los hooks (para producción)"));
b.push(H3("Lun 4 — Tu Revit ya tiene IA (carrusel 6 slides)"));
b.push(bul("1) «Tu Revit ya tiene IA adentro. Y probablemente nunca la activaste. 3 funciones →»"));
b.push(bul("2) 01 · Genera detalles constructivos con Autodesk AI Assist"));
b.push(bul("3) 02 · Detecta y RESUELVE choques (te sugiere la solución)"));
b.push(bul("4) 03 · Propone distribución en planta: le das los m² y da 3 layouts"));
b.push(bul("5) «Ninguna te da el proyecto terminado. Te dan el primer borrador. Tú pones el criterio.»"));
b.push(bul("6) CTA: «¿Cuál no conocías? Comenta BIM o IA y te mando cómo activarlas.»"));

b.push(H3("Mié 6 — 5 errores al usar IA en BIM (carrusel 7 slides)"));
b.push(bul("01 Confiar en la primera respuesta · 02 Pedirle criterio en vez de velocidad · 03 No revisar contra la norma · 04 Meter datos sin contexto · 05 No documentar lo que la IA hizo"));

b.push(H3("Mié 20 — Conexiones en acero (post plano) · NUEVO"));
b.push(P("Imagen: detalle de conexión con ✅/❌. Texto grande: «El error #1 al diseñar conexiones en acero.»"));
b.push(P("Cuerpo del caption: el error típico (asumir empotramiento perfecto cuando la conexión es semi-rígida), qué provoca, y cómo verificarlo. Cierra con la pregunta y «Comenta ACERO»."));

b.push(H3("Mié 27 — Acero sobredimensionado (carrusel 6 slides) · NUEVO"));
b.push(bul("01 Usas el mismo perfil en toda la estructura · 02 No revisaste las derivas, solo la resistencia · 03 El costo de acero se te disparó sin razón técnica · Cierre: «no es más acero, es mejor criterio»"));

// BLOG
b.push(new Paragraph({children:[new PageBreak()]}));
b.push(H1("6 · AGOSTO — Blog y LinkedIn"));
b.push(P("El blog trae tráfico por búsqueda (SEO) y alimenta LinkedIn, que es donde está el comprador del Máster.",{run:{color:GREY}}));
b.push(tbl(["Fecha","Pieza","Dónde","CTA"],[
 ["Vie 15","Blog: «IA en BIM: qué automatizar y qué NUNCA delegar (guía 2026)»","Blog + LinkedIn post largo + post IG que lleva al blog","LinkedIn: «¿Dónde ponen ustedes esa línea?» · IG: «Comenta BIM o IA»"],
 ["Vie 22","Blog: «Acero: 5 verificaciones que no puedes saltarte»","Blog + LinkedIn + post IG","LinkedIn: «¿Cuál revisan primero?» · IG: «Comenta ACERO»"],
],[1100,3600,2900,3100]));
b.push(H2("Estructura del blog de IA (Vie 15)"));
b.push(bul("Intro: la IA no reemplaza al profesional BIM; le quita lo repetitivo. La clave es saber la línea."));
b.push(bul("Qué SÍ automatizar: cantidades · documentación · detección de choques · primeras versiones de detalles · renders."));
b.push(bul("Qué NO delegar: decisiones normativas · priorización · negociación entre disciplinas · la firma y la responsabilidad."));
b.push(bul("Regla de oro: la IA da el borrador; el criterio profesional lo pones tú. → CTA al Máster."));
b.push(H2("Post de LinkedIn (Vie 15) — texto listo"));
cap(["Llevo semanas dejando que la IA haga parte de mi trabajo BIM. Esto aprendí sobre qué",
"automatizar… y qué NO delegar jamás.","",
"Automatiza sin miedo: cantidades, documentación, detección de choques, primeras versiones",
"de detalles. Te devuelve horas cada semana.","",
"Pero NO delegues el criterio: decisiones normativas, priorización, negociación, y sobre",
"todo la responsabilidad — eso lo firmas tú, no una IA.","",
"La regla: la IA te da el borrador; el criterio profesional lo pones tú.","",
"¿Dónde ponen ustedes esa línea en sus proyectos?"]).forEach(p=>b.push(p));

// COMUNIDAD Y EMPRESA
b.push(H1("7 · AGOSTO — Comunidad y novedades"));
b.push(tbl(["Fecha","Pieza","Formato","Qué incluir"],[
 ["Vie 29","Comunidad: recap del mes","Post/reel IG+FB","Qué se resolvió, qué recurso se compartió, logro de un miembro + invitación"],
 ["Sáb 30","Conferencia / convención","Carrusel + reel","⚠️ Pendiente: me pasas los datos del evento"],
 ["Lun 31","«Lo que hicimos en agosto en Design Modeling»","Carrusel + LinkedIn","Resumen del mes: proyectos, novedades, logros"],
],[1100,3200,1800,4600]));
b.push(note("Vie 22 también estaba reservado para «proyecto / caso de alumno» — pendiente de que me pases el caso."));

// VENTA / ADS
b.push(new Paragraph({children:[new PageBreak()]}));
b.push(H1("8 · AGOSTO — VENTA y PAUTA (ads directas)"));
b.push(P("Estas piezas SÍ venden. Van a pauta y llevan a WhatsApp (nunca a landing — el dato: landing = CPL $164 vs WhatsApp = CPL $0.45).",{run:{color:RED,bold:true}}));

b.push(H2("A · Anuncios a replicar (los que ya funcionan)"));
b.push(tbl(["Anuncio base","Producto","Fórmula a replicar","Presupuesto sugerido"],[
 ["IMG2 (558 leads · CPL $0.58)","ACERO","Imagen simple + copy directo al dolor + botón a WhatsApp","El grueso de la inversión"],
 ["IG 28/05 (222 leads · CPL $0.43)","ACERO/Máster","Creativo de feed reutilizado como ad","Escalar"],
 ["ACERO geo-split (CPL $0.45)","ACERO","Segmentar por ciudad/país + WSP y SMS","Mantener y ampliar zonas"],
 ["MÁSTER WSP API (CPL $0.51)","Máster BIM+IA","Conversación directa a WhatsApp","Escalar — es el mejor del Máster"],
],[2600,1600,3800,2700]));

b.push(H2("B · Piezas de venta orgánica del mes (con gancho, no promo pura)"));
b.push(tbl(["Fecha","Pieza","Producto","Hook de valor primero"],[
 ["S1 · Vie 8","Lead magnet / herramienta gratuita","Máster BIM+IA","Regalo útil → «comenta la palabra». El formato #1 del mes pasado"],
 ["S2 · Mié 13","«De modelador a BIM Manager: las 3 habilidades que te faltan»","Máster BIM+IA","Valor primero; el Máster se menciona al final"],
 ["S3 · Sáb 23","«¿Por dónde empezar con acero según tu perfil?»","Espec. ACERO","Ruta útil → «Comenta ACERO y armamos la tuya»"],
 ["S4 · Vie 29","«3 tareas de BIM que la IA ya hace por ti»","Máster BIM+IA","Demo concreta; cierra con la especialización"],
],[1100,3800,1700,4100]));
b.push(note("Regla para venta: NUNCA abrir con «inscríbete» ni con el precio. Se abre con valor o con un dolor real, y el CTA solo invita a conversar. La promo pura fue el peor post del mes (0 comentarios)."));

b.push(H2("C · Cómo separar valor y venta"));
b.push(tbl(["","CONTENIDO DE VALOR","VENTA / PAUTA"],[
 ["Objetivo","Conversación, guardados, autoridad","Leads a WhatsApp"],
 ["Proporción del mes","~70%","~30%"],
 ["CTA","«Comenta BIM/IA/ACERO»","Botón directo a WhatsApp"],
 ["Dónde vive","Orgánico (IG, FB, LinkedIn, TikTok)","Pauta (Meta Ads)"],
 ["Nunca","Vender directo ni poner precio","Mandar a una landing"],
],[1800,4200,4200]));

// CIERRE
b.push(H1("9 · Resumen operativo del mes"));
b.push(tbl(["Formato","Cantidad","Notas"],[
 ["Carruseles","6","El formato de mejor engagement (8.5%)"],
 ["Reels","3","Humor y demos. Van también a TikTok"],
 ["Posts planos","2","Uno de ellos es el lead magnet"],
 ["Blogs","2","+ su versión de LinkedIn"],
 ["Comunidad / novedades","3","Recap, evento y cierre de mes"],
 ["Piezas de venta","4","Con gancho de valor, no promo pura"],
],[2600,1400,6200]));
b.push(H2("Checklist antes de publicar cada pieza"));
b.push(bul("¿Es NÚCLEO (BIM · IA · acero) y no obra genérica?"));
b.push(bul("¿Tiene una demo o algo concreto en pantalla (no solo hablar)?"));
b.push(bul("¿Cierra con una PREGUNTA directa sobre una duda real?"));
b.push(bul("¿El CTA es el correcto: ACERO o BIM/IA? ¿Adaptado si va a LinkedIn?"));
b.push(bul("¿Se publicó también en Facebook?"));
b.push(new Paragraph({spacing:{before:300},border:{top:{style:BorderStyle.SINGLE,size:8,color:"D9E0E7",space:8}},
  children:[new TextRun({text:"Design Modeling Academy · Matriz de contenido agosto 2026 · Construida sobre datos reales de la matriz viral y de las campañas activas",size:17,color:GREY})]}));

const doc=new Document({styles:{default:{document:{run:{font:"Calibri"}}}},
 sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:900,bottom:900,left:900,right:900}}},children:b}]});
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync("Matriz-Contenido-Agosto-2026-DMA.docx",buf);console.log("OK");});
