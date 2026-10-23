# Auditoría de pauta contra GHL · 23-oct-2026

Fuentes:

- **Meta:** anuncios del 9 al 22-oct y campañas del 23-sep al 22-oct (`fuentes/ads-copys/anuncios.json`, `fuentes/ads-insights/`).
- **GHL:** oportunidades ganadas vía Windsor, filtradas por fecha de cambio a ganada entre el 23-sep y el 22-oct. Etapas del volcado del repo, que son las últimas 1.200 oportunidades.
- **Cobros:** `fuentes/ingresos/` (Stripe y PayPal).
- **Consultoría:** $15.239,14, $1.000, $2.000 y $3.928,75. Excluidos.

## 1 · Lo que se gastó y lo que trajo (30 días)

| | |
|---|---|
| Inversión Meta | $1.090,76 |
| Leads (formulario + conversaciones de WhatsApp) | 1.097 · $0,99 por lead |
| Cobrado por la Academy | $4.896,82 |
| — recurrente (cuotas del Máster) | $2.642,88 (19 cobros) |
| — venta nueva | $2.253,94 (9 cobros) |
| ROAS de caja (todo lo cobrado ÷ inversión) | 4,49x |
| ROAS de venta nueva | 2,07x |
| ROAS de adquisición (ventas con fuente de anuncio en GHL) | 0,55x ($600: Samuel $400 por registro-formulario + Victor $200 por Facebook) |

El 0,55x es un mínimo: las ventas por `sales-agent` (bot de WhatsApp) pueden venir de la campaña ACERO WSP, pero GHL no lo distingue del orgánico.

## 2 · Campañas activas (9 al 22-oct)

| Campaña | Gasto | Resultados | Costo | Lectura |
|---|---|---|---|---|
| MASTER FORM (29SEP) | $118,10 | 321 leads | $0,37 | Barato, pero ver §4: casi no se califica |
| ACERO FORM (29SEP) | $97,54 | 109 leads | $0,89 | **Mismo texto que ACERO WSP y 2,3 veces más caro** |
| ACERO WSP SMS (29SEP) | $95,33 | 246 conversaciones | $0,39 | La mejor de la cuenta. Las ventas de Acero del mes entraron por WhatsApp |
| MÁSTER TEST GANCHOS (15OCT) | $48,69 | 60 | $0,81 | Gana V3 («tutoriales sueltos de YouTube», $0,65). V2 sin entrega |
| ACERO TEST GANCHOS (15OCT) | $47,08 | 36 | $1,31 | Gana V2 («acero de más», $1,29), pero sigue más caro que la campaña madre |
| LEAD MAGNETS ACERO + MÁSTER | $24,54 | clics | — | Tráfico, sin leads atribuibles |
| Workshop (22OCT) | $0 | 0 | — | Creada el 22: todavía sin entrega. El workshop tiene 0 registros |

## 3 · Hallazgos del método

1. **Canibalismo real en Acero.** «¿Modelas estructuras de acero en BIM… pero dependes de otro para el cálculo?» vive en dos campañas: en FORM sale a $0,89 y en WSP a $0,39. Es la misma subasta con dos pujas.
2. **Promesa vencida en el Máster.** 6 anuncios activos (MásterBloque1 V03/V04/V05 y MasterAGO-feed01) cierran con «¡Únete ahora en preventa y aprovecha el precio exclusivo!». La preventa era de agosto.
3. **Desorden.** De 81 anuncios activos, 44 no entregaron en 14 días. Hay 26 textos distintos y la diversidad está bien. Se pueden pausar los que no entregan.
4. **Primera línea de más de 125 caracteres** en 5 textos del Máster (157, 179, 142, 164 y 126). La frase que vende queda detrás de «ver más».
5. **Frecuencia:** bien en 14 días (máximo 2,4). En 30 días, ACERO WSP está en 3,84, en zona de aviso: hay que rotar el creativo antes de Black Friday.

## 4 · El cuello de botella está después del lead, no en el anuncio

Etapas del Máster High Ticket (342 oportunidades recientes):

- 165 no calificado/perdido y 44 no calificado + downsell: 61 %.
- 3 lead calificado.
- 5 reunión agendada, 3 asistió y 9 no show.
- 37 oportunidad futura.

Con 591 leads del Máster en 30 días salieron 2 ventas en GHL: Samuel $400 y Dennys $200. El lead de $0,37 no es el problema: casi nadie llega a reunión y la mitad de los que agendan no se presentan.

Acero / lowcost (333): 144 en LEAD CONVERSACIÓN, 118 en seguimiento 1-4, 6 en POR PAGAR/ENLACE y 3 INSCRITO ACERO. Los 6 por pagar son la venta más cercana de la semana.

## 5 · Higiene del CRM (GHL contra pasarelas)

Cobrado sin oportunidad ganada:

- $750 (7-oct, módulo del Máster).
- $250 (20-oct, cuota del Diplomado).
- PayPal $199,99 del 11 y del 18-oct.

Ganado en GHL sin cobro en Stripe ni PayPal (¿transferencia u otra cuenta?):

- Santiago O. $225 (8-oct).
- Dennys Arrieta $200 (8-oct, sin fuente).
- Angel Marchena $100 (8-oct).
- Victor Perugachi $200 (13-oct).

Etiqueta contradictoria: «Samuel Alvarado - No Calificado» está ganado por $400.

Cobertura: el primer cobro de PayPal en la ventana es del 11-oct. Hay que confirmar que no faltan cobros del 23-sep al 10-oct.

## 6 · Qué hacer

1. **Acero:** pasar el presupuesto de ACERO FORM a ACERO WSP, o darle a FORM otro texto. Con la regla de noviembre (la oferta solo por WhatsApp), WSP es además la campaña que encaja con Black Friday.
2. **Máster:** quitar o reescribir los 6 anuncios con «preventa / precio exclusivo». Recortar la primera línea de los 5 textos largos.
3. **Pausar** los 44 anuncios activos sin entrega y las 2 campañas de LEAD MAGNETS (ya estaba en la matriz para el 2-nov).
4. **Tests de ganchos:** quedarse con el ganador de cada test, V3 en Máster y V2 en Acero, y moverlo a la campaña madre. Apagar los perdedores.
5. **Workshop:** comprobar mañana que la campaña entrega. Si sigue en $0, revisar si está en revisión o con fecha de inicio.
6. **Setter y closer (no es pauta):** recordatorio de cita 24 h y 1 h antes por WhatsApp para bajar los no show (9 de 17), y llamar hoy a los 6 de POR PAGAR/ENLACE.
7. **Higiene:** cerrar en GHL los 4 cobros sin oportunidad y confirmar cómo pagaron los 4 ganados sin cobro.
