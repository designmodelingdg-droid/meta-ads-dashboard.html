# Matriz de Contenido Viral — Design Modeling Academy

**Actualizada:** 2026-07-08 (base) · 2026-07-16 (+DM18 y re-medición de 10 reels — ver §"Actualización 2026-07-16")
**Cuentas analizadas:** 2 en Instagram (`@bimpure`, `@design_modeling_dg`)
**Reels totales:** 37 (BIM Pure: 19 · DMA: 18)
**Fuente cruda:** `fuentes/ig_bimpure.json` + `fuentes/ig_design_modeling_dg.json` + `fuentes/ig_design_modeling_dg_reel_Da1ABdbJ7ji_2026-07-16.json` + `fuentes/ig_design_modeling_dg_ultimos10_2026-07-16.json`
**Referente descartado:** Dana de Filippi (`@danadefilippi` privada/sin reels visibles, `@danamobim` no existe). No se pudo confirmar handle. Se sigue el análisis con solo 2 cuentas.

---

## Convenciones y advertencias sobre los datos

- **ID:** `BP#` = @bimpure · `DM#` = @design_modeling_dg. La numeración es la posición del reel en su respectivo dataset ordenado por views desc dentro de cada cuenta. La tabla de abajo mezcla ambas cuentas ordenadas por views globalmente.
- **Sh (shares):** todos `s/d` (sin dato). El add-on `includeSharesCount` de Apify está OFF por regla de costo ($0.007 extra por reel).
- **Estructura:** categorización del formato/gancho principal (creada aquí para uso interno de la matriz).
- **Hook:** primeros ~10-15 palabras de la transcripción de audio (los primeros ~3 segundos aproximados). Cuando el audio del reel es CC de TikTok sin narración propia, se marca `s/d (audio-CC)` porque no es hook narrativo de la marca.
- **Nota:** observación de por qué performa (o no).

**Reels con transcript parcial o sospechoso — flags manuales:**

- **BP4:** transcript devuelto = `"Hello, how may I help you?"`. Duración real 16s. Muy improbable que sea el hook real. Bandera para re-verificar (posiblemente el video tiene voz muy baja o música que confundió al transcript engine).
- **DM4, DM6, DM9:** reels de humor con audio importado (CC de TikTok, sin voz de DMA). Los transcripts salen vacíos o con letra de canción de fondo. El hook narrativo real es el texto en pantalla del reel, que **no lo tenemos scrapeado** (Apify solo devuelve transcript de audio, no texto visual). Se marcan `s/d (audio-CC)`.

---

## Tabla completa — 36 reels ordenados por views desc

