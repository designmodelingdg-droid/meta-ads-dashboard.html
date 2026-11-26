// «Revit tiene 3 orígenes» · pizarra dibujada. El cuadro «Vincular Revit» va como ESQUEMA dibujado (no hay captura real en el banco); no se escriben los nombres de las opciones.
// Datos del guion: origen interno (nunca se mueve, modelo a menos de 16 km), punto base del proyecto (referencia local), punto de reconocimiento (coordenadas reales).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import T0 from "../../reels/origenes.json";
import { BEBAS } from "../brand";
import { Tiempos, Subs, Hoja, Cierre, Escenas, cuando } from "./base";
import { Tr, Ln, Caja, Circ, Equis, Flecha, Cota, Svg, Tx, Sello, INK, GREY, RED, COPPER, CON, BLUE, hand, loop, p, useT, Pt } from "./pz";
export const T = T0 as Tiempos;
const w = (i: number, re: RegExp, fb: number) => cuando(T, i, re, fb);

// los tres símbolos, dibujados a mano
const Ejes: React.FC<{ x: number; y: number; s?: number; t0: number; c?: string; sw?: number }> = ({ x, y, s = 80, t0, c = INK, sw = 7 }) => (<g>
  <Flecha a={[x, y]} b={[x + s, y]} t0={t0} color={c} w={sw} head={s * 0.24} dur={0.14} /><Flecha a={[x, y]} b={[x, y - s]} t0={t0 + 0.12} color={c} w={sw} head={s * 0.24} dur={0.14} />
  <Flecha a={[x, y]} b={[x - s * 0.6, y + s * 0.52]} t0={t0 + 0.24} color={c} w={sw} head={s * 0.24} dur={0.14} /><Tr d={loop(x, y, sw * 0.9, sw * 0.9, 2)} t0={t0} dur={0.1} color={c} w={sw} fill={c} /></g>);
const PBase: React.FC<{ x: number; y: number; s?: number; t0: number; c?: string; sw?: number; dash?: string }> = ({ x, y, s = 56, t0, c = BLUE, sw = 7, dash }) => (<g>
  <Tr d={loop(x, y, s, s, 5)} t0={t0} dur={0.28} color={c} w={sw} dash={dash} /><Ln a={[x - s * 0.7, y - s * 0.7]} b={[x + s * 0.7, y + s * 0.7]} t0={t0 + 0.24} dur={0.1} color={c} w={sw} seed={21} dash={dash} />
  <Ln a={[x + s * 0.7, y - s * 0.7]} b={[x - s * 0.7, y + s * 0.7]} t0={t0 + 0.32} dur={0.1} color={c} w={sw} seed={22} dash={dash} /></g>);
const PRec: React.FC<{ x: number; y: number; s?: number; t0: number; c?: string; sw?: number }> = ({ x, y, s = 66, t0, c = COPPER, sw = 7 }) => (<g>
  <Tr d={hand([[x, y - s], [x + s * 0.92, y + s * 0.6], [x - s * 0.92, y + s * 0.6], [x, y - s]], 33, 1.6)} t0={t0} dur={0.3} color={c} w={sw} />
  <Ln a={[x - s * 0.24, y + s * 0.12]} b={[x + s * 0.24, y + s * 0.12]} t0={t0 + 0.28} dur={0.08} color={c} w={sw} seed={23} /><Ln a={[x, y - s * 0.12]} b={[x, y + s * 0.36]} t0={t0 + 0.34} dur={0.08} color={c} w={sw} seed={24} /></g>);
// edificio en planta: arquitectura (azul marino lleno) o estructura (contorno cobre rayado)
const Edif: React.FC<{ x: number; y: number; w: number; h: number; t0: number; est?: boolean }> = ({ x, y, w: bw, h, t0, est }) => (<g>
  <Caja x={x} y={y} w={bw} h={h} t0={t0} color={est ? COPPER : INK} fill={est ? COPPER : INK} fo={est ? 0.2 : 0.92} seed={est ? 14 : 13} dur={0.4} sw={est ? 8 : 6} />
  {est ? <Tr d={"M" + Array.from({ length: Math.floor((bw + h) / 44) }).map((_, i) => { const k = 30 + i * 44; return `${x + Math.min(k, bw)},${y + Math.max(0, k - bw)} L${x + Math.max(0, k - h)},${y + Math.min(k, h)}`; }).join(" M")} t0={t0 + 0.3} dur={0.4} color={COPPER} w={3} />
    : <Tr d={`M${x + bw / 3},${y + 8} L${x + bw / 3},${y + h - 8} M${x + (2 * bw) / 3},${y + 8} L${x + (2 * bw) / 3},${y + h - 8} M${x + 8},${y + h / 2} L${x + bw - 8},${y + h / 2}`} t0={t0 + 0.3} dur={0.4} color="#5E7396" w={3} />}</g>);
