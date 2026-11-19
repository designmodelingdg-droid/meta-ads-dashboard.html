import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { brand } from "../brand/brand";
import { ease } from "../lib/motion";
import data from "../data/espec.json";
import { AppTile, Burst, Carousel, Finale, Frame, Glass, Hero, HookRow, K, LOGO, LightLine, Pop, StepCard, TextTile, Whip, clamp, makeTiming, sp } from "./kit";

// Especializaciones: de 2 a 4 cursos encadenados sobre un software o un tipo de estructura.
const t = makeTiming(data, 30);
export const ESP_DURATION = t.duration;
const { S, at } = t;

const STEPS = [
  { n: "1", kicker: "UN ENFOQUE", title: "SOFTWARE O ESTRUCTURA", chips: [["ACERO", "acero"], ["HORMIGÓN ARMADO", "hormig"], ["CIMENTACIONES", "ciment"], ["TANQUES", "tanque"]] },
  { n: "2", kicker: "CURSO POR CURSO", title: "EN EL ORDEN QUE CONVIENE", chips: [["EN ORDEN", "orden"], ["2 A 4 MESES", "meses"]] },
  { n: "3", kicker: "POR EJEMPLO", title: "DISEÑO ESTRUCTURAL BIM EN ACERO", chips: [["REVIT", "revit"], ["ROBOT", "robot"], ["ADVANCE STEEL", "advance"], ["TUTOR IA", "tutor"]] },
  { n: "4", kicker: "AL TERMINAR", title: "CERTIFICACIÓN INTERNACIONAL", chips: [["AVAL DESIGN MODELING", "certific"], ["QR DE VERIFICACIÓN", "qr"]] },
] as const;
const chipAt = (s: number, i: number) => at(STEPS[s].chips[i][1], s + 1, i, STEPS[s].chips.length);

const NINE = [
  "Diseño Estructural BIM en Acero",
  "Hormigón Armado BIM",
  "Diseño y Análisis de Cimentaciones",
  "Diseño Estructural BIM de Tanques",
  "Diseño y Análisis en ETABS",
  "Diseño y Análisis en SAP2000",
  "Modelado BIM Arquitectura y MEP",
  "Planos BIM Arquitectónicos y Estructurales",
  "Costos, Presupuesto y Control de Obras",
];

/** Una viga I, un pilar de hormigón, una zapata y un tanque: los tipos de estructura. */
const Estructuras: React.FC = () => {
  const items = [
    { t: "ACERO", x: -170, y: -150, art: <Viga /> },
    { t: "HORMIGÓN", x: 170, y: -150, art: <Pilar /> },
    { t: "CIMENTACIÓN", x: -170, y: 170, art: <Zapata /> },
    { t: "TANQUES", x: 170, y: 170, art: <Tanque /> },
  ];
  return (
    <>
      {items.map((it, i) => (
        <Pop key={it.t} at={chipAt(0, i) - 4} x={it.x} y={it.y} w={300} h={290}>
          <Glass w={300} h={290}>
            <div style={{ position: "absolute", left: 0, right: 0, top: 22, height: 180, display: "flex", alignItems: "center", justifyContent: "center" }}>{it.art}</div>
            <div style={{ position: "absolute", left: 0, right: 0, bottom: 24, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: 44, color: K.white }}>{it.t}</div>
          </Glass>
        </Pop>
      ))}
    </>
  );
};
const stroke = { fill: "none", stroke: K.copperHi, strokeWidth: 6, strokeLinejoin: "round" as const };
const Viga = () => (
  <svg width={170} height={150} viewBox="0 0 170 150">
    <path d="M30 30 H140 V46 H94 V104 H140 V120 H30 V104 H76 V46 H30 Z" {...stroke} fill={`${K.copper}33`} />
  </svg>
);
const Pilar = () => (
  <svg width={170} height={150} viewBox="0 0 170 150">
    <rect x={60} y={14} width={50} height={124} {...stroke} fill="rgba(255,255,255,.08)" />
    {[0, 1, 2, 3, 4].map((k) => (
      <line key={k} x1={60} x2={110} y1={30 + k * 24} y2={30 + k * 24} stroke={K.copper} strokeWidth={3} />
    ))}
  </svg>
);
const Zapata = () => (
  <svg width={170} height={150} viewBox="0 0 170 150">
    <rect x={72} y={14} width={26} height={70} {...stroke} />
    <path d="M30 84 H140 V122 H30 Z" {...stroke} fill={`${K.copper}33`} />
    <path d="M10 136 H160" stroke={K.muted} strokeWidth={4} strokeDasharray="8 8" />
  </svg>
);
const Tanque = () => (
  <svg width={170} height={150} viewBox="0 0 170 150">
    <path d="M30 24 V122 H140 V24" {...stroke} />
    <path d="M36 70 Q60 62 85 70 T134 70 V116 H36 Z" fill="#3B9EFF66" />
  </svg>
);

