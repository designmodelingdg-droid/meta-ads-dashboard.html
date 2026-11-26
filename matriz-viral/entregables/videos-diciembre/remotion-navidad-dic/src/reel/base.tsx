// Base de los reels animados: línea de tiempo (anclada a la voz cuando existe), subtítulo palabra por palabra en caja cobre,
// hojas de papel que se deslizan, encabezado con logos y cierre de pregunta en azul marino.
import React from "react";
import { AbsoluteFill, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BEBAS, MONT, NAVY, OR, CU, FPS, F, clamp, Bg, Logos, Pop } from "../brand";
import { PAPER, GREY } from "./pz";

export type Tiempos = { id: string; voz: boolean; escenas: { s: number; dur: number }[]; palabras: { w: string; s: number; e: number }[]; total: number };
export const frames = (T: Tiempos) => Math.round(T.total * FPS);
// instante (s, local a la escena i) en que la voz dice la primera palabra que cumple `re`; si no aparece, fracción `fb` de la escena
export const cuando = (T: Tiempos, i: number, re: RegExp, fb: number) => { const e = T.escenas[i]; const w = T.palabras.find((q) => q.s >= e.s - 0.01 && q.s < e.s + e.dur && re.test(q.w));
  return w ? w.s - (i ? e.s : 0) : fb * e.dur; };
const limpia = (w: string) => w.replace(/^[¿¡"«(]+|[?!.,;:…"»)]+$/g, "").toUpperCase();

export const Subs: React.FC<{ T: Tiempos; y?: number; oscuro?: boolean }> = ({ T, y = 1396 }) => {
  const f = useCurrentFrame(); const t = f / FPS;
  const pages = React.useMemo(() => { const out: { t: string[]; s: number; e: number }[] = []; let cur: Tiempos["palabras"] = [];
    T.palabras.forEach((w, i) => { cur.push(w); const nx = T.palabras[i + 1]; const txt = cur.map((x) => limpia(x.w)).join(" ");
      if (!nx || /[.,?!:;…]$/.test(w.w) || cur.length >= 3 || nx.s - w.e > 0.3 || txt.length + limpia(nx.w).length > 16 || txt.length >= 12) {
        out.push({ t: cur.map((x) => limpia(x.w)).filter(Boolean), s: cur[0].s, e: nx ? Math.min(nx.s, w.e + 0.5) : w.e + 0.4 }); cur = []; } });
    return out.filter((p) => p.t.length); }, [T]);
  const g = pages.find((x) => t >= x.s - 0.04 && t < x.e); if (!g) return null;
  const k = interpolate(t - g.s, [-0.04, 0.09], [0.82, 1], clamp);
  return (<div style={{ position: "absolute", top: y, left: 0, right: 0, height: 118, display: "flex", justifyContent: "center", alignItems: "center", transform: `scale(${k})`, zIndex: 50 }}>
    <span style={{ fontFamily: BEBAS, fontSize: 88, lineHeight: 1, color: "#fff", background: CU, borderRadius: 12, padding: "14px 30px 4px", whiteSpace: "nowrap", letterSpacing: 1, boxShadow: "0 10px 26px rgba(13,30,58,.35)" }}>{g.t.join(" ")}</span></div>);
};

// Hoja de papel con cuadrícula de 60 px; cada escena nueva entra deslizándose sobre la anterior
export const Hoja: React.FC<{ first?: boolean; n?: string; children: React.ReactNode }> = ({ first, n, children }) => {
  const f = useCurrentFrame();
  const k = first ? 1 : interpolate(f, [0, 10], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.55, 1) });
  return (<AbsoluteFill style={{ transform: `translateX(${(1 - k) * 1080}px)`, background: PAPER, boxShadow: k < 1 ? "-30px 0 60px rgba(0,0,0,.22)" : "none", overflow: "hidden" }}>
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      {Array.from({ length: 19 }).map((_, i) => <line key={`v${i}`} x1={i * 60} y1={0} x2={i * 60} y2={1920} stroke="#E3E9F0" strokeWidth={1.5} />)}
      {Array.from({ length: 33 }).map((_, i) => <line key={`h${i}`} x1={0} y1={i * 60} x2={1080} y2={i * 60} stroke="#E3E9F0" strokeWidth={1.5} />)}</svg>
    <div style={{ position: "absolute", left: 0, right: 0, top: 128, display: "flex", justifyContent: "center", alignItems: "center", gap: 24 }}>
      <Img src={staticFile("logo-dark.png")} style={{ height: 62 }} /><div style={{ width: 2, height: 50, background: "rgba(13,30,58,.3)" }} /><Img src={staticFile("marcas/atc-blk.png")} style={{ height: 46 }} /></div>
    {n && <div style={{ position: "absolute", left: 0, right: 0, top: 214, textAlign: "center", fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: 6, color: GREY }}>{n}</div>}
    {children}
  </AbsoluteFill>);
};

