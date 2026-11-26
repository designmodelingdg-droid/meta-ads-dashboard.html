// «1,4D + 1,7L: ¿de qué norma es?» · pizarra dibujada. Cifras literales del guion; nunca se dice que 1,4/1,7 esté mal u obsoleta: el error es mezclar.
// E.060 (Perú) 1,4 CM + 1,7 CV · NEC-SE-CG (Ecuador) 1,2 D + 1,6 L · ACI 318-19 1,2 D + 1,6 L · el ACI usó 1,4 y 1,7 hasta 1999 · cortante φ 0,85 / 0,75 · +13 %.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import T0 from "../../reels/combos.json";
import { MONT } from "../brand";
import { Tiempos, Subs, Hoja, Cierre, Escenas, cuando } from "./base";
import { Tr, Ln, Caja, Circ, Equis, Visto, Flecha, Svg, Tx, Sello, INK, GREY, RED, COPPER, BLUE, hand, p, useT, Pt } from "./pz";
export const T = T0 as Tiempos;
const w = (i: number, re: RegExp, fb: number) => cuando(T, i, re, fb);
const PHI = <span style={{ fontFamily: `${MONT}, "DejaVu Sans"`, fontWeight: 900 }}>φ</span>;
// renglones de texto simulado (garabato gris) de una hoja de memoria
const Renglones: React.FC<{ x: number; y: number; w: number; n: number; t0: number; gap?: number }> = ({ x, y, w: lw, n, t0, gap = 34 }) => (<>
  {Array.from({ length: n }).map((_, i) => <Ln key={i} a={[x, y + i * gap]} b={[x + lw * (i === n - 1 ? 0.55 : 1 - ((i * 7) % 3) * 0.08), y + i * gap]} t0={t0 <= 0 ? t0 : t0 + i * 0.06} color="#C9D2DD" w={9} seed={80 + i} dur={0.15} />)}</>);

const Portada: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const k = 1 + 0.025 * Math.sin(f / 5);
  return (<Hoja first>
    <div style={{ position: "absolute", left: 60, top: 246, width: 960, height: 760, background: "#fff", borderRadius: 10, boxShadow: "0 22px 50px rgba(13,30,58,.22)", transform: `rotate(${-1.6 + 0.3 * Math.sin(f / 13)}deg)` }}>
      <div style={{ position: "absolute", left: 40, top: 34, fontFamily: MONT, fontWeight: 800, fontSize: 30, letterSpacing: 4, color: GREY }}>MEMORIA DE CÁLCULO</div>
      <div style={{ position: "absolute", left: 40, top: 92, fontFamily: MONT, fontWeight: 900, fontSize: 52, color: INK, border: `5px solid ${INK}`, borderRadius: 10, padding: "8px 24px" }}>NORMA: ACI 318-19</div>
      <svg width={960} height={760} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        <Renglones x={44} y={236} w={860} n={3} t0={-1} /><Renglones x={44} y={610} w={860} n={4} t0={-1} />
        <g transform={`translate(480 450) scale(${k}) translate(-480 -450)`}><Circ cx={480} cy={452} rx={452} ry={112} t0={-1} seed={5} w={11} /></g>
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 366, textAlign: "center", fontFamily: MONT, fontWeight: 900, fontSize: 138, letterSpacing: -3, color: INK, lineHeight: 1.1, transform: `scale(${k})` }}>1,4D + 1,7L</div>
    </div>
    <Tx text="¿DE QUÉ NORMA ES?" x={540} y={1074} t0={-1} size={132} font="h" color="#fff" bg={COPPER} align="center" />
    <Svg><Flecha a={[540, 1052]} b={[540, 1000]} t0={d * 0.55} color={COPPER} w={9} head={26} /></Svg>
  </Hoja>); };

const Fila: React.FC<{ y: number; a: string; b: string; c: string; t0: number; col: string; seed: number }> = ({ y, a, b, c, t0, col, seed }) => (<>
  <Svg><Caja x={50} y={y} w={980} h={150} t0={t0} seed={seed} dur={0.35} fill="#fff" sw={5} /><Ln a={[450, y + 6]} b={[450, y + 144]} t0={t0 + 0.2} w={4} seed={seed + 1} />
    <Flecha a={[400, y + 75]} b={[500, y + 75]} t0={t0 + 0.3} color={col} w={7} head={20} dur={0.14} /></Svg>
  <Tx text={a} x={76} y={y + 22} t0={t0 + 0.1} size={70} font="h" /><Tx text={b} x={78} y={y + 96} t0={t0 + 0.2} size={30} color={GREY} />
  <Tx text={c} x={526} y={y + 42} t0={t0 + 0.35} size={60} font="f" color={col} /></>);
