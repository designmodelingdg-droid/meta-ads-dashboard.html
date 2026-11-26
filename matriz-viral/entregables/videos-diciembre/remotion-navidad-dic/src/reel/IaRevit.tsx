// «IA en Revit: lo que uso según lo que necesito» · tres bandas con pantallas reales del workshop del 17-nov (recortadas: sin barras laterales ni datos privados).
// Arriba, titular fijo; al centro, la pantalla real con acercamientos; abajo, banda fija «Comenta NIVEL».
import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import T0 from "../../reels/iarevit.json";
import { BEBAS, MONT, NAVY, OR, CU, FPS, F, clamp, Bg, Logos } from "../brand";
import { Tiempos, Subs, Cierre, Escenas } from "./base";
import { Tr, Sello, Sale, loop, rect, un, RED } from "./pz";
export const T = T0 as Tiempos;
const VW = 1080, VH = 660, VY = 585;
const EIO = Easing.bezier(0.45, 0, 0.55, 1);
// instante (s, local a la escena) en que la voz dice una palabra; si no la encuentra, fracción de la escena
const at = (i: number, re: RegExp, fb: number) => { const e = T.escenas[i]; const w = T.palabras.find((q) => q.s >= e.s - 0.01 && q.s < e.s + e.dur && re.test(q.w));
  return w ? w.s - (i ? e.s : 0) : fb * e.dur; };

type Key = [number, number, number, number];   // t (s), centro x, centro y (px de la fuente), escala
const cam = (keys: Key[], t: number) => { let a = keys[0], b = keys[keys.length - 1];
  for (let i = 0; i < keys.length - 1; i++) if (t >= keys[i][0]) { a = keys[i]; b = keys[i + 1]; }
  if (t <= keys[0][0]) b = a; if (t >= keys[keys.length - 1][0]) a = b;
  const k = a === b ? 0 : interpolate(t, [a[0], b[0]], [0, 1], { ...clamp, easing: EIO });
  return [a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k, a[3] + (b[3] - a[3]) * k]; };
