/* Pendientes de la reunion de cierre y apertura, en Word para el equipo.
 * Lee matriz-viral/matriz/calendario-septiembre.json (seccion pendientes_reunion)
 * para que el documento y la matriz no se puedan contradecir.
 *   node scripts/build_pendientes_docx.js
 */
const fs=require('fs'), path=require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, BorderStyle } = require('docx');

const ROOT=path.dirname(__dirname);
const CAL=JSON.parse(fs.readFileSync(path.join(ROOT,'matriz-viral/matriz/calendario-septiembre.json'),'utf8'));
const PR=CAL.pendientes_reunion, K=CAL.kpis_mensuales;
if(!PR){console.error('ERROR: falta pendientes_reunion en el calendario');process.exit(1);}

const NAVY='0E2438', ORANGE='C96A1C', GREY='5A6B7B', RED='A33B2A',
      GREEN='1E7A55', WARN='FBF0DA', ALARM='F7E5E2', OK='E2F0E9';

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:140},
  children:[new TextRun({text:t,bold:true,color:NAVY,size:32,font:'Overpass'})]});
const H2=t=>new Paragraph({spacing:{before:260,after:100},
  children:[new TextRun({text:t,bold:true,color:ORANGE,size:25,font:'Overpass'})]});
const P=(t,o={})=>new Paragraph({spacing:{after:110},
  children:[new TextRun({text:t,size:21,font:'Nunito',...(o.run||{})})]});
const CAJA=(t,color,fill)=>new Paragraph({spacing:{before:140,after:160},
  shading:{type:ShadingType.CLEAR,fill},
  border:{left:{style:BorderStyle.SINGLE,size:20,color,space:10}},
  children:[new TextRun({text:t,size:21,font:'Nunito',color})]});

const celda=(t,{b=false,w=0,fill=null,color=null}={})=>new TableCell({
  width:{size:w,type:WidthType.DXA},
  ...(fill?{shading:{type:ShadingType.CLEAR,fill}}:{}),
  margins:{top:90,bottom:90,left:130,right:130},
  children:[new Paragraph({children:[new TextRun({text:t,size:19,font:'Nunito',bold:b,
    ...(color?{color}:{})})]})]});
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
  text:'Pendientes del mes',bold:true,color:NAVY,size:42,font:'Overpass'})]}));
push(P(PR.reunion,{run:{color:GREY,italics:true}}));
push(P('Cada tarea lleva responsable y, cuando bloquea algo, qué bloquea. El orden no es cronológico: es de impacto.'));

/* ── bloqueantes ── */
push(H1('1 · Bloquean la campaña de Acero'));
push(P('Nada de la campaña sale hasta que estos cuatro estén. El precio sube a $225 porque incluye el tutor: si el anuncio sale antes, alguien paga y no lo encuentra.'));
push(tabla(['Tarea','Responsable','Estado / qué bloquea'],
  PR.bloqueantes.map(t=>[t.tarea, t.responsable, t.estado?('HECHO — '+t.bloquea):t.bloquea]),
  [3000,1500,4700]));

/* ── esta semana ── */
push(H1('2 · Esta semana'));
push(tabla(['Tarea','Responsable','Nota'],
  PR.esta_semana.map(t=>[t.tarea, t.responsable, t.nota||'—']),
  [3600,1500,4100]));

/* ── de los informes ── */
push(H1('3 · Lo que sale de los informes de KPIs'));
push(P('Once acciones que no estaban en el cierre y que salieron de los tres informes del área. La primera es la de mayor retorno de todo el paquete.'));
push(tabla(['Acción','Responsable','Por qué'],
  PR.de_los_kpis_de_ester.map(t=>[t.tarea, t.responsable, t.por_que]),
  [2900,1500,4800]));

/* ── decisiones ── */
push(H1('4 · Decisiones que faltan'));
push(P('Ninguna de estas se puede resolver por el equipo: necesitan una respuesta de Dirección para que el resto avance.'));
push(tabla(['Decisión','Quién','Por qué importa'],
  PR.decisiones_que_faltan.map(t=>[t.decision, t.quien, t.por_que]),
  [3000,1200,5000]));

