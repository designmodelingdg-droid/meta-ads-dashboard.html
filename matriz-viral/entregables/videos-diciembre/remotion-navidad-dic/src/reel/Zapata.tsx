// «Tu zapata se levanta de un lado (y la calculaste con P/A)» · pizarra dibujada.
// Datos del guion (ejemplo): zapata 1,80 × 1,80 m, P = 40 t → 1,23 kg/cm²; e = 0,30 m = L/6 → 2,47 y 0; e = 0,45 m → 3,29 kg/cm², apoya en 1,35 m.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import T0 from "../../reels/zapata.json";
import { Tiempos, Subs, Hoja, Cierre, Escenas } from "./base";
import { Tr, Ln, Caja, Poli, Circ, Equis, Visto, Flecha, Cota, Rayado, Svg, Tx, Sello, INK, GREY, RED, COPPER, SOIL, CON, CON_D, hand, Pt } from "./pz";
export const T = T0 as Tiempos;
const X0 = 270, X1 = 810, YT = 860, YB = 960, BASE = 975, CX = 540;   // 300 px por metro; 60 px por kg/cm²

// zapata en corte con su columna; rot = giro (grados) alrededor del borde derecho de la base
const Corte: React.FC<{ t0: number; rot?: number }> = ({ t0, rot = 0 }) => (<>
  <Ln a={[130, YB]} b={[X0, YB]} t0={t0} seed={11} w={5} /><Ln a={[X1, YB]} b={[950, YB]} t0={t0 + 0.1} seed={12} w={5} />
  <Rayado x0={150} x1={X0 - 6} y={YB + 4} t0={t0 + 0.2} /><Rayado x0={X1 + 24} x1={950} y={YB + 4} t0={t0 + 0.3} />
  <g transform={`rotate(${rot} ${X1} ${YB})`}>
    <Caja x={CX - 60} y={600} w={120} h={YT - 600} t0={t0 + 0.25} fill={CON_D} seed={5} />
    <Caja x={X0} y={YT} w={X1 - X0} h={YB - YT} t0={t0 + 0.5} fill={CON} seed={6} dur={0.45} />
  </g></>);
const Carga: React.FC<{ x: number; t0: number; y0?: number }> = ({ x, t0, y0 = 440 }) => <Flecha a={[x, y0]} b={[x, 590]} t0={t0} color={COPPER} w={10} head={30} />;
// bloque de presiones bajo la base: de xa (altura ha) a xb (altura hb), con flechas hacia arriba
const Presion: React.FC<{ xa: number; xb: number; ha: number; hb: number; t0: number; color?: string }> = ({ xa, xb, ha, hb, t0, color = COPPER }) => {
  const pts: Pt[] = [[xa, BASE], [xb, BASE], [xb, BASE + hb], [xa, BASE + ha]]; const n = 6;
  return (<><Poli pts={pts} t0={t0 + 0.25} fill={SOIL} op={0.7} /><Tr d={hand([...pts, pts[0]], 31, 1.5)} t0={t0} dur={0.5} color={color} w={5} />
    {Array.from({ length: n }).map((_, i) => { const f = (i + 0.5) / n; const x = xa + (xb - xa) * f; const h = ha + (hb - ha) * f; if (h < 26) return null;
      return <Flecha key={i} a={[x, BASE + h - 6]} b={[x, BASE + 8]} t0={t0 + 0.5 + i * 0.05} color={color} w={4} head={12} dur={0.12} />; })}</>);
};
const Titulo: React.FC<{ a: string; t0?: number; size?: number; y?: number }> = ({ a, t0 = 0.25, size = 116, y = 262 }) => <Tx text={a} x={540} y={y} t0={t0} size={size} font="h" align="center" />;
const Flechita: React.FC<{ c?: string }> = ({ c = INK }) => <svg width={62} height={40} viewBox="0 0 62 40" style={{ margin: "0 14px", verticalAlign: "baseline" }}><path d="M4 22 H50 M36 8 L52 22 L36 36" stroke={c} strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>;

const Portada: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const rot = -2.4 - 0.5 * Math.sin(f / 9); const pulso = 0.55 + 0.45 * Math.abs(Math.sin(f / 7));
  return (<Hoja first>
    <Tx text="ESTA ZAPATA SE ESTÁ" x={540} y={250} t0={-1} size={112} font="h" align="center" />
    <Tx text="LEVANTANDO DE UN LADO" x={540} y={356} t0={-1} size={112} font="h" align="center" />
    <Tx text="Y TU HOJA DICE QUE CUMPLE" x={540} y={476} t0={-1} size={78} font="h" color="#fff" bg={COPPER} align="center" />
    <Svg><g transform="translate(0,190)">
      <Corte t0={-1} rot={rot} /><Carga x={CX + 135} t0={-1} y0={470 + 6 * Math.sin(f / 6)} />
      <Presion xa={405} xb={X1} ha={0} hb={197} t0={-1} color={RED} />
      <polygon points={`${X0},${YB - 23} 405,${YB - 15} 405,${BASE - 2} ${X0},${BASE - 2}`} fill={RED} opacity={0.25 + 0.35 * pulso} />
      <Circ cx={338} cy={952} rx={104} ry={56} t0={d * 0.45} seed={7} w={9} />
    </g></Svg>
    <Tx text="SE LEVANTA" x={60} y={1215} t0={d * 0.5} size={64} font="h" color={RED} />
  </Hoja>); };

