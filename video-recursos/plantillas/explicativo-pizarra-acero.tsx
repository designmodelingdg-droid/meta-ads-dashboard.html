import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import WORDS from "./words.json";

// Anuncio ACERO · «Sobredimensionar» · ficha de anuncios (patrones-virales-dma)
const PAPER = "#F4F1E6";
const INK = "#1B1B1B";
const RED = "#E5252A";
const COPPER = "#D78631";
const COPPER_L = "#E8A04A";
const NAVY = "#0D1E3A";
const NAVY2 = "#12305A";
const HEAD = "AntonDMA";
const BODY = "OverpassDMA";
const HAND = "KalamDMA";
loadFont({ family: HEAD, url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: HEAD, url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: BODY, url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });
loadFont({ family: HAND, url: staticFile("YA9Qr0Wd4kDdMtDqHTLMkiQ.woff2"), weight: "700" });
loadFont({ family: HAND, url: staticFile("YA9Qr0Wd4kDdMtDqHTLCkiQ4tg.woff2"), weight: "700", unicodeRange: "U+0100-024F" });

const FPS = 30;
const TOP = 300;          // gancho escrito, fijo
const BAND = 1640;        // banda de oferta, fija
const SEAM = 960;         // costura pizarra / Gabriel
const PH = SEAM - TOP;    // alto de la pizarra (660)
const VOICE_END = 33.9;
const TOTAL_S = 35.6;
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const useT = () => useCurrentFrame() / FPS;
const p = (t: number, t0: number, d = 0.3, e = EASE) =>
  interpolate(t, [t0, t0 + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });

