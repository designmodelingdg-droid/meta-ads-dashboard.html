import React from "react";
import { Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { brand } from "../brand/brand";
import data from "../data/diplomado.json";
import { AppTile, Burst, Caption, Finale, Frame, Glass, Hero, HookRow, K, LOGO, LightLine, Pop, StepCard, Whip, clamp, makeTiming, sp, useStage } from "./kit";

// Diplomado BIM en Cálculo Estructural y Documentación Técnica: 5 módulos, 200 h, 4 meses,
// MasterClass en vivo por módulo, Tutor IA y 5 certificaciones (DM, Autodesk, DQ, Sabal, UdN).
const t = makeTiming(data, 40);
export const DIPLO_DURATION = t.duration;
const { S, at } = t;

const MODS = [
  { n: "1", title: "ACERO SISMORRESISTENTE", chips: [["EDIFICIOS DE ACERO", "edificios"], ["SISMORRESISTENTE", "sismo"], ["ROBOT", "robot"]] },
  { n: "2", title: "CONEXIONES PRECALIFICADAS", chips: [["CONEXIONES", "conexiones"], ["PRECALIFICADAS", "precalif"], ["ADVANCE STEEL", "advance"]] },
  { n: "3", title: "HORMIGÓN ARMADO SISMORRESISTENTE", chips: [["SISMORRESISTENTE", "sismo"], ["EDIFICIOS", "edificios"], ["HORMIGÓN ARMADO", "hormig"]] },
  { n: "4", title: "DETALLADO DEL REFUERZO", chips: [["REFUERZO", "refuerzo"], ["PLANOS DE ARMADO", "armado"], ["DESPIECE", "despiece"]] },
  { n: "5", title: "DOCUMENTACIÓN BIM", chips: [["REVIT", "revit"], ["HORMIGÓN", "hormig"], ["ACERO", "acero"]] },
] as const;
const chipAt = (m: number, i: number) => at(MODS[m].chips[i][1], m + 1, i, 3);
const st = { fill: "none", stroke: K.copperHi, strokeLinejoin: "round" as const, strokeLinecap: "round" as const };

/** Pórtico de 3 pisos que oscila con el sismo. `concreto` lo dibuja con columnas gruesas de hormigón. */
const Sismo: React.FC<{ m: number; concreto?: boolean }> = ({ m, concreto }) => {
  const frame = useCurrentFrame();
  const a = S(m + 1) + 12;
  const pIn = sp(frame, a, 15);
  const tS = chipAt(m, concreto ? 0 : 1);
  const amp = interpolate(frame, [tS - 4, tS + 10], [0, 1], clamp);
  const sway = Math.sin(frame / 5) * 24 * amp;
  const lv = [0, 1, 2, 3].map((k) => ({ y: 200 - k * 130, dx: sway * (k / 3) ** 1.2 }));
  const col = concreto ? "#C9CED8" : K.copperHi;
  const wCol = concreto ? 30 : 14;
  return (
    <div style={{ position: "absolute", left: -260, top: -260, opacity: Math.min(1, pIn * 1.5), transform: `translateY(${(1 - pIn) * 60}px)` }}>
      <svg width={520} height={560} viewBox="-20 -230 520 560" style={{ overflow: "visible", filter: `drop-shadow(0 0 14px ${K.copper}88)` }}>
        {[0, 1, 2].map((k) =>
          [60, 240, 420].map((x) => <line key={`${k}-${x}`} x1={x + lv[k].dx} y1={lv[k].y} x2={x + lv[k + 1].dx} y2={lv[k + 1].y} {...st} stroke={col} strokeWidth={wCol} strokeLinecap="butt" />),
        )}
        {[1, 2, 3].map((k) => (
          <line key={`b${k}`} x1={60 + lv[k].dx} y1={lv[k].y} x2={420 + lv[k].dx} y2={lv[k].y} {...st} stroke={concreto ? "#E3E6EC" : "#FFFFFF"} strokeWidth={concreto ? 22 : 12} />
        ))}
        {concreto &&
          [1, 2, 3].map((k) => <line key={`r${k}`} x1={60 + lv[k].dx} y1={lv[k].y + 5} x2={420 + lv[k].dx} y2={lv[k].y + 5} stroke={K.copper} strokeWidth={3} strokeDasharray="14 8" />)}
        {[0, 1, 2].map((k) => (
          <path key={`w${k}`} d={`M ${-10 + k * 4} ${226 + k * 18} q 30 -${16 * amp} 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0`} fill="none" stroke={K.red} strokeWidth={4} opacity={amp * (0.8 - k * 0.2)} transform={`translate(${(frame * 3) % 60 - 30} 0)`} />
        ))}
        <line x1={-10} y1={210} x2={490} y2={210} stroke={K.muted} strokeWidth={6} />
      </svg>
      <div style={{ position: "absolute", left: 470, top: 0 }}>
        <Pop at={concreto ? a + 6 : chipAt(m, 2) - 6} x={0} y={0} w={140} h={140}>
          <AppTile src={LOGO("robot.png")} w={140} h={140} pad={8} />
        </Pop>
      </div>
    </div>
  );
};

/** Unión viga-columna con placa extrema y pernos (conexión precalificada). */
const Union: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(2) + 12;
  const pIn = sp(frame, a, 15);
  const tBolts = chipAt(1, 1) - 4;
  return (
    <div style={{ position: "absolute", left: -280, top: -240, opacity: Math.min(1, pIn * 1.5), transform: `scale(${0.85 + 0.15 * pIn})` }}>
      <svg width={460} height={480} viewBox="0 0 460 480" style={{ filter: `drop-shadow(0 0 14px ${K.copper}88)` }}>
        <rect x={40} y={0} width={34} height={480} fill={`${K.copper}55`} stroke={K.copperHi} strokeWidth={6} />
        <rect x={74} y={0} width={14} height={480} fill={`${K.copper}33`} stroke={K.copperHi} strokeWidth={4} />
        <rect x={88} y={150} width={22} height={200} fill="#FFFFFF33" stroke="#FFFFFF" strokeWidth={5} />
        <rect x={110} y={170} width={330} height={20} fill={`${K.copper}55`} stroke={K.copperHi} strokeWidth={5} />
        <rect x={110} y={310} width={330} height={20} fill={`${K.copper}55`} stroke={K.copperHi} strokeWidth={5} />
        <rect x={110} y={190} width={14} height={120} fill={`${K.copper}33`} stroke={K.copperHi} strokeWidth={4} />
        <line x1={110} y1={250} x2={440} y2={250} stroke={K.copperHi} strokeWidth={4} strokeDasharray="10 8" opacity={0.5} />
        {[165, 215, 285, 335].map((y, i) => {
          const p = sp(frame, tBolts + i * 3, 10);
          return <circle key={y} cx={99} cy={y} r={11 * p} fill={K.white} stroke={K.copper} strokeWidth={3} />;
        })}
      </svg>
      <div style={{ position: "absolute", left: 470, top: 40 }}>
        <Pop at={chipAt(1, 2) - 6} x={0} y={0} w={150} h={150}>
          <AppTile src={LOGO("advance.png")} w={150} h={150} pad={8} />
        </Pop>
      </div>
    </div>
  );
};

