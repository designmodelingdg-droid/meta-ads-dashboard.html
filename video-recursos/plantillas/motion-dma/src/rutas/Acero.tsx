import React from "react";
import { Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { brand } from "../brand/brand";
import { ease } from "../lib/motion";
import data from "../data/acero.json";
import { AppTile, Burst, Caption, Finale, Frame, Glass, Hero, HookRow, K, LOGO, LightLine, Pop, StepCard, Whip, clamp, makeTiming, sp, useStage } from "./kit";

// Especialización en Diseño Estructural BIM en Acero: sus 4 cursos, Tutor IA, sesiones 1 a 1
// y los certificados (Design Modeling + Autodesk, como Authorized Training Center).
const t = makeTiming(data, 40);
export const ACERO_DURATION = t.duration;
const { S, at } = t;

const COURSES = [
  { n: "1", title: "ESTRUCTURAS DE ACERO EN ROBOT", chips: [["ANÁLISIS MODAL", "modal"], ["FUERZAS SÍSMICAS", "sism"], ["DISEÑO DE ELEMENTOS", "diseno"]] },
  { n: "2", title: "NAVES INDUSTRIALES", chips: [["CÁLCULO", "calculo"], ["CERCHAS", "serch"], ["MARCOS RÍGIDOS", "marcos"]] },
  { n: "3", title: "UNIONES METÁLICAS", chips: [["TEORÍA", "teoria"], ["CÁLCULO DE UNIONES", "uniones"], ["ADVANCE STEEL", "advance"]] },
  { n: "4", title: "MODELADO BIM EN REVIT", chips: [["PLANOS", "planos"], ["FAMILIAS", "familias"], ["LISTAS DE MATERIALES", "listas"]] },
] as const;
const chipAt = (c: number, i: number) => at(COURSES[c].chips[i][1], c + 1, i, 3);
const st = { fill: "none", stroke: K.copperHi, strokeLinejoin: "round" as const, strokeLinecap: "round" as const };

/** Pórtico de 3 pisos que oscila en su primer modo, con ondas sísmicas en la base. */
const Sismo: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(1) + 12;
  const pIn = sp(frame, a, 15);
  const amp = interpolate(frame, [chipAt(0, 0) - 4, chipAt(0, 0) + 10], [0, 1], clamp) * (1 - 0.4 * interpolate(frame, [chipAt(0, 2), chipAt(0, 2) + 20], [0, 1], clamp));
  const sway = Math.sin(frame / 5) * 26 * amp;
  const lv = [0, 1, 2, 3].map((k) => ({ y: 200 - k * 130, dx: sway * (k / 3) ** 1.2 }));
  const waves = interpolate(frame, [chipAt(0, 1) - 4, chipAt(0, 1) + 4], [0, 1], clamp);
  return (
    <div style={{ position: "absolute", left: -260, top: -260, opacity: Math.min(1, pIn * 1.5), transform: `translateY(${(1 - pIn) * 60}px)` }}>
      <svg width={520} height={560} viewBox="-20 -230 520 560" style={{ overflow: "visible", filter: `drop-shadow(0 0 14px ${K.copper}88)` }}>
        {[0, 1, 2].map((k) =>
          [60, 240, 420].map((x) => <line key={`${k}-${x}`} x1={x + lv[k].dx} y1={lv[k].y} x2={x + lv[k + 1].dx} y2={lv[k + 1].y} {...st} strokeWidth={14} />),
        )}
        {[1, 2, 3].map((k) => (
          <line key={`b${k}`} x1={60 + lv[k].dx} y1={lv[k].y} x2={420 + lv[k].dx} y2={lv[k].y} {...st} stroke="#FFFFFF" strokeWidth={12} />
        ))}
        {[0, 1, 2].map((k) => (
          <path key={`w${k}`} d={`M ${-10 + k * 4} ${226 + k * 18} q 30 -${16 * waves} 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0`} fill="none" stroke={K.red} strokeWidth={4} opacity={waves * (0.8 - k * 0.2)} transform={`translate(${(frame * 3) % 60 - 30} 0)`} />
        ))}
        <line x1={-10} y1={210} x2={490} y2={210} stroke={K.muted} strokeWidth={6} />
      </svg>
      <div style={{ position: "absolute", left: 470, top: 0 }}>
        <Pop at={a + 6} x={0} y={0} w={140} h={140}>
          <AppTile src={LOGO("robot.png")} w={140} h={140} pad={8} />
        </Pop>
      </div>
    </div>
  );
};

