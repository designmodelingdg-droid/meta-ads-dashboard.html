/* Comprueba que el trozo de la LECCIÓN de GHL (ghl-leccion.html) deja la guía
   a su alto real, sin una segunda barra de scroll dentro de la lección.

   Por qué existe: el ajuste automático se hizo primero midiendo
   documentElement.scrollHeight, que NUNCA baja del alto de la ventana — y
   dentro de un marco la ventana es el marco. Al agrandarlo, la medida crecía
   con él y se quedaba trabada arriba: 12.457 px de contenido reportados como
   15.617, con 80 mensajes en vez de 2. Se mide el body y converge.

   Uso:  node scripts/prueba_ghl_leccion.js
   Los altos esperados son los de cada guía a 820 px de ancho, medidos con las
   imágenes y las fuentes ya cargadas.                                        */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const SCR = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/';
const REPO = '/home/user/meta-ads-dashboard.html/';

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  let mal = false;
  for (const [d, esperado] of [['guia-revit-ia', 12458], ['memoria-calculo', 9157], ['pack-dynamo', 5160]]) {
    // se simula la leccion de GHL: el trozo generado, con la guia servida en local
    const trozo = fs.readFileSync(REPO + d + '/ghl-leccion.html', 'utf8')
      .replace('https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/' + d + '/guia.html',
               'file://' + REPO + d + '/guia.html');
    const tmp = SCR + 'lec-' + d + '.html';
    fs.writeFileSync(tmp, '<!doctype html><meta charset=utf8><body style="margin:0">\n' + trozo);

    const p = await b.newPage({ viewport: { width: 820, height: 900 } });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + tmp, { waitUntil: 'load' });
    await p.waitForTimeout(3000);
    const alto = await p.evaluate(() => Math.round(document.getElementById('dma-guia').getBoundingClientRect().height));
    /* No se puede mirar dentro del marco: es otro origen y el navegador lo
       tapa a proposito. La prueba de que no hay barra interna es que el marco
       mida lo que mide el contenido: si midiera menos, habria barra. */
    const ok = Math.abs(alto - (esperado + 40)) < 120 && !errs.length;
    console.log(d.padEnd(16), 'marco', String(alto).padStart(6), 'px  = contenido',
                esperado, '+ 40  ', ok ? 'OK' : 'MAL');
    if (!ok) { mal = true; if (errs.length) console.log('   errores:', errs); }
    await p.close();
  }
  await b.close();
  console.log(mal ? '\nPRUEBA MAL' : '\nprueba OK');
  process.exit(mal ? 1 : 0);
})();
