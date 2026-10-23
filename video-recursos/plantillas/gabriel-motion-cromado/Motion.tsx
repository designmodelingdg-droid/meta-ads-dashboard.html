import React from "react";
import { AbsoluteFill, Easing, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/fonts";
import { GUION, Elemento } from "./guion";

/*
 * Estilo 10 · «Gabriel motion cromado» (estilos-reels-dma) — para PAUTA con Gabriel a cámara.
 * Motor: no se toca por reel; todo lo de cada video está en guion.ts.
 * Palabras clave en cromo 3D con los colores de DMA (cobre / navy) delante o DETRÁS de Gabriel,
 * palabras pequeñas en cobre claro que entran con desenfoque, íconos 3D que rebotan,
 * transiciones: zoom con desenfoque, cortina de puntos a estudio navy, destello cobre,
 * golpes de zoom y contador circular.
 */
const FPS = 30;
export const TOTAL = GUION.total;
const HEAD = "AntonDMA";
const BODY = "OverpassDMA";
loadFont({ family: HEAD, url: staticFile("anton-latin-400-normal.woff2"), weight: "400" });
loadFont({ family: HEAD, url: staticFile("anton-latin-ext-400-normal.woff2"), weight: "400", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-800-normal.woff2"), weight: "800" });
loadFont({ family: BODY, url: staticFile("overpass-latin-ext-800-normal.woff2"), weight: "800", unicodeRange: "U+0100-024F" });
loadFont({ family: BODY, url: staticFile("overpass-latin-600-normal.woff2"), weight: "600" });

// paleta DMA
const NAVY = "#0D1E3A";
const NAVY_2 = "#13305A";
const COBRE = "#D78631";
const COBRE_C = "#F3B26B";
const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const p = (t: number, t0: number, d = 0.3, e = EASE) => interpolate(t, [t0, t0 + d], [0, 1], { ...clamp, easing: e });
const bell = (t: number, c: number, w: number) => Math.max(0, 1 - Math.abs(t - c) / w);
const useT = () => useCurrentFrame() / FPS;

// ---------- cámara (la misma para el fondo y el recorte) ----------
const camara = (t: number) => {
  let s = 1 + 0.035 * ((t % 4) / 4);
  let blur = 0;
  // empujes: se quedan hasta el siguiente whip/estudio
  for (const e of GUION.empujes) {
    const fin = Math.min(...[...GUION.whips, GUION.estudio?.in ?? 1e9, GUION.total].filter((x) => x > e.t));
    if (t >= e.t && t < fin) s += (e.escala - 1) * p(t, e.t, 0.25);
  }
  for (const w of GUION.whips) {
    if (t >= w - 0.14 && t < w) { const k = p(t, w - 0.14, 0.14, Easing.in(Easing.cubic)); s += 0.35 * k; blur = Math.max(blur, 18 * k); }
    if (t >= w && t < w + 0.22) { const k = 1 - p(t, w, 0.22); s += 0.35 * k; blur = Math.max(blur, 18 * k); }
  }
  let shake = 0;
  for (const g of GUION.golpes) { s += 0.1 * (g.fuerza ?? 1) * bell(t, g.t, 0.18); shake = Math.max(shake, bell(t, g.t, 0.2) * 10 * (g.fuerza ?? 1)); }
  for (const z of GUION.zoomFuera) if (t >= z && t < z + 1.6) s = 1.2 - 0.2 * p(t, z, 0.9);
  return { s, blur, dx: Math.sin(t * 90) * shake, dy: Math.cos(t * 77) * shake };
};

const Capa: React.FC<{ alfa?: boolean }> = ({ alfa }) => {
  const c = camara(useT());
  return (
    <AbsoluteFill style={{ transform: `translate(${c.dx}px, ${c.dy}px) scale(${c.s})`, transformOrigin: "50% 38%", filter: c.blur > 0.3 ? `blur(${c.blur}px)` : undefined }}>
      {alfa
        ? <OffthreadVideo src={staticFile(GUION.alfa)} transparent muted style={{ width: 1080, height: 1920 }} />
        : <OffthreadVideo src={staticFile(GUION.video)} style={{ width: 1080, height: 1920 }} />}
    </AbsoluteFill>
  );
};

// ---------- texto cromado 3D en colores DMA ----------
const CARAS = {
  cobre: { cara: "linear-gradient(180deg,#fff4e3 0%,#f6c58c 28%,#c0712e 50%,#ffd9a6 60%,#d98a3f 82%,#8f4b1b 100%)", canto: ["#b8692a", "#7f4317", "#3a1e0a"], borde: "rgba(255,240,220,.7)" },
  navy: { cara: "linear-gradient(180deg,#9fb7d9 0%,#3d6296 26%,#13305A 50%,#4f78ad 60%,#1c3d6e 80%,#0D1E3A 100%)", canto: ["#0D1E3A", "#081428", "#030810"], borde: "rgba(255,255,255,.95)" },
  blanco: { cara: "linear-gradient(180deg,#ffffff 0%,#f3f6f9 40%,#c9d3de 52%,#ffffff 64%,#dfe6ee 100%)", canto: ["#b7c3cf", "#6f8094", NAVY], borde: "rgba(255,255,255,.6)" },
};

const Cromo: React.FC<{ txt: string; x?: number; y: number; size: number; t0: number; t1: number; v?: keyof typeof CARAS }> = ({ txt, x = 540, y, size, t0, t1, v = "cobre" }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t < t0 - 0.01 || t > t1 + 0.2) return null;
  const sp = t0 <= 0 ? 1 : spring({ frame: f - Math.round(t0 * FPS), fps: FPS, config: { damping: 11, stiffness: 160, mass: 0.7 } });
  const out = p(t, t1, 0.16);
  const sc = interpolate(sp, [0, 1], [1.9, 1]) * (1 + 0.04 * p(t, t0, t1 - t0, Easing.linear)) * (1 - 0.15 * out);
  const op = Math.min(1, sp * 1.4) * (1 - out);
  const blur = (1 - Math.min(1, sp)) * 16 + out * 12;
  const c = CARAS[v];
  const canto = Array.from({ length: 12 }).map((_, k) => `0 ${k + 1}px 0 ${k < 4 ? c.canto[0] : k < 9 ? c.canto[1] : c.canto[2]}`).join(",");
  const halo = v === "navy" ? "0 0 3px #fff, 0 0 2px #fff," : "";
  const base: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: "100%", textAlign: "center", fontFamily: HEAD, fontSize: size, lineHeight: 1, letterSpacing: size * 0.01, whiteSpace: "nowrap" };
  return (
    <div style={{ position: "absolute", left: x - 540, top: y - size * 0.55, width: 1080, height: size * 1.2, transform: `scale(${sc})`, transformOrigin: "50% 55%", opacity: op, filter: blur > 0.3 ? `blur(${blur}px)` : undefined }}>
      <div style={{ ...base, color: c.canto[1], textShadow: `${halo}${canto}, 0 22px 30px rgba(0,0,0,.5)`, WebkitTextStroke: v === "navy" ? "5px #ffffff" : undefined }}>{txt}</div>
      <div style={{ ...base, backgroundImage: c.cara, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", WebkitTextStroke: `1.5px ${c.borde}` }}>{txt}</div>
    </div>
  );
};

// ---------- palabras pequeñas (cobre claro) con desenfoque ----------
const Chicas: React.FC<{ words: [string, number][]; y: number; t1: number; size?: number; x?: number }> = ({ words, y, t1, size = 52, x = 540 }) => {
  const t = useT();
  if (t < words[0][1] - 0.01 || t > t1 + 0.2) return null;
  const out = p(t, t1, 0.15);
  return (
    <div style={{ position: "absolute", left: x - 540, top: y, width: 1080, textAlign: "center", fontFamily: BODY, fontWeight: 800, fontSize: size, color: COBRE_C, letterSpacing: 2, textShadow: `0 2px 0 ${NAVY}, 0 4px 14px rgba(13,30,58,.85)`, opacity: 1 - out }}>
      {words.map(([w, t0], i) => {
        const a = p(t, t0, 0.18);
        return <span key={i} style={{ display: "inline-block", margin: "0 10px", opacity: a, filter: `blur(${(1 - a) * 12}px)`, transform: `translateY(${(1 - a) * 14}px)`, fontStyle: "italic" }}>{w}</span>;
      })}
    </div>
  );
};

// ---------- íconos 3D (blanco brillante con glifo navy/cobre) ----------
const GLIFOS: Record<string, React.ReactNode> = {
  pregunta: <text x="50" y="72" textAnchor="middle" fontFamily={HEAD} fontSize="70" fill={NAVY}>?</text>,
  foco: <g fill="none" stroke={NAVY} strokeWidth="6" strokeLinecap="round"><path d="M50 18c-15 0-26 11-26 25 0 10 6 16 10 21 3 4 4 8 4 12h24c0-4 1-8 4-12 4-5 10-11 10-21 0-14-11-25-26-25z" fill="#ffe2b8" /><path d="M39 84h22M42 92h16" /><path d="M50 50v14M44 44l6 6 6-6" stroke={COBRE} /></g>,
  codigo: <g fill="none" stroke={NAVY} strokeWidth="8" strokeLinecap="round" strokeLinejoin="round"><path d="M36 30L16 50l20 20M64 30l20 20-20 20" /><path d="M56 22L44 78" stroke={COBRE} /></g>,
  archivo: <g strokeLinejoin="round"><path d="M28 14h32l16 16v56H28z" fill="#fff" stroke={NAVY} strokeWidth="6" /><path d="M60 14v16h16" fill="none" stroke={NAVY} strokeWidth="6" /><path d="M38 50h28M38 62h28M38 74h18" stroke={COBRE} strokeWidth="6" strokeLinecap="round" /></g>,
  flecha: <g fill="none" stroke={COBRE} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round"><path d="M50 18v58M28 56l22 22 22-22" /></g>,
  check: <g fill="none" stroke={COBRE} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round"><path d="M24 52l17 17 36-38" /></g>,
  grafica: <g strokeLinecap="round"><path d="M22 78h58" stroke={NAVY} strokeWidth="6" /><rect x="28" y="52" width="10" height="22" fill={NAVY} /><rect x="45" y="40" width="10" height="34" fill={NAVY} /><rect x="62" y="24" width="10" height="50" fill={COBRE} /></g>,
  dinero: <g><circle cx="50" cy="50" r="30" fill="#ffe2b8" stroke={COBRE} strokeWidth="6" /><text x="50" y="64" textAnchor="middle" fontFamily={HEAD} fontSize="40" fill={NAVY}>$</text></g>,
};

const Icono: React.FC<{ g: string; x: number; y: number; size?: number; t0: number; t1: number; num?: string; rebote?: boolean }> = ({ g, x, y, size = 170, t0, t1, num, rebote }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t < t0 - 0.01 || t > t1 + 0.2) return null;
  const sp = spring({ frame: f - Math.round(t0 * FPS), fps: FPS, config: { damping: 8, stiffness: 180, mass: 0.6 } });
  const out = p(t, t1, 0.15);
  const flota = rebote ? Math.abs(Math.sin((t - t0) * 6)) * -22 : Math.sin((t - t0) * 3.2) * 8;
  return (
    <div style={{ position: "absolute", left: x - size / 2, top: y - size / 2 + flota, width: size, height: size, borderRadius: size * 0.26, transform: `scale(${sp * (1 - out)}) rotate(${(1 - sp) * -18}deg)`, background: "linear-gradient(160deg,#ffffff 0%,#eef2f5 45%,#cfd7de 100%)", boxShadow: `0 24px 40px rgba(13,30,58,.45), inset 0 -8px 14px rgba(13,30,58,.14), inset 0 6px 10px rgba(255,255,255,.95), 0 0 0 4px ${COBRE}`, opacity: 1 - out }}>
      <svg viewBox="0 0 100 100" width={size} height={size} style={{ position: "absolute", inset: 0 }}>{GLIFOS[g]}</svg>
      <div style={{ position: "absolute", left: "8%", top: "6%", width: "84%", height: "38%", borderRadius: size * 0.2, background: "linear-gradient(180deg,rgba(255,255,255,.75),rgba(255,255,255,0))" }} />
      {num && <div style={{ position: "absolute", right: -12, top: -12, width: size * 0.36, height: size * 0.36, borderRadius: "50%", background: COBRE, color: "#fff", fontFamily: HEAD, fontSize: size * 0.24, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 6px 12px rgba(0,0,0,.3)" }}>{num}</div>}
    </div>
  );
};

// ---------- contador circular ----------
const Anillo: React.FC<{ x: number; y: number; t0: number; t1: number; dur?: number }> = ({ x, y, t0, t1, dur = 1.0 }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t < t0 || t > t1 + 0.2) return null;
  const sp = spring({ frame: f - Math.round(t0 * FPS), fps: FPS, config: { damping: 10, stiffness: 170 } });
  const k = p(t, t0 + 0.1, dur, Easing.inOut(Easing.cubic));
  const out = p(t, t1, 0.15);
  const R = 92, C = 2 * Math.PI * R;
  return (
    <div style={{ position: "absolute", left: x - 120, top: y - 120, width: 240, height: 240, transform: `scale(${sp * (1 - out)})` }}>
      <svg width={240} height={240}>
        <defs><linearGradient id="an" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#ffe0b0" /><stop offset="1" stopColor={COBRE} /></linearGradient></defs>
        <circle cx={120} cy={120} r={112} fill="rgba(13,30,58,.88)" stroke={COBRE} strokeWidth={3} />
        <circle cx={120} cy={120} r={R} fill="none" stroke="rgba(255,255,255,.15)" strokeWidth={16} />
        <circle cx={120} cy={120} r={R} fill="none" stroke="url(#an)" strokeWidth={16} strokeLinecap="round" strokeDasharray={`${C * k} ${C}`} transform="rotate(-90 120 120)" />
      </svg>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: "#fff" }}>
        <div style={{ fontFamily: HEAD, fontSize: 64, lineHeight: 1 }}>{Math.round(k * 100)}%</div>
        <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: 22, letterSpacing: 2, marginTop: 6, color: k >= 1 ? COBRE_C : "#cfd8e3" }}>{k >= 1 ? "✓ LISTO" : "CARGANDO"}</div>
      </div>
    </div>
  );
};

