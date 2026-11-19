// Renderiza las plantillas a PNG con el Chromium del entorno.
//   NODE_PATH=<carpeta con playwright-core>/node_modules node render.cjs portada-carrusel.html [historia.html …]
// Lee el tamaño del propio HTML (body); por defecto 1080×1350. Guarda <nombre>.png al lado.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
(async () => {
  const exe = fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-')).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`).find(fs.existsSync);
  const b = await chromium.launch({ executablePath: exe });
  for (const f of process.argv.slice(2)) {
    const alto = /historia/.test(f) ? 1920 : 1350;
    const p = await b.newPage({ viewport: { width: 1080, height: alto } });
    await p.goto('file://' + path.resolve(f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    const fuentes = await p.evaluate(() => [...new Set([...document.fonts].filter(x => x.status === 'loaded').map(x => x.family))]);
    const out = f.replace(/\.html$/, '.png');
    await p.screenshot({ path: out });
    console.log(out, '· fuentes cargadas:', fuentes.join(', '));
    await p.close();
  }
  await b.close();
})();
