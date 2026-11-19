import { AMBER, BLUE, BLUE_D, BLUE_L, El, INK, NAVY, Pt, RED, SOIL, SOIL_D, Scene, box, iso } from "./draw";
import T from "./timing.json";

// T.scenes[i] = { start, dur } en segundos (de la voz por escena); T.pages = inicio de cada página
type Tm = { start: number; dur: number };
const S = T.scenes as Tm[];

const CONC: [string, string, string] = ["#E8EEF3", "#C9D5DF", "#A7B9C8"];
const COLS: [string, string, string] = [BLUE_L, BLUE, BLUE_D];
const TIERRA: [string, string, string] = ["#F6DDBF", SOIL, SOIL_D];
const MURO: [string, string, string] = ["#DCE5EC", "#B3C6D4", "#8FA8BA"];

// comprime la escena para que termine al 90 % de su ventana
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

const titulo = (sc: Scene, n: string, txt: string) => {
  sc.text(540, 205, n, 34, { color: "#4A5F73", weight: 700, dur: 0.2 });
  sc.text(540, 300, txt, 84, { weight: 700, dur: 0.45 });
  const w = txt.length * 22;
  sc.underline(540 - w, 540 + w, 322);
};
const leader = (sc: Scene, a: Pt, b: Pt) => sc.stroke([a, b], INK, 3, { wob: 0.8, gap: 0.02 });

// ---------- 0 · Portada ----------
const portada = (tm: Tm) => {
  // PORTADA: ya dibujada en el fotograma 0 (es la que se usa de miniatura en redes)
  const pre = new Scene(0, -8, 4);
  pre.text(540, 330, "5 TIPOS DE", 112, { weight: 700 });
  pre.text(540, 470, "CIMENTACIÓN", 132, { weight: 700 });
  pre.underline(130, 950, 500);
  // aislada (izquierda)
  let P = iso(285, 980, 64);
  box(pre, P, -2, -2, -0.4, 4, 4, 0.4, TIERRA, 4);
  box(pre, P, -1, -1, 0, 2, 2, 0.6, CONC, 4.5);
  box(pre, P, -0.25, -0.25, 0.6, 0.5, 0.5, 3.2, COLS, 4.5);
  pre.arrow(P(0, 0, 4.7), P(0, 0, 3.9), "#C8721E", 5, 18);
  // combinada (derecha)
  P = iso(790, 980, 56);
  box(pre, P, -2.6, -1.6, -0.4, 5.2, 3.2, 0.4, TIERRA, 4);
  box(pre, P, -2.1, -0.8, 0, 4.2, 1.6, 0.5, CONC, 4.5);
  box(pre, P, -1.45, -0.22, 0.5, 0.44, 0.44, 3.2, COLS, 4.5);
  box(pre, P, 1.0, -0.22, 0.5, 0.44, 0.44, 3.2, COLS, 4.5);
  pre.arrow(P(-1.23, 0, 4.6), P(-1.23, 0, 3.8), "#C8721E", 5, 18);
  pre.arrow(P(1.22, 0, 4.6), P(1.22, 0, 3.8), "#C8721E", 5, 18);
  // pilotes (abajo, al centro)
  P = iso(540, 1290, 58);
  [-0.7, 0, 0.7].forEach((x) => box(pre, P, x - 0.15, 0.15, -4.2, 0.3, 0.3, 3.7, CONC, 4));
  box(pre, P, -1.1, -0.7, -0.5, 2.2, 1.4, 0.5, CONC, 4.5);
  box(pre, P, -0.22, -0.22, 0, 0.44, 0.44, 2.6, COLS, 4.5);
  pre.text(285, 1180, "Aislada", 46, { weight: 700 });
  pre.text(800, 1180, "Combinada", 46, { weight: 700 });
  pre.text(300, 1480, "Pilotes", 46, { weight: 700 });
  // en vivo, mientras habla: subtítulo cobre y +2 tipos
  const sc = new Scene(0, tm.start + 0.35, 1.2);
  sc.text(540, 585, "y cuándo usar cada una", 54, { color: "#C8721E", weight: 700 });
  sc.text(800, 1470, "+ corrida y losa", 40, { color: "#C8721E", weight: 700 });
  return [...pre.els, ...fit(sc, tm, 0.95)];
};

