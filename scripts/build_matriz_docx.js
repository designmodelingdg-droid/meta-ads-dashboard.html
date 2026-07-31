/**
 * Genera matriz-viral/entregables/Matriz-Contenido-Agosto-2026-DMA.docx
 *
 * Fuentes (no se escribe nada a mano aquí):
 *   matriz-viral/matriz/calendario-agosto.json    → orden de publicación del mes
 *   matriz-viral/matriz/guiones-completos.json    → contenido completo de cada pieza
 *   matriz-viral/matriz/analisis-campanas.md      → datos de pauta (resumidos abajo)
 *
 * Uso:  node scripts/build_matriz_docx.js
 * Requiere: npm i docx
 */
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,ShadingType,PageBreak,
Table,TableRow,TableCell,WidthType}=require('docx');
const fs=require('fs'), path=require('path');

const ROOT=path.resolve(__dirname,'..');
const CAL=JSON.parse(fs.readFileSync(path.join(ROOT,'matriz-viral/matriz/calendario-agosto.json'),'utf8'));
const GUI=JSON.parse(fs.readFileSync(path.join(ROOT,'matriz-viral/matriz/guiones-completos.json'),'utf8'));
const BY={}; GUI.piezas.forEach(p=>BY[p.id]=p);

const NAVY="0E2438", ORANGE="C96A1C", GREY="5A6B7B", RED="A33B2A", LIGHT="F4F7FA", BOX="F7F9FB";

/* ───────────────────────────── helpers de formato ───────────────────────────── */
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:140},
  children:[new TextRun({text:t,color:NAVY,bold:true})]});
const H2=t=>new Paragraph({spacing:{before:280,after:100},
  children:[new TextRun({text:t,color:ORANGE,bold:true,size:26})]});
const H3=t=>new Paragraph({spacing:{before:200,after:80},
  children:[new TextRun({text:t,color:NAVY,bold:true,size:22})]});
const LBL=t=>new Paragraph({spacing:{before:150,after:50},
  children:[new TextRun({text:t,color:GREY,bold:true,size:18,allCaps:true})]});
const P=(t,o={})=>new Paragraph({spacing:{after:80},...o,
  children:[new TextRun({text:t,size:21,...(o.run||{})})]});
const note=t=>new Paragraph({spacing:{after:100},shading:{type:ShadingType.CLEAR,fill:LIGHT},
  border:{left:{style:BorderStyle.SINGLE,size:18,color:ORANGE,space:8}},
  children:[new TextRun({text:t,size:20,italics:true,color:GREY})]});
const bul=t=>new Paragraph({bullet:{level:0},spacing:{after:50},
  children:[new TextRun({text:t,size:21})]});
const pageBreak=()=>new Paragraph({children:[new PageBreak()]});

// bloque monoespaciado (captions, copys) — se parte en líneas de ~95 caracteres
const wrap=(s,w=95)=>String(s).split('\n').flatMap(line=>{
  if(line.length<=w) return [line];
  const out=[]; let cur='';
  line.split(' ').forEach(word=>{
    if((cur+' '+word).trim().length>w){out.push(cur.trim());cur=word;} else cur+=' '+word;});
  if(cur.trim())out.push(cur.trim());
  return out;});
const block=(text,fill=BOX)=>wrap(text).map((l,i,a)=>new Paragraph({
  shading:{type:ShadingType.CLEAR,fill},spacing:{after:i===a.length-1?140:0},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"B9C6D3",space:8}},
  children:[new TextRun({text:l||" ",size:18,font:"Consolas"})]}));
// bloque destacado para el hook
const hookBlock=text=>wrap(text,90).map((l,i,a)=>new Paragraph({
  shading:{type:ShadingType.CLEAR,fill:"FDF1E4"},spacing:{after:i===a.length-1?140:0},
  border:{left:{style:BorderStyle.SINGLE,size:20,color:ORANGE,space:8}},
  children:[new TextRun({text:l||" ",size:21,bold:true,color:NAVY})]}));

