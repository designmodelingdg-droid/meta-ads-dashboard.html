import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/fonts";
import WORDS from "./words.json";

// Anuncio ACERO · «Sobredimensionar» · estilo 8 MOTION GRAPHICS + GABRIEL
// Capas: fondo real → gráficas «detrás» → Gabriel recortado → gráficas «delante» → gancho, subtítulo, banda.
const RED = "#E5252A";
const COPPER = "#D78631";
const COPPER_L = "#E8A04A";
const NAVY = "#0D1E3A";
const HEAD = "AntonDMA";
const BODY = "OverpassDMA";
loadFont({ family: HEAD, url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: HEAD, url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: BODY, url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });

const FPS = 30;
const BAND = 1700;
const CAP_Y = 1480;
const VOICE_END = 33.9;
const TOTAL_S = 35.6;
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const lin = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE });
type Cfg = "dry" | "standard" | "heavy" | "playful";
const CFG: Record<Cfg, { damping: number; stiffness: number; mass: number }> = {
  dry: { damping: 26, stiffness: 180, mass: 1 }, standard: { damping: 18, stiffness: 120, mass: 1 },
  heavy: { damping: 22, stiffness: 70, mass: 1.6 }, playful: { damping: 10, stiffness: 150, mass: 0.8 },
};
const sp = (f: number, t0: number, c: Cfg = "standard") => spring({ frame: f - Math.round(t0 * FPS), fps: FPS, config: CFG[c] });
// visible entre a y b con salida corta
const win = (t: number, a: number, b: number, out = 0.2) => (t < a || t >= b ? 0 : 1 - lin(t, b - out, out));

