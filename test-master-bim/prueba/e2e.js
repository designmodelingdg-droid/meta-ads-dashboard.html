/* Prueba de punta a punta del Diagnóstico BIM del Máster.
 *
 * Contesta las 20 preguntas en el test, arma el enlace que se guarda en
 * `enlace_resultado` del CRM, lo abre como lo abriría el asesor y comprueba
 * que el panel dice lo mismo que calculó el test.
 *
 * Lo que de verdad vigila: que el test y el panel no se separen. Comparten
 * `preguntas.js` justamente para eso, y esta prueba lo verifica.
 *
 *   node test-master-bim/prueba/e2e.js
 */
/* playwright esta instalado global en este contenedor, no en el repo */
const { execSync } = require('child_process');
const GLOBAL = execSync('npm root -g').toString().trim();
module.paths.push(GLOBAL);
const { chromium } = require(require.resolve('playwright', {paths:[GLOBAL, __dirname]}));
const path=require('path');
const BASE='file://'+path.join(__dirname,'..')+'/';
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:430,height:1000}});
  let fugas=0;
  const errs=[]; p.on('pageerror',e=>errs.push('test: '+e.message));
  await p.goto(BASE+'app.html?cid=CT123&nombre=Andrea',{waitUntil:'load'});
  const resp=[3,3,3,3, 3,3,2,2, 1,1,0, 0,0,0, 3,3,2, 1,1,0];
  for(let i=0;i<20;i++){ await p.locator('.op').nth(resp[i]).click(); await p.waitForTimeout(190); }
  await p.waitForSelector('.cita');

  const payload = await p.evaluate(()=>{
    const r=calcular(R);
    const e=new URL('resultado.html',location.href);
    e.searchParams.set('r',empaquetar(R)); e.searchParams.set('n',CONTACTO.nombre);
    return { enlace:e.toString(), codigo:r.codigo, nivel:r.nombreNivel };
  });
  console.log('enlace que se guarda en GHL:');
  console.log('  ' + payload.enlace.replace(BASE,'…/test-master-bim/'));
  console.log('  nivel real:', payload.nivel, '·', payload.codigo);

  /* Lo que mas importa: la pantalla final NO puede soltar el nivel ni el
     perfil. El resultado se entrega en la llamada; si se filtra aqui, la cita
     deja de tener motivo y no nos enteramos hasta ver caer la asistencia. */
  const visible = await p.locator('body').innerText();
  const filtra = ['Modelador BIM','Coordinador BIM','BIM Manager','Especialista BIM',
                  'cálculo y diseño estructural','Arquitectura y edificación']
                 .filter(t => visible.includes(t));
  console.log('  pantalla final filtra el resultado:',
              filtra.length ? 'SI — ' + filtra.join(', ') : 'no');
  fugas = filtra.length;
  const p2 = p;
  /* ── Montaje del formulario de GHL ──────────────────────────────────────
     Estas cuatro comprobaciones existen porque los tres fallos que tuvo el
     montaje del 9-sep no los veia nadie a simple vista:
       · 6 de las 7 claves no coincidian con las del formulario (GHL las genera
         desde la etiqueta, CON TILDES) y esos campos llegaban vacios;
       · GHL borra el signo «+», asi que «Especialista BIM + IA» llegaba roto;
       · el formulario iba en un iframe de altura 0 y la pantalla decia «Listo,
         tu asesor ya lo tiene» sin que nadie lo hubiera enviado.
     Las claves se comparan contra una copia de las `data-q` del formulario
     real. Si alguien renombra una etiqueta en GHL, esto falla y se entera. */
  const CLAVES_DEL_FORM = ['nivel_bim','perfil_técnico','código_de_diagnóstico',
    'módulo_recomendado','enlace_del_resultado','detalle_del_diagnóstico',
    'puntajes_por_bloque'];

  const fs2 = require('fs');
  const dir = path.join(__dirname,'..');
  const appTxt = fs2.readFileSync(path.join(dir,'app.html'),'utf8');
  const idxTxt = fs2.readFileSync(path.join(dir,'index.html'),'utf8');

  console.log('\nmontaje del formulario:');
  const gemelos = appTxt === idxTxt;
  console.log('  app.html e index.html idénticos:', gemelos ? 'sí' : 'NO — se separaron');
  /* se le pregunta a la pagina, no al texto: la cadena PEGAR_ID tambien
     aparece en el `if` que detecta el marcador, y buscarla en el fuente daba
     un falso positivo */
  const formUrl = await p2.evaluate(() => CFG.FORM_GHL);
  const sinPegar = !formUrl.includes('PEGAR_ID');
  console.log('  formulario conectado:', sinPegar ? 'sí — ' + formUrl.split('/').pop() : 'NO, sigue el marcador');

  const envio = await p2.evaluate(()=>{
    const r = calcular(R);
    const e = new URL('resultado.html', location.href);
    e.searchParams.set('r', empaquetar(R));
    return {
      [CFG.CAMPOS.nivel]:    paraGHL(r.nivel===0?'En camino a Modelador BIM':BLOQUES[r.nivel-1].nivel),
      [CFG.CAMPOS.perfil]:   paraGHL(r.perfil),
      [CFG.CAMPOS.modulo]:   paraGHL(r.siguiente ? r.siguiente.modulo : 'Ruta completa'),
      [CFG.CAMPOS.codigo]:   r.codigo,
      [CFG.CAMPOS.enlace]:   e.toString(),
      [CFG.CAMPOS.detalle]:  paraGHL(detalleTexto(r)),
      [CFG.CAMPOS.puntajes]: r.bloques.map(b=>b.id+':'+b.pts+'/'+b.max).join(' '),
    };
  });
  const enviadas = Object.keys(envio);
  const noExisten = enviadas.filter(k => !CLAVES_DEL_FORM.includes(k));
  console.log('  las 7 claves existen en el formulario:',
              noExisten.length ? 'NO — ' + noExisten.join(', ') : 'sí');
  /* el enlace lleva «/» y «?» pero nunca «+»; los demas tampoco deben llevarlo */
  const conMas = Object.entries(envio).filter(([k,v]) => String(v).includes('+'));
  console.log('  ningún valor lleva «+» (GHL lo borra):',
              conMas.length ? 'NO — ' + conMas.map(([k])=>k).join(', ') : 'sí');

  const mienteEntrega = /ya lo tiene|Listo\. Tu asesor/.test(
      appTxt.split('cont.innerHTML = `').pop());
  console.log('  la pantalla NO da por enviado lo que no se envió:',
              mienteEntrega ? 'NO — sigue diciéndolo' : 'sí');
  const alturaCero = /iframe[^>]*height:0/.test(appTxt);
  console.log('  el formulario se ve (no va en altura 0):', alturaCero ? 'NO' : 'sí');

  /* El aviso del correo es lo unico que separa «se actualiza su ficha» de
     «se crea un contacto duplicado». Casi todos llegan desde pauta y ya tienen
     ficha: si escriben otro correo, el asesor acaba con la persona partida en
     dos. Esta prueba corre SIN email en el enlace, asi que toca la rama que
     pide escribir el mismo correo. */
  const aviso = await p2.locator('.aviso-correo').innerText();
  const avisaDelCorreo = /mismo correo/i.test(aviso);
  console.log('  avisa de usar el mismo correo (evita duplicar):',
              avisaDelCorreo ? 'sí' : 'NO');

  /* El telefono del formulario es obligatorio: si no viaja en el enlace, la
     persona lo teclea y lo tecleado SUSTITUYE al del CRM. Se comprueba que el
     enlace lo lleve hasta el formulario, con los dos nombres de parametro. */
  const pasaTel = await p2.evaluate(() => {
    /* se llama a la funcion DE LA PAGINA, no a una copia: si el saneador
       cambia, la prueba lo nota */
    const local   = limpiaTel('0983241210') === '0983241210';
    const roto    = limpiaTel(' 593983241210') === '593983241210';
    const basura  = limpiaTel('') === '' && limpiaTel('abc') === '';
    return local && roto && basura;
  });
  const mandaTel = /datos\.phone\s*=\s*CONTACTO\.tel/.test(appTxt);
  console.log('  el teléfono del enlace llega al formulario:',
              pasaTel && mandaTel ? 'sí' : 'NO');

  const montajeMal = !gemelos || !sinPegar || noExisten.length || conMas.length
                     || mienteEntrega || alturaCero || !avisaDelCorreo
                     || !pasaTel || !mandaTel;
  await p.close();

  // el asesor abre ese enlace
  const q=await b.newPage({viewport:{width:1280,height:1000},deviceScaleFactor:2});
  const e2=[]; q.on('pageerror',e=>e2.push('panel: '+e.message));
  await q.goto(payload.enlace,{waitUntil:'load'});
  await q.waitForSelector('.top h1');
  const titulo=(await q.locator('.top h1').innerText()).trim();
  const perfil=(await q.locator('.top .perfil').innerText()).trim();
  const nResp=await q.locator('.r').count();
  console.log('\npanel del asesor:');
  console.log('  titulo   :', titulo);
  console.log('  perfil   :', perfil);
  console.log('  respuestas mostradas:', nResp, '(deben ser 20)');
  console.log('  coincide con el test:', titulo.includes(payload.nivel) ? 'sí' : 'NO');
  console.log(errs.concat(e2).length ? '\nJS: '+errs.concat(e2).join(' | ') : '\nsin errores de JS');
  await b.close();

  const mal = fugas || nResp!==20 || !titulo.includes(payload.nivel)
              || errs.concat(e2).length || montajeMal;
  if(mal){ console.log('\nPRUEBA FALLIDA'); process.exit(1); }
  console.log('prueba OK');
})();