// ---------- trazo a mano ----------
const rnd = (seed: number) => {
  const x = Math.sin(seed * 9301 + 49297) * 233280;
  return x - Math.floor(x);
};
type Pt = [number, number];
// línea con leve temblor, como marcador
const hand = (pts: Pt[], seed = 1, j = 3): string => {
  let d = `M${pts[0][0]},${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) {
    const [x0, y0] = pts[i - 1];
    const [x1, y1] = pts[i];
    const mx = (x0 + x1) / 2 + (rnd(seed + i) - 0.5) * j * 2;
    const my = (y0 + y1) / 2 + (rnd(seed + i * 7) - 0.5) * j * 2;
    d += ` Q${mx.toFixed(1)},${my.toFixed(1)} ${x1},${y1}`;
  }
  return d;
};
const rect = (x: number, y: number, w: number, h: number, seed = 1) =>
  hand([[x, y], [x + w, y + 2], [x + w - 2, y + h], [x + 2, y + h - 1], [x, y - 4]], seed, 4);
// círculo de marcador: pasa un poco de largo, como hecho a mano
const loop = (cx: number, cy: number, rx: number, ry: number, seed = 1): string => {
  const pts: Pt[] = [];
  for (let i = 0; i <= 26; i++) {
    const a = -0.5 + (i / 24) * Math.PI * 2;
    const k = 1 + (rnd(seed + i) - 0.5) * 0.06 + i * 0.004;
    pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
  }
  return hand(pts, seed, 2);
};

const Stroke: React.FC<{ d: string; t0: number; dur?: number; color?: string; w?: number; dash?: string; fill?: string }> = ({
  d, t0, dur = 0.3, color = INK, w = 6, dash, fill = "none",
}) => {
  const t = useT();
  const k = p(t, t0, dur, Easing.inOut(Easing.quad));
  if (k <= 0) return null;
  if (dash) {
    return <path d={d} stroke={color} strokeWidth={w} fill="none" strokeLinecap="round" strokeDasharray={dash} opacity={k} />;
  }
  return (
    <path d={d} pathLength={1} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round"
      fill={fill} strokeDasharray={1} strokeDashoffset={1 - k} />
  );
};
const Circle: React.FC<{ cx: number; cy: number; rx: number; ry: number; t0: number; seed?: number }> = ({ cx, cy, rx, ry, t0, seed = 3 }) => (
  <Stroke d={loop(cx, cy, rx, ry, seed)} t0={t0} dur={0.32} color={RED} w={8} />
);

// texto escrito a mano: se revela de izquierda a derecha
const Write: React.FC<{
  text: string; x: number; y: number; t0: number; size?: number; color?: string; dur?: number;
  align?: "left" | "center"; rot?: number; w?: number;
}> = ({ text, x, y, t0, size = 56, color = INK, dur, align = "left", rot = 0, w }) => {
  const t = useT();
  const d = dur ?? Math.min(0.55, 0.06 + text.length * 0.035);
  const k = p(t, t0, d, Easing.linear);
  if (k <= 0) return null;
  return (
    <div style={{
      position: "absolute", left: align === "center" ? 0 : x, width: align === "center" ? (w ?? 1080) : undefined,
      top: y, textAlign: align, fontFamily: HAND, fontWeight: 700, fontSize: size, color, lineHeight: 1.05,
      whiteSpace: "nowrap", clipPath: `inset(-20% ${(1 - k) * 100}% -20% -2%)`,
      transform: `rotate(${rot}deg)`, transformOrigin: "center",
      marginLeft: align === "center" ? x : 0,
    }}>{text}</div>
  );
};

// cada lámina de la pizarra: entra y sale levantándose
const Sheet: React.FC<{ a: number; b: number; children: React.ReactNode; exit?: boolean }> = ({ a, b, children, exit = true }) => {
  const t = useT();
  if (t < a - 0.05 || t > b + 0.02) return null;
  const out = exit ? p(t, b - 0.2, 0.2, Easing.in(Easing.quad)) : 0;
  const inn = p(t, a, 0.2);
  return (
    <AbsoluteFill style={{ opacity: Math.min(inn, 1 - out), transform: `translateY(${(1 - inn) * 24 - out * 40}px)` }}>
      {children}
    </AbsoluteFill>
  );
};
const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1080} height={PH} viewBox={`0 0 1080 ${PH}`} style={{ position: "absolute", inset: 0 }}>{children}</svg>
);

const Paper: React.FC = () => (
  <AbsoluteFill style={{ background: PAPER }}>
    <svg width={1080} height={PH} style={{ position: "absolute" }}>
      {Array.from({ length: 23 }).map((_, i) => (
        <line key={`v${i}`} x1={i * 48 + 12} y1={0} x2={i * 48 + 12} y2={PH} stroke="#CFCAB8" strokeWidth={1.2} />
      ))}
      {Array.from({ length: 21 }).map((_, i) => (
        <line key={`h${i}`} x1={0} y1={i * 48 + 20} x2={1080} y2={i * 48 + 20} stroke="#CFCAB8" strokeWidth={1.2} />
      ))}
    </svg>
    <div style={{ position: "absolute", inset: 0, boxShadow: "inset 0 0 120px rgba(120,100,60,0.18)" }} />
  </AbsoluteFill>
);

// ---------- dibujos propios (esquemas, sin cifras) ----------
const IBeam: React.FC<{ cx: number; cy: number; w: number; h: number; t0: number; color?: string; seed?: number }> = ({ cx, cy, w, h, t0, color = INK, seed = 500 }) => {
  const tf = Math.max(10, h * 0.12);
  const tw = Math.max(8, w * 0.12);
  const x0 = cx - w / 2, y0 = cy - h / 2;
  return (
    <g>
      <Stroke d={rect(x0, y0, w, tf, seed)} t0={t0} dur={0.18} w={6} color={color} />
      <Stroke d={rect(cx - tw / 2, y0 + tf, tw, h - 2 * tf, seed + 1)} t0={t0 + 0.12} dur={0.18} w={6} color={color} />
      <Stroke d={rect(x0, y0 + h - tf, w, tf, seed + 2)} t0={t0 + 0.24} dur={0.18} w={6} color={color} />
    </g>
  );
};
const Face: React.FC<{ cx: number; cy: number; t0: number; sad?: boolean }> = ({ cx, cy, t0, sad }) => (
  <g>
    <Stroke d={loop(cx, cy, 52, 52, 520)} t0={t0} dur={0.22} w={7} />
    <Stroke d={loop(cx - 18, cy - 10, 4, 4, 521)} t0={t0 + 0.2} dur={0.05} w={7} />
    <Stroke d={loop(cx + 18, cy - 10, 4, 4, 522)} t0={t0 + 0.2} dur={0.05} w={7} />
    <Stroke d={sad ? `M${cx - 22},${cy + 26} q22,-18 44,0` : `M${cx - 22},${cy + 16} q22,18 44,0`} t0={t0 + 0.28} dur={0.12} w={7} color={sad ? RED : INK} />
  </g>
);

// lámina 1 · el perfil sobredimensionado y quién paga (5.41 – 13.9)
const L1: React.FC = () => (
  <Sheet a={5.41} b={13.9}>
    <Svg>
      <IBeam cx={170} cy={250} w={110} h={150} t0={5.6} seed={530} />
      <IBeam cx={420} cy={250} w={190} h={290} t0={6.4} seed={540} color={RED} />
      <Stroke d={hand([[260, 330], [300, 210]], 550, 2)} t0={6.9} dur={0.2} w={7} color={RED} />
      <Stroke d={`M280,228 L300,210 L312,236`} t0={7.05} dur={0.08} w={7} color={RED} />
      {/* factura */}
      <Stroke d={hand([[650, 110], [900, 112], [902, 400], [876, 386], [850, 400], [824, 386], [798, 400], [772, 386], [746, 400], [720, 386], [694, 400], [650, 398], [650, 110]], 551, 2)} t0={8.48} dur={0.4} w={6} />
      {[180, 225, 270].map((y, i) => <Stroke key={y} d={hand([[680, y], [870 - i * 40, y + 2]], 552 + i, 1)} t0={8.8 + i * 0.06} dur={0.1} w={4} color="#5A554B" />)}
      <Face cx={790} cy={492} t0={12.1} sad />
      <Circle cx={790} cy={492} rx={90} ry={86} t0={12.58} seed={16} />
    </Svg>
    <Write text="el justo" x={95} y={350} t0={5.6} size={44} />
    <Write text="sobredimensionado" x={290} y={420} t0={6.6} size={44} color={RED} />
    <Write text="$$$" x={700} y={300} t0={9.08} size={70} color={RED} />
    <Write text="factura" x={705} y={45} t0={9.08} size={52} />
    <Write text="+ peso" x={90} y={500} t0={10.16} size={58} color={RED} />
    <Write text="+ soldadura" x={300} y={500} t0={10.98} size={58} color={RED} />
    <Write text="tu cliente" x={705} y={556} t0={12.1} size={44} />
  </Sheet>
);

// lámina 2 · el camino correcto: criterio (13.9 – 22.14)
const L2: React.FC = () => (
  <Sheet a={13.9} b={22.2} exit={false}>
    <Svg>
      <IBeam cx={170} cy={230} w={70} h={100} t0={14.3} seed={560} />
      <Stroke d={hand([[120, 170], [220, 290]], 561, 1)} t0={15.26} dur={0.1} w={9} color={RED} />
      <Stroke d={hand([[220, 170], [120, 290]], 562, 1)} t0={15.34} dur={0.1} w={9} color={RED} />
      <IBeam cx={830} cy={230} w={190} h={290} t0={14.5} seed={563} color="#9A9488" />
      <Stroke d={hand([[740, 90], [920, 380]], 564, 1)} t0={15.0} dur={0.1} w={9} color={RED} />
      <IBeam cx={500} cy={260} w={130} h={190} t0={16.6} seed={565} />
      <Stroke d={hand([[560, 410], [590, 440], [640, 380]], 566, 1)} t0={18.62} dur={0.15} w={10} color={COPPER} />
      <Circle cx={500} cy={500} rx={170} ry={56} t0={20.1} seed={17} />
    </Svg>
    <Write text="arriesgar" x={90} y={320} t0={15.26} size={46} color={RED} />
    <Write text="sobredimensionar" x={680} y={410} t0={15.0} size={40} color="#5A554B" />
    <Write text="el perfil justo" x={380} y={40} t0={16.6} size={56} />
    <Write text="criterio" x={410} y={470} t0={20.1} size={62} color={COPPER} />
    <Write text="lo enseñamos en la Especialización en Acero" x={0} align="center" y={575} t0={20.56} size={40} />
  </Sheet>
);

// ---------- presentador ----------
const CLIPS = [
  { a: 0, faceY: 560, s: 1.0 },
  { a: 5.41, faceY: 520, s: 1.0 },
  { a: 13.9, faceY: 660, s: 1.3 },
  { a: 22.14, faceY: 650, s: 1.0 },
];
const clipAt = (t: number) => [...CLIPS].reverse().find((c) => t >= c.a) ?? CLIPS[0];
const PUNCH = [7.98, 11.96, 17.3, 26.46, 32.28];
const splitAmt = (t: number) => p(t, 5.41, 0.32) - p(t, 22.14, 0.28);
const Presenter: React.FC = () => {
  const t = useT();
  const c = clipAt(t);
  const m = splitAmt(t);
  const punch = PUNCH.filter((x) => t >= x).length % 2 === 1 ? 1.07 : 1;
  const sFull = c.s * punch * (1 + 0.04 * p(t, c.a, 6, Easing.linear));
  const tyFull = 720 - c.faceY * sFull;   // cara en y≈720 con la pantalla completa
  const sSplit = c.s * punch;
  const tySplit = 1200 - c.faceY * sSplit; // cara en y≈1200 con la pizarra arriba
  const s = sFull + (sSplit - sFull) * m;
  const ty = tyFull + (tySplit - tyFull) * m;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `translateY(${ty}px) scale(${s})`, transformOrigin: "50% 0" }}>
        <Video src={staticFile("gabriel_editado.mp4")} style={{ width: 1080, height: 1920 }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
const Board: React.FC = () => {
  const t = useT();
  const m = splitAmt(t);
  if (m <= 0) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: TOP, width: 1080, height: PH, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${-PH * (1 - m)}px)` }}>
        <Paper />
        <L1 />
        <L2 />
      </div>
    </div>
  );
};

