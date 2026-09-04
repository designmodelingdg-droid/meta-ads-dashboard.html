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

## 1. EL DINERO QUE ENTRÓ (Stripe + PayPal) — se lee ANTES que nada

**Esta sección existe porque en agosto no existía y el cierre salió con menos
de la mitad de la facturación del mes.**

Lo que pasó, para que no se repita: el cierre de agosto reportó $3.595,92
—oportunidades marcadas ganadas en GoHighLevel— y se presentó como el ingreso
del mes. En el repositorio, desde el 1 de septiembre y generado solo dos veces
por semana, estaba `matriz-viral/fuentes/ingresos/resumen.json` diciendo
**$10.317,91 realmente cobrados**. Nadie lo abrió. La meta de septiembre se fijó
como «2,78 veces agosto» sobre una base que era menos de la mitad de la real, y
esa cifra viajó a una presentación y a una reunión con todo el equipo.

El CRM **no sabe cuánto entró**. Sabe qué se marcó. Son cosas distintas y la
diferencia en agosto fue de más de seis mil dólares.

### Qué leer, siempre, y en este orden

```
matriz-viral/fuentes/ingresos/resumen.json   ← el total del mes. Empezar aquí.
matriz-viral/fuentes/ingresos/stripe.json    ← cobro por cobro: fecha, bruto, reembolsado, neto, correo, descripcion
matriz-viral/fuentes/ingresos/paypal.json    ← idem
```

Los baja sola la Action `metricas-semanales.yml` (lunes y viernes) con los
secretos `STRIPE_SECRET_KEY`, `CLIEND_ID_PAYPAL` y `SECRET_KEY_PAYPAL`. No hace
falta ningún token a mano.

### Tres comprobaciones obligatorias antes de usar el número

1. **La ventana del archivo tiene que ser la del cierre.** `resumen.json` trae
   su propia `ventana`. Si no coincide con la del mes, disparar
   `metricas-semanales.yml` con `desde` y `hasta` correctos y esperar. Nunca
   comparar un total de una ventana con el gasto de otra.
2. **Buscar huecos de cobertura.** En agosto el listado de PayPal empezaba el
   11-ago y el mes arrancaba el 5: seis días sin cubrir que nadie notó. Mirar la
   fecha del primer y del último cobro de CADA pasarela y decirlo en la
   presentación si no cubren la ventana entera.
3. **Preguntar por las cuentas que no están.** Los archivos cubren UNA cuenta de
   Stripe y UNA de PayPal. Si hay transferencias bancarias, otra cuenta de
   PayPal, o cobros por un tercero, no están aquí. Preguntarle a Dayana qué
   falta antes de dar un total por cerrado.

### Cómo se leen los cobros

- `neto` = bruto − reembolsado. Es **antes** de comisiones de pasarela: es el
  mismo criterio que usa el área, así que las cifras son comparables.
- Agrupar por `descripcion` y por monto: en agosto, 16 cobros de $160
  («Subscription update») eran cuotas mensuales del Máster de contratos
  vigentes. **Eso es ingreso recurrente, no captación nueva**, y hay que
  separarlo o la meta del mes siguiente sale mal planteada.
- Los correos permiten cruzar cobro contra persona contra oportunidad del CRM.

## 2. Composición y atribución (GoHighLevel vía Windsor.ai)

**Este número NO es el ingreso del mes.** Sirve para saber QUÉ se vendió, a
QUIÉN y de dónde vino — la mezcla y la atribución. El cuánto sale de la
sección 1.

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

## 3. Campañas y anuncios ganadores (Meta Ads API vía GitHub Actions)

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

## 4. Cruce pauta → dinero cobrado

El ROAS se reporta SIEMPRE en dos versiones, porque responden preguntas
distintas y en agosto una sola dio una imagen falsa:

| ROAS | Fórmula | Para qué sirve |
|---|---|---|
| **De adquisición** | revenue atribuido a anuncios ÷ inversión | decidir presupuesto de captación |
| **De caja** | cobros verificados ÷ inversión | saber si el negocio ganó dinero |

El de adquisición excluye los pagos recurrentes; el de caja los incluye. Decir
cuál es cuál. En agosto salieron 2,74x y 5,54x sobre los mismos días.

Cruzar `opportunity_source` de cada venta con su campaña:
`registro-formulario` → MÁSTER Formulario V2 · `sms-whatsapp` → ACERO geo-split
WSP+SMS · `whatsapp-api` → MÁSTER BIM+IA WSP API · `Campaña de facebook Ads` →
Facebook · `sales-agent` / `Instagram` → orgánico/bot. Calcular ROAS real por
campaña (ingreso atribuido / gasto) y señalar: campañas con gasto sin ventas
atribuidas, y ventas sin fuente (van a la lista de higiene).

## 4b. Lo que trae la matriz del mes que abre

Antes de las metas, mirar la pestaña de la matriz del mes nuevo y traerse a la
presentación lo que cambia la operación: productos con precio nuevo, campañas
que salen, recursos gratuitos por crear y lo que bloquea a qué. El cierre no es
solo mirar atrás; la mitad de la reunión es qué se hace distinto.

