/* Creativos estáticos de la pauta de octubre (4:5 y 9:16), dibujados por código.
 *
 *   node scripts/creativos_octubre.mjs
 *     → matriz-viral/entregables/pauta-octubre/<id>-4x5.png  (1080×1350)
 *     → matriz-viral/entregables/pauta-octubre/<id>-9x16.png (1080×1920)
 *
 * Solo los anuncios cuyo creativo es un dibujo en línea (la marca DMA sobre
 * navy): ACERO A (naves) y MÁSTER A, B y C. Los demás piden material REAL
 * (foto de obra, pantallazo del tutor, reel recortado o los ganadores vigentes)
 * y no se inventan aquí.
 *
 * El texto de la imagen es corto a propósito: el copy completo va en el texto
 * principal del anuncio (guiones-completos.json). Nada de precio del Máster;
 * ACERO tampoco lleva precio en la imagen.
 *
 * En 9:16 el texto se queda dentro de la zona segura (250 px arriba y abajo).
 */
import playwright from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const RAIZ = resolve(new URL('..', import.meta.url).pathname);
const SAL = resolve(RAIZ, 'matriz-viral/entregables/pauta-octubre');
mkdirSync(SAL, { recursive: true });
const b64 = f => readFileSync(resolve(RAIZ, f)).toString('base64');
const LOGO = `data:image/png;base64,${b64('video-tutor-ia/marca/logo-dma-claro.png')}`;
const F = 'video-tutor-ia/fuentes/';
const FUENTES = `
@font-face{font-family:Overpass;font-weight:900;src:url(data:font/woff2;base64,${b64(F + 'qFdH35WCmI96Ajtm81GlU9s.woff2')}) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+2260}
@font-face{font-family:Overpass;font-weight:900;src:url(data:font/woff2;base64,${b64(F + 'qFdH35WCmI96Ajtm81GrU9vyww.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F}
@font-face{font-family:Overpass;font-weight:700;src:url(data:font/woff2;base64,${b64(F + 'qFdH35WCmI96Ajtm81GlU9s.woff2')}) format('woff2')}
@font-face{font-family:Nunito;font-weight:700;src:url(data:font/woff2;base64,${b64(F + 'XRXV3I6Li01BKofINeaB.woff2')}) format('woff2')}`;

const NAVY = '#0E2438', AMBAR = '#E8A04A', TINTA = '#EAF1F7', ROJO = '#E0634F';

/* ── dibujos en línea (viewBox 900×560) ── */
const nave = `
<svg viewBox="40 90 820 420" fill="none" stroke="${TINTA}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <g opacity=".9">
    <path d="M110 470 V250 L450 120 L790 250 V470"/>
    <path d="M110 250 H790" stroke-dasharray="10 10" opacity=".5"/>
    ${[190, 270, 350, 450, 550, 630, 710].map(x => `<path d="M${x} 470 V${x < 450 ? 250 - (x - 110) * 130 / 340 + 130 * 0 : 250 - (790 - x) * 130 / 340 + 0}" opacity=".35"/>`).join('')}
    <path d="M60 470 H840" stroke-width="4"/>
    ${[110, 790].map(x => `<path d="M${x - 22} 470 h44 v14 h-44z"/>`).join('')}
  </g>
  <g transform="rotate(-9 330 330)">
    <rect x="135" y="285" width="390" height="92" rx="10" stroke="${ROJO}" stroke-width="7"/>
    <text x="330" y="348" text-anchor="middle" fill="${ROJO}" stroke="none" font-family="Overpass" font-weight="900" font-size="46" letter-spacing="3">RECHAZADO</text>
    <path d="M120 335 H540" stroke="${TINTA}" stroke-width="8"/>
  </g>
  <g transform="rotate(-6 620 400)">
    <rect x="425" y="358" width="390" height="92" rx="10" stroke="${AMBAR}" stroke-width="7" fill="${NAVY}"/>
    <text x="620" y="421" text-anchor="middle" fill="${AMBAR}" stroke="none" font-family="Overpass" font-weight="900" font-size="46" letter-spacing="3">CALCULADO</text>
  </g>
</svg>`;

