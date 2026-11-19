import React from "react";
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { ease, progress } from "../lib/motion";
import { LOGO, clamp } from "./kit";
import { loadFont as loadOverpass } from "@remotion/google-fonts/Overpass";
import { loadFont as loadNunito } from "@remotion/google-fonts/Nunito";

// Tipografía de la Academia (web designmodelingacademy): títulos Overpass, texto Nunito.
const OVERPASS = loadOverpass("normal", { weights: ["800", "900"], subsets: ["latin"] }).fontFamily;
const NUNITO = loadNunito("normal", { weights: ["700", "800"], subsets: ["latin"] }).fontFamily;

// Anuncio estilo «cromado»: cortes de cámara con zoom in/out y falsos cambios de ángulo,
// barridos con desenfoque, destello, palabra cromada que se escribe letra por letra
// e íconos cromados 3D. Material: tomas del workshop (Gabriel).
const FPS = 30;
const F = (s: number) => Math.round(s * FPS);

type Word = { at: number; kicker: string; big: string; copper?: boolean };
type Shot = {
  src: string;
  from: number; // segundo dentro del clip
  dur: number;
  cam: { s0: number; s1: number; ox: string; oy: string; x0: number; x1: number; rot: number; ry: number };
  words: Word[];
  icons?: { at: number; kind: "revit" | "doc" | "cal" | "cam" | "chat"; x: number; y: number }[];
  flash?: boolean;
};

const SHOTS: Shot[] = [
  {
    src: "s0.mp4",
    from: 0,
    dur: 3.85,
    cam: { s0: 1.0, s1: 1.1, ox: "50%", oy: "30%", x0: 0, x1: 0, rot: 0, ry: 0 },
    words: [{ at: 0, kicker: "WORKSHOP IA + REVIT", big: "NO ES PARA TODOS" }],
  },
  {
    src: "s1.mp4",
    from: 0,
    dur: 3.16,
    cam: { s0: 1.3, s1: 1.36, ox: "42%", oy: "18%", x0: -30, x1: -50, rot: -1.6, ry: -7 },
    words: [
      { at: 0.55, kicker: "ES PARA TI SI USAS", big: "REVIT", copper: true },
      { at: 2.45, kicker: "TE TOCA REVISAR", big: "MODELOS" },
    ],
    icons: [{ at: 0.6, kind: "revit", x: 950, y: 1150 }],
  },
  {
    src: "s1.mp4",
    from: 3.16,
    dur: 3.34,
    cam: { s0: 1.16, s1: 1.0, ox: "60%", oy: "30%", x0: 40, x1: 0, rot: 1.2, ry: 8 },
    words: [
      { at: 0, kicker: "LLENAR", big: "PARÁMETROS" },
      { at: 1.5, kicker: "REVISAR", big: "CANTIDADES" },
      { at: 2.65, kicker: "EXPORTAR", big: "PLANOS", copper: true },
    ],
    icons: [{ at: 1.5, kind: "doc", x: 130, y: 1150 }],
  },
  {
    src: "s3.mp4",
    from: 0,
    dur: 4.92,
    cam: { s0: 1.04, s1: 1.14, ox: "48%", oy: "28%", x0: 0, x1: -20, rot: 0, ry: -5 },
    words: [
      { at: 0.85, kicker: "GRATIS · EN VIVO", big: "MARTES 17", copper: true },
      { at: 2.8, kicker: "DE NOVIEMBRE", big: "8 PM" },
      { at: 4.1, kicker: "100% ONLINE", big: "VÍA ZOOM" },
    ],
    icons: [
      { at: 0.9, kind: "cal", x: 950, y: 1150 },
      { at: 4.15, kind: "cam", x: 130, y: 1150 },
    ],
    flash: true,
  },
  {
    src: "s3.mp4",
    from: 4.92,
    dur: 3.28,
    cam: { s0: 1.12, s1: 1.2, ox: "50%", oy: "14%", x0: 0, x1: 0, rot: 0, ry: 0 },
    words: [{ at: 1.1, kicker: "COMENTA", big: "WORKSHOP", copper: true }],
    icons: [{ at: 1.15, kind: "chat", x: 950, y: 1150 }],
  },
];

