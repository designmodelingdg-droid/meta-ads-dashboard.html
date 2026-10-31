import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { brand } from "../brand/brand";
import { ease } from "../lib/motion";
import data from "../data/coleccion.json";
import { AppTile, Burst, Caption, Carousel, Finale, Frame, Glass, Hero, HookRow, K, LOGO, LightLine, Pop, StepCard, TextTile, Whip, clamp, makeTiming, sp, useStage } from "./kit";

// Colección Autodesk con IA: 12 cursos en 4 grupos, cada curso con clase en vivo y certificado.
const t = makeTiming(data, 45);
export const COL_DURATION = t.duration;
const { S, at } = t;

const GROUPS = [
  { n: "1", title: "AUTOMATIZACIÓN", chips: [["AUTOMATIZACIÓN EN REVIT", "herramient"], ["AI ASSISTANTS", "asistent"], ["FAMILIAS PARAMÉTRICAS", "familias"]] },
  { n: "2", title: "DATOS Y CANTIDADES", chips: [["BIM DATA DASHBOARD", "tableros"], ["PLANILLAS Y CANTIDADES", "planillas"], ["DIAGRAMAS TÉCNICOS", "diagramas"]] },
  { n: "3", title: "COLABORACIÓN Y PRESENTACIÓN", chips: [["ACC", "nube"], ["RENDER + IA", "render"], ["PRESENTACIONES", "presentaciones"]] },
  { n: "4", title: "GESTIÓN Y NORMATIVAS", chips: [["PLANTILLAS", "plantillas"], ["ROL BIM MANAGER", "manager"], ["NORMATIVAS CON IA", "normativ"]] },
] as const;
const chipAt = (g: number, i: number) => at(GROUPS[g].chips[i][1], g + 1, i, 3);

const COURSES = [
  "Automatización en Revit",
  "AI Assistants para Autodesk",
  "BIM Data Dashboard",
  "Autodesk Construction Cloud",
  "Familias Paramétricas con IA",
  "Plantillas Profesionales en Revit",
  "Renderizado Inteligente",
  "Diagramas Técnicos con IA",
  "Planillas y Cantidades",
  "IA para el BIM Manager",
  "Presentaciones Técnicas con IA",
  "Normativas con IA",
];

const Automation: React.FC = () => {
  const frame = useCurrentFrame();
  const sats = [
    { x: -270, y: -170, el: <TextTile txt="ADD-INS" w={230} h={120} size={46} />, w: 230, h: 120, a: chipAt(0, 0) },
    { x: 270, y: -170, el: <AppTile src={LOGO("openai.png")} w={140} h={140} pad={26} />, w: 140, h: 140, a: chipAt(0, 1) },
    { x: 0, y: 190, el: <Cube />, w: 220, h: 220, a: chipAt(0, 2) },
  ];
  return (
    <>
      <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
        {sats.map((s, i) => {
          const g = interpolate(frame, [s.a - 8, s.a], [0, 1], clamp);
          return <path key={i} d={`M 0 0 L ${s.x} ${s.y}`} pathLength={1} stroke={K.copperHi} strokeWidth={6} strokeDasharray="1 1" strokeDashoffset={1 - g} style={{ filter: `drop-shadow(0 0 8px ${K.copper})` }} />;
        })}
      </svg>
      <Pop at={S(1) + 12} x={0} y={0} w={190} h={190}>
        <AppTile src={LOGO("revit.png")} w={190} h={190} pad={30} />
      </Pop>
      {sats.map((s, i) => (
        <Pop key={i} at={s.a - 4} x={s.x} y={s.y} w={s.w} h={s.h}>
          {s.el}
        </Pop>
      ))}
    </>
  );
};

