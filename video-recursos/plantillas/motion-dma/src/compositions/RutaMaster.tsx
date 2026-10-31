import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { brand } from "../brand/brand";
import { ease, progress } from "../lib/motion";
import { useScale } from "../lib/useScale";
import data from "../data/master.json";

// Ruta del Máster DMA: una línea de luz cobre recorre 4 bloques y llega al título.
// Tiempos anclados a la voz IA de Gabriel (data/master.json, verificada con Whisper).

type Word = { w: string; s: number; e: number };
type Scene = { start: number; dur: number };
const WORDS: Word[] = data.words;
const SCENES: Scene[] = data.scenes;
const FPS = 30;
const F = (s: number) => Math.round(s * FPS);
export const RM_DURATION = Math.ceil(data.total * FPS);

const C = {
  navy: "#0D1E3A",
  surface: "#14284B",
  copper: "#D78631",
  copperHi: "#F2A95C",
  copperDeep: "#8E5219",
  green: "#3FB68B",
  muted: "#9FB0CC",
  off: "#2B3E63",
  offDeep: "#16243F",
  offText: "#6F82A6",
};

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]/g, "");

/** Segundo en que empieza la primera palabra que arranca con `stem`, después de `after`. */
const wordAt = (stem: string, after = 0): number => {
  const w = WORDS.find((x) => x.s >= after - 0.05 && norm(x.w).startsWith(stem));
  return w ? w.s : after;
};

const sc = (i: number) => SCENES[i];
const sStart = (i: number) => F(sc(i).start);

const BLOCKS = [
  { n: 1, name: "BIM PROFESSIONAL", chips: [["COMPRENDE", "comprend"], ["ESTRUCTURA", "estructur"], ["IMPLEMENTA", "implement"]] },
  { n: 2, name: "BIM COORDINATION", chips: [["INTEGRA", "integr"], ["COORDINA", "coordinas"], ["RESUELVE", "resuelv"]] },
  { n: 3, name: "BIM MANAGEMENT", chips: [["PLANIFICA", "planific"], ["4D · 5D", "tiempo"], ["DIRIGE", "dirig"]] },
  { n: 4, name: "BIM + AI", chips: [["AUTOMATIZA", "automatiz"], ["DYNAMO", "dynamo"], ["PYTHON", "python"]] },
] as const;

// ── Geometría del mundo ────────────────────────────────────────────────────
type Pt = { x: number; y: number };
type Layout = {
  w: number;
  h: number;
  pts: Pt[]; // S, B1..B4, G
  vertical: boolean;
  focusAnchor: Pt;
  overview: { c: Pt; s: number; a: Pt };
};
const LAYOUT_V: Layout = {
  w: 1080,
  h: 1900,
  pts: [
    { x: 540, y: 1700 },
    { x: 290, y: 1480 },
    { x: 790, y: 1160 },
    { x: 290, y: 840 },
    { x: 790, y: 520 },
    { x: 310, y: 210 },
  ],
  vertical: true,
  focusAnchor: { x: 540, y: 650 },
  overview: { c: { x: 540, y: 840 }, s: 0.5, a: { x: 540, y: 1000 } },
};
const LAYOUT_H: Layout = {
  w: 3400,
  h: 1080,
  pts: [
    { x: 150, y: 600 },
    { x: 500, y: 640 },
    { x: 1150, y: 420 },
    { x: 1800, y: 640 },
    { x: 2450, y: 420 },
    { x: 3100, y: 540 },
  ],
  vertical: false,
  focusAnchor: { x: 520, y: 560 },
  overview: { c: { x: 1625, y: 540 }, s: 0.56, a: { x: 960, y: 590 } },
};

const segCtrl = (a: Pt, b: Pt, vertical: boolean): [Pt, Pt] =>
  vertical
    ? [{ x: a.x, y: a.y + (b.y - a.y) * 0.5 }, { x: b.x, y: b.y - (b.y - a.y) * 0.5 }]
    : [{ x: a.x + (b.x - a.x) * 0.5, y: a.y }, { x: b.x - (b.x - a.x) * 0.5, y: b.y }];

const bez = (p0: Pt, p1: Pt, p2: Pt, p3: Pt, t: number): Pt => {
  const m = 1 - t;
  return {
    x: m * m * m * p0.x + 3 * m * m * t * p1.x + 3 * m * t * t * p2.x + t * t * t * p3.x,
    y: m * m * m * p0.y + 3 * m * m * t * p1.y + 3 * m * t * t * p2.y + t * t * t * p3.y,
  };
};