const tbl=(head,rows,widths)=>new Table({columnWidths:widths,
  width:{size:widths.reduce((a,b)=>a+b),type:WidthType.DXA},
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:NAVY},
      children:[new Paragraph({children:[new TextRun({text:h,bold:true,color:"FFFFFF",size:18})]})]}))}),
    ...rows.map(r=>new TableRow({children:r.map((c,i)=>new TableCell({
      width:{size:widths[i],type:WidthType.DXA},
      children:String(c).split('\n').map(line=>new Paragraph({
        children:[new TextRun({text:line,size:18})]}))}))}))]});

const b=[];
const push=(...x)=>x.flat().forEach(p=>b.push(p));

/* ───────────────────────────── datos de apoyo ───────────────────────────── */
const CTA_DE=eje=>eje&&eje.includes('ACERO')
  ? {prod:'Especialización en ACERO',pal:'ACERO'}
  : {prod:'Máster BIM + IA',pal:'BIM / IA'};
const REDES=['instagram','facebook','linkedin','tiktok','youtube','blog','meta-ads'];
const NOMBRE_RED={instagram:'Instagram',facebook:'Facebook',linkedin:'LinkedIn',
  tiktok:'TikTok',youtube:'YouTube',blog:'Blog',"meta-ads":'Meta Ads'};

