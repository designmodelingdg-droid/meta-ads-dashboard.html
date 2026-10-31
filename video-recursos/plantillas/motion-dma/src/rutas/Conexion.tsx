import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand/brand";
import { ease, progress } from "../lib/motion";
// Kit isométrico de Anatomy (MIT, github.com/wheresryan22/anatomy): cámara, sólidos y sombreado.
import * as I from "../anatomy/iso-kit.mjs";
import * as G from "../anatomy/lathe.mjs";
import data from "../data/conexion.json";
import { Frame, K, Whip, clamp, makeTiming, sp, useStage } from "./kit";

// Prueba «Anatomy en video»: una conexión viga-columna a momento que se desarma y se arma
// pieza por pieza, sincronizada con la voz de Gabriel.
const t = makeTiming(data, 50);
export const CONEXION_DURATION = t.duration;
const { S, at } = t;

type P3 = [number, number, number];
type Group = "col" | "stiff" | "beam" | "bolt";
type Part = { id: string; group: Group; center: P3; svg: string; lit: string; idx?: number };
type Proj = { origin: [number, number]; scale: number; azimuth?: number; elevation?: number };

const EXPLODE: Record<Group, P3> = { col: [0, 0, 0], stiff: [0, 300, 0], beam: [330, 0, 0], bolt: [520, 0, 0] };

/** Toda la geometría en coordenadas de mundo (z hacia arriba), construida una vez por proyección. */
const buildParts = (P: Proj): Part[] => {
  const parts: Part[] = [];
  const solid = (paths: unknown, lit: boolean) => I.solidSvg(paths, { lit, tone: "hi", crease: "faint" });
  const add = (id: string, group: Group, center: P3, paths: unknown, idx?: number) =>
    parts.push({ id, group, center, svg: solid(paths, false), lit: solid(paths, true), idx });

  // Columna W: perfil I con las alas perpendiculares a x (la viga llega por +x).
  const bf = 100, d = 110, tf = 18, tw = 7;
  const ring: [number, number][] = [
    [-d, -bf], [-d + tf, -bf], [-d + tf, -tw], [d - tf, -tw], [d - tf, -bf], [d, -bf],
    [d, bf], [d - tf, bf], [d - tf, tw], [-d + tf, tw], [-d + tf, bf], [-d, bf],
  ];
  add("columna", "col", [0, 0, 380], I.extrude(ring, 0, 760, P, { convex: false, bevel: 0.6 }));

  // Placas de continuidad, del lado visible (+y), a la altura de las alas de la viga.
  for (const z of [270, 554]) add(`rig-${z}`, "stiff", [0, 54, z], I.slabOf({ x: -d + tf, y: tw, w: 2 * (d - tf), d: bf - tw - 4, r: 0 }, z, 16, P, 2));

  // Viga W con su placa extrema soldada (un solo grupo).
  const x0 = d + 25;
  add("placa", "beam", [d + 12, 0, 420], I.slabOf({ x: d, y: -110, w: 25, d: 220, r: 0 }, 220, 400, P, 2, 0.6));
  add("ala-inf", "beam", [x0 + 260, 0, 278], I.slabOf({ x: x0, y: -80, w: 520, d: 160, r: 0 }, 270, 16, P, 2));
  add("alma", "beam", [x0 + 260, 0, 420], I.slabOf({ x: x0, y: -5, w: 520, d: 10, r: 0 }, 286, 268, P, 2));
  add("ala-sup", "beam", [x0 + 260, 0, 562], I.slabOf({ x: x0, y: -80, w: 520, d: 160, r: 0 }, 554, 16, P, 2, 0.6));

  // 8 pernos de cabeza hexagonal a lo largo de x.
  const hex: [number, number][] = Array.from({ length: 6 }, (_, k) => [17 * Math.cos((k * Math.PI) / 3 + Math.PI / 6), 17 * Math.sin((k * Math.PI) / 3 + Math.PI / 6)]);
  let k = 0;
  for (const z of [245, 310, 530, 595]) {
    for (const y of [-55, 55]) {
      const F = G.frameAlong([x0, y, z], [1, 0, 0]);
      const shank = I.solidSvg(G.disc(-48, 0, 9, F, P), { tone: "hi", crease: "faint" });
      const shankLit = I.solidSvg(G.disc(-48, 0, 9, F, P), { tone: "hi", crease: "faint", lit: true });
      const head = G.prismOf(F, hex, 0, 13, P);
      parts.push({ id: `perno-${k}`, group: "bolt", center: [x0 + 6, y, z], svg: shank + solid(head, false), lit: shankLit + solid(head, true), idx: k });
      k++;
    }
  }
  return parts;
};

