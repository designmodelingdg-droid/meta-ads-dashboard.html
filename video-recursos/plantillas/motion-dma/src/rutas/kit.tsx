import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { brand } from "../brand/brand";
import { ease, progress } from "../lib/motion";

// Kit de las rutas DMA (estilo fusión): fondo navy con cuadrícula, línea de luz cobre,
// barridos de cámara, nodo 3D cobre y tarjeta navy con chips sincronizados a la voz.

export const FPS = 30;
export const F = (s: number) => Math.round(s * FPS);
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const K = {
  bg: "#0D1E3A",
  copper: "#D78631",
  copperHi: "#F5B266",
  white: "#FFFFFF",
  muted: "#9FB0CC",
  card: "#122546",
  card2: "#1A3159",
  red: "#FF4D4D",
  green: "#3FD89B",
};
export const LOGO = (f: string) => staticFile(`rutas/logos/${f}`);
export const sp = (frame: number, at: number, damping = 14) => spring({ frame: frame - at, fps: FPS, config: { damping, stiffness: 160 } });

export type Word = { w: string; s: number; e: number };
export type VoiceData = { scenes: { start: number; dur: number }[]; words: Word[]; total: number };

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]/g, "");

/** Utilidades de tiempo a partir de la voz verificada con Whisper. */
export const makeTiming = (data: VoiceData, extra = 15) => {
  const duration = Math.ceil(data.total * FPS) + extra;
  const S = (i: number) => (i >= data.scenes.length ? duration : F(data.scenes[i].start));
  const end = (i: number) => S(i + 1);
  /** Frame de la palabra que empieza con `stem` dentro de la escena i; si no aparece, reparte por la escena. */
  const at = (stem: string, scene: number, slot = 0, slots = 3): number => {
    const sc = data.scenes[scene];
    const w = data.words.find((x) => x.s >= sc.start - 0.05 && x.s < sc.start + sc.dur && norm(x.w).startsWith(stem));
    if (w) return F(w.s);
    return F(sc.start + (sc.dur * (slot + 1)) / (slots + 1.2));
  };
  const talking = (f: number) => data.words.some((w) => f / FPS >= w.s - 0.25 && f / FPS <= w.e + 0.35);
  return { duration, S, end, at, talking };
};
export type Timing = ReturnType<typeof makeTiming>;

export const useStage = () => {
  const { width: W, height: H } = useVideoConfig();
  const V = H > W;
  return { W, H, V, cx: W / 2, cy: H * (V ? 0.48 : 0.44) };
};

/** Barrido de cámara: entra desde la derecha y sale hacia la izquierda con desenfoque. */
export const Whip: React.FC<{ from: number; to: number; children: React.ReactNode; first?: boolean }> = ({ from, to, children, first }) => {
  const frame = useCurrentFrame();
  const { W } = useStage();
  if (frame < from - 8 || frame > to + 1) return null;
  const pin = first ? 1 : progress(frame, from - 7, 11);
  const pout = progress(frame, to - 6, 7, ease.in);
  const x = (1 - pin) * W * 0.75 - pout * W * 0.75;
  const blur = (1 - pin) * 26 + pout * 26;
  return <AbsoluteFill style={{ transform: `translateX(${x}px)`, filter: blur > 0.5 ? `blur(${blur}px)` : undefined }}>{children}</AbsoluteFill>;
};

/** Línea de luz que entra por la izquierda, llega al centro y sale por la derecha. */
export const LightLine: React.FC<{ from: number; to: number; exit?: boolean }> = ({ from, to, exit = true }) => {
  const frame = useCurrentFrame();
  const { W, H, cx, cy } = useStage();
  const dy = H * 0.2;
  const dIn = `M ${-0.08 * W} ${cy + dy} C ${0.22 * W} ${cy + dy}, ${0.3 * W} ${cy}, ${cx} ${cy}`;
  const dOut = `M ${cx} ${cy} C ${0.7 * W} ${cy}, ${0.78 * W} ${cy - dy}, ${1.08 * W} ${cy - dy}`;
  const pIn = progress(frame, from - 2, 14, ease.inOut);
  const pOut = exit ? progress(frame, to - 14, 12, ease.inOut) : 0;
  const stroke = (d: string, p: number, key: string) => (
    <g key={key}>
      <path d={d} pathLength={1} fill="none" stroke={K.copper} strokeWidth={34} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - p} opacity={0.3} style={{ filter: "blur(14px)" }} />
      <path d={d} pathLength={1} fill="none" stroke={K.copperHi} strokeWidth={10} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - p} />
      <path d={d} pathLength={1} fill="none" stroke="#FFF3E0" strokeWidth={3} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - p} />
    </g>
  );
  return (
    <svg width={W} height={H} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
      {stroke(dIn, pIn, "in")}
      {pOut > 0 && stroke(dOut, pOut, "out")}
    </svg>
  );
};