/* ───────────────────────────── renderizador de pieza ───────────────────────────── */
function renderPieza(entry,idx){
  const p=BY[entry.id];
  const out=[];
  const titulo=p?p.titulo:'(pendiente de definir)';
  out.push(new Paragraph({spacing:{before:340,after:60},
    border:{bottom:{style:BorderStyle.SINGLE,size:12,color:ORANGE,space:6}},
    children:[
      new TextRun({text:`${entry.fecha}  ·  `,color:ORANGE,bold:true,size:24}),
      new TextRun({text:titulo,color:NAVY,bold:true,size:24})]}));

  if(!p){
    out.push(note(entry.nota));
    out.push(P('Formato previsto: '+entry.formato_publicacion+' · Redes: '+entry.redes));
    return out;
  }

  const cta=CTA_DE(p.eje);
  out.push(tbl(['Formato','Redes','Eje','Producto / palabra clave'],
    [[entry.formato_publicacion,entry.redes,p.eje.replace('NUCLEO-','')+' · '+p.pilar,
      cta.prod+'\n→ «'+cta.pal+'»']],[1900,3400,1700,3200]));
  if(entry.nota) out.push(note(entry.nota));

  out.push(LBL('Hook (los primeros 3 segundos / el primer slide)'));
  out.push(...hookBlock(p.hook));

  /* ── YOUTUBE: ficha del video ── */
  if(p.youtube){
    out.push(LBL('YouTube — título optimizado para búsqueda'));
    out.push(P(p.youtube.titulo_seo,{run:{bold:true,size:22,color:NAVY}}));
    out.push(LBL('Descripción del video (con capítulos) — lista para copiar'));
    out.push(...block(p.youtube.descripcion));
    out.push(LBL('Etiquetas'));
    out.push(P(p.youtube.tags,{run:{size:19,color:GREY}}));
    out.push(new Paragraph({spacing:{after:80},
      children:[new TextRun({text:'🖼  Miniatura: ',bold:true,size:19,color:NAVY}),
                new TextRun({text:p.youtube.miniatura,size:19,italics:true,color:GREY})]}));
  }

  /* ── REEL / VIDEO: guion segundo a segundo ── */
  if(p.guion_reel){
    out.push(LBL(p.formato==='youtube'
      ? 'Guion del video — capítulo por capítulo'
      : 'Guion del reel — segundo a segundo'));
    out.push(tbl([p.formato==='youtube'?'Minuto':'Tiempo','Qué se ve en pantalla','Qué se dice (voz / texto)'],
      p.guion_reel.map(g=>[g.tiempo,g.accion,g.voz]),[1300,3100,5800]));
    if(p.notas_produccion){
      out.push(LBL('Notas de producción'));
      out.push(P(p.notas_produccion,{run:{color:RED}}));
    }
    if(p.meme_alt){
      out.push(LBL('Versión alterna en imagen (solo para Facebook)'));
      out.push(P('Texto en la imagen: '+p.meme_alt.texto_en_imagen));
      out.push(P('Concepto: '+p.meme_alt.concepto,{run:{italics:true,color:GREY}}));
    }
  }

  /* ── CARRUSEL: slide por slide ── */
  if(p.slides){
    out.push(LBL(`Carrusel — qué va en cada diapositiva (${p.slides.length} slides)`));
    p.slides.forEach(s=>{
      out.push(new Paragraph({spacing:{before:130,after:40},
        children:[new TextRun({text:`SLIDE ${s.n} de ${p.slides.length}`,bold:true,size:19,color:ORANGE})]}));
      out.push(...block(s.texto));
      if(s.visual) out.push(new Paragraph({spacing:{after:60},indent:{left:180},
        children:[new TextRun({text:'🖼  Imagen: ',bold:true,size:19,color:NAVY}),
                  new TextRun({text:s.visual,size:19,italics:true,color:GREY})]}));
    });
  }

  /* ── POST PLANO: imagen + desarrollo ── */
  if(p.imagen){
    out.push(LBL('Post plano — qué va en la imagen'));
    out.push(...block(p.imagen.texto_en_imagen));
    out.push(new Paragraph({spacing:{after:80},
      children:[new TextRun({text:'🖼  Concepto visual: ',bold:true,size:19,color:NAVY}),
                new TextRun({text:p.imagen.concepto,size:19,italics:true,color:GREY})]}));
  }
  if(p.cuerpo_desarrollado){
    out.push(LBL('Desarrollo del contenido (lo que se explica)'));
    p.cuerpo_desarrollado.forEach(t=>out.push(bul(t)));
  }

  /* ── BLOG ── */
  if(p.blog){
    out.push(LBL('Blog — título SEO'));
    out.push(P(p.blog.titulo_seo,{run:{bold:true,size:22,color:NAVY}}));
    out.push(LBL('Estructura del artículo (un bloque por punto)'));
    (p.blog.estructura||p.blog.secciones||[]).forEach(t=>out.push(bul(t)));
  }
  if(p.post_linkedin){
    out.push(LBL('Post de LinkedIn — texto listo para copiar'));
    out.push(...block(p.post_linkedin));
  }

  /* ── ANUNCIO DE PAUTA ── */
  if(p.anuncio){
    const a=p.anuncio;
    out.push(LBL('Ficha del anuncio'));
    out.push(tbl(['Campo','Contenido'],[
      ['Anuncio base (lo que ya funciona)',a.base],
      ['Producto',a.producto],
      ['Objetivo de campaña',a.objetivo],
      ['Destino',a.destino],
      ['Público',a.publico],
      ['Botón',a.boton],
      ['Mensaje precargado',a.mensaje_precargado],
      ['Presupuesto',a.presupuesto_sugerido],
      ['Qué medir',a.que_medir],
    ],[2800,7400]));
    out.push(LBL('Creativo'));
    out.push(P(a.creativo));
    out.push(LBL('Texto que va DENTRO de la imagen'));
    out.push(...block(a.texto_en_imagen));
    out.push(LBL('Texto principal del anuncio (copy) — listo para pegar'));
    out.push(...block(a.texto_principal));
    out.push(LBL('Titular y descripción'));
    out.push(P('Titular: '+a.titular,{run:{bold:true}}));
    out.push(P('Descripción: '+a.descripcion));
    if(a.prohibido) out.push(note('⛔ '+a.prohibido));
  }

  /* ── HISTORIAS ── */
  if(p.historias){
    out.push(LBL(`Historias — secuencia de ${p.historias.length} frames`));
    out.push(P('La historia no repite el post: le abre la puerta. El sticker es el CTA, y quien responde recibe DM.',{run:{color:GREY,italics:true,size:19}}));
    out.push(tbl(['#','Qué se ve','Texto en pantalla','Sticker','Qué hacer con quien responde'],
      p.historias.map(h=>[String(h.n),h.visual,h.texto,h.sticker,h.seguimiento]),
      [500,2500,2400,2300,2500]));
  }

  /* ── CAPTION ── */
  if(p.caption){
    out.push(LBL('Descripción / caption completo — listo para copiar'));
    out.push(...block(p.caption));
  }

  /* ── CTA POR RED ── */
  if(p.cta_por_red){
    const rows=REDES.filter(r=>p.cta_por_red[r]).map(r=>[NOMBRE_RED[r],p.cta_por_red[r]]);
    if(rows.length){
      out.push(LBL('CTA por red'));
      out.push(tbl(['Red','Cómo se cierra ahí'],rows,[1800,8400]));
    }
  }

  /* ── ADAPTACIÓN A OTRAS REDES ── */
  if(p.adaptacion_redes){
    out.push(LBL('Cómo se adapta a las otras redes'));
    out.push(tbl(['Red','Qué cambia'],
      Object.entries(p.adaptacion_redes).map(([k,v])=>[NOMBRE_RED[k]||k,v]),[1800,8400]));
  }

  /* ── PROMPT DE IMÁGENES ── */
  if(p.prompt_imagenes){
    out.push(LBL('Prompt para generar las imágenes (ChatGPT / IA de imagen)'));
    out.push(...block(p.prompt_imagenes,"EEF3F8"));
  }

  /* ── COMUNIDAD ── */
  if(p.comunidad_contenido){
    out.push(LBL('Contenido para la comunidad'));
    out.push(tbl(['Qué','Texto'],
      Object.entries(p.comunidad_contenido).map(([k,v])=>[k.replace(/_/g,' '),v]),[2400,7800]));
  }

  return out;
}

