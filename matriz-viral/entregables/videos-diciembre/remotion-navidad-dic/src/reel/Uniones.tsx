// «6 formas de unir una viga de acero a una columna: solo 3 pasan momento» · isométrico que se arma (kit Anatomy, como rutas/Conexion.tsx).
// 1 placa de cortante · 2 ángulos dobles al alma · 3 asiento → solo cortante (articulada); 4 placa de extremo extendida · 5 placas de ala empernadas ·
// 6 alas y alma soldadas → momento (rígida). Columna de ACERO (perfil H), no de hormigón.
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import * as I from "../anatomy/iso-kit.mjs";
import * as G from "../anatomy/lathe.mjs";
import T0 from "../../reels/uniones.json";
import { BEBAS, MONT, NAVY, OR, CU, FPS, F, clamp, Bg, Logos, Pop } from "../brand";
import { Tiempos, Subs, Cierre, Escenas } from "./base";
export const T = T0 as Tiempos;

type P3 = [number, number, number];
type Proj = { origin: [number, number]; scale: number; azimuth?: number; elevation?: number };
type Grp = "col" | "con" | "beam" | "bolt" | "weld";
type Part = { grp: Grp; ord: number; center: P3; from: P3; svg: string; lit: string; idx: number; hot: boolean };
const NOMBRE = ["PLACA DE CORTANTE", "ÁNGULOS DOBLES AL ALMA", "ASIENTO", "PLACA DE EXTREMO EXTENDIDA", "PLACAS DE ALA EMPERNADAS", "ALAS Y ALMA SOLDADAS"];
export const ISO_DMA = `
.iso{--anatomy-paper:#132648;--anatomy-face:#1B3560;--anatomy-top:#244274;
--anatomy-shade-0:#0F1F3B;--anatomy-shade-1:#142A4E;--anatomy-shade-2:#19335E;--anatomy-shade-3:#1F3C6C;
--anatomy-lit-top:#F2A95C;--anatomy-lit-shade:#B8681F;--anatomy-lit:#FFE3BF;
--anatomy-hi:#DCE6F5;--anatomy-mid:#9FB0CC;--anatomy-lo:#5C719A;--anatomy-faint:#3A5582;--anatomy-weight:2.2px;}
.iso-solid[data-lit]>.iso-fill{fill:#C97A2A}
`;
const D = 110, BF = 100, TF = 18, TW = 7;             // columna H: medio canto, medio ancho de ala, espesor de ala, medio espesor de alma
const ZB = 270, ZT = 570, FW = 80, FT = 16, WEB = 5;   // viga: cara inferior, cara superior, medio ancho de ala, espesor de ala, medio espesor de alma
const hex = (r: number): [number, number][] => Array.from({ length: 6 }, (_, k) => [r * Math.cos((k * Math.PI) / 3 + Math.PI / 6), r * Math.sin((k * Math.PI) / 3 + Math.PI / 6)]);