export const Burst: React.FC<{ at: number; color?: string; r?: number }> = ({ at, color = K.copper, r = 340 }) => {
  const frame = useCurrentFrame();
  const { cx, cy } = useStage();
  const p = interpolate(frame, [at, at + 22], [0, 1], { ...clamp, easing: ease.out });
  if (p <= 0 || p >= 1) return null;
  return (
    <>
      {Array.from({ length: 18 }, (_, i) => {
        const a = (i / 18) * Math.PI * 2 + (i % 2) * 0.17;
        const d = r * (0.55 + (i % 4) * 0.15) * p;
        const s = 10 + (i % 3) * 6;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: cx + Math.cos(a) * d - s / 2,
              top: cy + Math.sin(a) * d - s / 2,
              width: s,
              height: s,
              borderRadius: i % 3 ? 3 : "50%",
              background: i % 2 ? color : "#FFFFFF",
              opacity: 1 - p,
              transform: `rotate(${i * 30 + p * 120}deg)`,
              boxShadow: `0 0 12px ${color}`,
            }}
          />
        );
      })}
      <div style={{ position: "absolute", left: cx - r * p, top: cy - r * p, width: r * 2 * p, height: r * 2 * p, borderRadius: "50%", border: `4px solid ${color}`, opacity: (1 - p) * 0.8 }} />
    </>
  );
};

export const Glass: React.FC<{ w: number; h: number; color?: string; children?: React.ReactNode; style?: React.CSSProperties }> = ({ w, h, color = K.copper, children, style }) => (
  <div
    style={{
      position: "absolute",
      width: w,
      height: h,
      borderRadius: 26,
      background: `linear-gradient(160deg, ${K.card2} 0%, ${K.card} 70%)`,
      border: `4px solid ${color}`,
      boxShadow: `0 0 40px ${color}55, inset 0 0 40px ${color}22, 0 30px 60px rgba(0,0,0,.6)`,
      overflow: "hidden",
      ...style,
    }}
  >
    <div style={{ position: "absolute", left: -w * 0.3, top: -h * 0.6, width: w * 0.9, height: h * 1.2, background: "linear-gradient(120deg, rgba(255,255,255,.10), transparent 60%)", transform: "rotate(-12deg)" }} />
    {children}
  </div>
);

/** Ícono de app real sobre una baldosa blanca. */
export const AppTile: React.FC<{ src: string; w: number; h: number; pad?: number }> = ({ src, w, h, pad = 22 }) => (
  <div style={{ width: w, height: h, borderRadius: 26, background: "#FFFFFF", boxShadow: `0 0 34px ${K.copper}66, 0 20px 40px rgba(0,0,0,.45)`, display: "flex", alignItems: "center", justifyContent: "center", padding: pad, boxSizing: "border-box" }}>
    <Img src={src} style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }} />
  </div>
);

/** Texto en una baldosa (para herramientas sin logo en el Drive). */
export const TextTile: React.FC<{ txt: string; w: number; h: number; size?: number }> = ({ txt, w, h, size = 44 }) => (
  <div
    style={{
      width: w,
      height: h,
      borderRadius: 24,
      background: `linear-gradient(160deg, ${K.card2}, ${K.card})`,
      border: `4px solid ${K.copper}`,
      boxShadow: `0 0 30px ${K.copper}55`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      textAlign: "center",
      fontFamily: brand.fontDisplay,
      fontSize: size,
      color: K.white,
      lineHeight: 1,
      padding: 12,
      boxSizing: "border-box",
    }}
  >
    {txt}
  </div>
);

/** Aparición con resorte en una posición relativa al centro del protagonista. */
export const Pop: React.FC<{ at: number; x: number; y: number; w: number; h: number; children: React.ReactNode; rot?: number }> = ({ at, x, y, w, h, children, rot = 0 }) => {
  const frame = useCurrentFrame();
  const p = sp(frame, at, 13);
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `translateY(${(1 - p) * 60}px) scale(${0.6 + 0.4 * p}) rotate(${rot * (1 - p)}deg)`, opacity: Math.min(1, p * 1.6) }}>
      {children}
    </div>
  );
};

