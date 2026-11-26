// «¿Dónde revisas el cortante de tu zapata? 5 medidas» · isométrico (kit Anatomy). Datos literales del guion:
// 1 flexión en la cara de la columna · 2 cortante en una dirección a d de la cara · 3 punzonamiento a d/2 todo alrededor · 4 recubrimiento contra el suelo 75 mm · 5 d ≥ 150 mm · ACI 318-19.
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import * as I from "../anatomy/iso-kit.mjs";
import T0 from "../../reels/medidas.json";
import { BEBAS, MONT, NAVY, OR, CU, FPS, clamp } from "../brand";
import { Tiempos, Subs, Escenas, cuando } from "./base";
import { Base } from "./Uniones";
export const T = T0 as Tiempos;
const w = (i: number, re: RegExp, fb: number) => cuando(T, i, re, fb);

type P3 = [number, number, number];
type Proj = { origin: [number, number]; scale: number };
const L = 300, H = 140, C = 60, ZS = 34, DD = H - ZS, CH = 250, GND = 356, LIFT = 150;   // zapata 600×600×140, columna 120×120, acero a 34 del suelo → d = 106
const FW = 1040, FH = 800;
const P = I.fitProjection([...(I.boxCorners({ x: -GND, y: -GND, w: 2 * GND, d: 2 * GND }, -14, 0) as P3[]), [C, C, H + CH + LIFT], [-C, -C, H + CH + LIFT]], FW, FH, { pad: 14 }) as unknown as Proj;
const slab = (x: number, y: number, sw: number, d: number, z: number, h: number, b = 0.5) => I.slabOf({ x, y, w: sw, d, r: 0 }, z, h, P, 2, b);
const SUELO = I.solidSvg(slab(-GND, -GND, 2 * GND, 2 * GND, -14, 14), { tone: "lo", crease: "faint" });
const BARRAS = [-4, -3, -2, -1, 0, 1, 2, 3, 4].map((i) => I.solidSvg(slab(-L + 24, i * 62 - 5, 2 * L - 48, 10, ZS - 6, 10, 0), { lit: true, tone: "hi", crease: "none" })).join("")
  + [-4, -3, -2, -1, 0, 1, 2, 3, 4].map((i) => I.solidSvg(slab(i * 62 - 5, -L + 24, 10, 2 * L - 48, ZS + 4, 10, 0), { lit: true, tone: "hi", crease: "none" })).join("");
const ZAPATA = I.solidSvg(slab(-L, -L, 2 * L, 2 * L, 0, H, 0.6), { tone: "hi", crease: "faint" });
const COLUMNA = I.solidSvg(slab(-C, -C, 2 * C, 2 * C, H, CH, 0.6), { tone: "hi", crease: "faint" });
const S = (q: P3): [number, number] => I.iso(q, P) as [number, number];
const pts = (a: P3[]) => a.map((q) => S(q).map((v) => v.toFixed(1)).join(",")).join(" ");
const mv = (by: P3) => I.translateAlong(P, by) as string;

/** La zapata: suelo y parrilla fijos; hormigón (translúcido, para que se vea el acero) y columna pueden levantarse. */
const Zap: React.FC<{ lift?: number; hop?: number; colDz?: number; children?: React.ReactNode; scale?: number }> = ({ lift = 0, hop = 0.66, colDz = 0, children }) => (
  <svg className="iso-svg" width={FW} height={FH} viewBox={`0 0 ${FW} ${FH}`} style={{ display: "block", overflow: "visible" }}>
    <g dangerouslySetInnerHTML={{ __html: SUELO + BARRAS }} />
    <g transform={mv([0, 0, lift])} opacity={hop} dangerouslySetInnerHTML={{ __html: ZAPATA }} />
    <g transform={mv([0, 0, lift + colDz])} dangerouslySetInnerHTML={{ __html: COLUMNA }} />
    {children}
  </svg>);
// plano de corte vertical perpendicular a x
const Plano: React.FC<{ x: number; k?: number; op?: number; dash?: boolean; color?: string }> = ({ x, k = 1, op = 1, dash, color = OR }) => { const top = -16 + (H + 140) * k;
  return <polygon points={pts([[x, -L - 36, -16], [x, L + 36, -16], [x, L + 36, top], [x, -L - 36, top]])} fill={color} fillOpacity={0.2 * op} stroke={color} strokeWidth={5} strokeDasharray={dash ? "14 12" : undefined} strokeLinejoin="round" opacity={op} />; };