| ID | Cuenta | Fecha | Dur | Views | Likes | Comm | Sh | Tema | Estructura | Hook | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DM1 | @design_modeling_dg | 2026-06-25 | 19s | 19,934 | 443 | 4 | s/d | Humor voladizo arqui vs inge | DIÁLOGO-HUMOR | "¿Estás dentro o fuera? ¿De qué hablas, dentro o fuera de qué?" | Top view absoluto. CC de TikTok (@marcos_a_z_) reutilizando meme de película. Corto + tensión narrativa (cliffhanger) |
| DM2 | @design_modeling_dg | 2026-06-18 | 19s | 19,486 | 190 | 11 | s/d | Material sorpresa: caucho de poliurea | REVELACIÓN-MITO | "Esto parece concreto, pero mira lo que pasa: se puede doblar como si fuera goma." | Patrón "parece X pero no es" + demostración visual + pregunta cierre "¿lo conocías?". CC de TikTok |
| DM3 | @design_modeling_dg | 2026-06-14 | 73s | 17,031 | 279 | 4 | s/d | Por qué el concreto necesita acero (tensión) | PREGUNTA-REVELACIÓN | "Si el concreto es tan fuerte, ¿por qué le ponen varillas de acero?" | Pregunta que todo estudiante se hace + explicación técnica clara. 73s largo pero funciona porque el hook es una duda universal |
| DM4 | @design_modeling_dg | 2026-06-30 | 13s | 7,926 | 222 | 0 | s/d | Humor obra: 3 verdades del trabajo | LISTICLE-HUMOR | s/d (audio-CC, sin narración) | Sin audio hablado, se apoya en texto en pantalla + listicle de 3 puntos + humor Coca-Cola. Ratio likes/views 2.8% (el más alto de la matriz) |
| DM5 | @design_modeling_dg | 2025-05-17 | 63s | 7,688 | 72 | 5 | s/d | Certificaciones internacionales Autodesk | PREGUNTA-DESDE-COMENTARIOS | "Uno de los comentarios que más me preguntan, ¿para qué sirven realmente las certificaciones internacionales de Autodesk?" | Promo camuflada de curso DMA usando pregunta real recurrente como hook |
| DM6 | @design_modeling_dg | 2026-06-11 | 10s | 7,577 | 102 | 3 | s/d | Humor: mientras albañiles trabajan, arquis conversan | DIÁLOGO-HUMOR | s/d (audio-CC: letra de canción de fondo) | Ultra corto (10s) + humor visual + relatable. CC de TikTok (@arqbooksc) |
| DM7 | @design_modeling_dg | 2024-05-07 | 70s | 6,847 | 60 | 11 | s/d | Promo título universitario US (Sabal University) | PROMO-ANUNCIO | "Tenemos una excelente noticia para ti." | Formato promo directo. Buena performance atípica para promo pura — probable boost por tema "título internacional" |
| DM8 | @design_modeling_dg | 2026-06-23 | 53s | 5,660 | 99 | 0 | s/d | Cómo se construye una losa deck | TUTORIAL-CONSTRUCCIÓN | "¿Has visto este tipo de losas? Aquí te cuento cómo se construyen." | Hook interrogativo directo + paso a paso técnico corto |
| DM9 | @design_modeling_dg | 2026-06-21 | 13s | 5,273 | 65 | 0 | s/d | Humor: fingir inspección para no responder | DIÁLOGO-HUMOR | s/d (audio-CC: letra de canción de fondo) | Ultra corto + situación relatable de la industria. CC de TikTok (@arquingenio) |
| DM10 | @design_modeling_dg | 2026-06-16 | 6s | 4,768 | 35 | 0 | s/d | Humor: cliente ofrece "monedita" por dibujitos | DIÁLOGO-HUMOR | "Claro, el rico piensa que con una monedita puede comprar al pobre." | El más corto de toda la matriz (6s) + rabia comunitaria del gremio arqui. CC de TikTok |
| DM11 | @design_modeling_dg | 2026-06-28 | 83s | 4,180 | 94 | 3 | s/d | Errores en mampostería reforzada | ADVERTENCIA-ERROR | "Pasó lo que no debía pasar. A veces cometemos un grave error..." | Hook de tensión ("lo que no debía pasar"). Largo (83s) pero funciona en contenido técnico de obra |
| DM12 | @design_modeling_dg | 2026-07-02 | 37s | 3,619 | 63 | 0 | s/d | Pernos de anclaje acero-concreto | PREGUNTA-REVELACIÓN | "¿Sabes cómo se fija una estructura de acero al concreto?" | Pregunta que ing. civil se hizo alguna vez + explicación técnica corta |
| BP1 | @bimpure | 2026-03-09 | 32s | 3,611 | 97 | 1 | s/d | Historia Slantis (arquitectura tech) | STORY-DOCUMENTAL | "Are we rolling? Hola, what does that mean? I traveled to Uruguay and Argentina to meet Slantis..." | Top view de BIM Pure. Humor bilingual + travel + "detrás de la empresa". Idioma inglés |
| DM13 | @design_modeling_dg | 2026-01-06 | 120s | 3,349 | 22 | 4 | s/d | Curso IA aplicada a BIM (BIM Manager) | PROMO-CURSO | "La continuidad de cómo se va a conectar directamente con el módulo 1..." | Máxima duración de la matriz (120s). Promo directa con engagement bajo (likes/views 0.66%) |
| DM14 | @design_modeling_dg | 2026-06-17 | 73s | 1,544 | 17 | 8 | s/d | Análisis estructural: derivas y deformaciones | TUTORIAL-TÉCNICO | "va a indicarnos cuáles son las deformaciones, cuáles son las derivas..." | Muy nicho (ing. estructural). Hook comienza en medio de frase — mala edición del inicio |
| DM18 | @design_modeling_dg | 2026-07-15 | 40s | 1,453 | 32 | 27 | s/d | ChatGPT diseña una losa → la IA falla en el criterio, no en la fórmula (BIM+IA original) | MITO/EXPECTATIVA-VS-REALIDAD | "Le pedí a ChatGPT que me diseñara una losa de entrepiso y esto fue lo que pasó." | ⭐ **27 comentarios — récord absoluto de la matriz** (top previo: DM2 con 11). Primer reel con CTA real "comenta BIM o IA" → validó el fix de §5 (cuenta genera views, no conversación). Views 1,453 pero medido a <24h de publicado. Likes/views 2.2% (top-3 de la cuenta). Sh `s/d`: `includeSharesCount` no está disponible en plan free de Apify. Datos al 2026-07-16 |
| BP2 | @bimpure | 2025-05-05 | 42s | 1,221 | 24 | 0 | s/d | Recurso gratis: colección de íconos Revit | PROMO-RECURSO | "This is the brand new Revit's icon collection by Beam Pure, which includes different colors for different yearly release." | Regalo gratis + soporte multilenguaje. Palabra clave "free download" |
| BP3 | @bimpure | 2025-05-20 | 65s | 1,204 | 22 | 1 | s/d | Curso D5 render con líder de KPF | PROMO-CURSO | "Hi everybody, my name is Andy Crisoforo. I lead the visualization and AI efforts at KPF" | Autoridad de firma top (KPF) + promesa "amazing renders" |
| BP4 | @bimpure | 2024-09-19 | 16s | 1,177 | 43 | 1 | s/d | Lanzamiento revista BIM & BEYOND | NOTICIA-LANZAMIENTO | "Hello, how may I help you?" ⚠️ transcript sospechosa | Corto (16s), announcement. Transcript claramente incompleto — bandera manual |
| BP5 | @bimpure | 2025-05-29 | 102s | 1,166 | 32 | 0 | s/d | Vibe-coding con ChatGPT en Revit | TUTORIAL-IA | "Hello everybody and welcome to a new BIMpure video. In this one, we're going to do some vibe coding inside of Revit." | Tema trendy (vibe-coding) + IA + Revit. Formato tutorial largo (102s) — top-3 en duración de BP |
| DM15 | @design_modeling_dg | 2026-07-01 | 53s | 1,067 | 2 | 0 | s/d | Serie "Noticias BIM que SÍ importan" — ep. 1 | NOTICIA-SERIE | "¿Hasta dónde puede llegar la IA en el mundo BIM? Te lo cuento." | Hook fuerte pero engagement mínimo (2 likes / 1067 views = 0.19%). Recién lanzada + rebrand de serie sin audiencia establecida |
| DM16 | @design_modeling_dg | 2026-07-05 | 45s | 997 | 9 | 2 | s/d | Revit + Power BI + IA (dashboard) | TUTORIAL-INTEGRACIÓN | "¿Sabía que con Power BI y la inteligencia artificial podemos cambiar cómo identificamos nuestra data y la interpretamos?" | Combo triple (IA + BI + BIM). Muy alineado con línea editorial DMA pero engagement bajo |
| BP6 | @bimpure | 2025-04-16 | 36s | 948 | 29 | 0 | s/d | Mini-curso: ChatGPT para BIM Managers | PROMO-CURSO | "Hey everybody, my name is Stefan and I'm the founder and CEO of AI in AEC. The point of this masterclass is to teach you how to fully utilize ChatGPT" | Founder credential + AI angle + promesa de "30 use cases" |
| BP7 | @bimpure | 2024-08-23 | 58s | 881 | 21 | 0 | s/d | Autodesk Content Catalog release | NOTICIA-PRODUCTO | "Content Catalog for Revit has just been released." | Noticia straight de Autodesk. Timing importante para BIM Managers |
| BP8 | @bimpure | 2025-06-20 | 65s | 829 | 15 | 0 | s/d | D5 Render vs Enscape | COMPARACIÓN-VS | "This video will explore what makes DeFi so special. Seven years ago, we published an article called Comparing Six Revit Rendering Plugins." | Angle "who wins" + throwback ("hace 7 años") + reveal del cambio de ganador |
| BP9 | @bimpure | 2024-12-09 | 62s | 823 | 17 | 0 | s/d | Plugin Guardian para worksets | PROMO-PLUGIN | "With worksets, and especially using Revit templates, you rely on users to create their own worksets." | Pain point directo (chaos de worksets manuales) + solución del plugin |
| BP10 | @bimpure | 2025-03-04 | 58s | 781 | 8 | 0 | s/d | Mini-curso Open BIM | PROMO-CURSO | "Hi, I am Henrik Groth Levin. I'm a former carpenter turned into a digital nerd." | Origin story memorable ("carpintero → digital nerd") — hook diferenciador dentro del cliché "Hi, I'm X" |
| BP11 | @bimpure | 2024-11-29 | 35s | 760 | 12 | 1 | s/d | Webinar gratis: familias de ventanas en Revit | PROMO-WEBINAR | "Hello, this is Nick from BIMpure. I am hosting a webinar about high-quality Revit Windows families that is on Monday, December 2nd at 11 a.m. Eastern." | Free live event + voz del founder de BIM Pure (Nick) — más autoridad |
| BP12 | @bimpure | 2024-08-28 | 56s | 756 | 15 | 1 | s/d | Revizto mixed-reality en obra | ENTREVISTA-TECH | "Just to be clear, so that means you're pointing your phone or your iPad and you can see kind of the reality but mixed with the plan, both the floor plan and the 3D view, right?" | Cool feature demo (AR + BIM) revelado desde entrevista |
| BP13 | @bimpure | 2024-09-16 | 50s | 744 | 11 | 0 | s/d | Importancia de la coordinación BIM | ENTREVISTA-OPINIÓN | "So people are also asking me, like the clients who I'm working, why it's so important. In my opinion, as an engineer, we shouldn't rely on common sense of people, but rely on processes..." | Q&A del cliente convertido en content + autoridad del entrevistado |
| BP14 | @bimpure | 2024-11-12 | 73s | 632 | 6 | 0 | s/d | Hollow Knight ($195M / 3 devs) como analogía para BIM | STORY-ANALOGÍA | "One game that I especially love is Hollow Knight. And because it's a video game, it's software. And that means lines of code..." | Analogía inesperada (indie gaming → BIM software) + narrativa fuerte. Engagement bajo pese al concepto llamativo |
| BP15 | @bimpure | 2024-10-01 | 68s | 597 | 17 | 0 | s/d | "Deuda técnica" aplicada a arquitectura | ENTREVISTA-CONCEPTO | "Okay, another thing that I really wanted to talk about for people is an article that you wrote, Technical Debt, Architecture's Ticking Time Bomb" | Concepto de software (deuda técnica) importado a arquitectura. Nicho conceptual |
| BP16 | @bimpure | 2024-08-15 | 54s | 581 | 13 | 0 | s/d | Mini-curso: desarrollo con Revit API | PROMO-CURSO | "Hi everybody. Welcome to this mini course about learning Revit API." | Nicho técnico (API) + producto de Erik Frits (@LearnRevitAPI) |
| BP17 | @bimpure | 2024-08-21 | 66s | 558 | 8 | 0 | s/d | Ehsan (creador pyRevit) usa Notion | ENTREVISTA-HERRAMIENTA | "One of the first things that I looked into Notion is that can I export all the data that I have in Notion into HTML" | Cross-industry tip (Notion) desde figura reconocida (pyRevit) |
| BP18 | @bimpure | 2024-09-23 | 105s | 516 | 8 | 0 | s/d | IA para autogenerar detalles Revit | ENTREVISTA-IA | "So the idea is that you could upload your own details and then the AI would match the Revit model, the simple Revit model, to an actual detail from your own firm, right?" | Feature futurista (AI + arch details) + nicho AECtech. Larga (105s) |
| BP19 | @bimpure | 2024-10-18 | 79s | 504 | 12 | 1 | s/d | Claude vs ChatGPT para Revit API | ENTREVISTA-COMPARACIÓN | "I find Claude's interface is a lot sort of user-friendly. ChatGPT has custom GPTs. Claude has what are called projects." | AI-tool tribalism (Claude vs GPT) + Revit API dev |
| DM17 | @design_modeling_dg | 2026-07-07 | 53s | 413 | 4 | 0 | s/d | FAQ curso SAP2000 Naves Industriales | PROMO-FAQ | "Las tres preguntas más frecuentes que me hacen sobre SAP 2000 las respondo rápido y sin rodeos." | Formato FAQ + promo curso. Recién publicada (7 jul) — muestra pequeña, aún no medible |