/** Geometría de la unión n (1..6) en coordenadas de mundo; se construye una vez por proyección. */
const build = (n: number, P: Proj, o: { len: number; z0: number; z1: number }): Part[] => {
  const parts: Part[] = []; let idx = 0;
  const S = (paths: unknown, lit: boolean) => I.solidSvg(paths, { lit, tone: "hi", crease: "faint" });
  const add = (grp: Grp, ord: number, center: P3, paths: unknown, from: P3 = [0, 0, 0], hot = false) => parts.push({ grp, ord, center, from, svg: S(paths, false), lit: S(paths, true), idx: grp === "bolt" ? idx++ : 0, hot });
  const slab = (x: number, y: number, w: number, d: number, z: number, h: number) => I.slabOf({ x, y, w, d, r: 0 }, z, h, P, 2, 0.5);
  const bolt = (at: P3, axis: P3, ord: number, hot = false) => { const Fr = G.frameAlong(at, axis);
    const sh = G.disc(-26, 0, 8, Fr, P); const hd = G.prismOf(Fr, hex(15), 0, 12, P);
    parts.push({ grp: "bolt", ord, center: at, from: [axis[0] * 260, axis[1] * 260, axis[2] * 220], svg: S(sh, false) + S(hd, false), lit: S(sh, true) + S(hd, true), idx: idx++, hot }); };
  // columna H con las alas perpendiculares a x (la viga llega por +x)
  const ring: [number, number][] = [[-D, -BF], [-D + TF, -BF], [-D + TF, -TW], [D - TF, -TW], [D - TF, -BF], [D, -BF], [D, BF], [D - TF, BF], [D - TF, TW], [-D + TF, TW], [-D + TF, BF], [-D, BF]];
  add("col", 0, [0, 0, (o.z0 + o.z1) / 2], I.extrude(ring, o.z0, o.z1 - o.z0, P, { convex: false, bevel: 0.6 }));
  const x0 = n === 4 ? D + 25 : n === 6 ? D + 2 : D + 12;      // arranque de la viga
  const BV: P3 = [300, 0, 0];                                    // la viga llega desde +x
  const viga = () => {
    add("beam", 20, [x0 + o.len / 2, 0, ZB + 8], slab(x0, -FW, o.len, 2 * FW, ZB, FT), BV);
    add("beam", 30, [x0 + o.len / 2, 0, (ZB + ZT) / 2], slab(x0, -WEB, o.len, 2 * WEB, ZB + FT, ZT - ZB - 2 * FT), BV);
    add("beam", 60, [x0 + o.len / 2, 0, ZT - 8], slab(x0, -FW, o.len, 2 * FW, ZT - FT, FT), BV);
  };
  const placaAlma = () => { add("con", 40, [D + 55, 10, 420], slab(D, WEB, 112, 10, 330, 180), [0, 240, 0], true);
    for (const z of [365, 420, 475]) bolt([D + 70, WEB + 10, z], [0, 1, 0], 45, true); };
  if (n === 1) { viga(); placaAlma(); }
  if (n === 2) { viga();
    add("con", 10, [D + 45, -10, 420], slab(D, -WEB - 10, 92, 10, 330, 180), [0, -240, 0], true); add("con", 10, [D + 5, -45, 420], slab(D, -80, 10, 80 - WEB, 330, 180), [0, -240, 0], true);
    add("con", 40, [D + 45, 10, 420], slab(D, WEB, 92, 10, 330, 180), [0, 240, 0], true); add("con", 41, [D + 5, 45, 420], slab(D, WEB, 10, 75, 330, 180), [0, 240, 0], true);
    for (const z of [365, 420, 475]) { bolt([D + 62, WEB + 10, z], [0, 1, 0], 45, true); bolt([D + 10, 56, z], [1, 0, 0], 46, true); } }
  if (n === 3) { viga();
    add("con", 8, [D + 6, 0, 205], slab(D, -FW, 12, 2 * FW, 140, 130), [0, 0, -200], true); add("con", 9, [D + 60, 0, ZB - 6], slab(D, -FW, 120, 2 * FW, ZB - 12, 12), [0, 0, -200], true);
    add("con", 70, [D + 50, 0, ZT + 5], slab(D, -60, 100, 120, ZT, 10), [0, 0, 220], true); add("con", 71, [D + 5, 0, ZT + 55], slab(D, -60, 10, 120, ZT, 100), [0, 0, 220], true);
    for (const y of [-40, 40]) { bolt([D + 12, y, 185], [1, 0, 0], 12, true); bolt([D + 10, y, ZT + 62], [1, 0, 0], 75, true); bolt([D + 62, y, ZT + 10], [0, 0, 1], 76, true); } }
  if (n === 4) { add("beam", 10, [D + 12, 0, 420], slab(D, -110, 25, 220, ZB - 95, ZT - ZB + 190), BV, true); viga();
    for (const y of [-55, 55]) for (const z of [ZB - 52, ZB + 52, ZT - 52, ZT + 52]) { const fuera = z < ZB || z > ZT; const oculto = y < 0 && z < ZT;
      bolt([x0, y, z], [1, 0, 0], oculto ? 15 : 80, fuera); } }
  if (n === 5) { viga(); placaAlma();
    add("con", 9, [D + 130, 0, ZB - 7], slab(D, -FW - 6, 260, 2 * FW + 12, ZB - 14, 14), [0, 0, -220], true);
    add("con", 70, [D + 130, 0, ZT + 7], slab(D, -FW - 6, 260, 2 * FW + 12, ZT, 14), [0, 0, 220], true);
    for (const x of [D + 80, D + 150, D + 220]) for (const y of [-45, 45]) bolt([x, y, ZT + 14], [0, 0, 1], 75, true); }
  if (n === 6) { viga();
    add("weld", 65, [D + 5, 0, ZT], slab(D, -FW, 12, 2 * FW, ZT - FT - 4, FT + 10), [0, 0, 0], true);
    add("weld", 25, [D + 5, 0, ZB], slab(D, -FW, 12, 2 * FW, ZB - 6, FT + 10), [0, 0, 0], true);
    add("weld", 42, [D + 5, 8, 420], slab(D, WEB, 12, 9, ZB + FT + 4, ZT - ZB - 2 * FT - 8), [0, 0, 0], true); }
  return parts;
};
const extent = (o: { len: number; z0: number; z1: number }, abierto: boolean): P3[] => [
  ...(I.boxCorners({ x: -D, y: -BF, w: 2 * D, d: 2 * BF }, o.z0, o.z1) as P3[]),
  [D + 25 + o.len + (abierto ? 300 : 0), -FW, ZB], [D + 25 + o.len + (abierto ? 300 : 0), FW, ZT], [D + 60, abierto ? 330 : 110, 420], [D + 60, 0, abierto ? 60 : 160], [D + 60, 0, abierto ? 800 : 700],
];

