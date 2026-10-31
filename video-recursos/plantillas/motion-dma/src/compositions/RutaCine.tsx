import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { brand } from "../brand/brand";
import { ease, progress } from "../lib/motion";
import data from "../data/master.json";

// Ruta del Máster · versión cine: fondo negro, una línea de luz cobre que la cámara
// persigue con barridos, y un objeto protagonista por bloque. Voz IA de Gabriel.

type Word = { w: string; s: number; e: number };
type Scene = { start: number; dur: number };
const WORDS: Word[] = data.words;
const SCENES: Scene[] = data.scenes;
const FPS = 30;
const F = (s: number) => Math.round(s * FPS);
export const RC_DURATION = Math.ceil(data.total * FPS) + 15;

const K = {
  bg: "#05080F",
  copper: "#D78631",
  copperHi: "#F5B266",
  white: "#FFFFFF",
  muted: "#8C9BB5",
  card: "#0C1424",
  card2: "#111C31",
  red: "#FF4D4D",
  green: "#3FD89B",
};
const COL = ["#D78631", "#3B9EFF", "#3FD89B", "#A57BFF"];

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]/g, "");
const wordAt = (stem: string, after = 0): number => {
  const w = WORDS.find((x) => x.s >= after - 0.05 && norm(x.w).startsWith(stem));
  return w ? w.s : after;
};
const S = (i: number) => (i >= SCENES.length ? RC_DURATION : F(SCENES[i].start));
const after = (i: number) => SCENES[i].start;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const sp = (frame: number, at: number, damping = 14) => spring({ frame: frame - at, fps: FPS, config: { damping, stiffness: 160 } });

const BLOCKS = [
  { n: 1, name: "BIM PROFESSIONAL", words: [["COMPRENDE", "comprend"], ["ESTRUCTURA", "estructur"], ["IMPLEMENTA", "implement"]] },
  { n: 2, name: "BIM COORDINATION", words: [["INTEGRA", "integr"], ["COORDINA", "coordinas"], ["RESUELVE", "resuelv"]] },
  { n: 3, name: "BIM MANAGEMENT", words: [["PLANIFICA", "planific"], ["TIEMPO Y COSTOS", "tiempo"], ["DIRIGE", "dirig"]] },
  { n: 4, name: "BIM + AI", words: [["AUTOMATIZA", "automatiz"], ["DYNAMO", "dynamo"], ["PYTHON", "python"]] },
] as const;

// ── Utilidades de escena ──────────────────────────────────────────────────
const useStage = () => {
  const { width: W, height: H } = useVideoConfig();
  const V = H > W;
  return { W, H, V, cx: W / 2, cy: H * (V ? 0.47 : 0.47) };
};

/** Barrido de cámara: entra desde la derecha y sale hacia la izquierda con desenfoque. */
const Whip: React.FC<{ from: number; to: number; children: React.ReactNode; first?: boolean }> = ({ from, to, children, first }) => {
  const frame = useCurrentFrame();
  const { W } = useStage();
  if (frame < from - 8 || frame > to + 1) return null;
  const pin = first ? 1 : progress(frame, from - 7, 11);
  const pout = progress(frame, to - 6, 7, ease.in);
  const x = (1 - pin) * W * 0.75 - pout * W * 0.75;
  const blur = (1 - pin) * 26 + pout * 26;
  return (
    <AbsoluteFill style={{ transform: `translateX(${x}px)`, filter: blur > 0.5 ? `blur(${blur}px)` : undefined }}>{children}</AbsoluteFill>
  );
};

