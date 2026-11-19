/*
 * GUION del reel · lo único que se cambia para cada crudo nuevo.
 * Tiempos en segundos sobre el video editado (words.json de Whisper da los tiempos exactos).
 *
 * capa "detras" = entre el fondo y Gabriel (necesita public/<base>_alfa.webm de matte.py)
 * capa "delante" = encima de todo
 * v: "cobre" (palabra principal) · "navy" (palabra de apoyo) · "blanco" (sobre fondo navy)
 */
export type Cromo = { tipo: "cromo"; txt: string; t0: number; t1: number; y: number; size: number; x?: number; v?: "cobre" | "navy" | "blanco"; capa?: "detras" | "delante" };
export type Chicas = { tipo: "chicas"; words: [string, number][]; t1: number; y: number; size?: number; x?: number };
export type Icono = { tipo: "icono"; g: "pregunta" | "foco" | "codigo" | "archivo" | "flecha" | "check" | "grafica" | "dinero"; t0: number; t1: number; x: number; y: number; size?: number; num?: string; rebote?: boolean };
export type Anillo = { tipo: "anillo"; t0: number; t1: number; x: number; y: number; dur?: number };
export type Elemento = Cromo | Chicas | Icono | Anillo;

export type Guion = {
  video: string;            // en public/, editado y con voz
  alfa: string;             // en public/, WebM con alfa del mismo video (matte.py)
  total: number;            // duración en s
  portada: { arriba: string; abajo: string; chip: string };   // fotograma 0 (dentro del 3:4)
  portadaHasta: number;
  golpes: { t: number; fuerza?: number }[];                    // golpe de zoom + temblor
  empujes: { t: number; escala: number }[];                    // zoom que se queda hasta el siguiente corte
  zoomFuera: number[];                                         // empieza en 1.2 y abre a 1.0
  whips: number[];                                             // zoom con desenfoque + destello blanco
  estudio?: { in: number; out: number; elementos: Elemento[] }; // cortina de puntos → fondo navy de estudio
  destellos: number[];                                         // destello cobre
  elementos: Elemento[];
};

export const GUION: Guion = {
  video: "gabriel_editado.mp4",
  alfa: "gabriel_alfa.webm",
  total: 14.1,
  portada: { arriba: "5 SCRIPTS", abajo: "DE DYNAMO", chip: "GRATIS · ARCHIVO REAL" },
  portadaHasta: 0.42,
  golpes: [{ t: 10.3 }],
  empujes: [{ t: 3.24, escala: 1.12 }],
  zoomFuera: [10.78],
  whips: [3.9],
  estudio: {
    in: 5.38, out: 6.62,
    elementos: [
      { tipo: "icono", g: "foco", t0: 5.62, t1: 6.62, x: 540, y: 760, size: 300 },
      { tipo: "chicas", words: [["NO", 5.38], ["SE", 5.5], ["ATASCA", 5.6], ["POR", 5.66]], t1: 6.62, y: 1060, size: 56 },
      { tipo: "cromo", txt: "FALTA DE IDEAS", t0: 5.86, t1: 6.62, y: 1250, size: 150, v: "cobre" },
    ],
  },
  destellos: [6.7, 12.68],
  elementos: [
    { tipo: "chicas", words: [["ABRISTE", 0.5]], t1: 1.6, y: 300 },
    { tipo: "cromo", txt: "DYNAMO", t0: 0.6, t1: 1.6, y: 520, size: 240, v: "navy", capa: "detras" },
    { tipo: "chicas", words: [["NO", 1.64], ["SUPISTE", 1.88], ["POR", 2.22], ["DÓNDE", 2.42]], t1: 3.2, y: 300 },
    { tipo: "icono", g: "pregunta", t0: 1.9, t1: 3.2, x: 860, y: 820 },
    { tipo: "cromo", txt: "SEGUIR", t0: 2.6, t1: 3.2, y: 520, size: 250, v: "cobre", capa: "detras" },
    { tipo: "cromo", txt: "CERRASTE", t0: 3.24, t1: 3.84, y: 1260, size: 200, v: "navy" },
    { tipo: "chicas", words: [["LA", 3.92]], t1: 5.38, y: 300 },
    { tipo: "cromo", txt: "AUTOMATIZACIÓN", t0: 4.04, t1: 5.38, y: 430, size: 150, v: "navy", capa: "detras" },
    { tipo: "chicas", words: [["EN", 4.58]], t1: 5.38, y: 1120 },
    { tipo: "cromo", txt: "BIM", t0: 4.76, t1: 5.36, y: 1270, size: 200, v: "cobre" },
    { tipo: "chicas", words: [["SE", 6.66], ["ATASCA", 6.7], ["EN", 7.04], ["EL", 7.26]], t1: 8.1, y: 300 },
    { tipo: "cromo", txt: "PRIMER SCRIPT", t0: 7.4, t1: 8.1, y: 1260, size: 160, v: "cobre" },
    { tipo: "icono", g: "codigo", t0: 7.72, t1: 8.1, x: 210, y: 820 },
    { tipo: "chicas", words: [["AQUÍ", 8.16], ["VAN", 8.32]], t1: 9.0, y: 300 },
    { tipo: "cromo", txt: "5", t0: 8.54, t1: 9.0, x: 840, y: 700, size: 560, v: "cobre", capa: "detras" },
    { tipo: "chicas", words: [["SCRIPTS", 8.6]], t1: 9.0, x: 840, y: 1030, size: 64 },
    { tipo: "icono", g: "archivo", t0: 9.02, t1: 10.7, x: 270, y: 420, size: 160, num: "1" },
    { tipo: "icono", g: "archivo", t0: 9.24, t1: 10.7, x: 540, y: 400, size: 160, num: "2" },
    { tipo: "icono", g: "archivo", t0: 9.42, t1: 10.7, x: 810, y: 420, size: 160, num: "3" },
    { tipo: "chicas", words: [["LOS", 9.54], ["PUEDES", 9.76], ["CORRER", 9.88]], t1: 10.7, y: 1120 },
    { tipo: "cromo", txt: "HOY", t0: 10.26, t1: 10.72, y: 1300, size: 300, v: "navy" },
    { tipo: "chicas", words: [["EN", 10.78], ["UN", 11.04], ["ARCHIVO", 11.2]], t1: 12.6, y: 300 },
    { tipo: "anillo", t0: 11.0, t1: 12.6, x: 800, y: 980 },
    { tipo: "chicas", words: [["COMPLETAMENTE", 11.62]], t1: 12.6, y: 1150 },
    { tipo: "cromo", txt: "VIVO", t0: 12.2, t1: 12.62, y: 1310, size: 230, v: "cobre" },
    { tipo: "cromo", txt: "GRATIS", t0: 12.68, t1: 14.1, y: 520, size: 270, v: "cobre", capa: "detras" },
    { tipo: "chicas", words: [["EL", 13.12], ["ENLACE", 13.2], ["ESTÁ", 13.44]], t1: 14.1, y: 1150 },
    { tipo: "cromo", txt: "AQUÍ ABAJO", t0: 13.6, t1: 14.1, y: 1300, size: 140, v: "navy" },
    { tipo: "icono", g: "flecha", t0: 13.7, t1: 14.1, x: 540, y: 1540, size: 130, rebote: true },
  ],
};