/** Una unión dibujada. k = 0 (despiezada) → 1 (armada) por grupo según el tiempo local t (s); t < 0 = ya armada. */
const Union: React.FC<{ n: number; w: number; h: number; t: number; grande?: boolean; apagada?: boolean; luz?: boolean }> = ({ n, w, h, t, grande, apagada, luz = true }) => {
  const o = grande ? { len: 430, z0: 70, z1: 770 } : { len: 300, z0: 150, z1: 700 };
  const P = React.useMemo(() => I.fitProjection(extent(o, !!grande), w, h, { pad: grande ? 24 : 10 }) as Proj, [w, h, grande]);
  const parts = React.useMemo(() => build(n, P, o), [n, P]);
  const ease = Easing.bezier(0.22, 1, 0.36, 1);
  const kOf = (p: Part) => { if (t < 0 || p.grp === "col") return 1;
    if (p.grp === "con") return interpolate(t, [0.15, 0.7], [0, 1], { ...clamp, easing: ease });
    if (p.grp === "beam") return interpolate(t, n === 4 ? [0.2, 0.9] : [0.55, 1.2], [0, 1], { ...clamp, easing: ease });
    if (p.grp === "bolt") return interpolate(t, [1.15 + p.idx * 0.07, 1.5 + p.idx * 0.07], [0, 1], { ...clamp, easing: ease });
    return 1; };
  const body = [...parts].map((p) => { const k = kOf(p); const off: P3 = [p.from[0] * (1 - k), p.from[1] * (1 - k), p.from[2] * (1 - k)];
      const c: P3 = [p.center[0] + off[0], p.center[1] + off[1], p.center[2] + off[2]]; return { p, off, k, depth: I.depthOf(c, P) as number }; })
    .sort((a, b) => a.p.ord - b.p.ord || a.depth - b.depth)
    .map(({ p, off, k }) => { const soldadura = p.grp === "weld" ? interpolate(t < 0 ? 9 : t, [1.2, 1.9], [0, 1], clamp) : 1;
      const lit = luz && !apagada && p.hot && (p.grp !== "bolt" || k > 0.98 || t < 0);
      return `<g transform="${I.translateAlong(P, off)}" opacity="${p.grp === "bolt" ? Math.min(1, k * 3) : soldadura}">${lit ? p.lit : p.svg}</g>`; }).join("");
  return <svg className="iso-svg" width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ display: "block", filter: apagada ? "grayscale(1) brightness(.75)" : undefined, opacity: apagada ? 0.6 : 1 }} dangerouslySetInnerHTML={{ __html: body }} />;
};