/* ═══════════════════════════════ PORTADA ═══════════════════════════════ */
push(new Paragraph({spacing:{after:40},
  children:[new TextRun({text:"DESIGN MODELING ACADEMY",color:ORANGE,bold:true,size:20})]}));
push(new Paragraph({heading:HeadingLevel.TITLE,spacing:{after:80},
  children:[new TextRun({text:"Matriz de Contenido — Agosto 2026",color:NAVY,bold:true})]}));
push(new Paragraph({spacing:{after:200},
  children:[new TextRun({text:"Desarrollo completo de cada pieza · incluye los pendientes de julio",
    color:GREY,italics:true,size:22})]}));
push(P("Cada pieza viene desarrollada de principio a fin: el hook, el guion segundo a segundo de los reels, el texto de cada diapositiva de los carruseles con su dirección de imagen, la descripción completa de los posts planos, el copy de los anuncios de pauta y la adaptación a cada red."));
push(P("Todo está construido sobre datos reales: la matriz viral de la cuenta (124 reels analizados) y el rendimiento de las campañas activas de los últimos 30 días."));
push(note("Cómo usar este documento: busca la fecha, copia el texto tal cual está en los bloques grises (están listos para pegar) y pásale a diseño el bloque «Imagen» de cada slide. El prompt de imágenes se pega directo en ChatGPT."));

/* ═══════════════════════════════ 1 · REGLAS ═══════════════════════════════ */
push(H1("1 · Las reglas del mes (probadas con tus datos)"));
push(H2("Lo que SÍ funciona"));
push(bul("Ángulo ganador: «la IA te da velocidad, el CRITERIO es tuyo» — 8.5% de engagement en 2 piezas."));
push(bul("Herramientas gratuitas (lead magnets): el post de la calculadora se llevó el 70% del alcance del mes."));
push(bul("Cerrar SIEMPRE con pregunta directa + CTA de comentar. Sin pregunta = 0 comentarios (comprobado 3 veces)."));
push(bul("El humor va en REEL, nunca en post plano (meme estático: 1,321 views vs 4,700+ en video)."));
push(bul("Publicar también en FACEBOOK, cuidado y no como auto-repost: 9,103 de las 11,193 views del post ganador vinieron de ahí."));
push(H2("Lo que NO funciona"));
push(bul("Promo de curso pura sin gancho: «3 FAQ SAP2000» tuvo 5,195 views y CERO comentarios y guardados."));
push(bul("Hooks tipo trivia: «Los maestros del BIM» fue el peor del mes (538 views, 0 de todo)."));
push(bul("Contenido de obra/construcción: da millones de views pero atrae público que NO compra."));
push(note("Regla de oro del mes: ≥60% del contenido debe ser NÚCLEO (BIM · IA · modelado · acero), no obra."));

