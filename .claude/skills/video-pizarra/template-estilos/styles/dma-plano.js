// DMA · Plano — la marca de Design Modeling Academy: navy con cuadrícula de plano, pórtico en línea fina,
// Overpass pesada para titulares, Nunito para el texto y un solo acento ámbar. Sale de «minimal».
import * as L from '../engine/lib.js';
import { BASE, title, para, drawFrame } from '../engine/base.js';

const BG = '#0E2438', INK = '#FFFFFF', MUTED = '#AAB8C8', DIM = '#7F93A8', LINE = 'rgba(255,255,255,.10)', GRID = 'rgba(255,255,255,.045)';
const ACC = '#E8A04A', BLUE = '#003E5C';
const SLOW = t => 1 - Math.pow(1 - t, 4);
const LOGO = await L.loadImg('assets/logo-dma.png').catch(() => null);

// pórtico de la tarjeta del tutor: dos vanos, diagonales, zapatas y un nudo ámbar. Se dibuja con el progreso p.
function portico(K, x, y, w, h, p, alpha = 1) {
  const { ctx, u } = K; if (p <= 0) return;
  const segs = [
    [0, 0, 0, 1], [0.5, 0, 0.5, 1], [1, 0, 1, 1],          // columnas
    [0, 0, 1, 0], [0, 0.45, 1, 0.45],                      // vigas
    [0, 0.45, 0.5, 0], [0.5, 1, 1, 0.45],                  // diagonales
  ];
  ctx.save(); ctx.globalAlpha = 0.55 * alpha; ctx.strokeStyle = '#4A6582'; ctx.lineWidth = 2.2 * u; ctx.lineCap = 'round';
  segs.forEach((sg, i) => {
    const q = L.clamp(p * segs.length - i); if (q <= 0) return; const e = SLOW(q);
    ctx.beginPath(); ctx.moveTo(x + sg[0] * w, y + sg[1] * h); ctx.lineTo(x + (sg[0] + (sg[2] - sg[0]) * e) * w, y + (sg[1] + (sg[3] - sg[1]) * e) * h); ctx.stroke();
  });
  const fp = L.clamp(p * 1.4 - 0.4);
  for (const fx of [0, 0.5, 1]) { ctx.globalAlpha = 0.55 * alpha * fp; ctx.strokeRect(x + fx * w - 26 * u, y + h, 52 * u, 22 * u); }
  ctx.setLineDash([10 * u, 10 * u]); ctx.beginPath(); ctx.moveTo(x - 60 * u, y + h + 36 * u); ctx.lineTo(x + (w + 120 * u) * fp - 60 * u, y + h + 36 * u); ctx.stroke(); ctx.setLineDash([]);
  const np = L.clamp(p * 1.6 - 0.9); if (np > 0) { ctx.globalAlpha = alpha; ctx.strokeStyle = ACC; ctx.lineWidth = 3.2 * u; ctx.beginPath(); ctx.arc(x + 0.5 * w, y + 0.45 * h, 13 * u * SLOW(np), 0, 7); ctx.stroke(); }
  ctx.restore();
}