const Pintar: React.FC<{ e: Elemento }> = ({ e }) => {
  if (e.tipo === "cromo") return <Cromo {...e} />;
  if (e.tipo === "chicas") return <Chicas {...e} />;
  if (e.tipo === "icono") return <Icono {...e} />;
  return <Anillo {...e} />;
};

// ---------- transiciones ----------
const Halftone: React.FC<{ t0: number }> = ({ t0 }) => {
  const t = useT();
  if (t < t0 || t > t0 + 0.4) return null;
  const k = p(t, t0, 0.3, Easing.in(Easing.quad));
  const S = 40;
  const dots: React.ReactNode[] = [];
  for (let gy = 0; gy <= 1920 / S; gy++) {
    for (let gx = 0; gx <= 1080 / S; gx++) {
      const cx = gx * S + (gy % 2) * S / 2, cy = gy * S;
      const d = Math.hypot((cx - 540) / 540, (cy - 900) / 960) / 1.42;
      const r = Math.max(0, Math.min(1, (k * 1.7 - (1 - d)) / 0.7)) * S * 0.78;
      if (r > 0.5) dots.push(<circle key={`${gx}-${gy}`} cx={cx} cy={cy} r={r} fill={(gx + gy) % 5 === 0 ? COBRE : NAVY} />);
    }
  }
  return <svg width={1080} height={1920} style={{ position: "absolute" }}>{dots}</svg>;
};