// Cierre en azul marino: pregunta, opciones numeradas y «Comenta PALABRA»
export const Cierre: React.FC<{ titulo: React.ReactNode; opciones?: [string, string][]; pie?: string; boton: string; segunda?: string; fondo?: React.ReactNode; fila?: boolean }> = ({ titulo, opciones = [], pie, boton, segunda, fondo, fila }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const inn = interpolate(f, [0, 10], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.55, 1) });
  const k = spring({ frame: f - 30, fps, config: { damping: 10 } }); const pulse = 1 + 0.03 * Math.sin(f / 5);
  const yb = fila ? 1010 : 800 + opciones.length * 128 + (pie ? 70 : 0);
  return (<AbsoluteFill style={{ transform: `translateX(${(1 - inn) * 1080}px)`, overflow: "hidden" }}>
    <Bg />
    {fondo && <AbsoluteFill style={{ opacity: 0.13 }}>{fondo}</AbsoluteFill>}
    <Logos y={262} h={84} />
    <Pop at={6} style={{ position: "absolute", left: 50, right: 50, top: 420, textAlign: "center" }}><div style={{ fontFamily: BEBAS, fontSize: 132, lineHeight: 0.94, color: "#fff", letterSpacing: 1 }}>{titulo}</div></Pop>
    {!fila && <div style={{ position: "absolute", left: 70, right: 70, top: 730, display: "flex", flexDirection: "column", gap: 20 }}>
      {opciones.map(([n, t], i) => { const s = spring({ frame: f - 16 - i * 8, fps, config: { damping: 13 } });
        return <div key={i} style={{ display: "flex", alignItems: "center", gap: 26, background: "#fff", borderRadius: 26, padding: "16px 30px", opacity: Math.min(1, s * 1.5), transform: `translateX(${(1 - s) * -40}px)`, boxShadow: "0 18px 40px rgba(0,0,0,.4)", borderLeft: `14px solid ${OR}` }}>
          <div style={{ fontFamily: BEBAS, fontSize: 104, lineHeight: 0.9, color: OR, width: 70, textAlign: "center", paddingTop: 8 }}>{n}</div>
          <div style={{ fontFamily: MONT, fontWeight: 900, fontSize: 40, color: "#0F1E33", lineHeight: 1.12 }}>{t}</div></div>; })}
    </div>}
    {fila && <div style={{ position: "absolute", left: 50, right: 50, top: 730, display: "flex", justifyContent: "center", gap: 22 }}>
      {opciones.map(([n, t], i) => { const s = spring({ frame: f - 16 - i * 7, fps, config: { damping: 12 } });
        return <div key={i} style={{ background: "#fff", borderRadius: 26, padding: "18px 10px 14px", width: t ? 300 : opciones.length > 4 ? 142 : 200, textAlign: "center", opacity: Math.min(1, s * 1.5), transform: `scale(${0.7 + 0.3 * s})`, boxShadow: "0 18px 40px rgba(0,0,0,.4)", borderBottom: `12px solid ${OR}` }}>
          <div style={{ fontFamily: BEBAS, fontSize: t ? 96 : opciones.length > 4 ? 118 : 150, lineHeight: 0.92, color: OR }}>{n}</div>
          {t && <div style={{ fontFamily: MONT, fontWeight: 900, fontSize: 27, color: "#0F1E33", lineHeight: 1.12, marginTop: 4 }}>{t}</div>}</div>; })}
    </div>}
    {pie && <Pop at={34} style={{ position: "absolute", left: 0, right: 0, top: yb - 78, textAlign: "center" }}><div style={{ fontFamily: MONT, fontWeight: 900, fontSize: 42, letterSpacing: 5, color: "#fff" }}>{pie}</div></Pop>}
    <div style={{ position: "absolute", left: 40, right: 40, top: yb + 6, display: "flex", justifyContent: "center", transform: `scale(${(0.8 + 0.2 * k) * pulse})`, opacity: Math.min(1, k * 1.5) }}>
      <div style={{ background: OR, borderRadius: 999, padding: "32px 50px 20px", fontFamily: BEBAS, fontSize: 112, lineHeight: 1, color: "#fff", border: "5px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.45)", letterSpacing: 2, whiteSpace: "nowrap" }}>{boton}</div></div>
    {segunda && <Pop at={48} style={{ position: "absolute", left: 50, right: 50, top: yb + 196, textAlign: "center" }}><div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 31, lineHeight: 1.3, color: "#B9C6DA" }}>{segunda}</div></Pop>}
  </AbsoluteFill>);
};

// Monta las escenas: cada una en su <Sequence>, que dura hasta que la siguiente termina de entrar
export const Escenas: React.FC<{ T: Tiempos; children: React.ReactNode[] }> = ({ T, children }) => (<>
  {T.escenas.map((e, i) => <Sequence key={i} from={F(e.s) - (i ? 0 : F(e.s))} durationInFrames={F(e.dur) + (i ? 0 : F(e.s)) + (i === T.escenas.length - 1 ? 90 : 14)}>{children[i]}</Sequence>)}
</>);