/** Puntos extremos (armado y desarmado) para encuadrar la cámara. */
const EXTENT: P3[] = [
  ...(I.boxCorners({ x: -110, y: -100, w: 220, d: 200 }, 0, 760) as P3[]),
  [110 + 25 + 520 + 330, -80, 270],
  [110 + 25 + 520 + 330, 80, 570],
  [135 + 520, 100, 700],
  [0, 100 + 300, 270],
  [135 + 520, -110, 220],
];

// ── Línea de tiempo (anclada a la voz) ──────────────────────────────────────
const T_EXPLODE = S(0) + 30;
const T_COL = S(1) + 4;
const T_STIFF = at("continuidad", 1, 1, 2) - 4;
const T_BEAM = S(2) + 4;
const T_BEAM_IN = at("placa", 2, 1, 2) - 4;
const T_BOLT = S(3) + 4;
const T_BOLT_IN = at("ocho", 3, 0, 2);

const offsetOf = (p: Part, frame: number): P3 => {
  const e = interpolate(frame, [T_EXPLODE, T_EXPLODE + 26], [0, 1], { ...clamp, easing: ease.inOut });
  let back = 0;
  if (p.group === "stiff") back = interpolate(frame, [T_STIFF, T_STIFF + 20], [0, 1], { ...clamp, easing: ease.inOut });
  if (p.group === "beam") back = interpolate(frame, [T_BEAM_IN, T_BEAM_IN + 24], [0, 1], { ...clamp, easing: ease.inOut });
  if (p.group === "bolt") {
    const a = T_BOLT_IN + (p.idx ?? 0) * 4;
    back = interpolate(frame, [a, a + 14], [0, 1], { ...clamp, easing: ease.out });
  }
  const k = e * (1 - back);
  const v = EXPLODE[p.group];
  return [v[0] * k, v[1] * k, v[2] * k];
};

const isLit = (p: Part, frame: number) => {
  if (p.group === "col" || p.group === "stiff") return frame >= T_COL && frame < T_BEAM;
  if (p.group === "beam") return frame >= T_BEAM && frame < T_BOLT;
  if (p.group === "bolt") return frame >= T_BOLT && frame < t.duration - 55;
  return false;
};

const ISO_DMA = `
.iso{--anatomy-paper:#132648;--anatomy-face:#1B3560;--anatomy-top:#244274;
--anatomy-shade-0:#0F1F3B;--anatomy-shade-1:#142A4E;--anatomy-shade-2:#19335E;--anatomy-shade-3:#1F3C6C;
--anatomy-lit-top:#F2A95C;--anatomy-lit-shade:#B8681F;--anatomy-lit:#FFE3BF;
--anatomy-hi:#DCE6F5;--anatomy-mid:#9FB0CC;--anatomy-lo:#5C719A;--anatomy-faint:#3A5582;
--anatomy-weight:2.2px;}
.iso-solid[data-lit]>.iso-fill{fill:#C97A2A}
`;

const Label: React.FC<{ txt: string; anchor: P3; dx: number; dy: number; from: number; to: number; P: Proj; ox: number; oy: number; off?: P3 }> = ({ txt, anchor, dx, dy, from, to, P, ox, oy, off = [0, 0, 0] }) => {
  const frame = useCurrentFrame();
  const pin = progress(frame, from, 10);
  const pout = progress(frame, to - 6, 6, ease.in);
  const op = pin * (1 - pout);
  if (op <= 0) return null;
  const [ax, ay] = I.iso([anchor[0] + off[0], anchor[1] + off[1], anchor[2] + off[2]], P) as [number, number];
  const x = ox + ax;
  const y = oy + ay;
  return (
    <>
      <svg style={{ position: "absolute", inset: 0, overflow: "visible" }} width="100%" height="100%">
        <line x1={x} y1={y} x2={x + dx * pin} y2={y + dy * pin} stroke={K.copperHi} strokeWidth={3} opacity={op} />
        <circle cx={x} cy={y} r={8} fill={K.copperHi} opacity={op} />
      </svg>
      <div
        style={{
          position: "absolute",
          left: x + dx + (dx >= 0 ? 12 : -12),
          top: y + dy - 26,
          transform: dx >= 0 ? "none" : "translateX(-100%)",
          padding: "10px 18px 6px",
          borderRadius: 10,
          background: "rgba(13,30,58,.92)",
          border: `3px solid ${K.copper}`,
          fontFamily: brand.fontBody,
          fontWeight: 800,
          fontSize: 30,
          letterSpacing: 2,
          color: K.white,
          whiteSpace: "nowrap",
          opacity: op,
        }}
      >
        {txt}
      </div>
    </>
  );
};