export default {
  id: 'dma-plano', name: 'DMA · Plano',
  // Overpass y Nunito van en local (fonts/marca.css): el Chromium del render no llega a Google Fonts.
  fontLoads: ['900 60px Overpass', '700 60px Overpass', '400 30px Nunito', '700 30px Nunito'],
  palette: { bg: BG, ink: INK, accent: ACC, muted: MUTED, panel: '#13304B', line: LINE, good: INK, bad: DIM, mascot: ACC },
  type: { display: s => `900 ${s}px Overpass`, em: s => `900 ${s}px Overpass`, body: s => `400 ${s}px Nunito`, bodyEm: s => `700 ${s}px Nunito`, label: s => `700 ${s}px Nunito`, mono: s => `700 ${s}px Nunito`, thin: s => `900 ${s}px Overpass`, semi: s => `700 ${s}px Overpass` },
  ls: -0.02, lh: 1.02,
  sfx: 'soft', transDur: 0.6, push: 0.015,
  music: 'modern corporate electronic, confident, clean plucks and soft pads, steady pulse, 104 BPM, instrumental, engineering tech brand',
  background(K, s) {
    const { ctx, W, H, u } = K; ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
    // cuadrícula de plano: fina cada 60 px, un poco más marcada cada 300 px
    const g = 60 * u; ctx.fillStyle = GRID;
    for (let x = (W % g) / 2; x < W; x += g) ctx.fillRect(Math.round(x), 0, 1, H);
    for (let y = 0; y < H; y += g) ctx.fillRect(0, Math.round(y), W, 1);
    // viñeta suave hacia los bordes
    const vg = ctx.createRadialGradient(W / 2, H * 0.45, H * 0.2, W / 2, H * 0.5, H * 0.8); vg.addColorStop(0, 'rgba(14,36,56,0)'); vg.addColorStop(1, 'rgba(6,18,30,.55)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
    // pórtico en las escenas que tienen aire abajo
    if (s.type === 'hook') portico(K, W * 0.16, H * 0.56, W * 0.68, H * 0.2, L.clamp((s.t - 0.4) / 1.6));
    if (s.type === 'cta') portico(K, W * 0.1, H * 0.6, W * 0.46, H * 0.15, L.clamp((s.t - 0.2) / 1.2), 0.8);
    // logo DMA abajo al centro
    if (LOGO && K.spec.chrome !== false) { const lw = 330 * u, lh = lw * LOGO.height / LOGO.width; ctx.save(); ctx.globalAlpha = 0.95; ctx.drawImage(LOGO, (W - lw) / 2, H - lh - 70 * u, lw, lh); ctx.restore(); }
  },
  headline(K, str, box, p, s, o = {}) {
    const top = (K.vertical ? 110 : 90) * K.u; if (box.y < top) box = { ...box, y: top, h: box.h - (top - box.y) };
    title(K, str, box, SLOW(p), { align: o.align, size: o.size, color: INK, emColor: ACC, reveal: 'rise', valign: 'middle', max: o.size === 'm' ? 104 : 150 });
  },
  text(K, str, box, p, role, s, o = {}) {
    const top = (K.vertical ? 110 : 90) * K.u; if (box.y < top) box = { ...box, y: top, h: box.h - (top - box.y) };
    if (role === 'kicker' || role === 'label') return para(K, str, box, p, { font: sz => K.S.type.label(sz), color: role === 'kicker' ? ACC : MUTED, upper: role === 'kicker', ls: role === 'kicker' ? 0.14 : 0, max: role === 'kicker' ? 30 : 30, align: o.align || 'left' });
    if (role === 'headBad' || role === 'headGood') return title(K, str, box, p, { color: role === 'headGood' ? INK : DIM, max: 60, reveal: 'rise', font: sz => K.S.type.semi(sz) });
    return BASE.text(K, str, box, p, role, s, { color: role === 'bad' ? DIM : role === 'body' ? MUTED : INK, font: role === 'item' || role === 'step' ? (sz => K.S.type.semi(sz)) : role === 'body' ? (sz => K.S.type.body(sz)) : undefined, max: role === 'item' ? 58 : role === 'step' ? 46 : 42, ...o });
  },
  panel(K, b, p, s, kind) {
    if (p <= 0) return; const { ctx, u } = K, e = SLOW(p);
    if (kind === 'row') { ctx.fillStyle = LINE; ctx.fillRect(b.x, b.y + b.h, b.w * e, 1.5 * u); return; }
    ctx.save(); ctx.globalAlpha = L.clamp(p * 1.5); ctx.translate(0, (1 - e) * 16 * u);
    L.rrect(ctx, b.x, b.y, b.w, b.h, 22 * u); ctx.fillStyle = '#13304B'; ctx.fill(); ctx.strokeStyle = LINE; ctx.lineWidth = 1.5 * u; ctx.stroke();
    ctx.fillStyle = ACC; ctx.fillRect(b.x, b.y + 18 * u, 5 * u, b.h - 36 * u);
    ctx.restore();
  },
  bullet(K, i, b, p) { if (p <= 0) return; para(K, String(i + 1).padStart(2, '0'), b, SLOW(p), { font: sz => K.S.type.display(sz), color: ACC, max: b.h * 0.42 / K.u, align: 'center' }); },
  number(K, str, box, p, s, o) { title(K, str, box, SLOW(p), { align: 'center', color: o?.small ? ACC : INK, emColor: ACC, reveal: 'rise', max: o?.small ? 110 : 300, font: sz => K.S.type.thin(sz), ls: -0.03 }); },
  quote(K, str, box, p) { title(K, '“' + str + '”', box, p, { size: 'm', max: 90, color: INK, reveal: 'words', font: sz => K.S.type.semi(sz), lh: 1.08 }); },
  portrait: BASE.portrait,
  mascot(K, box, p, s, mood) {
    if (p <= 0) return; const { ctx, u } = K; ctx.save(); ctx.globalAlpha = L.clamp(p * 1.6); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 30 * u; ctx.shadowOffsetY = 12 * u;
    L.mascot(ctx, K.spec.mascot, { ...box, y: box.y + (1 - SLOW(p)) * 20 * u }, { color: K.spec.mascotColor || ACC, outline: false, eye: BG, eyeStyle: mood === 'happy' ? 'happy' : 'dot', bob: Math.sin(K.t * 1.8) * 3 * u });
    ctx.restore();
  },
  media(K, img, box, p, s, frame) { drawFrame(K, img, box, SLOW(p), frame, { bezel: '#0A1A2A', shadowColor: 'rgba(0,0,0,.45)', barColor: '#E9EEF3', stroke: 'rgba(232,160,74,.0)' }); },
  prompt(K, str, box, p, s, tp) {
    if (p <= 0) return; const { ctx, u } = K, e = SLOW(p);
    ctx.save(); ctx.globalAlpha = L.clamp(p * 1.5); L.rrect(ctx, box.x, box.y - 6 * u, box.w, box.h + 12 * u, 20 * u); ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.restore();
    ctx.fillStyle = ACC; ctx.fillRect(box.x + 28 * u, box.y + box.h + 6 * u - 5 * u, (box.w - 56 * u) * e, 5 * u);
    para(K, str.slice(0, Math.ceil(str.length * tp)) + (tp < 1 || (K.frame >> 3) % 2 ? '|' : ''), { x: box.x + 30 * u, y: box.y, w: box.w - 60 * u, h: box.h }, 1, { font: sz => K.S.type.bodyEm(sz), color: BG, max: 46, valign: 'middle' });
  },
  caption(K, words, act, box, p) {
    const { ctx, u } = K; ctx.save(); ctx.globalAlpha = p; ctx.font = K.S.type.bodyEm(32 * u);
    const w = ctx.measureText(words.join(' ')).width; let cx = box.x + (box.w - w) / 2;
    ctx.fillStyle = 'rgba(6,18,30,.8)'; L.rrect(ctx, cx - 24 * u, box.y + box.h * 0.1, w + 48 * u, box.h * 0.8, 10 * u); ctx.fill();
    words.forEach((wd, i) => { ctx.fillStyle = i === act ? ACC : i < act ? INK : DIM; ctx.fillText(wd, cx, box.y + box.h * 0.63); cx += ctx.measureText(wd + ' ').width; });
    ctx.restore();
  },
  connector(K, a, b, p) { if (p <= 0) return; const ctx = K.ctx; ctx.save(); ctx.strokeStyle = 'rgba(232,160,74,.45)'; ctx.lineWidth = 2 * K.u; ctx.beginPath(); ctx.moveTo(...a); const e = SLOW(p); ctx.lineTo(a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e); ctx.stroke(); ctx.restore(); },
  button(K, str, b, p) {
    if (p <= 0) return; const { ctx, u } = K, e = SLOW(p); ctx.save(); ctx.globalAlpha = L.clamp(p * 1.5);
    L.rrect(ctx, b.x, b.y, b.w, b.h, b.h / 2); ctx.fillStyle = ACC; ctx.fill(); ctx.restore();
    para(K, str, L.inset(b, b.h * 0.4, b.h * 0.22), e, { font: sz => K.S.type.label(sz), color: BG, max: 34, align: 'center' });
  },
  transition(K, A, B, p, info) { // la escena nueva entra desde abajo, como una lámina que se desliza sobre el plano
    const { ctx, W, H, u } = K, r = SLOW(info.raw);
    ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
    ctx.save(); ctx.globalAlpha = 1 - L.clamp(info.raw * 1.4); ctx.drawImage(A, 0, -80 * u * r); ctx.restore();
    ctx.save(); ctx.globalAlpha = L.clamp(info.raw * 1.6 - 0.2); ctx.drawImage(B, 0, 120 * u * (1 - r)); ctx.restore();
    ctx.fillStyle = ACC; ctx.fillRect(0, H * (1 - r) - 3 * u, W * (info.raw < 0.95 ? 1 : 0), 4 * u);
  },
};