---

## Actualización 2026-07-16 (corrida Apify — reel DM18 + re-medición de 10 reels)

Corrida real de `apify/instagram-reel-scraper` (plan free, ~$0.004). Se agregó el reel nuevo **DM18** (`Da1ABdbJ7ji`) y se re-midieron 10 reels de `@design_modeling_dg` para ver cómo evolucionaron desde el snapshot del 2026-07-08. `includeSharesCount` sigue devolviendo `s/d` — **el add-on de shares no está disponible en el plan free de Apify** (lo confirmó el log: `includeSharesCount is not supported for free users`), no es decisión de costo esta vez.

### El reel nuevo — DM18 (ChatGPT diseña una losa)

- **Views 1,453 · Likes 32 · Comentarios 27 · Sh s/d.** Publicado 2026-07-15 21:11, medido 2026-07-16 (~16 h de vida).
- **27 comentarios rompe el techo histórico de toda la matriz** (máximo previo: DM2 con 11; el top de views DM1 tenía 4). Es el primer reel con el CTA real "comenta BIM o IA" y es evidencia directa de que el fix de §5 (la cuenta genera views, no conversación) funciona.
- Tasa de conversación: 27/1,453 = **1.86%** vs. el ~0.02% del reel top histórico. ~90× la media de la cuenta.
- Ver comparación completa contra la estimación en `guiones/2026-07-08_chatgpt-losa-revit/simulacion.md` → §"Resultado real".