/** Nave industrial: pórtico con cercha que se dibuja; los marcos rígidos se resaltan. */
const Nave: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(2) + 10;
  const draw = interpolate(frame, [a, a + 40], [0, 1], { ...clamp, easing: ease.inOut });
  const truss = interpolate(frame, [chipAt(1, 1) - 6, chipAt(1, 1) + 20], [0, 1], { ...clamp, easing: ease.inOut });
  const mr = interpolate(frame, [chipAt(1, 2) - 4, chipAt(1, 2) + 6], [0, 1], clamp);
  const diag = [];
  for (let i = 0; i < 8; i++) {
    const x0 = i * 60;
    const yT = (x: number) => 40 - (x <= 240 ? x : 480 - x) * 0.35;
    diag.push(`M ${x0} 40 L ${x0 + 60} ${yT(x0 + 60)}`, `M ${x0 + 60} 40 L ${x0 + 60} ${yT(x0 + 60)}`);
  }
  return (
    <div style={{ position: "absolute", left: -270, top: -200 }}>
      <svg width={540} height={420} viewBox="-30 -80 540 420" style={{ overflow: "visible", filter: `drop-shadow(0 0 14px ${K.copper}88)` }}>
        <path d="M 0 300 L 0 40 M 480 300 L 480 40" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw} {...st} stroke={mr > 0.5 ? K.green : K.copperHi} strokeWidth={16} />
        <path d="M 0 40 L 480 40 M 0 40 L 240 -44 L 480 40" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw} {...st} strokeWidth={12} />
        <path d={diag.join(" ")} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - truss} {...st} stroke="#FFFFFF" strokeWidth={5} />
        <line x1={-30} y1={300} x2={510} y2={300} stroke={K.muted} strokeWidth={6} />
        {mr > 0 &&
          [0, 480].map((x) => (
            <circle key={x} cx={x} cy={40} r={22 * mr} fill="none" stroke={K.green} strokeWidth={6} />
          ))}
      </svg>
    </div>
  );
};

/** Unión viga-columna con placa extrema y pernos. */
const Union: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(3) + 12;
  const pIn = sp(frame, a, 15);
  const tBolts = chipAt(2, 1) - 4;
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
        <Pop at={chipAt(2, 2) - 6} x={0} y={0} w={150} h={150}>
          <AppTile src={LOGO("advance.png")} w={150} h={150} pad={8} />
        </Pop>
      </div>
    </div>
  );
};

/** Revit: un plano y una lista de materiales que se llena. */
const Planos: React.FC = () => {
  const frame = useCurrentFrame();
  const rows = ["W12x26 · 24", "W8x18 · 36", "HSS 4x4 · 12", "Placa 3/8 · 48"];
  const tL = chipAt(3, 2) - 4;
  return (
    <>
      <Pop at={S(4) + 12} x={-300} y={-170} w={160} h={160}>
        <AppTile src={LOGO("revit.png")} w={160} h={160} pad={26} />
      </Pop>
      <Pop at={chipAt(3, 0) - 6} x={-60} y={-40} w={420} h={300} rot={-6}>
        <div style={{ width: 420, height: 300, borderRadius: 10, background: "#F4F1E8", border: `6px solid ${K.copper}`, boxShadow: `0 0 30px ${K.copper}88`, position: "relative", overflow: "hidden" }}>
          <svg width={420} height={300} viewBox="0 0 420 300">
            {[60, 140, 220, 300].map((x) => (
              <line key={x} x1={x} y1={30} x2={x} y2={230} stroke="#1D3A6E" strokeWidth={3} />
            ))}
            {[30, 130, 230].map((y) => (
              <line key={y} x1={40} y1={y} x2={320} y2={y} stroke="#1D3A6E" strokeWidth={4} />
            ))}
            <rect x={330} y={230} width={80} height={60} fill="none" stroke="#1D3A6E" strokeWidth={3} />
          </svg>
          <div style={{ position: "absolute", left: 12, bottom: 8, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 18, color: "#1D3A6E" }}>E-101 · PLANTA ESTRUCTURAL</div>
        </div>
      </Pop>
      <Pop at={chipAt(3, 1) - 4} x={250} y={60} w={300} h={260} rot={6}>
        <Glass w={300} h={260}>
          <div style={{ position: "absolute", left: 22, top: 18, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 20, letterSpacing: 3, color: K.copperHi }}>LISTA DE MATERIALES</div>
          {rows.map((r, i) => {
            const p = interpolate(frame, [tL + i * 5, tL + i * 5 + 8], [0, 1], clamp);
            return (
              <div key={r} style={{ position: "absolute", left: 22, top: 62 + i * 46, right: 22, height: 36, borderRadius: 8, background: "rgba(255,255,255,.08)", opacity: p, transform: `translateX(${(1 - p) * 30}px)`, display: "flex", alignItems: "center", paddingLeft: 12, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 20, color: K.white }}>
                {r}
              </div>
            );
          })}
        </Glass>
      </Pop>
    </>
  );
};