const buildPath = (L: Layout) => {
  let d = `M ${L.pts[0].x} ${L.pts[0].y}`;
  const samples: { p: Pt; len: number }[] = [{ p: L.pts[0], len: 0 }];
  const cum = [0];
  let len = 0;
  for (let i = 1; i < L.pts.length; i++) {
    const a = L.pts[i - 1];
    const b = L.pts[i];
    const [c1, c2] = segCtrl(a, b, L.vertical);
    d += ` C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${b.x} ${b.y}`;
    let prev = a;
    for (let k = 1; k <= 60; k++) {
      const p = bez(a, c1, c2, b, k / 60);
      len += Math.hypot(p.x - prev.x, p.y - prev.y);
      samples.push({ p, len });
      prev = p;
    }
    cum.push(len);
  }
  return { d, samples, cum, total: len };
};

const pointAt = (samples: { p: Pt; len: number }[], l: number): Pt => {
  for (let i = 1; i < samples.length; i++) {
    if (samples[i].len >= l) {
      const a = samples[i - 1];
      const b = samples[i];
      const t = (l - a.len) / Math.max(1e-6, b.len - a.len);
      return { x: a.p.x + (b.p.x - a.p.x) * t, y: a.p.y + (b.p.y - a.p.y) * t };
    }
  }
  return samples[samples.length - 1].p;
};

// ── Línea de tiempo ────────────────────────────────────────────────────────
const MOVE = 20; // frames de cámara/línea al llegar a un bloque
// Ventana en que la línea viaja hacia el punto i (1..5)
const travel = (i: number): [number, number] => {
  if (i <= 4) return [sStart(i), sStart(i) + MOVE];
  return [sStart(6), sStart(6) + 26];
};
const litAt = (i: number) => travel(i)[1];

const T_MICRO = F(wordAt("microcredencial", sc(5).start));
const T_INSIGNIA = F(wordAt("insignia", sc(5).start));
const T_SEPARADO = F(wordAt("separado", sc(5).start) - 0.35);
const T_TITULO = F(wordAt("titulo", sc(6).start));
const T_PIDE = F(wordAt("pide", sc(6).start) - 0.1);

type Cam = { c: Pt; s: number; a: Pt };
const lerpCam = (x: Cam, y: Cam, t: number): Cam => ({
  c: { x: x.c.x + (y.c.x - x.c.x) * t, y: x.c.y + (y.c.y - x.c.y) * t },
  s: x.s + (y.s - x.s) * t,
  a: { x: x.a.x + (y.a.x - x.a.x) * t, y: x.a.y + (y.a.y - x.a.y) * t },
});

