/* Fotografía una landing y mide lo que se puede medir.
 *
 *   node .claude/skills/landing-craft/scripts/mirar.mjs <archivo.html | URL> [--out lab]
 *
 * Qué hace:
 *   · captura la página entera a 1200 px y a 390 px
 *   · recorre el scroll en seis posiciones en cada ancho
 *   · mide el contraste REAL de cada bloque de texto sobre LOS PÍXELES que tiene
 *     detrás, ya compuestos — no sobre lo que dice el CSS
 *   · lista enlaces que se quedaron en «#» o vacíos
 *   · avisa si el cuerpo se mueve en horizontal a 390 px
 *
 * Por qué mide píxeles y no el CSS: casi todos los heroes de DMA llevan un
 * degradado o una foto detrás. Leyendo el CSS, el fondo de un titular blanco
 * sobre un hero azul resuelve al blanco del <body> y sale 1:1, que es mentira.
 * Aquí se esconde el texto, se fotografía lo que hay debajo y se mide eso.
 *
 * Sale con código 1 si hay contraste por debajo del mínimo o enlaces muertos.
 * Lo que NO puede decirte está en references/verificacion.md: por eso el paso
 * siguiente es abrir las capturas y mirarlas.
 */
import playwright from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
const { chromium } = playwright;

const args = process.argv.slice(2);
const destino = args.find(a => !a.startsWith('--'));
const salida = (() => { const i = args.indexOf('--out'); return i >= 0 ? args[i + 1] : 'lab'; })();
if (!destino) { console.error('Uso: node mirar.mjs <archivo.html | URL> [--out lab]'); process.exit(2); }
const url = /^https?:\/\//.test(destino) ? destino : 'file://' + resolve(destino);

// Reúne los bloques de texto con su caja en coordenadas de página y su color.
const CANDIDATOS = () => {
  const rgb = s => (s.match(/\d+(\.\d+)?/g) || []).slice(0, 3).map(Number);
  const out = [];
  document.querySelectorAll('p,li,h1,h2,h3,h4,h5,h6,a,button,label,td,th,span').forEach((el, i) => {
    const txt = (el.innerText || '').trim();
    if (!txt) return;
    // solo hojas de texto: si tiene hijos con texto propio, se mide el hijo
    if ([...el.children].some(c => (c.innerText || '').trim())) return;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return;
    const st = getComputedStyle(el);
    if (st.visibility === 'hidden' || st.display === 'none' || +st.opacity === 0) return;
    const f = rgb(st.color);
    if (f.length < 3) return;
    const px = parseFloat(st.fontSize);
    // Fondo propio opaco (botones, chips, insignias): es fiable y se usa tal cual.
    // Esconder el elemento para fotografiar lo de debajo escondería TAMBIÉN su
    // propio fondo, y un botón naranja con texto blanco saldría 1:1, que es falso.
    // Solo cuenta como fondo propio si es OPACO. Un rgba(255,255,255,.2) deja ver
    // lo de detrás, y tomarlo por blanco daba 1:1 en cualquier insignia translúcida
    // sobre un fondo de color: texto blanco contra «blanco» que no existe.
    const cb = st.backgroundColor || '';
    const alfa = (cb.match(/rgba?\([^)]*?([\d.]+)\s*\)/) || [])[1];
    const opaco = cb && !/transparent/.test(cb) && (alfa === undefined || parseFloat(alfa) >= 0.95);
    const propio = opaco ? rgb(cb) : null;
    if (!propio) el.setAttribute('data-mirar', String(i));
    out.push({
      id: String(i), txt: txt.replace(/\s+/g, ' ').slice(0, 58), fg: f, propio,
      px: Math.round(px), grande: px >= 24 || (px >= 18.66 && +st.fontWeight >= 700),
      box: { x: Math.round(r.x + scrollX), y: Math.round(r.y + scrollY),
             w: Math.round(r.width), h: Math.round(r.height) },
    });
  });
  return out;
};

const lum = ([r, g, b]) => {
  const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};

// Media de color de cada caja sobre el PNG ya tomado. PIL está disponible.
function fondosReales(png, cajas) {
  const py = `
import json,sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
W,H = im.size
out = []
for c in json.load(sys.stdin):
    x,y,w,h = c["x"],c["y"],c["w"],c["h"]
    x2,y2 = min(x+w,W), min(y+h,H); x,y = max(x,0), max(y,0)
    if x2<=x or y2<=y: out.append(None); continue
    d = im.crop((x,y,x2,y2)).tobytes()
    n = len(d)//3
    out.append([sum(d[k] for k in range(i,len(d),3))//n for i in range(3)])
print(json.dumps(out))`;
  const r = execFileSync('python3', ['-c', py, png], { input: JSON.stringify(cajas), encoding: 'utf8' });
  return JSON.parse(r);
}

