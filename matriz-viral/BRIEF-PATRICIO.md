# Brief de contenido — Matriz Viral BIM+IA (Design Modeling Academy)

**Para:** Patricio (estrategia de contenido / publicaciones)
**De:** Dayana + Claude (análisis de datos reales de Instagram)
**Actualizado:** 2026-07-16 (reescrito sobre el barrido completo)
**Fuente viva:** carpeta `matriz-viral/` en el repo `meta-ads-dashboard.html`, [PR #3](https://github.com/designmodelingdg-droid/meta-ads-dashboard.html/pull/3). Datos legibles por máquina en `matriz/matriz.json`.

> ⚠️ Este brief reemplaza al del 2026-07-08. Aquel se basaba en 17 reels (~14% de la cuenta) y concluía cosas que el barrido completo (124 reels) corrigió. Lee este.

---

## El diagnóstico, en una frase

**La cuenta se viraliza con OBRA/construcción, que trae al público equivocado.** Hay views millonarias (hasta 4.7M en un reel) pero **casi ningún lead que compre el Máster BIM+IA**, porque el 99% del alcance viene de contenido de obra (obreros, curiosos del gremio) y no de ingenieros/arquitectos que modelan desde la computadora — que son quienes compran.

Los números (124 reels reales):

| Eje | % de piezas | % del alcance |
|---|---|---|
| 🏗️ OBRA (construcción/humor de campo) | 62% | **98.8%** |
| 🎯 NÚCLEO BIM + IA (lo que se vende) | 35% | **1.2%** |

El formato viral funciona; está aplicado al tema equivocado.

---

## La estrategia (qué cambiar)

**No hacer más obra viral. Hacer el NÚCLEO (BIM / modelado / coordinación / IA "desde la computadora") con el formato que YA viraliza.**

### El formato que funciona (4 pilares — sacados de 124 reels reales)

**Pilar 1 — Hook de revelación en los primeros 3s.** Tres tipos, en orden de potencia:
1. **REVELACIÓN-TÉCNICA** — "mira este dato/técnica que no conocías" + visual (es el motor: los 4 reels sobre 1M son de este tipo).
2. **DIÁLOGO-HUMOR** — conflicto de roles del gremio (el de mejor cariño: un reel de humor tiene 9.6% de likes).
3. **PREGUNTA-REVELACIÓN** — una duda que el viewer ya se hizo.
Nunca abrir con presentación personal ni promo.

**Pilar 2 — Duración 10-75s.** Lo corto (<15s) tiene el piso más alto; pero un reveal fuerte escala a cualquier duración (el 2º reel más visto dura 72s).

**Pilar 3 — El tema debe ser NÚCLEO, no obra.** Traducir el reveal del sitio de obra a la pantalla:
- "¿Sabías que Revit detecta este choque de instalaciones antes de que cueste miles en obra?"
- "Le pedí a la IA que coordinara un modelo BIM. Mira dónde falló." (línea del reel DM18)
- "Coordinador BIM vs. el que sigue modelando a mano" (humor del núcleo)
- "3 cosas que tu Revit ya hace con IA y no sabías"
Meta de mezcla: **≥60% núcleo**; la obra solo como gancho que *puentea* al núcleo, nunca como fin.

**Pilar 4 — La conversación se diseña con el CTA.** El reach ya existe; lo que falta es conversación. Ni el reel de 4.7M pasó de 0.01% de comentarios. **El único reel que rompió el patrón (1.90%, ~100× la media) fue el que usó el CTA "comenta BIM o IA"** (DM18, un reel de IA). Ese comentario dispara el bot de ventas por WhatsApp.

### Reglas de cierre (sin excepción)
1. CTA siempre **"comenta BIM o IA"** — nunca "sígueme" ni "guarda el video".
2. Nunca precio ni "inscríbete" en el video. El Máster se vende en DM/llamada.
3. Subtítulos quemados, tono cercano y técnico, español neutro.
4. Prueba social (testimonios, acreditaciones) como contenido en pantalla, no solo como link.

---

## Cómo tienes SIEMPRE la matriz fresca (el loop)

La matriz cambia seguido. Para que tú y la app de contenido nunca trabajen con una copia vieja:

- **La fuente de verdad es el repo** (carpeta `matriz-viral/`). Nadie edita copias en Word/PDF.
- **La app** lee `matriz/matriz.json` desde la URL cruda de GitHub (build o runtime) → siempre fresca automáticamente.
- **Tú** ves la última versión abriendo `matriz/matriz-contenido-viral.md` y `matriz/patrones-de-viralidad.md` en GitHub (URL fija).
- **El loop:** cuando tengas resultados reales (views/likes/comentarios "BIM"/"IA" por pieza), pásaselos a Dayana → se re-corre el barrido de Apify → se actualiza la matriz y los patrones → confirmamos qué acertó y qué no → ajustamos los próximos guiones sobre evidencia real. Es un ciclo, no un documento cerrado.

---

## Guiones
En `matriz-viral/guiones/`. Los 5 primeros ya existen; los próximos deben nacer del Pilar 3 corregido (núcleo BIM/IA con formato de reveal/humor + CTA "comenta BIM o IA").
