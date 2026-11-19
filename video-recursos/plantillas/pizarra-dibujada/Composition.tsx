import React from "react";
import { AbsoluteFill, Audio, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/fonts";
import { El, NAVY, AMBER, Pt, polyLen, pointAt } from "./draw";
import { ELS, PAGE_OF, PAGE_START, TOTAL } from "./scenes";
import WORDS from "./words.json";

// Cimentaciones · pizarra dibujada a mano + voz de Gabriel (IA, Chatterbox, con su permiso)
loadFont({ family: "Kalam", url: staticFile("kalam-latin-700-normal.woff2"), weight: "700" });
loadFont({ family: "Kalam", url: staticFile("kalam-latin-ext-700-normal.woff2"), weight: "700", unicodeRange: "U+0100-024F" });
loadFont({ family: "Kalam", url: staticFile("kalam-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: "Anton", url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: "Anton", url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: "Overpass", url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: "Overpass", url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });
loadFont({ family: "PermanentMarker", url: staticFile("permanent-marker-latin-400-normal.woff2"), weight: "400" });

const FPS = 30;
const W = 1080;
const H = 1920;
const PAPER = "#FAFBFC";
const EASE = Easing.bezier(0.45, 0, 0.55, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const useT = () => useCurrentFrame() / FPS;

const pageOf = (e: El) => PAGE_OF[e.scene];
const NP = PAGE_START.length;
const pageEnd = (p: number) => (p + 1 < NP ? PAGE_START[p + 1] : TOTAL + 10);
const SLIDE = 0.32;

// ancho aproximado de un texto (para que la punta siga la escritura)
const textW = (e: Extract<El, { k: "text" }>) => {
  const anton = e.font === "Anton";
  const over = e.font === "Overpass";
  let w = 0;
  for (const ch of e.txt) {
    const up = /[A-ZÁÉÍÓÚÑ¿?0-9±+]/.test(ch);
    w += ch === " " ? (anton ? 0.2 : 0.28) : anton ? (up ? 0.47 : 0.4) : over ? (up ? 0.7 : 0.56) : up ? 0.6 : 0.47;
  }
  return w * e.size * (e.font === "PermanentMarker" ? 1.08 : 1);
};

// ---------- Trazos y rellenos de una página ----------
const Page: React.FC<{ p: number }> = ({ p }) => {
  const t = useT();
  const els = ELS.filter((e) => pageOf(e) === p);
  return (
    <AbsoluteFill>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        {els.map((e, i) => {
          if (e.k === "fill") {
            const o = interpolate(t, [e.t0, e.t0 + 0.25], [0, e.op ?? 1], clamp);
            if (o <= 0) return null;
            return <polygon key={i} points={e.pts.map((q) => q.join(",")).join(" ")} fill={e.color} opacity={o} />;
          }
          if (e.k === "stroke") {
            if (t < e.t0) return null;
            const L = polyLen(e.pts);
            const k = interpolate(t, [e.t0, e.t0 + e.dur], [0, 1], clamp);
            return (
              <polyline
                key={i}
                points={e.pts.map((q) => q.join(",")).join(" ")}
                fill="none"
                stroke={e.color}
                strokeWidth={e.w}
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeDasharray={L}
                strokeDashoffset={L * (1 - k)}
              />
            );
          }
          return null;
        })}
      </svg>
      {els.map((e, i) => {
        if (e.k !== "text" || t < e.t0) return null;
        const k = interpolate(t, [e.t0, e.t0 + e.dur], [0, 1], clamp);
        const w = textW(e);
        const left = e.anchor === "middle" ? e.x - w / 2 : e.x;
        const kb = interpolate(t, [e.t0, e.t0 + 0.2], [0, 1], clamp);
        return (
          <div key={`t${i}`} style={{ position: "absolute", left: left - 30, top: e.y - e.size * 1.0, width: w + 60, textAlign: "center" }}>
            {e.bg ? (
              <div
                style={{
                  position: "absolute",
                  left: 0,
                  right: 0,
                  top: e.size * 0.08,
                  height: e.size * 1.18,
                  background: e.bg,
                  borderRadius: 18,
                  transform: `rotate(-1.5deg) scaleX(${kb})`,
                  transformOrigin: "left center",
                }}
              />
            ) : null}
            <div
              style={{
                position: "relative",
                fontFamily: e.font,
                fontWeight: e.weight,
                fontSize: e.size,
                lineHeight: 1.25,
                color: e.color,
                whiteSpace: "nowrap",
                clipPath: `inset(-20% ${(1 - k) * 100}% -20% 0)`,
              }}
            >
              {e.txt}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- Hojas con cambio de página deslizando ----------
const Hojas: React.FC = () => {
  const t = useT();
  return (
    <>
      {PAGE_START.map((s, p) => {
        const e = pageEnd(p);
        if (t < s - 0.01 || t > e + SLIDE) return null;
        const out = interpolate(t, [e, e + SLIDE], [0, 1], { ...clamp, easing: EASE });
        const inn = p === 0 ? 1 : interpolate(t, [s, s + SLIDE], [0, 1], { ...clamp, easing: EASE });
        const x = -W * out + W * (1 - inn) * 0.0;
        return (
          <AbsoluteFill key={p} style={{ transform: `translateX(${x}px)`, zIndex: 10 - p, background: PAPER, boxShadow: out > 0 ? "30px 0 60px rgba(0,0,0,.18)" : "none" }}>
            <Papel />
            <Page p={p} />
          </AbsoluteFill>
        );
      })}
    </>
  );
};

const Papel: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(130% 90% at 50% 40%, ${PAPER} 0%, #EEF2F6 100%)`,
    }}
  >
    <AbsoluteFill
      style={{
        backgroundImage: "linear-gradient(rgba(13,30,58,.11) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(13,30,58,.11) 1.5px, transparent 1.5px)",
        backgroundSize: "60px 60px",
        backgroundPosition: "0 0",
      }}
    />
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 150, display: "flex", alignItems: "center", justifyContent: "center", gap: 22, opacity: 0.9 }}>
      <Img src={staticFile("logo-dma-dark.png")} style={{ width: 230 }} />
    </div>
  </AbsoluteFill>
);

// ---------- El marcador ----------
type Ev = { t0: number; t1: number; a: Pt; b: Pt; at: (t: number) => Pt; page: number };
const EVENTS: Ev[] = ELS.filter((e) => e.k !== "fill")
  .map((e): Ev => {
    if (e.k === "stroke") {
      const L = polyLen(e.pts);
      return { t0: e.t0, t1: e.t0 + e.dur, a: e.pts[0], b: e.pts[e.pts.length - 1], at: (t) => pointAt(e.pts, L * Math.min(1, Math.max(0, (t - e.t0) / e.dur))), page: pageOf(e) };
    }
    const te = e as Extract<El, { k: "text" }>;
    const w = textW(te);
    const left = te.anchor === "middle" ? te.x - w / 2 : te.x;
    const y = te.y - te.size * 0.25;
    return {
      t0: te.t0,
      t1: te.t0 + te.dur,
      a: [left, y],
      b: [left + w, y],
      at: (t) => {
        const k = Math.min(1, Math.max(0, (t - te.t0) / te.dur));
        return [left + w * k, y + Math.sin(k * 40) * te.size * 0.12];
      },
      page: pageOf(te),
    };
  })
  .sort((x, y) => x.t0 - y.t0);
const PARK: Pt = [980, 1820];

const penAt = (t: number): { p: Pt; lift: number } => {
  const cur = EVENTS.find((e) => t >= e.t0 && t <= e.t1);
  if (cur) return { p: cur.at(t), lift: 0 };
  const prev = [...EVENTS].reverse().find((e) => e.t1 < t);
  const next = EVENTS.find((e) => e.t0 > t);
  const from: Pt = prev ? prev.b : PARK;
  const t0 = prev ? prev.t1 : 0;
  // si la siguiente acción está lejos (o en otra página), el marcador se aparca
  if (!next || next.t0 - t0 > 1.6 || (prev && next.page !== prev.page)) {
    const tgt: Pt = next && next.t0 - t < 0.5 ? next.a : PARK;
    const s = next && next.t0 - t < 0.5 ? next.t0 - 0.5 : t0;
    const e = next && next.t0 - t < 0.5 ? next.t0 : t0 + 0.5;
    const src: Pt = next && next.t0 - t < 0.5 ? PARK : from;
    const k = interpolate(t, [s, e], [0, 1], { ...clamp, easing: EASE });
    return { p: [src[0] + (tgt[0] - src[0]) * k, src[1] + (tgt[1] - src[1]) * k], lift: 1 };
  }
  const k = interpolate(t, [t0, next.t0], [0, 1], { ...clamp, easing: EASE });
  return { p: [from[0] + (next.a[0] - from[0]) * k, from[1] + (next.a[1] - from[1]) * k], lift: Math.sin(Math.PI * k) };
};

const Marcador: React.FC = () => {
  const t = useT();
  const { p, lift } = penAt(t);
  // en la portada (primer fotograma) no hay marcador: entra después
  const vis = interpolate(t, [0.35, 0.6], [0, 1], clamp);
  if (vis <= 0) return null;
  const dx = 10 * lift;
  const dy = -16 * lift;
  return (
    <svg width={W} height={H} style={{ position: "absolute", inset: 0, zIndex: 50, pointerEvents: "none", overflow: "visible", opacity: vis }}>
      <defs>
        <filter id="sh" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="9" />
        </filter>
        <linearGradient id="body" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#081428" />
          <stop offset="0.45" stopColor="#1E3A60" />
          <stop offset="1" stopColor="#0A1830" />
        </linearGradient>
      </defs>
      {/* sombra */}
      <g transform={`translate(${p[0] + 26 + dx * 2.5},${p[1] + 30 - dy * 1.5}) rotate(35)`} opacity={0.22 - 0.08 * lift} filter="url(#sh)">
        <rect x={-27} y={-470} width={54} height={440} rx={22} fill="#000" />
      </g>
      {/* marcador: punta en (0,0), cuerpo hacia arriba a la derecha */}
      <g transform={`translate(${p[0] + dx},${p[1] + dy}) rotate(35)`}>
        <path d="M -6 -4 L 6 -4 L 9 -26 L -9 -26 Z" fill="#1a1a1a" />
        <path d="M -14 -26 L 14 -26 L 22 -70 L -22 -70 Z" fill="#1E3A60" />
        <rect x={-27} y={-470} width={54} height={402} rx={22} fill="url(#body)" />
        <rect x={-27} y={-300} width={54} height={92} fill={AMBER} />
        <text x={0} y={-238} transform="rotate(-90 0 -254)" textAnchor="middle" fontFamily="Anton" fontWeight={400} fontSize={30} fill={NAVY}>
          DMA
        </text>
        <rect x={-27} y={-470} width={54} height={60} rx={22} fill="#2E4A70" />
        <rect x={-16} y={-455} width={8} height={360} rx={4} fill="rgba(255,255,255,.18)" />
      </g>
    </svg>
  );
};

// ---------- Subtítulos de 1–2 palabras ----------
type Wd = { w: string; s: number; e: number };
const GROUPS = (() => {
  const ws = WORDS as Wd[];
  const out: { txt: string; s: number; e: number }[] = [];
  let i = 0;
  while (i < ws.length) {
    const a = ws[i];
    const b = ws[i + 1];
    const join = b && b.s - a.e < 0.2 && (a.w + b.w).length <= 12 && !/[.,?:!]$/.test(a.w);
    if (join) {
      out.push({ txt: `${a.w} ${b.w}`, s: a.s, e: b.e });
      i += 2;
    } else {
      out.push({ txt: a.w, s: a.s, e: a.e });
      i += 1;
    }
  }
  return out.map((g, k) => ({ ...g, end: Math.min(out[k + 1] ? out[k + 1].s : g.e + 0.35, g.e + 0.45) }));
})();
const Subtitulos: React.FC = () => {
  const t = useT();
  const g = GROUPS.find((x) => t >= x.s - 0.03 && t < x.end);
  if (!g || t < 0.35) return null;
  const k = interpolate(t, [g.s - 0.03, g.s + 0.09], [0, 1], clamp);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1630, textAlign: "center", zIndex: 40 }}>
      <span
        style={{
          display: "inline-block",
          fontFamily: "Anton",
          fontWeight: 400,
          fontSize: 66,
          color: "#FFFFFF",
          background: "#D78631",
          padding: "4px 22px 0",
          borderRadius: 12,
          letterSpacing: 1,
          transform: `scale(${0.85 + 0.15 * k})`,
        }}
      >
        {g.txt.replace(/[.,:]$/, "").toUpperCase()}
      </span>
    </div>
  );
};

const Reel: React.FC = () => (
  <AbsoluteFill style={{ background: "#DDE5EC" }}>
    <Hojas />
    <Subtitulos />
    <Marcador />
    <Audio src={staticFile("mezcla.wav")} />
  </AbsoluteFill>
);

export const MyComposition: React.FC = () => (
  <Composition id="Niveles" component={Reel} durationInFrames={Math.round(TOTAL * FPS)} fps={FPS} width={W} height={H} />
);
