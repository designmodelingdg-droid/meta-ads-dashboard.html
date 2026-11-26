// Reels de la promo de Navidad «Los jefes se fueron de vacaciones».
// Gancho con las tomas (sin rostros) + explicación de la promo con las escenas de historias-dma/Promo.tsx.
// Los cortes caen en el compás de musica_energica.py (1 compás = 1,75 s).
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BEBAS, MONT, NAVY, NAVY2, OR, INK, RED, FPS, F, clamp, Bg, Logos, Pop, card, Chrome, Chip, BoxLine, Flash } from "./brand";

export const INTRO = 0.5;      // subida de la música sobre la portada (fotograma 0)
export const BAR = 1.75;
export const COLA = 2.0;

type Line = { t: string; kind?: "navy" | "or" | "plain"; at?: number; size?: number };
type Item = { t: string; tag?: string };
export type Scene = {
  bars: number; say: string;
  type: "clip" | "cal" | "price" | "list" | "deadline" | "cta";
  kicker?: string; title?: string; accent?: string;
  // clip
  src?: string; logo?: boolean; rate?: number; from?: number; z?: [number, number]; origin?: string; punch?: number[];
  top?: { y: number; kicker?: string; chrome?: [string, string?]; size?: number; lines?: Line[] };
  low?: { y: number; kicker?: string; lines: Line[] }[];
  chips?: { t: string; at: number; x: number; y: number; dark?: boolean }[];
  stamp?: { t: string; at: number; y: number };
  // tarjetas
  items?: Item[]; small?: string; big?: string; foot?: string; button?: string;
};
export type NavProps = { scenes: Scene[]; bg?: string };

export const timeline = (p: NavProps) => {
  let t = 0;
  return p.scenes.map((sc, i) => { const s = t; const e = s + sc.bars * BAR + (i === 0 ? INTRO : 0) + (i === p.scenes.length - 1 ? COLA : 0); t = e; return { ...sc, s, e }; });
};
export const navDuration = (p: NavProps) => Math.round(timeline(p).slice(-1)[0].e * FPS);

const Title: React.FC<{ sc: Scene; size?: number; top?: number }> = ({ sc, size = 112, top = 370 }) => (
  <div style={{ position: "absolute", left: 60, right: 60, top }}>
    {sc.kicker && <Pop at={2}><div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: 5, color: OR, marginBottom: 14 }}>{sc.kicker}</div></Pop>}
    <Pop at={5}><div style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 0.93, color: "#fff", letterSpacing: 1 }}>
      {sc.title} {sc.accent && <span style={{ color: OR, display: ((sc.title ?? "") + sc.accent).length > 18 ? "block" : "inline" }}>{sc.accent}</span>}</div></Pop>
  </div>
);