const Txt: React.FC<{ at: [number, number]; text: string; size?: number; color?: string; anchor?: "start" | "middle" | "end"; op?: number; bebas?: boolean }> = ({ at, text, size = 54, color = "#FFE3BF", anchor = "middle", op = 1, bebas }) => (
  <text x={at[0]} y={at[1]} textAnchor={anchor} fontFamily={bebas ? BEBAS : MONT} fontWeight={bebas ? 400 : 900} fontSize={size} fill={color} stroke="#0B1A33" strokeWidth={size * 0.16} paintOrder="stroke" strokeLinejoin="round" opacity={op}>{text}</text>);
// cota entre dos puntos 3D con topes; k = avance 0..1
const Cota: React.FC<{ a: P3; b: P3; k: number; label?: string; off?: [number, number]; size?: number; color?: string; anchor?: "start" | "middle" | "end" }> = ({ a, b, k, label, off = [0, -18], size = 58, color = "#FFE3BF", anchor = "middle" }) => { if (k <= 0) return null;
  const A = S(a), B0 = S(b), B: [number, number] = [A[0] + (B0[0] - A[0]) * k, A[1] + (B0[1] - A[1]) * k]; const ang = Math.atan2(B0[1] - A[1], B0[0] - A[0]); const nx = -Math.sin(ang) * 13, ny = Math.cos(ang) * 13;
  return (<g><g stroke={color} strokeWidth={6} strokeLinecap="round"><line x1={A[0]} y1={A[1]} x2={B[0]} y2={B[1]} /><line x1={A[0] - nx} y1={A[1] - ny} x2={A[0] + nx} y2={A[1] + ny} />{k > 0.95 && <line x1={B[0] - nx} y1={B[1] - ny} x2={B[0] + nx} y2={B[1] + ny} />}</g>
    {label && k > 0.6 && <Txt at={[(A[0] + B0[0]) / 2 + off[0], (A[1] + B0[1]) / 2 + off[1]]} text={label} size={size} color={color} anchor={anchor} op={interpolate(k, [0.6, 1], [0, 1], clamp)} />}</g>); };
const Bola: React.FC<{ at: [number, number]; n: string; r?: number }> = ({ at, n, r = 30 }) => (<g transform={`translate(${at[0]} ${at[1]})`}><circle r={r} fill={OR} stroke="#fff" strokeWidth={4} /><text y={r * 0.42} textAnchor="middle" fontFamily={BEBAS} fontSize={r * 1.5} fill="#fff">{n}</text></g>);
// «d», «d/2», «mm» y «≥» en Montserrat: Bebas no tiene minúsculas
const dm = (s: string): React.ReactNode => s.split(/(d\/2|\bd\b|mm|≥)/g).map((x, i) => (i % 2 ? <span key={i} style={{ fontFamily: `${MONT}, "DejaVu Sans"`, fontWeight: 900, fontSize: x === "mm" ? "0.6em" : "0.78em", letterSpacing: 0 }}>{x}</span> : x));
const tt = () => useCurrentFrame() / FPS;
const kk = (t: number, a: number, d = 0.4, e = Easing.bezier(0.22, 1, 0.36, 1)) => interpolate(t, [a, a + d], [0, 1], { ...clamp, easing: e });

const Cab: React.FC<{ n: string; a: React.ReactNode; sub: string; size?: number }> = ({ n, a, sub, size = 118 }) => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); const k = spring({ frame: f - 3, fps, config: { damping: 12, stiffness: 190 } }); const k2 = spring({ frame: f - 12, fps, config: { damping: 12 } });
  return (<>
    <div style={{ position: "absolute", left: 56, top: 236, fontFamily: BEBAS, fontSize: 300, lineHeight: 0.86, color: OR, transform: `scale(${0.6 + 0.4 * k})`, transformOrigin: "0 50%", textShadow: "0 8px 0 rgba(0,0,0,.3)" }}>{n}</div>
    <div style={{ position: "absolute", left: 226, right: 30, top: 244, height: 150, display: "flex", alignItems: "center", opacity: Math.min(1, k * 1.4), transform: `translateX(${(1 - k) * 40}px)` }}>
      <div style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 0.93, color: "#fff", letterSpacing: 1 }}>{a}</div></div>
    <div style={{ position: "absolute", left: 226, top: 408, opacity: Math.min(1, k2 * 1.5), transform: `scale(${0.85 + 0.15 * k2})`, transformOrigin: "0 50%" }}>
      <span style={{ display: "inline-block", fontFamily: BEBAS, fontSize: 70, lineHeight: 1, color: "#fff", background: CU, borderRadius: 12, padding: "12px 24px 2px", whiteSpace: "nowrap" }}>{dm(sub)}</span></div></>); };