/** Sección de viga con varillas y estribos que se dibujan, y la barra de despiece. */
const Refuerzo: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(4) + 12;
  const pIn = sp(frame, a, 15);
  const tR = chipAt(3, 0) - 4;
  const tA = chipAt(3, 1) - 4;
  const tD = chipAt(3, 2) - 4;
  const est = interpolate(frame, [tR, tR + 16], [0, 1], clamp);
  return (
    <div style={{ position: "absolute", left: -330, top: -230, opacity: Math.min(1, pIn * 1.5), transform: `scale(${0.85 + 0.15 * pIn})` }}>
      <svg width={300} height={400} viewBox="0 0 300 400" style={{ filter: `drop-shadow(0 0 14px ${K.copper}88)` }}>
        <rect x={20} y={20} width={260} height={360} rx={8} fill="#C9CED822" stroke="#C9CED8" strokeWidth={6} />
        <rect x={50} y={50} width={200} height={300} rx={14} fill="none" stroke={K.copperHi} strokeWidth={6} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - est} />
        {[
          [75, 75],
          [150, 75],
          [225, 75],
          [75, 325],
          [150, 325],
          [225, 325],
        ].map(([x, y], i) => {
          const p = sp(frame, tR + 6 + i * 3, 10);
          return <circle key={i} cx={x} cy={y} r={15 * p} fill={K.copper} stroke="#FFFFFF" strokeWidth={3} />;
        })}
      </svg>
      <div style={{ position: "absolute", left: 330, top: 10 }}>
        <Pop at={tA} x={170} y={110} w={340} h={220} rot={6}>
          <div style={{ width: 340, height: 220, borderRadius: 10, background: "#F4F1E8", border: `6px solid ${K.copper}`, boxShadow: `0 0 30px ${K.copper}88`, position: "relative", overflow: "hidden" }}>
            <svg width={340} height={220} viewBox="0 0 340 220">
              <rect x={20} y={60} width={300} height={70} fill="none" stroke="#1D3A6E" strokeWidth={4} />
              <line x1={30} y1={72} x2={310} y2={72} stroke={K.copper} strokeWidth={4} />
              <line x1={30} y1={118} x2={310} y2={118} stroke={K.copper} strokeWidth={4} />
              {Array.from({ length: 13 }, (_, k) => (
                <line key={k} x1={34 + k * 22} y1={64} x2={34 + k * 22} y2={126} stroke="#1D3A6E" strokeWidth={2} />
              ))}
            </svg>
            <div style={{ position: "absolute", left: 12, bottom: 10, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 18, color: "#1D3A6E" }}>PLANO DE ARMADO · V-101</div>
          </div>
        </Pop>
        <Pop at={tD} x={170} y={330} w={340} h={120}>
          <Glass w={340} h={120}>
            <div style={{ position: "absolute", left: 20, top: 14, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 18, letterSpacing: 3, color: K.copperHi }}>DESPIECE</div>
            <svg width={340} height={120} viewBox="0 0 340 120" style={{ position: "absolute", left: 0, top: 0 }}>
              <path d="M 30 90 L 30 60 L 300 60 L 300 90" fill="none" stroke="#FFFFFF" strokeWidth={6} />
              <text x="165" y="104" textAnchor="middle" fontFamily={brand.fontBody} fontWeight={800} fontSize="18" fill={K.copperHi}>
                Ø16 · L = 6,40 m · 4 u
              </text>
            </svg>
          </Glass>
        </Pop>
      </div>
    </div>
  );
};

