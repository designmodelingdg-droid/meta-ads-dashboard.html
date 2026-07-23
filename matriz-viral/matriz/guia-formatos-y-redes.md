# Guía de formatos y redes — Sistema de contenido mensual DMA

**Fecha:** 2026-07-21 · **Base:** aprendizajes reales de `matriz-contenido-viral.md` y `patrones-de-viralidad.md`.

La idea: **una sola idea núcleo → muchas piezas**, adaptadas a cada formato y a cada red. No republicar lo mismo en todos lados — cada red habla distinto.

---

## 1. Regla de oro (de las estadísticas reales)

- **Eje:** ≥60% del mes debe ser **NÚCLEO BIM + IA** (lo que vende), no obra. La obra solo como gancho que puentea al núcleo.
- **Fórmula ganadora** (los 2 mejores posts, 8.5% engagement): **núcleo + demo concreta (visual) + CTA de comentar**.
- **Lo que NO:** promo de curso pura sin gancho (el "3 FAQ SAP2000" tuvo 5,195 views y 0 comentarios). Alcance alto ≠ negocio.

---

## 2. Los 3 formatos de Instagram (y para qué sirve cada uno)

| Formato | Trabajo principal | Cuándo usarlo | Evidencia |
|---|---|---|---|
| **Reel** | Alcance / descubrimiento | Idea con demo en video, humor, reveal | El motor de reach |
| **Carrusel** | Guardado + autoridad | Listicles, pasos, "cómo se hace" | El de mejor engagement (8.5%, 46 guardados) |
| **Post plano** | Conversación rápida / lead magnets | Un mensaje fuerte, un regalo, una frase | El post de zapatas: 35 comentarios |

> Regla práctica: **cada idea núcleo se publica en los 3 formatos a lo largo del mes** (no el mismo día). El reel capta, el carrusel da autoridad y guardados, el post plano abre conversación.

---

## 3. Adaptación por red (misma idea, distinto idioma)

### 📸 Instagram (casa base)
- Reels (alcance) · Carruseles (guardado) · Post plano (conversación).
- Tono cercano-técnico, español neutro, **subtítulos quemados**.
- **CTA: "comenta BIM o IA"** (dispara el bot).
- Hashtags: 8-15, mezcla nicho + amplios.

### 💼 LinkedIn (aquí está el comprador del Máster)
- **Formato estrella: post de TEXTO largo** (historia/insight profesional en primera persona) + imagen o **carrusel en PDF** (documento). Video nativo sí, pero más "profesional" que casual.
- Tono profesional, sin "comenta la palabra X". **CTA = pregunta abierta** ("¿cómo lo manejan en sus proyectos?") o "escríbeme por DM".
- Ángulos que pegan: ROI, liderazgo, carrera, casos reales, "lección aprendida", opinión de industria. El ángulo **"IA vs criterio"** encaja perfecto aquí.
- Hashtags: 3-5 profesionales (#BIM #BIMManagement #AECtech #IngenieríaEstructural).
- **Úsalo para:** posicionar el Máster ante decisores y empresas.

### ▶️ YouTube (autoridad + búsqueda)
- **Dos modos:** (a) **Shorts** = reutiliza el reel vertical tal cual (descubrimiento); (b) **video largo 5-15 min** = el mismo tema expandido a tutorial real paso a paso (autoridad + SEO).
- Ej: el reel "3 cosas que Revit hace con IA" → video largo "Cómo activar la IA de Revit: 3 funciones paso a paso (2026)".
- **Título SEO** (piensa en búsqueda) + **descripción con enlaces** (Máster, lead magnet, curso).
- CTA: "link en la descripción" + suscríbete.
- **Úsalo para:** autoridad duradera y captar por búsqueda a largo plazo.

### 🎵 TikTok (descubrimiento nuevo, público joven)
- Reutiliza el reel pero con **energía TikTok**: hook aún más rápido (1er segundo), audio/tendencia, ritmo, texto en pantalla nativo, más crudo/auténtico.
- Menos corporativo, más directo. Humor y reveals funcionan muy bien.
- **CTA: "link en bio"** (TikTok penaliza links directos) + pedir comentarios.
- **Úsalo para:** alcance nuevo y futuros estudiantes.

**Resumen del CTA por red:** IG → "comenta BIM/IA" · LinkedIn → pregunta abierta/DM · YouTube → "link en descripción" · TikTok → "link en bio".

---

## 4. Espacios recurrentes del mes (fijos, no negociables)

Además del contenido núcleo, cada mes reserva:

- **📝 Blog (1-2/mes):** un post que dirige al blog (SEO + autoridad). En IG/LinkedIn: "escribimos sobre X → link". El blog alimenta YouTube y LinkedIn.
- **👥 Comunidad (1-2/mes):** contenido para la comunidad/membresía — recursos exclusivos, Q&A, behind-the-scenes, referencia de lo hecho en el mes.
- **🏛️ Empresa / Novedades (1-2/mes):** **proyectos, conferencias, convenciones, logros, nuevas herramientas DMA.** Muestra tracción y prueba social. Formato ideal: carrusel "lo que hicimos este mes" + versión LinkedIn. **Este es el espacio para mostrar todo lo nuevo que sale en Design Modeling.**

---

## 5. Estructura de un mes tipo (plantilla repetible)

Cadencia objetivo: 3-4 piezas/semana. Semana tipo (se repite ×4):

| Día | Pieza | Formato IG | Se adapta a |
|---|---|---|---|
| Lun | Núcleo BIM+IA (demo/reveal) | **Reel** | TikTok + YT Short + post LinkedIn |
| Mié | Núcleo / herramienta | **Carrusel** | Documento PDF LinkedIn |
| Vie | *Rota:* lead magnet · blog · comunidad · empresa-novedades | Post plano / Reel | según la pieza |
| Sáb (opcional) | Humor-diálogo o post plano rápido | Reel / Post | TikTok |

**Una vez al mes:** carrusel "Resumen del mes en Design Modeling" (proyectos/conferencias/novedades) + su versión LinkedIn.

Distribución mensual objetivo: **~60% núcleo BIM/IA · ~15% lead magnet · ~10% blog · ~10% empresa-novedades · ~5% comunidad/humor.**

---

## 6. Cómo se registra en la matriz

Cada pieza publicada entra en `matriz.json` con: `tipo` (reel/carrusel/post), `red` (instagram/linkedin/youtube/tiktok), `eje`, y sus métricas. Así medimos qué formato y qué red rinde mejor para cada tema, y ajustamos el mes siguiente sobre evidencia.
