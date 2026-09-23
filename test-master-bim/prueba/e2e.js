/* Prueba de punta a punta del Diagnóstico BIM del Máster.
 *
 * Contesta el test, arma el enlace que se guarda en `enlace_resultado` del
 * CRM, lo abre como lo abriría el asesor y comprueba que el panel dice lo
 * mismo que calculó el test.
 *
 * Lo que de verdad vigila: que el test y el panel no se separen. Comparten
 * `preguntas.js` justamente para eso, y esta prueba lo verifica.
 *
 * Desde el 23-sep el test empieza con dos preguntas de PUNTO DE PARTIDA
 * (¿cuánto BIM sabes? ¿qué te interesa?) y quien dice que no ha trabajado con
 * BIM se salta el eje A. Por eso corre TRES recorridos:
 *
 *   A · con experiencia: los mismos 20 de siempre, más el punto de partida.
 *       Tiene que salir el MISMO código que salía antes del cambio.
 *   B · un enlace de 20 dígitos, de los que ya están enviados a citas. Tiene
 *       que abrir exactamente igual que antes: es lo que no se puede romper.
 *   C · sin BIM y con interés en la IA: 8 preguntas, «No se preguntó» en el
 *       eje BIM, y los avisos para el asesor en el CRM pero NO en el panel.
 *
 *   node test-master-bim/prueba/e2e.js
 */
/* playwright esta instalado global en este contenedor, no en el repo */
const { execSync } = require('child_process');
const GLOBAL = execSync('npm root -g').toString().trim();
module.paths.push(GLOBAL);
const { chromium } = require(require.resolve('playwright', {paths:[GLOBAL, __dirname]}));
const path=require('path');
const fs=require('fs');
const BASE='file://'+path.join(__dirname,'..')+'/';

/* Un enlace real de los de antes del 23-sep. Es la foto fija contra la que se
   comprueba que el cambio no movió nada: su código era B2-EST-57. */
const ENLACE_VIEJO = '33333322110000332110';
const CODIGO_VIEJO = 'B2-EST-57';

const fallos = [];
const ok = (cond, texto) => { console.log(`  ${cond?'sí':'NO'} · ${texto}`); if(!cond) fallos.push(texto); };

/* Hace el test como una persona: primero el punto de partida, luego lo que
   toque. Devuelve lo que el test calculó y lo que de verdad va al CRM. */