/** Revit: plano estructural y lista de materiales de hormigón y acero. */
const Planos: React.FC = () => {
  const frame = useCurrentFrame();
  const rows = ["Hormigón f'c 240 · 86 m³", "Acero Ø12 · 3.410 kg", "W12x26 · 24 u", "Placa 3/8 · 48 u"];
  const tL = chipAt(4, 1) - 4;
  return (
    <>
      <Pop at={Math.min(chipAt(4, 0) - 6, S(5) + 12)} x={-300} y={-170} w={160} h={160}>
        <AppTile src={LOGO("revit.png")} w={160} h={160} pad={26} />
      </Pop>
      <Pop at={S(5) + 16} x={-60} y={-40} w={420} h={300} rot={-6}>
        <div style={{ width: 420, height: 300, borderRadius: 10, background: "#F4F1E8", border: `6px solid ${K.copper}`, boxShadow: `0 0 30px ${K.copper}88`, position: "relative", overflow: "hidden" }}>
          <svg width={420} height={300} viewBox="0 0 420 300">
            {[60, 140, 220, 300].map((x) => (
              <line key={x} x1={x} y1={30} x2={x} y2={230} stroke="#1D3A6E" strokeWidth={3} />
            ))}
            {[30, 130, 230].map((y) => (
              <line key={y} x1={40} y1={y} x2={320} y2={y} stroke="#1D3A6E" strokeWidth={4} />
            ))}
            {[60, 140, 220, 300].map((x) => [30, 130, 230].map((y) => <rect key={`${x}${y}`} x={x - 8} y={y - 8} width={16} height={16} fill="#1D3A6E" />))}
            <rect x={330} y={230} width={80} height={60} fill="none" stroke="#1D3A6E" strokeWidth={3} />
          </svg>
          <div style={{ position: "absolute", left: 12, bottom: 8, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 18, color: "#1D3A6E" }}>E-101 · PLANTA ESTRUCTURAL</div>
        </div>
      </Pop>
      <Pop at={tL} x={250} y={60} w={330} h={260} rot={6}>
        <Glass w={330} h={260}>
          <div style={{ position: "absolute", left: 22, top: 18, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 20, letterSpacing: 3, color: K.copperHi }}>LISTA DE MATERIALES</div>
          {rows.map((r, i) => {
            const p = interpolate(frame, [tL + 4 + i * 5, tL + 12 + i * 5], [0, 1], clamp);
            return (
              <div key={r} style={{ position: "absolute", left: 22, top: 62 + i * 46, right: 22, height: 36, borderRadius: 8, background: "rgba(255,255,255,.08)", opacity: p, transform: `translateX(${(1 - p) * 30}px)`, display: "flex", alignItems: "center", paddingLeft: 12, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 19, color: K.white }}>
                {r}
              </div>
            );
          })}
        </Glass>
      </Pop>
    </>
  );
};