const Cadena: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(2) + 12;
  const tMes = chipAt(1, 1);
  const xs = [-330, -110, 110, 330];
  return (
    <>
      <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
        <path d={`M ${xs[0]} -40 L ${xs[3]} -40`} stroke="#2B3E63" strokeWidth={16} strokeDasharray="2 30" strokeLinecap="round" />
        <path d={`M ${xs[0]} -40 L ${xs[3]} -40`} pathLength={1} stroke={K.copperHi} strokeWidth={14} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - interpolate(frame, [a, a + 60], [0, 1], { ...clamp, easing: ease.inOut })} style={{ filter: `drop-shadow(0 0 12px ${K.copper})` }} />
      </svg>
      {xs.map((x, i) => {
        const on = frame >= a + i * 20;
        const p = sp(frame, a + i * 20, 12);
        return (
          <div key={i} style={{ position: "absolute", left: x - 80, top: -120, width: 160, height: 174, transform: `scale(${1 + 0.12 * Math.sin(Math.PI * Math.min(1, p))})` }}>
            <div style={{ position: "absolute", left: 0, top: 14, width: 160, height: 160, borderRadius: "50%", background: on ? "#8E5219" : "#16243F" }} />
            <div
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                width: 160,
                height: 160,
                borderRadius: "50%",
                background: on ? `radial-gradient(circle at 38% 30%, #FFD09A 0%, ${K.copperHi} 30%, ${K.copper} 75%)` : "radial-gradient(circle at 38% 30%, #3A5080 0%, #2B3E63 60%)",
                boxShadow: on ? `0 0 50px ${K.copper}AA` : "none",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                color: on ? K.white : "#6F82A6",
              }}
            >
              <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 22, letterSpacing: 3 }}>CURSO</div>
              <div style={{ fontFamily: brand.fontDisplay, fontSize: 80, lineHeight: 1 }}>{i + 1}</div>
            </div>
          </div>
        );
      })}
      <Pop at={tMes - 4} x={0} y={170} w={420} h={130}>
        <TextTile txt="2 A 4 MESES" w={420} h={130} size={76} />
      </Pop>
    </>
  );
};

const Acero: React.FC = () => {
  const logos = [
    { src: "revit.png", pad: 30, x: -330 },
    { src: "robot.png", pad: 10, x: -110 },
    { src: "advance.png", pad: 10, x: 110 },
  ];
  const tTutor = chipAt(2, 3) - 4;
  return (
    <>
      {logos.map((l, i) => (
        <Pop key={l.src} at={chipAt(2, i) - 6} x={l.x} y={-60} w={190} h={190}>
          <AppTile src={LOGO(l.src)} w={190} h={190} pad={l.pad} />
        </Pop>
      ))}
      <Pop at={tTutor} x={330} y={-60} w={190} h={190}>
        <Glass w={190} h={190} style={{ borderRadius: 40 }}>
          <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: K.white }}>
            <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 26, letterSpacing: 3, color: K.copperHi }}>TUTOR</div>
            <div style={{ fontFamily: brand.fontDisplay, fontSize: 96, lineHeight: 1, textShadow: `0 0 26px ${K.copper}` }}>IA</div>
          </div>
        </Glass>
      </Pop>
      <Pop at={S(3) + 14} x={0} y={150} w={520} h={110}>
        <div style={{ width: 520, height: 110, borderRadius: 999, border: `4px solid ${K.copper}`, background: K.card, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: brand.fontDisplay, fontSize: 56, color: K.white, boxShadow: `0 0 30px ${K.copper}55` }}>
          4 MESES · 120 HORAS
        </div>
      </Pop>
    </>
  );
};