async function recorrer(b, entrada, respuestas){
  const p=await b.newPage({viewport:{width:430,height:1000}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto(BASE+'app.html?cid=CT123&nombre=Andrea',{waitUntil:'load'});
  const clics = [...entrada, ...respuestas];
  for(const v of clics){ await p.locator('.op').nth(v).click(); await p.waitForTimeout(190); }
  await p.waitForSelector('.cita');
  const out = await p.evaluate(()=>{
    const r = calcular(R, E);
    return { r:{codigo:r.codigo, nombreNivel:r.nombreNivel, sinBIM:r.sinBIM, avisos:r.avisos},
             datos: datosParaGHL(r), pasos: pasos().length };
  });
  out.visible = await p.locator('body').innerText();
  out.errs = errs;
  out.pagina = p;
  return out;
}

async function abrirPanel(b, enlace){
  const q=await b.newPage({viewport:{width:1280,height:1000}});
  const errs=[]; q.on('pageerror',e=>errs.push(e.message));
  await q.goto(enlace,{waitUntil:'load'});
  await q.waitForSelector('.top h1');
  const panel = {
    titulo: (await q.locator('.top h1').innerText()).trim(),
    texto:  await q.locator('body').innerText(),
    nResp:  await q.locator('section', {hasText:'Lo que respondiste'}).locator('.r').count(),
    noPreg: await q.locator('.vn').count(),
    partida: await q.locator('section', {hasText:'Tu punto de partida'}).count(),
    escalera: await q.locator('.esc').innerText(),
    errs,
  };
  await q.close();
  return panel;
}

/* Lo que nunca puede aparecer en la pantalla final del test: el resultado se
   entrega en la llamada. Si se filtra aquí, la cita deja de tener motivo. */
const FUGAS = ['Modelador BIM','Coordinador BIM','BIM Manager','Especialista BIM',
               'cálculo y diseño estructural','Arquitectura y edificación',
               'Sin experiencia BIM todavía','Nivel BIM inicial'];

(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});

  /* ═══ A · con experiencia ═══════════════════════════════════════════════ */
  console.log('A · con experiencia (usa BIM en proyectos · ruta completa)');
  const A = await recorrer(b, [2,3], [3,3,3,3, 3,3,2,2, 1,1,0, 0,0,0, 3,3,2, 1,1,0]);
  ok(A.pasos === 22, `22 preguntas (2 de punto de partida + 20) — fueron ${A.pasos}`);
  ok(A.r.codigo === CODIGO_VIEJO, `mismo código que antes del cambio: ${A.r.codigo}`);
  const enlaceA = A.datos['enlace_del_resultado'];
  const rA = new URL(enlaceA).searchParams.get('r');
  ok(rA === ENLACE_VIEJO + '23', `el enlace = los 20 de siempre + 2 detrás: ${rA}`);
  ok(!FUGAS.some(t => A.visible.includes(t)), 'la pantalla final no suelta el resultado');

  /* ── Montaje del formulario de GHL ──────────────────────────────────────
     Estas comprobaciones existen porque los tres fallos que tuvo el montaje
     del 9-sep no los veia nadie a simple vista:
       · 6 de las 7 claves no coincidian con las del formulario (GHL las genera
         desde la etiqueta, CON TILDES) y esos campos llegaban vacios;
       · GHL borra el signo «+», asi que «Especialista BIM + IA» llegaba roto;
       · el formulario iba en un iframe de altura 0 y la pantalla decia «Listo,
         tu asesor ya lo tiene» sin que nadie lo hubiera enviado.
     Se comprueba el objeto que de verdad se envía (datosParaGHL), no una
     copia: la copia fue lo que dejaba esto en verde aunque el envío cambiara. */
  console.log('\nmontaje del formulario:');
  const CLAVES_DEL_FORM = ['nivel_bim','perfil_técnico','código_de_diagnóstico',
    'módulo_recomendado','enlace_del_resultado','detalle_del_diagnóstico',
    'puntajes_por_bloque'];
  const dir = path.join(__dirname,'..');
  const appTxt = fs.readFileSync(path.join(dir,'app.html'),'utf8');
  const idxTxt = fs.readFileSync(path.join(dir,'index.html'),'utf8');
  ok(appTxt === idxTxt, 'app.html e index.html idénticos (el enlace sirve index.html)');
  /* se le pregunta a la pagina, no al texto: la cadena PEGAR_ID tambien
     aparece en el `if` que detecta el marcador */
  const formUrl = await A.pagina.evaluate(() => CFG.FORM_GHL);
  ok(!formUrl.includes('PEGAR_ID'), 'formulario conectado — ' + formUrl.split('/').pop());
  ok(Object.keys(A.datos).length === 7 && Object.keys(A.datos).every(k => CLAVES_DEL_FORM.includes(k)),
     'se mandan exactamente las 7 claves del formulario, ninguna nueva');
  ok(!Object.values(A.datos).some(v => String(v).includes('+')), 'ningún valor lleva «+» (GHL lo borra)');
  ok(!/ya lo tiene|Listo\. Tu asesor/.test(appTxt.split('cont.innerHTML = `').pop()),
     'la pantalla NO da por enviado lo que no se envió');
  ok(!/iframe[^>]*height:0/.test(appTxt), 'el formulario se ve (no va en altura 0)');
  /* El aviso del correo es lo unico que separa «se actualiza su ficha» de
     «se crea un contacto duplicado». Esta prueba corre SIN email en el enlace. */
  ok(/mismo correo/i.test(await A.pagina.locator('.aviso-correo').innerText()),
     'avisa de usar el mismo correo (evita duplicar)');
  const pasaTel = await A.pagina.evaluate(() =>
    limpiaTel('0983241210') === '0983241210' && limpiaTel(' 593983241210') === '593983241210'
    && limpiaTel('') === '' && limpiaTel('abc') === '');
  ok(pasaTel && /datos\.phone\s*=\s*CONTACTO\.tel/.test(appTxt), 'el teléfono del enlace llega al formulario');
  await A.pagina.close();

  console.log('\npanel del asesor (A):');
  const PA = await abrirPanel(b, enlaceA);
  ok(PA.titulo.includes(A.r.nombreNivel), `título: ${PA.titulo}`);
  ok(PA.nResp === 20, `20 respuestas en «Lo que respondiste» — son ${PA.nResp}`);
  ok(PA.partida === 1, 'enseña el punto de partida');

  /* ═══ B · un enlace de los ya enviados ═══════════════════════════════════ */
  console.log('\nB · enlace viejo de 20 dígitos (los que ya están en las citas)');
  const PB = await abrirPanel(b, BASE+'resultado.html?r='+ENLACE_VIEJO+'&n=Andrea');
  ok(PB.titulo === 'Andrea, tu nivel es Coordinador BIM', `título: ${PB.titulo}`);
  ok(PB.texto.includes('Código '+CODIGO_VIEJO), 'mismo código que antes: '+CODIGO_VIEJO);
  ok(PB.texto.includes('20 competencias evaluadas · 57% de dominio global'),
     '«20 competencias evaluadas · 57% de dominio global», como antes');
  ok(PB.nResp === 20 && PB.noPreg === 0, `20 respuestas y ninguna «No se preguntó»`);
  ok(PB.partida === 0, 'no inventa un punto de partida que el enlace no trae');

  /* ═══ C · sin BIM, viene por la IA ═══════════════════════════════════════ */
  console.log('\nC · sin BIM y con interés en la IA');
  const C = await recorrer(b, [0,2], [3,3,2, 1,1,0]);
  ok(C.pasos === 8, `solo 8 preguntas: 2 de punto de partida + 6 de base técnica — fueron ${C.pasos}`);
  ok(C.r.codigo.startsWith('B0-'), `el código conserva su formato: ${C.r.codigo}`);
  ok(C.datos['nivel_bim'] === 'Sin experiencia BIM todavía', `nivel_bim en el CRM: «${C.datos['nivel_bim']}»`);
  const det = C.datos['detalle_del_diagnóstico'];
  ok(det.includes('PUNTO DE PARTIDA: Sin experiencia BIM') && det.includes('LE INTERESA: Sobre todo la IA'),
     'el detalle del CRM trae el punto de partida');
  ok(det.includes('OJO:') && det.includes('la base BIM es el camino'),
     'el detalle del CRM trae el aviso para el asesor');
  ok(!Object.values(C.datos).some(v => String(v).includes('+')), 'ningún valor lleva «+»');
  ok(!/Modelador BIM — \d/.test(det) && det.includes('Modelador BIM — no se preguntó'),
     'el detalle del CRM tampoco puntúa lo que no se preguntó');
  ok(!FUGAS.some(t => C.visible.includes(t)), 'la pantalla final no suelta el resultado');
  await C.pagina.close();

  console.log('\npanel del asesor (C):');
  const PC = await abrirPanel(b, C.datos['enlace_del_resultado']);
  ok(PC.titulo === 'Andrea, tu ruta empieza por la base', `título que ve la persona: ${PC.titulo}`);
  ok(PC.noPreg === 14, `las 14 del eje BIM salen «No se preguntó» — son ${PC.noPreg}`);
  ok(PC.texto.includes('6 competencias técnicas evaluadas'), 'dice cuántas se evaluaron de verdad');
  /* Solo en la ESCALERA: la base técnica sí se preguntó y su «8 de 9» es
     legítimo. La primera versión de esta comprobación miraba toda la página y
     daba por fallo justo eso. */
  ok(!/\d+ de \d+/.test(PC.escalera) && (PC.escalera.match(/no se evaluó/g)||[]).length === 4
     && !PC.texto.includes('dominio global'),
     'la escalera no puntúa lo que no se preguntó: 4 × «no se evaluó», sin «% de dominio»');
  ok(PC.texto.includes('Te interesa sobre todo la IA'), 'le explica a la persona dónde entra la IA');
  /* El panel se comparte EN PANTALLA con el prospecto. Los avisos son para el
     asesor: no pueden aparecer aquí. */
  ok(!PC.texto.includes('OJO') && !PC.texto.includes('la base BIM es el camino')
     && !PC.texto.includes('Preguntarle'), 'los avisos del asesor NO salen en el panel compartido');

  const errs = [...A.errs, ...PA.errs, ...PB.errs, ...C.errs, ...PC.errs];
  console.log(errs.length ? '\nJS: '+errs.join(' | ') : '\nsin errores de JS');
  if(errs.length) fallos.push('errores de JS');
  await b.close();

  if(fallos.length){ console.log(`\nPRUEBA FALLIDA — ${fallos.length}:`); fallos.forEach(f=>console.log('  · '+f)); process.exit(1); }
  console.log('prueba OK');
})();
