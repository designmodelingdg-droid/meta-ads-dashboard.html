# Auditoría Meta Ads — Design Modeling Academy

**Ventana analizada:** 2026-07-22 → 2026-08-20 (30 días) | **Gasto real:** $1,098.54 | **Fuente:** exports estáticos (`ads-insights/`, `ads-creativos/`) — **sin MCP, sin acceso en vivo a Events Manager / Ads Manager / Business Manager.**

---

## ⚠️ Aviso de cobertura — léase antes que el score

De los **50 checks** del framework, solo **14 (28%)** se pudieron evaluar con datos reales (PASS/WARNING/FAIL). Los otros **36 (72%)** quedaron en **N/A** porque el export de Insights de la API no trae absolutamente nada de Pixel, CAPI, EMQ, dedup rate, ni Events Manager — tal como se anticipó en el encargo.

Esto pega más fuerte de lo habitual porque **Pixel/CAPI Health pesa 30% del score total** y de sus 11 checks solo 1 (M07, "usa eventos estándar") fue evaluable. Ese check pasó, así que la categoría marca 100/100 — **pero eso NO significa "pixel saludable"**. Es un artefacto de la fórmula (score = solo sobre lo evaluado), no una medición de EMQ, CAPI o deduplicación. Tomarlo como "el pixel está bien" sería un error.

> **CORRECCIÓN aplicada al revisar este informe (24-ago-2026).** El agente
> calculó 46.2 dando **100/100 a Píxel/CAPI evaluando 1 de sus 11 checks**.
> Esa categoría pesa 30%, así que 30 puntos salían de algo prácticamente sin
> medir. Recalculado solo sobre las tres categorías con datos reales —Creative,
> Estructura y Audiencia, el 70% del peso— el score es **43.2/100, Grade D**.
> Píxel/CAPI queda como **sin medir**, que no es lo mismo que aprobado.

**Score corregido: 43.2/100 — Grade D** (el agente reportó 46.2). Este número:
- Se calculó únicamente sobre los 14 checks con evidencia real.
- **No es comparable** con un audit hecho con MCP de Meta conectado.
- Debe leerse como una fotografía parcial y direccional, no como el número final de salud de la cuenta.

**Qué falta conectar para cerrar los huecos:**
1. **Events Manager** → Pixel firing rate, CAPI en paralelo, dedup rate, EMQ (Purchase/Lead/PageView), AEM/top 8 eventos, CAPI Gateway, ventana de atribución, frescura de eventos.
2. **Ads Manager a nivel de anuncio** → creativos activos por ad set, aspect ratio de video, hook rate/skip rate, boosting de contenido orgánico, Advantage+ Creative, fecha real de lanzamiento de cada pieza, frecuencia de 7 días por ad set.
3. **Business Manager** → verificación de dominio, CBO vs ABO, badge de "Learning Limited", historial de ediciones, estrategia de puja, placements, UTM, experimentos activos, Custom Audiences/Lookalike, presupuesto configurado vs gasto real.

Si el objetivo es un número 100% confiable, la respuesta honesta es: **no se puede dar ese número con este export**. Lo que sí se puede dar —y es la parte útil de este informe— es un diagnóstico sólido de estructura, fatiga creativa y geografía, que **no depende** de Events Manager.

---

## Score y desglose por categoría

| Categoría | Peso | Score (solo evaluados) | Checks evaluados / total |
|---|---|---|---|
| Pixel / CAPI Health | 30% | 100 *(no confiable, ver arriba)* | 1 / 11 |
| Creative (Diversidad y Fatiga) | 30% | 45.2 | 5 / 13 |
| Account Structure | 20% | 33.3 | 6 / 19 |
| Audience & Targeting | 20% | 50.0 | 2 / 7 |
| **Total ponderado** | 70% medido | **43.2 — Grade D** | **14 / 50 (28%)** |

---

## Resultados por check

### Pixel / CAPI Health (11 checks — 1 evaluado, 10 N/A)

| ID | Check | Resultado | Hallazgo |
|---|---|---|---|
| M01 | Pixel instalado | N/A | Se ven action_types `fb_pixel_lead/purchase/complete_registration` → confirma que algo dispara, no confirma cobertura |
| M02 | CAPI activa | N/A | No se distingue pixel-only vs pixel+CAPI desde Insights |
| M03 | Dedup rate | N/A | Requiere event_id match, exclusivo de Events Manager |
| M04 | EMQ | N/A | Diagnóstico exclusivo de Events Manager |
| M05 | Verificación de dominio | N/A | Config de Business Manager |
| M06 | AEM (top 8 eventos) | N/A | Config de Events Manager |
| M07 | Eventos estándar vs custom | **PASS** | `lead`, `purchase`, `complete_registration`, `lead_grouped` son estándar, no custom |
| M08 | CAPI Gateway | N/A | Infraestructura, no observable |
| M09 | Ventana de atribución iOS | N/A | Setting de ad set, no en el export |
| M10 | Frescura de datos | N/A | Requiere timestamps en tiempo real |
| M-AT1 | Offline Conversions API discontinuada | N/A | No se ve uso de offline conversions, pero no se puede confirmar en Business Manager |