/** Escala el protagonista: en horizontal hay menos alto disponible. */
export const Hero: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { V, cx, cy } = useStage();
  const k = V ? 0.92 : 0.78;
  return (
    <AbsoluteFill style={{ transform: `scale(${k})`, transformOrigin: `${cx}px ${cy}px` }}>
      <div style={{ position: "absolute", left: cx, top: cy }}>{children}</div>
    </AbsoluteFill>
  );
};

export type Chip = { label: string; at: number };

/** Nodo 3D cobre (arriba) y tarjeta navy con chips sincronizados (abajo). */
export const StepCard: React.FC<{ n: string; kicker: string; title: string; chips: Chip[]; from: number; to: number }> = ({ n, kicker, title, chips, from, to }) => {
  const frame = useCurrentFrame();
  const { W, H, V } = useStage();
  const hit = from + 12;
  const pc = sp(frame, from + 2, 13);
  const lit = progress(frame, hit - 2, 6);
  const ring = interpolate(frame, [hit, hit + 22], [0, 1], clamp);
  const pop = interpolate(frame, [hit, hit + 12], [0, 1], clamp);
  const R = 78;
  const ccx = W / 2;
  const ccy = H * (V ? 0.235 : 0.13);
  const cardTop = H * (V ? 0.635 : 0.7);
  const pin = progress(frame, from + 14, 12);
  const pout = progress(frame, to - 8, 8, ease.in);
  return (
    <>
      <div style={{ position: "absolute", left: ccx - R, top: ccy - R, width: R * 2, height: R * 2 + 14, transform: `scale(${pc * (1 + 0.12 * Math.sin(Math.PI * pop))})` }}>
        {ring > 0 && ring < 1 && (
          <div style={{ position: "absolute", left: R - R * (1 + ring), top: R - R * (1 + ring), width: R * 2 * (1 + ring), height: R * 2 * (1 + ring), borderRadius: "50%", border: `7px solid ${K.copperHi}`, opacity: 1 - ring }} />
        )}
        <div style={{ position: "absolute", left: 0, top: 14, width: R * 2, height: R * 2, borderRadius: "50%", background: lit > 0.5 ? "#8E5219" : "#16243F" }} />
        <div style={{ position: "absolute", left: 0, top: 0, width: R * 2, height: R * 2, borderRadius: "50%", background: "radial-gradient(circle at 38% 30%, #3A5080 0%, #2B3E63 60%)" }} />
        <div style={{ position: "absolute", left: 0, top: 0, width: R * 2, height: R * 2, borderRadius: "50%", opacity: lit, background: `radial-gradient(circle at 38% 30%, #FFD09A 0%, ${K.copperHi} 30%, ${K.copper} 75%)`, boxShadow: `0 0 ${60 * lit}px ${K.copper}AA` }} />
        <div style={{ position: "absolute", left: 0, top: 0, width: R * 2, height: R * 2, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: brand.fontDisplay, fontSize: n.length > 1 ? 64 : 96, color: lit > 0.5 ? "#FFFFFF" : "#6F82A6", paddingTop: 4 }}>{n}</div>
      </div>
      <div
        style={{
          position: "absolute",
          left: V ? 70 : W / 2 - 560,
          width: V ? W - 140 : 1120,
          top: cardTop,
          padding: V ? "30px 40px 36px" : "24px 40px 28px",
          borderRadius: 16,
          background: "rgba(20,40,75,.96)",
          borderTop: `8px solid ${K.copper}`,
          boxShadow: "0 30px 80px rgba(0,0,0,.45)",
          opacity: pin * (1 - pout),
          transform: `translateY(${(1 - pin) * 40}px)`,
          textAlign: V ? "left" : "center",
        }}
      >
        <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 30, letterSpacing: 5, color: K.copperHi }}>{kicker}</div>
        <div style={{ fontFamily: brand.fontDisplay, fontSize: title.length > 20 ? (V ? 72 : 70) : V ? 92 : 84, color: K.white, lineHeight: 1.05 }}>{title}</div>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 18, flexWrap: "wrap", justifyContent: V ? "flex-start" : "center" }}>
          {chips.map((c, i) => {
            const p = spring({ frame: frame - (c.at - 3), fps: FPS, config: { damping: 14, stiffness: 180 } });
            return (
              <React.Fragment key={c.label}>
                {i > 0 && <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 34, color: K.copper, opacity: p }}>·</div>}
                <div
                  style={{
                    padding: "12px 22px 8px",
                    borderRadius: 999,
                    background: p > 0.5 ? K.copper : "transparent",
                    border: `3px solid ${K.copper}`,
                    fontFamily: brand.fontBody,
                    fontWeight: 800,
                    fontSize: 28,
                    color: K.white,
                    opacity: Math.min(1, p * 1.5),
                    transform: `scale(${0.9 + 0.1 * p})`,
                    boxShadow: p > 0.5 ? `0 0 22px ${K.copper}88` : "none",
                  }}
                >
                  {c.label}
                </div>
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </>
  );
};