const Fig: React.FC<{ children: React.ReactNode; y?: number }> = ({ children, y = 520 }) => <div style={{ position: "absolute", left: 20, top: y, width: FW, height: FH }}>{children}</div>;

const Portada: React.FC = () => { const f = useCurrentFrame(); const X = [C, C + DD / 2, C + DD];
  return (<Base first>
    <div style={{ position: "absolute", left: 30, right: 30, top: 232, textAlign: "center", fontFamily: BEBAS, fontSize: 104, lineHeight: 0.95, color: "#fff", letterSpacing: 1 }}>¿DÓNDE REVISAS EL CORTANTE<br />DE TU ZAPATA?</div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 446, textAlign: "center" }}><span style={{ display: "inline-block", fontFamily: BEBAS, fontSize: 84, lineHeight: 1, color: "#fff", background: CU, borderRadius: 12, padding: "12px 30px 2px" }}>{dm("CARA · d · d/2")}</span></div>
    <Fig y={540}><Zap>
      {X.map((x, i) => { const on = 0.55 + 0.45 * Math.sin(f / 6 + i * 2.1); const q = S([x, [-L - 36, 0, L + 36][i], H + 124]);
        return (<g key={i}><Plano x={x} dash op={0.55 + 0.45 * on} /><Txt at={[q[0] + 6, q[1] - 22 - 8 * Math.sin(f / 7 + i)]} text="?" size={92} color="#fff" bebas /></g>); })}
    </Zap></Fig>
  </Base>); };

// 1 · flexión en la cara de la columna: el voladizo se enciende y se flexiona
const Flexion: React.FC = () => { const t = tt(); const f = useCurrentFrame(); const a = kk(t, 0.35, 0.45), b = kk(t, 0.9, 0.4); const dz = b * (10 + 7 * Math.sin(f / 4));
  const cara = S([C, L + 36, H + 124]);
  return (<Base><Cab n="1" a="FLEXIÓN" sub="EN LA CARA DE LA COLUMNA" size={170} />
    <Fig><Zap>
      {b > 0 && <g opacity={b}>
        <polygon points={pts([[C, -L, H], [L, -L, H + dz], [L, L, H + dz], [C, L, H]])} fill={OR} fillOpacity={0.55} stroke="#FFE3BF" strokeWidth={4} strokeLinejoin="round" />
        <polygon points={pts([[L, -L, dz], [L, L, dz], [L, L, H + dz], [L, -L, H + dz]])} fill={CU} fillOpacity={0.6} stroke="#FFE3BF" strokeWidth={4} strokeLinejoin="round" />
        <polygon points={pts([[C, L, 0], [L, L, dz], [L, L, H + dz], [C, L, H]])} fill="#B8681F" fillOpacity={0.6} stroke="#FFE3BF" strokeWidth={4} strokeLinejoin="round" /></g>}
      <Plano x={C} k={a} op={Math.min(1, a * 2)} />
      {a > 0.7 && <Txt at={[cara[0] - 10, cara[1] - 20]} text="CARA" size={64} bebas color="#fff" op={kk(t, 0.7, 0.2)} />}
    </Zap></Fig></Base>); };

// 2 · cortante en una dirección: el plano se desliza una distancia d; d también es la altura hasta el acero
const Cortante: React.FC = () => { const t = tt(); const s0 = Math.max(0.9, w(2, /^distancia/i, 0.4) - 0.5); const s = kk(t, s0, 0.8, Easing.inOut(Easing.cubic)); const c1 = kk(t, s0 + 0.7, 0.35), c2 = kk(t, Math.max(s0 + 1.4, w(2, /^peralte/i, 0.75) - 0.7), 0.4);
  const x = C + DD * s;
  return (<Base><Cab n="2" a={<>CORTANTE EN<br />UNA DIRECCIÓN</>} sub="A d DE LA CARA" size={96} />
    <Fig><Zap>
      <Plano x={C} dash op={0.5} /><Plano x={x} op={1} />
      <polyline points={pts([[C, L + 4, H], [C, L + 70, H]])} stroke="#FFE3BF" strokeWidth={3} opacity={c1} /><polyline points={pts([[C + DD, L + 4, H], [C + DD, L + 70, H]])} stroke="#FFE3BF" strokeWidth={3} opacity={c1} />
      <Cota a={[C, L + 56, H]} b={[C + DD, L + 56, H]} k={c1} label="d" off={[-34, 46]} size={84} />
      <polyline points={pts([[L, L, ZS], [L + 70, L, ZS]])} stroke="#FFE3BF" strokeWidth={3} opacity={c2} /><polyline points={pts([[L, L, H], [L + 70, L, H]])} stroke="#FFE3BF" strokeWidth={3} opacity={c2} />
      <Cota a={[L + 56, L, H]} b={[L + 56, L, ZS]} k={c2} label="d" off={[40, 26]} size={84} />
    </Zap></Fig></Base>); };