### Creative — Diversidad y Fatiga (13 checks — 5 evaluados, 8 N/A)

| ID | Check | Resultado | Hallazgo |
|---|---|---|---|
| M25 | Diversidad de formato | **WARNING** | 57 archivos exportados, todos `.jpg` (imagen estática); 6 conceptos base según el manifest de ganadores. Sin video ni carrusel en el export, aunque los `video_view` en insights sugieren que sí hay video activo no capturado en esta muestra |
| M26 | Creativos por ad set | N/A | No hay desglose a nivel de anuncio |
| M27 | Aspect ratio de video | N/A | No hay archivos de video para inspeccionar |
| M28 | **Fatiga creativa** | **FAIL** | Ver sección dedicada abajo |
| M29 | Hook rate | N/A | No hay ThruPlay/retención a 3s |
| M30 | Prueba social / boosting | N/A | No se distingue post orgánico boosteado de creativo nuevo |
| M31 | UGC / social-nativo | N/A | Se intentó inspección visual de 2 imágenes ganadoras — son placeholders abstractos, no contenido real inspeccionable |
| M32 | Advantage+ Creative | N/A | No confirmable desde nombres de ad set |
| M-CR1 | Frescura del creativo | **WARNING** | Nombres de archivo ("JulioV01") sugieren pieza activa desde julio, más allá de los 14-21 días recomendados |
| M-CR2 | Frecuencia prospecting 7d | N/A | Solo hay frecuencia acumulada de 30 días |
| M-CR3 | Frecuencia retargeting 7d | N/A | No se identifica ningún ad set de retargeting en la cuenta |
| M-CR4 | CTR vs benchmark | **PASS** | 1.88%-2.39% en las 4 campañas de leads/ventas, por encima de ≥1.0% |
| M-AN1 | Diversidad Andromeda | **WARNING** | Solo 6 conceptos base distintos para 5 campañas activas — por debajo del umbral de 10 |

### Account Structure (19 checks — 6 evaluados, 13 N/A)

| ID | Check | Resultado | Hallazgo |
|---|---|---|---|
| M11 | Cantidad de campañas | **WARNING** | 5 campañas para $36.6/día de gasto total — sobre-fragmentado para el presupuesto |
| M12 | CBO vs ABO | N/A | No está en el export |
| M13 | Fase de aprendizaje | N/A | No se puede leer el badge; señal de riesgo circunstancial: muchos ad sets con <10 conversiones/semana |
| M14 | Reinicios de aprendizaje | N/A | Sin historial de ediciones |
| M15 | Advantage+ Sales/catálogo | N/A | No aplica (negocio de leads, no e-commerce) |
| M16 | Solapamiento de ad sets | **WARNING** | Dos campañas ACERO corren en simultáneo sobre los mismos países |
| M17 | **Distribución de presupuesto** | **FAIL** | Ver sección dedicada abajo |
| M18 | Alineación de objetivo | **WARNING** | Campaña de tráfico IG (LINK_CLICKS) sin conexión al KPI de leads del trimestre |
| M33-M36, M38-M40 | (placements, puja, UTM, testing, etc.) | N/A | Sin datos en el export |
| M37 | Frequency cap campaña (7d) | **WARNING** | MASTER FORM V2 acumula 4.37 en 30 días, riesgo de superar 4.0 en 7 días |
| M-ST1 | **Adecuación de presupuesto (5x CPA)** | **FAIL** | Ad sets chicos no cubren ni 1x su propio CPA en presupuesto diario |
| M-ST2 | Utilización de presupuesto | N/A | No hay presupuesto configurado en el export, solo gasto real |
| M-IA1 | Incremental Attribution | N/A | Gasto mensual (~$1,098) muy por debajo del umbral (>$5,000) que justificaría esta prueba |

### Audience & Targeting (7 checks — 2 evaluados, 5 N/A)

| ID | Check | Resultado | Hallazgo |
|---|---|---|---|
| M19 | Solapamiento de audiencias | **WARNING** | Mismo hallazgo que M16 |
| M20 | Frescura de Custom Audiences | N/A | Sin metadata de CA |
| M21 | Calidad de fuente Lookalike | N/A | Ningún ad set sugiere uso de Lookalike |
| M22 | Test de Advantage+ Audience | **WARNING** | Solo se usa en la campaña de tráfico (bajo impacto), no en las 4 campañas de leads/ventas |
| M23 | Audiencias de exclusión | N/A | Sin listas de exclusión visibles |
| M24 | Datos first-party | N/A | Sin evidencia de Customer List/Lookalike |
| M-TH1 | Placement Threads | N/A | Sin desglose de placement |