// ---------- gancho fijo, oferta fija, subtítulos ----------
const HOOKS: Record<string, [string, string]> = {
  A: ["SOBREDIMENSIONAR NO ES", "IR POR EL LADO SEGURO"],
  B: ["¿QUIÉN PAGA TU PERFIL", "SOBREDIMENSIONADO?"],
  C: ["TU CLIENTE PAGA", "TU INSEGURIDAD"],
};
const Blur: React.FC<{ children: React.ReactNode; t0: number }> = ({ children, t0 }) => {
  const t = useT();
  const k = p(t, t0, 0.18);
  return <span style={{ display: "inline-block", opacity: k, filter: `blur(${(1 - k) * 12}px)`, transform: `translateY(${(1 - k) * 10}px)` }}>{children}</span>;
};
const TopBand: React.FC<{ v: string }> = ({ v }) => {
  const [l1, l2] = HOOKS[v] ?? HOOKS.A;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: TOP, background: `radial-gradient(ellipse at 50% 30%, ${NAVY2} 0%, ${NAVY} 75%)`, textAlign: "center", fontFamily: HEAD, lineHeight: 1.04 }}>
      <div style={{ paddingTop: 52, fontSize: 92, color: "#fff", whiteSpace: "nowrap" }}><Blur t0={0}>{l1}</Blur></div>
      <div style={{ fontSize: 100, color: COPPER_L, whiteSpace: "nowrap" }}><Blur t0={0.25}>{l2}</Blur></div>
    </div>
  );
};
const OfferBand: React.FC = () => {
  const t = useT();
  const pulse = 1 + 0.035 * Math.sin(Math.max(0, t - 32.2) * 7) * p(t, 32.2, 0.3);
  return (
    <div style={{ position: "absolute", left: 0, top: BAND, width: 1080, height: 1920 - BAND, background: COPPER, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
      <div style={{ fontFamily: HEAD, fontSize: 82, color: "#fff", lineHeight: 1, transform: `scale(${pulse})`, textShadow: "0 4px 0 rgba(0,0,0,0.18)" }}>ESPECIALIZACIÓN EN ACERO</div>
      <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 36, color: NAVY }}>$225 USD · con tutor de IA · escríbenos</div>
    </div>
  );
};
type Wd = { w: string; s: number; e: number };
const FIX: Record<string, string> = { "guía": "IA", le: "TE" };
const KEY = /SOBREDIMENSION|FACTURA|PESO|SOLDADURA|CLIENTE|CRITERIO|ACERO|225|TUTOR|IA|ESCRÍBENOS|PERFIL|INSEGURIDAD/;
const CAPS = (() => {
  const ws = (WORDS as Wd[]).map((x) => {
    const c = x.w.replace(/[.,¿?¡!]/g, "");
    return { w: (FIX[c.toLowerCase()] ?? c).toUpperCase(), s: x.s, e: x.e };
  });
  const out: Wd[] = [];
  for (let i = 0; i < ws.length; i++) {
    const cur = ws[i];
    const nx = ws[i + 1];
    if (cur.w.length <= 2 && nx && nx.s - cur.e < 0.3 && cur.w !== "NO" && cur.w !== "IA") {
      out.push({ w: `${cur.w} ${nx.w}`, s: cur.s, e: nx.e });
      i++;
    } else out.push(cur);
  }
  return out.map((c, i) => ({ ...c, w: c.w === "225" ? "$225" : c.w, e: Math.min(out[i + 1]?.s ?? c.e + 0.4, c.e + 0.4) }));
})();
const Caption: React.FC = () => {
  const t = useT();
  const c = CAPS.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const m = splitAmt(t);
  const k = p(t, c.s - 0.03, 0.1);
  const key = KEY.test(c.w);
  if (m > 0.98) {
    return (
      <div style={{ position: "absolute", left: 0, right: 0, top: SEAM - 52, display: "flex", justifyContent: "center" }}>
        <div style={{ minWidth: 560, height: 104, background: COPPER, borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center", padding: "0 34px", transform: `scale(${0.9 + 0.1 * k})`, boxShadow: "0 8px 22px rgba(0,0,0,0.35)" }}>
          <span style={{ fontFamily: BODY, fontWeight: 800, fontSize: 60, color: "#fff", WebkitTextStroke: `7px ${NAVY}`, paintOrder: "stroke fill", lineHeight: 1, marginTop: 8 }}>{c.w}</span>
        </div>
      </div>
    );
  }
  if (m > 0.02) return null;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1450, display: "flex", justifyContent: "center" }}>
      <span style={{
        fontFamily: HEAD, fontSize: 104, lineHeight: 1, color: "#fff", padding: key ? "10px 28px 4px" : "10px 0 4px",
        background: key ? COPPER : "transparent", borderRadius: 10, transform: `scale(${0.9 + 0.1 * k})`, display: "inline-block",
        WebkitTextStroke: key ? undefined : `5px ${NAVY}`, paintOrder: "stroke fill", textShadow: key ? "0 8px 22px rgba(0,0,0,0.35)" : "0 6px 20px rgba(0,0,0,0.5)",
      }}>{c.w}</span>
    </div>
  );
};