/** Línea de luz que entra por la izquierda, llega al centro y sale por la derecha. */
const LightLine: React.FC<{ from: number; to: number }> = ({ from, to }) => {
  const frame = useCurrentFrame();
  const { W, H, cx, cy } = useStage();
  const dy = H * 0.2;
  const dIn = `M ${-0.08 * W} ${cy + dy} C ${0.22 * W} ${cy + dy}, ${0.3 * W} ${cy}, ${cx} ${cy}`;
  const dOut = `M ${cx} ${cy} C ${0.7 * W} ${cy}, ${0.78 * W} ${cy - dy}, ${1.08 * W} ${cy - dy}`;
  const pIn = progress(frame, from - 2, 14, ease.inOut);
  const pOut = progress(frame, to - 14, 12, ease.inOut);
  const stroke = (d: string, p: number, key: string) => (
    <g key={key}>
      <path d={d} pathLength={1} fill="none" stroke={K.copper} strokeWidth={34} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - p} opacity={0.28} style={{ filter: "blur(14px)" }} />
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

/** Estallido de partículas al llegar la línea. */
const Burst: React.FC<{ at: number; color: string; r?: number }> = ({ at, color, r = 340 }) => {
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
      <div
        style={{
          position: "absolute",
          left: cx - r * p,
          top: cy - r * p,
          width: r * 2 * p,
          height: r * 2 * p,
          borderRadius: "50%",
          border: `4px solid ${color}`,
          opacity: (1 - p) * 0.8,
        }}
      />
    </>
  );
};

/** Tarjeta brillante con borde neón. */
const Glass: React.FC<{ w: number; h: number; color: string; children?: React.ReactNode; style?: React.CSSProperties }> = ({ w, h, color, children, style }) => (
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

/** Rótulo superior del bloque y palabra clave grande sincronizada con la voz. */
const BlockText: React.FC<{ b: (typeof BLOCKS)[number] }> = ({ b }) => {
  const frame = useCurrentFrame();
  const { H, V } = useStage();
  const col = COL[b.n - 1];
  const pl = progress(frame, S(b.n) + 4, 12);
  const times = b.words.map(([, stem]) => F(wordAt(stem, after(b.n))));
  let idx = -1;
  times.forEach((t, i) => {
    if (frame >= t - 3) idx = i;
  });
  const t = idx >= 0 ? times[idx] - 3 : 0;
  const pw = idx >= 0 ? progress(frame, t, 7) : 0;
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: H * (V ? 0.215 : 0.08),
          textAlign: "center",
          opacity: pl,
          transform: `translateY(${(1 - pl) * 20}px)`,
        }}
      >
        <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 34, letterSpacing: 8, color: col }}>BLOQUE {b.n} DE 4</div>
        <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 104 : 92, color: K.white, lineHeight: 1.05, textShadow: `0 0 30px ${col}66` }}>{b.name}</div>
      </div>
      {idx >= 0 && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: H * (V ? 0.71 : 0.8),
            textAlign: "center",
            fontFamily: brand.fontDisplay,
            fontSize: V ? 120 : 104,
            color: K.white,
            letterSpacing: 2,
            opacity: pw,
            filter: `blur(${(1 - pw) * 12}px)`,
            transform: `scale(${1.08 - 0.08 * pw})`,
            textShadow: `0 0 34px ${col}`,
          }}
        >
          {b.words[idx][0]}
        </div>
      )}
    </>
  );
};

// ── Protagonistas ─────────────────────────────────────────────────────────
const Docs: React.FC = () => {
  const frame = useCurrentFrame();
  const { cx, cy } = useStage();
  const items = [
    { t: "EIR", stem: "comprend" },
    { t: "BEP", stem: "estructur" },
    { t: "ISO 19650", stem: "implement" },
  ];
  return (
    <div style={{ position: "absolute", left: cx, top: cy, perspective: 1400 }}>
      {items.map((it, i) => {
        const at = Math.min(F(wordAt(it.stem, after(1))) - 6, S(1) + 14 + i * 6);
        const p = sp(frame, at, 13);
        const x = (i - 1) * 250;
        const rot = (i - 1) * 14;
        return (
          <div key={it.t} style={{ position: "absolute", transform: `translate(${x - 150}px, ${-210 + (1 - p) * 260}px) rotateY(${-rot}deg) rotateZ(${rot * 0.4}deg)`, opacity: Math.min(1, p * 1.6) }}>
            <Glass w={300} h={400} color={COL[0]}>
              <div style={{ position: "absolute", left: 34, top: 40, right: 34 }}>
                {[0, 1, 2, 3, 4, 5].map((k) => (
                  <div key={k} style={{ height: 14, borderRadius: 7, marginBottom: 22, width: `${[90, 70, 84, 60, 78, 50][k]}%`, background: k === 0 ? COL[0] : "rgba(255,255,255,.16)" }} />
                ))}
              </div>
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 34, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: it.t.length > 4 ? 56 : 84, color: K.white }}>{it.t}</div>
            </Glass>
          </div>
        );
      })}
    </div>
  );
};