const Cube: React.FC = () => {
  const frame = useCurrentFrame();
  const r = frame * 1.6;
  const face = (tr: string, c: string) => <div style={{ position: "absolute", width: 120, height: 120, border: `4px solid ${c}`, background: `${c}22`, transform: tr, boxShadow: `0 0 18px ${c}66` }} />;
  return (
    <div style={{ width: 220, height: 220, perspective: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", width: 120, height: 120, transformStyle: "preserve-3d", transform: `rotateX(-24deg) rotateY(${r}deg)` }}>
        {face("translateZ(60px)", K.copperHi)}
        {face("rotateY(90deg) translateZ(60px)", K.copper)}
        {face("rotateY(180deg) translateZ(60px)", K.copperHi)}
        {face("rotateY(-90deg) translateZ(60px)", K.copper)}
        {face("rotateX(90deg) translateZ(60px)", "#FFFFFF")}
      </div>
    </div>
  );
};

const Dashboard: React.FC = () => {
  const frame = useCurrentFrame();
  const a0 = S(2) + 12;
  const p = sp(frame, a0, 15);
  const bars = [0.45, 0.7, 0.55, 0.9, 0.65, 0.8];
  const donut = interpolate(frame, [chipAt(1, 0), chipAt(1, 0) + 30], [0, 0.72], { ...clamp, easing: ease.out });
  const kpi = Math.round(interpolate(frame, [chipAt(1, 1) - 4, chipAt(1, 1) + 26], [0, 1248], clamp));
  return (
    <div style={{ position: "absolute", left: -400, top: -250, transform: `scale(${0.85 + 0.15 * p})`, opacity: Math.min(1, p * 1.5) }}>
      <Glass w={800} h={500}>
        <div style={{ position: "absolute", left: 40, top: 30, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 26, letterSpacing: 4, color: K.copperHi }}>BIM DATA DASHBOARD</div>
        {bars.map((b, i) => {
          const g = interpolate(frame, [a0 + 6 + i * 3, a0 + 24 + i * 3], [0, 1], { ...clamp, easing: ease.out });
          return <div key={i} style={{ position: "absolute", left: 50 + i * 62, bottom: 50, width: 40, height: 300 * b * g, borderRadius: 8, background: `linear-gradient(180deg, ${K.copperHi}, ${K.copper})`, boxShadow: `0 0 14px ${K.copper}88` }} />;
        })}
        <svg width={220} height={220} viewBox="0 0 100 100" style={{ position: "absolute", left: 470, top: 70 }}>
          <circle cx={50} cy={50} r={36} fill="none" stroke="rgba(255,255,255,.12)" strokeWidth={14} />
          <circle cx={50} cy={50} r={36} fill="none" stroke={K.green} strokeWidth={14} pathLength={1} strokeDasharray={`${donut} 1`} transform="rotate(-90 50 50)" />
        </svg>
        <div style={{ position: "absolute", left: 470, top: 320, width: 220, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: 72, color: K.white }}>{kpi.toLocaleString("es")}</div>
        <div style={{ position: "absolute", left: 470, top: 410, width: 220, textAlign: "center", fontFamily: brand.fontBody, fontWeight: 800, fontSize: 22, letterSpacing: 3, color: K.muted }}>m² CUANTIFICADOS</div>
      </Glass>
    </div>
  );
};

const Cloud: React.FC = () => {
  const frame = useCurrentFrame();
  const a = chipAt(2, 0) - 6;
  const pc = sp(frame, Math.min(a, S(3) + 12), 14);
  const links = [
    { x: -300, y: 170, src: "revit.png", pad: 26 },
    { x: 300, y: 170, src: "navisworks.png", pad: 10 },
  ];
  return (
    <>
      <div style={{ position: "absolute", left: -230, top: -260, transform: `scale(${0.7 + 0.3 * pc})`, opacity: Math.min(1, pc * 1.5) }}>
        <svg width={460} height={300} viewBox="0 0 460 300" style={{ filter: `drop-shadow(0 0 30px ${K.copper}88)` }}>
          <path d="M120 250 Q40 250 40 180 Q40 115 110 108 Q125 30 210 30 Q290 30 315 95 Q420 90 420 175 Q420 250 340 250 Z" fill={K.card2} stroke={K.copperHi} strokeWidth={8} />
          <text x="230" y="195" textAnchor="middle" fontFamily={brand.fontDisplay} fontSize="96" fill="#FFFFFF">
            ACC
          </text>
        </svg>
      </div>
      <svg width={2} height={2} style={{ position: "absolute", overflow: "visible" }}>
        {links.map((l, i) => {
          const g = interpolate(frame, [a + 6 + i * 4, a + 18 + i * 4], [0, 1], clamp);
          return <path key={i} d={`M ${l.x} ${l.y} Q ${l.x * 0.5} ${l.y - 40} 0 -20`} pathLength={1} fill="none" stroke={K.copperHi} strokeWidth={6} strokeDasharray="0.04 0.03" strokeDashoffset={-frame * 0.01} opacity={g} />;
        })}
      </svg>
      {links.map((l, i) => (
        <Pop key={l.src} at={a + 4 + i * 4} x={l.x} y={l.y} w={150} h={150}>
          <AppTile src={LOGO(l.src)} w={150} h={150} pad={l.pad} />
        </Pop>
      ))}
      <Pop at={chipAt(2, 1) - 4} x={0} y={210} w={300} h={190} rot={-8}>
        <div style={{ width: 300, height: 190, borderRadius: 18, overflow: "hidden", border: "5px solid #FFFFFF", boxShadow: `0 0 30px ${K.copper}88`, background: "linear-gradient(180deg,#F7B267 0%,#F4845F 45%,#2A3F66 46%,#13233F 100%)", position: "relative" }}>
          <div style={{ position: "absolute", left: 40, bottom: 0, width: 70, height: 120, background: "#0D1E3A" }} />
          <div style={{ position: "absolute", left: 120, bottom: 0, width: 110, height: 80, background: "#122546" }} />
          <div style={{ position: "absolute", left: 230, bottom: 0, width: 40, height: 140, background: "#0D1E3A" }} />
          <div style={{ position: "absolute", right: 8, top: 6, fontFamily: brand.fontBody, fontWeight: 800, fontSize: 18, color: "#FFFFFF" }}>RENDER</div>
        </div>
      </Pop>
    </>
  );
};

const Gestion: React.FC = () => {
  const items = [
    { t: "PLANTILLA", sub: "Revit", a: chipAt(3, 0) },
    { t: "BIM MANAGER", sub: "IA personal", a: chipAt(3, 1) },
    { t: "NORMATIVA", sub: "ACI 318 · NEC · E.030", a: chipAt(3, 2) },
  ];
  return (
    <>
      {items.map((it, i) => (
        <Pop key={it.t} at={Math.min(it.a - 6, S(4) + 14 + i * 6)} x={(i - 1) * 260} y={-20} w={290} h={380} rot={(i - 1) * 10}>
          <div style={{ transform: `rotate(${(i - 1) * 6}deg)` }}>
            <Glass w={290} h={380}>
              <div style={{ position: "absolute", left: 30, top: 34, right: 30 }}>
                {[0, 1, 2, 3, 4].map((k) => (
                  <div key={k} style={{ height: 14, borderRadius: 7, marginBottom: 20, width: `${[90, 70, 84, 60, 78][k]}%`, background: k === 0 ? K.copper : "rgba(255,255,255,.16)" }} />
                ))}
              </div>
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 64, textAlign: "center", fontFamily: brand.fontDisplay, fontSize: it.t.length > 9 ? 36 : 44, color: K.white }}>{it.t}</div>
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 30, textAlign: "center", fontFamily: brand.fontBody, fontWeight: 800, fontSize: 20, color: K.copperHi }}>{it.sub}</div>
            </Glass>
          </div>
        </Pop>
      ))}
    </>
  );
};