---

## Issues críticos (ordenados por impacto)

1. **[CRÍTICO] Fatiga creativa en MASTER - FORM V2 (M28) — FAIL**
   El ad set "COMPORTAMIENTOS" de la campaña del Máster (25% del gasto total, $273.02) muestra CTR cayendo de **2.49% a 1.82% (−27%)** medido sobre volúmenes comparables (primeros 7 días: 21.349 impresiones; últimos 7: 21.982) — con frecuencia acumulada de 4.37 (hasta 4.70 en el desglose por país, Ecuador). Cumple el criterio de FAIL del framework (caída de CTR >20% + frecuencia elevada). El creativo base sigue siendo el mismo desde julio (ver M-CR1). Dado que el Máster se cierra por llamada, no por contenido, esta fatiga golpea el volumen de conversaciones que alimentan ese cierre, no solo el CTR.
   **Tiempo estimado de arreglo:** 10 min para un ajuste inmediato de frequency cap / ampliación de audiencia; el refresco real de creativo (pieza nueva) toma más tiempo de producción.

2. **[ALTO] Fragmentación de presupuesto — M17 y M-ST1 FAIL**
   13 ad sets para $1,098.54 en 30 días = ~$2.82/día promedio por ad set. Los más chicos (Resto·Acero FORM $0.59/día, PA·Acero FORM $0.88/día, GT·Acero FORM $0.87/día) están muy por debajo del mínimo de $5/día, y ni siquiera el ad set más grande de toda la cuenta (MX·Acero WSP SMS, $7.19/día) llega al umbral de PASS ($10/día). Con presupuestos tan chicos, ad sets como PA·Acero FORM gastan menos por día de lo que cuesta un solo lead ($0.88/día vs CPL de $1.47) — la cuenta no alcanza ni 1x su propio CPA en varios ad sets, muy lejos del 5x recomendado. Esto también es la explicación más probable (no confirmada) de por qué M13 (fase de aprendizaje) es de alto riesgo: varios ad sets reciben menos de 10 conversiones por semana.
   **Tiempo estimado de arreglo:** 15-30 min para consolidar geo-splits chicos en un solo ad set con presupuesto mínimo de $10/día.

3. **[ALTO] Mercado España con 0% de cobertura**
   El negocio declara vender a "LatAm y España", pero **ninguna** de las 39 filas de `por-pais.json` corresponde a España (ES). Los países con pauta activa son: CL, CR, EC, SV, GT, MX, PA, US (+ una fila "unknown"). Esto no es un check numerado del framework estándar, pero es un hallazgo de negocio de alto impacto: un mercado objetivo declarado tiene cero inversión y cero alcance en la ventana auditada.
   **Tiempo estimado de arreglo:** 10 min para agregar España a la segmentación de al menos un ad set de MASTER FORM V2 o ACERO FORM.

4. **[ALTO] Solapamiento entre las dos campañas de ACERO (M16/M19) — WARNING**
   "[JUL] ESPE.1 ACERO - WSP SMS" y "[AGOSTO] ESPE.1 ACERO - FORM" corren en simultáneo sobre los mismos países (MX, EC, GT, PA + resto) para el mismo producto, compitiendo probablemente por la misma audiencia en la misma subasta.
   **Tiempo estimado de arreglo:** 15 min para revisar overlap real en Ads Manager y aplicar exclusiones si corresponde.

5. **[MEDIO] Objetivo desalineado en campaña de tráfico IG (M18) — WARNING**
   La campaña "🟢[12MAYO] TRÁFICO AL PERFIL - IG" usa objetivo LINK_CLICKS (no leads), con CTR altísimo (10-14%) pero prácticamente cero leads reales (1 conversación de WhatsApp en 30 días para $82.37, ~7.5% del gasto total). Puede ser intencional para alimentar el crecimiento orgánico de la cuenta (ver estrategia de contenido en `matriz-viral/CLAUDE.md`), pero no aporta al KPI de leads del trimestre.
   **Tiempo estimado de arreglo:** 10 min para decidir si se pausa/reduce o se reclasifica como gasto de "marca", separado del KPI de leads.

6. **[MEDIO] Diversidad creativa limitada (M-AN1) — WARNING**
   Solo 6 conceptos creativos base distintos sostienen 5 campañas activas durante 30 días — por debajo del umbral de 10 que recomienda el framework para evitar supresión por Similarity Score de Andromeda. Los archivos "a-j" por concepto parecen ser recortes por placement, no variantes de mensaje/ángulo.
   **Tiempo estimado de arreglo:** no es un quick fix — requiere producción de nuevos conceptos (angulo, hook, formato).