### Re-medición de reels ya en la matriz (07-08 → 07-16)

| ID | shortCode | Fecha pub | Views 07-08 → 07-16 | Likes → | Comm → | Lectura |
|---|---|---|---|---|---|---|
| DM4 | DaNg_igD_LC | 2026-06-30 | 7,926 → **8,989** | 222 → 248 | 0 → 0 | Sigue creciendo; humor 14s confirma top-tier (ratio likes 2.76%) |
| DM5 | DJwlI94tck3 | 2025-05-17 | 7,688 → 7,709 | 72 → 72 | 5 → 5 | Plano — reel viejo, fuera de feed (confirma §4.6) |
| DM7 | C6rnuz7upu7 | 2024-05-07 | 6,847 → 6,869 | 60 → 61 | 11 → 11 | Plano — maduro |
| DM12 | DaTwRB3pCN1 | 2026-07-02 | 3,619 → **4,992** | 63 → 83 | 0 → 3 | Buen crecimiento (+38%); hook-pregunta sigue tirando |
| DM13 | DTJlMHiCczr | 2026-01-06 | 3,349 → 3,370 | 22 → 22 | 4 → 4 | Plano — promo larga sin recorrido |
| DM16 | Daa2ZnORqWR | 2026-07-05 | 997 → **1,341** | 9 → 11 | 2 → 2 | Subió pero sigue en tier bajo (educativo puro) |
| DM15 | DaQ71d0peMU | 2026-07-01 | 1,067 → 1,308 | 2 → 4 | 0 → 0 | Serie nueva sigue sin despegar (confirma §2.5) |
| DM17 | Daglc57JSrQ | 2026-07-07 | 413 → **1,071** | 4 → 4 | 0 → 0 | Se estabilizó ×2.6, pero sigue tier bajo (promo-FAQ) |