/* ═══════════════════════════════ 2 · CTAs ═══════════════════════════════ */
push(H1("2 · Los CTA de este mes"));
push(P("Todo apunta a dos productos. Cada pieza lleva el CTA que le corresponde:"));
push(tbl(["Producto","Palabra","Formato del CTA","Cuándo usarlo"],[
 ["Especialización en ACERO","ACERO","«Comenta ACERO y te mando la info»","Piezas de estructuras, acero, conexiones, verificaciones, cálculo"],
 ["Máster BIM + IA","BIM o IA","«Comenta BIM o IA y te cuento cómo»","Piezas de BIM, Revit, coordinación, IA aplicada"],
 ["Lead magnet (calculadora)","ZAPATA","«Comenta ZAPATA y te la mando»","Solo la pieza de la herramienta gratuita"],
],[2300,1200,3000,3700]));
push(note("En LinkedIn NUNCA se usa «comenta la palabra» — ahí va una pregunta abierta o «escríbeme por DM». En TikTok: «link en bio»."));

/* ═══════════════════════════════ 3 · CAMPAÑAS ═══════════════════════════════ */
push(pageBreak());
push(H1("3 · Qué está trayendo clientes (campañas reales, últimos 30 días)"));
push(P("Datos de tu cuenta publicitaria: $1,474 invertidos · 1,873 leads · CPL promedio $0.79."));
push(tbl(["Leads","Campaña","CPL","Lectura"],[
 ["582","ESPE.1 ACERO – WhatsApp","$0.61","ACERO manda en volumen"],
 ["535","MÁSTER – Formulario V2","$0.71","El Máster convierte bien y sostenido"],
 ["486","ACERO geo-split – WSP + SMS","$0.45","EL MEJOR CPL. Segmentar por zona funciona"],
 ["125","MÁSTER BIM+IA – WSP API","$0.51","CPL excelente con $64. Hay que escalarla"],
 ["1","Curso SAP2000 – LANDING","$164.64","❌ La landing destruye el CPL"],
 ["0","Tráfico al perfil – IG","—","CTR 15% y cero leads. No genera negocio"],
],[900,3300,1200,4800]));
push(H2("Las 3 conclusiones para la pauta"));
push(bul("WhatsApp gana siempre. Todos los ganadores van a WSP; la única landing hizo CPL $164 contra $0.45 del mejor."));
push(bul("ACERO es el caballo de batalla: 1,086 leads combinados con el CPL más bajo. Por eso este mes suma 3 piezas orgánicas de acero."));
push(bul("Los anuncios ganadores son IMÁGENES simples (el top, «IMG2»: 558 leads, CPL $0.58), no producciones caras."));
push(note("Ojo con la métrica bonita: «Tráfico al perfil» tuvo el CTR más alto de la cuenta (15%) y cero negocio. El CTR sin conversión no es una buena campaña."));

/* ═══════════════════════════════ 4 · CALENDARIO ═══════════════════════════════ */
push(pageBreak());
push(H1("4 · Calendario del mes de un vistazo"));
push(P("El desarrollo completo de cada una está en la sección 5, en este mismo orden.",{run:{color:GREY,italics:true}}));
const ICON={valor:'🎯 valor','venta-blanda':'💰 venta',blog:'📝 blog',comunidad:'👥 comunidad',
  empresa:'🏛️ empresa',youtube:'▶️ YouTube'};
push(tbl(["Fecha","Formato","Tipo","Pieza","Redes"],
  CAL.piezas.map(e=>[e.fecha,e.formato_publicacion,ICON[e.tipo]||e.tipo,
    (BY[e.id]?BY[e.id].titulo:'⚠️ PENDIENTE — faltan tus datos'),e.redes]),
  [1500,1900,1300,3400,3300]));
push(note("Semana 1 arranca con dos carruseles porque es el formato de mejor engagement de la cuenta (8.5%). Los reels se concentran en semanas 2 y 4 para no cargar la grabación."));

/* ═══════════════════════════════ 5 · DESARROLLO ═══════════════════════════════ */
push(pageBreak());
push(H1("5 · Desarrollo completo, pieza por pieza"));
push(P("Todo lo que está en bloque gris se copia y se pega tal cual. Lo que está en cursiva junto al ícono 🖼 es la indicación para diseño.",{run:{color:GREY,italics:true}}));
let semanaActual=null;
CAL.piezas.forEach((e,i)=>{
  if(e.semana!==semanaActual){semanaActual=e.semana;push(H2('▸ '+semanaActual));}
  push(renderPieza(e,i));
});