const CW = 320, CH0 = 372, GX = 14, MX = 46, MY0 = 600;
const Mosaico: React.FC<{ modo: "portada" | "sello" | "resumen"; d: number }> = ({ modo, d }) => { const CH = modo === "resumen" ? 330 : CH0; const MY = modo === "resumen" ? 584 : MY0;
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const a1 = d * 0.08, a2 = d * 0.36;
  return (<>{[1, 2, 3, 4, 5, 6].map((n, i) => { const col = i % 3, row = Math.floor(i / 3); const x = MX + col * (CW + GX), y = MY + row * (CH + 22 + (modo === "resumen" ? 80 : 0));
    const rig = n > 3; const on = modo === "resumen" ? t >= (rig ? a2 : a1) : false; const s = modo === "resumen" && on ? spring({ frame: f - F(rig ? a2 : a1) - col * 3, fps, config: { damping: 12 } }) : 0;
    const flot = modo === "portada" ? Math.sin(f / 14 + i) * 5 : 0;
    return (<div key={n} style={{ position: "absolute", left: x, top: y + flot, width: CW, height: CH, borderRadius: 22, background: "rgba(19,38,72,.9)", border: `3px solid ${modo === "resumen" && on ? (rig ? OR : "#7C8AA3") : "rgba(232,137,58,.55)"}`,
      overflow: "hidden", opacity: modo === "sello" ? interpolate(t, [0, 0.3], [1, 0.3], clamp) : 1, transform: `scale(${1 + 0.04 * s * (rig ? 1 : 0)})`, boxShadow: "0 16px 40px rgba(0,0,0,.4)" }}>
      <Union n={n} w={CW} h={CH} t={-1} apagada={modo === "resumen" && on && !rig} luz={modo !== "resumen" || (on && rig)} />
      <div style={{ position: "absolute", left: 14, top: 2, fontFamily: BEBAS, fontSize: 96, lineHeight: 1, color: modo === "resumen" && on && !rig ? "#9FB0CC" : OR, textShadow: "0 4px 0 rgba(0,0,0,.35)" }}>{n}</div>
      {modo === "resumen" && on && <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, background: rig ? OR : "#5C6B85", color: "#fff", fontFamily: MONT, fontWeight: 900, fontSize: 21, letterSpacing: 1, textAlign: "center", padding: "7px 0", opacity: s }}>{rig ? "CORTANTE + MOMENTO" : "SOLO CORTANTE"}</div>}
    </div>); })}</>);
};
export const Base: React.FC<{ children: React.ReactNode; first?: boolean }> = ({ children, first }) => { const f = useCurrentFrame();
  const w = first ? 0 : interpolate(f, [0, 7], [1, 0], clamp);
  return (<AbsoluteFill className="iso" style={{ overflow: "hidden" }}><style>{I.ISO_CSS + ISO_DMA}</style><Bg />
    <AbsoluteFill style={{ transform: `translateX(${w * 140}px)`, filter: w > 0.02 ? `blur(${w * 14}px)` : undefined, opacity: 1 - w * 0.4 }}><Logos y={128} h={64} />{children}</AbsoluteFill></AbsoluteFill>);
};

const Portada: React.FC<{ d: number }> = ({ d }) => (<Base first>
  <div style={{ position: "absolute", left: 30, right: 30, top: 232, textAlign: "center", fontFamily: BEBAS, fontSize: 100, lineHeight: 0.95, color: "#fff", letterSpacing: 1 }}>6 FORMAS DE UNIR UNA VIGA<br />DE ACERO A UNA COLUMNA</div>
  <div style={{ position: "absolute", left: 0, right: 0, top: 440, textAlign: "center" }}><span style={{ fontFamily: BEBAS, fontSize: 66, lineHeight: 1, color: "#fff", background: CU, borderRadius: 12, padding: "12px 26px 2px" }}>¿CUÁL USAS TÚ? DINOS EL NÚMERO</span></div>
  <Mosaico modo="portada" d={d} /></Base>);
const SelloEsc: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); const k = spring({ frame: f - 6, fps, config: { damping: 9, stiffness: 220 } }); const k2 = spring({ frame: f - 26, fps, config: { damping: 12 } });
  return (<Base first>
    <div style={{ position: "absolute", left: 30, right: 30, top: 232, textAlign: "center", fontFamily: BEBAS, fontSize: 100, lineHeight: 0.95, color: "#fff", letterSpacing: 1, opacity: 0.35 }}>6 FORMAS DE UNIR UNA VIGA<br />DE ACERO A UNA COLUMNA</div>
    <Mosaico modo="sello" d={d} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", transform: `rotate(-5deg) scale(${1.8 - 0.8 * Math.min(1, k)})`, opacity: Math.min(1, k * 2) }}>
      <span style={{ display: "inline-block", fontFamily: BEBAS, fontSize: 150, lineHeight: 0.95, color: "#fff", background: CU, border: "7px solid #fff", borderRadius: 20, padding: "22px 40px 8px", boxShadow: "0 24px 60px rgba(0,0,0,.55)" }}>SOLO 3<br />PASAN MOMENTO</span></div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 1190, textAlign: "center", fontFamily: BEBAS, fontSize: 110, color: "#fff", opacity: k2, transform: `translateY(${(1 - k2) * 30}px)`, textShadow: "0 6px 20px rgba(0,0,0,.6)" }}>¿SABES CUÁLES?</div>
  </Base>); };
