// Estilos compartidos por los dos documentos de Esther.
const d = require('docx');
const {
  Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, ExternalHyperlink,
} = d;

const NAVY = '001E30';
const NARANJA = 'CA7520';
const CREMA = 'FAFAF7';
const GRIS = '5A6B7B';
const ROJO = 'B3261E';
const ANCHO = 10080;            // ancho util con margenes de 0.75"

// ── bloques de texto ───────────────────────────────────────────────
const p = (texto, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 },
  alignment: o.align,
  indent: o.indent,
  children: [new TextRun({
    text: texto, bold: o.bold, italics: o.italics, size: o.size ?? 21,
    color: o.color ?? '333333', font: 'Calibri',
  })],
});

// parrafo con trozos en negrita: pasa un array ['normal', ['negrita'], 'normal']
const pmix = (partes, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 },
  indent: o.indent,
  children: partes.map(x => Array.isArray(x)
    ? new TextRun({ text: x[0], bold: true, size: 21, color: x[1] ?? '333333', font: 'Calibri' })
    : new TextRun({ text: x, size: 21, color: '333333', font: 'Calibri' })),
});

const h1 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 360, after: 180 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NARANJA, space: 6 } },
  children: [new TextRun({ text: t, bold: true, size: 30, color: NAVY, font: 'Calibri' })],
});

const h2 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 280, after: 130 },
  children: [new TextRun({ text: t, bold: true, size: 24, color: NAVY, font: 'Calibri' })],
});

const h3 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text: t, bold: true, size: 21, color: NARANJA, font: 'Calibri' })],
});

const bullet = (t, nivel = 0) => new Paragraph({
  numbering: { reference: 'vinetas', level: nivel },
  spacing: { after: 80, line: 276 },
  children: [new TextRun({ text: t, size: 21, color: '333333', font: 'Calibri' })],
});

const paso = (t) => new Paragraph({
  numbering: { reference: 'pasos', level: 0 },
  spacing: { after: 110, line: 276 },
  children: [new TextRun({ text: t, size: 21, color: '333333', font: 'Calibri' })],
});

// enlace largo: en su propia linea, monoespaciado, para copiar sin errores
const enlace = (url) => new Paragraph({
  spacing: { after: 140 },
  indent: { left: 280 },
  children: [new ExternalHyperlink({
    link: url,
    children: [new TextRun({ text: url, size: 17, color: '1155CC', underline: {}, font: 'Consolas' })],
  })],
});

const codigo = (lineas) => new Paragraph({
  spacing: { before: 100, after: 140 },
  shading: { type: ShadingType.CLEAR, fill: 'F2F4F6' },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: NARANJA, space: 8 } },
  indent: { left: 200, right: 200 },
  children: lineas.flatMap((l, i) => [
    ...(i ? [new TextRun({ break: 1 })] : []),
    new TextRun({ text: l, size: 18, font: 'Consolas', color: '1F2933' }),
  ]),
});

// aviso destacado: tipo 'alerta' (rojo) o 'nota' (naranja)
const aviso = (titulo, texto, tipo = 'nota') => new Table({
  columnWidths: [ANCHO],
  width: { size: ANCHO, type: WidthType.DXA },
  borders: {
    top:    { style: BorderStyle.SINGLE, size: 4, color: tipo === 'alerta' ? 'F0C4C0' : 'F0DCC0' },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: tipo === 'alerta' ? 'F0C4C0' : 'F0DCC0' },
    left:   { style: BorderStyle.SINGLE, size: 24, color: tipo === 'alerta' ? ROJO : NARANJA },
    right:  { style: BorderStyle.SINGLE, size: 4, color: tipo === 'alerta' ? 'F0C4C0' : 'F0DCC0' },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [new TableRow({ children: [new TableCell({
    width: { size: ANCHO, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: tipo === 'alerta' ? 'FDF3F2' : 'FFF8EE' },
    margins: { top: 140, bottom: 140, left: 200, right: 200 },
    children: [
      new Paragraph({ spacing: { after: 70 }, children: [
        new TextRun({ text: titulo, bold: true, size: 21, color: tipo === 'alerta' ? ROJO : '8A4D0D', font: 'Calibri' })] }),
      ...(Array.isArray(texto) ? texto : [texto]).map(t =>
        new Paragraph({ spacing: { after: 60, line: 276 }, children: [
          new TextRun({ text: t, size: 20, color: '333333', font: 'Calibri' })] })),
    ],
  })] })],
});