/** Rótulo grande que entra con desenfoque (para escenas sin tarjeta). */
export const Caption: React.FC<{ txt: string; from: number; to: number; y?: number }> = ({ txt, from, to, y }) => {
  const frame = useCurrentFrame();
  const { H, V } = useStage();
  const p = progress(frame, from, 8) * (1 - progress(frame, to - 6, 6, ease.in));
  if (p <= 0) return null;
  return (
    <div style={{ position: "absolute", left: 30, right: 30, top: y ?? H * (V ? 0.71 : 0.8), textAlign: "center", fontFamily: brand.fontDisplay, fontSize: V ? 80 : 86, color: K.white, opacity: p, filter: `blur(${(1 - p) * 10}px)`, textShadow: `0 0 30px ${K.copper}` }}>
      {txt}
    </div>
  );
};

/** Carrusel 3D de tarjetas que pasa y converge al centro. */
export const Carousel: React.FC<{ items: { kicker: string; title: string }[]; from: number; converge: number; cardW?: number }> = ({ items, from, converge, cardW = 420 }) => {
  const frame = useCurrentFrame();
  const { W, V, cx, cy } = useStage();
  const conv = interpolate(frame, [converge - 4, converge + 10], [0, 1], { ...clamp, easing: ease.inOut });
  const scroll = interpolate(frame, [from, converge], [0, 1], clamp);
  const step = cardW + (V ? 60 : 80);
  const n = items.length;
  const travel = (n - 1) * step;
  return (
    <>
      {items.map((it, i) => {
        const x0 = i * step - scroll * travel + (1 - scroll) * W * 0.5 - (V ? 0 : 0);
        const x = x0 * (1 - conv);
        const p = sp(frame, from + Math.min(i, 6) * 2, 15);
        const h = cardW * 0.66;
        return (
          <div
            key={it.title}
            style={{
              position: "absolute",
              left: cx + x - cardW / 2,
              top: cy - h / 2,
              transform: `perspective(1400px) rotateY(${-26 * (1 - conv)}deg) scale(${(0.9 + 0.1 * p) * (1 - conv * 0.25)})`,
              opacity: Math.min(1, p * 1.5) * (1 - progress(frame, converge + 8, 8)),
              filter: conv > 0 && conv < 1 ? `blur(${Math.sin(conv * Math.PI) * 10}px)` : undefined,
            }}
          >
            <Glass w={cardW} h={h}>
              <div style={{ position: "absolute", left: 30, top: 28, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 26, letterSpacing: 5, color: K.copperHi }}>{it.kicker}</div>
              <div style={{ position: "absolute", left: 30, right: 26, bottom: 30, fontFamily: brand.fontDisplay, fontSize: it.title.length > 26 ? 36 : it.title.length > 16 ? 42 : 54, color: K.white, lineHeight: 1.02 }}>{it.title}</div>
            </Glass>
          </div>
        );
      })}
    </>
  );
};