const TitN: React.FC<{ n: string; a: string; size?: number }> = ({ n, a, size = 92 }) => (<>
  <Tx text={n} x={64} y={226} t0={0.2} size={196} font="h" color={COPPER} /><Tx text={a} x={172} y={226 + (204 - size * 1.04) / 2 + 6} t0={0.3} size={size} font="h" /></>);
const Num: React.FC<{ x: number; y: number; n: string; r?: number; t0: number }> = ({ x, y, n, r = 30, t0 }) => { const t = useT(); const k = p(t, t0, 0.2, Easing.out(Easing.back(2))); if (k <= 0) return null;
  return (<g transform={`translate(${x} ${y}) scale(${k})`}><circle r={r} fill={COPPER} /><text y={r * 0.42} textAnchor="middle" fontFamily={BEBAS} fontSize={r * 1.5} fill="#fff">{n}</text></g>); };

const Portada: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const dx = 7 * Math.sin(f / 8), dy = -5 * Math.cos(f / 10); const k = 1 + 0.05 * Math.sin(f / 5);
  return (<Hoja first>
    <Tx text="VINCULASTE ESTRUCTURA" x={540} y={250} t0={-1} size={112} font="h" align="center" />
    <Tx text="Y APARECIÓ A KILÓMETROS DE ARQUITECTURA" x={540} y={370} t0={-1} size={60} font="h" color="#fff" bg={COPPER} align="center" />
    <Svg>
      <Tr d={hand([[70, 900], [600, 860], [640, 1310], [90, 1330], [70, 900]], 3, 3)} t0={-1} color={GREY} w={4} dash="18 12" />
      <Edif x={190} y={960} w={300} h={250} t0={-1} />
      <g transform={`translate(${dx} ${dy}) rotate(-7 960 650)`}><Edif x={850} y={540} w={260} h={210} t0={-1} est /></g>
      <Cota a={[494, 956]} b={[846, 760]} t0={-1} color={RED} w={5} tick={16} />
      <Circ cx={610} cy={800} rx={150} ry={74} t0={d * 0.5} seed={9} w={7} />
    </Svg>
    <Tx text="ARQUITECTURA" x={190} y={1222} t0={-1} size={32} color={INK} />
    <Tx text="ESTRUCTURA" x={826} y={470} t0={-1} size={32} color={COPPER} />
    <div style={{ position: "absolute", left: 480, top: 746, transform: `rotate(-29deg) scale(${k})` }}><Tx text="¿? km" x={0} y={0} t0={-1} size={104} font="h" color={RED} /></div>
    <Tx text="LOTE" x={100} y={1270} t0={-1} size={26} color={GREY} />
  </Hoja>); };

const Tres: React.FC<{ d: number }> = ({ d }) => { const a = 0.75, b = w(1, /^cada$/i, 0.62) - 0.15;
  return (<Hoja>
    <Tx text="REVIT TIENE" x={540} y={250} t0={0.2} size={110} font="h" align="center" /><Tx text="3 ORÍGENES" x={540} y={356} t0={0.45} size={150} font="h" color={COPPER} align="center" />
    <Svg>
      <Ejes x={190} y={760} s={96} t0={a} /><PBase x={540} y={730} s={74} t0={a + 0.4} /><PRec x={880} y={730} s={86} t0={a + 0.8} />
      <Num x={200} y={920} n="1" r={54} t0={a + 0.3} /><Num x={540} y={920} n="2" r={54} t0={a + 0.7} /><Num x={880} y={920} n="3" r={54} t0={a + 1.1} />
      <Ln a={[200, 990]} b={[250, 1100]} t0={b} color={GREY} w={4} dash="10 10" /><Ln a={[540, 990]} b={[700, 1100]} t0={b + 0.5} color={GREY} w={4} dash="10 10" />
      <Edif x={150} y={1110} w={230} h={170} t0={b + 0.1} /><Edif x={620} y={1110} w={230} h={170} t0={b + 0.6} est />
    </Svg>
    <Tx text="ARQUITECTURA" x={150} y={1290} t0={b + 0.3} size={28} color={INK} /><Tx text="ESTRUCTURA" x={620} y={1290} t0={b + 0.8} size={28} color={COPPER} />
  </Hoja>); };