// tabla: cabeceras + filas, anchos en porcentaje del ancho util
const tabla = (cabeceras, filas, pesos) => {
  const total = pesos.reduce((a, b) => a + b, 0);
  const cols = pesos.map(x => Math.round(ANCHO * x / total));
  cols[cols.length - 1] = ANCHO - cols.slice(0, -1).reduce((a, b) => a + b, 0);
  const celda = (t, i, esCab) => new TableCell({
    width: { size: cols[i], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: esCab ? NAVY : 'FFFFFF' },
    margins: { top: 90, bottom: 90, left: 130, right: 130 },
    children: [new Paragraph({ spacing: { after: 0, line: 260 }, children: [
      new TextRun({ text: String(t), bold: esCab, size: esCab ? 19 : 19,
        color: esCab ? 'FFFFFF' : '333333', font: 'Calibri' })] })],
  });
  return new Table({
    columnWidths: cols,
    width: { size: ANCHO, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: 'D5DBE0' },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: 'D5DBE0' },
      left: { style: BorderStyle.SINGLE, size: 2, color: 'D5DBE0' },
      right: { style: BorderStyle.SINGLE, size: 2, color: 'D5DBE0' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: 'E5E9EC' },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: 'E5E9EC' },
    },
    rows: [
      new TableRow({ tableHeader: true, children: cabeceras.map((c, i) => celda(c, i, true)) }),
      ...filas.map(f => new TableRow({ children: f.map((c, i) => celda(c, i, false)) })),
    ],
  });
};

// portada
const portada = (titulo, subtitulo, etiqueta, colorEtiqueta, meta) => [
  new Paragraph({ spacing: { before: 900, after: 200 }, children: [
    new TextRun({ text: 'DESIGN MODELING ACADEMY', bold: true, size: 18,
      color: NARANJA, characterSpacing: 60, font: 'Calibri' })] }),
  // El titulo llega como array de lineas: Word no interpreta "\n" dentro de
  // un run, hay que usar saltos explicitos.
  new Paragraph({ spacing: { after: 100, line: 300 }, children:
    (Array.isArray(titulo) ? titulo : [titulo]).map((l, i) => new TextRun({
      text: l, bold: true, size: 46, color: NAVY, font: 'Calibri', break: i ? 1 : 0 })) }),
  new Paragraph({ spacing: { after: 320 }, children: [
    new TextRun({ text: subtitulo, size: 24, color: GRIS, font: 'Calibri' })] }),
  new Table({
    columnWidths: [3000],
    width: { size: 3000, type: WidthType.DXA },
    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } },
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 3000, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: colorEtiqueta },
      margins: { top: 110, bottom: 110, left: 180, right: 180 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: etiqueta, bold: true, size: 22, color: 'FFFFFF', font: 'Calibri' })] })],
    })] })],
  }),
  new Paragraph({ spacing: { before: 400, after: 0 }, children: meta.map((m, i) => new TextRun({
    text: m, size: 19, color: GRIS, font: 'Calibri', break: i ? 1 : 0 })) }),
];

const numeracion = {
  config: [
    { reference: 'vinetas', levels: [
      { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 460, hanging: 230 } } } },
      { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 880, hanging: 230 } } } },
    ] },
    { reference: 'pasos', levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 460, hanging: 300 } } } },
    ] },
  ],
};

const seccion = (hijos) => ({
  properties: { page: {
    size: { width: 12240, height: 15840 },
    margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
  } },
  children: hijos,
});

module.exports = { d, p, pmix, h1, h2, h3, bullet, paso, enlace, codigo, aviso,
  tabla, portada, numeracion, seccion, NAVY, NARANJA, CREMA, GRIS, ROJO, ANCHO, PageBreak, Paragraph, TextRun };