/** MasterClass en vivo por módulo + Tutor IA (grabación real). */
const Acompanamiento: React.FC = () => {
  const frame = useCurrentFrame();
  const { V } = useStage();
  const tT = at("tutor", 6, 1, 2) - 6;
  return (
    <>
      <Pop at={S(6) + 10} x={V ? 0 : -330} y={V ? -200 : -20} w={420} h={220}>
        <div style={{ width: 420, height: 220, borderRadius: 24, background: K.card, border: `5px solid ${K.red}`, boxShadow: `0 0 40px ${K.red}66`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 10 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ width: 34, height: 34, borderRadius: "50%", background: K.red, opacity: 0.5 + 0.5 * Math.abs(Math.sin(frame / 6)), boxShadow: `0 0 20px ${K.red}` }} />
            <div style={{ fontFamily: brand.fontDisplay, fontSize: 70, color: K.white }}>EN VIVO</div>
          </div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 26, letterSpacing: 4, color: K.copperHi }}>MASTERCLASS POR MÓDULO</div>
        </div>
      </Pop>
      <Pop at={tT} x={V ? 0 : 260} y={V ? 140 : -20} w={560} h={350}>
        <div style={{ width: 560, height: 350, borderRadius: 22, overflow: "hidden", border: `6px solid ${K.copper}`, boxShadow: `0 0 40px ${K.copper}88`, position: "relative", background: "#000" }}>
          <OffthreadVideo src={staticFile("rutas/tutor.mp4")} muted startFrom={90} style={{ position: "absolute", width: 640, left: -40, top: -235 }} />
          <div style={{ position: "absolute", left: 14, top: 12, padding: "8px 16px 4px", borderRadius: 999, background: K.copper, fontFamily: brand.fontDisplay, fontSize: 34, color: K.white }}>TUTOR IA</div>
        </div>
      </Pop>
    </>
  );
};

const CERTS = [
  { src: "cert-dm.jpg", ratio: 0.707, stem: "design", slot: 0 },
  { src: "cert-autodesk.jpg", ratio: 0.576, stem: "autodesk", slot: 1 },
  { src: "cert-dq.jpg", ratio: 0.696, stem: "dq", slot: 2 },
  { src: "cert-sabal.jpg", ratio: 1.406, stem: "sabal", slot: 3 },
  { src: "cert-udn.jpg", ratio: 1.259, stem: "naciones", slot: 4 },
];
const certAt = (i: number) => at(CERTS[i].stem, 7, CERTS[i].slot, 5) - 6;

