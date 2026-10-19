// Motor de «dibujo a mano»: trazos que se dibujan solos, rellenos que aparecen después del
// contorno, textos que se escriben, y la posición de la punta del marcador en cada instante.
export type Pt = [number, number];
export type El =
  | { k: "stroke"; pts: Pt[]; t0: number; dur: number; color: string; w: number; scene: number }
  | { k: "fill"; pts: Pt[]; t0: number; color: string; scene: number; op?: number }
  | { k: "text"; x: number; y: number; txt: string; size: number; t0: number; dur: number; color: string; anchor: "start" | "middle"; font: string; scene: number; weight?: number; bg?: string };

export const INK = "#0D1E3A";
export const RED = "#C8721E";
export const BLUE = "#2E6A8E";
export const BLUE_D = "#004A70";
export const BLUE_L = "#8FB3CB";
export const CON_T = "#E8EEF3";
export const CON_X = "#C9D5DF";
export const CON_Y = "#A7B9C8";
export const SOIL = "#E9B47E";
export const SOIL_D = "#D78631";
export const AMBER = "#D78631";
export const NAVY = "#0D1E3A";

// ruido determinista para que el trazo tiemble como hecho a mano
const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};
let seed = 1;
export const wobble = (pts: Pt[], amp = 1.3): Pt[] => {
  const out: Pt[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [ax, ay] = pts[i];
    const [bx, by] = pts[i + 1];
    const L = Math.hypot(bx - ax, by - ay);
    const n = Math.max(1, Math.round(L / 28));
    const nx = -(by - ay) / (L || 1);
    const ny = (bx - ax) / (L || 1);
    for (let j = 0; j < n; j++) {
      const f = j / n;
      const o = j === 0 ? 0 : (rnd(seed++) - 0.5) * 2 * amp;
      out.push([ax + (bx - ax) * f + nx * o, ay + (by - ay) * f + ny * o]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
};

export const polyLen = (pts: Pt[]) => {
  let L = 0;
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return L;
};
export const pointAt = (pts: Pt[], d: number): Pt => {
  let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const s = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (acc + s >= d) {
      const f = s ? (d - acc) / s : 0;
      return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f];
    }
    acc += s;
  }
  return pts[pts.length - 1];
};

// ---------- Constructor de escena ----------
export class Scene {
  els: El[] = [];
  cur: number;
  constructor(public id: number, public t0: number, public speed = 1) {
    this.cur = t0;
  }
  // duración de un trazo según su longitud (≈ 1500 px/s, mínimo 0.12 s)
  private dur(L: number) {
    return Math.max(0.12, L / 1500) / this.speed;
  }
  stroke(pts: Pt[], color = INK, w = 5, opts: { wob?: number; gap?: number; dur?: number } = {}) {
    const p = opts.wob === 0 ? pts : wobble(pts, opts.wob ?? 1.3);
    const d = opts.dur ?? this.dur(polyLen(p));
    this.els.push({ k: "stroke", pts: p, t0: this.cur, dur: d, color, w, scene: this.id });
    this.cur += d + (opts.gap ?? 0.05);
    return this;
  }
  // relleno: se inserta DEBAJO de los trazos que se añadan después y aparece ahora
  fill(pts: Pt[], color: string, op = 1, at?: number) {
    this.els.push({ k: "fill", pts, t0: at ?? this.cur, color, scene: this.id, op });
    return this;
  }
  text(x: number, y: number, txt: string, size = 44, opts: { color?: string; anchor?: "start" | "middle"; font?: string; weight?: number; dur?: number; bg?: string } = {}) {
    const d = opts.dur ?? Math.max(0.25, txt.length * 0.045) / this.speed;
    this.els.push({ k: "text", x, y, txt, size, t0: this.cur, dur: d, color: opts.color ?? INK, anchor: opts.anchor ?? "middle", font: opts.font ?? "Anton", scene: this.id, weight: opts.weight ?? ((opts.font ?? "Anton") === "Anton" ? 400 : 800), bg: opts.bg });
    this.cur += d + 0.08;
    return this;
  }
  wait(s: number) {
    this.cur += s;
    return this;
  }
  arrow(a: Pt, b: Pt, color = RED, w = 6, head = 22) {
    const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
    this.stroke([a, b], color, w, { gap: 0.02 });
    const h1: Pt = [b[0] - head * Math.cos(ang - 0.5), b[1] - head * Math.sin(ang - 0.5)];
    const h2: Pt = [b[0] - head * Math.cos(ang + 0.5), b[1] - head * Math.sin(ang + 0.5)];
    this.stroke([h1, b, h2], color, w, { wob: 0.4, gap: 0.03 });
    return this;
  }
  // subrayado de título
  underline(x0: number, x1: number, y: number, color = INK) {
    return this.stroke([[x0, y], [x1, y + 4]], color, 5, { wob: 2 });
  }
  // rayado de terreno en zigzag dentro de una franja
  hatch(x0: number, x1: number, y0: number, h: number, step = 22, color = INK, w = 2.5) {
    const pts: Pt[] = [];
    for (let x = x0; x <= x1; x += step) {
      pts.push([x, y0], [x - h * 0.6, y0 + h]);
    }
    return this.stroke(pts, color, w, { wob: 0.6, dur: Math.max(0.3, (x1 - x0) / 1400) / this.speed });
  }
}

// ---------- Isométrico ----------
const C30 = Math.cos(Math.PI / 6);
export const iso = (cx: number, cy: number, s: number) => (x: number, y: number, z: number): Pt => [cx + (x - y) * C30 * s, cy + (x + y) * 0.5 * s - z * s];

type P3 = (x: number, y: number, z: number) => Pt;
// caja: contorno visible en 3 trazos + relleno de las 3 caras visibles (debajo del contorno)
export const box = (
  sc: Scene,
  P: P3,
  x0: number,
  y0: number,
  z0: number,
  dx: number,
  dy: number,
  dz: number,
  cols: [string, string, string] = [CON_T, CON_X, CON_Y],
  w = 5,
) => {
  const x1 = x0 + dx;
  const y1 = y0 + dy;
  const z1 = z0 + dz;
  const top: Pt[] = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)];
  const fx: Pt[] = [P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0), P(x1, y0, z0)];
  const fy: Pt[] = [P(x0, y1, z1), P(x1, y1, z1), P(x1, y1, z0), P(x0, y1, z0)];
  const start = sc.cur;
  // contorno
  const tmp = new Scene(sc.id, 0);
  void tmp;
  const fillIdx = sc.els.length;
  sc.stroke([...top, top[0]], INK, w);
  sc.stroke([P(x1, y0, z1), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0), P(x0, y1, z1)], INK, w);
  sc.stroke([P(x1, y1, z1), P(x1, y1, z0)], INK, w, { gap: 0.04 });
  // rellenos insertados por debajo del contorno de esta caja, aparecen al terminarlo
  const at = sc.cur - 0.05;
  const fills: El[] = [
    { k: "fill", pts: top, t0: at, color: cols[0], scene: sc.id, op: 1 },
    { k: "fill", pts: fx, t0: at, color: cols[1], scene: sc.id, op: 1 },
    { k: "fill", pts: fy, t0: at, color: cols[2], scene: sc.id, op: 1 },
  ];
  sc.els.splice(fillIdx, 0, ...fills);
  void start;
};