/* ── contexto de números ── */
if(K){
  push(H1('5 · Contra qué números vamos'));
  push(CAJA('La facturación de agosto NO está cerrada. Hay tres cifras para el mismo mes y una diferencia de $2.902,02 sin explicar. Antes de comunicar cualquier meta hay que resolverlo.', RED, ALARM));
  push(tabla(['Fuente','Dice'],[
    ['Cobrado en pasarelas (Stripe + PayPal)', '$'+K.dinero.cobrado_pasarelas.toLocaleString('es')],
    ['Verificado por Ester', '$'+K.dinero.verificado_por_ester.toLocaleString('es')],
    ['Ganados en el CRM (lo que se presentó)', '$'+K.dinero.ganados_en_crm.toLocaleString('es')],
  ],[6400,2800]));
  push(P(''));
  push(P('De lo cobrado, $'+K.dinero.recurrente_del_master.toLocaleString('es')+' son 16 cuotas mensuales de contratos vigentes del Máster: entran solas y no las vendió nadie este mes. La captación nueva fue de unos $'+K.dinero.captacion_nueva_aprox.toLocaleString('es')+'.'));

  push(H2('Comercial'));
  push(tabla(['Indicador','Real','Meta'],[
    ['Estudiantes nuevos del Máster', String(K.comercial.estudiantes_master_nuevos.real), String(K.comercial.estudiantes_master_nuevos.meta)],
    ['Cursos lowcost', '$'+K.comercial.cursos_lowcost.real.toLocaleString('es'), '$'+K.comercial.cursos_lowcost.meta.toLocaleString('es')],
    ['Citas agendadas', String(K.comercial.citas_agendadas.real), String(K.comercial.citas_agendadas.meta)],
    ['Asistencia a citas', K.comercial.asistencia_a_citas.real+' (antes '+K.comercial.asistencia_a_citas.anterior+')', K.comercial.asistencia_a_citas.meta],
    ['Conversaciones sin asignar', K.comercial.conversaciones_sin_asignar.real+' ('+K.comercial.conversaciones_sin_asignar.n+')', '0%'],
    ['Tiempo medio de respuesta', K.comercial.tiempo_medio_respuesta.real, K.comercial.tiempo_medio_respuesta.umbral],
  ],[4000,3000,2200]));

  push(H2('Marketing'));
  push(tabla(['Indicador','Valor'],[
    ['Inversión', '$'+K.marketing.inversion.toLocaleString('es')],
    ['Leads', String(K.marketing.leads)+' · CPL $'+K.marketing.cpl],
    ['Compras en CRM', String(K.marketing.compras_crm)+' ('+K.marketing.conversion+' de conversión)'],
    ['ROAS', K.marketing.roas_adquisicion+'x de adquisición · '+K.marketing.roas_caja+'x de caja'],
    ['Ventas sin atribuir', K.marketing.sin_atribuir.pct+' ('+K.marketing.sin_atribuir.n+' de '+K.marketing.sin_atribuir.de+')'],
    ['Máster BIM', '$'+K.marketing.master_bim.gasto+' ('+K.marketing.master_bim.pct_presupuesto+' del presupuesto) · '+K.marketing.master_bim.compras+' compras'],
    ['Contenido', K.marketing.contenido.producido+' producidas · '+K.marketing.contenido.publicado+' publicada · '+K.marketing.contenido.borrador+' en borrador'],
    ['Email', K.marketing.email.envios+' envíos ('+K.marketing.email.variacion+') · '+K.marketing.email.aperturas+' aperturas · '+K.marketing.email.respuestas+' respuesta'],
  ],[3000,6200]));

  push(H2('Lo que esto le dice al contenido'));
  K.lo_que_manda_al_contenido_de_septiembre.forEach(t=>push(P('· '+t)));
}

push(H1('Dónde vive todo esto'));
push(P('Los pendientes y los KPIs están en la matriz del repositorio (calendario-septiembre.json), así que este documento y la matriz no se pueden contradecir: se regeneran del mismo archivo. La conciliación completa de agosto está en cierres/2026-08.json.'));
push(P('Grabación de la reunión: '+PR.grabacion,{run:{color:GREY}}));

const doc=new Document({styles:{default:{document:{run:{font:'Nunito',size:21}}}},
  sections:[{properties:{page:{margin:{top:900,bottom:900,left:900,right:900}}},children:h}]});
const OUT=path.join(ROOT,'matriz-viral/entregables/Pendientes-Reunion-Cierre-Septiembre-2026-DMA.docx');
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync(OUT,buf);
  const n=PR.bloqueantes.length+PR.esta_semana.length+PR.de_los_kpis_de_ester.length+PR.decisiones_que_faltan.length;
  console.log(`OK → ${OUT} (${(buf.length/1024).toFixed(0)} KB)`);
  console.log(`   ${n} pendientes · ${PR.bloqueantes.length} bloqueantes · ${PR.decisiones_que_faltan.length} decisiones`);});
