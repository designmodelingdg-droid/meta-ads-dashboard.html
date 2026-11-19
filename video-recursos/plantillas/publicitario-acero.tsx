import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import WORDS from "./words.json";

// Anuncio ACERO · «Sobredimensionar» · estilo 6 PUBLICITARIO (estilos-reels-dma)
// Gabriel a pantalla completa todo el video, cortes con zoom, insertos gráficos
// a pantalla completa como B-roll, subtítulo de 1 palabra en caja cobre a media altura,
// rótulo «TIP CLAVE», gancho fijo arriba y banda de oferta fija abajo (ficha de anuncios).
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

const FPS = 30;
const BAND = 1700;
const CAP_Y = 1170;
const VOICE_END = 33.9;
const TOTAL_S = 35.6;
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const useT = () => useCurrentFrame() / FPS;
const p = (t: number, t0: number, d = 0.3, e = EASE) =>
  interpolate(t, [t0, t0 + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });

// ---------- insertos (B-roll gráfico a pantalla completa) ----------
const INSERTS: [number, number][] = [
  [6.55, 7.95],   // perfil justo vs sobredimensionado
  [8.95, 9.9],    // la factura
  [10.4, 11.74],  // + peso + soldadura
  [14.85, 16.15], // ni sobredimensionar ni arriesgar
];
const inInsert = (t: number) => INSERTS.some(([a, b]) => t >= a && t < b);

const Grid: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, #13305A 0%, ${NAVY_D} 70%)` }}>
    <svg width={1080} height={1920} style={{ position: "absolute", opacity: 0.16 }}>
      {Array.from({ length: 24 }).map((_, i) => <line key={`v${i}`} x1={i * 48} y1={0} x2={i * 48} y2={1920} stroke="#9FB0C8" strokeWidth={1} />)}
      {Array.from({ length: 41 }).map((_, i) => <line key={`h${i}`} x1={0} y1={i * 48} x2={1080} y2={i * 48} stroke="#9FB0C8" strokeWidth={1} />)}
    </svg>
  </AbsoluteFill>
);
const Insert: React.FC<{ a: number; b: number; children: React.ReactNode }> = ({ a, b, children }) => {
  const t = useT();
  if (t < a || t >= b) return null;
  const k = p(t, a, 0.14);
  return (
    <AbsoluteFill style={{ transform: `scale(${1.12 - 0.12 * k})`, filter: `blur(${(1 - k) * 10}px)` }}>
      <Grid />
      {children}
    </AbsoluteFill>
  );
};
const Pop: React.FC<{ t0: number; children: React.ReactNode; style?: React.CSSProperties; back?: boolean }> = ({ t0, children, style, back }) => {
  const t = useT();
  const k = p(t, t0, 0.18, back ? Easing.out(Easing.back(2.2)) : EASE);
  if (t < t0) return null;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, textAlign: "center", opacity: Math.min(1, k * 2), filter: `blur(${Math.max(0, 1 - k * 1.5) * 12}px)`, transform: `translateY(${(1 - k) * 14}px) scale(${back ? interpolate(k, [0, 1], [1.5, 1]) : 1})`, ...style }}>
      {children}
    </div>
  );
};
const Beam: React.FC<{ w: number; h: number; color: string }> = ({ w, h, color }) => {
  const tf = h * 0.13;
  const tw = w * 0.13;
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <rect x={0} y={0} width={w} height={tf} rx={4} fill={color} />
      <rect x={(w - tw) / 2} y={tf - 1} width={tw} height={h - 2 * tf + 2} fill={color} />
      <rect x={0} y={h - tf} width={w} height={tf} rx={4} fill={color} />
    </svg>
  );
};
const BIG: React.CSSProperties = { fontFamily: HEAD, color: "#fff", lineHeight: 1 };