// ---------- encuadre compartido por el fondo y por Gabriel recortado ----------
const CLIPS = [
  { a: 0, faceY: 560, s: 1.0 },
  { a: 5.41, faceY: 520, s: 1.0 },
  { a: 13.9, faceY: 660, s: 1.3 },
  { a: 22.14, faceY: 650, s: 1.0 },
];
const PUNCH: [number, number][] = [
  [0, 1.0], [2.52, 1.1], [5.41, 1.0], [9.46, 1.08], [11.76, 1.0], [12.58, 1.14], [13.9, 1.0],
  [16.06, 1.08], [18.04, 1.0], [20.1, 1.1], [22.14, 1.0], [24.28, 1.08], [26.46, 1.0], [28.64, 1.08], [32.28, 1.0],
];
const frameT = (t: number) => {
  const c = [...CLIPS].reverse().find((x) => t >= x.a) ?? CLIPS[0];
  const pu = [...PUNCH].reverse().find((x) => t >= x[0]) ?? PUNCH[0];
  const s = c.s * pu[1] * (1 + 0.025 * lin(t, pu[0], 2.4));
  return { s, ty: 860 - c.faceY * s };
};
const Layer: React.FC<{ fg?: boolean }> = ({ fg }) => {
  const t = useCurrentFrame() / FPS;
  const { s, ty } = frameT(t);
  return (
    <AbsoluteFill style={{ transform: `translateY(${ty}px) scale(${s})`, transformOrigin: "50% 0" }}>
      {fg
        ? <OffthreadVideo src={staticFile("gabriel_fg.webm")} transparent muted style={{ width: 1080, height: 1920 }} />
        : <OffthreadVideo src={staticFile("gabriel_editado.mp4")} style={{ width: 1080, height: 1920 }} />}
    </AbsoluteFill>
  );
};
// fondo sustituido por render real de acero (MATERIAL PARA VIDEOS 2026 / Videos Acero y Naves Industriales)
const BROLL: [number, number, string][] = [[5.41, 13.9, "broll_viga.mp4"], [22.14, 34.2, "broll_placas.mp4"]];
const Broll: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  return (
    <AbsoluteFill>
      {BROLL.map(([a, b, src]) => {
        const o = t < a || t >= b ? 0 : Math.min(lin(t, a, 0.25), 1 - lin(t, b - 0.2, 0.2));
        return (
          <Sequence key={src} from={Math.round(a * FPS)} durationInFrames={Math.round((b - a) * FPS)} layout="none">
            <AbsoluteFill style={{ opacity: o, transform: `scale(${1.05 + 0.05 * lin(t, a, b - a)})` }}>
              <OffthreadVideo src={staticFile(src)} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
// el fondo real, oscurecido en navy para que las gráficas de detrás lean
const BgTint: React.FC = () => (
  <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(13,30,58,0.72) 0%, rgba(13,30,58,0.55) 45%, rgba(13,30,58,0.35) 100%)` }} />
);

// ---------- piezas gráficas ----------
const Beam: React.FC<{ w: number; h: number; color: string }> = ({ w, h, color }) => {
  const tf = h * 0.13, tw = w * 0.13;
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ overflow: "visible" }}>
      <rect x={0} y={0} width={w} height={tf} rx={4} fill={color} />
      <rect x={(w - tw) / 2} y={tf - 1} width={tw} height={h - 2 * tf + 2} fill={color} />
      <rect x={0} y={h - tf} width={w} height={tf} rx={4} fill={color} />
    </svg>
  );
};
// palabra gigante detrás de Gabriel
const BigWord: React.FC<{ a: number; b: number; text: string; color?: string; size?: number; top?: number; outline?: boolean }> = ({ a, b, text, color = COPPER_L, size = 250, top = 360, outline }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const o = win(t, a, b);
  if (o <= 0) return null;
  const k = sp(f, a, "playful");
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top, textAlign: "center", opacity: o * Math.min(1, k * 1.4), transform: `scale(${0.7 + 0.3 * k})`, fontFamily: HEAD, fontSize: size, lineHeight: 0.92, color: outline ? "transparent" : color, WebkitTextStroke: outline ? `6px ${color}` : undefined, letterSpacing: -2 }}>
      {text.split("\n").map((l) => <div key={l}>{l}</div>)}
    </div>
  );
};
const Chip: React.FC<{ t0: number; t1: number; x: number; y: number; text: string; bg?: string; color?: string; size?: number; rot?: number; from?: "l" | "r" | "u" }> = ({ t0, t1, x, y, text, bg = COPPER, color = "#fff", size = 64, rot = 0, from = "u" }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const o = win(t, t0, t1);
  if (o <= 0) return null;
  const k = sp(f, t0, "playful");
  const dx = from === "l" ? -260 : from === "r" ? 260 : 0;
  const dy = from === "u" ? 60 : 0;
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o * Math.min(1, k * 1.5), transform: `translate(${(1 - k) * dx}px, ${(1 - k) * dy}px) rotate(${rot}deg) scale(${0.8 + 0.2 * k})` }}>
      <span style={{ display: "inline-block", whiteSpace: "nowrap", background: bg, color, fontFamily: HEAD, fontSize: size, padding: "12px 28px 2px", borderRadius: 14, boxShadow: "0 14px 34px rgba(0,0,0,0.45)" }}>{text}</span>
    </div>
  );
};

// detrás de Gabriel
const Behind: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  return (
    <AbsoluteFill>
      <BigWord a={0.48} b={2.52} text={"SOBRE\nDIMENSIONAR"} size={210} top={330} />
      <BigWord a={2.52} b={5.41} text={"INSEGU\nRIDAD"} color={RED} size={260} top={320} outline />
      <BigWord a={14.8} b={18.04} text={"NO ES\nARRIESGAR"} color="#ffffff" size={230} top={330} outline />
      <BigWord a={20.1} b={22.14} text="CRITERIO" size={230} top={330} />
      <BigWord a={23.74} b={24.7} text="ACERO" size={330} top={330} />
      <BigWord a={24.7} b={29.2} text="$225" size={360} top={320} />
      <BigWord a={29.2} b={32.28} text={"TUTOR\nDE IA"} size={250} top={320} />
    </AbsoluteFill>
  );
};

// delante de Gabriel
const Factura: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const o = win(t, 9.08, 12.1);
  if (o <= 0) return null;
  const k = sp(f, 9.08, "standard");
  const n = Math.round(interpolate(t, [9.2, 11.6], [1200, 3480], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }));
  return (
    <div style={{ position: "absolute", left: 40, top: 900, width: 380, opacity: o, transform: `translateX(${(1 - k) * -420}px) rotate(-5deg)` }}>
      <div style={{ background: "#fff", borderRadius: 18, padding: "26px 28px", boxShadow: "0 24px 60px rgba(0,0,0,0.5)" }}>
        <div style={{ fontFamily: HEAD, fontSize: 56, color: NAVY, lineHeight: 1 }}>FACTURA</div>
        {[0, 1, 2].map((i) => <div key={i} style={{ height: 14, width: 260 - i * 50, borderRadius: 7, background: "#D5DAE2", marginTop: 16 }} />)}
        <div style={{ fontFamily: HEAD, fontSize: 84, color: RED, marginTop: 14, lineHeight: 1 }}>${n.toLocaleString("en-US")}</div>
        <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 22, color: "#64748B" }}>(ejemplo)</div>
      </div>
    </div>
  );
};
const Face: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const o = win(t, 12.1, 13.9);
  if (o <= 0) return null;
  const k = sp(f, 12.1, "playful");
  return (
    <div style={{ position: "absolute", right: 60, top: 920, opacity: o * Math.min(1, k * 1.5), transform: `scale(${0.6 + 0.4 * k})`, textAlign: "center" }}>
      <svg width={190} height={190}>
        <circle cx={95} cy={95} r={86} fill="#fff" stroke={RED} strokeWidth={10} />
        <circle cx={65} cy={78} r={10} fill={NAVY} /><circle cx={125} cy={78} r={10} fill={NAVY} />
        <path d="M55,140 Q95,105 135,140" stroke={RED} strokeWidth={10} fill="none" strokeLinecap="round" />
      </svg>
      <div style={{ fontFamily: HEAD, fontSize: 52, color: "#fff", textShadow: "0 4px 14px rgba(0,0,0,0.6)" }}>TU CLIENTE</div>
    </div>
  );
};
const Arrow: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const o = win(t, 4.3, 5.41);
  const k = lin(t, 4.4, 0.35);
  if (o <= 0) return null;
  return (
    <svg width={1080} height={300} style={{ position: "absolute", left: 0, top: 1010, opacity: o }}>
      <path d="M300,120 C450,40 630,40 760,110" stroke="#fff" strokeWidth={12} fill="none" strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
      {k > 0.95 && <path d="M730,70 L765,112 L715,128" stroke="#fff" strokeWidth={12} fill="none" strokeLinecap="round" strokeLinejoin="round" />}
    </svg>
  );
};
const Logos: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const o = win(t, 27.2, 29.2);
  if (o <= 0) return null;
  const items: [string, number][] = [["lk_revit.png", 1696], ["lk_robot.png", 3947], ["lk_advance.png", 2301]];
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1110, display: "flex", flexDirection: "column", alignItems: "center", gap: 18, opacity: o }}>
      {items.map(([src, w], i) => {
        const k = sp(f, 27.22 + i * 0.18, "dry");
        return (
          <div key={src} style={{ background: "rgba(13,30,58,0.82)", borderRadius: 16, padding: "18px 30px", opacity: k, transform: `translateX(${(1 - k) * (i % 2 ? 300 : -300)}px)` }}>
            <Img src={staticFile(src)} style={{ height: 62, width: Math.min(860, (62 * w) / 322), objectFit: "contain" }} />
          </div>
        );
      })}
    </div>
  );
};
const Front: React.FC = () => (
  <AbsoluteFill>
    <Chip t0={4.16} t1={5.41} x={70} y={1100} text="TU CÁLCULO" bg={NAVY} from="l" size={58} />
    <Chip t0={4.78} t1={5.41} x={690} y={1100} text="CLIENTE" bg={RED} from="r" size={58} />
    <Arrow />
    <Chip t0={6.6} t1={9.0} x={60} y={1060} text="SOBREDIMENSIONADO" bg={COPPER} rot={-3} size={70} />
    <Factura />
    <Chip t0={10.48} t1={12.1} x={600} y={940} text="+ PESO" bg={RED} rot={4} from="r" size={76} />
    <Chip t0={10.98} t1={12.1} x={520} y={1080} text="+ SOLDADURA" bg={RED} rot={-3} from="r" size={70} />
    <Face />
    <Chip t0={14.9} t1={18.04} x={60} y={1050} text="SOBREDIMENSIONAR ✗" bg={NAVY} rot={-2} from="l" size={60} />
    <Chip t0={15.26} t1={18.04} x={360} y={1170} text="ARRIESGAR ✗" bg={RED} rot={2} from="r" size={60} />
    <Chip t0={18.04} t1={22.14} x={60} y={1080} text="EL PERFIL JUSTO ✓" bg={COPPER} rot={-2} from="l" size={66} />
    <Chip t0={20.8} t1={22.14} x={150} y={1200} text="lo enseñamos en la Especialización" bg="#fff" color={NAVY} size={42} />
    <Chip t0={22.88} t1={27.2} x={60} y={1050} text="ESPECIALIZACIÓN EN ACERO" bg={NAVY} color={COPPER_L} from="l" size={58} />
    <Logos />
    <Chip t0={29.22} t1={33.9} x={130} y={1080} text="+ TUTOR DE IA EN TUS CLASES" bg="#fff" color={NAVY} size={54} />
    <Chip t0={32.28} t1={33.9} x={310} y={1220} text="ESCRÍBENOS" bg={COPPER} size={78} />
  </AbsoluteFill>
);

// ---------- gancho fijo, banda fija, subtítulo, cierre ----------
const HOOKS: Record<string, [string, string]> = {
  A: ["SOBREDIMENSIONAR NO ES", "IR POR EL LADO SEGURO"],
  B: ["¿QUIÉN PAGA TU PERFIL", "SOBREDIMENSIONADO?"],
  C: ["TU CLIENTE PAGA", "TU INSEGURIDAD"],
};
const Hook: React.FC<{ v: string }> = ({ v }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const [l1, l2] = HOOKS[v] ?? HOOKS.A;
  const k1 = sp(f, 0, "dry"), k2 = sp(f, 0.2, "dry");
  const out = lin(t, VOICE_END, 0.3);
  return (
    <AbsoluteFill style={{ opacity: 1 - out }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 330, background: "linear-gradient(180deg, rgba(5,12,26,0.9) 0%, rgba(5,12,26,0.6) 65%, rgba(5,12,26,0) 100%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 60, textAlign: "center", fontFamily: HEAD, lineHeight: 1.04 }}>
        <div style={{ fontSize: 90, color: "#fff", whiteSpace: "nowrap", opacity: k1, transform: `translateY(${(1 - k1) * -30}px)` }}>{l1}</div>
        <div style={{ fontSize: 98, color: COPPER_L, whiteSpace: "nowrap", opacity: k2, transform: `translateY(${(1 - k2) * -30}px)` }}>{l2}</div>
      </div>
    </AbsoluteFill>
  );
};
const OfferBand: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const pulse = 1 + 0.035 * Math.sin(Math.max(0, t - 32.2) * 7) * lin(t, 32.2, 0.3);
  return (
    <div style={{ position: "absolute", left: 0, top: BAND, width: 1080, height: 1920 - BAND, background: COPPER, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 2 }}>
      <div style={{ fontFamily: HEAD, fontSize: 80, color: "#fff", lineHeight: 1, transform: `scale(${pulse})`, textShadow: "0 4px 0 rgba(0,0,0,0.18)" }}>ESPECIALIZACIÓN EN ACERO</div>
      <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 36, color: NAVY }}>$225 USD · con tutor de IA · escríbenos</div>
    </div>
  );
};
type Wd = { w: string; s: number; e: number };
const FIX: Record<string, string> = { "guía": "IA", le: "TE" };
const CAPS = (() => {
  const ws = (WORDS as Wd[]).map((x) => {
    const c = x.w.replace(/[.,¿?¡!]/g, "");
    return { w: (FIX[c.toLowerCase()] ?? c).toUpperCase(), s: x.s, e: x.e };
  });
  const out: Wd[] = [];
  for (let i = 0; i < ws.length; i++) {
    const cur = ws[i];
    const nx = ws[i + 1];
    if (cur.w.length <= 2 && nx && nx.s - cur.e < 0.3 && cur.w !== "NO" && cur.w !== "IA") { out.push({ w: `${cur.w} ${nx.w}`, s: cur.s, e: nx.e }); i++; } else out.push(cur);
  }
  return out.map((c, i) => ({ ...c, w: c.w === "225" ? "$225" : c.w, e: Math.min(out[i + 1]?.s ?? c.e + 0.4, c.e + 0.4) }));
})();
const Caption: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  if (t >= VOICE_END) return null;
  const c = CAPS.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const k = lin(t, c.s - 0.03, 0.1);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: CAP_Y, display: "flex", justifyContent: "center" }}>
      <span style={{ fontFamily: HEAD, fontSize: c.w.length > 13 ? 80 : 96, lineHeight: 1, color: "#fff", padding: "12px 28px 2px", background: "rgba(10,22,36,0.85)", border: `4px solid ${COPPER}`, borderRadius: 12, transform: `scale(${0.88 + 0.12 * k})`, display: "inline-block" }}>{c.w}</span>
    </div>
  );
};
const End: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const d = lin(t, VOICE_END, 0.35);
  if (d <= 0) return null;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: NAVY, opacity: d * 0.97 }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 600, textAlign: "center", opacity: d }}>
        <Img src={staticFile("logo-dma.png")} style={{ width: 600 }} />
        <div style={{ fontFamily: HEAD, fontSize: 96, color: "#fff", marginTop: 40 }}>ESCRÍBENOS</div>
        <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COPPER_L }}>y te damos toda la información</div>
        <Img src={staticFile("atc.png")} style={{ width: 360, marginTop: 50, opacity: 0.9 }} />
      </div>
    </AbsoluteFill>
  );
};

const Reel: React.FC<{ v?: string }> = ({ v = "A" }) => (
  <AbsoluteFill style={{ background: NAVY }}>
    <Layer />
    <Broll />
    <BgTint />
    <Behind />
    <Layer fg />
    <Front />
    <Hook v={v} />
    <Caption />
    <OfferBand />
    <End />
  </AbsoluteFill>
);

export const MyComposition = () => (
  <Composition id="Reel" component={Reel} defaultProps={{ v: "A" }} durationInFrames={Math.round(TOTAL_S * FPS)} fps={FPS} width={1080} height={1920} />
);