const Estudio: React.FC = () => {
  const t = useT();
  const E = GUION.estudio;
  if (!E) return null;
  const a = p(t, E.in + 0.24, 0.1) * (1 - p(t, E.out, 0.18));
  if (a <= 0) return null;
  return (
    <AbsoluteFill style={{ opacity: a, background: `radial-gradient(ellipse at 50% 40%, ${NAVY_2} 0%, ${NAVY} 60%, #060f1f 100%)` }}>
      <svg width={1080} height={1920} style={{ position: "absolute", opacity: 0.12 }}>
        {Array.from({ length: 24 }).map((_, i) => <line key={`v${i}`} x1={i * 48} y1={0} x2={i * 48} y2={1920} stroke="#9FB0C8" />)}
        {Array.from({ length: 41 }).map((_, i) => <line key={`h${i}`} x1={0} y1={i * 48} x2={1080} y2={i * 48} stroke="#9FB0C8" />)}
      </svg>
      {E.elementos.map((e, i) => <Pintar key={i} e={e} />)}
    </AbsoluteFill>
  );
};

const Destello: React.FC<{ c: number; w?: number }> = ({ c, w = 0.22 }) => {
  const t = useT();
  const a = bell(t, c, w);
  if (a <= 0) return null;
  return <AbsoluteFill style={{ mixBlendMode: "screen", opacity: a, background: `radial-gradient(circle at ${30 + 40 * (t - c + w) / (2 * w)}% 40%, rgba(255,190,120,.95) 0%, rgba(215,134,49,.75) 30%, rgba(255,226,190,.35) 55%, rgba(0,0,0,0) 80%)` }} />;
};