const Credenciales: React.FC = () => {
  const frame = useCurrentFrame();
  const { V, cx, cy } = useStage();
  const aH = at("15", 5, 0, 3) - 4;
  const aV = at("vivo", 5, 1, 3) - 4;
  const aC = at("certificado", 5, 2, 3) - 4;
  const hours = Math.round(interpolate(frame, [aH, aH + 20], [0, 20], clamp));
  const gap = V ? 300 : 420;
  const k = V ? 0.85 : 1;
  return (
    <div style={{ position: "absolute", left: cx, top: cy, transform: `scale(${k})` }}>
      <Pop at={aH} x={-gap} y={0} w={260} h={260}>
        <div style={{ width: 260, height: 260, borderRadius: "50%", border: `8px solid ${K.copperHi}`, background: K.card, boxShadow: `0 0 40px ${K.copper}88`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: 92, color: K.white, lineHeight: 1 }}>{hours < 15 ? hours : `15–${hours}`}</div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 28, letterSpacing: 4, color: K.copperHi }}>HORAS</div>
        </div>
      </Pop>
      <Pop at={aV} x={0} y={0} w={260} h={200}>
        <div style={{ width: 260, height: 200, borderRadius: 24, background: K.card, border: `5px solid ${K.red}`, boxShadow: `0 0 40px ${K.red}66`, display: "flex", alignItems: "center", justifyContent: "center", gap: 18 }}>
          <div style={{ width: 34, height: 34, borderRadius: "50%", background: K.red, opacity: 0.5 + 0.5 * Math.abs(Math.sin(frame / 6)), boxShadow: `0 0 20px ${K.red}` }} />
          <div style={{ fontFamily: brand.fontDisplay, fontSize: 70, color: K.white }}>EN VIVO</div>
        </div>
      </Pop>
      <Pop at={aC} x={gap} y={0} w={300} h={220} rot={8}>
        <div style={{ width: 300, height: 220, borderRadius: 14, background: "#FDFBF6", border: `6px solid ${K.copper}`, boxShadow: `0 0 40px ${K.copper}88`, position: "relative", overflow: "hidden" }}>
          <div style={{ position: "absolute", left: 18, right: 18, top: 16, height: 46, background: K.bg, borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Img src={staticFile("logo-dma.png")} style={{ height: 30 }} />
          </div>
          <div style={{ position: "absolute", left: 22, top: 80, fontFamily: brand.fontDisplay, fontSize: 34, color: K.bg }}>CERTIFICADO</div>
          {[0, 1, 2].map((r) => (
            <div key={r} style={{ position: "absolute", left: 22, top: 130 + r * 20, width: [170, 140, 110][r], height: 9, borderRadius: 5, background: "#C9CED8" }} />
          ))}
          <div style={{ position: "absolute", right: 20, bottom: 18, width: 64, height: 64, backgroundImage: `repeating-linear-gradient(0deg, ${K.bg} 0 6px, transparent 6px 12px), repeating-linear-gradient(90deg, ${K.bg} 0 6px, transparent 6px 12px)`, opacity: 0.85 }} />
        </div>
      </Pop>
    </div>
  );
};

