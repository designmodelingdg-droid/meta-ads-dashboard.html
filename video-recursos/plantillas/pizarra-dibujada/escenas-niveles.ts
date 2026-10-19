import { AMBER, El, INK, NAVY, Pt, Scene } from "./draw";
import T from "./timing.json";

// Simbología de niveles en planos · estilo 9 (pizarra dibujada) con las letras de marca:
// Anton para títulos y códigos, Overpass 800 para etiquetas.
type Tm = { start: number; dur: number };
const S = T.scenes as Tm[];
const COBRE = "#C8721E";
const GRIS = "#4A5F73";

const fit = (sc: Scene, tm: Tm, frac = 0.9) => {
  const used = sc.cur - tm.start;
  const room = tm.dur * frac;
  if (used <= room) return sc.els;
  const f = room / used;
  for (const e of sc.els) {
    e.t0 = tm.start + (e.t0 - tm.start) * f;
    if (e.k !== "fill") e.dur *= f;
  }
  return sc.els;
};

const circle = (cx: number, cy: number, r: number, a0 = -Math.PI, a1 = Math.PI, n = 40): Pt[] => {
  const pts: Pt[] = [];
  for (let i = 0; i <= n; i++) {
    const a = a0 + ((a1 - a0) * i) / n;
    pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
  }
  return pts;
};
const sector = (cx: number, cy: number, r: number, a0: number, a1: number): Pt[] => [[cx, cy], ...circle(cx, cy, r, a0, a1, 16)];
const rect = (x0: number, y0: number, x1: number, y1: number): Pt[] => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];

// símbolo de nivel: círculo con dos cuadrantes rellenos + línea de nivel
const simbolo = (sc: Scene, cx: number, cy: number, r: number, lineTo: number, w = 6) => {
  sc.stroke([[cx - r - 26, cy], [lineTo, cy]], INK, w, { wob: 0.8 });
  sc.stroke([[cx, cy - r - 26], [cx, cy + r + 26]], INK, w, { wob: 0.8 });
  sc.stroke(circle(cx, cy, r), INK, w, { wob: 0.6 });
  sc.fill(sector(cx, cy, r, Math.PI, 1.5 * Math.PI), NAVY);
  sc.fill(sector(cx, cy, r, 0, 0.5 * Math.PI), NAVY);
  sc.wait(0.12);
};

// línea de nivel discontinua (aparece de golpe, como un sello)
const discontinua = (sc: Scene, x0: number, x1: number, y: number, color = COBRE) => {
  for (let x = x0; x < x1; x += 34) sc.fill(rect(x, y - 2.5, Math.min(x + 20, x1), y + 2.5), color);
};

