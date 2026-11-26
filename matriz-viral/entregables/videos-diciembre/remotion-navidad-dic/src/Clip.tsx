// Clip de pantalla con voz (shorts del workshop y fragmentos de clase): portada en el fotograma 0, titular fijo arriba,
// la pantalla real en un marco, subtítulos palabra por palabra de la transcripción real y cierre de marca.
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BEBAS, MONT, NAVY, OR, FPS, F, clamp, Bg, Logos, Pop, Flash, fit } from "./brand";
import { CLIPS } from "./clips";

export const PRE = 0.5;
type W = { w: string; s: number; e: number };
export type ClipData = {
  id: string; kind: "short" | "clase"; fin: number; empalmes: number[]; hook: [string, string]; pie: string; words: W[];
  portada: { lines: string[]; accent: number; chip: string }; keys?: string;
};
export const postOf = (d: ClipData) => (d.kind === "clase" ? 4.0 : 1.8);
export const clipDuration = (id: string) => { const d = CLIPS[id]; return Math.round((PRE + d.fin + postOf(d)) * FPS); };

const KICKER = { short: "WORKSHOP · IA CONECTADA A REVIT", clase: "PROMO DE NAVIDAD · CLASE REAL" };
const KEY = /\d|^(IA|BIM|MCP|GPT|EJE|XZ|X|Z|SAFE|MIL|SAP2000)$|REVIT|CHATGPT|CLAUDE|PROMPT|MUROS|PUERTAS|NIVELES|CRITERIO|MAGIA|PLUGIN|CONECT|FILTRO|ZAPATA|PÓRTICO|ESPECÍFIC|ERROR|MANUAL|CUALQUIER|CAPTURAS|PROFESIONAL|NONICA|MANAGER|SENCILLO|VERDAD/;
const clean = (w: string) => w.replace(/^[¿¡"(]+|[?!.,;:…")]+$/g, "").toUpperCase();

export const pagesOf = (words: W[]) => {
  const out: { t: string[]; s: number; e: number }[] = []; let cur: W[] = [];
  words.forEach((w, i) => { cur.push(w); const nx = words[i + 1]; const txt = cur.map((x) => clean(x.w)).join(" ");
    const brk = !nx || /[.,?!:;…]$/.test(w.w) || cur.length >= 3 || nx.s - w.e > 0.32 || txt.length + clean(nx.w).length > 15 || txt.length >= 11;
    if (brk) { out.push({ t: cur.map((x) => clean(x.w)).filter(Boolean), s: cur[0].s, e: nx ? Math.min(nx.s, w.e + 0.55) : w.e + 0.35 }); cur = []; } });
  return out.filter((p) => p.t.length);
};

// ---------- portada (fotograma 0 del video y JPG de miniatura) ----------
export const Portada: React.FC<{ id: string }> = ({ id }) => {
  const d = CLIPS[id]; const L = d.portada.lines; const size = fit(L, 950, 215); const lh = 0.93;
  const top = 505; const cardTop = top + L.length * size * lh + 46; const cardH = Math.min(690, 1568 - cardTop);
  return (
    <AbsoluteFill>
      <Bg />
      <Logos y={300} h={92} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 438, textAlign: "center", fontFamily: MONT, fontWeight: 800, fontSize: 30, letterSpacing: 6, color: OR }}>{KICKER[d.kind]}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top, textAlign: "center", fontFamily: BEBAS, fontSize: size, lineHeight: lh, color: "#fff", letterSpacing: 1, textShadow: "0 8px 0 rgba(0,0,0,.25)" }}>
        {L.map((l, i) => <div key={i} style={{ color: i >= d.portada.accent ? OR : "#fff", whiteSpace: "nowrap" }}>{l}</div>)}</div>
      <div style={{ position: "absolute", left: 70, width: 940, top: cardTop, height: cardH, borderRadius: 26, overflow: "hidden", border: `7px solid ${OR}`, boxShadow: "0 34px 80px rgba(0,0,0,.55)", transform: "rotate(-1.6deg)", background: "#fff" }}>
        <Img src={staticFile(`clip/${id}-cover.jpg`)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 30%" }} /></div>
      <div style={{ position: "absolute", left: 96, top: cardTop + cardH - 44, background: NAVY, color: "#fff", border: `4px solid ${OR}`, borderRadius: 999, padding: "12px 30px 6px", fontFamily: BEBAS, fontSize: 52, lineHeight: 1, letterSpacing: 1, boxShadow: "0 12px 30px rgba(0,0,0,.45)", transform: "rotate(-1.6deg)" }}>{d.portada.chip}</div>
    </AbsoluteFill>
  );
};

const Subs: React.FC<{ d: ClipData; t: number }> = ({ d, t }) => {
  const pages = React.useMemo(() => pagesOf(d.words), [d]);
  const g = pages.find((x) => t >= x.s - 0.05 && t < x.e); if (!g) return null;
  const k = interpolate(t - g.s, [-0.05, 0.1], [0.8, 1], clamp);
  const size = g.t.join(" ").length > 13 ? 88 : 100;
  return (<div style={{ position: "absolute", top: 1300, left: 0, right: 0, height: 120, display: "flex", justifyContent: "center", alignItems: "center", gap: 18, transform: `scale(${k})` }}>
    {g.t.map((w, i) => { const key = KEY.test(w); return (<span key={i} style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 1, padding: key ? "10px 18px 0" : 0, background: key ? OR : "transparent", color: "#fff", borderRadius: 10, WebkitTextStroke: key ? "0" : `3px ${NAVY}`, paintOrder: "stroke fill", textShadow: "0 6px 18px rgba(0,0,0,.45)", whiteSpace: "nowrap" }}>{w}</span>); })}
  </div>);
};