const Certificado: React.FC = () => {
  const frame = useCurrentFrame();
  const a = S(4) + 12;
  const tQR = chipAt(3, 1) - 6;
  const scan = interpolate(frame, [tQR, tQR + 24], [0, 1], clamp);
  return (
    <>
      <Pop at={a} x={-60} y={-20} w={560} h={390} rot={-6}>
        <div style={{ width: 560, height: 390, borderRadius: 18, background: "#FDFBF6", border: `7px solid ${K.copper}`, boxShadow: `0 0 50px ${K.copper}88`, position: "relative", overflow: "hidden" }}>
          <div style={{ position: "absolute", left: 26, right: 26, top: 24, height: 76, background: K.bg, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Img src={staticFile("logo-dma.png")} style={{ height: 50 }} />
          </div>
          <div style={{ position: "absolute", left: 34, top: 126, fontFamily: brand.fontDisplay, fontSize: 52, color: K.bg }}>CERTIFICACIÓN</div>
          <div style={{ position: "absolute", left: 34, top: 186, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 24, letterSpacing: 4, color: K.copper }}>INTERNACIONAL</div>
          {[0, 1, 2].map((r) => (
            <div key={r} style={{ position: "absolute", left: 34, top: 250 + r * 28, width: [300, 250, 200][r], height: 12, borderRadius: 6, background: "#C9CED8" }} />
          ))}
          <div style={{ position: "absolute", right: 34, bottom: 30, width: 120, height: 120 }}>
            <svg width={120} height={120} viewBox="0 0 12 12">
              {Array.from({ length: 144 }, (_, k) => {
                const x = k % 12;
                const y = Math.floor(k / 12);
                const finder = (x < 3 && y < 3) || (x > 8 && y < 3) || (x < 3 && y > 8);
                const on = finder ? !(x % 9 === 1 && y % 9 === 1) : (x * 7 + y * 13 + x * y) % 3 === 0;
                return on ? <rect key={k} x={x} y={y} width={1} height={1} fill={K.bg} /> : null;
              })}
            </svg>
            {scan > 0 && scan < 1 && <div style={{ position: "absolute", left: -6, right: -6, top: scan * 120, height: 5, background: K.green, boxShadow: `0 0 16px ${K.green}` }} />}
          </div>
        </div>
      </Pop>
      <Pop at={tQR + 22} x={270} y={-200} w={130} h={130}>
        <div style={{ width: 130, height: 130, borderRadius: "50%", background: K.green, boxShadow: `0 0 40px ${K.green}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: brand.fontBody, fontWeight: 800, fontSize: 72, color: K.white }}>✓</div>
      </Pop>
    </>
  );
};

export const Especializaciones: React.FC = () => {
  const conv = at("elige", 5, 0, 2) - 6;
  const cta = Math.max(at("pide", 5, 1, 2) - 3, conv + 42);
  return (
    <Frame
      t={t}
      voice="rutas/voz_espec.wav"
      cta={cta}
      whooshes={[1, 2, 3, 4, 5].map(S)}
      bongs={[1, 2, 3, 4].map((i) => S(i) + 11)}
      extra={[
        { at: at("encaden", 0, 1, 2) - 3, src: "sfx/casino/chips-stack-3.ogg", vol: 0.35 },
        { at: conv + 4, src: "sfx/impact/impactBell_heavy_000.ogg", vol: 0.35 },
      ]}
    >
      <Whip from={0} to={S(1)} first>
        <HookRow kicker="¿CÓMO FUNCIONAN LAS?" title={<span style={{ color: K.copperHi }}>ESPECIALIZACIONES</span>} labels={["1", "2", "3", "4"]} at={at("encaden", 0, 1, 2) - 8} goal="ESPECIALISTA" />
      </Whip>
      {STEPS.map((s, i) => (
        <Whip key={s.n} from={S(i + 1)} to={S(i + 2)}>
          <LightLine from={S(i + 1)} to={S(i + 2)} />
          <Burst at={S(i + 1) + 12} />
          <Hero>
            {i === 0 && <Estructuras />}
            {i === 1 && <Cadena />}
            {i === 2 && <Acero />}
            {i === 3 && <Certificado />}
          </Hero>
          <StepCard n={s.n} kicker={s.kicker} title={s.title} chips={s.chips.map((c, k) => ({ label: c[0], at: chipAt(i, k) }))} from={S(i + 1)} to={S(i + 2)} />
        </Whip>
      ))}
      <Whip from={S(5)} to={t.duration + 20}>
        <Carousel items={NINE.map((c, i) => ({ kicker: `ESPECIALIZACIÓN ${i + 1}`, title: c }))} from={S(5) - 4} converge={conv} cardW={400} />
        <Finale at={conv + 6} cta={cta} kicker="ELIGE LA TUYA" big="9" sub="ESPECIALIZACIONES" meta="2 A 4 CURSOS · 80 A 135 HORAS" />
      </Whip>
    </Frame>
  );
};
