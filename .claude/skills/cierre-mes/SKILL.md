---
name: cierre-mes
description: >
  Genera la presentación de cierre y apertura de mes de Design Modeling Academy
  (DMA): ventas reales de GoHighLevel depuradas, resultado de campañas de Meta
  Ads con las imágenes de los anuncios ganadores, resultado orgánico, cruce
  pauta→ventas, metas del mes para closer y setter, y la presentación en Gamma
  exportada a PPTX/PDF. ACTIVA cuando Dayana diga: "cierre de mes", "cierre y
  apertura", "/cierre-mes", "presentación de cierre", "métricas del mes",
  "cuánto vendimos este mes", o cuando llegue el recordatorio mensual programado.
---

# Cierre y apertura de mes — DMA

> **Requisito:** este metodo usa el repo `designmodelingdg-droid/meta-ads-dashboard.html`
> (workflow de creativos + matriz organica) y los conectores **Windsor.ai** (GHL)
> y **Gamma**. Si la conversacion no tiene el repo, añadirlo/clonarlo PRIMERO;
> si falta un conector, avisar a Dayana que lo active en claude.ai antes de seguir.

Método oficial validado con Dayana (agosto 2026). El resultado final es una
presentación en Gamma + PPTX/PDF con los números REALES del mes.

## 0. Ventana del mes

Del **día 5 del mes anterior** al **día 5 del mes actual** (así lo mide Dayana).
Confirmar la ventana con ella solo si el mes tiene algo raro.

## 1. Ventas reales (GoHighLevel vía Windsor.ai)

Connector `gohighlevel` (cuenta "Design Modeling Academy", location
`nkKbOarn5IwHeMv48uY9`). Traer oportunidades con campos:
`opportunity_name, opportunity_status, opportunity_monetary_value,
opportunity_pipeline_id, opportunity_created_at, opportunity_last_status_change_at,
opportunity_source`.

**Reglas de depuración (el método, en orden):**
1. Filtrar `status == won` y `last_status_change_at` DENTRO de la ventana
   (no la fecha de creación).
2. **Deduplicar por cliente** entre pipelines: el mismo nombre solo cuenta UNA
   vez, con el registro de mayor valor (ej. Ronal en Máster HT $1,900, se borra
   su copia de $1,800 en Acero).
3. Excluir registros con "Prueba" en el nombre.
4. Los de etapa **PAGO RECURRENTE** se consultan con Dayana caso por caso
   (en julio Luis Alberto sí contó como venta).
5. Los cierres con valor $0 NO suman al total, pero van a la lista de higiene
   con nombre y apellido para que el equipo les ponga monto.

**Agrupar así:** Máster (pipelines Máster High Ticket + Máster BIM+IA) ·
Especialización Acero (etapas INSCRITO ACERO / ACERO 2 / OTRO, viven en el
pipeline "OLYMPUS CURSOS LOWCOST" y en "ESPECIALIZACIONES") · Cursos lowcost
(~$27) · Diplomados. **Precios (cambiaron en septiembre — usar estos):** el Máster ya NO se cotiza
como programa de 12 meses, se vende POR MÓDULOS: BIM Professional $750 · BIM
Coordination $750 · BIM Management $600 · BIM + IA $900. La ruta completa
(~$3.000 sueltos) la maneja el closer, y NO va en ninguna pieza publicada.
Acero pasó de $199.99 a **$225 desde el 3-sep**, porque ahora incluye el tutor
de IA. Al cerrar un mes anterior a septiembre, usar los precios de ese mes.

**Pipelines (IDs):** Máster HT `fOeASz8t5bzDPA0SXTWq` · Máster BIM+IA
`Ap8J7yGAiijJCHXSBxOB` · Especializaciones `WoSW1cuowh9wXwKotAeW` · Cursos
Lowcost `CIRfFG6WLQq8yuLcdPz9` · Diplomados `tDlrQaFOjdRb0Wn6yaCW` · Landing
`kOnlGngoJYTpcbbVlz4I` · IG-FB-TikTok `qjXIsYXjqdWbge7bZCdT` · Autodesk
`O3bJlZnAKDNcGV1Ffu5t` · Progreso `qADFbtxPRI1N5OLEEcwW`.

**SIEMPRE mostrar a Dayana la lista nominal de ventas antes de armar la
presentación final** — ella valida contra su memoria y sus filtros de GHL.

## 2. Campañas y anuncios ganadores (Meta Ads API vía GitHub Actions)

El token vive en el secreto `META_TOKEN` del repo. Disparar el workflow
`metricas-semanales.yml` con inputs
`{"solo_creativos": "true", "desde": "YYYY-MM-DD", "hasta": "YYYY-MM-DD"}`
(ref: la rama de trabajo). El job corre `scripts/ads_creativos.py`, que:
- rankea anuncios por leads (lead + conversaciones WhatsApp iniciadas),
- baja la imagen de cada creativo del top 6 a
  `matriz-viral/fuentes/ads-creativos/` + `manifest.json` con gasto/leads/CPL/CTR,