// ---------- Corte de capas (de abajo arriba) ----------
const X0 = 140;
const X1 = 940;
type Capa = { code: string; top: number; bot: number };
const CAPAS: Capa[] = [
  { code: "NTN", top: 1270, bot: 1450 },
  { code: "NR", top: 1170, bot: 1270 },
  { code: "NFP", top: 1100, bot: 1170 },
  { code: "NCP", top: 1060, bot: 1100 },
  { code: "NPT", top: 1030, bot: 1060 },
];
// dibuja las capas hasta la k (incluida); las anteriores van rápido
const corte = (sc: Scene, k: number, rapidoHasta: number) => {
  for (let i = 0; i <= k; i++) {
    const c = CAPAS[i];
    const fast = i < rapidoHasta;
    const sp = sc.speed;
    if (fast) sc.speed = 9;
    if (i === 0) {
      // terreno natural: borde irregular + matas de hierba
      const top: Pt[] = [];
      for (let x = X0; x <= X1; x += 40) top.push([x, c.top + Math.sin(x * 0.05) * 7]);
      sc.fill([...top, [X1, c.bot], [X0, c.bot]], "#F2D2AE");
      sc.stroke(top, INK, 5, { wob: 1.2 });
      sc.hatch(X0 + 20, X1, c.top + 22, 26, 30, "#D78631", 3);
      if (!fast) [200, 330, 470, 640, 790, 900].forEach((x) => sc.stroke([[x - 14, c.top - 4], [x - 6, c.top - 30], [x, c.top - 6], [x + 8, c.top - 34], [x + 14, c.top - 4]], NAVY, 3.5, { wob: 0.4, gap: 0.01 }));
    } else {
      const col = i === 1 ? "#F7E2C8" : i === 2 ? "#D9E2EA" : i === 3 ? "#C3D0DC" : "#2E6A8E";
      sc.fill(rect(X0, c.top, X1, c.bot), col);
      sc.stroke([[X0, c.top], [X1, c.top]], INK, 5, { wob: 1 });
      if (i === 1) for (let x = X0 + 18; x < X1; x += 38) for (let y = c.top + 18; y < c.bot - 8; y += 30) sc.fill(circle(x + ((y / 30) % 2) * 16, y, 4, -Math.PI, Math.PI, 8), "#D78631");
      if (i === 2) for (let x = X0 + 24; x < X1; x += 46) sc.fill(circle(x, (c.top + c.bot) / 2 + ((x / 46) % 2) * 10 - 5, 5, -Math.PI, Math.PI, 8), "#7F93A6");
      if (i === 4) for (let x = X0; x <= X1; x += 100) sc.fill(rect(x, c.top, x + 3, c.bot), "#9FC0D6");
    }
    sc.stroke([[X0, c.top], [X0, c.bot]], INK, 4, { wob: 0.4, gap: 0.01 });
    sc.stroke([[X1, c.top], [X1, c.bot]], INK, 4, { wob: 0.4, gap: 0.01 });
    sc.speed = sp;
  }
};
// marca el nivel de la capa k: línea discontinua cobre + mini símbolo y código a la derecha
const marcaNivel = (sc: Scene, k: number) => {
  const y = CAPAS[k].top;
  discontinua(sc, X0 - 40, X1 + 30, y);
  sc.fill(sector(990, y - 34, 22, Math.PI, 1.5 * Math.PI), COBRE);
  sc.fill(sector(990, y - 34, 22, 0, 0.5 * Math.PI), COBRE);
  sc.stroke(circle(990, y - 34, 22, -Math.PI, Math.PI, 20), COBRE, 4, { wob: 0.2, gap: 0.02 });
};

// página de un nivel: código grande + etiqueta + corte
const pagina = (id: number, tm: Tm, n: string, code: string, label: string, k: number) => {
  const sc = new Scene(id, tm.start + 0.05, 1.9);
  sc.text(540, 205, `SIMBOLOGÍA DE NIVELES · ${n}`, 30, { font: "Overpass", color: GRIS, dur: 0.2 });
  simbolo(sc, 290, 560, 78, 960);
  sc.text(420, 640, code, 168, { anchor: "start", color: NAVY, dur: 0.35 });
  const lw = label.length * 40 * 0.66 + 60;
  sc.stroke([[540 - lw / 2, 720], [540 + lw / 2, 720], [540 + lw / 2, 800], [540 - lw / 2, 800], [540 - lw / 2, 720]], INK, 4, { wob: 1.2 });
  sc.text(540, 778, label, 40, { font: "Overpass", color: NAVY, dur: 0.4 });
  corte(sc, k, k);
  marcaNivel(sc, k);
  return fit(sc, tm);
};

// ---------- 0 · Portada (ya dibujada en el fotograma 0) ----------
const portada = (tm: Tm) => {
  const pre = new Scene(0, -8, 4);
  pre.text(540, 380, "SIMBOLOGÍA", 172, { color: NAVY });
  pre.text(540, 560, "DE NIVELES", 172, { color: NAVY });
  pre.text(540, 700, "EN PLANOS", 112, { color: "#D78631" });
  pre.stroke([[230, 655], [300, 655]], "#D78631", 7, { wob: 0.5 });
  pre.stroke([[780, 655], [850, 655]], "#D78631", 7, { wob: 0.5 });
  simbolo(pre, 300, 1080, 150, 520, 9);
  const codes = ["N±0.00", "NPT", "NCP", "NFP", "NR", "NTN"];
  codes.forEach((c, i) => {
    const y = 905 + i * 72;
    pre.text(600, y, c, 64, { anchor: "start", color: i === 0 ? "#D78631" : NAVY });
  });
  const sc = new Scene(0, tm.start + 0.35, 1.2);
  sc.text(540, 1460, "y qué significa cada una", 50, { font: "Overpass", color: COBRE });
  return [...pre.els, ...fit(sc, tm, 0.95)];
};