// ---------- toma a pantalla completa con texto de marca ----------
const ClipScene: React.FC<{ sc: Scene & { s: number; e: number }; first: boolean }> = ({ sc, first }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps; const dur = sc.e - sc.s;
  const [z0, z1] = sc.z ?? [1.0, 1.08];
  let scale = interpolate(t, [0, dur], [z0, z1], clamp);
  for (const p of sc.punch ?? []) {
    const k = spring({ frame: f - F(p), fps, config: { damping: 14, stiffness: 260 } });
    scale += 0.06 * k * interpolate(t, [p + 0.3, p + 0.85], [1, 0], clamp);
  }
  const whip = first ? 0 : interpolate(f, [0, 7], [1, 0], clamp);
  const pre = (at?: number) => (first && (at ?? 0) <= 0 ? -30 : F(at ?? 0) + (first ? 0 : 4));
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `translateX(${whip * 160}px) scale(${scale + whip * 0.12})`, transformOrigin: sc.origin ?? "50% 60%", filter: whip > 0.02 ? `blur(${whip * 16}px)` : undefined }}>
        {sc.src!.endsWith(".mp4")
          ? <OffthreadVideo src={staticFile(sc.src!)} muted playbackRate={sc.rate ?? 1} startFrom={Math.round((sc.from ?? 0) * 30)} style={{ width: 1080, height: 1920, objectFit: "cover" }} />
          : <Img src={staticFile(sc.src!)} style={{ width: 1080, height: 1920, objectFit: "cover" }} />}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(13,30,58,.62) 0%, rgba(13,30,58,.22) 24%, rgba(13,30,58,0) 34%)" }} />
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(13,30,58,.78) 0%, rgba(13,30,58,.42) 22%, rgba(13,30,58,0) 40%)" }} />
      {sc.logo !== false && <div style={{ position: "absolute", top: 118, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{ background: "rgba(13,30,58,.9)", borderRadius: 999, padding: "10px 30px 8px", border: "2px solid rgba(232,137,58,.7)" }}><Img src={staticFile("logo-claro.png")} style={{ height: 54, display: "block" }} /></div>
      </div>}
      {sc.top && <div style={{ position: "absolute", top: sc.top.y, left: 30, right: 30 }}>
        {sc.top.kicker && <Pop at={pre(0)} style={{ textAlign: "center", marginBottom: 12 }}><span style={{ fontFamily: MONT, fontWeight: 900, fontSize: 34, letterSpacing: 6, color: "#fff", background: OR, borderRadius: 999, padding: "8px 26px" }}>{sc.top.kicker}</span></Pop>}
        {sc.top.chrome && <><Chrome text={sc.top.chrome[0]} size={sc.top.size ?? 130} at={pre(0)} />
          {sc.top.chrome[1] && <><div style={{ height: 4 }} /><Chrome text={sc.top.chrome[1]} size={(sc.top.size ?? 130) * 1.28} at={pre(0) + (first ? 0 : 6)} copper /></>}</>}
        {sc.top.lines && <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>{sc.top.lines.map((l, i) => <BoxLine key={i} text={l.t} kind={l.kind} size={l.size} at={pre(l.at)} />)}</div>}
      </div>}
      {(sc.low ?? []).map((g, gi) => { const a = Math.min(...g.lines.map((l) => l.at ?? 0)); const nx = sc.low![gi + 1]; const b = nx ? Math.min(...nx.lines.map((l) => l.at ?? 0)) : 99;
        if (t < a - 0.01 && !(first && a <= 0) || t >= b) return null;
        return <div key={gi} style={{ position: "absolute", top: g.y, left: 30, right: 30, display: "flex", flexDirection: "column", gap: 12 }}>
          {g.kicker && <Pop at={pre(a)} style={{ textAlign: "center" }}><span style={{ fontFamily: MONT, fontWeight: 900, fontSize: 36, letterSpacing: 6, color: "#fff", background: OR, borderRadius: 999, padding: "8px 28px", border: "3px solid #fff" }}>{g.kicker}</span></Pop>}
          {g.lines.map((l, i) => <BoxLine key={i} text={l.t} kind={l.kind} size={l.size} at={pre(l.at)} />)}</div>; })}
      {(sc.chips ?? []).map((c, i) => <Chip key={i} text={c.t} at={F(c.at)} x={c.x} y={c.y} dark={c.dark} size={58} />)}
      {sc.stamp && t >= sc.stamp.at && (() => { const k = spring({ frame: f - F(sc.stamp!.at), fps, config: { damping: 9, stiffness: 220 } });
        return <div style={{ position: "absolute", top: sc.stamp!.y, left: 0, right: 0, textAlign: "center", transform: `rotate(-5deg) scale(${1.7 - 0.7 * Math.min(1, k)})`, opacity: Math.min(1, k * 2) }}>
          <span style={{ fontFamily: BEBAS, fontSize: 132, lineHeight: 1, color: "#fff", background: RED, border: "6px solid #fff", borderRadius: 16, padding: "12px 34px 0", boxShadow: "0 16px 40px rgba(0,0,0,.5)" }}>{sc.stamp!.t}</span></div>; })()}
      {!first && <Flash at={1} />}
    </AbsoluteFill>
  );
};