// ---------- cierre de venta (pantalla completa) ----------
const Offer: React.FC = () => {
  const t = useT();
  if (t < 22.4) return null;
  const k1 = p(t, 22.88, 0.25);
  const k2 = p(t, 24.7, 0.2, Easing.out(Easing.back(2)));
  const k3 = p(t, 29.2, 0.25);
  const dim = p(t, VOICE_END, 0.35);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 60, top: TOP + 40, opacity: k1, transform: `translateX(${(1 - k1) * -40}px)` }}>
        <span style={{ display: "inline-block", background: NAVY, color: COPPER_L, fontFamily: BODY, fontWeight: 800, fontSize: 34, letterSpacing: 3, padding: "10px 22px", borderRadius: 12 }}>ESPECIALIZACIÓN EN ACERO</span>
      </div>
      {t >= 24.7 && (
        <div style={{ position: "absolute", right: 50, top: TOP + 130, transform: `rotate(-4deg) scale(${interpolate(k2, [0, 1], [1.6, 1])})`, opacity: Math.min(1, k2 * 2) }}>
          <div style={{ background: COPPER, color: "#fff", fontFamily: HEAD, fontSize: 150, lineHeight: 1, padding: "16px 34px 6px", borderRadius: 18, boxShadow: "0 18px 40px rgba(0,0,0,0.45)" }}>$225</div>
          <div style={{ textAlign: "center", fontFamily: BODY, fontWeight: 800, fontSize: 34, color: "#fff", marginTop: 8, textShadow: "0 3px 10px rgba(0,0,0,0.6)" }}>USD</div>
        </div>
      )}
      {t >= 29.2 && (
        <div style={{ position: "absolute", left: 60, top: 1300, opacity: k3, transform: `translateY(${(1 - k3) * 20}px)` }}>
          <span style={{ display: "inline-block", background: "#fff", color: NAVY, fontFamily: BODY, fontWeight: 800, fontSize: 40, padding: "12px 24px", borderRadius: 14, boxShadow: "0 12px 30px rgba(0,0,0,0.35)" }}>+ tutor de IA dentro de tus clases</span>
        </div>
      )}
      <AbsoluteFill style={{ background: NAVY, opacity: dim * 0.97 }} />
      {dim > 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 700, textAlign: "center", opacity: dim }}>
          <Img src={staticFile("logo-dma.png")} style={{ width: 620 }} />
          <div style={{ fontFamily: HEAD, fontSize: 96, color: "#fff", marginTop: 40 }}>ESCRÍBENOS</div>
          <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COPPER_L }}>y te damos toda la información</div>
        </div>
      )}
    </AbsoluteFill>
  );
};
const Shade: React.FC = () => {
  const t = useT();
  const m = splitAmt(t);
  return <AbsoluteFill style={{ opacity: 1 - m, background: "linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,0.55) 75%, rgba(0,0,0,0.65) 85%)" }} />;
};

const Reel: React.FC<{ v?: string }> = ({ v = "A" }) => (
  <AbsoluteFill style={{ background: NAVY }}>
    <Presenter />
    <Shade />
    <Board />
    <Offer />
    <TopBand v={v} />
    <Caption />
    <OfferBand />
  </AbsoluteFill>
);

export const MyComposition = () => (
  <Composition id="Reel" component={Reel} defaultProps={{ v: "A" }} durationInFrames={Math.round(TOTAL_S * FPS)} fps={FPS} width={1080} height={1920} />
);
