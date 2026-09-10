/* Comprueba los dos botones de las páginas de gracias, en las dos versiones de
   cada una: gracias-agenda.html (GitHub Pages) y ghl-gracias.html (la que se
   pega en GHL). Son archivos distintos y nada impide que se separen.

   Qué se exige:
     · el botón 1 tiene destino real — el producto si URL_PRODUCTO está puesta,
       y si no la guía en Pages, que es lo que hace hoy;
     · el botón 2 se muestra si URL_COMUNIDAD está puesta, y se esconde si no
       (un botón que no lleva a ninguna parte es peor que ningún botón);
     · ningún botón se queda en href="#";
     · cero errores de JavaScript.

   Uso:  node scripts/prueba_ghl_gracias.js                                   */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const REPO = '/home/user/meta-ads-dashboard.html/';

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  let mal = false;
  for (const d of ['guia-revit-ia', 'memoria-calculo', 'pack-dynamo']) {
    for (const cual of ['gracias-agenda.html', 'ghl-gracias.html']) {
      const p = await b.newPage({ viewport: { width: 900, height: 900 } });
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto('file://' + REPO + d + '/' + cual + '?acceso=dm2026', { waitUntil: 'load' });
      await p.waitForTimeout(300);
      const r = await p.evaluate(() => {
        const g = document.getElementById('btnGuia');
        const c = document.getElementById('btnComunidad');
        return { guia: g ? g.getAttribute('href') : null,
                 com: c ? c.getAttribute('href') : null,
                 oculto: c ? c.hidden : null };
      });
      const guiaOk = r.guia && r.guia !== '#' && r.guia.startsWith('http');
      const comOk = r.oculto === false && r.com && r.com !== '#' && r.com.startsWith('http');
      const ok = guiaOk && comOk && !errs.length;
      console.log((d + '/' + cual).padEnd(38), ok ? 'OK' : 'MAL',
                  ' comunidad:', r.oculto ? 'oculta' : (r.com || '').slice(0, 46));
      if (!ok) { mal = true; if (errs.length) console.log('   errores:', errs); }
      await p.close();
    }
  }
  await b.close();
  console.log(mal ? '\nPRUEBA MAL' : '\nprueba OK');
  process.exit(mal ? 1 : 0);
})();