// ---------- calendario animado: el 5 cierra la promo, el 6 vuelven los jefes ----------
const CalScene: React.FC<{ sc: Scene }> = ({ sc }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const cells: (number | null)[] = [null, null, null, null, ...Array.from({ length: 31 }, (_, i) => i + 1)]; // 1-ene-2027 = viernes (semana desde lunes)
  const circ = interpolate(f, [34, 50], [0, 1], clamp);
  const five = spring({ frame: f - 24, fps, config: { damping: 9, stiffness: 200 } });
  const shake = Math.sin(f * 1.9) * 7 * interpolate(f, [50, 51, 64], [0, 1, 0], clamp);
  return (<>
    <Title sc={sc} size={124} top={370} />
    <Pop at={6} style={{ position: "absolute", left: 60, right: 60, top: 668 }}>
      <div style={{ ...card, overflow: "hidden", transform: `translateX(${shake}px) rotate(${-1.2 + shake * 0.05}deg)` }}>
        <div style={{ background: OR, padding: "20px 0 10px", textAlign: "center", fontFamily: BEBAS, fontSize: 92, color: "#fff", letterSpacing: 6, lineHeight: 1 }}>ENERO 2027</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", padding: "16px 22px 0" }}>
          {["L", "M", "X", "J", "V", "S", "D"].map((d) => <div key={d} style={{ textAlign: "center", fontFamily: MONT, fontWeight: 900, fontSize: 30, color: OR }}>{d}</div>)}</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", padding: "0 22px 20px" }}>
          {cells.map((d, i) => { if (!d) return <div key={i} />; const k = spring({ frame: f - 8 - Math.floor(i / 7) * 2 - (i % 7), fps, config: { damping: 14, stiffness: 200 } });
            const promo = d <= 5; const is5 = d === 5; const is6 = d === 6;
            return <div key={i} style={{ position: "relative", height: 96, display: "flex", alignItems: "center", justifyContent: "center", opacity: Math.min(1, k * 1.5), transform: `scale(${0.6 + 0.4 * k})` }}>
              {is5 && <div style={{ position: "absolute", width: 86, height: 86, borderRadius: 43, background: OR, transform: `scale(${five})` }} />}
              <span style={{ position: "relative", fontFamily: BEBAS, fontSize: 62, lineHeight: 1, paddingTop: 6, color: is5 ? "#fff" : promo ? OR : d > 6 ? "#A9B4C6" : INK }}>{d}</span>
              {is6 && <svg viewBox="0 0 200 200" style={{ position: "absolute", width: 124, height: 124, left: "50%", top: "50%", transform: "translate(-50%,-50%) rotate(-8deg)" }}>
                <path d="M100 14 C150 10 190 50 186 102 C182 156 140 190 96 186 C46 182 12 146 16 96 C20 48 60 16 112 20" fill="none" stroke={RED} strokeWidth={13} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - circ} /></svg>}
            </div>; })}
        </div>
      </div></Pop>
    <Pop at={26} style={{ position: "absolute", left: 60, right: 60, top: 1362 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 18, fontFamily: MONT, fontWeight: 800, fontSize: 34, color: "#fff" }}>
        <div style={{ width: 40, height: 40, borderRadius: 20, background: OR, flexShrink: 0 }} />MARTES 5 · CIERRA LA PROMO · 23:59</div></Pop>
    <Pop at={46} style={{ position: "absolute", left: 60, right: 60, top: 1426 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 18, fontFamily: MONT, fontWeight: 800, fontSize: 34, color: "#fff" }}>
        <div style={{ width: 40, height: 40, borderRadius: 20, border: `7px solid ${RED}`, boxSizing: "border-box", flexShrink: 0 }} />MIÉRCOLES 6 · VUELVEN LOS JEFES</div></Pop>
  </>);
};