// 3 · punzonamiento: perímetro a d/2 de cada cara; la columna «atraviesa»
const Punzo: React.FC = () => { const t = tt(); const f = useCurrentFrame(); const a = kk(t, 0.45, 0.6, Easing.inOut(Easing.quad)); const g = Math.max(1.3, w(3, /^perímetro/i, 0.4) + 0.2); const dn = kk(t, g, 0.25, Easing.out(Easing.back(3))); const R = C + DD / 2;
  const per: P3[] = [[R, -R, H], [R, R, H], [-R, R, H], [-R, -R, H]]; const c = kk(t, g + 0.3, 0.35);
  return (<Base><Cab n="3" a="PUNZONAMIENTO" sub="A d/2, TODO ALREDEDOR" size={128} />
    <Fig><Zap colDz={-18 * dn}>
      <polygon points={pts(per)} fill={OR} fillOpacity={0.38 * a + 0.12 * a * Math.sin(f / 5)} stroke={OR} strokeWidth={8} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - a} />
      <g dangerouslySetInnerHTML={{ __html: `<g transform="${mv([0, 0, -18 * dn])}">${COLUMNA}</g>` }} />
      <Cota a={[C, R + 26, H]} b={[R, R + 26, H]} k={c} label="d/2" off={[-64, 58]} size={72} />
    </Zap></Fig></Base>); };

// 4 · recubrimiento contra el suelo: el hormigón se levanta y queda la parrilla sobre el suelo
const Recub: React.FC = () => { const t = tt(); const up = kk(t, 0.3, 0.7); const c = kk(t, Math.max(1.2, w(4, /^setenta/i, 0.45) - 0.3), 0.35); const q = S([L + 30, L - 24, ZS / 2]);
  return (<Base><Cab n="4" a={<>RECUBRIMIENTO<br />CONTRA EL SUELO</>} sub="75 mm" size={96} />
    <Fig><Zap lift={LIFT * up} hop={0.66 + 0.2 * up}>
      <Cota a={[L - 24, L + 30, 0]} b={[L - 24, L + 30, ZS - 6]} k={c} />
      {c > 0 && <g opacity={c}><line x1={q[0] - 150} y1={q[1] + 40} x2={q[0] - 250} y2={q[1] + 96} stroke="#FFE3BF" strokeWidth={4} /><Txt at={[q[0] - 256, q[1] + 150]} text="75 mm" size={96} /></g>}
    </Zap></Fig></Base>); };

// 5 · peralte efectivo mínimo: se vuelve a armar; d desde la cara superior hasta el acero
const Peralte: React.FC = () => { const t = tt(); const dn = 1 - kk(t, 0.2, 0.6); const c = kk(t, Math.max(1.0, w(5, /^mínimo/i, 0.35) - 0.2), 0.4);
  return (<Base><Cab n="5" a={<>PERALTE EFECTIVO<br />MÍNIMO</>} sub="d ≥ 150 mm" size={96} />
    <Fig><Zap lift={LIFT * dn} hop={0.86 - 0.2 * (1 - dn)}>
      <polyline points={pts([[L, L, ZS], [L + 70, L, ZS]])} stroke="#FFE3BF" strokeWidth={3} opacity={c} /><polyline points={pts([[L, L, H], [L + 70, L, H]])} stroke="#FFE3BF" strokeWidth={3} opacity={c} />
      <Cota a={[L + 56, L, H]} b={[L + 56, L, ZS]} k={c} />
      {c > 0.5 && (() => { const q = S([L + 56, L, (H + ZS) / 2]); return <g opacity={kk(t, 1.2, 0.3)}><Txt at={[q[0] + 26, q[1] + 96]} text="d ≥ 150 mm" size={78} anchor="middle" /></g>; })()}
    </Zap></Fig></Base>); };