/* ═══════════════════════════════ 6 · HISTORIAS ═══════════════════════════════ */
push(pageBreak());
push(H1("6 · HISTORIAS — cómo se convierte con stories"));
const HR=GUI.historias_rutina;
push(P(HR.nota,{run:{color:GREY,italics:true}}));
push(H2("Las 8 reglas"));
HR.reglas.forEach(r=>push(bul(r)));
push(note("Traducción a tu embudo: en el feed el CTA es «comenta ACERO / BIM / IA» y lo recoge el bot. En historias el CTA es el STICKER, y lo recoges tú por DM. Es el mismo camino — comentario o sticker → DM → conversación → venta."));

push(H2("Qué sticker usar según lo que buscas"));
push(tbl(["Sticker","Qué te da","Cuándo usarlo","Cómo se cobra"],[
 ["Encuesta (2 opciones)","Volumen de respuestas","Cuando quieres saber en qué bando está tu gente","DM a los que votan la opción «equivocada» — son los que necesitan lo que vendes"],
 ["Quiz (con respuesta correcta)","Los que fallan","Cuando hay un dato técnico que sorprende","DM con la explicación a cada uno que falló. Es el lead más calificado"],
 ["Caja de preguntas","Conversación real","Cuando quieres material y confianza","Contestar UNA POR UNA por DM. Republicar las mejores al día siguiente"],
 ["Deslizador (0-100%)","Participación fácil","Cuando quieres números, no charla","Poco valor de conversión: úsalo para calentar la cuenta"],
 ["Cuenta regresiva","Recordatorio automático","Antes de un video, un evento o un lanzamiento","Los que la activan reciben aviso solos. Cero trabajo"],
 ["Enlace","Tráfico directo","Al blog, al post o al video","En historias el enlace SÍ va directo (la regla de «nunca a landing» es solo para la pauta)"],
],[1900,1900,2900,3500]));

push(H2("La semana tipo de historias"));
push(tbl(["Día","Qué se publica","Sticker"],
  HR.semana_tipo.map(s=>[s.dia,s.historia,s.sticker]),[1400,4900,3900]));

push(H2("Destacadas del perfil"));
push(P("Las buenas secuencias no se pierden a las 24 horas: se guardan en destacadas. Son la portada del perfil para quien te descubre.",{run:{color:GREY}}));
HR.destacadas.forEach(x=>push(bul(x)));
push(note("Cada pieza del mes tiene su secuencia de historias escrita frame por frame — está dentro del desarrollo de la pieza, en la sección 5."));

/* ═══════════════════════════════ 7 · PAUTA ═══════════════════════════════ */
push(pageBreak());
push(H1("7 · VENTA y PAUTA — los anuncios (copy listo)"));
push(P("Estas piezas SÍ venden y van a pauta. Todas llevan a WhatsApp — nunca a landing. El dato es contundente: landing = CPL $164.64 · WhatsApp = CPL $0.45.",{run:{color:RED,bold:true}}));
push(H2("Cómo se separa el contenido de valor del de venta"));
push(tbl(["","CONTENIDO DE VALOR (orgánico)","VENTA / PAUTA (ads)"],[
 ["Objetivo","Conversación, guardados, autoridad","Leads a WhatsApp"],
 ["Proporción del mes","~70%","~30%"],
 ["CTA","«Comenta BIM / IA / ACERO»","Botón directo a WhatsApp"],
 ["Dónde vive","Orgánico (IG, FB, LinkedIn, TikTok)","Meta Ads"],
 ["Métrica que importa","Comentarios y guardados","Leads y CPL"],
 ["Nunca","Vender directo ni poner precio","Mandar a una landing"],
],[1900,4200,4100]));
push(note("Regla para las piezas de venta orgánica: NUNCA abrir con «inscríbete» ni con el precio. Se abre con valor o con un dolor real, y el CTA solo invita a conversar. La promo pura fue el peor post del mes."));
CAL.pauta.forEach((id,i)=>push(renderPieza({id,fecha:'ANUNCIO '+(i+1),
  formato_publicacion:'Imagen para pauta',redes:'Meta Ads (Instagram + Facebook)',
  nota:'Se activa en paralelo al contenido orgánico. El orgánico calienta; la pauta cierra.'},i)));