/** Tutor IA (grabación real) + 4 sesiones 1 a 1. */
const Acompanamiento: React.FC = () => {
  const frame = useCurrentFrame();
  const { V } = useStage();
  const tS = at("sesiones", 5, 1, 2) - 6;
  return (
    <>
      <Pop at={S(5) + 10} x={V ? 0 : -230} y={V ? -130 : -20} w={600} h={380}>
        <div style={{ width: 600, height: 380, borderRadius: 22, overflow: "hidden", border: `6px solid ${K.copper}`, boxShadow: `0 0 40px ${K.copper}88`, position: "relative", background: "#000" }}>
          <OffthreadVideo src={staticFile("rutas/tutor.mp4")} muted startFrom={F_TUTOR} style={{ position: "absolute", width: 680, left: -40, top: -250 }} />
          <div style={{ position: "absolute", left: 14, top: 12, padding: "8px 16px 4px", borderRadius: 999, background: K.copper, fontFamily: brand.fontDisplay, fontSize: 34, color: K.white }}>TUTOR IA</div>
        </div>
      </Pop>
      <Pop at={tS} x={V ? 0 : 330} y={V ? 190 : -20} w={340} h={200}>
        <Glass w={340} h={200}>
          <div style={{ position: "absolute", left: 0, right: 0, top: 26, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: 76, color: K.white }}>4 × 1 A 1</div>
          <div style={{ position: "absolute", left: 0, right: 0, top: 112, display: "flex", justifyContent: "center", gap: 16 }}>
            {[0, 1, 2, 3].map((k) => (
              <div key={k} style={{ width: 30, height: 30, borderRadius: "50%", background: frame >= tS + 6 + k * 4 ? K.copperHi : "#2B3E63", boxShadow: frame >= tS + 6 + k * 4 ? `0 0 14px ${K.copper}` : "none" }} />
            ))}
          </div>
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 16, textAlign: "center", fontFamily: brand.fontBody, fontWeight: 800, fontSize: 20, letterSpacing: 2, color: K.copperHi }}>SESIONES CON TU INSTRUCTOR</div>
        </Glass>
      </Pop>
    </>
  );
};
const F_TUTOR = 90;

/** Los dos certificados reales: Design Modeling y Autodesk (Authorized Training Center). */
const Certificados: React.FC = () => {
  const { V } = useStage();
  const tDM = at("design", 6, 0, 2) - 6;
  const tAD = at("autodesk", 6, 1, 2) - 6;
  const w = V ? 520 : 600;
  return (
    <>
      <Pop at={Math.min(tDM, S(6) + 14)} x={V ? 0 : -330} y={V ? -230 : -40} w={w} h={w * 0.707} rot={-10}>
        <div style={{ transform: "rotate(-5deg)", borderRadius: 10, overflow: "hidden", border: "5px solid #FFFFFF", boxShadow: `0 0 40px ${K.copper}88, 0 20px 40px rgba(0,0,0,.5)` }}>
          <Img src={LOGO("cert-dm.jpg")} style={{ width: w, display: "block" }} />
        </div>
      </Pop>
      <Pop at={tAD} x={V ? 0 : 330} y={V ? 160 : -40} w={w} h={w * 0.576} rot={10}>
        <div style={{ transform: "rotate(4deg)", borderRadius: 10, overflow: "hidden", border: "5px solid #FFFFFF", boxShadow: `0 0 50px ${K.copper}, 0 20px 40px rgba(0,0,0,.5)` }}>
          <Img src={LOGO("cert-autodesk.jpg")} style={{ width: w, display: "block" }} />
        </div>
      </Pop>
      <Pop at={at("autorizado", 6, 1, 2) - 8} x={V ? 0 : 330} y={V ? 380 : 230} w={420} h={110}>
        <Img src={LOGO("atc-white.png")} style={{ width: 420 }} />
      </Pop>
    </>
  );
};