const Una: React.FC<{ n: number; d: number }> = ({ n, d }) => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps; const k = spring({ frame: f - 3, fps, config: { damping: 12, stiffness: 190 } });
  const nombre = NOMBRE[n - 1]; const size = nombre.length > 20 ? 92 : nombre.length > 14 ? 108 : 150;
  return (<Base>
    <div style={{ position: "absolute", left: 60, top: 236, fontFamily: BEBAS, fontSize: 300, lineHeight: 0.86, color: OR, transform: `scale(${0.6 + 0.4 * k})`, transformOrigin: "0 50%", textShadow: "0 8px 0 rgba(0,0,0,.3)" }}>{n}</div>
    <div style={{ position: "absolute", left: 230, right: 40, top: 250, height: 230, display: "flex", alignItems: "center", opacity: Math.min(1, k * 1.4), transform: `translateX(${(1 - k) * 40}px)` }}>
      <div style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 0.95, color: "#fff", letterSpacing: 1 }}>{nombre}</div></div>
    <div style={{ position: "absolute", left: 20, top: 500, transform: `scale(${1.13 + 0.04 * Math.min(1, t / Math.max(1, d))})`, transformOrigin: "30% 45%" }}><Union n={n} w={1040} h={880} t={t} grande /></div>
    <div style={{ position: "absolute", left: 60, top: 1322, fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: 4, color: "#9FB0CC" }}>UNIÓN {n} DE 6</div>
  </Base>); };
const Resumen: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const t = f / 30; const a1 = d * 0.08, a2 = d * 0.36;
  const fila = (y: number, txt: string, sub: string, color: string, at: number) => t >= at && <Pop at={F(at)} style={{ position: "absolute", left: MX, right: MX, top: y }}>
    <div style={{ display: "flex", alignItems: "baseline", gap: 18, justifyContent: "center" }}><span style={{ fontFamily: BEBAS, fontSize: 72, lineHeight: 1, color }}>{txt}</span><span style={{ fontFamily: MONT, fontWeight: 900, fontSize: 30, color: "#fff", letterSpacing: 2 }}>{sub}</span></div></Pop>;
  return (<Base>
    <div style={{ position: "absolute", left: 30, right: 30, top: 236, textAlign: "center", fontFamily: BEBAS, fontSize: 124, lineHeight: 0.95, color: "#fff" }}>SOLO 3 <span style={{ color: OR }}>PASAN MOMENTO</span></div>
    {fila(500, "1 · 2 · 3", "SOLO CORTANTE (ARTICULADA)", "#C9D3E3", a1)}
    {fila(932, "4 · 5 · 6", "MOMENTO (RÍGIDA)", OR, a2)}
    <Mosaico modo="resumen" d={d} />
  </Base>); };

export const Uniones: React.FC = () => { const E = T.escenas;
  return (<AbsoluteFill style={{ background: NAVY }}>
    <Escenas T={T}>{[
      <Portada d={E[0].dur + E[0].s} />, <SelloEsc d={E[1].dur} />, ...[1, 2, 3, 4, 5, 6].map((n) => <Una n={n} d={E[n + 1].dur} />), <Resumen d={E[8].dur} />,
      <Cierre titulo={<>¿CUÁL USAS TÚ?</>} fila opciones={[["1", ""], ["2", ""], ["3", ""], ["4", ""], ["5", ""], ["6", ""]]} pie="DINOS EL NÚMERO" boton="COMENTA «ACERO»" segunda="Más información de la Especialización en Acero: comenta TEMARIO" />,
    ]}</Escenas>
    <Subs T={T} />
  </AbsoluteFill>); };