// Pantalla real dentro de la banda central: la cámara (centro y escala) se mueve entre claves; los hijos se dibujan en coordenadas de la fuente
const Pantalla: React.FC<{ src: string; w: number; h: number; from?: number; rate?: number; keys: Key[]; t0?: number; t1?: number; children?: (s: number) => React.ReactNode }> = ({ src, w, h, from = 0, rate = 1, keys, t0 = 0, t1 = 1e9, children }) => {
  const f = useCurrentFrame(); const t = f / FPS; if (t < t0 || t >= t1) return null;
  const [cx, cy, s] = cam(keys, t);
  const left = Math.min(0, Math.max(VW - w * s, VW / 2 - cx * s)), top = Math.min(0, Math.max(VH - h * s, VH / 2 - cy * s));
  const fl = t0 > 0 ? interpolate(t - t0, [0, 0.14], [0.85, 0], clamp) : 0;
  return (<div style={{ position: "absolute", inset: 0, overflow: "hidden", background: "#fff" }}>
    <div style={{ position: "absolute", left, top, width: w * s, height: h * s }}>
      <OffthreadVideo src={staticFile(src)} muted startFrom={Math.round(from * FPS)} playbackRate={rate} style={{ width: "100%", height: "100%" }} />
      {children && <svg viewBox={`0 0 ${w} ${h}`} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", overflow: "visible" }}>{children(s)}</svg>}
    </div>
    {fl > 0 && <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: fl }} />}
  </div>);
};
// banda central: entra deslizándose sobre la anterior
const Centro: React.FC<{ first?: boolean; children: React.ReactNode; y?: number; h?: number }> = ({ first, children, y = VY, h = VH }) => {
  const f = useCurrentFrame(); const k = first ? 1 : interpolate(f, [0, 9], [0, 1], { ...clamp, easing: EIO });
  return (<div style={{ position: "absolute", left: 0, top: y - 6, width: VW, height: h + 12, background: CU, transform: `translateX(${(1 - k) * 1080}px)`, boxShadow: "0 24px 60px rgba(0,0,0,.5)" }}>
    <div style={{ position: "absolute", left: 0, top: 6, width: VW, height: h, overflow: "hidden", background: "#fff" }}>{children}</div></div>);
};
// rótulo numerado sobre la banda central
const Rotulo: React.FC<{ n: string; text: string }> = ({ n, text }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const k = spring({ frame: f - 3, fps, config: { damping: 13 } }); const size = Math.min(62, Math.floor(880 / (text.length * 0.4)));
  return (<div style={{ position: "absolute", left: 36, right: 36, top: 474, height: 96, display: "flex", alignItems: "center", gap: 20, opacity: Math.min(1, k * 1.6), transform: `translateX(${(1 - k) * -60}px)` }}>
    <div style={{ width: 92, height: 92, borderRadius: 46, background: OR, border: "5px solid #fff", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: BEBAS, fontSize: 80, lineHeight: 1, color: "#fff", paddingTop: 8, flexShrink: 0, transform: `scale(${0.6 + 0.4 * k})` }}>{n}</div>
    <div style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 1, color: "#fff", letterSpacing: 1, paddingTop: 8, whiteSpace: "nowrap" }}>{text}</div></div>);
};
// etiqueta de herramienta (minúsculas reales: Montserrat) pegada al borde inferior de la pantalla
const Etiqueta: React.FC<{ a: string; b: string; t0: number; t1?: number }> = ({ a, b, t0, t1 = 1e9 }) => { const t = useCurrentFrame() / FPS; if (t >= t1) return null;
  return (<Sale t0={t0} style={{ position: "absolute", left: 30, top: VH - 138 }}>
    <div style={{ background: "rgba(13,30,58,.95)", borderLeft: `12px solid ${CU}`, borderRadius: 14, padding: "14px 26px 14px 22px", boxShadow: "0 12px 30px rgba(0,0,0,.35)" }}>
      <div style={{ fontFamily: MONT, fontWeight: 900, fontSize: 36, color: "#fff", lineHeight: 1.15, whiteSpace: "nowrap" }}>{a}</div>
      <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 30, color: "#F2B777", lineHeight: 1.2, whiteSpace: "nowrap" }}>{b}</div></div></Sale>);
};
// cifra grande sobre la pantalla
const Cifra: React.FC<{ text: React.ReactNode; t0: number; size?: number; y?: number }> = ({ text, t0, size = 100, y = VH - 150 }) => { const f = useCurrentFrame();
  return (<Sale t0={t0} dy={50} style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center" }}>
    <div style={{ background: OR, border: "5px solid #fff", borderRadius: 20, padding: "20px 34px 6px", fontFamily: BEBAS, fontSize: size, lineHeight: 1, color: "#fff", letterSpacing: 1, whiteSpace: "nowrap", boxShadow: "0 18px 44px rgba(0,0,0,.45)", transform: `scale(${1 + 0.02 * Math.sin(f / 5)})` }}>{text}</div></Sale>);
};
const Cabecera: React.FC = () => (<>
  <Logos y={146} h={62} />
  <div style={{ position: "absolute", left: 0, right: 0, top: 246, textAlign: "center", fontFamily: BEBAS, fontSize: 128, lineHeight: 1, color: "#fff", letterSpacing: 2 }}>IA EN REVIT:</div>
  <div style={{ position: "absolute", left: 0, right: 0, top: 366, display: "flex", justifyContent: "center" }}>
    <div style={{ background: CU, borderRadius: 12, padding: "12px 24px 2px", fontFamily: BEBAS, fontSize: 70, lineHeight: 1, color: "#fff", letterSpacing: 1, whiteSpace: "nowrap" }}>LO QUE USO SEGÚN LO QUE NECESITO</div></div></>);