/** Las 5 certificaciones reales de muestra, en abanico. */
const Certificados: React.FC = () => {
  const { V } = useStage();
  const pos = V
    ? [
        { x: -180, y: -250, w: 380, r: -8 },
        { x: 190, y: -230, w: 380, r: 7 },
        { x: 0, y: -20, w: 400, r: -3 },
        { x: -200, y: 230, w: 230, r: -6 },
        { x: 200, y: 230, w: 230, r: 6 },
      ]
    : [
        { x: -700, y: -40, w: 400, r: -8 },
        { x: -290, y: -90, w: 400, r: -2 },
        { x: 130, y: -40, w: 400, r: 4 },
        { x: 490, y: -30, w: 230, r: 6 },
        { x: 760, y: -20, w: 240, r: 9 },
      ];
  return (
    <>
      {CERTS.map((c, i) => {
        const p = pos[i];
        const { w, x, y } = p;
        return (
          <Pop key={c.src} at={Math.max(S(7) + 10 + i * 2, certAt(i))} x={x} y={y} w={w} h={w * c.ratio} rot={p.r * 2}>
            <div style={{ transform: `rotate(${p.r}deg)`, borderRadius: 8, overflow: "hidden", border: "4px solid #FFFFFF", boxShadow: `0 0 30px ${K.copper}88, 0 16px 30px rgba(0,0,0,.5)` }}>
              <Img src={LOGO(c.src)} style={{ width: w, display: "block" }} />
            </div>
          </Pop>
        );
      })}
    </>
  );
};

export const Diplomado: React.FC = () => {
  const conv = at("200", 8, 0, 2) - 4;
  const cta = Math.max(at("pide", 8, 1, 2) - 3, conv + 40);
  return (
    <Frame
      t={t}
      voice="rutas/voz_diplomado.wav"
      cta={cta}
      whooshes={[1, 2, 3, 4, 5, 6, 7, 8].map(S)}
      bongs={[1, 2, 3, 4, 5].map((i) => S(i) + 11)}
      extra={[
        { at: at("5", 0, 1, 2) - 3, src: "sfx/casino/chips-stack-3.ogg", vol: 0.35 },
        ...CERTS.map((_, i) => ({ at: certAt(i), src: "sfx/interface/drop_002.ogg", vol: 0.3 })),
        { at: conv + 4, src: "sfx/impact/impactBell_heavy_000.ogg", vol: 0.35 },
      ]}
    >
      <Whip from={0} to={S(1)} first>
        <HookRow kicker="DIPLOMADO BIM" title={<>CÁLCULO ESTRUCTURAL<br /><span style={{ color: K.copperHi }}>Y DOCUMENTACIÓN</span></>} labels={["1", "2", "3", "4", "5"]} at={at("5", 0, 1, 2) - 4} goal="DIPLOMADO" size={104} />
      </Whip>
      {MODS.map((m, i) => (
        <Whip key={m.n} from={S(i + 1)} to={S(i + 2)}>
          <LightLine from={S(i + 1)} to={S(i + 2)} />
          <Burst at={S(i + 1) + 12} />
          <Hero>
            {i === 0 && <Sismo m={0} />}
            {i === 1 && <Union />}
            {i === 2 && <Sismo m={2} concreto />}
            {i === 3 && <Refuerzo />}
            {i === 4 && <Planos />}
          </Hero>
          <StepCard n={m.n} kicker={`MÓDULO ${m.n} DE 5`} title={m.title} chips={m.chips.map((x, k) => ({ label: x[0], at: chipAt(i, k) }))} from={S(i + 1)} to={S(i + 2)} />
        </Whip>
      ))}
      <Whip from={S(6)} to={S(7)}>
        <LightLine from={S(6)} to={S(7)} />
        <Hero>
          <Acompanamiento />
        </Hero>
        <Caption txt="MASTERCLASS EN VIVO" from={S(6) + 10} to={at("tutor", 6, 1, 2) - 6} />
        <Caption txt="TUTOR IA INCLUIDO" from={at("tutor", 6, 1, 2) - 6} to={S(7)} />
      </Whip>
      <Whip from={S(7)} to={S(8)}>
        <LightLine from={S(7)} to={S(8)} />
        <Burst at={S(7) + 12} />
        <Hero>
          <Certificados />
        </Hero>
        <Caption txt="5 CERTIFICACIONES" from={S(7) + 12} to={S(8)} />
      </Whip>
      <Whip from={S(8)} to={t.duration + 20}>
        <Finale at={conv} cta={cta} kicker="DIPLOMADO BIM" big="DIPLOMADO" sub="CÁLCULO ESTRUCTURAL Y DOCUMENTACIÓN" meta="5 MÓDULOS · 200 HORAS · 4 MESES" />
      </Whip>
    </Frame>
  );
};