export const Conexion: React.FC = () => {
  const frame = useCurrentFrame();
  const { H, V } = useStage();
  const region = V ? { x: 40, y: 700, w: 1000, h: 860 } : { x: 760, y: 140, w: 1120, h: 900 };
  const P = React.useMemo(() => I.fitProjection(EXTENT, region.w, region.h, { pad: 20 }) as Proj, [region.w, region.h]);
  const parts = React.useMemo(() => buildParts(P), [P]);

  const placed = parts
    .map((p) => {
      const off = offsetOf(p, frame);
      const c: P3 = [p.center[0] + off[0], p.center[1] + off[1], p.center[2] + off[2]];
      return { p, off, depth: I.depthOf(c, P) as number };
    })
    .sort((a, b) => a.depth - b.depth);

  const body = placed.map(({ p, off }) => `<g transform="${I.translateAlong(P, off)}">${isLit(p, frame) ? p.lit : p.svg}</g>`).join("");
  const tIn = 1;
  const titleOut = progress(frame, T_COL - 8, 8, ease.in);
  const pEnd = progress(frame, t.duration - 55, 12);

  return (
    <Frame t={t} voice="rutas/voz_conexion.wav" cta={t.duration + 99} whooshes={[T_EXPLODE, T_BEAM_IN, T_BOLT_IN]} bongs={[T_COL, T_BEAM, T_BOLT]}>
      <Whip from={0} to={t.duration + 20} first>
        <AbsoluteFill className="iso">
          <style>{I.ISO_CSS + ISO_DMA}</style>
          <svg className="iso-svg" style={{ position: "absolute", left: region.x, top: region.y, width: region.w, height: region.h }} viewBox={`0 0 ${region.w} ${region.h}`} dangerouslySetInnerHTML={{ __html: body }} />
        </AbsoluteFill>
        <div style={{ position: "absolute", left: V ? 30 : 90, right: V ? 30 : 1100, top: H * (V ? 0.2 : 0.3), textAlign: V ? "center" : "left", opacity: tIn * (1 - titleOut) + pEnd }}>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 34, letterSpacing: 9, color: K.copperHi }}>{pEnd > 0.5 ? "ACERO ESTRUCTURAL" : "ASÍ SE ARMA UNA"}</div>
          <div style={{ fontFamily: brand.fontDisplay, fontSize: V ? 118 : 104, color: K.white, lineHeight: 1, textShadow: `0 0 40px ${K.copper}88` }}>
            CONEXIÓN<br /><span style={{ color: K.copperHi }}>VIGA–COLUMNA</span>
          </div>
          <div style={{ fontFamily: brand.fontBody, fontWeight: 800, fontSize: 34, letterSpacing: 5, color: K.muted, marginTop: 10 }}>A MOMENTO · PLACA EXTREMA</div>
        </div>
        <Label txt="COLUMNA W" anchor={[-110, -100, 700]} dx={V ? -10 : -120} dy={-90} from={T_COL} to={T_BEAM} P={P} ox={region.x} oy={region.y} />
        <Label txt="PLACAS DE CONTINUIDAD" anchor={[0, 96, 562]} dx={V ? 40 : 160} dy={-120} from={T_STIFF} to={T_BEAM} P={P} ox={region.x} oy={region.y} off={offsetOf(parts.find((p) => p.group === "stiff") as Part, frame)} />
        <Label txt="VIGA W" anchor={[480, 80, 570]} dx={V ? -40 : 80} dy={-110} from={T_BEAM} to={T_BOLT} P={P} ox={region.x} oy={region.y} off={offsetOf(parts.find((p) => p.group === "beam") as Part, frame)} />
        <Label txt="PLACA EXTREMA SOLDADA" anchor={[123, -110, 620]} dx={V ? 60 : -140} dy={-120} from={T_BEAM_IN} to={T_BOLT} P={P} ox={region.x} oy={region.y} off={offsetOf(parts.find((p) => p.group === "beam") as Part, frame)} />
        <Label txt="8 PERNOS DE ALTA RESISTENCIA" anchor={[148, 55, 595]} dx={V ? 30 : 140} dy={-140} from={T_BOLT} to={t.duration - 55} P={P} ox={region.x} oy={region.y} off={offsetOf(parts.find((p) => p.group === "bolt") as Part, frame)} />
      </Whip>
    </Frame>
  );
};