const cameraAt = (frame: number, L: Layout): Cam => {
  const ov: Cam = L.overview;
  const focus = (i: number): Cam => ({ c: L.pts[i], s: 1, a: L.focusAnchor });
  const keys: { t: number; cam: Cam }[] = [
    { t: 0, cam: ov },
    { t: sStart(1), cam: ov },
    { t: sStart(1) + MOVE + 4, cam: focus(1) },
    { t: sStart(2), cam: focus(1) },
    { t: sStart(2) + MOVE + 4, cam: focus(2) },
    { t: sStart(3), cam: focus(2) },
    { t: sStart(3) + MOVE + 4, cam: focus(3) },
    { t: sStart(4), cam: focus(3) },
    { t: sStart(4) + MOVE + 4, cam: focus(4) },
    { t: sStart(5), cam: focus(4) },
    { t: sStart(5) + 24, cam: ov },
  ];
  // Respiración lenta en el plano general
  for (let k = keys.length - 1; k >= 0; k--) {
    if (frame >= keys[k].t) {
      const nx = keys[k + 1];
      if (!nx) return keys[k].cam;
      const t = interpolate(frame, [keys[k].t, nx.t], [0, 1], {
        easing: ease.inOut,
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return lerpCam(keys[k].cam, nx.cam, t);
    }
  }
  return ov;
};

// ── Piezas ─────────────────────────────────────────────────────────────────
const Node: React.FC<{ p: Pt; n: number; lit: number; pop: number; ring: number; k: number }> = ({ p, n, lit, pop, ring, k }) => {
  const R = 95;
  const scale = 1 + 0.12 * Math.sin(Math.PI * pop);
  return (
    <div style={{ position: "absolute", left: p.x - R, top: p.y - R, width: R * 2, height: R * 2 + 18, transform: `scale(${k})`, transformOrigin: `${R}px ${R}px` }}>
      {ring > 0 && ring < 1 && (
        <div
          style={{
            position: "absolute",
            left: R - R * (1 + ring * 0.9),
            top: R - R * (1 + ring * 0.9),
            width: R * 2 * (1 + ring * 0.9),
            height: R * 2 * (1 + ring * 0.9),
            borderRadius: "50%",
            border: `8px solid ${C.copperHi}`,
            opacity: 1 - ring,
          }}
        />
      )}
      <div style={{ position: "absolute", inset: 0, transform: `scale(${scale})`, transformOrigin: "50% 50%" }}>
        {/* canto 3D */}
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 18,
            width: R * 2,
            height: R * 2,
            borderRadius: "50%",
            background: lit > 0.5 ? C.copperDeep : C.offDeep,
          }}
        />
        {/* cara apagada */}
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: R * 2,
            height: R * 2,
            borderRadius: "50%",
            background: `radial-gradient(circle at 38% 30%, #3A5080 0%, ${C.off} 60%)`,
            boxShadow: "inset 0 -6px 0 rgba(0,0,0,.18)",
          }}
        />
        {/* cara encendida */}
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: R * 2,
            height: R * 2,
            borderRadius: "50%",
            opacity: lit,
            background: `radial-gradient(circle at 38% 30%, #FFD09A 0%, ${C.copperHi} 30%, ${C.copper} 75%)`,
            boxShadow: `0 0 ${70 * lit}px ${C.copper}AA, inset 0 -6px 0 rgba(0,0,0,.15)`,
          }}
        />
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: R * 2,
            height: R * 2,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: brand.fontDisplay,
            fontSize: 112,
            color: lit > 0.5 ? "#FFFFFF" : C.offText,
            textShadow: lit > 0.5 ? "0 4px 0 rgba(142,82,25,.6)" : "none",
            paddingTop: 6,
          }}
        >
          {n}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          top: R * 2 + 34,
          left: -80,
          width: R * 2 + 160,
          textAlign: "center",
          fontFamily: brand.fontBody,
          fontWeight: 800,
          fontSize: 34,
          letterSpacing: 3,
          color: lit > 0.5 ? "#FFFFFF" : C.offText,
        }}
      >
        BLOQUE {n}
      </div>
    </div>
  );
};

const Cap: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <path d="M50 18 L95 38 L50 58 L5 38 Z" fill={color} />
    <path d="M25 48 L25 70 Q50 84 75 70 L75 48 L50 60 Z" fill={color} opacity={0.85} />
    <path d="M88 41 L88 66" stroke={color} strokeWidth={4} />
    <circle cx={88} cy={69} r={5} fill={color} />
  </svg>
);

const Goal: React.FC<{ p: Pt; lit: number; burst: number; k: number; label: boolean }> = ({ p, lit, burst, k, label }) => {
  const R = 125;
  const pieces = Array.from({ length: 22 }, (_, i) => {
    const ang = (i / 22) * Math.PI * 2 + (i % 3) * 0.2;
    const dist = 140 + (i % 5) * 38;
    return { ang, dist, col: [C.copperHi, C.green, "#FFFFFF"][i % 3], sz: 14 + (i % 4) * 5 };
  });
  return (
    <div style={{ position: "absolute", left: p.x - R, top: p.y - R, width: R * 2, height: R * 2, transform: `scale(${k})`, transformOrigin: `${R}px ${R}px` }}>
      {burst > 0 &&
        burst < 1 &&
        pieces.map((q, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: R + Math.cos(q.ang) * q.dist * burst - q.sz / 2,
              top: R + Math.sin(q.ang) * q.dist * burst - q.sz / 2 + 60 * burst * burst,
              width: q.sz,
              height: q.sz,
              borderRadius: i % 2 ? "50%" : 3,
              background: q.col,
              opacity: 1 - burst,
            }}
          />
        ))}
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: 48,
          transform: "rotate(45deg)",
          border: `6px dashed ${C.offText}`,
          opacity: 1 - lit,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: 48,
          transform: `rotate(45deg) scale(${0.96 + 0.04 * lit})`,
          background: `linear-gradient(135deg, ${C.copperHi}, ${C.copper})`,
          boxShadow: `0 0 ${110 * lit}px ${C.copper}`,
          opacity: lit,
        }}
      />
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Cap size={150} color={lit > 0.5 ? C.navy : C.offText} />
      </div>
      <div
        style={{
          display: label ? "block" : "none",
          position: "absolute",
          top: R * 2 + 46,
          left: -120,
          width: R * 2 + 240,
          textAlign: "center",
          fontFamily: brand.fontDisplay,
          fontSize: 76,
          color: lit > 0.5 ? C.copperHi : C.offText,
          letterSpacing: 2,
        }}
      >
        MÁSTER
      </div>
    </div>
  );
};

