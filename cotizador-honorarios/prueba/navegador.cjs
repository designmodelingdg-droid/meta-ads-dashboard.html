/* Prueba en navegador del cotizador: candado, cálculo en vivo, ajuste al mínimo,
 * país con retenciones, propuesta imprimible y sin errores de JS.
 *   NODE_PATH=$(npm root -g) node cotizador-honorarios/prueba/navegador.cjs [carpeta de capturas]
 */
const { chromium } = require('playwright');
const path = require('path');
const OUT = process.argv[2] || '.';
const BASE = 'file://' + path.join(__dirname, '..') + '/app.html';
let fallos = 0; const es = (c,t)=>{ console.log(`  ${c?'sí':'NO'} · ${t}`); if(!c) fallos++; };
(async()=>{
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium', args:['--ignore-certificate-errors']});
  const ctx = await b.newContext({viewport:{width:1280,height:900}});
  const errs = []; ctx.on('page', p=> p.on('pageerror', e=> errs.push(e.message)));
  let p = await ctx.newPage();
  await p.goto(BASE, {waitUntil:'load'});
  es(await p.isVisible('#lock'), 'sin token: se ve el candado');
  await p.goto(BASE + '?acceso=dm2026', {waitUntil:'load'}); await p.waitForTimeout(500);
  es(!(await p.isVisible('#lock')), 'con token: sin candado');
  await p.goto(BASE, {waitUntil:'load'});
  es(!(await p.isVisible('#lock')), 'el token queda recordado');
  const golpe = await p.textContent('.golpe');
  es(/por hora/.test(golpe) && /NO CUBRE/.test(golpe), 'el ejemplo muestra la tarifa real y NO CUBRE');
  es(/14,71/.test(golpe), 'tarifa real del ejemplo = 14,71 USD/h');
  await p.screenshot({path: path.join(OUT,'app-escritorio.png'), fullPage:true});
  await p.click('#ajustar'); await p.waitForTimeout(200);
  es(/✔ CUBRE/.test(await p.textContent('.golpe')), 'ajustar al mínimo deja el precio cubriendo la tarifa');
  es(await p.inputValue('#precioM2') === '5.89', 'precio por m² ajustado a 5,89');
  await p.selectOption('#pais', 'DO'); await p.waitForTimeout(150);
  es(/ITBIS/.test(await p.textContent('#ivaLbl')), 'República Dominicana usa ITBIS');
  await p.check('[data-ret=do_isr]'); await p.waitForTimeout(150);
  es(/Retención de ISR 15/.test(await p.textContent('#resBody')), 'la retención de ISR 15 % aparece en el resultado');
  es(/DOP/.test(await p.textContent('.golpe')), 'la moneda cambia a DOP');
  await p.fill('#hitos', '50, 30'); await p.dispatchEvent('#hitos','input'); await p.waitForTimeout(150);
  es(/suman 80/.test(await p.textContent('#resBody')), 'avisa si los hitos no suman 100');
  await p.fill('#hitos', '40, 40, 20'); await p.dispatchEvent('#hitos','input');
  await p.fill('#pCliente', 'Constructora de prueba'); await p.dispatchEvent('#pCliente','input');
  await p.emulateMedia({media:'print'});
  const prop = await p.textContent('#propuesta');
  es(/Constructora de prueba/.test(prop) && /No incluye/.test(prop) && /Forma de pago/.test(prop), 'la propuesta trae cliente, exclusiones y forma de pago');
  es(!/\d h\b|horas/.test(prop), 'la propuesta no muestra horas');
  es(/<li>Visitas de obra<\/li>/.test(await p.innerHTML('#propuesta')), 'sin visitas incluidas, la exclusión dice «Visitas de obra»');
  es(await p.getAttribute('#ivaManual','hidden') !== null, 'con país conocido no se pide la tasa');
  await p.pdf({path: path.join(OUT,'propuesta-ejemplo.pdf'), format:'A4', printBackground:true});
  await p.emulateMedia({media:'screen'});
  const m = await ctx.newPage(); await m.setViewportSize({width:390,height:844});
  await m.goto(BASE, {waitUntil:'load'}); await m.waitForTimeout(400);
  const sw = await m.evaluate(()=> document.documentElement.scrollWidth);
  es(sw <= 390, `en celular no hay scroll horizontal (${sw}px)`);
  await m.screenshot({path: path.join(OUT,'app-celular.png'), fullPage:false});
  es(errs.length === 0, 'sin errores de JS' + (errs.length? ': '+errs.join(' | ') : ''));
  await b.close();
  console.log(fallos ? `\n${fallos} FALLOS` : '\nprueba OK'); process.exit(fallos?1:0);
})();