const I1: React.FC = () => {
  const t = useT();
  const g = p(t, 6.6, 0.9, Easing.out(Easing.cubic));
  return (
    <Insert a={6.55} b={7.95}>
      <div style={{ position: "absolute", left: 90, top: 1020, width: 240, textAlign: "center" }}>
        <Beam w={150} h={210} color="#fff" />
        <div style={{ fontFamily: HEAD, fontSize: 60, color: "#fff", marginTop: 26, lineHeight: 1 }}>EL JUSTO</div>
      </div>
      <div style={{ position: "absolute", left: 410, top: 1230 - 470 * (0.55 + 0.45 * g), width: 560, textAlign: "center" }}>
        <div style={{ display: "inline-block", transform: `scale(${0.55 + 0.45 * g})`, transformOrigin: "50% 100%" }}>
          <Beam w={340} h={470} color={COPPER} />
        </div>
      </div>
      <Pop t0={6.6} style={{ top: 1256, left: 360, right: 0 }}><span style={{ ...BIG, fontSize: 78, color: COPPER_L }}>SOBREDIMENSIONADO</span></Pop>
    </Insert>
  );
};
const I2: React.FC = () => (
  <Insert a={8.95} b={9.9}>
    <div style={{ position: "absolute", left: 250, top: 560, width: 580, height: 760, background: "#fff", borderRadius: 18, transform: "rotate(-4deg)", boxShadow: "0 30px 70px rgba(0,0,0,0.5)", padding: "56px 56px" }}>
      <div style={{ fontFamily: HEAD, fontSize: 96, color: NAVY, lineHeight: 1 }}>FACTURA</div>
      {[0, 1, 2, 3].map((i) => (
        <div key={i} style={{ display: "flex", justifyContent: "space-between", marginTop: 44 }}>
          <div style={{ width: 260 - i * 30, height: 22, borderRadius: 11, background: "#D5DAE2" }} />
          <div style={{ width: 90, height: 22, borderRadius: 11, background: "#D5DAE2" }} />
        </div>
      ))}
    </div>
    <Pop t0={9.08} back style={{ top: 1000 }}>
      <span style={{ ...BIG, display: "inline-block", fontSize: 230, color: RED, border: `12px solid ${RED}`, borderRadius: 24, padding: "20px 40px 0", transform: "rotate(-10deg)", background: "rgba(255,255,255,0.92)" }}>$$$</span>
    </Pop>
  </Insert>
);
const I3: React.FC = () => (
  <Insert a={10.4} b={11.74}>
    <Pop t0={10.45} back style={{ top: 700 }}>
      <span style={{ ...BIG, display: "inline-block", fontSize: 190, background: RED, padding: "26px 50px 6px", borderRadius: 20 }}>+ PESO</span>
    </Pop>
    <Pop t0={10.98} back style={{ top: 1000 }}>
      <span style={{ ...BIG, display: "inline-block", fontSize: 150, background: COPPER, padding: "24px 44px 4px", borderRadius: 20 }}>+ SOLDADURA</span>
    </Pop>
  </Insert>
);
const Strike: React.FC<{ t0: number; top: number; text: string; size: number }> = ({ t0, top, text, size }) => {
  const t = useT();
  const k = p(t, t0 + 0.12, 0.16, Easing.out(Easing.quad));
  return (
    <Pop t0={t0} style={{ top }}>
      <span style={{ position: "relative", display: "inline-block" }}>
        <span style={{ ...BIG, fontSize: size, opacity: 0.85 }}>{text}</span>
        <span style={{ position: "absolute", left: -20, right: -20, top: "48%", height: 16, background: RED, borderRadius: 8, transform: `scaleX(${k}) rotate(-4deg)`, transformOrigin: "0 50%" }} />
      </span>
      <span style={{ ...BIG, fontSize: size, color: RED, marginLeft: 30, opacity: k }}>✗</span>
    </Pop>
  );
};
const I4: React.FC = () => (
  <Insert a={14.85} b={16.15}>
    <Strike t0={14.9} top={760} text="SOBREDIMENSIONAR" size={118} />
    <Strike t0={15.26} top={1000} text="ARRIESGAR" size={150} />
  </Insert>
);