// ---------- 1 · Zapata aislada ----------
const aislada = (tm: Tm) => {
  const sc = new Scene(1, tm.start + 0.05);
  titulo(sc, "TIPO 1 DE 5", "ZAPATA AISLADA");
  const P = iso(540, 1020, 118);
  box(sc, P, -2.3, -2.3, -0.5, 4.6, 4.6, 0.5, TIERRA, 4);
  box(sc, P, -1, -1, 0, 2, 2, 0.6, CONC);
  box(sc, P, -0.25, -0.25, 0.6, 0.5, 0.5, 2.9, COLS);
  sc.arrow(P(0, 0, 4.4), P(0, 0, 3.6), RED, 7, 26);
  // la carga baja al terreno
  ([[1, -0.6], [1, 0.5], [-0.5, 1], [0.6, 1]] as [number, number][]).forEach(([x, y]) => {
    const a = P(x, y, 0);
    sc.arrow(a, [a[0], a[1] + 70], RED, 5, 16);
  });
  const c = P(-0.25, 0.25, 2.4);
  leader(sc, [c[0] - 10, c[1]], [c[0] - 120, c[1] - 40]);
  sc.text(c[0] - 220, c[1] - 50, "COLUMNA", 42);
  const z = P(1, -1, 0.3);
  leader(sc, [z[0] + 10, z[1]], [z[0] + 100, z[1] - 50]);
  sc.text(z[0] + 190, z[1] - 62, "ZAPATA", 42);
  const t = P(-2.3, 2.3, -0.5);
  sc.text(t[0] + 230, t[1] + 80, "TERRENO", 42);
  return fit(sc, tm);
};

// ---------- 2 · Zapata corrida ----------
const corrida = (tm: Tm) => {
  const sc = new Scene(2, tm.start + 0.05);
  titulo(sc, "TIPO 2 DE 5", "ZAPATA CORRIDA");
  const P = iso(520, 1000, 100);
  box(sc, P, -3, -1.6, -0.5, 6, 3.2, 0.5, TIERRA, 4);
  box(sc, P, -2.6, -0.6, 0, 5.2, 1.2, 0.45, CONC);
  box(sc, P, -2.6, -0.15, 0.45, 5.2, 0.3, 2.3, MURO);
  [-2.1, -1.05, 0, 1.05, 2.1].forEach((x) => sc.arrow(P(x, 0, 3.6), P(x, 0, 2.8), RED, 5, 18));
  const m = P(-2.6, 0.15, 1.6);
  leader(sc, [m[0] - 8, m[1]], [m[0] - 70, m[1] - 70]);
  sc.text(m[0] - 60, m[1] - 90, "MURO DE CARGA", 40);
  const z = P(2.6, 0.6, 0.2);
  leader(sc, [z[0] + 8, z[1] + 4], [z[0] + 40, z[1] + 90]);
  sc.text(z[0] - 30, z[1] + 140, "ZAPATA CORRIDA", 40);
  sc.text(540, 1470, "Reparte la carga en línea", 46, { color: RED });
  return fit(sc, tm);
};

// ---------- 3 · Zapata combinada ----------
const combinada = (tm: Tm) => {
  const sc = new Scene(3, tm.start + 0.05);
  titulo(sc, "TIPO 3 DE 5", "ZAPATA COMBINADA");
  const P = iso(540, 1020, 105);
  box(sc, P, -3, -1.8, -0.5, 6, 3.6, 0.5, TIERRA, 4);
  box(sc, P, -2.3, -0.9, 0, 4.6, 1.8, 0.5, CONC);
  box(sc, P, -1.55, -0.25, 0.5, 0.5, 0.5, 2.6, COLS);
  box(sc, P, 1.05, -0.25, 0.5, 0.5, 0.5, 2.6, COLS);
  sc.arrow(P(-1.3, 0, 4.0), P(-1.3, 0, 3.2), RED, 6, 22);
  sc.arrow(P(1.3, 0, 4.0), P(1.3, 0, 3.2), RED, 6, 22);
  const c1 = P(-1.55, 0.25, 2.2);
  sc.text(c1[0] - 120, c1[1] - 20, "COLUMNA 1", 38);
  const c2 = P(1.55, 0.25, 2.2);
  sc.text(c2[0] + 130, c2[1] - 20, "COLUMNA 2", 38);
  sc.text(540, 1440, "Una sola zapata para las dos", 46, { color: RED });
  return fit(sc, tm);
};

// ---------- 4 · Losa de cimentación ----------
const losa = (tm: Tm) => {
  const sc = new Scene(4, tm.start + 0.05);
  titulo(sc, "TIPO 4 DE 5", "LOSA DE CIMENTACIÓN");
  const P = iso(540, 960, 92);
  box(sc, P, -3.1, -3.1, -0.5, 6.2, 6.2, 0.5, TIERRA, 4);
  box(sc, P, -2.5, -2.5, 0, 5, 5, 0.35, CONC);
  const cols: [number, number][] = [];
  [-1.7, 0, 1.7].forEach((x) => [-1.7, 0, 1.7].forEach((y) => cols.push([x, y])));
  cols.sort((a, b) => a[0] + a[1] - (b[0] + b[1]));
  cols.forEach(([x, y]) => box(sc, P, x - 0.2, y - 0.2, 0.35, 0.4, 0.4, 1.5, COLS, 4));
  ([[2.4, 0], [0, 2.4], [-2.4, 0], [0, -2.4]] as Pt[]).forEach(([x, y]) => sc.arrow(P(x * 0.35, y * 0.35, 0.36), P(x, y, 0.36), RED, 5, 18));
  sc.text(540, 1460, "Toda la estructura sobre una placa", 44);
  sc.text(540, 1540, "Suelo blando", 46, { color: RED });
  return fit(sc, tm);
};