/** Gran titular final + tarjeta de cierre con logo y CTA. */
export const Finale: React.FC<{ at: number; cta: number; kicker: string; big: string; sub: string; meta: string }> = ({ at, cta, kicker, big, sub, meta }) => {
  const frame = useCurrentFrame();
  const { V, cy } = useStage();
  const pM = sp(frame, at, 13);
  const pE = progress(frame, cta, 12);
  return (
    <>
      <Burst at={at - 4} color={K.copperHi} r={420} />
      {pM > 0.01 && (
        <div style={{ position: "absolute", left: 20, right: 20, top: cy - (V ? 250 : 200), textAlign: "center", opacity: Math.min(1, pM * 1.5) * (1 - pE), transform: `scale(${0.85 + 0.15 * pM})` }}>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, letterSpacing: 9, color: K.copperHi }}>{kicker}</div>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: big.length > 10 ? (V ? 128 : 150) : V ? 190 : 210, color: K.white, lineHeight: 1, textShadow: `0 0 50px ${K.copper}` }}>{big}</div>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 62 : 64, color: K.white, marginTop: 6 }}>{sub}</div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 30, letterSpacing: 4, color: K.muted, marginTop: 20 }}>{meta}</div>
        </div>
      )}
      {pE > 0 && (
        <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 56, paddingBottom: V ? 140 : 0 }}>
          <Img src={staticFile("logo-dma.png")} style={{ width: V ? 580 : 560, opacity: pE, transform: `translateY(${(1 - pE) * 24}px)`, filter: `drop-shadow(0 0 24px ${K.copper}66)` }} />
          <div
            style={{
              padding: "26px 56px 18px",
              borderRadius: 14,
              background: K.copper,
              boxShadow: `0 0 40px ${K.copper}`,
              fontFamily: brand.fontDisplay,
              fontSize: V ? 86 : 80,
              color: K.white,
              opacity: Math.min(1, sp(frame, cta + 8) * 1.5),
              transform: `scale(${0.9 + 0.1 * sp(frame, cta + 8)})`,
            }}
          >
            PIDE INFORMACIÓN
          </div>
        </AbsoluteFill>
      )}
    </>
  );
};