export const Coleccion: React.FC = () => {
  const conv = S(6) + 40;
  const cta = Math.max(at("pide", 6, 1, 2) - 3, conv + 36);
  return (
    <Frame
      t={t}
      voice="rutas/voz_coleccion.wav"
      cta={cta}
      whooshes={[1, 2, 3, 4, 5, 6].map(S)}
      bongs={[1, 2, 3, 4].map((i) => S(i) + 11)}
      extra={[
        { at: at("doce", 0, 1, 2) - 3, src: "sfx/casino/chips-stack-3.ogg", vol: 0.35 },
        { at: conv + 4, src: "sfx/impact/impactBell_heavy_000.ogg", vol: 0.35 },
      ]}
    >
      <Whip from={0} to={S(1)} first>
        <HookRow kicker="¿QUÉ ES LA?" title={<>COLECCIÓN <span style={{ color: K.copperHi }}>AUTODESK + IA</span></>} labels={Array.from({ length: 12 }, (_, i) => String(i + 1))} at={at("doce", 0, 1, 2) - 3} />
      </Whip>
      {GROUPS.map((g, i) => (
        <Whip key={g.n} from={S(i + 1)} to={S(i + 2)}>
          <LightLine from={S(i + 1)} to={S(i + 2)} />
          <Burst at={S(i + 1) + 12} />
          <Hero>
            {i === 0 && <Automation />}
            {i === 1 && <Dashboard />}
            {i === 2 && <Cloud />}
            {i === 3 && <Gestion />}
          </Hero>
          <StepCard n={g.n} kicker="3 CURSOS" title={g.title} chips={g.chips.map((c, k) => ({ label: c[0], at: chipAt(i, k) }))} from={S(i + 1)} to={S(i + 2)} />
        </Whip>
      ))}
      <Whip from={S(5)} to={S(6)}>
        <LightLine from={S(5)} to={S(6)} exit={false} />
        <Burst at={S(5) + 12} />
        <Credenciales />
        <Caption txt="15 A 20 HORAS POR CURSO" from={at("15", 5, 0, 3) - 4} to={at("vivo", 5, 1, 3) - 4} />
        <Caption txt="CLASE EN VIVO" from={at("vivo", 5, 1, 3) - 4} to={at("certificado", 5, 2, 3) - 4} />
        <Caption txt="UN CERTIFICADO POR CURSO" from={at("certificado", 5, 2, 3) - 4} to={S(6)} />
      </Whip>
      <Whip from={S(6)} to={t.duration + 20}>
        <Carousel items={COURSES.map((c, i) => ({ kicker: `CURSO ${i + 1}`, title: c }))} from={S(6) - 4} converge={conv} cardW={380} />
        <Finale at={conv + 6} cta={cta} kicker="EMPIEZA POR EL QUE NECESITAS" big="COLECCIÓN" sub="AUTODESK + IA" meta="12 CURSOS · 180 A 240 HORAS" />
      </Whip>
    </Frame>
  );
};