const Layers: React.FC = () => {
  const frame = useCurrentFrame();
  const { cx, cy } = useStage();
  const L = [
    { t: "ARQ", c: "#3B9EFF" },
    { t: "EST", c: "#F5B266" },
    { t: "MEP", c: "#3FD89B" },
  ];
  const tInt = F(wordAt("integr", after(2))) - 4;
  const tCoord = F(wordAt("coordinas", after(2)));
  const tRes = F(wordAt("resuelv", after(2)));
  const merge = interpolate(frame, [tInt + 6, tCoord], [1, 0], { ...clamp, easing: ease.inOut });
  const clash = interpolate(frame, [tCoord, tCoord + 6], [0, 1], clamp);
  const fixed = progress(frame, tRes, 8);
  return (
    <div style={{ position: "absolute", left: cx, top: cy + 30 }}>
      {L.map((l, i) => {
        const p = sp(frame, Math.min(tInt, S(2) + 14) + i * 4, 15);
        const y = (i - 1) * (60 + 110 * merge) - (1 - p) * 300;
        return (
          <div
            key={l.t}
            style={{
              position: "absolute",
              left: -230,
              top: -230 + y,
              width: 460,
              height: 460,
              transform: "rotateX(60deg) rotateZ(45deg)",
              borderRadius: 28,
              border: `5px solid ${l.c}`,
              background: `${l.c}18`,
              boxShadow: `0 0 40px ${l.c}66, inset 0 0 50px ${l.c}33`,
              opacity: Math.min(1, p * 1.5),
              backgroundImage: `linear-gradient(${l.c}44 2px, transparent 2px), linear-gradient(90deg, ${l.c}44 2px, transparent 2px)`,
              backgroundSize: "46px 46px",
            }}
          />
        );
      })}
      {L.map((l, i) => {
        const p = sp(frame, Math.min(tInt, S(2) + 14) + i * 4 + 4, 15);
        const y = (i - 1) * (60 + 110 * merge);
        return (
          <div key={`t${l.t}`} style={{ position: "absolute", left: 270, top: y - 30, fontFamily: brand.fontDisplay, fontSize: 52, color: l.c, opacity: p * (merge > 0.05 ? 1 : 0.0) }}>
            {l.t}
          </div>
        );
      })}
      {clash > 0 && (
        <div
          style={{
            position: "absolute",
            left: -70,
            top: -100,
            width: 140,
            height: 140,
            borderRadius: "50%",
            background: fixed > 0.5 ? K.green : K.red,
            boxShadow: `0 0 ${60 + 30 * Math.sin(frame / 3)}px ${fixed > 0.5 ? K.green : K.red}`,
            transform: `scale(${clash * (1 + 0.15 * fixed)})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: brand.fontBody,
            fontWeight: 800,
            fontSize: 80,
            color: K.white,
          }}
        >
          {fixed > 0.5 ? "✓" : "!"}
        </div>
      )}
    </div>
  );
};

const Gantt: React.FC = () => {
  const frame = useCurrentFrame();
  const { cx, cy } = useStage();
  const tPlan = Math.min(F(wordAt("planific", after(3))) - 4, S(3) + 14);
  const tCost = F(wordAt("costos", after(3))) - 3;
  const tDir = F(wordAt("dirig", after(3))) - 3;
  const bars = [
    [0.0, 0.35],
    [0.18, 0.4],
    [0.32, 0.3],
    [0.5, 0.32],
    [0.62, 0.36],
  ];
  const pIn = sp(frame, tPlan, 15);
  const chips = ["4D", "5D"];
  return (
    <div style={{ position: "absolute", left: cx, top: cy }}>
      <div style={{ position: "absolute", transform: `translate(-380px, -230px) scale(${0.85 + 0.15 * pIn})`, opacity: Math.min(1, pIn * 1.5) }}>
        <Glass w={760} h={400} color={COL[2]}>
          {bars.map(([x, w], i) => {
            const g = interpolate(frame, [tPlan + 6 + i * 5, tPlan + 22 + i * 5], [0, 1], { ...clamp, easing: ease.out });
            return (
              <div key={i} style={{ position: "absolute", left: 50 + x * 660, top: 60 + i * 62, width: w * 660 * g, height: 34, borderRadius: 17, background: `linear-gradient(90deg, ${COL[2]}, #8FF0C8)`, boxShadow: `0 0 18px ${COL[2]}88` }} />
            );
          })}
          <div style={{ position: "absolute", left: 50 + 660 * interpolate(frame, [tPlan + 10, tDir + 20], [0, 0.98], clamp), top: 36, width: 4, height: 330, background: K.copperHi, boxShadow: `0 0 14px ${K.copperHi}` }} />
        </Glass>
      </div>
      {chips.map((c, i) => {
        const p = sp(frame, tCost + i * 5, 12);
        return (
          <div key={c} style={{ position: "absolute", transform: `translate(${-250 + i * 270}px, ${215 - (1 - p) * 80}px)`, opacity: Math.min(1, p * 1.6) }}>
            <div
              style={{
                width: 230,
                height: 150,
                borderRadius: 22,
                background: "linear-gradient(180deg,#1A2438,#0E1626)",
                border: `5px solid ${K.copper}`,
                boxShadow: `0 0 30px ${K.copper}77`,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: brand.fontDisplay,
                fontSize: 100,
                color: K.white,
              }}
            >
              {c}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const Nodes: React.FC = () => {
  const frame = useCurrentFrame();
  const { cx, cy, V } = useStage();
  const names = ["REVIT", "DYNAMO", "PYTHON", "IA"];
  const t0 = Math.min(F(wordAt("automatiz", after(4))) - 6, S(4) + 14);
  const tD = F(wordAt("dynamo", after(4))) - 3;
  const tP = F(wordAt("python", after(4))) - 3;
  const ats = [t0, tD - 4, tP - 4, tP + 8];
  const pos = V
    ? [
        { x: -230, y: -170 },
        { x: 230, y: -20 },
        { x: -230, y: 130 },
        { x: 230, y: 280 },
      ]
    : [
        { x: -540, y: 40 },
        { x: -180, y: -80 },
        { x: 180, y: 40 },
        { x: 540, y: -80 },
      ];
  return (
    <div style={{ position: "absolute", left: cx, top: cy }}>
      <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
        {pos.slice(1).map((p, i) => {
          const a = pos[i];
          const g = interpolate(frame, [ats[i + 1] - 6, ats[i + 1] + 2], [0, 1], clamp);
          const mx = (a.x + p.x) / 2;
          const d = V ? `M ${a.x} ${a.y} C ${a.x} ${(a.y + p.y) / 2}, ${p.x} ${(a.y + p.y) / 2}, ${p.x} ${p.y}` : `M ${a.x} ${a.y} C ${mx} ${a.y}, ${mx} ${p.y}, ${p.x} ${p.y}`;
          return (
            <g key={i}>
              <path d={d} pathLength={1} fill="none" stroke={COL[3]} strokeWidth={22} opacity={0.3} strokeDasharray="1 1" strokeDashoffset={1 - g} style={{ filter: "blur(8px)" }} />
              <path d={d} pathLength={1} fill="none" stroke="#D9C8FF" strokeWidth={6} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - g} />
            </g>
          );
        })}
      </svg>
      {names.map((n, i) => {
        const p = sp(frame, ats[i], 13);
        const ai = i === 3;
        const w = ai ? 230 : 250;
        const h = ai ? 230 : 130;
        return (
          <div key={n} style={{ position: "absolute", transform: `translate(${pos[i].x - w / 2}px, ${pos[i].y - h / 2}px) scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 1.6) }}>
            <Glass w={w} h={h} color={ai ? K.copper : COL[3]} style={ai ? { borderRadius: 40 } : undefined}>
              <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: brand.fontDisplay, fontSize: ai ? 110 : 54, color: K.white, textShadow: ai ? `0 0 30px ${K.copper}` : undefined }}>{n}</div>
            </Glass>
          </div>
        );
      })}
    </div>
  );
};

const Medal: React.FC<{ size: number }> = ({ size }) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: "50%",
      background: `radial-gradient(circle at 35% 30%, #FFFFFF 0%, ${K.copperHi} 30%, ${K.copper} 70%)`,
      border: "5px solid #FFE3BF",
      boxShadow: `0 0 26px ${K.copper}`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: size * 0.5,
      color: "#5A3008",
      fontFamily: brand.fontBody,
      fontWeight: 800,
    }}
  >
    ★
  </div>
);

const Shield: React.FC<{ size: number; color: string; n: number }> = ({ size, color, n }) => (
  <svg width={size} height={size * 1.15} viewBox="0 0 100 115" style={{ filter: `drop-shadow(0 0 18px ${color})` }}>
    <path d="M50 4 L92 18 L92 56 Q92 92 50 111 Q8 92 8 56 L8 18 Z" fill={K.card2} stroke={color} strokeWidth={6} />
    <text x="50" y="72" textAnchor="middle" fontFamily={brand.fontDisplay} fontSize="48" fill="#FFFFFF">
      {n}
    </text>
  </svg>
);

const Credentials: React.FC = () => {
  const frame = useCurrentFrame();
  const { W, H, V, cx, cy } = useStage();
  const tM = F(wordAt("microcredencial", after(5))) - 6;
  const tI = F(wordAt("insignia", after(5))) - 4;
  const tSep = F(wordAt("separado", after(5))) - 12;
  const caption = (txt: string, at: number, until: number) => {
    const p = progress(frame, at, 8) * (1 - progress(frame, until - 6, 6, ease.in));
    if (p <= 0) return null;
    return (
      <div style={{ position: "absolute", left: 0, right: 0, top: H * (V ? 0.71 : 0.8), textAlign: "center", fontFamily: brand.fontDisplay, fontSize: V ? 78 : 88, color: K.white, opacity: p, filter: `blur(${(1 - p) * 10}px)`, textShadow: `0 0 30px ${K.copper}` }}>
        {txt}
      </div>
    );
  };
  // Cadena de medallas que vuela por una curva
  const chain = Array.from({ length: 9 }, (_, i) => {
    const t = (frame - tM - i * 3) / 26;
    if (t < 0 || t > 1.4) return null;
    const u = Math.min(1, t);
    const x = -0.1 * W + u * 1.2 * W;
    const y = cy + Math.sin(u * Math.PI * 1.2) * -H * 0.12 + H * 0.05;
    const sc = 0.6 + Math.sin(u * Math.PI) * 0.7;
    return (
      <div key={i} style={{ position: "absolute", left: x - 60, top: y - 60, transform: `scale(${sc})`, filter: `blur(${(1 - Math.sin(u * Math.PI)) * 6 + 2}px)`, opacity: t > 1 ? 0 : 1 }}>
        <Medal size={120} />
      </div>
    );
  });
  const gap = interpolate(frame, [tSep, tSep + 16], [V ? 230 : 300, V ? 250 : 420], { ...clamp, easing: ease.inOut });
  const tilt = interpolate(frame, [tSep, tSep + 16], [0, 1], clamp);
  return (
    <>
      {chain}
      {[0, 1, 2, 3].map((i) => {
        const p = sp(frame, tI + i * 4, 12);
        const row = V ? { x: ((i % 2) - 0.5) * gap * 1.3, y: (Math.floor(i / 2) - 0.5) * gap * 1.45 } : { x: (i - 1.5) * gap, y: 0 };
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: cx + row.x - 90,
              top: cy + row.y - 104,
              transform: `scale(${p}) rotate(${(1 - p) * -25 + tilt * (i - 1.5) * 6}deg)`,
              opacity: Math.min(1, p * 2),
            }}
          >
            <Shield size={180} color={COL[i]} n={i + 1} />
          </div>
        );
      })}
      {caption("MICROCREDENCIAL POR MÓDULO", tM, tI)}
      {caption("INSIGNIA POR BLOQUE", tI, tSep)}
      {caption("SE CURSAN POR SEPARADO", tSep, S(6))}
    </>
  );
};

const Finale: React.FC = () => {
  const frame = useCurrentFrame();
  const { W, H, V, cx, cy } = useStage();
  const t0 = S(6);
  const tT = F(wordAt("titulo", after(6))) - 4;
  const tP = F(wordAt("pide", after(6))) - 3;
  const conv = interpolate(frame, [tT - 4, tT + 10], [0, 1], { ...clamp, easing: ease.inOut });
  const scroll = interpolate(frame, [t0, tT], [0, 1], clamp);
  const cards = BLOCKS.map((b, i) => {
    const step = V ? 560 : 640;
    const x0 = (i - 1.5) * step + (1 - scroll) * W * 0.9 - scroll * W * 0.05;
    const x = x0 * (1 - conv);
    const p = sp(frame, t0 + i * 3, 15);
    return (
      <div
        key={b.n}
        style={{
          position: "absolute",
          left: cx + x - 230,
          top: cy - 150 + i * conv * -6,
          transform: `perspective(1400px) rotateY(${-28 * (1 - conv)}deg) scale(${(0.9 + 0.1 * p) * (1 - conv * 0.25)})`,
          opacity: Math.min(1, p * 1.5) * (1 - progress(frame, tT + 8, 8)),
          filter: conv > 0 && conv < 1 ? `blur(${Math.sin(conv * Math.PI) * 10}px)` : `blur(${(1 - scroll) > 0.05 && scroll > 0 ? 3 : 0}px)`,
        }}
      >
        <Glass w={460} h={300} color={COL[i]}>
          <div style={{ position: "absolute", left: 36, top: 34, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 30, letterSpacing: 6, color: COL[i] }}>BLOQUE {b.n}</div>
          <div style={{ position: "absolute", left: 36, right: 30, bottom: 36, fontFamily: brand.fontDisplay, fontSize: 70, color: K.white, lineHeight: 1 }}>{b.name}</div>
        </Glass>
      </div>
    );
  });
  const pM = sp(frame, tT + 6, 13);
  const pE = progress(frame, tP, 12);
  return (
    <>
      {cards}
      <Burst at={tT + 2} color={K.copperHi} r={420} />
      {pM > 0.01 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: cy - (V ? 230 : 190), textAlign: "center", opacity: Math.min(1, pM * 1.5) * (1 - pE), transform: `scale(${0.85 + 0.15 * pM})` }}>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 38, letterSpacing: 10, color: K.copperHi }}>UN SOLO CAMINO</div>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 190 : 210, color: K.white, lineHeight: 1, textShadow: `0 0 50px ${K.copper}` }}>MÁSTER</div>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 64 : 66, color: K.white, marginTop: 6 }}>BIM MANAGEMENT + IA</div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 32, letterSpacing: 5, color: K.muted, marginTop: 20 }}>4 BLOQUES · 12 MESES · PROYECTO FINAL</div>
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
              opacity: Math.min(1, sp(frame, tP + 8) * 1.5),
              transform: `scale(${0.9 + 0.1 * sp(frame, tP + 8)})`,
            }}
          >
            PIDE INFORMACIÓN
          </div>
        </AbsoluteFill>
      )}
      <div style={{ display: "none" }}>{H}</div>
    </>
  );
};

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { W, H, V, cx, cy } = useStage();
  const t4 = F(wordAt("cuatro", 0)) - 3;
  const lines = Array.from({ length: 26 }, (_, i) => {
    const a = (i / 26) * Math.PI * 2 + (i % 3) * 0.05;
    const p = ((frame * 0.035 + (i * 0.37) % 1) % 1);
    const r0 = 260 + p * Math.max(W, H) * 0.7;
    const len = 80 + (i % 4) * 60;
    return (
      <div
        key={i}
        style={{
          position: "absolute",
          left: cx + Math.cos(a) * r0,
          top: cy + Math.sin(a) * r0,
          width: len,
          height: 4,
          borderRadius: 2,
          background: `linear-gradient(90deg, transparent, ${K.copperHi})`,
          transform: `rotate(${a}rad)`,
          transformOrigin: "0 50%",
          opacity: 0.5 * Math.sin(p * Math.PI),
        }}
      />
    );
  });
  const titleY = H * (V ? 0.36 : 0.3);
  return (
    <>
      {lines}
      <div style={{ position: "absolute", left: 0, right: 0, top: titleY, textAlign: "center" }}>
        <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 36, letterSpacing: 10, color: K.copperHi }}>¿CÓMO FUNCIONA?</div>
        <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 150 : 150, color: K.white, lineHeight: 1, textShadow: `0 0 50px ${K.copper}88` }}>
          LA RUTA DEL <span style={{ color: K.copperHi }}>MÁSTER</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: cx, top: H * (V ? 0.59 : 0.66) }}>
        <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
          <path d={`M ${-1.5 * (V ? 220 : 300)} 0 L ${1.5 * (V ? 220 : 300)} 0`} stroke={K.copperHi} strokeWidth={8} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - interpolate(frame, [t4, t4 + 18], [0, 1], clamp)} style={{ filter: `drop-shadow(0 0 10px ${K.copper})` }} />
        </svg>
        {[0, 1, 2, 3].map((i) => {
          const p = sp(frame, t4 + i * 5, 12);
          const x = (i - 1.5) * (V ? 220 : 300);
          return (
            <div key={i} style={{ position: "absolute", left: x - 70, top: -70, width: 140, height: 140, transform: `scale(${1 + 0.12 * Math.sin(Math.PI * Math.min(1, p))})`, opacity: frame < t4 ? 0.7 : 1 }}>
              <div style={{ position: "absolute", inset: 0, top: 12, borderRadius: "50%", background: "#5A3008" }} />
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  borderRadius: "50%",
                  background: frame >= t4 + i * 5 ? `radial-gradient(circle at 35% 30%, #FFE0B8, ${K.copperHi} 35%, ${K.copper} 75%)` : "radial-gradient(circle at 35% 30%, #3A4660, #1C2538)",
                  boxShadow: frame >= t4 + i * 5 ? `0 0 40px ${K.copper}` : "none",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: brand.fontDisplay,
                  fontSize: 80,
                  color: K.white,
                }}
              >
                {i + 1}
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
};

// ── Composición ───────────────────────────────────────────────────────────
export const RutaCine: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { W, H, V } = useStage();
  const tP = F(wordAt("pide", after(6))) - 3;
  // partículas de polvo en paralaje
  const dust = Array.from({ length: 40 }, (_, i) => {
    const x = ((i * 397) % W) - ((frame * (0.6 + (i % 5) * 0.5)) % W);
    const xx = x < 0 ? x + W : x;
    const y = (i * 211) % H;
    return <div key={i} style={{ position: "absolute", left: xx, top: y, width: 3 + (i % 3), height: 3 + (i % 3), borderRadius: "50%", background: K.copperHi, opacity: 0.12 + (i % 4) * 0.05 }} />;
  });
  return (
    <AbsoluteFill style={{ backgroundColor: K.bg, overflow: "hidden" }}>
      <AbsoluteFill style={{ background: `radial-gradient(55% 45% at 50% 47%, ${K.copper}22 0%, transparent 70%)` }} />
      {dust}

      <Whip from={0} to={S(1)} first>
        <Hook />
      </Whip>
      {BLOCKS.map((b, i) => (
        <Whip key={b.n} from={S(b.n)} to={S(b.n + 1)}>
          <LightLine from={S(b.n)} to={S(b.n + 1)} />
          <Burst at={S(b.n) + 12} color={COL[i]} />
          {b.n === 1 && <Docs />}
          {b.n === 2 && <Layers />}
          {b.n === 3 && <Gantt />}
          {b.n === 4 && <Nodes />}
          <BlockText b={b} />
        </Whip>
      ))}
      <Whip from={S(5)} to={S(6)}>
        <LightLine from={S(5)} to={S(6) + 999} />
        <Credentials />
      </Whip>
      <Whip from={S(6)} to={durationInFrames + 20}>
        <Finale />
      </Whip>

      <AbsoluteFill style={{ background: `radial-gradient(120% 90% at 50% 50%, transparent 55%, ${K.bg} 100%)`, pointerEvents: "none" }} />
      <Img
        src={staticFile("logo-dma.png")}
        style={{ position: "absolute", width: V ? 300 : 230, left: V ? 390 : W - 280, top: V ? 290 : 44, opacity: frame >= tP ? 0 : 0.95 }}
      />

      <Audio src={staticFile("rutas/voz_master.wav")} />
      <Audio
        src={staticFile("rutas/musica_master.wav")}
        volume={(f) => {
          const talk = WORDS.some((w) => f / FPS >= w.s - 0.25 && f / FPS <= w.e + 0.35);
          const end = interpolate(f, [durationInFrames - 20, durationInFrames], [1, 0], clamp);
          return (talk ? 0.07 : 0.3) * end;
        }}
      />
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <Sequence key={`wh${i}`} from={Math.max(0, S(i) - 8)} durationInFrames={20}>
          <Audio src={staticFile("rutas/whoosh.wav")} volume={0.5} />
        </Sequence>
      ))}
      {[1, 2, 3, 4].map((i) => (
        <Sequence key={`b${i}`} from={S(i) + 11} durationInFrames={40}>
          <Audio src={staticFile("sfx/interface/bong_001.ogg")} volume={0.4} />
        </Sequence>
      ))}
      <Sequence from={F(wordAt("cuatro", 0)) - 3} durationInFrames={40}>
        <Audio src={staticFile("sfx/casino/chips-stack-3.ogg")} volume={0.35} />
      </Sequence>
      <Sequence from={F(wordAt("microcredencial", after(5))) - 6} durationInFrames={40}>
        <Audio src={staticFile("sfx/casino/chips-handle-2.ogg")} volume={0.45} />
      </Sequence>
      <Sequence from={F(wordAt("insignia", after(5))) - 4} durationInFrames={40}>
        <Audio src={staticFile("sfx/impact/impactMetal_light_002.ogg")} volume={0.35} />
      </Sequence>
      <Sequence from={F(wordAt("titulo", after(6))) + 4} durationInFrames={60}>
        <Audio src={staticFile("sfx/impact/impactBell_heavy_000.ogg")} volume={0.35} />
      </Sequence>
    </AbsoluteFill>
  );
};
