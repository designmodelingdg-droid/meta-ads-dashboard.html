// Kit de marca compartido (mismas letras, colores y resortes que historias-dma/Promo.tsx, Faltan.tsx y black-friday/BF.tsx).
import React from "react";
import { AbsoluteFill, Img, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export const BEBAS = "BebasLocal";
export const MONT = "MontLocal";
if (typeof document !== "undefined") {
  const h = delayRender("fuentes");
  const fs = [
    new FontFace(BEBAS, `url(${staticFile("fonts/BebasNeue-400-latin.woff2")})`, { weight: "400" }),
    ...["600", "700", "800", "900"].map((w) => new FontFace(MONT, `url(${staticFile(`fonts/Montserrat-${w}-latin.woff2`)})`, { weight: w })),
  ];
  Promise.all(fs.map((f) => f.load())).then((l) => { l.forEach((f) => (document.fonts as any).add(f)); continueRender(h); }).catch(() => continueRender(h));
}

export const NAVY = "#0D1E3A";
export const NAVY2 = "#0C2442";
export const DEEP = "#05142A";
export const OR = "#E8893A";
export const CU = "#D78631";
export const INK = "#0F1E33";
export const RED = "#E5252A";
export const FPS = 30;
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const F = (s: number) => Math.round(s * FPS);

// Fondo navy con plano técnico (el de Promo.tsx). Con `photo`, una foto desenfocada debajo del velo.
export const Bg: React.FC<{ photo?: string; veil?: number }> = ({ photo, veil = 0.84 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 0%, ${NAVY2} 0%, #071A2F 55%, ${DEEP} 100%)`, overflow: "hidden" }}>
      {photo && <Img src={staticFile(photo)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", filter: "blur(22px)", transform: `scale(${1.15 + 0.03 * Math.sin(f / 80)})` }} />}
      {photo && <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(12,36,66,${veil}) 0%, rgba(5,20,42,${Math.min(1, veil + 0.08)}) 100%)` }} />}
      <Img src={staticFile("bp.svg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.16, transform: `scale(${1.05 + 0.04 * Math.sin(f / 90)}) translateY(${-f * 0.12}px)` }} />
    </AbsoluteFill>
  );
};

// Design Modeling + Autodesk Authorized Training Center
export const Logos: React.FC<{ y: number; h?: number }> = ({ y, h = 70 }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center", alignItems: "center", gap: h * 0.36 }}>
    <Img src={staticFile("logo-claro.png")} style={{ height: h }} />
    <div style={{ width: 2, height: h * 0.8, background: "rgba(255,255,255,.35)" }} />
    <Img src={staticFile("marcas/atc-wht.png")} style={{ height: h * 0.74 }} />
  </div>
);

export const Pop: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties; dy?: number }> = ({ at, children, style, dy = 40 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const k = spring({ frame: f - at, fps, config: { damping: 14, stiffness: 170 } });
  return <div style={{ opacity: interpolate(f - at, [0, 6], [0, 1], clamp), transform: `translateY(${(1 - k) * dy}px) scale(${0.94 + 0.06 * k})`, filter: `blur(${(1 - Math.min(1, k)) * 6}px)`, ...style }}>{children}</div>;
};

export const card: React.CSSProperties = { background: "#fff", borderRadius: 34, boxShadow: "0 30px 70px rgba(0,0,0,.45)", color: INK };

// Texto cromado letra a letra (Faltan.tsx). `at` en fotogramas; con at < 0 ya está puesto en el fotograma 0 (portada).
export const Chrome: React.FC<{ text: string; size: number; at: number; copper?: boolean }> = ({ text, size, at, copper }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const grad = copper ? "linear-gradient(180deg,#F4A35C 0%,#E8893A 55%,#D9772A 100%)" : "linear-gradient(180deg,#FFFFFF 0%,#FFFFFF 45%,#D3D8DF 100%)";
  return (
    <div style={{ display: "flex", justifyContent: "center", gap: size * 0.02 }}>
      {text.split("").map((ch, i) => {
        const p = spring({ frame: frame - at - i * 1.6, fps, config: { damping: 12, stiffness: 170 } });
        return (
          <span key={i} style={{
            fontFamily: BEBAS, fontWeight: 400, fontSize: size, lineHeight: 1, letterSpacing: "-0.01em",
            backgroundImage: grad, WebkitBackgroundClip: "text", color: "transparent", WebkitTextStroke: `${Math.max(2, size / 60)}px ${NAVY}`,
            filter: `blur(${(1 - p) * 10}px) drop-shadow(0 ${size / 18}px 0 ${NAVY}) drop-shadow(0 8px 18px rgba(13,30,58,.45))`,
            transform: `translateY(${(1 - p) * 30}px) scale(${1.3 - 0.3 * p})`, opacity: p, display: "inline-block", whiteSpace: "pre",
          }}>{ch}</span>
        );
      })}
    </div>
  );
};

// Chip que entra con resorte (Faltan.tsx)
export const Chip: React.FC<{ text: string; at: number; x: number; y: number; dark?: boolean; size?: number }> = ({ text, at, x, y, dark = true, size = 50 }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const p = spring({ frame: frame - at, fps, config: { damping: 11, stiffness: 180 } });
  return (
    <div style={{
      position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) scale(${p}) rotate(${(1 - p) * -8}deg)`,
      background: dark ? NAVY : OR, color: "#fff", border: `3px solid ${dark ? OR : "#fff"}`, borderRadius: 999, padding: "8px 26px 4px",
      fontFamily: BEBAS, fontWeight: 400, fontSize: size, letterSpacing: 1, boxShadow: "0 10px 24px rgba(13,30,58,.35)", whiteSpace: "nowrap", opacity: Math.min(1, p * 1.5),
    }}>{text}</div>
  );
};

// Línea de titular en caja (subtítulo de la casa: Bebas blanca en caja navy con borde, o caja naranja para la clave)
export const BoxLine: React.FC<{ text: string; at: number; size?: number; kind?: "navy" | "or" | "plain" }> = ({ text, at, size = 104, kind = "navy" }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const k = spring({ frame: f - at, fps, config: { damping: 13, stiffness: 190 } });
  const st: React.CSSProperties = kind === "or" ? { background: OR, color: "#fff", border: "4px solid #fff" }
    : kind === "navy" ? { background: "rgba(13,30,58,.94)", color: "#fff", border: `4px solid ${OR}` }
    : { color: "#fff", WebkitTextStroke: `3px ${NAVY}`, paintOrder: "stroke fill", textShadow: "0 6px 18px rgba(0,0,0,.55)" };
  return (
    <div style={{ display: "flex", justifyContent: "center", opacity: Math.min(1, k * 1.6), transform: `translateY(${(1 - k) * 34}px) scale(${0.86 + 0.14 * k})`, filter: `blur(${(1 - Math.min(1, k)) * 8}px)` }}>
      <span style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 1, padding: kind === "plain" ? 0 : "12px 28px 2px", borderRadius: 14, whiteSpace: "nowrap", letterSpacing: 1, boxShadow: kind === "plain" ? undefined : "0 12px 30px rgba(0,0,0,.4)", ...st }}>{text}</span>
    </div>
  );
};

// Destello blanco de 4 fotogramas (Caja de efectos)
export const Flash: React.FC<{ at: number; color?: string }> = ({ at, color = "#fff" }) => {
  const f = useCurrentFrame();
  const o = interpolate(f - at, [-1, 1, 5], [0, 0.85, 0], clamp);
  return o > 0 ? <AbsoluteFill style={{ background: color, opacity: o, pointerEvents: "none" }} /> : null;
};

// Tamaño de Bebas para que la línea más larga quepa en `w` px
export const fit = (lines: string[], w: number, cap: number) => Math.floor(Math.min(cap, w / (Math.max(...lines.map((l) => l.length)) * 0.415)));