// ---------- 5 · Pilotes (corte) ----------
const pilotes = (tm: Tm) => {
  const sc = new Scene(5, tm.start + 0.05);
  titulo(sc, "TIPO 5 DE 5", "PILOTES");
  const rect = (x0: number, y0: number, x1: number, y1: number): Pt[] => [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]];
  // suelo blando y estrato firme
  sc.fill(rect(120, 760, 960, 1230), "#FBEBDA");
  sc.stroke([[120, 760], [960, 760]], INK, 5);
  sc.hatch(150, 960, 790, 26, 34, "#E2A86A", 2.5);
  sc.fill(rect(120, 1230, 960, 1420), SOIL);
  sc.stroke([[120, 1230], [960, 1230]], INK, 4, { wob: 2.5 });
  sc.hatch(150, 960, 1260, 40, 26, SOIL_D, 3);
  sc.text(250, 1120, "SUELO BLANDO", 36, { anchor: "start", color: "#8A4C12" });
  sc.text(250, 1390, "ESTRATO FIRME", 36, { anchor: "start", color: "#7A3F0A" });
  // pilotes, encepado y columna
  [425, 520, 615].forEach((x) => {
    sc.fill(rect(x, 800, x + 40, 1320), "#C9D5DF");
    sc.stroke(rect(x, 800, x + 40, 1320), INK, 4);
  });
  sc.fill(rect(395, 700, 685, 800), "#DCE5EC");
  sc.stroke(rect(395, 700, 685, 800), INK, 5);
  sc.fill(rect(505, 440, 575, 700), BLUE);
  sc.stroke(rect(505, 440, 575, 700), INK, 5);
  sc.arrow([540, 340], [540, 430], RED, 7, 26);
  [445, 540, 635].forEach((x) => sc.arrow([x, 1325], [x, 1395], RED, 5, 16));
  // cota de profundidad
  sc.stroke([[780, 800], [780, 1320]], INK, 3);
  sc.stroke([[765, 800], [795, 800]], INK, 3, { wob: 0 });
  sc.stroke([[765, 1320], [795, 1320]], INK, 3, { wob: 0 });
  sc.text(800, 1065, "PROFUNDIDAD", 32, { anchor: "start" });
  return fit(sc, tm);
};

// ---------- 6 · ¿Cuál te toca? + 7 · CTA (misma página) ----------
const cual = (tm: Tm) => {
  const sc = new Scene(6, tm.start + 0.05);
  sc.text(540, 330, "¿CUÁL TE TOCA?", 96, { weight: 700, dur: 0.45 });
  sc.underline(200, 880, 355);
  const caja = (cx: number, l1: string, l2?: string) => {
    const r: Pt[] = [[cx - 150, 520], [cx + 150, 520], [cx + 150, 680], [cx - 150, 680], [cx - 150, 520]];
    sc.stroke(r, INK, 5, { wob: 2 });
    sc.text(cx, l2 ? 590 : 615, l1, 40);
    if (l2) sc.text(cx, 645, l2, 40);
  };
  caja(185, "CARGAS");
  caja(540, "SUELO");
  caja(895, "ESTUDIO", "GEOTÉCNICO");
  sc.arrow([185, 690], [430, 860], RED, 5, 20);
  sc.arrow([540, 690], [540, 860], RED, 5, 20);
  sc.arrow([895, 690], [650, 860], RED, 5, 20);
  sc.text(540, 940, "TU CIMENTACIÓN", 64, { weight: 700 });
  return fit(sc, tm);
};
const cta = (tm: Tm) => {
  const sc = new Scene(7, tm.start + 0.05);
  sc.text(540, 1180, "Comenta", 70, { weight: 700, dur: 0.3 });
  sc.text(540, 1340, "ZAPATA", 150, { font: "PermanentMarker", weight: 400, color: NAVY, bg: AMBER, dur: 0.45 });
  sc.text(540, 1480, "y te llega gratis nuestra", 44, { dur: 0.35 });
  sc.text(540, 1545, "calculadora de zapatas", 50, { color: RED, dur: 0.35 });
  return fit(sc, tm);
};

export const ELS: El[] = [
  ...portada(S[0]),
  ...aislada(S[1]),
  ...corrida(S[2]),
  ...combinada(S[3]),
  ...losa(S[4]),
  ...pilotes(S[5]),
  ...cual(S[6]),
  ...cta(S[7]),
];
// página de cada escena (la 6 y la 7 comparten página)
export const PAGE_OF = [0, 1, 2, 3, 4, 5, 6, 6];
export const PAGE_START = [0, S[1].start - 0.15, S[2].start - 0.15, S[3].start - 0.15, S[4].start - 0.15, S[5].start - 0.15, S[6].start - 0.15];
export const TOTAL = S[7].start + S[7].dur + 0.8;
void INK;