/** Fondo, logo, música con ducking y efectos. Envuelve las escenas. */
export const Frame: React.FC<{ t: Timing; voice: string; cta: number; whooshes: number[]; bongs: number[]; extra?: { at: number; src: string; vol: number }[]; children: React.ReactNode }> = ({
  t,
  voice,
  cta,
  whooshes,
  bongs,
  extra = [],
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { W, H, V } = useStage();
  const dust = Array.from({ length: 40 }, (_, i) => {
    const x = ((i * 397) % W) - ((frame * (0.6 + (i % 5) * 0.5)) % W);
    const xx = x < 0 ? x + W : x;
    const y = (i * 211) % H;
    return <div key={i} style={{ position: "absolute", left: xx, top: y, width: 3 + (i % 3), height: 3 + (i % 3), borderRadius: "50%", background: K.copperHi, opacity: 0.12 + (i % 4) * 0.05 }} />;
  });
  return (
    <AbsoluteFill style={{ backgroundColor: K.bg, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          backgroundImage: "linear-gradient(rgba(255,255,255,.045) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.045) 2px, transparent 2px)",
          backgroundSize: "60px 60px",
          backgroundPosition: `${(frame * 0.4) % 60}px ${(frame * 0.4) % 60}px`,
        }}
      />
      <AbsoluteFill style={{ background: `radial-gradient(60% 50% at 50% 46%, ${K.copper}26 0%, transparent 70%)` }} />
      {dust}
      {children}
      <AbsoluteFill style={{ background: `radial-gradient(120% 90% at 50% 50%, transparent 55%, ${K.bg} 100%)`, pointerEvents: "none" }} />
      <Img src={staticFile("logo-dma.png")} style={{ position: "absolute", width: V ? 300 : 230, left: V ? 390 : W - 280, top: V ? 270 : 44, opacity: frame >= cta ? 0 : 0.95 }} />
      <Audio src={staticFile(voice)} />
      <Audio
        src={staticFile("rutas/musica_master.wav")}
        volume={(f) => {
          const end = interpolate(f, [durationInFrames - 20, durationInFrames], [1, 0], clamp);
          return (t.talking(f) ? 0.07 : 0.3) * end;
        }}
      />
      {whooshes.map((w, i) => (
        <Sequence key={`wh${i}`} from={Math.max(0, w - 8)} durationInFrames={20}>
          <Audio src={staticFile("rutas/whoosh.wav")} volume={0.5} />
        </Sequence>
      ))}
      {bongs.map((b, i) => (
        <Sequence key={`b${i}`} from={Math.max(0, b)} durationInFrames={40}>
          <Audio src={staticFile("sfx/interface/bong_001.ogg")} volume={0.4} />
        </Sequence>
      ))}
      {extra.map((e, i) => (
        <Sequence key={`x${i}`} from={Math.max(0, e.at)} durationInFrames={60}>
          <Audio src={staticFile(e.src)} volume={e.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

/** Gancho: titular + fila de nodos que se encienden. */
export const HookRow: React.FC<{ kicker: string; title: React.ReactNode; labels: string[]; at: number; goal?: string; size?: number }> = ({ kicker, title, labels, at, goal, size }) => {
  const frame = useCurrentFrame();
  const { W, H, V, cx } = useStage();
  const n = labels.length + (goal ? 1 : 0);
  const step = Math.min(V ? 200 : 280, (W - 160) / n);
  const R = Math.min(70, step * 0.36);
  const xs = (i: number) => (i - (n - 1) / 2) * step;
  const rowY = H * (V ? 0.6 : 0.66);
  const lines = Array.from({ length: 26 }, (_, i) => {
    const a = (i / 26) * Math.PI * 2 + (i % 3) * 0.05;
    const p = (frame * 0.035 + ((i * 0.37) % 1)) % 1;
    const r0 = 260 + p * Math.max(W, H) * 0.7;
    const len = 80 + (i % 4) * 60;
    return (
      <div
        key={i}
        style={{ position: "absolute", left: cx + Math.cos(a) * r0, top: H * 0.47 + Math.sin(a) * r0, width: len, height: 4, borderRadius: 2, background: `linear-gradient(90deg, transparent, ${K.copperHi})`, transform: `rotate(${a}rad)`, transformOrigin: "0 50%", opacity: 0.45 * Math.sin(p * Math.PI) }}
      />
    );
  });
  const lineP = interpolate(frame, [at, at + 6 * n], [0, 1], clamp);
  return (
    <>
      {lines}
      <div style={{ position: "absolute", left: 30, right: 30, top: H * (V ? 0.36 : 0.28), textAlign: "center" }}>
        <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, letterSpacing: 10, color: K.copperHi }}>{kicker}</div>
        <div style={{ fontFamily: brand.fontDisplay, fontSize: size ?? (V ? 140 : 150), color: K.white, lineHeight: 1, textShadow: `0 0 50px ${K.copper}88` }}>{title}</div>
      </div>
      <div style={{ position: "absolute", left: cx, top: rowY }}>
        <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
          <path d={`M ${xs(0)} 0 L ${xs(n - 1)} 0`} stroke={K.copperHi} strokeWidth={8} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - lineP} style={{ filter: `drop-shadow(0 0 10px ${K.copper})` }} />
        </svg>
        {labels.map((l, i) => {
          const t = at + i * 5;
          const p = sp(frame, t, 12);
          const on = frame >= t;
          return (
            <div key={i} style={{ position: "absolute", left: xs(i) - R, top: -R, width: R * 2, height: R * 2, transform: `scale(${1 + 0.12 * Math.sin(Math.PI * Math.min(1, p))})`, opacity: on ? 1 : 0.7 }}>
              <div style={{ position: "absolute", inset: 0, top: 10, borderRadius: "50%", background: on ? "#8E5219" : "#16243F" }} />
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  borderRadius: "50%",
                  background: on ? `radial-gradient(circle at 35% 30%, #FFE0B8, ${K.copperHi} 35%, ${K.copper} 75%)` : "radial-gradient(circle at 35% 30%, #3A5080, #2B3E63)",
                  boxShadow: on ? `0 0 40px ${K.copper}` : "none",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: brand.fontDisplay,
                  fontSize: R * 1.1,
                  color: on ? K.white : "#6F82A6",
                }}
              >
                {l}
              </div>
            </div>
          );
        })}
        {goal &&
          (() => {
            const t = at + labels.length * 5 + 4;
            const on = frame >= t;
            const g = sp(frame, t, 12);
            const x = xs(n - 1);
            const D = R * 2.3;
            return (
              <div style={{ position: "absolute", left: x - D / 2, top: -D / 2, width: D, height: D }}>
                <div style={{ position: "absolute", inset: D * 0.12, borderRadius: D * 0.18, transform: `rotate(45deg) scale(${1 + 0.1 * Math.sin(Math.PI * Math.min(1, g))})`, background: on ? `linear-gradient(135deg, ${K.copperHi}, ${K.copper})` : "#1C2B48", border: on ? "none" : "5px dashed #6F82A6", boxShadow: on ? `0 0 50px ${K.copper}` : "none" }} />
                <div style={{ position: "absolute", top: D + 6, left: -60, right: -60, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: 40, color: on ? K.copperHi : "#6F82A6" }}>{goal}</div>
              </div>
            );
          })()}
      </div>
    </>
  );
};
