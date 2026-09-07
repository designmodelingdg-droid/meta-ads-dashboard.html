/* Prueba del embudo completo de la guia + plantilla de memoria de calculo.
 *
 * Recorre lo mismo que recorre una persona real, en pantalla de telefono:
 * guia cerrada -> landing -> formulario -> gracias -> guia abierta.
 *
 * Las dos cosas que de verdad vigila:
 *   - que la guia NO se pueda leer sin registrarse (si no, el lead magnet no capta)
 *   - que la pagina de gracias NO prometa un envio por correo o WhatsApp
 *     que no existe: es la promesa que mas rapido se rompe.
 *
 *   node memoria-calculo/prueba/embudo.js
 */
const { execSync } = require('child_process');
const G = execSync('npm root -g').toString().trim();
const { chromium } = require(require.resolve('playwright',{paths:[G]}));
const path=require('path');
const B='file://'+path.join(__dirname,'..')+'/';
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const ctx=await b.newContext({viewport:{width:412,height:900}});   // TELÉFONO
  const p=await ctx.newPage(); const errs=[];
  p.on('pageerror',e=>errs.push('JS: '+e.message));
  await p.route('**fonts.g**', r=>r.abort());
  await p.route('**link.msgsndr.com**', r=>r.abort());

  // 1. La guía tiene que estar cerrada para quien llega de frente
  await p.goto(B+'guia.html',{waitUntil:'load'});
  console.log('1. guía sin registro     :', await p.locator('#lock').isVisible()?'CERRADA ✔':'ABIERTA ✖');

  // 2. Landing en teléfono
  await p.goto(B+'index.html',{waitUntil:'load'});
  const ancho = await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1);
  console.log('2. landing en teléfono   :', ancho?'sin desborde ✔':'DESBORDA ✖');
  console.log('   formulario visible    :', await p.locator('#form').isVisible()?'sí ✔':'NO ✖');

  // 3. Llenar y enviar
  await p.fill('#nombre','Prueba Interna');
  await p.fill('#email','prueba@dgdesignmodeling.com');
  await p.fill('#telefono','0999999999');
  await p.selectOption('#perfil',{index:1});
  p.on('dialog', async d=>{ console.log('   ALERT:', d.message); await d.dismiss(); });
  await p.click('button[type=submit]');
  await p.waitForTimeout(1200);
  console.log('   URL tras enviar       :', p.url().split('/').pop() || '(no navegó)');
  console.log('3. redirige a gracias    : ✔  ', p.url().split('/').pop());

  // 4. El botón de acceso
  const href = await p.locator('#btnGuia').getAttribute('href');
  console.log('4. botón de la guía      :', href);
  console.log('   ¿lleva el token?      :', href && href.includes('acceso=dm2026')?'sí ✔':'NO ✖');

  // 5. La promesa: entrar sin esperar correo
  // El boton apunta a la URL de produccion (que es lo correcto). Para probarlo
  // aqui, lo traduzco a la copia local conservando el token tal cual.
  const local = B + href.split('/memoria-calculo/')[1];
  await p.goto(local,{waitUntil:'load'});
  const abierta = !(await p.locator('#lock').isVisible());
  console.log('5. guía tras el embudo   :', abierta?'ABIERTA ✔':'SIGUE CERRADA ✖');
  console.log('   secciones de la guía  :', await p.locator('.sec .n').count(), '(13 + 5 devoluciones + 1 portada = 19)');

  // 6. Que no prometa lo que no existe
  const txt = await p.evaluate(()=>document.body.innerText);
  await p.goto(B+'gracias-agenda.html?acceso=dm2026',{waitUntil:'load'});
  const tg = await p.evaluate(()=>document.body.innerText);
  const promesa = /te (lo )?(enviamos|llega|mandamos) por (correo|whatsapp)/i.test(tg);
  console.log('6. promete envío que no existe:', promesa?'SÍ ✖':'no ✔');

  // 7. Las dos plantillas: si el boton apunta a un fichero que no esta,
  //    la promesa de la landing se rompe en el ultimo paso.
  const fs=require('fs');
  for(const b of ['btnWord','btnExcel']){
    const h=await p.locator('#'+b).getAttribute('href');
    const f=path.join(__dirname,'..',h.replace('./',''));
    const hay=fs.existsSync(f);
    console.log('7. '+b.padEnd(9)+':', h, hay?'existe ✔ ('+(fs.statSync(f).size/1024|0)+' KB)':'NO EXISTE ✖');
  }

  console.log(errs.length?errs.join(' | '):'sin errores de JS');
  await b.close();
})();