const capas = `
<svg viewBox="0 0 900 560" fill="none" stroke-linecap="round" stroke-linejoin="round" font-family="Overpass" font-weight="700">
  ${[0, 1, 2, 3].map(i => {
    const y = 400 - i * 92, c = i === 0 ? TINTA : AMBAR, op = i === 0 ? 1 : .55 + i * .15;
    const lab = ['Modelo en Revit', '+ Estructura', '+ Instalaciones', '+ Coordinación'][i];
    return `<g opacity="${op}"><path d="M90 ${y} L290 ${y - 60} L490 ${y} L290 ${y + 60} Z" stroke="${c}" stroke-width="3" ${i === 0 ? '' : 'stroke-dasharray="12 8"'}/>
      <text x="540" y="${y + 10}" fill="${c}" stroke="none" font-size="36">${lab}</text></g>`;
  }).join('')}
  <path d="M90 400 V430 L290 490 L490 430 V400" stroke="${TINTA}" stroke-width="3"/>
</svg>`;

const bases = `
<svg viewBox="0 0 900 560" fill="none" stroke-linecap="round" stroke-linejoin="round" font-family="Overpass">
  <rect x="190" y="20" width="520" height="520" rx="8" stroke="${TINTA}" stroke-width="3"/>
  <text x="230" y="80" fill="${TINTA}" font-weight="900" font-size="30" letter-spacing="3">BASES DEL CONCURSO</text>
  ${[130, 180, 230, 280].map((y, i) => `<path d="M230 ${y} H${[650, 600, 640, 560][i]}" stroke="${TINTA}" stroke-width="3" opacity=".35"/>`).join('')}
  <rect x="215" y="320" width="470" height="70" rx="6" fill="${AMBAR}" opacity=".16" stroke="${AMBAR}" stroke-width="3"/>
  <text x="235" y="365" fill="${AMBAR}" font-weight="900" font-size="29">Requisito: certificación BIM</text>
  <path d="M728 320 l60 60 M788 320 l-60 60" stroke="${ROJO}" stroke-width="10"/>
  ${[430, 480].map((y, i) => `<path d="M230 ${y} H${[620, 520][i]}" stroke="${TINTA}" stroke-width="3" opacity=".35"/>`).join('')}
</svg>`;

const mapa = (() => {
  const origen = [330, 350];
  const destinos = [[140, 170], [520, 150], [700, 230], [780, 400], [600, 470]];
  const arco = ([x, y]) => { const mx = (origen[0] + x) / 2, my = Math.min(origen[1], y) - 110; return `M${origen[0]} ${origen[1]} Q${mx} ${my} ${x} ${y}`; };
  let puntos = '';
  for (let x = 40; x <= 860; x += 28) for (let y = 40; y <= 520; y += 28) {
    const dx = (x - 450) / 420, dy = (y - 280) / 250;
    if (dx * dx + dy * dy < 1 && ((x * 7 + y * 13) % 5) < 3) puntos += `<circle cx="${x}" cy="${y}" r="2.6" fill="${TINTA}" opacity=".28"/>`;
  }
  return `<svg viewBox="0 0 900 560" fill="none" stroke-linecap="round">
    ${puntos}
    ${destinos.map(d => `<path d="${arco(d)}" stroke="${AMBAR}" stroke-width="4" stroke-dasharray="2 12"/><circle cx="${d[0]}" cy="${d[1]}" r="11" fill="${AMBAR}"/>`).join('')}
    <circle cx="${origen[0]}" cy="${origen[1]}" r="20" fill="${TINTA}"/><circle cx="${origen[0]}" cy="${origen[1]}" r="36" stroke="${TINTA}" stroke-width="3" opacity=".5"/>
    <text x="${origen[0]}" y="${origen[1] + 80}" text-anchor="middle" fill="${TINTA}" font-family="Overpass" font-weight="700" font-size="28">Tu escritorio</text>
  </svg>`;
})();