**Reel detectado que NO estaba en el snapshot 2026-07-08:** `DaWCI-cJn8i` (2026-07-03, 63s, 1,193 views / 4 L / 1 C, "¿Sabías que una tabla de Revit puede decirte…?"). Quedó fuera de la recolección original; se anota aquí como hueco a integrar en la próxima pasada completa, no se le asignó ID todavía.

> Nota de medición: la corrida dedicada al reel y la de perfil se lanzaron con ~30 s de diferencia; DM18 aparece como 1,455/28 en la de perfil y 1,453/27 en la dedicada (números vivos que suben minuto a minuto). Se usa la corrida dedicada como valor de registro.

---

## Observaciones al vuelo (pendientes de destilar en `patrones.md`)

Notas rápidas sin conclusión definitiva. Se procesan en el siguiente paso.

**Sobre @design_modeling_dg (tu cuenta):**

- Los 3 tops (>17k views) todos usan **DIÁLOGO-HUMOR** o **REVELACIÓN-MITO** en formato corto (19-73s).
- **5 reels de humor con CC de TikTok** (DM1, DM4, DM6, DM9, DM10) — TODOS entre 4.7k y 20k views. Es el patrón más consistente de la cuenta.
- **4 reels con hook de pregunta** (DM3, DM5, DM8, DM12) — todos superan 3k views. Es el segundo patrón fuerte.
- **Contenido puramente educativo técnico sin humor** (DM14, DM16) — engagement bajo (<1.5k views).
- **Promos puras** — resultados mixtos: DM7 (título US, 6.8k) funcionó; DM13 (curso IA+BIM, 3.3k) y DM17 (SAP2000, 413) menos.
- **Nueva serie "Noticias BIM que SÍ importan"** (DM15) tiene hook fuerte pero engagement mínimo — puede necesitar 2-3 episodios para estabilizarse.
- **Todos los reels bajo 20s en tu cuenta superan 4.7k views.** Duración parece ser factor de fuerza cruda.