const Tabla: React.FC<{ d: number }> = ({ d }) => { const nota = w(1, /^fue$/i, 0.22) - 0.1, ec = w(1, /^Ecuador/i, 0.42) - 0.15, hoy = w(1, /^hoy/i, 0.6) - 0.5;
  return (<Hoja>
    <Tx text="NORMA" x={76} y={262} t0={0.15} size={64} font="h" color={GREY} /><Tx text="COMBINACIÓN" x={526} y={262} t0={0.25} size={64} font="h" color={GREY} />
    <Fila y={346} a="E.060" b="PERÚ" c="1,4 CM + 1,7 CV" t0={0.3} col={COPPER} seed={31} />
    <Svg><Tr d="M 880,500 C 930,530 930,580 880,610" t0={nota} dur={0.25} color={RED} w={6} /><Tr d="M 904,596 L 878,611 L 900,632" t0={nota + 0.2} dur={0.1} color={RED} w={6} /></Svg>
    <Tx text="EL ACI USÓ 1,4 Y 1,7 HASTA 1999" x={500} y={562} t0={nota + 0.1} size={66} font="h" color={RED} align="center" w={900} rot={-1.5} />
    <Fila y={700} a="NEC-SE-CG" b="ECUADOR" c="1,2 D + 1,6 L" t0={ec} col={BLUE} seed={41} />
    <Fila y={880} a="ACI 318-19" b="HOY" c="1,2 D + 1,6 L" t0={Math.max(ec + 0.6, hoy)} col={BLUE} seed={51} />
    <Svg><Tr d="M 1040,720 C 1066,760 1066,980 1040,1012" t0={Math.max(ec + 1.2, hoy + 0.6)} dur={0.3} color={BLUE} w={6} /></Svg>
    <Tx text="1,2 Y 1,6" x={540} y={1090} t0={w(1, /^usan/i, 0.75)} size={150} font="h" color="#fff" bg={BLUE} align="center" />
  </Hoja>); };

const Par: React.FC<{ y: number; a: string; phi: string; t0: number; col: string; seed: number; h?: number; s?: number }> = ({ y, a, phi, t0, col, seed, h = 190, s = 1 }) => (<>
  <Svg><Caja x={56} y={y} w={400} h={h} t0={t0} seed={seed} color={col} sw={7} fill="#fff" /><Caja x={624} y={y} w={400} h={h} t0={t0 + 0.45} seed={seed + 2} color={col} sw={7} fill="#fff" />
    <Flecha a={[476, y + h / 2]} b={[604, y + h / 2]} t0={t0 + 0.3} color={col} w={8} head={22} dur={0.14} /><Flecha a={[604, y + h / 2]} b={[476, y + h / 2]} t0={t0 + 0.34} color={col} w={8} head={22} dur={0.05} /></Svg>
  <Tx text={a} x={256} y={y + h / 2 - 62 * s} t0={t0 + 0.1} size={124 * s} font="h" color={col} align="center" w={400} />
  {h > 150 && <Tx text="CORTANTE" x={824} y={y + 22} t0={t0 + 0.5} size={34} color={GREY} align="center" w={400} />}
  <Tx text={<>{PHI} = {phi}</>} x={824} y={y + (h > 150 ? 66 : h / 2 - 40)} t0={t0 + 0.6} size={h > 150 ? 84 : 70} font="f" color={col} align="center" w={400} len={9} /></>);
const Parejas: React.FC<{ d: number }> = ({ d }) => (<Hoja>
  <Tx text="CADA COMBINACIÓN" x={540} y={250} t0={0.2} size={112} font="h" align="center" />
  <Tx text={<>TRAE SU {PHI}</>} x={540} y={358} t0={0.5} size={128} font="h" color={COPPER} align="center" len={10} />
  <Par y={600} a="1,4 Y 1,7" phi="0,85" t0={w(2, /^primera/i, 0.25) - 0.35} col={COPPER} seed={61} />
  <Par y={900} a="1,2 Y 1,6" phi="0,75" t0={w(2, /^segunda/i, 0.6) - 0.5} col={BLUE} seed={71} />
</Hoja>);