// Fotografía sin dejar caer la corrida. Si no puede, lo dice y cuenta como fallo:
// una captura que no se pudo tomar no es una página verificada.
async function foto(pag, opts) {
  try { await pag.screenshot({ timeout: 15000, ...opts }); return true; }
  catch (e) {
    console.log(`  ✖ no se pudo fotografiar (${opts.path.split('/').pop()}): ${e.name}`);
    return false;
  }
}

const anchos = [
  { w: 1200, h: 900, nombre: 'escritorio' },
  { w: 390, h: 844, nombre: 'movil' },
];

let fallo = false;
const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

for (const { w, h, nombre } of anchos) {
  const dir = `${salida}/${nombre}`;
  mkdirSync(dir, { recursive: true });
  // escala 1 para que las coordenadas del DOM y los píxeles del PNG coincidan
  const pag = await nav.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const errs = [];
  pag.on('pageerror', e => errs.push(e.message));
  // Sin red externa salvo que se pida: una fuente o un CDN que cuelga deja la
  // captura esperando para siempre. Con --con-red se deja pasar todo.
  if (!args.includes('--con-red')) {
    const propio = url.startsWith('file://') ? null : new URL(url).host;
    await pag.route('**', r => {
      const u = r.request().url();
      if (u.startsWith('data:') || u.startsWith('file://')) return r.continue();
      if (propio && new URL(u).host === propio) return r.continue();
      return r.abort();
    });
  }
  await pag.goto(url, { waitUntil: 'domcontentloaded' });
  await pag.waitForTimeout(1200);

  console.log(`\n━━ ${nombre} · ${w}px ━━`);
  console.log('  errores JS:', errs.length ? errs.join(' | ') : 'ninguno');

  const desborda = await pag.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (desborda > 2) {
    console.log(`  ⚠ DESBORDA ${desborda}px a lo ancho`);
    if (nombre === 'movil') fallo = true;
  } else console.log('  ancho: sin desbordamiento');

  // ── contraste sobre píxeles ────────────────────────────────────────────────
  const cand = await pag.evaluate(CANDIDATOS);
  const limpio = `${dir}/_sin-texto.png`;
  await pag.evaluate(() => {
    document.querySelectorAll('[data-mirar]').forEach(e => { e.style.visibility = 'hidden'; });
  });
  await pag.waitForTimeout(200);
  const fotografiado = await foto(pag, { path: limpio, fullPage: true });
  if (!fotografiado) fallo = true;
  await pag.evaluate(() => {
    document.querySelectorAll('[data-mirar]').forEach(e => { e.style.visibility = ''; });
  });

  const fondos = fondosReales(limpio, cand.map(c => c.box));
  const bajos = [];
  cand.forEach((c, i) => {
    const bg = c.propio || fondos[i];
    if (!bg) return;
    const L1 = lum(c.fg), L2 = lum(bg);
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const min = c.grande ? 3 : 4.5;
    if (ratio < min) bajos.push({ ...c, ratio: +ratio.toFixed(2), min, bg });
  });

  if (bajos.length) {
    fallo = true;
    console.log(`  ✖ contraste por debajo del mínimo en ${bajos.length} bloques:`);
    bajos.slice(0, 10).forEach(b =>
      console.log(`      ${b.ratio}:1 (mín ${b.min}) ${b.px}px — «${b.txt}»`));
    if (bajos.length > 10) console.log(`      … y ${bajos.length - 10} más`);
  } else {
    console.log(`  contraste: ${cand.length} bloques medidos sobre píxeles, todos por encima del mínimo`);
  }

  // ── capturas del recorrido ─────────────────────────────────────────────────
  const alto = await pag.evaluate(() => document.body.scrollHeight);
  for (let i = 0; i < 6; i++) {
    await pag.evaluate(y => window.scrollTo(0, y), Math.round(Math.max(0, alto - h) * (i / 5)));
    await pag.waitForTimeout(350);
    if (!await foto(pag, { path: `${dir}/${String(i).padStart(2, '0')}.png` })) fallo = true;
  }
  await pag.evaluate(() => window.scrollTo(0, 0));
  await pag.waitForTimeout(300);
  if (!await foto(pag, { path: `${dir}/completa.png`, fullPage: true })) fallo = true;

  if (nombre === 'escritorio') {
    const muertos = await pag.evaluate(() => {
      const m = [];
      document.querySelectorAll('a').forEach(a => {
        const href = (a.getAttribute('href') || '').trim();
        if (!href || href === '#')
          m.push({ texto: (a.innerText || '').trim().slice(0, 40) || '(sin texto)', href: href || '(vacío)' });
      });
      return m;
    });
    if (muertos.length) {
      fallo = true;
      console.log(`  ✖ ${muertos.length} enlaces sin destino:`);
      muertos.slice(0, 8).forEach(m => console.log(`      «${m.texto}» → ${m.href}`));
    } else console.log('  enlaces: todos con destino');
  }
  await pag.close();
}

await nav.close();
console.log(`\nCapturas en ${salida}/. Ahora ábrelas y míralas: el script dice que cargó,`);
console.log('no dice si se entiende. Ver references/verificacion.md.');
process.exit(fallo ? 1 : 0);