const Flash: React.FC<{ c: number; w?: number; max?: number }> = ({ c, w = 0.08, max = 0.55 }) => {
  const a = bell(useT(), c, w) * max;
  return a > 0 ? <AbsoluteFill style={{ background: "#fff", opacity: a }} /> : null;
};

// ---------- composición ----------
export const Motion: React.FC = () => {
  const t = useT();
  const G = GUION;
  const enPortada = t < G.portadaHasta + 0.2;
  return (
    <AbsoluteFill style={{ background: NAVY }}>
      <Capa />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(13,30,58,.55) 0%, rgba(13,30,58,0) 38%, rgba(13,30,58,0) 60%, rgba(13,30,58,.5) 100%)" }} />

      {/* detrás de Gabriel */}
      {enPortada && <Cromo txt={G.portada.arriba} y={420} size={230} t0={0} t1={G.portadaHasta} v="navy" />}
      {G.elementos.filter((e) => e.tipo === "cromo" && e.capa === "detras").map((e, i) => <Pintar key={`d${i}`} e={e} />)}

      <Capa alfa />

      {/* delante */}
      {enPortada && (
        <>
          <Cromo txt={G.portada.abajo} y={1260} size={160} t0={0} t1={G.portadaHasta} v="cobre" />
          <div style={{ position: "absolute", top: 1440, width: 1080, display: "flex", justifyContent: "center", opacity: 1 - p(t, G.portadaHasta - 0.04, 0.1) }}>
            <div style={{ background: NAVY, color: "#fff", fontFamily: HEAD, fontSize: 60, padding: "10px 34px", borderRadius: 18, border: `4px solid ${COBRE}`, boxShadow: "0 12px 24px rgba(0,0,0,.35)" }}>{G.portada.chip}</div>
          </div>
        </>
      )}
      {G.elementos.filter((e) => !(e.tipo === "cromo" && e.capa === "detras")).map((e, i) => <Pintar key={`f${i}`} e={e} />)}

      {/* transiciones */}
      {G.whips.map((w) => <Flash key={`w${w}`} c={w} w={0.07} max={0.5} />)}
      {G.estudio && <Halftone t0={G.estudio.in} />}
      <Estudio />
      {G.destellos.map((d) => <Destello key={`l${d}`} c={d} w={0.22} />)}
      {G.golpes.map((g) => <Flash key={`g${g.t}`} c={g.t - 0.03} w={0.06} max={0.3} />)}
    </AbsoluteFill>
  );
};