// ---------- escenas de explicación (tarjetas de Promo.tsx) ----------
const CardScene: React.FC<{ sc: Scene & { s: number; e: number }; last: boolean }> = ({ sc, last }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const dur = F(sc.e - sc.s);
  const out = last ? 1 : interpolate(f, [dur - 5, dur + 3], [1, 0], clamp);
  const n = sc.items?.length ?? 0;
  const step = n ? Math.max(8, Math.min(20, Math.floor((dur - 40) / n))) : 0;
  let body: React.ReactNode = null;
  if (sc.type === "cal") body = <CalScene sc={sc} />;
  if (sc.type === "price") { const k = spring({ frame: f - 8, fps, config: { damping: 9, stiffness: 150 } }); const strike = interpolate(f, [16, 26], [0, 1], clamp);
    const st = spring({ frame: f - 34, fps, config: { damping: 9, stiffness: 220 } });
    body = (<>
      <Title sc={sc} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 720 }}>
        <div style={{ ...card, padding: "40px 30px 36px", textAlign: "center", transform: `scale(${0.8 + 0.2 * k})`, opacity: Math.min(1, k * 1.5), border: `6px solid ${OR}` }}>
          <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 32, letterSpacing: 3, color: NAVY }}>{sc.small}</div>
          <div style={{ position: "relative", display: "inline-block", fontFamily: BEBAS, fontSize: 120, lineHeight: 1, color: "#8A97AB", marginTop: 10 }}>$154.99
            <div style={{ position: "absolute", left: -10, top: "44%", height: 10, width: `${strike * 108}%`, background: RED, borderRadius: 5, transform: "rotate(-7deg)", transformOrigin: "0 50%" }} /></div>
          <div style={{ fontFamily: BEBAS, fontSize: 290, lineHeight: 0.88, color: OR, marginTop: 6, whiteSpace: "nowrap", transform: `scale(${0.7 + 0.3 * spring({ frame: f - 22, fps, config: { damping: 8, stiffness: 180 } })})` }}>{sc.big}</div>
          <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 36, lineHeight: 1.2, color: INK, marginTop: 10 }}>{sc.foot}</div>
        </div>
        <div style={{ position: "absolute", right: -6, top: -46, transform: `rotate(9deg) scale(${1.8 - 0.8 * Math.min(1, st)})`, opacity: Math.min(1, st * 2) }}>
          <div style={{ background: NAVY, border: `5px solid ${OR}`, borderRadius: 18, padding: "12px 26px 2px", fontFamily: BEBAS, fontSize: 86, lineHeight: 1, color: "#fff", boxShadow: "0 14px 34px rgba(0,0,0,.45)" }}>70 % <span style={{ color: OR }}>OFF</span></div></div>
      </div></>); }
  if (sc.type === "list") body = (<>
    <Title sc={sc} />
    <Pop at={8} style={{ position: "absolute", left: 60, right: 60, top: 690 }}>
      <div style={{ ...card, padding: "24px 38px" }}>
        {sc.items!.map((it, i) => { const k = spring({ frame: f - (16 + i * step), fps, config: { damping: 13 } });
          return <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, padding: "24px 0", borderTop: i ? "2px solid #E6EBF2" : "none", opacity: Math.min(1, k * 1.4), transform: `translateX(${(1 - k) * -30}px)` }}>
            <div style={{ width: 54, height: 54, borderRadius: 27, background: OR, color: "#fff", fontFamily: MONT, fontWeight: 900, fontSize: 32, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${k})`, flexShrink: 0 }}>✓</div>
            <div style={{ flex: 1 }}><div style={{ fontFamily: MONT, fontWeight: 900, fontSize: 44, lineHeight: 1.13 }}>{it.t}</div>
              {it.tag && <div style={{ fontFamily: MONT, fontWeight: 700, fontSize: 29, color: "#5B6B80", marginTop: 6, lineHeight: 1.2 }}>{it.tag}</div>}</div>
          </div>; })}
      </div></Pop>
  </>);
  if (sc.type === "deadline") { const k = spring({ frame: f - 8, fps, config: { damping: 9, stiffness: 150 } });
    body = (<>
      <Title sc={sc} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 760 }}>
        <div style={{ ...card, padding: "40px 40px 44px", textAlign: "center", transform: `scale(${0.8 + 0.2 * k})`, opacity: Math.min(1, k * 1.5), border: `6px solid ${OR}` }}>
          <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 34, letterSpacing: 3, color: NAVY }}>{sc.small}</div>
          <div style={{ fontFamily: BEBAS, fontSize: 300, lineHeight: 0.9, color: OR, marginTop: 6, whiteSpace: "nowrap" }}>{sc.big}</div>
          <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 36, lineHeight: 1.2, color: INK, marginTop: 8 }}>{sc.foot}</div>
        </div></div></>); }
  if (sc.type === "cta") { const k = spring({ frame: f - 14, fps, config: { damping: 10 } }); const pulse = 1 + 0.03 * Math.sin(f / 5);
    body = (<>
      <Title sc={sc} size={124} top={400} />
      <div style={{ position: "absolute", left: 40, right: 40, top: 800, display: "flex", justifyContent: "center", transform: `scale(${(0.8 + 0.2 * k) * pulse})`, opacity: Math.min(1, k * 1.5) }}>
        <div style={{ background: OR, borderRadius: 999, padding: "34px 52px 22px", fontFamily: BEBAS, fontSize: 118, lineHeight: 1, color: "#fff", border: "5px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.45)", letterSpacing: 2, whiteSpace: "nowrap" }}>{sc.button}</div>
      </div>
      <Pop at={22} style={{ position: "absolute", left: 50, right: 50, top: 1030, textAlign: "center" }}>
        <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 36, letterSpacing: 1, lineHeight: 1.3, color: "#fff" }}>{sc.foot}</div>
        <div style={{ fontFamily: MONT, fontWeight: 700, fontSize: 30, lineHeight: 1.3, color: "#B9C6DA", marginTop: 12 }}>{sc.small}</div></Pop>
      <Pop at={30} style={{ position: "absolute", left: 0, right: 0, top: 1235 }}><Logos y={0} h={92} /></Pop>
    </>); }
  return <AbsoluteFill style={{ opacity: out }}>{body}</AbsoluteFill>;
};

export const Nav: React.FC<NavProps> = (p) => {
  const f = useCurrentFrame(); const { fps, durationInFrames } = useVideoConfig();
  const t = f / fps; const tl = timeline(p);
  const firstCard = tl.find((x) => x.type !== "clip")!;
  const cardsFrom = tl.filter((x) => x.type !== "clip")[0].s;
  // texto de apoyo palabra a palabra (como Promo.tsx sin voz), solo en las escenas de tarjeta
  const words = tl.filter((sc) => sc.type !== "clip").flatMap((sc) => { const ws = sc.say.split(/\s+/).filter(Boolean); const a = sc.s + 0.35; const d = Math.min(0.34, (sc.e - a - 0.5) / ws.length); return ws.map((w, i) => ({ w, s: a + i * d, e: a + (i + 1) * d, sc: sc.s, end: sc.e })); });
  const pages: { ws: typeof words; s: number; e: number }[] = []; let cur: typeof words = [];
  words.forEach((w, i) => { cur.push(w); const nx = words[i + 1];
    if (!nx || nx.sc !== w.sc || cur.length >= 4 || /[,.:?!]$/.test(w.w)) { pages.push({ ws: cur, s: cur[0].s, e: nx && nx.sc === w.sc ? nx.s : w.end - 0.12 }); cur = []; } });
  const page = pages.find((x) => t >= x.s - 0.03 && t < x.e);
  const prog = interpolate(f, [0, durationInFrames - 30], [0, 100], clamp);
  const inCards = t >= cardsFrom;
  const escena = tl.find((x) => t >= x.s && t < x.e) ?? tl[tl.length - 1];
  const enTarjeta = escena.type !== "clip";
  return (
    <AbsoluteFill style={{ background: NAVY }}>
      {inCards && <Bg photo={p.bg} />}
      {inCards && <Img src={staticFile("logo-claro.png")} style={{ position: "absolute", left: 60, top: 240, width: 320 }} />}
      {inCards && <div style={{ position: "absolute", right: 60, top: 256, background: OR, color: "#fff", fontFamily: MONT, fontWeight: 900, fontSize: 24, letterSpacing: 3, padding: "8px 20px", borderRadius: 999 }}>PROMO DE NAVIDAD</div>}
      {tl.map((sc, i) => <Sequence key={i} from={F(sc.s)} durationInFrames={F(sc.e - sc.s) + (i === tl.length - 1 ? 0 : sc.type === "clip" ? 0 : 3)}>
        {sc.type === "clip" ? <ClipScene sc={sc} first={i === 0} /> : <CardScene sc={sc} last={i === tl.length - 1} />}</Sequence>)}
      {enTarjeta && page && <div style={{ position: "absolute", left: 50, right: 50, top: 1418, display: "flex", justifyContent: "center", flexWrap: "wrap", gap: 14 }}>
        {page.ws.map((w, i) => { const k = spring({ frame: f - F(w.s), fps, config: { damping: 14, stiffness: 240 } }); const on = t >= w.s - 0.03;
          return <span key={i} style={{ fontFamily: MONT, fontWeight: 900, fontSize: 46, color: on && t < w.e + 0.05 ? OR : "#fff", opacity: on ? 1 : 0.35, transform: `translateY(${(1 - k) * 8}px)`, textShadow: "0 3px 14px rgba(0,0,0,.6)" }}>{w.w}</span>; })}
      </div>}
      {enTarjeta && <div style={{ position: "absolute", left: 60, right: 180, top: 1510, height: 8, borderRadius: 4, background: "rgba(255,255,255,.14)" }}><div style={{ width: `${prog}%`, height: "100%", borderRadius: 4, background: OR }} /></div>}
      {t >= firstCard.s - 0.05 && <Flash at={F(firstCard.s)} />}
    </AbsoluteFill>
  );
};