const Interno: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const a = w(2, /^Nunca$/i, 0.3), b = w(2, /^menos$/i, 0.7) - 0.3; const C: Pt = [540, 800];
  return (<Hoja n="1 DE 3">
    <TitN n="1" a="ORIGEN INTERNO" size={112} />
    <Svg>
      <Ejes x={C[0]} y={C[1]} s={130} t0={0.5} sw={9} />
      <Ln a={[C[0] + 6, C[1] - 6]} b={[C[0] + 78, C[1] - 118]} t0={a - 0.1} color={GREY} w={6} dur={0.12} />
      {f / 30 > a && <circle cx={C[0] + 84} cy={C[1] - 128} r={24 + 2 * Math.sin(f / 5)} fill={RED} />}
      <Tr d={loop(C[0], C[1], 330, 330, 12)} t0={b} dur={0.7} color={GREY} w={5} dash="6 16" />
      <Cota a={[C[0] + 20, C[1] + 60]} b={[C[0] + 262, C[1] + 196]} t0={b + 0.4} color={COPPER} w={5} />
    </Svg>
    <Tx text="16 km" x={660} y={950} t0={b + 0.55} size={84} font="h" color={COPPER} rot={29} />
    <Tx text="NUNCA SE MUEVE" x={540} y={1168} t0={a + 0.1} size={88} font="h" color="#fff" bg={INK} align="center" />
    <Tx text="TODO A MENOS DE 16 km" x={540} y={1276} t0={b + 0.7} size={84} font="h" color={COPPER} align="center" />
  </Hoja>); };

const Base: React.FC<{ d: number }> = ({ d }) => { const a = w(3, /^Tu$/i, 0.42), b = w(3, /^esquina/i, 0.65) - 0.2;
  return (<Hoja n="2 DE 3">
    <TitN n="2" a="PUNTO BASE DEL PROYECTO" size={86} />
    <Svg>
      <Caja x={380} y={560} w={480} h={400} t0={0.5} fill={CON} seed={18} dur={0.45} />
      <Ln a={[380, 478]} b={[380, 1040]} t0={b} color={GREY} w={4} dash="22 10 4 10" /><Ln a={[250, 960]} b={[930, 960]} t0={b + 0.25} color={GREY} w={4} dash="22 10 4 10" />
      <Tr d={loop(380, 440, 36, 36, 4)} t0={b + 0.1} dur={0.2} color={GREY} w={4} /><Tr d={loop(212, 960, 36, 36, 6)} t0={b + 0.35} dur={0.2} color={GREY} w={4} />
      <PBase x={380} y={960} s={62} t0={a - 0.9 > 1 ? a - 0.9 : 1} sw={9} />
      <Circ cx={380} cy={960} rx={104} ry={98} t0={b + 0.7} seed={7} w={6} />
    </Svg>
    <Tx text="A" x={380} y={416} t0={b + 0.2} size={44} font="h" color={GREY} align="center" w={80} /><Tx text="1" x={212} y={936} t0={b + 0.45} size={44} font="h" color={GREY} align="center" w={80} />
    <Tx text="una esquina o un cruce de ejes" x={470} y={1010} t0={b + 0.3} size={30} color={GREY} />
    <Tx text="TU REFERENCIA LOCAL" x={540} y={1176} t0={a} size={100} font="h" color="#fff" bg={BLUE} align="center" />
  </Hoja>); };