const STARTS = SHOTS.reduce<number[]>((acc, s, i) => [...acc, i === 0 ? 0 : acc[i - 1] + F(SHOTS[i - 1].dur)], []);
const TOTAL = STARTS[STARTS.length - 1] + F(SHOTS[SHOTS.length - 1].dur);
export const ADCROMO_DURATION = TOTAL + 36;

// ── Texto cromado ──────────────────────────────────────────────────────────
const chromeFill = (copper?: boolean): React.CSSProperties => ({
  backgroundImage: copper
    ? "linear-gradient(180deg,#FFF4E2 0%,#F7C68A 22%,#C9772A 47%,#8A4A12 52%,#E7A15A 62%,#FFE2BC 82%,#B86A22 100%)"
    : "linear-gradient(180deg,#FFFFFF 0%,#DDE6F2 22%,#8C9AB0 47%,#46546B 52%,#C3CEDD 62%,#FFFFFF 82%,#9AA8BC 100%)",
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
  WebkitTextStroke: copper ? "1.5px #6A3A0E" : "1.5px #2A3445",
  filter: "drop-shadow(0 5px 0 rgba(10,20,40,.55)) drop-shadow(0 14px 22px rgba(0,0,0,.55))",
});

const ChromeWord: React.FC<{ w: Word; start: number; end: number; instant?: boolean }> = ({ w, start, end, instant }) => {
  const frame = useCurrentFrame();
  const t0 = start;
  const pout = progress(frame, end - 5, 5, ease.in);
  if (frame < t0 - 1 || frame >= end) return null;
  const letters = [...w.big];
  const kp = instant ? 1 : progress(frame, t0, 8);
  const size = Math.min(150, Math.floor(1000 / (w.big.length * 0.66)));
  return (
    <div style={{ position: "absolute", left: 30, right: 30, top: 1290, textAlign: "center", opacity: 1 - pout, transform: `translateY(${pout * -20}px)` }}>
      <div style={{ fontFamily: NUNITO, fontWeight: 800, fontSize: 40, letterSpacing: 4, color: "#FFFFFF", textShadow: "0 3px 10px rgba(0,0,0,.7)", opacity: kp, transform: `translateY(${(1 - kp) * 14}px)` }}>
        {w.kicker}
      </div>
      <div style={{ fontFamily: OVERPASS, fontWeight: 900, fontSize: size, lineHeight: 1.05, letterSpacing: "-0.01em", marginTop: 4, whiteSpace: "nowrap" }}>
        {letters.map((ch, i) => {
          const a = t0 + 3 + i * 1.6;
          const p = instant ? 1 : spring({ frame: frame - a, fps: FPS, config: { damping: 13, stiffness: 220 } });
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                ...chromeFill(w.copper),
                opacity: Math.min(1, p * 2),
                transform: `translateY(${(1 - p) * 40}px) scale(${1.35 - 0.35 * p})`,
                minWidth: ch === " " ? "0.28em" : undefined,
              }}
            >
              {ch}
            </span>
          );
        })}
      </div>
      {/* brillo que recorre la palabra */}
      {!instant && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 50,
            height: size * 1.1,
            background: "linear-gradient(100deg, transparent 40%, rgba(255,255,255,.55) 50%, transparent 60%)",
            mixBlendMode: "overlay",
            transform: `translateX(${interpolate(frame, [t0 + 6, t0 + 26], [-900, 900], clamp)}px)`,
            pointerEvents: "none",
          }}
        />
      )}
    </div>
  );
};