---

## Quick Wins (menos de 15 minutos, ordenados por impacto)

| # | Acción | Impacto estimado | Tiempo |
|---|---|---|---|
| 1 | Pausar/reducir "🟢 TRÁFICO AL PERFIL - IG" (LINK_CLICKS, ~7.5% del gasto, casi sin leads) y reasignar a ACERO FORM (mejor CPL, ~$0.48/lead) | Libera ~$82/mes hacia el KPI real del trimestre | 10 min |
| 2 | Agregar España como país objetivo en MASTER FORM V2 o ACERO FORM | Abre un mercado declarado con 0% de cobertura actual | 10 min |
| 3 | Agregar exclusión de audiencia cruzada entre las dos campañas de ACERO | Reduce competencia interna en subasta | 15 min |
| 4 | Ajustar frequency cap en el ad set COMPORTAMIENTOS de MASTER FORM V2 | Frena la fatiga mientras se produce refresco real de creativo | 10 min |
| 5 | Subir 1 video vertical 9:16 + 1 carrusel de prueba en ACERO FORM | Diversifica formato (hoy 100% imagen estática en el sample de ganadores) | 15 min |

---

## Bandera de fatiga creativa (detalle)

**Campaña:** 🟡[18MAYO] MASTER - FORM V2 · ad set "COMPORTAMIENTOS"
- CTR primeros 7 días: **2.49%** (21.349 impresiones)
- CTR últimos 7 días: **1.82%** (21.982 impresiones)
- Caída relativa: **−27%** (por tercios: −29%)
- **CORRECCIÓN:** el agente reportó ~45-50% comparando el mejor día del inicio
  (2.91%) contra el peor del final (1.45%). Comparar extremos infla la caída.
  Sobre volúmenes equiparables la caída real es de 27%. Sigue superando el
  umbral de FAIL del framework (>20%) y la frecuencia 4.37 lo confirma: el
  hallazgo se mantiene, la magnitud era otra.
- Frecuencia acumulada 30 días (adset): **4.37** — banda de riesgo para prospecting (umbral WARNING 3.0-5.0)
- Frecuencia por país dentro de esta campaña (30 días): EC 4.70, PA 4.11, CL 3.99, GT 3.90, MX 3.22, CR 3.54, US 2.48 — la mayoría ya en zona de saturación
- Veredicto: **FAIL** según criterio del framework (caída de CTR >20% + frecuencia elevada = fatiga confirmada)

Las otras 3 campañas de leads/ventas (ACERO WSP SMS, MASTER BIM+IA WSP API, ACERO FORM) mantienen CTR estable en toda la ventana — sin señal de fatiga.

---

## EMQ — qué se necesitaría para recomendar algo concreto

No hay ningún dato de EMQ en el export (ni Purchase, ni Lead, ni PageView). **No se inventa un número.** Para poder dar una recomendación real de EMQ se necesita conectar Events Manager (vía MCP de Meta o acceso directo) y revisar:
- EMQ de Purchase (objetivo ≥8.5) — relevante para el evento de depósito/pago del Máster.
- EMQ de Lead (evento clave del trimestre).
- Dedup rate entre pixel y CAPI (objetivo ≥90%).
- Si CAPI está corriendo en paralelo al pixel del lado del servidor, dado que el negocio depende fuertemente de WhatsApp (eventos `onsite_conversion.messaging_conversation_started_7d`), que suelen tener menor calidad de match que eventos con email/teléfono explícito.

Sin esos tres datos, cualquier cifra de EMQ que se reporte aquí sería inventada — por eso queda fuera del score.

---

## Compliance

- **Special Ad Category:** el giro del negocio es formación/educación (BIM/ingeniería), no vivienda, empleo, crédito ni productos financieros — **no aplica** Special Ad Category según lo observable en nombres de campaña y objetivos. No se detectó bandera de incumplimiento en el export.
- **Consent Mode V2:** es un concepto de Google Ads/GA4, no de Meta — fuera del alcance de este audit de Meta Ads. Si el sitio usa GA4 en paralelo para medir el funnel de leads, conviene revisarlo en el audit de Google/Analytics, no aquí.
- **Verificación de dominio, CAPI Gateway, atribución post-enero 2026:** no verificables desde este export — ver sección de cobertura arriba.

---

## Archivos generados

- `/home/user/meta-ads-dashboard.html/meta-audit-results.json` — validado contra el schema del framework (`platform: meta`, `data_source: export`).
- `/home/user/meta-ads-dashboard.html/meta-audit-results.md` — este archivo.