const Cierre: React.FC<{ d: ClipData }> = ({ d }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const k = spring({ frame: f - 10, fps, config: { damping: 10 } }); const pulse = 1 + 0.03 * Math.sin(f / 5);
  if (d.kind === "short") return (<AbsoluteFill><Bg />
    <Pop at={2} style={{ position: "absolute", left: 0, right: 0, top: 760 }}><Logos y={0} h={128} /></Pop>
    <Pop at={8} style={{ position: "absolute", left: 0, right: 0, top: 960, textAlign: "center", fontFamily: MONT, fontWeight: 800, fontSize: 32, letterSpacing: 6, color: OR }}>{KICKER.short}</Pop>
  </AbsoluteFill>);
  return (<AbsoluteFill><Bg />
    <Pop at={2} style={{ position: "absolute", left: 0, right: 0, top: 300 }}><Logos y={0} h={92} /></Pop>
    <Pop at={5} style={{ position: "absolute", left: 60, right: 60, top: 470, textAlign: "center" }}>
      <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 30, letterSpacing: 6, color: OR, marginBottom: 14 }}>PROMO DE NAVIDAD</div>
      <div style={{ fontFamily: BEBAS, fontSize: 118, lineHeight: 0.93, color: "#fff", whiteSpace: "nowrap" }}>ESTE CURSO Y 39 MÁS<div style={{ color: OR, fontSize: 250 }}>A $46.50</div></div>
      <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 38, color: "#fff", marginTop: 18 }}>Antes $154.99 · 70 % OFF</div></Pop>
    <div style={{ position: "absolute", left: 40, right: 40, top: 1010, display: "flex", justifyContent: "center", transform: `scale(${(0.8 + 0.2 * k) * pulse})`, opacity: Math.min(1, k * 1.5) }}>
      <div style={{ background: OR, borderRadius: 999, padding: "34px 52px 22px", fontFamily: BEBAS, fontSize: 118, lineHeight: 1, color: "#fff", border: "5px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.45)", letterSpacing: 2, whiteSpace: "nowrap" }}>COMENTA NAVIDAD</div></div>
    <Pop at={20} style={{ position: "absolute", left: 50, right: 50, top: 1250, textAlign: "center" }}>
      <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 36, letterSpacing: 1, color: "#fff" }}>HASTA EL MARTES 5 DE ENERO · 23:59</div>
      <div style={{ fontFamily: MONT, fontWeight: 700, fontSize: 30, color: "#B9C6DA", marginTop: 10 }}>Hora de Ecuador · Certificado de Design Modeling DG S.A.S.</div></Pop>
  </AbsoluteFill>);
};

export const Clip: React.FC<{ id: string }> = ({ id }) => {
  const d = CLIPS[id]; const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / FPS - PRE;
  const hs = fit(d.hook, 960, 108);
  // cambio de encuadre en cada pausa recortada (disimula el salto) + empuje lento
  const n = d.empalmes.filter((x) => x <= t).length; const last = n ? d.empalmes[n - 1] : -9;
  const tgt = n % 2 ? 1.035 : 1.0; const prev = n % 2 ? 1.0 : 1.035;
  const z = (n ? interpolate(t - last, [0, 0.12], [prev, tgt], clamp) : 1.0) + 0.02 * interpolate(t, [0, d.fin], [0, 1], clamp);
  const out = interpolate(f, [F(PRE) - 2, F(PRE) + 7], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: NAVY }}>
      <Bg />
      <Logos y={132} h={64} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 226, textAlign: "center", fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: 5, color: OR }}>{KICKER[d.kind]}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 268, height: 220, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center", fontFamily: BEBAS, fontSize: hs, lineHeight: 0.96, color: "#fff", letterSpacing: 1 }}>
        <div style={{ whiteSpace: "nowrap" }}>{d.hook[0]}</div><div style={{ color: OR, whiteSpace: "nowrap" }}>{d.hook[1]}</div></div>
      <div style={{ position: "absolute", left: 36, top: 496, width: 1008, height: 768, borderRadius: 16, overflow: "hidden", border: `4px solid ${OR}`, boxShadow: "0 24px 60px rgba(0,0,0,.45)", background: d.kind === "clase" ? "#fff" : NAVY, boxSizing: "border-box" }}>
        <Sequence from={F(PRE)} durationInFrames={F(d.fin) + 2} layout="none">
          <OffthreadVideo src={staticFile(`clip/${id}.mp4`)} muted style={{ width: 1000, height: 760, transform: `scale(${z})`, transformOrigin: "50% 45%" }} />
        </Sequence>
        {t < 0 && <Img src={staticFile(`clip/${id}-f0.jpg`)} style={{ position: "absolute", left: 0, top: 0, width: 1000, height: 760 }} />}
      </div>
      <Subs d={d} t={t} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 1440, textAlign: "center" }}>
        <span style={{ display: "inline-block", background: "rgba(13,30,58,.92)", border: `3px solid ${OR}`, color: "#fff", fontFamily: MONT, fontWeight: 800, fontSize: d.pie.length > 48 ? 26 : 32, padding: "12px 26px", borderRadius: 999 }}>{d.pie}</span></div>
      {f < F(PRE) + 8 && <AbsoluteFill style={{ transform: `translateY(${-out * 1920}px)`, filter: out > 0.02 ? `blur(${Math.sin(out * Math.PI) * 14}px)` : undefined }}><Portada id={id} /></AbsoluteFill>}
      <Flash at={F(PRE) + 3} />
      <Sequence from={F(PRE + d.fin)}><Cierre d={d} /></Sequence>
    </AbsoluteFill>
  );
};