const CREATIVOS = [
  { id: 'oct-ang-ads-acero-a-naves', eyebrow: 'Especialización en Acero', titulo: '¿Cuántas naves dijiste que <em>no</em>?',
    sub: 'Porque no sabías calcularlas.', dibujo: nave, pie: 'Cálculo y diseño en software: Revit, Robot y Advance Steel' },
  { id: 'oct-ang-ads-master-a-revit-no-es-bim', eyebrow: 'Máster BIM + IA', titulo: 'Revit <em>≠</em> BIM',
    sub: 'Sabes Revit. ¿Sabes coordinar un proyecto BIM?', dibujo: capas, pie: 'Del modelado a la coordinación, en 4 bloques' },
  { id: 'oct-ang-ads-master-b-concurso', eyebrow: 'Máster BIM + IA', titulo: 'Perdió el concurso <em>antes de presentarse</em>',
    sub: 'Pedían certificación BIM.', dibujo: bases, pie: 'Que no te deje fuera un requisito' },
  { id: 'oct-ang-ads-master-c-trabajar-afuera', eyebrow: 'Máster BIM + IA, 100 % online', titulo: 'Proyectos de afuera, <em>sin irte de tu país</em>',
    sub: 'BIM y coordinación para equipos que trabajan en remoto.', dibujo: mapa, pie: 'Trabaja para afuera desde tu país' },
];

const pagina = (c, alto) => `<!doctype html><html><head><meta charset="utf-8"><style>
${FUENTES}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;height:${alto}px;background:${NAVY};overflow:hidden}
body{font-family:Nunito,sans-serif;color:${TINTA};display:flex;flex-direction:column;
  padding:${alto > 1500 ? '270px 84px 270px' : '84px 84px 72px'};position:relative}
body::before{content:"";position:absolute;inset:0;background-image:linear-gradient(${TINTA}0d 1px,transparent 1px),linear-gradient(90deg,${TINTA}0d 1px,transparent 1px);background-size:54px 54px}
.eyebrow{font:700 30px/1 Overpass,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:${AMBAR};position:relative}
h1{font:900 ${alto > 1500 ? 96 : 88}px/1.02 Overpass,sans-serif;margin-top:26px;letter-spacing:-.01em;position:relative;text-wrap:balance}
h1 em{font-style:normal;color:${AMBAR}}
.sub{font:700 36px/1.3 Nunito,sans-serif;margin-top:22px;color:#B9CBDA;position:relative}
.dib{flex:1;display:flex;align-items:center;justify-content:center;position:relative;min-height:0;padding:${alto > 1500 ? '40px 0' : '8px 0'}}
.dib svg{width:100%;max-height:100%}
.pie{display:flex;align-items:center;justify-content:space-between;gap:24px;border-top:3px solid ${AMBAR};padding-top:26px;position:relative}
.pie span{font:700 28px/1.3 Overpass,sans-serif;max-width:640px}
.pie img{height:92px}
</style></head><body>
<p class="eyebrow">${c.eyebrow}</p><h1>${c.titulo}</h1><p class="sub">${c.sub}</p>
<div class="dib">${c.dibujo}</div>
<div class="pie"><span>${c.pie}</span><img src="${LOGO}" alt=""></div>
</body></html>`;

const nav = await playwright.chromium.launch();
for (const c of CREATIVOS) {
  for (const [nombre, alto] of [['4x5', 1350], ['9x16', 1920]]) {
    const p = await nav.newPage({ viewport: { width: 1080, height: alto } });
    await p.setContent(pagina(c, alto), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const desborda = await p.evaluate(() => [...document.body.children].some(el => el.getBoundingClientRect().bottom > innerHeight + 1));
    const f = `${SAL}/${c.id}-${nombre}.png`;
    await p.screenshot({ path: f });
    console.log((desborda ? '⚠ DESBORDA ' : 'OK ') + f.replace(RAIZ + '/', ''));
    await p.close();
  }
}
await nav.close();
