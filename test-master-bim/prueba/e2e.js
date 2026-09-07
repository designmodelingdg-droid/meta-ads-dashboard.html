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

  const mal = fugas || nResp!==20 || !titulo.includes(payload.nivel) || errs.concat(e2).length;
  if(mal){ console.log('\nPRUEBA FALLIDA'); process.exit(1); }
  console.log('prueba OK');
})();
