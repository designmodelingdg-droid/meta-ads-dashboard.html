// Guion en pantalla de los tres reels de Navidad. Promo: 40 cursos a $46.50 (antes $154.99, 70 % OFF),
// pregrabados, 1 mes de acceso en el nuevo campus, certificado de Design Modeling DG S.A.S.,
// hasta el martes 5 de enero 23:59 (Ecuador). CTA: Comenta NAVIDAD.
import type { NavProps, Scene } from "./Nav";

const incluye = (kicker: string): Scene => ({
  bars: 3, type: "list", kicker, title: "Esto te", accent: "llevas",
  say: "Eliges entre 40 cursos pregrabados, con 1 mes de acceso y certificado.",
  items: [
    { t: "40 cursos para elegir", tag: "BIM con IA aplicada e ingeniería estructural" },
    { t: "Curso pregrabado", tag: "Lo ves a tu ritmo, cuando quieras" },
    { t: "1 mes de acceso", tag: "En el nuevo campus" },
    { t: "Certificado al terminar", tag: "De Design Modeling DG S.A.S." },
  ],
});
const precio = (kicker: string): Scene => ({
  bars: 2, type: "price", kicker, title: "Cada curso", accent: "a $46.50", small: "ANTES", big: "$46.50", foot: "40 cursos para elegir",
  say: "Cada curso baja de $154.99 a $46.50.",
});
const cierra = (kicker: string): Scene => ({
  bars: 2, type: "deadline", kicker, title: "Solo hasta el", accent: "martes 5 de enero", small: "CIERRA A LAS", big: "23:59", foot: "hora de Ecuador",
  say: "Solo hasta el martes 5 de enero, a las 23:59.",
});
const cta = (kicker: string, title: string, accent: string): Scene => ({
  bars: 2, type: "cta", kicker, title, accent, button: "COMENTA NAVIDAD", foot: "HASTA EL MARTES 5 DE ENERO · 23:59", small: "Hora de Ecuador · Antes $154.99, ahora $46.50",
  say: "Comenta NAVIDAD y te mandamos los 40 cursos.",
});

export const NAVS: Record<string, NavProps> = {
  papeles: {
    scenes: [
      { bars: 2, type: "clip", say: "", src: "nav/c11.mp4", rate: 1.25, z: [1.22, 1.3], origin: "50% 100%", punch: [2.25],
        low: [{ y: 1150, kicker: "POV", lines: [{ t: "LOS JEFES SE FUERON", at: 0 }, { t: "DE VACACIONES", kind: "or", at: 0 }] },
          { y: 1210, lines: [{ t: "Y EL EQUIPO", at: 2.25 }, { t: "QUEDÓ A CARGO", kind: "or", at: 2.4 }] }] },
      { bars: 2, type: "clip", say: "", src: "nav/c12.mp4", logo: false, rate: 1.4, z: [1.18, 1.26], origin: "50% 100%", punch: [1.75],
        low: [{ y: 1150, kicker: "¿Y QUÉ HICIMOS?", lines: [{ t: "DEJAR LA PROMO", at: 0.1 }, { t: "ENCENDIDA", kind: "or", at: 0.25 }] },
          { y: 1210, lines: [{ t: "SHHH…", at: 1.75 }, { t: "QUE NO SE ENTEREN", kind: "or", at: 1.9 }] }] },
      precio("LA TRAVESURA DEL EQUIPO"), incluye("¿QUÉ INCLUYE?"), cierra("ANTES DE QUE VUELVAN LOS JEFES"),
      cta("¿CUÁL TE LLEVAS?", "Te mandamos", "los 40 cursos"),
    ],
  },
  regalo: {
    bg: "nav/i2.jpg",
    scenes: [
      { bars: 2, type: "clip", say: "", src: "nav/c21.mp4", rate: 1.25, z: [1.0, 1.1], origin: "50% 64%", punch: [2.25],
        top: { y: 250, kicker: "ESTA NAVIDAD", chrome: ["TENEMOS UN REGALO", "PARA TI"], size: 126 },
        low: [{ y: 1290, lines: [{ t: "DE PARTE DEL EQUIPO", at: 2.25, size: 92 }, { t: "(LOS JEFES NO SABEN)", kind: "or", at: 2.45, size: 92 }] }] },
      { bars: 2, type: "clip", say: "", src: "nav/c22.mp4", rate: 1.4, z: [1.0, 1.12], origin: "60% 45%", punch: [1.75],
        top: { y: 250, kicker: "ADENTRO HAY", chrome: ["40 CURSOS"], size: 190 },
        chips: [{ t: "BIM CON IA APLICADA", at: 0.9, x: 540, y: 1370 }, { t: "INGENIERÍA ESTRUCTURAL", at: 1.75, x: 540, y: 1470, dark: false }] },
      precio("TU REGALO DE NAVIDAD"), incluye("DENTRO DE LA CAJA"), cierra("EL REGALO TIENE FECHA"),
      cta("¿LO QUIERES?", "Pídelo", "por mensaje"),
    ],
  },
  escondido: {
    bg: "nav/i5.jpg",
    scenes: [
      { bars: 2, type: "clip", say: "", src: "nav/c31.mp4", rate: 1.25, z: [1.0, 1.1], origin: "50% 80%", punch: [2.25],
        top: { y: 250, lines: [{ t: "CUANDO ESCUCHAS QUE", at: 0, size: 92 }, { t: "VUELVEN LOS JEFES…", kind: "or", at: 0, size: 104 }] },
        stamp: { t: "¡ESCONDE LA PROMO!", at: 2.25, y: 880 } },
      { bars: 2, type: "cal", say: "", kicker: "MALAS NOTICIAS", title: "Vuelven el", accent: "6 de enero" },
      { bars: 2, type: "clip", say: "", src: "nav/i5.jpg", z: [1.04, 1.2], origin: "42% 78%", punch: [1.75],
        top: { y: 250, lines: [{ t: "HASTA ENTONCES:", at: 0.1, size: 92 }, { t: "CADA CURSO A $46.50", kind: "or", at: 0.3, size: 104 }] },
        chips: [{ t: "ANTES $154.99", at: 1.0, x: 330, y: 640 }, { t: "70 % OFF", at: 1.75, x: 760, y: 640, dark: false }] },
      incluye("¿QUÉ INCLUYE?"),
      cta("ANTES DE QUE VUELVAN", "Te mandamos", "los 40 cursos"),
    ],
  },
};