const Coin: React.FC<{ size: number }> = ({ size }) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: "50%",
      background: `radial-gradient(circle at 35% 30%, #FFFFFF, ${C.green} 60%)`,
      border: "4px solid #FFFFFF",
      boxShadow: "0 4px 0 rgba(0,0,0,.25)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: brand.fontBody,
      fontWeight: 800,
      fontSize: size * 0.42,
      color: C.navy,
    }}
  >
    ✓
  </div>
);

const Shield: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size * 1.15} viewBox="0 0 100 115">
    <path d="M50 4 L92 18 L92 56 Q92 92 50 111 Q8 92 8 56 L8 18 Z" fill={C.copperHi} stroke="#FFFFFF" strokeWidth={6} />
    <path d="M50 30 L57 46 L75 47 L61 58 L66 76 L50 66 L34 76 L39 58 L25 47 L43 46 Z" fill="#FFFFFF" />
  </svg>
);

const Card: React.FC<{ b: (typeof BLOCKS)[number]; frame: number; vertical: boolean; start: number; end: number }> = ({
  b,
  frame,
  vertical,
  start,
  end,
}) => {
  const pin = progress(frame, start, 14);
  const pout = progress(frame, end - 8, 8, ease.in);
  const op = pin * (1 - pout);
  if (op <= 0) return null;
  const box: React.CSSProperties = vertical
    ? { left: 80, width: 920, top: 905 }
    : { left: 980, width: 840, top: 330 };
  return (
    <div
      style={{
        position: "absolute",
        ...box,
        padding: "34px 40px 40px",
        borderRadius: 16,
        background: "rgba(20,40,75,.98)",
        borderTop: `8px solid ${C.copper}`,
        boxShadow: "0 30px 80px rgba(0,0,0,.45)",
        opacity: op,
        transform: `translateY(${(1 - pin) * 40 + pout * 20}px)`,
      }}
    >
      <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 32, letterSpacing: 4, color: C.copperHi }}>
        BLOQUE {b.n} DE 4
      </div>
      <div style={{ fontFamily: brand.fontDisplay, fontSize: vertical ? 96 : 92, color: "#FFFFFF", lineHeight: 1.08, marginTop: 6 }}>
        {b.name}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 26, flexWrap: "wrap" }}>
        {b.chips.map(([label, stem], i) => {
          const t = F(wordAt(stem, sc(b.n).start)) - 3;
          const p = spring({ frame: frame - t, fps: FPS, config: { damping: 14, stiffness: 180 } });
          return (
            <React.Fragment key={label}>
              {i > 0 && (
                <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, color: C.copper, opacity: p }}>→</div>
              )}
              <div
                style={{
                  padding: "14px 22px 10px",
                  borderRadius: 999,
                  background: p > 0.5 ? C.copper : "transparent",
                  border: `3px solid ${C.copper}`,
                  fontFamily: brand.fontBody,
                  fontWeight: 800,
                  fontSize: 31,
                  color: "#FFFFFF",
                  letterSpacing: 1,
                  opacity: Math.min(1, p * 1.5),
                  transform: `scale(${0.9 + 0.1 * p})`,
                }}
              >
                {label}
              </div>
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// Subtítulos de 1–2 palabras sincronizados con la voz
const KEY = ["bim", "master", "bloque", "microcredencial", "insignia", "ia", "dynamo", "python", "separado", "informacion"];
const GROUPS = (() => {
  const g: { t: string; s: number; e: number; key: boolean }[] = [];
  let i = 0;
  while (i < WORDS.length) {
    const a = WORDS[i];
    const b = WORDS[i + 1];
    const join = b && b.s - a.e < 0.12 && (a.w + b.w).length <= 14 && !/[.,:?]$/.test(a.w);
    const ws = join ? [a, b] : [a];
    g.push({
      t: ws.map((x) => x.w).join(" "),
      s: a.s,
      e: ws[ws.length - 1].e,
      key: ws.some((x) => KEY.includes(norm(x.w))),
    });
    i += ws.length;
  }
  return g;
})();

const Subs: React.FC<{ frame: number; vertical: boolean; hide: boolean }> = ({ frame, vertical, hide }) => {
  if (hide) return null;
  const t = frame / FPS;
  const idx = GROUPS.findIndex((g, k) => t >= g.s - 0.04 && t < (GROUPS[k + 1] ? Math.min(GROUPS[k + 1].s - 0.04, g.e + 0.5) : g.e + 0.5));
  if (idx < 0) return null;
  const g = GROUPS[idx];
  const p = progress(frame, F(g.s) - 1, 4);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: vertical ? 1465 : 980,
        textAlign: "center",
        fontFamily: brand.fontBody,
        fontWeight: 800,
        fontSize: vertical ? 64 : 58,
        color: g.key ? C.copperHi : "#FFFFFF",
        textShadow: "0 4px 14px rgba(0,0,0,.8), 0 0 3px rgba(0,0,0,.9)",
        textTransform: "uppercase",
        transform: `scale(${0.92 + 0.08 * p})`,
        opacity: p,
      }}
    >
      {g.t.replace(/[.,:?¿]/g, "")}
    </div>
  );
};