const garabato = (x: number, y: number, n: number, seed: number): string => { const pts: Pt[] = []; for (let i = 0; i <= n * 2; i++) pts.push([x + i * 13, y + (i % 2 ? -9 : 7) + ((seed * (i + 3)) % 5) - 2]); return hand(pts, seed, 2); };
const Recon: React.FC<{ d: number }> = ({ d }) => { const a = w(4, /^Las$/i, 0.5);
  return (<Hoja n="3 DE 3">
    <TitN n="3" a="PUNTO DE RECONOCIMIENTO" size={84} />
    <Svg>
      <Tr d={hand([[140, 620], [860, 560], [930, 1060], [190, 1100], [140, 620]], 5, 3)} t0={0.45} dur={0.7} color={INK} w={5} dash="26 10 5 10" />
      <Caja x={330} y={760} w={280} h={210} t0={0.9} fill={CON} seed={19} sw={4} color={GREY} />
      <Caja x={846} y={546} w={28} h={28} t0={1.1} fill={INK} seed={20} sw={4} />
      <PRec x={860} y={556} s={78} t0={1.3} sw={9} />
      <Flecha a={[210, 1040]} b={[210, 900]} t0={1.0} color={GREY} w={5} head={20} />
      <Tr d={garabato(560, 690, 9, 3)} t0={a + 0.1} dur={0.5} color={COPPER} w={5} /><Tr d={garabato(560, 762, 8, 7)} t0={a + 0.6} dur={0.5} color={COPPER} w={5} />
    </Svg>
    <Tx text="N" x={210} y={846} t0={1.1} size={40} font="h" color={GREY} align="center" w={60} />
    <Tx text="hito del lindero" x={560} y={600} t0={1.6} size={30} color={GREY} />
    <Tx text="N =" x={470} y={664} t0={a} size={44} font="f" color={COPPER} /><Tx text="E =" x={470} y={736} t0={a + 0.5} size={44} font="f" color={COPPER} />
    <Tx text="COORDENADAS REALES" x={540} y={1176} t0={a + 0.2} size={100} font="h" color="#fff" bg={COPPER} align="center" />
    <Tx text="las del terreno" x={540} y={1296} t0={a + 0.9} size={34} color={GREY} align="center" />
  </Hoja>); };

const Vincular: React.FC<{ d: number }> = ({ d }) => { const t = useT(); const a = w(5, /^Si$/, 0.42) - 0.15, mv = w(5, /^movió$/i, 0.55), vi = w(5, /^vinculas$/i, 0.75), no = w(5, /^no$/i, 0.88);
  const out = 1 - p(t, a - 0.25, 0.25); const ys = [806, 914, 1022];
  return (<Hoja>
    <Tx text="AL VINCULAR ELIGES" x={540} y={250} t0={0.05} size={108} font="h" align="center" /><Tx text="CON CUÁL ALINEAR" x={540} y={356} t0={0.25} size={108} font="h" color={COPPER} align="center" />
    {out > 0 && <AbsoluteFill style={{ opacity: out, transform: `translateY(${(1 - out) * -40}px)` }}>
      <Svg>
        <Caja x={110} y={500} w={860} h={640} t0={0.15} fill="#fff" seed={25} dur={0.35} /><Ln a={[110, 584]} b={[970, 584]} t0={0.4} w={4} />
        <Caja x={150} y={668} w={780} h={70} t0={0.5} sw={4} seed={26} fill="#fff" /><Tr d="M 876,692 L 892,712 L 908,692" t0={0.6} dur={0.1} w={5} />
        <Caja x={150} y={746} w={780} h={336} t0={0.7} sw={4} seed={27} fill="#F1F4F8" />
        {ys.map((y, i) => (<g key={i}><Num x={214} y={y} n={`${i + 1}`} r={32} t0={0.85 + i * 0.2} />
          <Flecha a={[470, y]} b={[610, y]} t0={0.95 + i * 0.2} color={GREY} w={5} head={16} dur={0.12} /><Flecha a={[610, y]} b={[470, y]} t0={1.0 + i * 0.2} color={GREY} w={5} head={16} dur={0.05} /></g>))}
        <Ejes x={350} y={ys[0] + 14} s={44} t0={0.9} sw={6} /><Ejes x={720} y={ys[0] + 14} s={44} t0={1.0} sw={6} c={COPPER} />
        <PBase x={360} y={ys[1]} s={34} t0={1.1} sw={6} /><PBase x={730} y={ys[1]} s={34} t0={1.2} sw={6} c={COPPER} />
        <PRec x={360} y={ys[2]} s={38} t0={1.3} sw={6} c={INK} /><PRec x={730} y={ys[2]} s={38} t0={1.4} sw={6} />
        <Circ cx={540} cy={914} rx={436} ry={196} t0={Math.max(1.6, a - 1.2)} seed={11} w={8} dur={0.45} />
      </Svg>
      <Tx text="Vincular Revit" x={144} y={520} t0={0.3} size={40} /><Tx text="×" x={908} y={506} t0={0.4} size={56} color={GREY} />
      <Tx text="Posicionamiento:" x={152} y={616} t0={0.45} size={34} color={GREY} />
      <Tx text="esquema del cuadro, no es una captura" x={540} y={1152} t0={0.8} size={28} color={GREY} align="center" />
    </AbsoluteFill>}
    <Svg>
      <Edif x={150} y={720} w={330} h={270} t0={a + 0.05} />
      <PBase x={150} y={990} s={40} t0={a + 0.4} sw={6} c={GREY} dash="8 8" />
      <Flecha a={[196, 1030]} b={[396, 1110]} t0={mv} color={BLUE} w={6} dur={0.3} /><PBase x={440} y={1128} s={44} t0={mv + 0.3} sw={7} />
      <g transform="translate(0 0)"><Edif x={560} y={560} w={330} h={270} t0={vi} est /></g>
      <Ejes x={560} y={830} s={46} t0={vi + 0.35} sw={5} c={COPPER} /><Ejes x={150} y={990} s={46} t0={vi + 0.5} sw={5} />
      <Ln a={[200, 964]} b={[540, 846]} t0={vi + 0.7} color={RED} w={5} dash="14 12" />
      <Equis cx={520} cy={1010} r={64} t0={no} w={16} />
    </Svg>
    <Tx text="ARQUITECTURA" x={150} y={672} t0={a + 0.3} size={30} color={INK} /><Tx text="ESTRUCTURA" x={560} y={512} t0={vi + 0.2} size={30} color={COPPER} />
    <Tx text="punto base movido" x={500} y={1108} t0={mv + 0.5} size={30} color={BLUE} />
  </Hoja>); };