const Abajo: React.FC = () => { const f = useCurrentFrame(); const k = 1 + 0.018 * Math.sin(f / 6);
  return (<div style={{ position: "absolute", left: 34, right: 34, top: 1410, height: 112, display: "flex", justifyContent: "center", alignItems: "center", gap: 18, background: NAVY, border: `5px solid ${OR}`, borderRadius: 26, transform: `scale(${k})`, boxShadow: "0 16px 40px rgba(0,0,0,.45)" }}>
    <span style={{ fontFamily: BEBAS, fontSize: 72, lineHeight: 1, color: "#fff", paddingTop: 8, letterSpacing: 1 }}>COMENTA <span style={{ color: OR }}>NIVEL</span></span>
    <svg width={70} height={46} viewBox="0 0 70 46" style={{ transform: `translateX(${4 * Math.sin(f / 4)}px)` }}><path d="M4 23 H58 M42 7 L60 23 L42 39" stroke={OR} strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
    <span style={{ fontFamily: BEBAS, fontSize: 72, lineHeight: 1, color: "#fff", paddingTop: 8, letterSpacing: 1 }}>TEST BIM GRATIS</span></div>);
};

// 0 · portada: las tres pantallas reales en mosaico
const Tarjeta: React.FC<{ src: string; x: number; y: number; w: number; h: number; i: number }> = ({ src, x, y, w, h, i }) => { const f = useCurrentFrame();
  const dy = 7 * Math.sin(f / 11 + i * 2.1), r = [-2.2, 1.8, -1.2][i] + 0.5 * Math.sin(f / 14 + i);
  return (<div style={{ position: "absolute", left: x, top: y + dy, width: w, height: h, borderRadius: 18, overflow: "hidden", border: `5px solid ${i === 1 ? OR : "#fff"}`, boxShadow: "0 22px 50px rgba(0,0,0,.55)", transform: `rotate(${r}deg) scale(${1 + 0.012 * Math.sin(f / 9 + i)})`, background: "#fff" }}>
    <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.03 * Math.sin(f / 16 + i)})` }} /></div>);
};
const Portada: React.FC = () => (<>
  <Tarjeta src="ia/p-revit.png" x={36} y={486} w={640} h={374} i={0} />
  <Tarjeta src="ia/p-claude.png" x={470} y={742} w={580} h={343} i={2} />
  <Tarjeta src="ia/p-chat.png" x={44} y={968} w={650} h={268} i={1} />
</>);

// 1 · preguntarle algo al modelo: pyRevit + servidor MCP → ChatGPT responde
const Uno: React.FC<{ d: number }> = ({ d }) => { const a = Math.min(at(1, /^conecto/i, 0.3) + 1.6, d * 0.42), b = at(1, /^lectura/i, 0.72) - 0.5; const c = b + 0.9;
  return (<><Rotulo n="1" text="SI QUIERO PREGUNTARLE ALGO AL MODELO" />
    <Centro>
      <Pantalla src="ia/mcp1.mp4" w={1920} h={1010} from={0.3} keys={[[0, 520, 300, 1.0], [a, 330, 240, 1.55]]} t1={a} />
      <Pantalla src="ia/mcp2.mp4" w={1920} h={1010} from={0.4} keys={[[a, 1000, 480, 0.9], [b, 950, 450, 1.5]]} t0={a} t1={b} />
      <Pantalla src="ia/chat.mp4" w={1340} h={820} from={1.4} keys={[[b, 670, 400, 0.85], [c + 0.5, 430, 400, 1.45], [d, 400, 420, 1.6]]} t0={b}>
        {(s) => <Tr d={loop(206, 450, 126, 56, 4)} t0={c + 0.35} dur={0.4} color={RED} w={9 / s} />}</Pantalla>
      <Etiqueta a="pyRevit + servidor MCP de código abierto" b="ChatGPT · Revit 2026" t0={Math.max(0.9, at(1, /^conecto/i, 0.3) - 0.2)} t1={c + 0.9} />
      <Cifra text="1.880 MUROS · 75 PUERTAS" t0={c + 0.9} size={92} />
    </Centro></>);
};
// 2 · leer datos sin exportar a Excel: NonicaTab AI Connector → Claude resume el archivo
const Dos: React.FC<{ d: number }> = ({ d }) => { const a = at(2, /^le$/i, 0.72) - 0.15;
  return (<><Rotulo n="2" text="SI QUIERO LEER DATOS SIN EXPORTAR A EXCEL" />
    <Centro>
      <Pantalla src="ia/nonica.mp4" w={1920} h={1010} from={3.4} keys={[[0, 1240, 400, 0.78], [1.6, 1000, 600, 1.3], [a, 960, 620, 1.5]]} t1={a} />
      <Pantalla src="ia/claude.mp4" w={900} h={940} from={0.2} rate={0.85} keys={[[a, 450, 330, 1.2], [d, 450, 420, 1.32]]} t0={a} />
      <Etiqueta a="NonicaTab AI Connector" b="Claude · Revit 2025" t0={Math.max(0.9, at(2, /^uso$/i, 0.4) - 0.1)} />
    </Centro></>);
};
// 3 · revisar antes de entregar: la línea real «Hay 3 niveles a la misma altura (8.70 m)»
const Tres: React.FC<{ d: number }> = ({ d }) => { const a = at(3, /^En$/, 0.55) - 0.1;
  return (<><Rotulo n="3" text="SI QUIERO REVISAR ANTES DE ENTREGAR" />
    <Centro>
      <Pantalla src="ia/claude.mp4" w={900} h={940} from={2.2} rate={0.36} keys={[[0, 450, 470, 1.2], [a, 450, 520, 1.3], [a + 0.7, 330, 566, 1.95], [d, 320, 566, 2.1]]}>
        {(s) => <Tr d={rect(44, 553, 474, 38, 6)} t0={a + 0.75} dur={0.5} color={RED} w={9 / s} />}</Pantalla>
      <Cifra text={un("3 NIVELES A 8,70 m")} t0={a + 1.4} size={108} />
    </Centro></>);
};
// 4 · lo que no le dejo: decidir. Pantalla real de Revit con los niveles del modelo
const NoDecide: React.FC<{ d: number }> = ({ d }) => { const a = at(4, /^decidir/i, 0.22), b = at(4, /^compruebo/i, 0.7);
  return (<>
    <Centro>
      <Pantalla src="ia/niveles.mp4" w={1920} h={1010} from={1.6} keys={[[0, 1250, 620, 0.95], [a + 0.6, 1200, 610, 1.15], [b - 0.2, 420, 600, 1.5], [d, 380, 600, 1.62]]}>
        {(s) => <Tr d={loop(175, 620, 150, 132, 8)} t0={b + 0.35} dur={0.5} color={RED} w={8 / s} />}</Pantalla>
    </Centro>
    <Sello text="LO QUE NO LE DEJO: DECIDIR" x={540} y={486} t0={Math.max(0.5, a - 0.35)} size={88} rot={-3} bg="#fff" />
    <div style={{ position: "absolute", left: 0, right: 0, top: VY }}><Cifra text="SE COMPRUEBA EN REVIT" t0={b - 0.1} size={92} /></div>
  </>);
};

export const IaRevit: React.FC = () => {
  const f = useCurrentFrame(); const E = T.escenas; const fin = F(E[5].s) + 8;
  return (<AbsoluteFill style={{ background: NAVY }}>
    <Bg />
    <Cabecera />
    <Abajo />
    <Escenas T={T}>{[
      <Portada />, <Uno d={E[1].dur} />, <Dos d={E[2].dur} />, <Tres d={E[3].dur} />, <NoDecide d={E[4].dur} />,
      <Cierre titulo="¿CUÁL USAS TÚ?" fila opciones={[["1", ""], ["2", ""], ["3", ""]]} pie="NINGUNA TODAVÍA" boton="COMENTA «NIVEL»" segunda="MÁS INFORMACIÓN DEL MÁSTER → COMENTA MÁSTER" />,
    ]}</Escenas>
    <Subs T={T} y={f < fin ? 1262 : 1396} />
  </AbsoluteFill>);
};