// ---------- presentador: cortes con zoom ----------
const CLIPS = [
  { a: 0, faceY: 560, s: 1.0 },
  { a: 5.41, faceY: 520, s: 1.0 },
  { a: 13.9, faceY: 660, s: 1.3 },
  { a: 22.14, faceY: 650, s: 1.0 },
];
const clipAt = (t: number) => [...CLIPS].reverse().find((c) => t >= c.a) ?? CLIPS[0];
// corte seco con cambio de plano cada ~2 s, al inicio de cada frase
const PUNCH: [number, number][] = [
  [0, 1.0], [2.52, 1.14], [5.41, 1.0], [7.95, 1.16], [9.9, 1.06], [11.74, 1.0], [12.58, 1.2], [13.9, 1.0],
  [16.15, 1.12], [17.46, 1.0], [19.08, 1.15], [20.56, 1.06], [22.14, 1.0], [24.28, 1.12], [26.46, 1.0],
  [28.64, 1.12], [30.38, 1.04], [32.28, 1.0],
];
const Presenter: React.FC = () => {
  const t = useT();
  const c = clipAt(t);
  const pu = [...PUNCH].reverse().find((x) => t >= x[0]) ?? PUNCH[0];
  const s = c.s * pu[1] * (1 + 0.03 * p(t, pu[0], 2.5, Easing.linear));
  const ty = 760 - c.faceY * s;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `translateY(${ty}px) scale(${s})`, transformOrigin: "50% 0" }}>
        <Video src={staticFile("gabriel_editado.mp4")} style={{ width: 1080, height: 1920 }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- gancho fijo arriba (sobre el video), oferta fija abajo ----------
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
const Hook: React.FC<{ v: string }> = ({ v }) => {
  const t = useT();
  const [l1, l2] = HOOKS[v] ?? HOOKS.A;
  const out = p(t, VOICE_END, 0.3);
  return (
    <AbsoluteFill style={{ opacity: 1 - out }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 440, background: "linear-gradient(180deg, rgba(5,12,26,0.82) 0%, rgba(5,12,26,0.55) 60%, rgba(5,12,26,0) 100%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 70, textAlign: "center", fontFamily: HEAD, lineHeight: 1.04, textShadow: "0 6px 18px rgba(0,0,0,0.55)" }}>
        <div style={{ fontSize: 92, color: "#fff", whiteSpace: "nowrap" }}><Blur t0={0}>{l1}</Blur></div>
        <div style={{ fontSize: 100, color: COPPER_L, whiteSpace: "nowrap" }}><Blur t0={0.25}>{l2}</Blur></div>
      </div>
    </AbsoluteFill>
  );
};
const OfferBand: React.FC = () => {
  const t = useT();
  const pulse = 1 + 0.035 * Math.sin(Math.max(0, t - 32.2) * 7) * p(t, 32.2, 0.3);
  return (
    <div style={{ position: "absolute", left: 0, top: BAND, width: 1080, height: 1920 - BAND, background: COPPER, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 2 }}>
      <div style={{ fontFamily: HEAD, fontSize: 80, color: "#fff", lineHeight: 1, transform: `scale(${pulse})`, textShadow: "0 4px 0 rgba(0,0,0,0.18)" }}>ESPECIALIZACIÓN EN ACERO</div>
      <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 36, color: NAVY }}>$225 USD · con tutor de IA · escríbenos</div>
    </div>
  );
};

// ---------- subtítulo: 1 palabra en caja cobre, a media altura ----------
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
    if (cur.w.length <= 2 && nx && nx.s - cur.e < 0.3 && cur.w !== "NO" && cur.w !== "IA") {
      out.push({ w: `${cur.w} ${nx.w}`, s: cur.s, e: nx.e });
      i++;
    } else out.push(cur);
  }
  return out.map((c, i) => ({ ...c, w: c.w === "225" ? "$225" : c.w, e: Math.min(out[i + 1]?.s ?? c.e + 0.4, c.e + 0.4) }));
})();
const Caption: React.FC = () => {
  const t = useT();
  if (inInsert(t) || t >= VOICE_END) return null;
  const c = CAPS.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const k = p(t, c.s - 0.03, 0.1);
  const long = c.w.length > 13;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: CAP_Y, display: "flex", justifyContent: "center" }}>
      <span style={{
        fontFamily: HEAD, fontSize: long ? 84 : 104, lineHeight: 1, color: "#fff", padding: "14px 30px 4px", background: COPPER,
        borderRadius: 10, transform: `scale(${0.88 + 0.12 * k})`, display: "inline-block", boxShadow: "0 10px 26px rgba(0,0,0,0.4)",
      }}>{c.w}</span>
    </div>
  );
};