const ErrorMezcla: React.FC<{ d: number }> = ({ d }) => { const t = useT(); const mz = w(3, /^mezclar/i, 0.06), red = w(3, /^reduces/i, 0.4), reg = w(3, /^regalas/i, 0.62), tr = w(3, /^trece/i, 0.68);
  const X0 = 90, W100 = 760, Y = 1010, H = 78; const k1 = p(t, reg - 0.9, 0.8, Easing.inOut(Easing.quad)), k2 = p(t, tr - 0.1, 0.5, Easing.out(Easing.back(1.5)));
  return (<Hoja>
    <Tx text="EL ERROR" x={70} y={240} t0={0.15} size={150} font="h" color={RED} />
    <Par y={430} a="1,4 Y 1,7" phi="0,85" t0={0.3} col={COPPER} seed={62} h={130} s={0.72} />
    <Par y={600} a="1,2 Y 1,6" phi="0,75" t0={0.5} col={BLUE} seed={72} h={130} s={0.72} />
    <Svg><Tr d={hand([[460, 664], [540, 580], [620, 496]], 9, 2)} t0={red - 0.2} dur={0.3} color={RED} w={12} /><Equis cx={540} cy={580} r={46} t0={red + 0.15} w={14} />
      <Tr d={`M${X0},${Y} L${X0 + W100 + 99},${Y} L${X0 + W100 + 99},${Y + H} L${X0},${Y + H} Z`} t0={reg - 1.1} dur={0.3} w={5} />
      {k1 > 0 && <rect x={X0 + 4} y={Y + 4} width={(W100 - 4) * k1} height={H - 8} fill={BLUE} opacity={0.85} />}
      {k2 > 0 && <g><rect x={X0 + W100} y={Y + 4} width={95 * Math.min(1, k2)} height={H - 8} fill={RED} opacity={0.3} />
        <path d={"M" + [0, 1, 2, 3].map((i) => `${X0 + W100 + 6 + i * 24},${Y + H - 6} L${X0 + W100 + 26 + i * 24},${Y + 6}`).join(" M")} stroke={RED} strokeWidth={5} strokeLinecap="round" opacity={Math.min(1, k2)} /></g>}
      <Ln a={[X0 + W100, Y - 14]} b={[X0 + W100, Y + H + 14]} t0={reg - 0.2} w={6} dur={0.1} />
    </Svg>
    <Sello text="MEZCLA" x={790} y={262} t0={mz + 0.25} size={96} rot={-8} w={460} />
    <Tx text={<>1,2 Y 1,6 CON {PHI} = 0,85</>} x={540} y={790} t0={red + 0.3} size={92} font="h" align="center" len={22} />
    <Tx text="RESISTENCIA" x={X0} y={Y - 50} t0={reg - 1.0} size={30} color={GREY} /><Tx text="100 %" x={X0 + W100 - 118} y={Y - 62} t0={reg - 0.2} size={48} font="h" color={BLUE} />
    <Tx text="+13 %" x={X0 + W100 - 30} y={Y + H + 8} t0={tr - 0.05} size={64} font="h" color={RED} />
    <Tx text="+13 % DE RESISTENCIA" x={60} y={1166} t0={tr + 0.1} size={104} font="h" color={RED} />
    <Tx text="QUE NO EXISTE" x={60} y={1268} t0={w(3, /^que$/i, 0.86)} size={104} font="h" />
  </Hoja>); };

const Revisor: React.FC<{ d: number }> = ({ d }) => { const a = w(4, /^norma/i, 0.2), b = w(4, /^combinación/i, 0.3), c = w(4, /^factor/i, 0.42), m = w(4, /^mismo/i, 0.55), s = w(4, /^Si$/, 0.72);
  return (<Hoja>
    <Tx text="LO QUE CRUZA" x={540} y={250} t0={0.15} size={112} font="h" align="center" /><Tx text="EL REVISOR" x={540} y={356} t0={0.4} size={128} font="h" color={COPPER} align="center" />
    <Svg><Caja x={70} y={540} w={940} h={520} t0={0.4} fill="#fff" seed={15} dur={0.45} sw={5} />
      <Renglones x={110} y={596} w={840} n={3} t0={0.7} />
      <Tr d="M 96,726 L 986,726 L 986,850 L 96,850 Z" t0={a - 0.2} dur={0.3} color={COPPER} w={5} fill={COPPER} fo={0.22} />
      <Ln a={[330, 790]} b={[380, 790]} t0={b - 0.1} color={COPPER} w={7} dur={0.1} /><Ln a={[786, 790]} b={[836, 790]} t0={c - 0.1} color={COPPER} w={7} dur={0.1} />
      <Renglones x={110} y={908} w={840} n={4} t0={0.9} />
      <Visto cx={930} cy={690} r={44} t0={m + 0.3} w={14} />
      <Tr d="M 800,1240 C 900,1240 930,1310 860,1330 L 760,1330" t0={s + 0.3} dur={0.3} color={RED} w={8} /><Tr d="M 790,1306 L 758,1330 L 792,1352" t0={s + 0.55} dur={0.1} color={RED} w={8} />
    </Svg>
    <Tx text="NORMA" x={212} y={748} t0={a} size={84} font="h" align="center" w={240} /><Tx text="COMBINACIÓN" x={583} y={748} t0={b} size={84} font="h" align="center" w={400} />
    <Tx text={PHI} x={900} y={734} t0={c} size={92} font="f" align="center" w={120} len={2} />
    <Tx text="DEL MISMO DOCUMENTO" x={540} y={1104} t0={m - 0.1} size={104} font="h" color="#fff" bg={INK} align="center" />
    <Tx text="si no, te la devuelve" x={250} y={1290} t0={s} size={44} color={RED} />
  </Hoja>); };

export const Combos: React.FC = () => { const E = T.escenas;
  return (<AbsoluteFill style={{ background: INK }}>
    <Escenas T={T}>{[
      <Portada d={E[0].dur + E[0].s} />, <Tabla d={E[1].dur} />, <Parejas d={E[2].dur} />, <ErrorMezcla d={E[3].dur} />, <Revisor d={E[4].dur} />,
      <Cierre titulo={<>¿CON CUÁL<br />DISEÑAS TÚ?</>} opciones={[["1", "1,4 Y 1,7"], ["2", "1,2 Y 1,6"]]} pie="DINOS EL NÚMERO Y TU PAÍS" boton="COMENTA «MEMORIA»" />,
    ]}</Escenas>
    <Subs T={T} />
  </AbsoluteFill>); };
