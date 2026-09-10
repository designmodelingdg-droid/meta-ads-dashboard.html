/* Comprueba que cada landing lleva anclado SU formulario nativo de GHL -el que
   toca, no el de otro recurso- y que el formulario propio de respaldo ya no se
   muestra. Se revisan las dos versiones: index.html (GitHub Pages) y
   ghl-landing.html (la que se pega en GHL), porque son archivos distintos y
   nada impide que se separen.

   Uso:  node scripts/prueba_ghl_form.js                                      */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const REPO = '/home/user/meta-ads-dashboard.html/';

const ESPERADO = {
  'guia-revit-ia':   'plyahRxXWHMgtqPPSsog',
  'memoria-calculo': 'BXVAWaiA6dYGPYZiQiRg',
  'pack-dynamo':     'Io7ZfUKHiS08NO9C5VBs',
};

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  let mal = false;
  for (const [d, id] of Object.entries(ESPERADO)) {
    for (const cual of ['index.html', 'ghl-landing.html']) {
      const p = await b.newPage({ viewport: { width: 900, height: 900 } });
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto('file://' + REPO + d + '/' + cual, { waitUntil: 'load' });
      await p.waitForTimeout(700);
      const r = await p.evaluate(() => {
        const box = document.getElementById('formBox');
        const f = box ? box.querySelector('iframe') : null;
        return {
          hayCaja: !!box,
          src: f ? f.getAttribute('src') : null,
          formId: f ? f.getAttribute('data-form-id') : null,
          propio: !!document.querySelector('#form input#email'),
        };
      });
      // el formulario nativo debe estar puesto, y el propio de respaldo fuera
      const ok = r.hayCaja && r.src && r.src.includes(id) && r.formId === id && !r.propio && !errs.length;
      console.log((d + '/' + cual).padEnd(34), ok ? 'OK' : 'MAL',
                  ' form:', r.formId || '(ninguno)', ' respaldo visible:', r.propio);
      if (!ok) { mal = true; if (errs.length) console.log('   errores:', errs); }
      await p.close();
    }
  }
  await b.close();
  console.log(mal ? '\nPRUEBA MAL' : '\nprueba OK');
  process.exit(mal ? 1 : 0);
})();