// ---------- 1 · N±0.00 ----------
const cero = (tm: Tm) => {
  const sc = new Scene(1, tm.start + 0.05, 1.6);
  sc.text(540, 205, "SIMBOLOGÍA DE NIVELES · 1 DE 6", 30, { font: "Overpass", color: GRIS, dur: 0.2 });
  simbolo(sc, 290, 560, 78, 960);
  sc.text(420, 640, "N±0.00", 150, { anchor: "start", color: "#D78631", dur: 0.35 });
  sc.stroke([[300, 720], [780, 720], [780, 800], [300, 800], [300, 720]], INK, 4, { wob: 1.2 });
  sc.text(540, 778, "NIVEL CERO DE REFERENCIA", 40, { font: "Overpass", color: NAVY, dur: 0.4 });
  // línea cero con alturas hacia arriba (+) y hacia abajo (−)
  sc.stroke([[X0, 1200], [X1, 1200]], INK, 6, { wob: 1 });
  discontinua(sc, X0, X1, 1200);
  sc.arrow([400, 1190], [400, 990], COBRE, 6, 24);
  sc.text(450, 1080, "+  ARRIBA", 46, { anchor: "start", font: "Overpass", color: NAVY, dur: 0.3 });
  sc.arrow([680, 1210], [680, 1410], COBRE, 6, 24);
  sc.text(730, 1330, "−  ABAJO", 46, { anchor: "start", font: "Overpass", color: NAVY, dur: 0.3 });
  sc.text(200, 1260, "±0.00", 54, { anchor: "start", color: "#D78631", dur: 0.25 });
  return fit(sc, tm);
};

// ---------- 7 · Resumen + CTA ----------
const cta = (tm: Tm) => {
  const sc = new Scene(7, tm.start + 0.05, 1.4);
  sc.text(540, 245, "COMENTA", 120, { color: NAVY, dur: 0.3 });
  sc.text(540, 500, "NIVEL", 190, { color: "#FFFFFF", bg: "#D78631", dur: 0.4 });
  sc.text(540, 630, "y te llega gratis nuestro", 44, { font: "Overpass", color: NAVY, dur: 0.3 });
  sc.text(540, 700, "test de nivel BIM", 52, { font: "Overpass", color: COBRE, dur: 0.3 });
  corte(sc, 4, 5);
  CAPAS.forEach((c, i) => {
    discontinua(sc, X1 - 120, X1 + 10, c.top, i === 4 ? COBRE : GRIS);
  });
  sc.text(160, 990, "NPT · NCP · NFP · NR · NTN", 40, { anchor: "start", color: NAVY, dur: 0.35 });
  return fit(sc, tm);
};

export const ELS: El[] = [
  ...portada(S[0]),
  ...cero(S[1]),
  ...pagina(2, S[2], "2 DE 6", "NTN", "NIVEL DE TERRENO NATURAL", 0),
  ...pagina(3, S[3], "3 DE 6", "NR", "NIVEL DE RELLENO", 1),
  ...pagina(4, S[4], "4 DE 6", "NFP", "NIVEL DE FALSO PISO", 2),
  ...pagina(5, S[5], "5 DE 6", "NCP", "NIVEL DE CONTRAPISO", 3),
  ...pagina(6, S[6], "6 DE 6", "NPT", "NIVEL DE PISO TERMINADO", 4),
  ...cta(S[7]),
];
export const PAGE_OF = [0, 1, 2, 3, 4, 5, 6, 7];
export const PAGE_START = [0, ...S.slice(1).map((s) => s.start - 0.15)];
export const TOTAL = S[7].start + S[7].dur + 0.8;
void AMBER;
