// Pizarra dibujada (estilo 9 de la casa) con las letras de marca: trazos navy con temblor de mano que se dibujan solos,
// rellenos que aparecen al cerrar el contorno y textos que se escriben. Adaptado de reel-valor/src/kit.tsx.
// Todos los tiempos (t0) van en segundos desde el inicio de la escena; con t0 <= 0 el elemento ya está dibujado (portada).
import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { BEBAS, MONT } from "../brand";

export const INK = "#0D1E3A";
export const GREY = "#5A6475";
export const RED = "#E5252A";
export const COPPER = "#D78631";
export const ORANGE = "#E8893A";
export const SOIL = "#E9B47E";
export const CON = "#DCE4EC";
export const CON_D = "#B9C7D4";
export const BLUE = "#004A70";
export const PAPER = "#FAFBFC";
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
export const useT = () => useCurrentFrame() / 30;
export const p = (t: number, t0: number, d = 0.3, e: (n: number) => number = EASE) =>
  interpolate(t, [t0, t0 + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const rnd = (seed: number) => { const x = Math.sin(seed * 9301 + 49297) * 233280; return x - Math.floor(x); };
export type Pt = [number, number];
export const hand = (pts: Pt[], seed = 1, j = 2.4): string => {
  let d = `M${pts[0][0]},${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) {
    const [x0, y0] = pts[i - 1]; const [x1, y1] = pts[i];
    const mx = (x0 + x1) / 2 + (rnd(seed + i) - 0.5) * j * 2; const my = (y0 + y1) / 2 + (rnd(seed + i * 7) - 0.5) * j * 2;
    d += ` Q${mx.toFixed(1)},${my.toFixed(1)} ${x1},${y1}`;
  }
  return d;
};
export const rect = (x: number, y: number, w: number, h: number, seed = 1) => hand([[x, y], [x + w, y + 1], [x + w - 1, y + h], [x + 1, y + h - 1], [x, y - 3]], seed, 2.2);
export const loop = (cx: number, cy: number, rx: number, ry: number, seed = 1): string => {
  const pts: Pt[] = [];
  for (let i = 0; i <= 26; i++) { const a = -0.5 + (i / 24) * Math.PI * 2; const k = 1 + (rnd(seed + i) - 0.5) * 0.06 + i * 0.004; pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); }
  return hand(pts, seed, 1.6);
};
export const Tr: React.FC<{ d: string; t0: number; dur?: number; color?: string; w?: number; fill?: string; fo?: number; dash?: string }> = ({ d, t0, dur = 0.3, color = INK, w = 6, fill = "none", fo = 1, dash }) => {
  const t = useT(); const k = p(t, t0, dur, Easing.inOut(Easing.quad));
  if (k <= 0) return null;
  if (dash) return <path d={d} stroke={color} strokeWidth={w} fill="none" strokeLinecap="round" strokeDasharray={dash} opacity={k} />;
  return <path d={d} pathLength={1} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill={fill} fillOpacity={fill === "none" ? 0 : k * fo} strokeDasharray={1} strokeDashoffset={1 - k} />;
};
export const Ln: React.FC<{ a: Pt; b: Pt; t0: number; color?: string; w?: number; dur?: number; seed?: number; dash?: string }> = ({ a, b, t0, color, w = 6, dur = 0.2, seed = 9, dash }) => <Tr d={hand([a, b], seed, 1.6)} t0={t0} dur={dur} color={color} w={w} dash={dash} />;
export const Caja: React.FC<{ x: number; y: number; w: number; h: number; t0: number; color?: string; sw?: number; fill?: string; fo?: number; seed?: number; dur?: number }> = ({ x, y, w, h, t0, color, sw = 6, fill, fo, seed = 3, dur = 0.35 }) => <Tr d={rect(x, y, w, h, seed)} t0={t0} dur={dur} color={color} w={sw} fill={fill} fo={fo} />;
export const Poli: React.FC<{ pts: Pt[]; t0: number; fill: string; op?: number; dur?: number }> = ({ pts, t0, fill, op = 1, dur = 0.25 }) => {
  const t = useT(); const k = p(t, t0, dur); if (k <= 0) return null;
  return <polygon points={pts.map((q) => q.join(",")).join(" ")} fill={fill} opacity={k * op} />;
};
export const Circ: React.FC<{ cx: number; cy: number; rx: number; ry: number; t0: number; seed?: number; color?: string; w?: number; dur?: number }> = ({ cx, cy, rx, ry, t0, seed = 3, color = RED, w = 8, dur = 0.34 }) => <Tr d={loop(cx, cy, rx, ry, seed)} t0={t0} dur={dur} color={color} w={w} />;
export const Equis: React.FC<{ cx: number; cy: number; r?: number; t0: number; w?: number }> = ({ cx, cy, r = 28, t0, w = 10 }) => (<g>
  <Ln a={[cx - r, cy - r]} b={[cx + r, cy + r]} t0={t0} dur={0.1} color={RED} w={w} seed={41} /><Ln a={[cx + r, cy - r]} b={[cx - r, cy + r]} t0={t0 + 0.08} dur={0.1} color={RED} w={w} seed={42} /></g>);
export const Visto: React.FC<{ cx: number; cy: number; r?: number; t0: number; color?: string; w?: number }> = ({ cx, cy, r = 30, t0, color = COPPER, w = 11 }) => <Tr d={hand([[cx - r, cy], [cx - r * 0.3, cy + r * 0.7], [cx + r, cy - r * 0.8]], 51, 1)} t0={t0} dur={0.16} color={color} w={w} />;
export const Flecha: React.FC<{ a: Pt; b: Pt; t0: number; color?: string; w?: number; head?: number; dur?: number }> = ({ a, b, t0, color = INK, w = 7, head = 22, dur = 0.2 }) => {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  const h1: Pt = [b[0] - head * Math.cos(ang - 0.5), b[1] - head * Math.sin(ang - 0.5)]; const h2: Pt = [b[0] - head * Math.cos(ang + 0.5), b[1] - head * Math.sin(ang + 0.5)];
  return (<g><Ln a={a} b={b} t0={t0} color={color} w={w} seed={61} dur={dur} /><Tr d={`M${h1[0]},${h1[1]} L${b[0]},${b[1]} L${h2[0]},${h2[1]}`} t0={t0 + dur * 0.8} dur={0.08} color={color} w={w} /></g>);
};
// cota: línea con topes en los extremos (el texto se pone aparte con <Tx>)
export const Cota: React.FC<{ a: Pt; b: Pt; t0: number; color?: string; w?: number; tick?: number }> = ({ a, b, t0, color = GREY, w = 4, tick = 14 }) => {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]); const nx = -Math.sin(ang) * tick; const ny = Math.cos(ang) * tick;
  return (<g><Ln a={a} b={b} t0={t0} color={color} w={w} seed={71} /><Ln a={[a[0] - nx, a[1] - ny]} b={[a[0] + nx, a[1] + ny]} t0={t0 + 0.12} dur={0.08} color={color} w={w} seed={72} />
    <Ln a={[b[0] - nx, b[1] - ny]} b={[b[0] + nx, b[1] + ny]} t0={t0 + 0.16} dur={0.08} color={color} w={w} seed={73} /></g>);
};
// rayado de terreno
export const Rayado: React.FC<{ x0: number; x1: number; y: number; h?: number; step?: number; t0: number; color?: string; w?: number }> = ({ x0, x1, y, h = 26, step = 22, t0, color = INK, w = 3 }) => {
  const pts: Pt[] = []; for (let x = x0; x <= x1; x += step) pts.push([x, y], [x - h * 0.6, y + h]);
  return <Tr d={"M" + pts.map((q) => q.join(",")).join(" L")} t0={t0} dur={0.4} color={color} w={w} />;
};
export const Svg: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute", inset: 0, overflow: "visible", ...style }}>{children}</svg>;
// texto que se escribe de izquierda a derecha. font h = Bebas Neue (títulos, cifras), b = Montserrat 800 (etiquetas)
export const Tx: React.FC<{ text: React.ReactNode; x: number; y: number; t0: number; size?: number; color?: string; align?: "left" | "center" | "right"; w?: number; font?: "h" | "b" | "f"; rot?: number; bg?: string; fg?: string; ls?: number; wt?: number; len?: number }> = ({ text, x, y, t0, size = 52, color = INK, align = "left", w = 1080, font = "b", rot = 0, bg, ls, wt, len }) => {
  const t = useT(); const n = len ?? (typeof text === "string" ? text.length : 12);
  const k = p(t, t0, Math.min(0.5, 0.1 + n * 0.028), Easing.linear);
  if (k <= 0) return null;
  const st: React.CSSProperties = { display: "inline-block", fontFamily: `${font === "h" ? BEBAS : MONT}, "DejaVu Sans"`, fontWeight: font === "h" ? 400 : wt ?? (font === "f" ? 900 : 800), fontSize: size, color, lineHeight: 1.04, whiteSpace: "nowrap",
    background: bg, padding: bg ? "8px 22px 2px" : undefined, borderRadius: bg ? 10 : undefined, letterSpacing: ls ?? (font === "h" ? 1 : -0.3), clipPath: `inset(-25% ${(1 - k) * 100}% -25% -3%)`, transform: `rotate(${rot}deg)` };
  return (<div style={{ position: "absolute", left: align === "left" ? x : align === "center" ? x - w / 2 : x - w, top: y, width: align === "left" ? undefined : w, textAlign: align }}><span style={st}>{typeof text === "string" && font === "h" ? un(text) : text}</span></div>);
};
// Bebas Neue no tiene minúsculas: las unidades (kg/cm², m, t, mm, km) van en Montserrat para que no salgan como «KG/CM²» o «M»
export const un = (s: string): React.ReactNode => s.split(/(kg\/cm²|mm|km|(?<=\d )m\b|(?<=\d )t\b)/g).map((x, i) => (i % 2 ? <span key={i} style={{ fontFamily: MONT, fontWeight: 900, fontSize: "0.6em", letterSpacing: 0 }}>{x}</span> : x));
// sello que cae con golpe
export const Sello: React.FC<{ text: string; x: number; y: number; t0: number; size?: number; color?: string; rot?: number; w?: number; bg?: string }> = ({ text, x, y, t0, size = 110, color = RED, rot = -6, w = 1080, bg = "rgba(250,251,252,.92)" }) => {
  const t = useT(); const k = p(t, t0, 0.18, Easing.out(Easing.back(2.2)));
  if (t < t0) return null;
  return (<div style={{ position: "absolute", left: x - w / 2, top: y, width: w, textAlign: "center" }}>
    <span style={{ display: "inline-block", fontFamily: BEBAS, fontSize: size, lineHeight: 1, color, padding: "12px 28px 2px", border: `8px solid ${color}`, borderRadius: 14, whiteSpace: "nowrap", background: bg,
      transform: `rotate(${rot}deg) scale(${interpolate(k, [0, 1], [1.7, 1])})`, opacity: Math.min(1, k * 2) }}>{text}</span></div>);
};
// aparece con un pequeño salto (para grupos HTML)
export const Sale: React.FC<{ t0: number; children: React.ReactNode; style?: React.CSSProperties; dy?: number }> = ({ t0, children, style, dy = 24 }) => {
  const t = useT(); const k = p(t, t0, 0.3, Easing.out(Easing.back(1.6))); if (t < t0) return null;
  return <div style={{ opacity: Math.min(1, k * 1.6), transform: `translateY(${(1 - k) * dy}px) scale(${0.92 + 0.08 * k})`, ...style }}>{children}</div>;
};