export const Acero: React.FC = () => {
  const conv = at("120", 7, 0, 2) - 4;
  const cta = Math.max(at("pide", 7, 1, 2) - 3, conv + 40);
  const capY = undefined;
  return (
    <Frame
      t={t}
      voice="rutas/voz_acero.wav"
      cta={cta}
      whooshes={[1, 2, 3, 4, 5, 6, 7].map(S)}
      bongs={[1, 2, 3, 4].map((i) => S(i) + 11)}
      extra={[
        { at: at("4", 0, 1, 2) - 3, src: "sfx/casino/chips-stack-3.ogg", vol: 0.35 },
        { at: at("autodesk", 6, 1, 2) - 6, src: "sfx/impact/impactMetal_light_002.ogg", vol: 0.4 },
        { at: conv + 4, src: "sfx/impact/impactBell_heavy_000.ogg", vol: 0.35 },
      ]}
    >
      <Whip from={0} to={S(1)} first>
        <HookRow kicker="ESPECIALIZACIÓN" title={<>DISEÑO ESTRUCTURAL<br /><span style={{ color: K.copperHi }}>BIM EN ACERO</span></>} labels={["1", "2", "3", "4"]} at={at("4", 0, 1, 2) - 4} goal="ESPECIALISTA" size={108} />
      </Whip>
      {COURSES.map((c, i) => (
        <Whip key={c.n} from={S(i + 1)} to={S(i + 2)}>
          <LightLine from={S(i + 1)} to={S(i + 2)} />
          <Burst at={S(i + 1) + 12} />
          <Hero>
            {i === 0 && <Sismo />}
            {i === 1 && <Nave />}
            {i === 2 && <Union />}
            {i === 3 && <Planos />}
          </Hero>
          <StepCard n={c.n} kicker={`CURSO ${c.n} DE 4`} title={c.title} chips={c.chips.map((x, k) => ({ label: x[0], at: chipAt(i, k) }))} from={S(i + 1)} to={S(i + 2)} />
        </Whip>
      ))}
      <Whip from={S(5)} to={S(6)}>
        <LightLine from={S(5)} to={S(6)} />
        <Hero>
          <Acompanamiento />
        </Hero>
        <Caption txt="TUTOR IA INCLUIDO" from={S(5) + 10} to={at("sesiones", 5, 1, 2) - 6} y={capY} />
        <Caption txt="4 SESIONES 1 A 1" from={at("sesiones", 5, 1, 2) - 6} to={S(6)} y={capY} />
      </Whip>
      <Whip from={S(6)} to={S(7)}>
        <LightLine from={S(6)} to={S(7)} />
        <Burst at={S(6) + 12} />
        <Hero>
          <Certificados />
        </Hero>
        <Caption txt="CERTIFICADO DESIGN MODELING" from={S(6) + 12} to={at("autodesk", 6, 1, 2) - 6} />
        <Caption txt="+ CERTIFICADO AUTODESK" from={at("autodesk", 6, 1, 2) - 6} to={S(7)} />
      </Whip>
      <Whip from={S(7)} to={t.duration + 20}>
        <Finale at={conv} cta={cta} kicker="ESPECIALIZACIÓN" big="ACERO" sub="DISEÑO ESTRUCTURAL BIM" meta="4 CURSOS · 120 HORAS · 4 MESES" />
      </Whip>
    </Frame>
  );
};