/* ═══════════════════════════════ 7 · BANCO DE RESERVA ═══════════════════════════════ */
push(pageBreak());
push(H1("8 · Banco de reserva (piezas listas por si se cae alguna)"));
push(P("Estas piezas ya tienen su contenido completo escrito. Si una fecha se cae o quieres reforzar una red concreta, se toma de aquí sin tener que crear nada.",{run:{color:GREY}}));
push(tbl(["Pieza","Formato","Red pensada","Hook"],
  CAL.banco_reserva.filter(id=>BY[id]).map(id=>{const p=BY[id];
    return [p.titulo,p.formato,NOMBRE_RED[p.red_principal]||p.red_principal,p.hook];}),
  [3000,1300,1500,4400]));
push(note("El contenido palabra por palabra de todas estas piezas está en el archivo guiones-completos.json del repositorio, que es el mismo que lee la app de contenido."));

/* ═══════════════════════════════ 8 · CIERRE ═══════════════════════════════ */
push(H1("9 · Resumen operativo y checklist"));
const cuenta={};
CAL.piezas.forEach(e=>{const f=(e.formato_publicacion.split(' ')[0]||'').toUpperCase();
  cuenta[f]=(cuenta[f]||0)+1;});
push(tbl(["Formato","Piezas en el mes"],Object.entries(cuenta).map(([k,v])=>[k,String(v)]),[3600,2000]));
push(note("El conteo incluye las 3 piezas pendientes de tus datos (Vie 22, Sáb 30 y Lun 31). Sin ellas: "+
  (CAL.piezas.length-3)+" piezas con contenido ya escrito y listo para producir."));
push(P("Proporción del mes: ~70% contenido de valor · ~30% venta (2 piezas de venta orgánica con gancho + los 3 anuncios de pauta de la sección 6). Del total, 3 piezas alimentan ACERO — el producto de mejor CPL, que hasta ahora el orgánico casi no cubría."));
push(H2("Checklist antes de publicar cada pieza"));
push(bul("¿Es NÚCLEO (BIM · IA · modelado · acero) y no obra genérica?"));
push(bul("¿Tiene algo concreto en pantalla (demo, captura, esquema) y no solo alguien hablando?"));
push(bul("¿Cierra con una PREGUNTA directa sobre una duda real del que mira?"));
push(bul("¿El CTA es el correcto — ACERO o BIM/IA — y está adaptado si va a LinkedIn?"));
push(bul("¿Se publicó también en Facebook, cuidado y no como auto-repost?"));
push(bul("¿Se registró en la matriz con sus métricas, incluidas las de Facebook?"));
push(H2("Lo que falta que me pases"));
push(bul("Vie 22 — el proyecto o caso de alumno (nombre, antes/después, qué estudió, resultado)."));
push(bul("Sáb 30 — los datos de la conferencia o convención (nombre, fecha, quién expone, tema)."));
push(bul("Mié 13 — si el nuevo lead magnet BIM+IA está listo, entra ahí y desplaza la pieza de venta."));
push(new Paragraph({spacing:{before:340},
  border:{top:{style:BorderStyle.SINGLE,size:8,color:"D9E0E7",space:8}},
  children:[new TextRun({text:"Design Modeling Academy · Matriz de contenido agosto 2026 · Construida sobre la matriz viral (124 reels) y el rendimiento real de las campañas activas",size:17,color:GREY})]}));

/* ═══════════════════════════════ SALIDA ═══════════════════════════════ */
const doc=new Document({styles:{default:{document:{run:{font:"Calibri"}}}},
 sections:[{properties:{page:{size:{width:12240,height:15840},
   margin:{top:900,bottom:900,left:900,right:900}}},children:b}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/Matriz-Contenido-Agosto-2026-DMA.docx');
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync(OUT,buf);
  console.log('OK →',OUT,(buf.length/1024).toFixed(0)+' KB');});
