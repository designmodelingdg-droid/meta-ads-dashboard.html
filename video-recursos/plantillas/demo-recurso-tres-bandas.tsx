import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import WORDS from "./words.json";
import CODE from "./code.json";

// Reel de pauta · lead magnet «Pack starter de Dynamo» (pauta-dynamo, leadmagnets-septiembre)
// Estilo 3 · DEMO DE RECURSO, variante «Tres bandas» (estilos-reels-dma):
// titular fijo arriba · material real al centro · banda cobre fija abajo · subtítulos 1–2 palabras.
const RED = "#E5252A";
const COPPER = "#D78631";
const COPPER_L = "#E8A04A";
const NAVY = "#0D1E3A";
const NAVY_D = "#0A1624";
const HEAD = "AntonDMA";
const BODY = "OverpassDMA";
loadFont({ family: HEAD, url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: HEAD, url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: BODY, url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-600-normal.woff2"), weight: "600" });

const FPS = 30;
const TOP = 300;
const BAND = 1660;
const CAP_Y = 1500;
const VOICE_END = 14.04;
const TOTAL_S = 15.6;
// tramos de la voz editada
const D1 = 3.85;   // «La automatización en BIM…»
const D2 = 8.08;   // «Aquí van cinco…»
const LIST = 9.0;  // «tres de ellos…»
const CIERRE = 12.54;
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const useT = () => useCurrentFrame() / FPS;
const p = (t: number, t0: number, d = 0.3, e = EASE) =>
  interpolate(t, [t0, t0 + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });

// ---------- Gabriel (fondo en hook y cierre) ----------
const Presenter: React.FC = () => {
  const t = useT();
  const cierre = t >= CIERRE;
  const s = cierre ? 1.06 : (t >= 1.57 ? 1.1 : 1.0) * (1 + 0.03 * p(t, 0, 3.8, Easing.linear));
  const faceY = cierre ? 640 : 600;
  const ty = 820 - faceY * s;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `translateY(${ty}px) scale(${s})`, transformOrigin: "50% 0" }}>
        <Video src={staticFile("gabriel_editado.mp4")} style={{ width: 1080, height: 1920 }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- panel del material real (D1 → CIERRE) ----------
const Grid: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, #13305A 0%, ${NAVY_D} 72%)` }}>
    <svg width={1080} height={1920} style={{ position: "absolute", opacity: 0.15 }}>
      {Array.from({ length: 24 }).map((_, i) => <line key={`v${i}`} x1={i * 48} y1={0} x2={i * 48} y2={1920} stroke="#9FB0C8" strokeWidth={1} />)}
      {Array.from({ length: 41 }).map((_, i) => <line key={`h${i}`} x1={0} y1={i * 48} x2={1080} y2={i * 48} stroke="#9FB0C8" strokeWidth={1} />)}
    </svg>
  </AbsoluteFill>
);
const Enter: React.FC<{ a: number; b: number; children: React.ReactNode }> = ({ a, b, children }) => {
  const t = useT();
  if (t < a || t >= b) return null;
  const k = p(t, a, 0.2);
  return <AbsoluteFill style={{ opacity: k, transform: `scale(${0.94 + 0.06 * k})`, filter: `blur(${(1 - k) * 8}px)` }}>{children}</AbsoluteFill>;
};

// código real del script 01, en un editor oscuro que se desplaza solo
const LH = 46;
const KW = /\b(import|from|def|if|else|not|return|None|in|for|any|True|False)\b/g;
const Line: React.FC<{ s: string; doc: boolean }> = ({ s, doc }) => {
  const trimmed = s.trimStart();
  if (doc) return <span style={{ color: "#A9D3B4" }}>{s || " "}</span>;
  if (trimmed.startsWith("#")) return <span style={{ color: "#7F8EA3" }}>{s || " "}</span>;
  const parts = s.split(KW);
  return <>{parts.map((x, i) => (i % 2 === 1 ? <span key={i} style={{ color: COPPER_L }}>{x}</span> : <span key={i}>{x}</span>))}{s ? "" : " "}</>;
};
const CodeCard: React.FC = () => {
  const t = useT();
  // sube 3 líneas y marca la 9 («Por qué es el primero del pack») cuando dice «el primer script»
  const scroll = interpolate(t, [D1 + 0.3, 7.1], [0, 3 * LH], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) });
  const box = p(t, 7.3, 0.25);
  const boxY = 70 + 20 + (9 - 1 - 3) * LH - 6;
  return (
    <div style={{ position: "absolute", left: 60, top: TOP + 70, width: 960, height: 1020, background: "#0B1220", borderRadius: 20, boxShadow: "0 30px 70px rgba(0,0,0,0.55)", overflow: "hidden", border: "1px solid #24324A" }}>
      <div style={{ height: 70, background: "#111A2C", display: "flex", alignItems: "center", gap: 12, padding: "0 26px" }}>
        {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => <div key={c} style={{ width: 18, height: 18, borderRadius: 9, background: c }} />)}
        <div style={{ marginLeft: 18, fontFamily: BODY, fontWeight: 600, fontSize: 28, color: "#C9D3E1" }}>01_auditoria_advertencias.py</div>
        <div style={{ marginLeft: "auto", fontFamily: BODY, fontWeight: 800, fontSize: 22, color: NAVY, background: "#BFE8D3", borderRadius: 14, padding: "4px 14px" }}>SOLO LEE</div>
      </div>
      <div style={{ position: "relative", height: 950, overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 20 - scroll, fontFamily: "DejaVu Sans Mono, monospace", fontSize: 30, lineHeight: `${LH}px`, color: "#E6EDF6", whiteSpace: "pre" }}>
          {(CODE as string[]).map((s, i) => (
            <div key={i} style={{ display: "flex" }}>
              <span style={{ width: 70, textAlign: "right", paddingRight: 22, color: "#4A5A73" }}>{i + 1}</span>
              <Line s={s} doc={i >= 1 && i <= 23} />
            </div>
          ))}
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 120, background: "linear-gradient(180deg, rgba(11,18,32,0), #0B1220)" }} />
      </div>
      {box > 0 && (
        <div style={{ position: "absolute", left: 20, right: 20, top: boxY, height: 0 }}>
          <svg width={920} height={100} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
            <rect x={4} y={4} width={912} height={LH + 6} rx={10} fill="none" stroke={RED} strokeWidth={6} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - box} />
          </svg>
        </div>
      )}
    </div>
  );
};

