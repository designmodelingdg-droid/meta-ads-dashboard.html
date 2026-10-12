import React from "react";
import { AbsoluteFill, Audio, Composition, continueRender, delayRender, Easing, IFrame, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/fonts";
import CODE from "./code.json";

// /brag-slim · Pack starter de Dynamo · vertical · tone polished
// Material real: la landing pack-dynamo/index.html (markup + CSS en iframe) y el script 01.
const NAVY = "#003e5c";
const AZUL = "#0a5a80";
const ORANGE = "#ca7520";
const ORANGE_D = "#e8a04a";
const ORANGE_BTN = "#a7611b";
const CREMA = "#fafaf7";
const HEAD = "AntonDMA";
const BODY = "OverpassDMA";
loadFont({ family: HEAD, url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: HEAD, url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: BODY, url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-600-normal.woff2"), weight: "600" });

const FPS = 30;
const TOTAL = 21.5;
// cortes en el beat (vol-10, ~110 BPM)
const S2 = 2.46, S3 = 6.28, S4 = 10.38, S5 = 14.2, S6 = 17.47, HIT = 20.19;
const useF = () => useCurrentFrame();
const sp = (f: number, t0: number, cfg: "dry" | "standard" | "heavy" | "playful" = "standard") =>
  spring({
    frame: f - Math.round(t0 * FPS), fps: FPS,
    config: { dry: { damping: 26, stiffness: 180, mass: 1 }, standard: { damping: 18, stiffness: 120, mass: 1 }, heavy: { damping: 22, stiffness: 70, mass: 1.6 }, playful: { damping: 9, stiffness: 140, mass: 0.8 } }[cfg],
  });
const lin = (t: number, a: number, b: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.22, 1, 0.36, 1) });
// escena visible entre a y b, con salida rápida (sale lo viejo, entra lo nuevo)
const vis = (t: number, a: number, b: number) => (t >= a && t < b ? Math.min(lin(t, a, a + 0.25), 1 - lin(t, b - 0.18, b)) : 0);

// ---------- fondo ----------
const Bg: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 35%, ${AZUL} 0%, ${NAVY} 70%)` }}>
    <svg width={1080} height={1920} style={{ position: "absolute", opacity: 0.1 }}>
      {Array.from({ length: 24 }).map((_, i) => <line key={`v${i}`} x1={i * 48} y1={0} x2={i * 48} y2={1920} stroke="#cfe3ee" strokeWidth={1} />)}
      {Array.from({ length: 41 }).map((_, i) => <line key={`h${i}`} x1={0} y1={i * 48} x2={1080} y2={i * 48} stroke="#cfe3ee" strokeWidth={1} />)}
    </svg>
  </AbsoluteFill>
);

// ---------- titular de cada escena ----------
const Title: React.FC<{ a: number; b: number; l1: string; l2?: string; top?: number }> = ({ a, b, l1, l2, top = 150 }) => {
  const f = useF();
  const t = f / FPS;
  const o = vis(t, a, b);
  if (o <= 0) return null;
  const k1 = sp(f, a, "dry");
  const k2 = sp(f, a + 0.12, "dry");
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top, textAlign: "center", opacity: o, fontFamily: HEAD, lineHeight: 1.02 }}>
      <div style={{ fontSize: 108, color: "#fff", transform: `translateY(${(1 - k1) * 40}px)`, opacity: k1 }}>{l1}</div>
      {l2 && <div style={{ fontSize: 108, color: ORANGE_D, transform: `translateY(${(1 - k2) * 40}px)`, opacity: k2 }}>{l2}</div>}
    </div>
  );
};

// ---------- escena 1: gancho ----------
const Hook: React.FC = () => {
  const f = useF();
  const t = f / FPS;
  const o = vis(t, 0, S2);
  if (o <= 0) return null;
  const a = sp(f, 0.1, "playful");
  const b = sp(f, 0.82, "playful");
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: o, fontFamily: HEAD, textAlign: "center" }}>
      <div style={{ fontSize: 170, color: "#fff", lineHeight: 1, transform: `scale(${0.6 + 0.4 * a}) translateY(${(1 - a) * -80}px)`, opacity: Math.min(1, a * 1.5) }}>¿ABRISTE<br />DYNAMO</div>
      <div style={{ fontSize: 170, color: ORANGE_D, lineHeight: 1.05, marginTop: 10, transform: `scale(${0.6 + 0.4 * b}) translateY(${(1 - b) * 80}px)`, opacity: Math.min(1, b * 1.5) }}>Y LO<br />CERRASTE?</div>
    </AbsoluteFill>
  );
};

// ---------- teléfono con la landing real ----------
const PX = 130, PY = 520, SW = 780, SH = 1360, SC = SW / 430;
type Box = { x: number; y: number; w: number; h: number };
type Geo = { qt: number; tres: number; cards: Box[]; chips: Box[] };
// posiciones medidas DENTRO del iframe (no a ojo): así los anillos caen siempre sobre el elemento real
const scrollAt = (f: number, g: Geo | null) => {
  const t = f / FPS;
  if (!g) return 0;
  let y = interpolate(t, [S2, S3], [0, 70], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const top = g.qt - 70;
  y += (top - 70) * sp(f, S3, "standard");
  const last = g.cards[4] ? g.cards[4].y + g.cards[4].h + 30 - SH / SC : top;
  y += Math.max(0, last - top) * lin(t, 7.2, 9.9);
  if (t >= S5) y = g.tres - 120 + 30 * lin(t, S5, S6);
  return y;
};
const Ring: React.FC<{ x: number; y: number; w: number; h: number; k: number; r?: number }> = ({ x, y, w, h, k, r = 18 }) => (
  <div style={{ position: "absolute", left: x - 8, top: y - 8, width: w + 16, height: h + 16, borderRadius: r, border: `7px solid ${ORANGE}`, opacity: k, transform: `scale(${1.08 - 0.08 * k})`, boxShadow: `0 0 28px rgba(202,117,32,${0.5 * k})` }} />
);
const Phone: React.FC = () => {
  const f = useF();
  const t = f / FPS;
  const show = (t >= S2 && t < S4) || (t >= S5 && t < S6);
  const enter = t < S4 ? sp(f, S2, "heavy") : sp(f, S5, "standard");
  const out = t < S4 ? lin(t, S4 - 0.2, S4) : lin(t, S6 - 0.2, S6);
  const [geo, setGeo] = React.useState<Geo | null>(null);
  const [handle] = React.useState(() => delayRender("landing en iframe"));
  const y = scrollAt(f, geo);
  const ref = React.useRef<HTMLIFrameElement>(null);
  const scrollTo = (v: number) => {
    const w = ref.current?.contentWindow;
    if (w) { w.document.documentElement.style.scrollBehavior = "auto"; if (w.document.body) w.document.body.style.scrollBehavior = "auto"; w.scrollTo({ top: v, left: 0, behavior: "instant" }); }
  };
  React.useLayoutEffect(() => { scrollTo(y); });
  const onLoad = () => {
    const w = ref.current?.contentWindow;
    if (!w) return;
    w.document.fonts.ready.then(() => {
      w.scrollTo({ top: 0, left: 0, behavior: "instant" });
      const d = w.document;
      const box = (e: Element): Box => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top + w.scrollY, w: r.width, h: r.height }; };
      const heads = [...d.querySelectorAll("h2")];
      const qt = heads.find((h) => /Qué trae el pack/.test(h.textContent ?? ""));
      const tres = heads.find((h) => /Tres solo leen/.test(h.textContent ?? ""));
      const titles = [...d.querySelectorAll("h3,h4,b,strong")].filter((e) => /Auditoría de advertencias →|Duplicados en el mismo sitio|Renombrar vistas en lote|Vistas que no|Rellenar un parámetro/.test(e.textContent ?? ""));
      const cards = titles.map((e) => box(e.closest("div,article,li") ?? e));
      const chips = [...d.querySelectorAll(".chip.ok")].map(box);
      setGeo({ qt: qt ? box(qt).y : 1044, tres: tres ? box(tres).y : 2016, cards, chips });
      continueRender(handle);
    });
  };
  const sy = (cy: number) => PY + (cy - y) * SC;
  return (
    <AbsoluteFill style={{ opacity: show ? 1 - out : 0, transform: `translateY(${(1 - enter) * 900}px)` }}>
      <div style={{ position: "absolute", left: PX - 20, top: PY - 20, width: SW + 40, height: SH + 40, borderRadius: 70, background: "#0b1520", boxShadow: "0 40px 90px rgba(0,0,0,0.55)" }} />
      <div style={{ position: "absolute", left: PX, top: PY, width: SW, height: SH, borderRadius: 52, overflow: "hidden", background: CREMA }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: 430, height: SH / SC, transform: `scale(${SC})`, transformOrigin: "0 0" }}>
          <IFrame ref={ref} src={staticFile("pack/index.html")} onLoad={onLoad} style={{ width: 430, height: SH / SC, border: "none" }} />
        </div>
      </div>
      {show && geo && t >= S3 && t < S4 && geo.cards.slice(0, 5).map((c, i) => {
        const t0 = 6.82 + i * 0.545;
        const k = t >= t0 ? 1 - lin(t, t0 + 0.5, t0 + 0.55) * (i < 4 ? 1 : 0) : 0;
        const ki = lin(t, t0, t0 + 0.12) * k;
        return ki > 0 ? <Ring key={i} x={PX + c.x * SC} y={sy(c.y)} w={c.w * SC} h={c.h * SC} k={ki} /> : null;
      })}
      {show && geo && t >= S5 && geo.chips.slice(0, 3).map((c, i) => {
        const k = lin(t, 14.73 + i * 0.545, 14.85 + i * 0.545);
        return k > 0 ? <Ring key={i} x={PX + c.x * SC} y={sy(c.y)} w={c.w * SC} h={c.h * SC} k={k} r={30} /> : null;
      })}
    </AbsoluteFill>
  );
};

// ---------- escena 4: el código real escribiéndose ----------
const LINES = (CODE as string[]).slice(0, 13);
const Code: React.FC = () => {
  const f = useF();
  const t = f / FPS;
  const o = vis(t, S4, S5);
  if (o <= 0) return null;
  const enter = sp(f, S4, "standard");
  const total = LINES.join("\n").length;
  const n = Math.floor(total * lin(t, S4 + 0.3, S5 - 0.6));
  let left = n;
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <div style={{ position: "absolute", left: 50, top: 520, width: 980, height: 1060, background: "#0B1220", borderRadius: 26, boxShadow: "0 40px 90px rgba(0,0,0,0.55)", overflow: "hidden", transform: `translateY(${(1 - enter) * 120}px) scale(${0.94 + 0.06 * enter})` }}>
        <div style={{ height: 80, background: "#111A2C", display: "flex", alignItems: "center", gap: 12, padding: "0 28px" }}>
          {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => <div key={c} style={{ width: 20, height: 20, borderRadius: 10, background: c }} />)}
          <div style={{ marginLeft: 18, fontFamily: BODY, fontWeight: 600, fontSize: 30, color: "#C9D3E1" }}>01_auditoria_advertencias.py</div>
        </div>
        <div style={{ padding: "28px 26px", fontFamily: "DejaVu Sans Mono, monospace", fontSize: 29, lineHeight: "50px", whiteSpace: "pre", color: "#A9D3B4" }}>
          {LINES.map((s, i) => {
            const take = Math.max(0, Math.min(s.length, left));
            left -= s.length + 1;
            const typing = take < s.length && take > 0;
            return (
              <div key={i} style={{ display: "flex" }}>
                <span style={{ width: 60, textAlign: "right", paddingRight: 22, color: "#4A5A73" }}>{i + 1}</span>
                <span>{s.slice(0, take)}{typing || (take === s.length && left < 0 && left > -2) ? <span style={{ background: ORANGE_D, color: ORANGE_D }}>▌</span> : null}</span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- escena 6: outro ----------
const Outro: React.FC = () => {
  const f = useF();
  const t = f / FPS;
  if (t < S6) return null;
  const k = sp(f, S6, "heavy");
  const name = sp(f, 18.01, "dry");
  const btn = sp(f, 18.55, "playful");
  const hit = t >= HIT ? 1 + 0.08 * Math.exp(-(t - HIT) * 6) * Math.cos((t - HIT) * 30) : 1;
  const flash = t >= HIT ? Math.max(0, 1 - (t - HIT) * 4) : 0;
  return (
    <AbsoluteFill style={{ alignItems: "center", textAlign: "center" }}>
      <div style={{ marginTop: 480, opacity: k, transform: `translateY(${(1 - k) * 60}px)` }}>
        <Img src={staticFile("logo-dma.png")} style={{ width: 560 }} />
      </div>
      <div style={{ marginTop: 70, fontFamily: HEAD, fontSize: 140, color: "#fff", lineHeight: 1, opacity: name, transform: `translateY(${(1 - name) * 40}px)` }}>PACK DE DYNAMO</div>
      <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 44, color: ORANGE_D, marginTop: 18, opacity: name }}>5 scripts · comentados por dentro</div>
      <div style={{ marginTop: 90, transform: `scale(${(0.6 + 0.4 * btn) * hit})`, opacity: Math.min(1, btn * 1.5) }}>
        <span style={{ display: "inline-block", background: ORANGE_BTN, color: "#fff", fontFamily: BODY, fontWeight: 800, fontSize: 64, padding: "30px 70px 22px", borderRadius: 999, boxShadow: `0 20px 50px rgba(0,0,0,0.45), 0 0 ${60 * flash}px rgba(232,160,74,${flash})` }}>Descargar gratis</span>
      </div>
    </AbsoluteFill>
  );
};

const Brag: React.FC = () => {
  const f = useF();
  const t = f / FPS;
  const vol = interpolate(t, [0, 0.4, TOTAL - 1.2, TOTAL], [0, 0.85, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <Bg />
      <Hook />
      <Title a={S2} b={S3} l1="PACK STARTER" l2="GRATIS" />
      <Title a={S3} b={S4} l1="5 SCRIPTS .PY" l2="LISTOS PARA PEGAR" />
      <Title a={S4} b={S5} l1="COMENTADOS" l2="LÍNEA A LÍNEA" />
      <Title a={S5} b={S6} l1="3 SOLO LEEN" l2="NO TOCAN TU MODELO" />
      <Phone />
      <Code />
      <Outro />
      <Audio src={staticFile("music.mp3")} volume={() => vol} />
    </AbsoluteFill>
  );
};

export const MyComposition = () => (
  <Composition id="Reel" component={Brag} durationInFrames={Math.round(TOTAL * FPS)} fps={FPS} width={1080} height={1920} />
);