// 6 · lámina resumen (cabe en 4:5) y llamada: las cinco medidas a la vez
const CHIPS: [string, string, string][] = [["1", "CARA", "FLEXIÓN"], ["2", "d", "CORTANTE"], ["3", "d/2", "PUNZONAMIENTO"], ["4", "75 mm", "RECUBRIMIENTO"], ["5", "150 mm", "PERALTE MÍNIMO"]];
const Resumen: React.FC = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); const R = C + DD / 2; const b = Math.round(Math.max(1.2, w(6, /^Comenta/i, 0.3) - 0.2) * FPS);
  const kb = spring({ frame: f - b, fps, config: { damping: 10 } }); const pulse = 1 + 0.03 * Math.sin(f / 5);
  return (<Base>
    <div style={{ position: "absolute", left: 20, right: 20, top: 292, textAlign: "center", fontFamily: BEBAS, fontSize: 112, lineHeight: 1, color: "#fff", letterSpacing: 1 }}>¿CUÁL SE TE PASA MÁS?</div>
    <div style={{ position: "absolute", left: 174, top: 400, width: FW, height: FH, transform: "scale(0.7)", transformOrigin: "0 0" }}><Zap>
      <polygon points={pts([[R, -R, H], [R, R, H], [-R, R, H], [-R, -R, H]])} fill={OR} fillOpacity={0.3} stroke={OR} strokeWidth={8} strokeLinejoin="round" />
      <g dangerouslySetInnerHTML={{ __html: COLUMNA }} />
      <polyline points={pts([[C, -L, H], [C, L, H], [C, L, 0]])} fill="none" stroke="#fff" strokeWidth={6} strokeDasharray="14 10" />
      <polyline points={pts([[C + DD, -L, H], [C + DD, L, H], [C + DD, L, 0]])} fill="none" stroke={OR} strokeWidth={6} />
      <Cota a={[L + 56, L, H]} b={[L + 56, L, ZS]} k={1} /><Cota a={[L - 24, L + 30, 0]} b={[L - 24, L + 30, ZS - 6]} k={1} />
      {([[S([C, -L, H]), "1", [0, -34]], [S([C + DD, -L, H]), "2", [44, -10]], [S([R, R, H]), "3", [-8, 44]], [S([L - 24, L + 30, 0]), "4", [-50, 30]], [S([L + 56, L, (H + ZS) / 2]), "5", [52, 10]]] as [[number, number], string, [number, number]][]).map(([q, n, o], i) => {
        const s = spring({ frame: f - 8 - i * 5, fps, config: { damping: 11 } }); return <g key={n} transform={`translate(${q[0] + o[0]} ${q[1] + o[1]}) scale(${s})`}><Bola at={[0, 0]} n={n} r={40} /></g>; })}
    </Zap></div>
    <div style={{ position: "absolute", left: 22, right: 22, top: 968, display: "flex", gap: 8, justifyContent: "center" }}>
      {CHIPS.map(([n, v, name], i) => { const s = spring({ frame: f - 10 - i * 5, fps, config: { damping: 13 } });
        return (<div key={n} style={{ width: 200, background: "#fff", borderRadius: 18, padding: "10px 6px 10px", textAlign: "center", borderBottom: `9px solid ${OR}`, opacity: Math.min(1, s * 1.5), transform: `translateY(${(1 - s) * 30}px)`, boxShadow: "0 14px 30px rgba(0,0,0,.4)" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}><span style={{ fontFamily: BEBAS, fontSize: 60, lineHeight: 0.9, color: OR, paddingTop: 6 }}>{n}</span>
            <span style={{ fontFamily: MONT, fontWeight: 900, fontSize: v.length > 5 ? 34 : 42, color: "#0F1E33", whiteSpace: "nowrap" }}>{v}</span></div>
          <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 17.5, letterSpacing: 0.3, color: "#5A6475", marginTop: 4 }}>{name}</div></div>); })}
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 1108, textAlign: "center", fontFamily: MONT, fontWeight: 900, fontSize: 36, letterSpacing: 4, color: "#fff" }}><span style={{ color: "#F2B777" }}>ACI 318-19</span> · DINOS EL NÚMERO</div>
    <div style={{ position: "absolute", left: 40, right: 40, top: 1172, display: "flex", justifyContent: "center", transform: `scale(${(0.8 + 0.2 * kb) * pulse})`, opacity: Math.min(1, kb * 1.5) }}>
      <div style={{ background: OR, borderRadius: 999, padding: "30px 50px 18px", fontFamily: BEBAS, fontSize: 108, lineHeight: 1, color: "#fff", border: "5px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.45)", letterSpacing: 2, whiteSpace: "nowrap" }}>COMENTA «ZAPATA»</div></div>
  </Base>); };

export const Medidas: React.FC = () => (<AbsoluteFill style={{ background: NAVY }}>
  <Escenas T={T}>{[<Portada />, <Flexion />, <Cortante />, <Punzo />, <Recub />, <Peralte />, <Resumen />]}</Escenas>
  <Subs T={T} />
</AbsoluteFill>);