// el celular real recorriendo la guía del pack
const Phone: React.FC = () => (
  <div style={{ position: "absolute", left: 90, top: TOP + 30, width: 900, height: 1300 - 30, borderRadius: 24, overflow: "hidden", boxShadow: "0 30px 70px rgba(0,0,0,0.55)" }}>
    <div style={{ position: "absolute", left: 0, top: -310, width: 900, height: 1600 }}>
      <Sequence from={Math.round(D2 * FPS)} layout="none"><Video src={staticFile("scroll.mp4")} muted style={{ width: 900, height: 1600 }} /></Sequence>
    </div>
  </div>
);

// la lista real de la landing con los tres «Solo lee» marcados
const LW = 900;
const LS = LW / 780; // escala de la captura (780×596)
const PILLS: [number, number][] = [[76, LIST + 0.12], [152, LIST + 0.32], [302, LIST + 0.52]];
const ListCard: React.FC = () => {
  const t = useT();
  const stamp = p(t, 10.26, 0.22, Easing.out(Easing.back(2)));
  const viv = p(t, 11.2, 0.25);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 90, top: TOP + 150, width: LW, height: 596 * LS, borderRadius: 26, overflow: "hidden", boxShadow: "0 30px 70px rgba(0,0,0,0.55)" }}>
        <Img src={staticFile("list.png")} style={{ width: LW, height: 596 * LS }} />
        <svg width={LW} height={596 * LS} style={{ position: "absolute", left: 0, top: 0 }}>
          {PILLS.map(([cy, t0]) => {
            const k = p(t, t0, 0.22, Easing.inOut(Easing.quad));
            return k > 0 ? <rect key={cy} x={(677 - 75) * LS} y={(cy - 32) * LS} width={150 * LS} height={64 * LS} rx={32 * LS} fill="none" stroke={RED} strokeWidth={6} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} /> : null;
          })}
        </svg>
      </div>
      {t >= 10.26 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: TOP + 150 + 596 * LS + 60, textAlign: "center", transform: `rotate(-3deg) scale(${interpolate(stamp, [0, 1], [1.5, 1])})`, opacity: Math.min(1, stamp * 2) }}>
          <span style={{ display: "inline-block", fontFamily: HEAD, fontSize: 110, color: "#fff", background: RED, padding: "18px 40px 4px", borderRadius: 18, boxShadow: "0 16px 36px rgba(0,0,0,0.45)" }}>3 SOLO LEEN</span>
        </div>
      )}
      {t >= 11.2 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: TOP + 150 + 596 * LS + 250, textAlign: "center", opacity: viv }}>
          <span style={{ fontFamily: BODY, fontWeight: 800, fontSize: 42, color: "#fff" }}>no tocan tu modelo · córrelos hoy</span>
        </div>
      )}
    </AbsoluteFill>
  );
};