const TopText: React.FC<{ frame: number; vertical: boolean }> = ({ frame, vertical }) => {
  const top = vertical ? 395 : 120;
  const size = vertical ? 104 : 96;
  const items: { a: number; b: number; node: React.ReactNode }[] = [
    {
      a: -999,
      b: sStart(1),
      node: (
        <>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: size, color: "#FFFFFF", lineHeight: 1 }}>
            LA RUTA DEL <span style={{ color: C.copperHi }}>MÁSTER</span>
          </div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, letterSpacing: 5, color: C.muted, marginTop: 14 }}>
            4 BLOQUES · EN ORDEN
          </div>
        </>
      ),
    },
    {
      a: T_MICRO - 4,
      b: sStart(6),
      node: (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
          {[
            { t: T_MICRO - 4, icon: <Coin size={54} />, txt: "MICROCREDENCIAL POR MÓDULO" },
            { t: T_INSIGNIA - 4, icon: <Shield size={50} />, txt: "INSIGNIA POR BLOQUE" },
            { t: T_SEPARADO, icon: null, txt: "SE CURSAN POR SEPARADO" },
          ].map((r) => {
            const p = progress(frame, r.t, 10);
            return (
              <div
                key={r.txt}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 18,
                  opacity: p,
                  transform: `translateY(${(1 - p) * 18}px)`,
                  fontFamily: r.icon ? brand.fontBody : brand.fontDisplay,
                  fontWeight: 800,
                  fontSize: r.icon ? (vertical ? 40 : 38) : vertical ? 64 : 60,
                  color: r.icon ? "#FFFFFF" : C.copperHi,
                  letterSpacing: r.icon ? 2 : 1,
                }}
              >
                {r.icon}
                {r.txt}
              </div>
            );
          })}
        </div>
      ),
    },
    {
      a: T_TITULO - 4,
      b: T_PIDE,
      node: (
        <>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: size, color: "#FFFFFF", lineHeight: 1 }}>
            TÍTULO DEL <span style={{ color: C.copperHi }}>MÁSTER</span>
          </div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, letterSpacing: 4, color: C.muted, marginTop: 14 }}>
            12 MESES · 4 BLOQUES · PROYECTO FINAL
          </div>
        </>
      ),
    },
  ];
  return (
    <>
      {items.map((it, k) => {
        if (frame < it.a || frame >= it.b) return null;
        const pin = it.a < 0 ? 1 : progress(frame, it.a, 12);
        const pout = progress(frame, it.b - 8, 8, ease.in);
        return (
          <div
            key={k}
            style={{
              position: "absolute",
              left: 40,
              right: 40,
              top,
              textAlign: "center",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              opacity: pin * (1 - pout),
              transform: `translateY(${(1 - pin) * 24}px)`,
            }}
          >
            {it.node}
          </div>
        );
      })}
    </>
  );
};