## 5. Orgánico

Sacar los datos del análisis del repo (`matriz-viral/matriz/`) y/o de la matriz
de contenido del mes: post ganador con views y de dónde vinieron, lead magnet,
mejor ángulo con su engagement, qué no funcionó. Solo números reales.

## 6. Metas del mes siguiente

Meta por defecto: **$10,000** (confirmar con Dayana si cambia). Construirla
sobre la base real del mes que cierra, por producto (Máster y Acero), con:
cierres necesarios, ritmo semanal, mezcla de entrada, y leads disponibles según
la pauta. Diapositiva de CLOSER y SETTER en dos columnas con metas semanales
concretas. Regla del ticket de Acero: defender $199.99, promo $100 solo como
rescate.

## 7. La presentación (Gamma)

**Tarjeta obligatoria: la conciliación de las fuentes.** Nunca presentar una
sola cifra de facturación. En agosto había cuatro fuentes dando cuatro números
para el mismo mes, con $4.684,12 de dispersión, y la que se presentó era la más
baja de todas. La tarjeta lleva: cobrado en pasarelas (el titular), suma de
pipelines del CRM, widget de eficiencia, planillas del área — y una línea que
diga cuál se usa y por qué.

Estructura probada (10 diapositivas): Portada · Campañas (tabla exacta) ·
Anuncios ganadores (imágenes reales en cuadrícula + métricas) · Cruce
pauta→ventas (tabla + 3 hallazgos) · Orgánico · Ventas reales (bloques sumando
al total) · Higiene CRM (checklist nominal para el equipo) · Plan del mes ·
Meta con la matemática por producto · Closer/Setter · Próximos pasos.

**El tema NO se elige por palabras: la cuenta tiene dos temas propios de DMA.**
`themeId: 5tee2tx4zjbm9go` es **DM-FondoAzul** (el de la marca, azul marino) y
`aas0rvhn9qj2w93` es **DM-FondoBlanco**. Usar el azul salvo que Dayana pida
otra cosa — sin `themeId` sale el tema genérico de Gamma, que es azul-violeta y
no es la marca. Se descubrió al generar el cierre de agosto: la primera corrida
salió con el tema por defecto y hubo que rehacerla.

Estilo: ejecutivo, cifras grandes,
`textMode: preserve`, `cardSplit: inputTextBreaks`, y para que no invente
imágenes: `imageOptions: {"source": "noImages"}` con las URLs reales en el
texto. Las imágenes de los creativos ganadores se copian a
`cierre-<mes>/img/` y se publican por GitHub Pages (`publish-matriz.yml`), NO
por `raw.githubusercontent`: la rama de trabajo desaparece con el merge y el
mazo se queda con huecos. Al terminar: exportar a **pptx y pdf** y entregar los links de descarga
(caducan en ~1 semana — avisarlo).

## Lo que dejó el cierre de agosto (para no repetir el trabajo)

El cierre de cada mes se guarda en `matriz-viral/cierres/<AAAA-MM>.json` con
ventas, pauta, orgánico, hallazgos, higiene y la matemática de la meta. Antes
de armar el mes siguiente, LEER el anterior: la comparación es la mitad del
valor de la reunión y sin el archivo hay que reconstruirla a mano.

Cuatro cosas que agosto enseñó sobre el método mismo:

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
- **Los anuncios ganadores se cuentan por imagen, no por fila.** El volcado de
  Meta lista un anuncio por conjunto, así que el mismo creativo aparece varias
  veces con nombres casi iguales. En agosto los 6 primeros eran 2 imágenes:
  `md5sum` sobre los archivos lo resuelve en un segundo, y cambia lo que se
  dice en la reunión — no son seis piezas que funcionan, es una dependencia de
  dos. Antes de mostrarlas, abrirlas: la portada que devuelve la API para un
  anuncio de video viene desenfocada y en ~28 KB (hay que usar un fotograma),
  y hay que comprobar que el precio impreso siga siendo el vigente.

## Reglas no negociables

1. **La facturación del mes sale de las pasarelas, nunca del CRM.** Leer
   `matriz-viral/fuentes/ingresos/` antes que cualquier otra cosa. El número de
   GoHighLevel sirve para la mezcla y la atribución, jamás como el ingreso del
   mes: en agosto la diferencia fue de más de seis mil dólares y la cifra baja
   llegó a una presentación de equipo.
2. **Separar recurrente de captación nueva** antes de plantear la meta del mes
   siguiente. Un multiplicador calculado sobre caja total exige un esfuerzo
   distinto al calculado sobre captación.
3. Nunca presentar el total de "ganados" crudo: siempre depurado (duplicados,
   pruebas, $0, recurrentes) y validado por Dayana.
4. Todos los números de la presentación deben ser reales y trazables a GHL,
   Meta API o la matriz del repo. Nada estimado sin marcarlo como estimado.
5. La lista de higiene del CRM (sin monto / duplicados / sin fuente / cruzados)
   va SIEMPRE, con nombres, como tarea del equipo.
6. Idioma: español. Tono: directo, de reunión de equipo.