const Centro: React.FC<{ d: number }> = ({ d }) => (<Hoja n="1 DE 3">
  <Titulo a="CARGA AL CENTRO" />
  <Svg><Corte t0={0.35} /><Carga x={CX} t0={1.2} />
    <Presion xa={X0} xb={X1} ha={74} hb={74} t0={d * 0.3} />
    <Cota a={[X0, 1088]} b={[X1, 1088]} t0={d * 0.4} /></Svg>
  <Tx text="P = 40 t" x={CX + 30} y={456} t0={1.45} size={46} font="f" color={COPPER} />
  <Tx text="(ejemplo)" x={CX + 32} y={516} t0={1.6} size={28} color={GREY} />
  <Tx text="1,80 m" x={540} y={1094} t0={d * 0.42} size={34} color={GREY} align="center" />
  <Tx text="P / A = 1,23 kg/cm²" x={540} y={1156} t0={d * 0.5} size={82} font="f" align="center" />
  <div style={{ position: "absolute", left: 0, right: 0, top: 1266, textAlign: "center" }}><Tx text={<>ADMISIBLE 2,0<Flechita c={COPPER} />CUMPLE</>} x={540} y={0} t0={d * 0.8} size={72} font="h" color={COPPER} align="center" len={20} /></div>
  <Svg><Visto cx={905} cy={1300} r={34} t0={d * 0.86} /></Svg>
</Hoja>);

const Momento: React.FC<{ d: number }> = ({ d }) => (<Hoja n="2 DE 3">
  <Titulo a="CARGA + MOMENTO" />
  <Svg><Corte t0={0.3} />
    <Tr d="M 432,800 C 362,770 362,690 432,652" t0={d * 0.12} dur={0.35} color={RED} w={9} /><Tr d="M 406,640 L 434,651 L 420,680" t0={d * 0.12 + 0.3} dur={0.1} color={RED} w={9} />
    <Ln a={[CX, 450]} b={[CX, 596]} t0={d * 0.2} color={GREY} w={3} dash="10 10" />
    <Carga x={CX + 90} t0={d * 0.26} y0={470} /><Cota a={[CX, 440]} b={[CX + 90, 440]} t0={d * 0.3} color={RED} tick={10} />
    <Presion xa={X0} xb={X1} ha={0} hb={148} t0={d * 0.52} color={RED} />
    <Equis cx={300} cy={1318} r={26} t0={d * 0.86} /></Svg>
  <Tx text="M" x={318} y={690} t0={d * 0.14} size={64} font="h" color={RED} />
  <Tx text="e = 0,30 m" x={CX + 112} y={412} t0={d * 0.32} size={40} font="f" color={RED} />
  <Tx text="0" x={236} y={972} t0={d * 0.74} size={62} font="h" color={RED} />
  <Tx text="2,47 kg/cm²" x={818} y={1128} t0={d * 0.64} size={62} font="h" color={RED} align="right" w={420} />
  <Tx text="e = M / P = 0,30 m = L/6" x={540} y={1200} t0={d * 0.34} size={64} font="f" align="center" />
  <Tx text="NO CUMPLE" x={346} y={1284} t0={d * 0.88} size={76} font="h" color={RED} />
  <Tx text="2,47 > 2,0 admisible" x={640} y={1304} t0={d * 0.9} size={32} color={GREY} />
</Hoja>);