const Panel: React.FC = () => {
  const t = useT();
  if (t < D1 || t >= CIERRE) return null;
  return (
    <AbsoluteFill>
      <Grid />
      <Enter a={D1} b={D2}><CodeCard /></Enter>
      <Enter a={D2} b={LIST}><Phone /></Enter>
      <Enter a={LIST} b={CIERRE}><ListCard /></Enter>
    </AbsoluteFill>
  );
};

// ---------- cierre: GRATIS + flecha a la banda ----------
const Cierre: React.FC = () => {
  const t = useT();
  if (t < CIERRE) return null;
  const k = p(t, 12.6, 0.22, Easing.out(Easing.back(2)));
  const card = p(t, 12.9, 0.3);
  const arrow = p(t, 13.6, 0.3);
  const end = p(t, VOICE_END, 0.35);
  const bob = Math.sin(t * 9) * 8 * arrow;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 60, top: TOP + 60, transform: `rotate(-5deg) scale(${interpolate(k, [0, 1], [1.6, 1])})`, opacity: Math.min(1, k * 2), transformOrigin: "0 50%" }}>
        <span style={{ display: "inline-block", fontFamily: HEAD, fontSize: 140, color: "#fff", background: COPPER, padding: "18px 40px 4px", borderRadius: 20, boxShadow: "0 18px 40px rgba(0,0,0,0.45)" }}>GRATIS</span>
      </div>
      <div style={{ position: "absolute", right: 50, top: TOP + 90, width: 360, borderRadius: 18, overflow: "hidden", boxShadow: "0 22px 50px rgba(0,0,0,0.5)", opacity: card, transform: `translateX(${(1 - card) * 60}px) rotate(3deg)` }}>
        <Img src={staticFile("index_top.png")} style={{ width: 360 }} />
      </div>
      {arrow > 0 && (
        <>
          {[70, 890].map((x) => (
            <svg key={x} width={120} height={150} style={{ position: "absolute", left: x, top: 1490 + bob, opacity: arrow * (1 - end) }}>
              <path d="M60,8 L60,120 M22,84 L60,128 L98,84" stroke="#fff" strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" fill="none" />
            </svg>
          ))}
        </>
      )}
      <AbsoluteFill style={{ background: NAVY, opacity: end * 0.97 }} />
      {end > 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 560, textAlign: "center", opacity: end }}>
          <Img src={staticFile("logo-dma.png")} style={{ width: 600 }} />
          <div style={{ fontFamily: HEAD, fontSize: 104, color: "#fff", marginTop: 50, lineHeight: 1 }}>PACK DE DYNAMO</div>
          <div style={{ fontFamily: HEAD, fontSize: 104, color: COPPER_L, lineHeight: 1.05 }}>GRATIS</div>
          <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 40, color: "#fff", marginTop: 24 }}>el enlace está aquí abajo ↓</div>
        </div>
      )}
    </AbsoluteFill>
  );
};