// ── Íconos cromados 3D ─────────────────────────────────────────────────────
const Glyph: React.FC<{ kind: string }> = ({ kind }) => {
  const s = { fill: "none", stroke: "#FFFFFF", strokeWidth: 7, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (kind === "doc")
    return (
      <svg width={96} height={96} viewBox="0 0 100 100">
        <path d="M28 12 H62 L78 28 V88 H28 Z" {...s} />
        <path d="M62 12 V28 H78 M38 46 H68 M38 60 H68 M38 74 H58" {...s} />
      </svg>
    );
  if (kind === "cal")
    return (
      <svg width={96} height={96} viewBox="0 0 100 100">
        <rect x={16} y={22} width={68} height={62} rx={10} {...s} />
        <path d="M16 40 H84 M34 14 V28 M66 14 V28" {...s} />
        <text x="50" y="76" textAnchor="middle" fontFamily={OVERPASS} fontWeight={900} fontSize="28" fill="#FFFFFF">
          17
        </text>
      </svg>
    );
  if (kind === "cam")
    return (
      <svg width={96} height={96} viewBox="0 0 100 100">
        <rect x={12} y={30} width={54} height={40} rx={9} {...s} />
        <path d="M66 44 L88 32 V68 L66 56 Z" {...s} />
      </svg>
    );
  return (
    <svg width={96} height={96} viewBox="0 0 100 100">
      <path d="M18 22 H82 V66 H46 L28 82 V66 H18 Z" {...s} />
      <path d="M32 40 H68 M32 52 H56" {...s} />
    </svg>
  );
};

const ChromeIcon: React.FC<{ kind: string; x: number; y: number; start: number; end: number }> = ({ kind, x, y, start, end }) => {
  const frame = useCurrentFrame();
  if (frame < start || frame >= end) return null;
  const p = spring({ frame: frame - start, fps: FPS, config: { damping: 9, stiffness: 160 } });
  const pout = progress(frame, end - 5, 5, ease.in);
  const bob = Math.sin((frame - start) / 9) * 8;
  const S = 200;
  return (
    <div style={{ position: "absolute", left: x - S / 2, top: y - S / 2 + bob, width: S, height: S, perspective: 800, opacity: (1 - pout) * Math.min(1, p * 2) }}>
      <div
        style={{
          width: S,
          height: S,
          borderRadius: 46,
          padding: 9,
          boxSizing: "border-box",
          background: "conic-gradient(from 210deg, #FFFFFF, #8C9AB0, #F2F6FB, #46546B, #DDE6F2, #FFFFFF)",
          boxShadow: "0 22px 40px rgba(0,0,0,.55), 0 0 30px rgba(215,134,49,.35)",
          transform: `rotateY(${(1 - p) * 75 + Math.sin((frame - start) / 14) * 10}deg) rotateX(${(1 - p) * -20}deg) scale(${0.5 + 0.5 * p - pout * 0.3})`,
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            borderRadius: 38,
            background: kind === "revit" ? "#FFFFFF" : "linear-gradient(160deg,#2A4370,#0D1E3A)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
            overflow: "hidden",
          }}
        >
          {kind === "revit" ? <Img src={LOGO("revit.png")} style={{ width: 110 }} /> : <Glyph kind={kind} />}
          <div style={{ position: "absolute", inset: 0, background: "linear-gradient(135deg, rgba(255,255,255,.55) 0%, transparent 38%)" }} />
        </div>
      </div>
    </div>
  );
};

// ── Composición ────────────────────────────────────────────────────────────
export const AdCromo: React.FC = () => {
  const frame = useCurrentFrame();
  const endCard = progress(frame, TOTAL - 4, 12);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {SHOTS.map((s, i) => {
        const st = STARTS[i];
        const len = F(s.dur);
        const local = frame - st;
        if (local < -2 || local > len + 1 && i < SHOTS.length - 1) return null;
        const t = interpolate(local, [0, len], [0, 1], { ...clamp, easing: ease.inOut });
        const sc = s.cam.s0 + (s.cam.s1 - s.cam.s0) * t;
        const tx = s.cam.x0 + (s.cam.x1 - s.cam.x0) * t;
        // barrido de entrada y salida (falso cambio de cámara)
        const pin = i === 0 ? 1 : progress(frame, st - 1, 6);
        const pout = i === SHOTS.length - 1 ? 0 : progress(frame, st + len - 5, 5, ease.in);
        const dir = i % 2 ? -1 : 1;
        const whipX = (1 - pin) * 380 * dir - pout * 380 * dir;
        const blur = (1 - pin) * 28 + pout * 28;
        return (
          <Sequence key={i} from={st} durationInFrames={i === SHOTS.length - 1 ? len + 36 : len + 1} layout="none">
            <AbsoluteFill style={{ overflow: "hidden", perspective: 1400 }}>
              <AbsoluteFill
                style={{
                  transform: `translateX(${tx + whipX}px) rotateY(${s.cam.ry}deg) rotate(${s.cam.rot}deg) scale(${sc})`,
                  transformOrigin: `${s.cam.ox} ${s.cam.oy}`,
                  filter: blur > 0.5 ? `blur(${blur}px)` : undefined,
                }}
              >
                <OffthreadVideo src={staticFile(`adcromo/${s.src}`)} startFrom={F(s.from)} style={{ width: 1080, height: 1920 }} />
              </AbsoluteFill>
              {/* viñeta y degradado inferior para leer el texto */}
              <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,.25) 0%, transparent 18%, transparent 55%, rgba(5,12,28,.75) 100%)" }} />
            </AbsoluteFill>
            {s.words.map((w, k) => {
              const a = F(w.at);
              const b = k + 1 < s.words.length ? F(s.words[k + 1].at) : len + (i === SHOTS.length - 1 ? 36 : 0);
              return (
                <Sequence key={k} from={0} layout="none">
                  <ChromeWord w={w} start={a} end={b} instant={i === 0 && k === 0} />
                </Sequence>
              );
            })}
            {(s.icons ?? []).map((ic, k) => (
              <ChromeIcon key={k} kind={ic.kind} x={ic.x} y={ic.y} start={F(ic.at)} end={len + (i === SHOTS.length - 1 ? 36 : 0)} />
            ))}
            <Audio src={staticFile(`adcromo/${s.src}`)} startFrom={F(s.from)} endAt={F(s.from + s.dur)} />
          </Sequence>
        );
      })}
      {/* destello blanco antes del bloque de fecha */}
      {SHOTS.map((s, i) =>
        s.flash ? (
          <AbsoluteFill key={`fl${i}`} style={{ background: "#FFFFFF", opacity: interpolate(frame, [STARTS[i] - 3, STARTS[i], STARTS[i] + 8], [0, 0.95, 0], clamp), pointerEvents: "none" }} />
        ) : null,
      )}
      {/* cierre con logo */}
      {endCard > 0 && (
        <AbsoluteFill style={{ background: `rgba(13,30,58,${0.96 * endCard})`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 40 }}>
          <Img src={staticFile("logo-dma.png")} style={{ width: 560, opacity: endCard }} />
          <div style={{ fontFamily: OVERPASS, fontWeight: 900, fontSize: 88, letterSpacing: "-0.01em", ...chromeFill(true), opacity: endCard }}>COMENTA WORKSHOP</div>
          <div style={{ fontFamily: NUNITO, fontWeight: 800, fontSize: 38, letterSpacing: 3, color: "#FFFFFF", opacity: endCard }}>MARTES 17 DE NOVIEMBRE · 8 PM · GRATIS</div>
        </AbsoluteFill>
      )}
      <Img src={staticFile("logo-dma.png")} style={{ position: "absolute", width: 260, left: 410, top: 150, opacity: endCard > 0 ? 0 : 0.95, filter: "drop-shadow(0 2px 6px rgba(0,0,0,.6))" }} />
      <Audio src={staticFile("rutas/musica_master.wav")} volume={0.06} />
      {STARTS.slice(1).map((st, i) => (
        <Sequence key={`w${i}`} from={st - 5} durationInFrames={20}>
          <Audio src={staticFile("rutas/whoosh.wav")} volume={0.5} />
        </Sequence>
      ))}
      {SHOTS.flatMap((s, i) =>
        (s.icons ?? []).map((ic, k) => (
          <Sequence key={`ic${i}${k}`} from={STARTS[i] + F(ic.at)} durationInFrames={30}>
            <Audio src={staticFile("sfx/interface/drop_002.ogg")} volume={0.35} />
          </Sequence>
        )),
      )}
    </AbsoluteFill>
  );
};