// ---------- rótulo «TIP CLAVE» ----------
const Tip: React.FC = () => {
  const t = useT();
  if (t < 16.15 || t >= 22.14) return null;
  const k = p(t, 16.15, 0.22, Easing.out(Easing.back(1.8)));
  const k2 = p(t, 18.6, 0.25);
  const k3 = p(t, 20.8, 0.25);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 60, top: 470, transform: `scale(${k}) rotate(-3deg)`, transformOrigin: "0 50%" }}>
        <span style={{ display: "inline-block", background: RED, color: "#fff", fontFamily: HEAD, fontSize: 64, padding: "14px 28px 4px", borderRadius: 12, boxShadow: "0 10px 24px rgba(0,0,0,0.4)" }}>TIP CLAVE</span>
      </div>
      {t >= 18.6 && (
        <div style={{ position: "absolute", left: 60, right: 60, top: 1360, opacity: k2, transform: `translateY(${(1 - k2) * 24}px)` }}>
          <div style={{ background: "#fff", borderRadius: 18, padding: "22px 30px", boxShadow: "0 14px 34px rgba(0,0,0,0.4)", textAlign: "center" }}>
            <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 44, color: NAVY, lineHeight: 1.15 }}>
              Elige el perfil con <span style={{ color: COPPER }}>criterio</span> ✓
            </div>
            <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 30, color: "#64748B", marginTop: 6, opacity: k3 }}>lo enseñamos en la Especialización en Acero</div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

// ---------- cierre de venta ----------
const Offer: React.FC = () => {
  const t = useT();
  if (t < 22.4) return null;
  const k1 = p(t, 22.88, 0.25);
  const k2 = p(t, 24.7, 0.2, Easing.out(Easing.back(2)));
  const k3 = p(t, 29.2, 0.25);
  const dim = p(t, VOICE_END, 0.35);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 60, top: 460, opacity: k1, transform: `translateX(${(1 - k1) * -40}px)` }}>
        <span style={{ display: "inline-block", background: NAVY, color: COPPER_L, fontFamily: BODY, fontWeight: 800, fontSize: 34, letterSpacing: 3, padding: "10px 22px", borderRadius: 12 }}>ESPECIALIZACIÓN EN ACERO</span>
      </div>
      {t >= 24.7 && (
        <div style={{ position: "absolute", right: 50, top: 560, transform: `rotate(-4deg) scale(${interpolate(k2, [0, 1], [1.6, 1])})`, opacity: Math.min(1, k2 * 2) }}>
          <div style={{ background: COPPER, color: "#fff", fontFamily: HEAD, fontSize: 150, lineHeight: 1, padding: "16px 34px 6px", borderRadius: 18, boxShadow: "0 18px 40px rgba(0,0,0,0.45)" }}>$225</div>
          <div style={{ textAlign: "center", fontFamily: BODY, fontWeight: 800, fontSize: 34, color: "#fff", marginTop: 8, textShadow: "0 3px 10px rgba(0,0,0,0.6)" }}>USD</div>
        </div>
      )}
      {t >= 29.2 && (
        <div style={{ position: "absolute", left: 60, top: 1400, opacity: k3, transform: `translateY(${(1 - k3) * 20}px)` }}>
          <span style={{ display: "inline-block", background: "#fff", color: NAVY, fontFamily: BODY, fontWeight: 800, fontSize: 40, padding: "12px 24px", borderRadius: 14, boxShadow: "0 12px 30px rgba(0,0,0,0.35)" }}>+ tutor de IA dentro de tus clases</span>
        </div>
      )}
      <AbsoluteFill style={{ background: NAVY, opacity: dim * 0.97 }} />
      {dim > 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 640, textAlign: "center", opacity: dim }}>
          <Img src={staticFile("logo-dma.png")} style={{ width: 620 }} />
          <div style={{ fontFamily: HEAD, fontSize: 96, color: "#fff", marginTop: 40 }}>ESCRÍBENOS</div>
          <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COPPER_L }}>y te damos toda la información</div>
        </div>
      )}
    </AbsoluteFill>
  );
};
const Shade: React.FC = () => (
  <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 80%, rgba(0,0,0,0.5) 88%)" }} />
);

const Reel: React.FC<{ v?: string }> = ({ v = "A" }) => (
  <AbsoluteFill style={{ background: NAVY }}>
    <Presenter />
    <Shade />
    <Tip />
    <Offer />
    <I1 />
    <I2 />
    <I3 />
    <I4 />
    <Hook v={v} />
    <Caption />
    <OfferBand />
  </AbsoluteFill>
);

export const MyComposition = () => (
  <Composition id="Reel" component={Reel} defaultProps={{ v: "A" }} durationInFrames={Math.round(TOTAL_S * FPS)} fps={FPS} width={1080} height={1920} />
);