const Acuerdo: React.FC<{ d: number }> = ({ d }) => { const f = useCurrentFrame(); const k = interpolate(f, [12, 30], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.4)) });
  return (<Hoja>
    <Svg>
      <Ln a={[300, 300]} b={[300, 960]} t0={-1} color={GREY} w={4} dash="22 10 4 10" /><Ln a={[180, 860]} b={[900, 860]} t0={-1} color={GREY} w={4} dash="22 10 4 10" />
      <Edif x={300} y={380} w={500} h={480} t0={-1} />
      <g transform={`translate(${k * 230} ${k * -150})`}><Edif x={300} y={380} w={500} h={480} t0={-1} est /></g>
      <PBase x={300} y={860} s={50} t0={0.95} sw={8} />
    </Svg>
    <Sello text="SE ACUERDA ANTES DE MODELAR" x={540} y={570} t0={1.0} size={72} color={COPPER} rot={-4} bg="rgba(250,251,252,.96)" />
    <Tx text="CON TODO EL EQUIPO" x={540} y={1020} t0={1.35} size={118} font="h" align="center" />
  </Hoja>); };

export const Origenes: React.FC = () => { const E = T.escenas;
  return (<AbsoluteFill style={{ background: INK }}>
    <Escenas T={T}>{[
      <Portada d={E[0].dur + E[0].s} />, <Tres d={E[1].dur} />, <Interno d={E[2].dur} />, <Base d={E[3].dur} />, <Recon d={E[4].dur} />, <Vincular d={E[5].dur} />, <Acuerdo d={E[6].dur} />,
      <Cierre titulo={<>¿CON CUÁL<br />VINCULAS TÚ?</>} fila opciones={[["1", "ORIGEN INTERNO"], ["2", "PUNTO BASE DEL PROYECTO"], ["3", "PUNTO DE RECONOCIMIENTO"]]} pie="DINOS EL NÚMERO" boton="COMENTA «NIVEL»" />,
    ]}</Escenas>
    <Subs T={T} />
  </AbsoluteFill>); };