// ---------- titular fijo, banda fija, subtítulos ----------
const HOOKS: Record<string, [string, string]> = {
  A: ["¿ABRISTE DYNAMO", "Y LO CERRASTE?"],
  B: ["TU PRIMER SCRIPT", "DE DYNAMO, HECHO"],
  C: ["5 SCRIPTS DE DYNAMO", "LISTOS PARA PEGAR"],
};
const Blur: React.FC<{ children: React.ReactNode; t0: number }> = ({ children, t0 }) => {
  const t = useT();
  const k = p(t, t0, 0.18);
  return <span style={{ display: "inline-block", opacity: k, filter: `blur(${(1 - k) * 12}px)`, transform: `translateY(${(1 - k) * 10}px)` }}>{children}</span>;
};
const TopBand: React.FC<{ v: string }> = ({ v }) => {
  const [l1, l2] = HOOKS[v] ?? HOOKS.A;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: TOP, background: `radial-gradient(ellipse at 50% 30%, #12305A 0%, ${NAVY} 75%)`, textAlign: "center", fontFamily: HEAD, lineHeight: 1.04 }}>
      <div style={{ paddingTop: 50, fontSize: 98, color: "#fff", whiteSpace: "nowrap" }}><Blur t0={0}>{l1}</Blur></div>
      <div style={{ fontSize: 106, color: COPPER_L, whiteSpace: "nowrap" }}><Blur t0={0.25}>{l2}</Blur></div>
    </div>
  );
};
const OfferBand: React.FC = () => {
  const t = useT();
  const pulse = 1 + 0.04 * Math.sin(Math.max(0, t - 13.6) * 8) * p(t, 13.6, 0.3);
  return (
    <div style={{ position: "absolute", left: 0, top: BAND, width: 1080, height: 1920 - BAND, background: COPPER, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
      <div style={{ fontFamily: HEAD, fontSize: 84, color: "#fff", lineHeight: 1, transform: `scale(${pulse})`, textShadow: "0 4px 0 rgba(0,0,0,0.18)" }}>PACK DE DYNAMO · GRATIS</div>
      <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 36, color: NAVY }}>5 scripts comentados · descárgalo abajo</div>
    </div>
  );
};
type Wd = { w: string; s: number; e: number };
const CAPS = (() => {
  const ws = (WORDS as Wd[]).map((x) => ({ w: x.w.replace(/[.,¿?¡!]/g, "").toUpperCase(), s: x.s, e: x.e }));
  const out: Wd[] = [];
  for (let i = 0; i < ws.length; i++) {
    const cur = ws[i];
    const nx = ws[i + 1];
    if (cur.w.length <= 3 && nx && nx.s - cur.e < 0.3 && cur.w !== "NO" && !/^\d$/.test(cur.w)) {
      out.push({ w: `${cur.w} ${nx.w}`, s: cur.s, e: nx.e });
      i++;
    } else out.push(cur);
  }
  return out.map((c, i) => ({ ...c, e: Math.min(out[i + 1]?.s ?? c.e + 0.4, c.e + 0.4) }));
})();
const KEY = /DYNAMO|CERRASTE|SCRIPT|ATASCA|5|3|HOY|VIVO|GRATIS|ABAJO|IDEAS|AUTOMATIZACIÓN/;
const Caption: React.FC = () => {
  const t = useT();
  if (t >= VOICE_END) return null;
  const c = CAPS.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const k = p(t, c.s - 0.03, 0.1);
  const key = KEY.test(c.w);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: CAP_Y, display: "flex", justifyContent: "center" }}>
      <span style={{
        fontFamily: HEAD, fontSize: c.w.length > 13 ? 84 : 100, lineHeight: 1, color: "#fff", padding: "14px 30px 4px",
        background: key ? COPPER : "rgba(10,22,36,0.82)", borderRadius: 10, transform: `scale(${0.88 + 0.12 * k})`, display: "inline-block",
        boxShadow: "0 10px 26px rgba(0,0,0,0.4)",
      }}>{c.w}</span>
    </div>
  );
};
const Shade: React.FC = () => (
  <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.35) 78%, rgba(0,0,0,0.5) 86%)" }} />
);

const Reel: React.FC<{ v?: string }> = ({ v = "A" }) => (
  <AbsoluteFill style={{ background: NAVY }}>
    <Presenter />
    <Shade />
    <Panel />
    <Cierre />
    <TopBand v={v} />
    <Caption />
    <OfferBand />
  </AbsoluteFill>
);

export const MyComposition = () => (
  <Composition id="Reel" component={Reel} defaultProps={{ v: "A" }} durationInFrames={Math.round(TOTAL_S * FPS)} fps={FPS} width={1080} height={1920} />
);