const Despega: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const pulso = 0.5 + 0.5 * Math.abs(Math.sin(f / 7));
  return (<Hoja n="3 DE 3">
    <Titulo a="UN POCO MÁS DE MOMENTO" size={96} y={270} />
    <Svg><Corte t0={0.3} rot={-2.4} />
      <Ln a={[CX, 450]} b={[CX, 596]} t0={0.9} color={GREY} w={3} dash="10 10" /><Carga x={CX + 135} t0={1.0} y0={470} />
      <Cota a={[CX, 440]} b={[CX + 135, 440]} t0={1.2} color={RED} tick={10} />
      <Presion xa={405} xb={X1} ha={0} hb={197} t0={d * 0.3} color={RED} />
      {f / 30 > d * 0.22 && <polygon points={`${X0},${YB - 23} 405,${YB - 15} 405,${BASE - 2} ${X0},${BASE - 2}`} fill={RED} opacity={0.2 + 0.4 * pulso} />}
      <Tr d={"M" + [0, 1, 2, 3, 4, 5].map((i) => `${X0 + 8 + i * 24},${BASE - 4} L${X0 + 26 + i * 24},${YB - 18}`).join(" M")} t0={d * 0.22} dur={0.4} color={RED} w={4} />
      <Cota a={[X0, 1010]} b={[405, 1010]} t0={d * 0.26} color={RED} tick={10} /></Svg>
    <Tx text="e = 0,45 m" x={CX + 156} y={412} t0={1.3} size={40} font="f" color={RED} />
    <Tx text="0,45 m" x={338} y={1020} t0={d * 0.28} size={44} font="h" color={RED} align="center" w={200} />
    <Tx text="EN EL AIRE" x={338} y={1066} t0={d * 0.3} size={30} color={RED} align="center" w={240} />
    <Tx text="3,29 kg/cm²" x={818} y={1178} t0={d * 0.52} size={70} font="h" color={RED} align="right" w={460} />
    <Sello text="SE DESPEGA" x={290} y={560} t0={d * 0.4} size={84} rot={-8} w={600} />
    <Tx text="e = 0,45 m > L/6" x={60} y={1206} t0={d * 0.2} size={52} font="f" />
    <Tx text="APOYA EN 1,35 m DE 1,80" x={540} y={1290} t0={d * 0.72} size={76} font="h" color="#fff" bg={RED} align="center" />
  </Hoja>); };

const Regla: React.FC<{ d: number }> = ({ d }) => (<Hoja>
  <Titulo a="LA REGLA" size={128} y={250} />
  <Svg>
    <Caja x={320} y={470} w={440} h={440} t0={0.4} fill={CON} seed={8} dur={0.5} />
    <Poli pts={[[466.7, 470], [613.3, 470], [613.3, 910], [466.7, 910]]} t0={1.1} fill={COPPER} op={0.45} />
    <Ln a={[466.7, 470]} b={[466.7, 910]} t0={1.0} color={COPPER} w={5} dash="14 10" /><Ln a={[613.3, 470]} b={[613.3, 910]} t0={1.05} color={COPPER} w={5} dash="14 10" />
    <Caja x={490} y={640} w={100} h={100} t0={0.8} color={GREY} sw={4} seed={9} />
    <Cota a={[466.7, 438]} b={[613.3, 438]} t0={1.3} color={COPPER} tick={10} /><Cota a={[320, 944]} b={[760, 944]} t0={0.9} />
    <circle cx={585} cy={690} r={interpolateR(d)} fill={RED} /><Circ cx={585} cy={690} rx={38} ry={34} t0={d * 0.42} w={6} />
  </Svg>
  <Tx text="L/3" x={540} y={382} t0={1.35} size={50} font="h" color={COPPER} align="center" w={200} />
  <Tx text="L" x={540} y={952} t0={0.95} size={50} font="h" color={GREY} align="center" w={100} />
  <Tx text="RESULTANTE" x={640} y={668} t0={d * 0.45} size={30} color={RED} />
  <Tx text="e = M / P" x={540} y={1036} t0={d * 0.25} size={100} font="f" align="center" />
  <Tx text={<><span style={{ fontFamily: "MontLocal, DejaVu Sans", fontWeight: 900, fontSize: "0.8em" }}>e ≤ L / 6</span><Flechita c={COPPER} /><span style={{ color: COPPER }}>APOYA COMPLETA</span></>} x={540} y={1262} t0={d * 0.55} size={78} font="h" align="center" len={24} />
  <Tx text="si pasa de L/6, no apoya completa" x={540} y={1180} t0={d * 0.62} size={34} color={GREY} align="center" />
</Hoja>);
function interpolateR(_d: number) { return 13; }

export const Zapata: React.FC = () => { const E = T.escenas;
  return (<AbsoluteFill style={{ background: INK }}>
    <Escenas T={T}>{[
      <Portada d={E[0].dur + E[0].s} />, <Centro d={E[1].dur} />, <Momento d={E[2].dur} />, <Despega d={E[3].dur} />, <Regla d={E[4].dur} />,
      <Cierre titulo={<>¿CÓMO<br />DIMENSIONAS TÚ?</>} opciones={[["1", "SOLO CON LA CARGA"], ["2", "CON CARGA Y MOMENTO"]]} pie="DINOS EL NÚMERO" boton="COMENTA «ZAPATA»" />,
    ]}</Escenas>
    <Subs T={T} />
  </AbsoluteFill>); };