const EndCard: React.FC<{ frame: number; vertical: boolean }> = ({ frame, vertical }) => {
  const p = progress(frame, T_PIDE, 14);
  if (p <= 0) return null;
  const b = spring({ frame: frame - T_PIDE - 8, fps: FPS, config: { damping: 14 } });
  return (
    <AbsoluteFill
      style={{
        background: `rgba(13,30,58,${0.9 * p})`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: vertical ? 60 : 44,
        paddingBottom: vertical ? 120 : 0,
      }}
    >
      <Img src={staticFile("logo-dma.png")} style={{ width: vertical ? 560 : 520, opacity: p, transform: `translateY(${(1 - p) * 20}px)` }} />
      <div
        style={{
          padding: "26px 54px 18px",
          borderRadius: 12,
          background: C.copper,
          fontFamily: brand.fontDisplay,
          fontSize: vertical ? 84 : 76,
          color: "#FFFFFF",
          opacity: Math.min(1, b * 1.4),
          transform: `scale(${0.9 + 0.1 * b})`,
        }}
      >
        PIDE INFORMACIÓN
      </div>
    </AbsoluteFill>
  );
};

// ── Composición ────────────────────────────────────────────────────────────
export const RutaMaster: React.FC = () => {
  const frame = useCurrentFrame();
  const { isVertical } = useScale();
  const { durationInFrames } = useVideoConfig();
  const L = isVertical ? LAYOUT_V : LAYOUT_H;
  const path = React.useMemo(() => buildPath(L), [L]);

  // Longitud encendida de la línea
  let lit = 0;
  for (let i = 1; i <= 5; i++) {
    const [a, b] = travel(i);
    const p = interpolate(frame, [a, b], [0, 1], { easing: ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    if (frame >= a) lit = path.cum[i - 1] + (path.cum[i] - path.cum[i - 1]) * p;
  }
  const head = pointAt(path.samples, lit);
  const cam = cameraAt(frame, L);
  const tx = cam.a.x - cam.c.x * cam.s;
  const ty = cam.a.y - cam.c.y * cam.s;
  const k = interpolate(cam.s, [L.overview.s, 1], [isVertical ? 1.55 : 1.35, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const gridShift = (frame * 0.4) % 60;

  return (
    <AbsoluteFill style={{ backgroundColor: C.navy, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.045) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.045) 2px, transparent 2px)",
          backgroundSize: "60px 60px",
          backgroundPosition: `${gridShift}px ${gridShift}px`,
        }}
      />
      <AbsoluteFill style={{ background: `radial-gradient(70% 55% at 50% 45%, ${C.copper}1F 0%, transparent 70%)` }} />

      {/* Mundo */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: L.w,
          height: L.h,
          transformOrigin: "0 0",
          transform: `translate(${tx}px, ${ty}px) scale(${cam.s})`,
        }}
      >
        <svg width={L.w} height={L.h} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <path d={path.d} fill="none" stroke={C.off} strokeWidth={22} strokeLinecap="round" strokeDasharray="2 40" />
          <path
            d={path.d}
            fill="none"
            stroke={C.copper}
            strokeWidth={36}
            strokeLinecap="round"
            strokeDasharray={`${path.total} ${path.total}`}
            strokeDashoffset={path.total - lit}
            opacity={0.25}
            style={{ filter: "blur(10px)" }}
          />
          <path
            d={path.d}
            fill="none"
            stroke={C.copperHi}
            strokeWidth={16}
            strokeLinecap="round"
            strokeDasharray={`${path.total} ${path.total}`}
            strokeDashoffset={path.total - lit}
          />
          {lit > 2 && <circle cx={head.x} cy={head.y} r={20} fill="#FFFFFF" style={{ filter: `drop-shadow(0 0 18px ${C.copperHi})` }} />}
          <circle cx={L.pts[0].x} cy={L.pts[0].y} r={20} fill={C.copperHi} />
        </svg>

        {BLOCKS.map((b) => {
          const t = litAt(b.n);
          const on = progress(frame, t - 2, 8);
          const pop = interpolate(frame, [t, t + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const ring = interpolate(frame, [t, t + 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const p = L.pts[b.n];
          const coin = (j: number) => spring({ frame: frame - T_MICRO - b.n * 3 - j * 4, fps: FPS, config: { damping: 12 } });
          const sh = spring({ frame: frame - T_INSIGNIA - b.n * 3, fps: FPS, config: { damping: 12 } });
          return (
            <React.Fragment key={b.n}>
              <Node p={p} n={b.n} lit={on} pop={pop} ring={ring} k={k} />
              {/* microcredenciales */}
              {[0, 1, 2].map((j) => (
                <div
                  key={j}
                  style={{
                    position: "absolute",
                    left: p.x + (70 + j * 46) * k,
                    top: p.y - (150 + j * 6) * k,
                    transform: `scale(${coin(j) * k})`,
                    transformOrigin: "0 0",
                    opacity: Math.min(1, coin(j) * 2),
                  }}
                >
                  <Coin size={82} />
                </div>
              ))}
              {/* insignia */}
              <div
                style={{
                  position: "absolute",
                  left: p.x - 200 * k,
                  top: p.y - 170 * k,
                  transform: `scale(${sh * k}) rotate(${(1 - sh) * -20}deg)`,
                  transformOrigin: "0 0",
                  opacity: Math.min(1, sh * 2),
                }}
              >
                <Shield size={110} />
              </div>
            </React.Fragment>
          );
        })}
        <Goal
          p={L.pts[5]}
          lit={progress(frame, litAt(5) - 2, 10)}
          burst={interpolate(frame, [litAt(5), litAt(5) + 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
          k={k}
          label={!isVertical}
        />
      </div>

      {(
        <AbsoluteFill
          style={{
            background: isVertical
              ? "linear-gradient(180deg, transparent 0px, transparent 1150px, rgba(13,30,58,.95) 1270px)"
              : "linear-gradient(90deg, transparent 0px, transparent 930px, rgba(13,30,58,.85) 1010px)",
            opacity: interpolate(k, [1, 1.2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        />
      )}
      {/* Tarjetas de cada bloque */}
      {BLOCKS.map((b) => (
        <Card key={b.n} b={b} frame={frame} vertical={isVertical} start={sStart(b.n) + 10} end={sStart(b.n + 1)} />
      ))}

      <TopText frame={frame} vertical={isVertical} />
      <Subs frame={frame} vertical={isVertical} hide={frame >= T_PIDE || frame < 4} />

      <Img
        src={staticFile("logo-dma.png")}
        style={{
          position: "absolute",
          width: isVertical ? 300 : 230,
          left: isVertical ? 390 : 1650,
          top: isVertical ? 255 : 40,
          opacity: frame >= T_PIDE ? 0 : 1,
        }}
      />
      <EndCard frame={frame} vertical={isVertical} />

      {/* Audio */}
      <Audio src={staticFile("rutas/voz_master.wav")} />
      <Audio
        src={staticFile("rutas/musica_master.wav")}
        volume={(f) => {
          const talk = WORDS.some((w) => f / FPS >= w.s - 0.25 && f / FPS <= w.e + 0.35);
          const end = interpolate(f, [durationInFrames - 20, durationInFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (talk ? 0.07 : 0.32) * end;
        }}
      />
      {[1, 2, 3, 4].map((i) => (
        <Sequence key={i} from={litAt(i) - 1} durationInFrames={40}>
          <Audio src={staticFile("sfx/interface/bong_001.ogg")} volume={0.45} />
        </Sequence>
      ))}
      {[1, 2, 3, 4, 5].map((i) => (
        <Sequence key={`w${i}`} from={sStart(i)} durationInFrames={30}>
          <Audio src={staticFile("sfx/ui/rollover2.ogg")} volume={0.35} />
        </Sequence>
      ))}
      {BLOCKS.flatMap((b) =>
        b.chips.map(([label, stem]) => (
          <Sequence key={label} from={Math.max(0, F(wordAt(stem, sc(b.n).start)) - 3)} durationInFrames={20}>
            <Audio src={staticFile("sfx/ui/switch7.ogg")} volume={0.25} />
          </Sequence>
        )),
      )}
      <Sequence from={T_MICRO} durationInFrames={30}>
        <Audio src={staticFile("sfx/casino/chips-stack-2.ogg")} volume={0.4} />
      </Sequence>
      <Sequence from={T_INSIGNIA} durationInFrames={30}>
        <Audio src={staticFile("sfx/interface/drop_002.ogg")} volume={0.4} />
      </Sequence>
      <Sequence from={litAt(5)} durationInFrames={60}>
        <Audio src={staticFile("sfx/impact/impactBell_heavy_000.ogg")} volume={0.35} />
      </Sequence>
    </AbsoluteFill>
  );
};