- para anuncios de VIDEO baja todos los thumbnails candidatos (-a, -b, -c…):
  **revisarlos visualmente** y elegir el nítido (el cover autogenerado suele ser
  un degradado borroso).

Hacer `git pull`, mirar las imágenes, y usar las URLs raw
(`https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/<rama>/matriz-viral/fuentes/ads-creativos/<archivo>.jpg`)
como `![...](url)` en el inputText de Gamma. Anuncios repetidos en varios
conjuntos (mismo creativo) se muestran una vez con leads combinados.

## 3. Cruce pauta → ventas reales

Cruzar `opportunity_source` de cada venta con su campaña:
`registro-formulario` → MÁSTER Formulario V2 · `sms-whatsapp` → ACERO geo-split
WSP+SMS · `whatsapp-api` → MÁSTER BIM+IA WSP API · `Campaña de facebook Ads` →
Facebook · `sales-agent` / `Instagram` → orgánico/bot. Calcular ROAS real por
campaña (ingreso atribuido / gasto) y señalar: campañas con gasto sin ventas
atribuidas, y ventas sin fuente (van a la lista de higiene).

## 3b. Lo que trae la matriz del mes que abre

Antes de las metas, mirar la pestaña de la matriz del mes nuevo y traerse a la
presentación lo que cambia la operación: productos con precio nuevo, campañas
que salen, recursos gratuitos por crear y lo que bloquea a qué. El cierre no es
solo mirar atrás; la mitad de la reunión es qué se hace distinto.

## 4. Orgánico

Sacar los datos del análisis del repo (`matriz-viral/matriz/`) y/o de la matriz
de contenido del mes: post ganador con views y de dónde vinieron, lead magnet,
mejor ángulo con su engagement, qué no funcionó. Solo números reales.

## 5. Metas del mes siguiente

Meta por defecto: **$10,000** (confirmar con Dayana si cambia). Construirla
sobre la base real del mes que cierra, por producto (Máster y Acero), con:
cierres necesarios, ritmo semanal, mezcla de entrada, y leads disponibles según
la pauta. Diapositiva de CLOSER y SETTER en dos columnas con metas semanales
concretas. Regla del ticket de Acero: defender $199.99, promo $100 solo como
rescate.

## 6. La presentación (Gamma)

Estructura probada (10 diapositivas): Portada · Campañas (tabla exacta) ·
Anuncios ganadores (imágenes reales en cuadrícula + métricas) · Cruce
pauta→ventas (tabla + 3 hallazgos) · Orgánico · Ventas reales (bloques sumando
al total) · Higiene CRM (checklist nominal para el equipo) · Plan del mes ·
Meta con la matemática por producto · Closer/Setter · Próximos pasos.

Estilo: ejecutivo, azul marino + naranja (marca DMA), cifras grandes,
`textMode: preserve`, `cardSplit: inputTextBreaks`, y para que no invente
imágenes: `imageOptions: {"source": "noImages"}` con las URLs reales en el
texto. Al terminar: exportar a **pptx y pdf** y entregar los links de descarga
(caducan en ~1 semana — avisarlo).

## Lo que dejó el cierre de agosto (para no repetir el trabajo)

El cierre de cada mes se guarda en `matriz-viral/cierres/<AAAA-MM>.json` con
ventas, pauta, orgánico, hallazgos, higiene y la matemática de la meta. Antes
de armar el mes siguiente, LEER el anterior: la comparación es la mitad del
valor de la reunión y sin el archivo hay que reconstruirla a mano.

Tres cosas que agosto enseñó sobre el método mismo:

- **El archivo de campañas puede tener otra ventana que la de las ventas.**
  `por-campana.json` se genera con su propia fecha; si no coincide con la
  ventana del mes, decirlo en la presentación en vez de mezclar.
- **La reunión suele caer antes del día 5**, así que el cierre llega hasta el
  día anterior. Anotarlo: al comparar dos meses hay que saber que uno tiene
  menos días.
- **Mirar las oportunidades en $0 antes de contarlas.** No todas son ventas sin
  monto: en agosto ocho eran reservas de un curso gratuito marcadas como
  ganadas, y dos eran pruebas. Un pipeline que marca ganado lo gratuito hace
  que el conteo de ganados no signifique nada.

## Reglas no negociables

1. Nunca presentar el total de "ganados" crudo: siempre depurado (duplicados,
   pruebas, $0, recurrentes) y validado por Dayana.
2. Todos los números de la presentación deben ser reales y trazables a GHL,
   Meta API o la matriz del repo. Nada estimado sin marcarlo como estimado.
3. La lista de higiene del CRM (sin monto / duplicados / sin fuente / cruzados)
   va SIEMPRE, con nombres, como tarea del equipo.
4. Idioma: español. Tono: directo, de reunión de equipo.