**Sobre @bimpure (referente B2B tech):**

- Views concentrados 500-1,200 — audiencia mucho más chica que DMA pero más pro/nicho.
- **Estructura dominante: ENTREVISTA + PROMO-CURSO.** BIM Pure funciona como network de expertos + tienda de cursos.
- Top view (BP1, 3,611) rompe patrón — es un STORY-DOCUMENTAL de viaje/empresa (Slantis) con humor bilingual. La única pieza sin formato "hi, my name is X".
- **Ratio likes/views más consistentes en BP** (~1.5-3%) que en DMA — audiencia más pequeña pero más comprometida.
- Contenido IA (BP5 vibe-coding, BP6 ChatGPT BIM Managers, BP18 AI details, BP19 Claude vs GPT) — 4 piezas. Tu ángulo BIM+IA calza directo con lo que ellos publican.

**Diferencias entre cuentas — implicación para DMA:**

- DMA es **B2C-ES-humor-viral** con picos de 20k. BIM Pure es **B2B-EN-tech-nicho** con techo ~3.6k.
- Tu edge sobre BIM Pure: idioma ES + humor + brevedad. Su edge sobre ti: profundidad técnica + red de expertos entrevistados.
- **La intersección BIM+IA** (tema declarado en `CLAUDE.md`) tiene cobertura en BIM Pure (4 piezas) pero casi nada en DMA (solo DM13 promo curso, DM15 serie recién lanzada, DM16 tutorial Power BI). Hay espacio grande para producir contenido BIM+IA en formato humor+revelación que DMA sabe hacer.

**Pendiente:**

- Re-verificar BP4 (transcript sospechoso — solo devolvió "Hello, how may I help you?" para un reel de 16s).
- Ampliar cobertura de DMA con reels más antiguos si necesitamos más data (los 17 actuales cubren mayo 2024 – julio 2026).
