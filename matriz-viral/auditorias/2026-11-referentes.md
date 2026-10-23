# Referentes para la matriz de noviembre 2026: @lexmrbim y @aecode.ai

Preparado el 23-oct-2026. Todas las cifras salen de datos públicos y llevan su fuente. Lo que no se pudo obtener aparece como **s/d**.

## 0 · De dónde salen los datos y qué falta

| Paso | Resultado |
|---|---|
| Apify (Action «Traer un post (Apify)», rama `claude/apify-referentes-nov`, run 39943744385) | **Falló.** Los 6 actores devolvieron `HTTP 403 · platform-feature-disabled · "Monthly usage hard limit exceeded"`. La cuenta de Apify ya agotó su límite mensual. **Costo cobrado: $0,00**: no llegó a arrancar ninguna corrida. Queda en `fuentes/referentes/costo-referentes-2026-10-23.json`. |
| oEmbed / og: con curl | No sirvió. La página del reel devuelve 429 y el embed llega sin datos, porque Instagram lo arma con JavaScript. |
| **Plan B: Meta Graph API `business_discovery`** (Action nueva «Referentes por Graph API», runs 39946644593 y 39947071740) | **Funcionó y es gratis.** Trajo las últimas 50 publicaciones de cada cuenta con texto, likes, comentarios, fecha y tipo, y además **vistas de los reels** (`view_count`). Los videos más fuertes se bajaron con yt-dlp, se midió la edición con ffmpeg (cortes) y se transcribieron con faster-whisper. |

**Qué no se pudo obtener (s/d):**
- guardados, compartidos y alcance en Instagram: Meta no los da de cuentas ajenas;
- el texto de las portadas y las diapositivas de los carruseles, así que el «gancho» de un carrusel es la primera línea del texto del post;
- la muestra de comentarios;
- si había música de fondo;
- si algún post tuvo pauta pagada.

**Las transcripciones son automáticas** (faster-whisper «small»). Las copio tal cual salen y marco entre [corchetes] los errores evidentes. Antes de citar una frase literal en una pieza, hay que revisarla contra el video.

**Datos crudos (rama `claude/apify-referentes-nov`, sin fusionar):**
- `matriz-viral/fuentes/referentes/meta-lexmrbim.json`: 50 publicaciones, con análisis de video y transcripción de 4 reels.
- `matriz-viral/fuentes/referentes/meta-aecode.ai.json`: 50 publicaciones, con análisis de video y transcripción de 4 reels.
- `matriz-viral/fuentes/referentes/costo-referentes-2026-10-23.json`: el intento con Apify, a $0.
- Ya existían: `matriz-viral/fuentes/edicion-ganadora/datos-2026-10-08.json` (TikTok de lexmrbim con guardados y compartidos, Apify del 8-oct) y `matriz-viral/matriz/competencia.json` (aecode.ai, 19-oct).
- Fotogramas a 1 por segundo de los 8 reels analizados: copia local en `/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/frames/`. También están como artefacto de la Action, que caduca en 3 días. No se suben al repo porque son imágenes de terceros.

---

## 1 · El reel DeGtyhfoXar (@lexmrbim): «Conecta Revit+IA paso a paso»

### 1.1 Métricas reales

| Métrica | Valor | Fuente |
|---|---|---|
| Fecha | 2026-10-05, 07:56 UTC (02:56 en Perú/Ecuador) | Graph API |
| Vistas (Instagram) | **98.570** | Graph API `view_count`, 23-oct 11:33 UTC |
| Likes | **3.471** | Graph API |
| Comentarios | **3.162** | Graph API |
| Duración | **60,6 s** | ffprobe sobre el video |
| Guardados / compartidos / alcance (IG) | s/d | Meta no los da |
| Seguidores de la cuenta | 8.431 en IG (223 publicaciones) | Graph API |
| Mediana de vistas de sus reels (24 reels, 17-ago a 21-oct) | 5.224 | Graph API |

**Ratios:**
- **18,9 veces** la mediana de vistas de sus propios reels;
- **11,7 vistas por seguidor**;
- **32,1 comentarios por cada 1.000 vistas** y 35,2 likes por cada 1.000;
- comentarios / likes = **0,91**: casi un comentario por cada like.

Como referencia, los reels de DMA sin el patrón de acusación sacan 0,54 comentarios por cada 1.000 vistas y los que lo usan 8,61 (`OCTUBRE-QUE-FUNCIONA.md`).

**El mismo video en TikTok** (casi con seguridad es el mismo: subido el 5-oct, «Conecta Revit con IA paso a paso», 60 s, pide la palabra por DM). Medición de Apify del 8-oct, guardada en `edicion-ganadora/datos-2026-10-08.json`:
- 173.200 vistas, 17.400 likes y 387 comentarios;
- **12.241 guardados** y **2.499 compartidos**.

Es la única señal de guardado y compartido que tenemos de esta pieza: **1 de cada 14 personas lo guardó**.

**Su «hermano» del mismo día** (DeHDZn4BrL-, 5-oct, 11:00 UTC): «Revit + ChatGPT paso a paso», 76,7 s, más técnico y con la cara del creador al inicio. Sacó 22.727 vistas, 790 likes y 419 comentarios (18,4 por cada 1.000). **La versión corta, informal y con menos detalle sacó 4,3 veces más vistas.** Esa comparación interna es la lección más limpia que deja el caso.

### 1.2 Texto del post (literal)

> Conecta Revit+IA paso a paso 🔥🚀 Soy Lex y te ayudo a integrar IA para tus modelos BIM con Revit.
> Comenta QUIERO y te mando el prompt y un video tutorial 🤓 #revit #ia #bim #arquitectura

### 1.3 Transcripción completa (automática, con tiempos)

```
[ 0.0– 5.6] Todavía no usas IA en Revit, entonces quédate en este video para que sepas el paso a paso,
[ 5.7– 6.1] mi King.
[ 6.4–12.1] Primero, descargas una IA de tu preferencia, que puede ser ChatGPT o Cloud [Claude], incluso si
[12.1–17.5] no tienes ninguna suscripción te va a funcionar, yo te recomiendo usar ChatGPT y si preguntas
[17.5–20.0] por qué, no preguntes, solo gózalo.
[20.3–24.7] Luego descargas PyRevit, esta diablura de plugin va a permitir la conexión de la
[24.7–28.7] IA con Revit, además, también te deja crear plugins, que golazo.
[28.7–34.3] Después de eso, vas aquí configuración de PyRevit y activas este conector de rutas,
[34.4–36.8] que va a habilitar la conexión con tu IA.
[37.1–42.1] Luego le das a tu ChatGPT el prompt que yo te voy a enviar por mensaje y se va a hacer
[42.1–47.6] esa conexión con Revit y listo, ya conectaste la IA a Revit y puedes pedirle que haga
[47.6–52.8] algunos modelados, renombrar familias, tipos y organizar tu proyecto en general.
[53.3–57.5] Comenta quiero y te mando el prompt y un video completo para que conectes la IA
[57.5–60.3] a Revit hoy mismo y también sígueme mineto [s/d: palabra no clara].
```

### 1.4 Gancho (0–3 s)

- **Dicho:** «Todavía no usas IA en Revit, entonces quédate…». Es exactamente el patrón de DMA de **acusar un hábito** («¿todavía…?») más una promesa concreta («el paso a paso»).
- **Escrito:** subtítulo blanco palabra por palabra, centrado en el tercio inferior: «Todavía no usas» → «IA en REVIT?».
- **Visual:**
  - 0–1 s: el celular, en mano, filma el monitor con una planta de Revit;
  - ~1 s: entra un **sticker-meme** (una tortuga) sobre la pantalla;
  - el primer corte llega a los 6,3 s. Lo que retiene al principio son el subtítulo, que cambia cada medio segundo, y el meme, no el montaje.
- **No hay cara** en todo el video. Es solo su voz sobre la pantalla grabada con el celular.

### 1.5 Estructura segundo a segundo

Sale de la transcripción, los cortes de ffmpeg y los fotogramas a 1 por segundo.

| Tramo | Qué se dice | Qué se ve | Función |
|---|---|---|---|
| 0–6 s | «Todavía no usas IA en Revit… quédate… paso a paso, mi King» | Monitor con planta de Revit, filmado con el celular en mano. Sticker-meme a ~1 s. Chat y vista 3D azul de Revit a ~4–5 s | Gancho de acusación, promesa y tono de pana |
| 6,3 s (corte) – 14,8 s | «Primero, descargas una IA… ChatGPT o Claude, incluso si no tienes ninguna suscripción…» | Página «Descargar ChatGPT para computadora» y después «Descargar Claude». El dedo señala el botón | Paso 1, sin barrera («gratis te sirve») |
| 14,8–18,4 s | «…yo te recomiendo usar ChatGPT» | Animación de galaxia con «GPT» / «Astra» | Respiro visual |
| 18,4–20,2 s | «y si preguntas por qué, no preguntes, solo gózalo» | **Meme en video** («NO PREGUNTES ¡SÓLO GÓZALO!») | Humor que corta la objeción «¿por qué ChatGPT?» |
| 20,2–28,9 s | «Luego descargas pyRevit, esta diablura de plugin… también te deja crear plugins, qué golazo» | GitHub de pyRevit, página de la versión v6.5.5 y la cinta de Revit con 2–3 stickers de emoji | Paso 2, con jerga y emoción |
| 28,9–37,1 s | «vas a configuración de pyRevit y activas este conector de rutas, que va a habilitar la conexión con tu IA» | Configuración de pyRevit → «Rutas» → interruptor «Servidor de Rutas (Beta)» en primer plano, con el dedo | Paso 3, el «truco» visible |
| 37,1–47,9 s | «le das a tu ChatGPT el prompt que yo te voy a enviar por mensaje… y listo, ya conectaste la IA a Revit» | Plano abierto del monitor: chat a un lado, Revit 3D al otro. Ventana de permiso «Permitir una vez». En el chat se lee «Conectado. Revit está activo y el modelo abierto es 2027-…» | **Prueba**: el momento «funciona». Retiene el dato clave (el prompt), que va por DM |
| 47,9–53,3 s | «puedes pedirle que haga algunos modelados, renombrar familias, tipos y organizar tu proyecto» | Planta, familias y vista 3D | Beneficio |
| 53,3–60,6 s | «Comenta QUIERO y te mando el prompt y un video completo… hoy mismo… sígueme» | Prompt/JSON en pantalla, VS Code y un documento de pasos | CTA con palabra y recurso concreto |

**Edición medida:**
- 12 cortes en 60,6 s (2,0 por cada 10 s);
- el primer corte llega a los 6,3 s y no hay ninguno en los primeros 3 s;
- lo que cambia cada ~0,5–1 s es el **subtítulo de 1–2 palabras**.

### 1.6 Formato y estilo de edición

- **Lo-fi auténtico:** el celular en mano filma un monitor real. Se ve la lámpara del escritorio, el dedo señalando y el reflejo de la pantalla. No hay grabación de pantalla limpia ni cara.
- **Subtítulos:** blancos con borde negro, 1–2 palabras, centrados abajo y sincronizados con la voz.
- **3 memes o stickers** colocados en los momentos de «¿y por qué?» o «¡qué bueno!». Es el humor como respiro.
- **Voz en jerga peruana y de pana:** «mi King», «diablura de plugin», «qué golazo», «no preguntes, solo gózalo». Cercanía total; no suena a profesor.
- **Tutorial en 3 pasos** que se ven en pantalla: descargar la IA → pyRevit → activar el servidor de rutas. El dato que hace que funcione (el prompt) se queda fuera y llega por DM.
- Duración de **60 s** justos.

### 1.7 CTA

«**Comenta QUIERO** y te mando el prompt y un video completo para que conectes la IA a Revit hoy mismo». Se dice en voz (53–58 s) y se repite en el texto del post. Promete **dos recursos concretos y gratis** (prompt + video), con un resultado inmediato («hoy mismo»).

### 1.8 Por qué funciona

1. **Acusación y promesa en la primera frase.** «Todavía no usas IA en Revit» le habla a quien se siente atrasado; «paso a paso» le dice que lo resuelve aquí.
2. **Tema caliente.** Conectar IA a Revit (MCP) era el tema que más vistas daba en el nicho desde octubre (`EDICION-GANADORA-NICHO.md`: 6 de los 12 TikTok más vistos).
3. **Barrera cero.** «Incluso si no tienes ninguna suscripción te va a funcionar» quita la objeción del costo.
4. **Prueba visible.** El «Conectado. Revit está activo…» en pantalla hace creíble la promesa.
5. **El recurso que falta se pide comentando.** El video da el 80 % del camino, y lo único que falta (el prompt) llega con QUIERO. Eso explica los 3.162 comentarios, y los comentarios empujan la distribución. En su cuenta, **los reels con palabra tienen una mediana de 11.183 vistas y 14 comentarios por cada 1.000; los reels sin palabra, 4.076 vistas y 0 comentarios**.
6. **Ritmo y humor.** El subtítulo cambia cada segundo y los memes entran justo en los puntos donde uno se iría.
7. **Corto y menos técnico que su «hermano».** El de 77 s con todos los pasos detallados sacó 4,3 veces menos. Gana el que promete más y explica menos.

> **Cuidado (regla 0 de CLAUDE.md):** el reel dice que la IA «puede hacer modelados, renombrar familias…». Eso solo pasa con un servidor MCP **de terceros** sobre pyRevit (en su otro reel menciona «MCP Server for Revit Python» de un autor particular). Según `EDICION-GANADORA-NICHO.md`, el conector oficial de Revit 2027 es de solo lectura. DMA no puede copiar esa promesa tal cual: hay que decir qué es oficial y qué es de terceros, con la versión, y comprobarlo en help.autodesk.com y en la documentación de pyRevit antes de grabar.

### 1.9 Tres ideas adaptadas para DMA, con Gabriel Pantoja

Base común: mismo esqueleto (acusación → 3 pasos en pantalla grabada con el celular → prueba → recurso por palabra), 45–60 s, subtítulos de 1–2 palabras, un meme como mucho y sin precios. El tono es el de DMA, cercano y técnico, sin imitar la jerga peruana de Lex.

**Idea A · Máster, bloque BIM + IA: «Conectar la IA a Revit, sin humo»**
- **Gancho exacto (0–3 s, dicho y escrito):** «¿Todavía no conectas la IA a Revit? Te lo dejo en 3 pasos… y te digo lo que nadie dice.»
- **Estructura:**
  - 0–3 s: Gabriel a cámara 1 s y después el celular sobre el monitor con Revit.
  - 3–35 s: paso 1, la IA que usamos; paso 2, el conector; paso 3, la primera consulta al modelo («¿cuántas puertas no tienen resistencia al fuego?», gancho ya validado en la ficha de anuncios de DMA).
  - 35–45 s: **la frase de criterio**: «Ojo: el conector oficial de Autodesk lee tu modelo, no lo modifica. Si alguien te promete que la IA te modela sola, pregúntale con qué add-in y en qué versión». Esta frase hay que comprobarla antes de grabar.
  - 45–55 s: «En el Máster esto es el bloque BIM + IA, y llegas después de dominar modelado, coordinación y gestión».
- **CTA:** «Comenta **NIVEL** y el test te dice en qué bloque del Máster estás hoy». Alternativa: si en noviembre hay un taller en vivo de Revit + IA confirmado, «Comenta **WORKSHOP** y te mando el acceso: lo conectamos juntos en vivo», como hizo Lex con su live de ASTRA.
- **Por qué:** es el mismo tema y el mismo gancho que sacaron 98,6 mil vistas, con la diferencia que nadie en el nicho ofrece: la honestidad técnica.

**Idea B · Especialización en Acero: «Revisar la nave a ojo»**
- **Gancho exacto:** «¿Todavía revisas tu nave de acero a ojo? Quédate: tres verificaciones en 50 segundos.»
- **Estructura:**
  - 0–3 s: el celular sobre Robot o Revit con el pórtico de una nave.
  - 3–40 s: verificación 1, 2 y 3 en pantalla (de la `GUIA-5-VERIFICACIONES-ACERO.md`), con el dedo señalando la barra que falla y un «PASO 1/2/3» grande.
  - 40–48 s: prueba, el resultado en rojo/verde.
  - 48–55 s: «Las otras dos te las mando».
- **CTA:** «Comenta **ACERO** y te mando la guía con las 5 verificaciones». Después pasa al seguimiento de GHL de la Especialización.
- **Por qué:** copia la mecánica de «el video da 3 pasos y el resto llega por DM». Además, Lex probó el tema acero + IA el 21-oct («ChatGPT modeló los aceros de columnas en Revit», 15.410 vistas, casi 3 veces su mediana). El comprador de Acero quiere hacerlo **en software** (632 de 859 respuestas del formulario).

**Idea C · Máster, bloque BIM Coordination: «Interferencias una por una»**
- **Gancho exacto:** «¿Todavía revisas las interferencias una por una? Así lo hago en 3 pasos.»
- **Estructura:**
  - 0–3 s: Navisworks con 1.000+ choques en pantalla.
  - 3–35 s: paso 1, agrupar por especialidad; paso 2, reglas; paso 3, priorizar (si se usa IA, decir exactamente qué hace y qué no).
  - 35–45 s: la viga picada en obra como imagen del costo, que es el gancho que llevó al mejor carrusel reciente de AECODE.
  - 45–55 s: «Coordinar es el segundo bloque del Máster».
- **CTA:** «Comenta **NIVEL** y el test te dice si ya estás para coordinar».
- **Por qué:** junta la mecánica del reel de Lex con el tema que más conversación dio en AECODE (DeQGKN7ES6W: 1.294 likes y 195 comentarios).

---

## 2 · @lexmrbim (Alexis Vera | BIM Consultor)

**Perfil:** 8.431 seguidores en IG y 223 publicaciones. Bio: «Ayudo a profesionales y constructoras a automatizar el seguimiento de su obra con BIM+Power BI+IA». En TikTok tenía unos 30.000 seguidores el 8-oct.

**Muestra:** sus últimas 50 publicaciones, del 17-ago al 21-oct de 2026: 24 reels y 26 carruseles.

### 2.1 Top 8 por engagement (likes + comentarios)

| # | Fecha | Formato | Vistas | Likes | Coment. | Gancho (1.ª línea) | Tema | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 05-oct | Reel 60 s | **98.570** | 3.471 | **3.162** | «Todavía no usas IA en Revit…» | Conectar IA a Revit (pyRevit + MCP) | QUIERO (prompt + video) |
| 2 | 26-ago | Carrusel | s/d | 2.928 | **808** | «Si tu problema es que haces lo mismo una y otra vez en el modelo, Dynamo te lo resuelve…» | Mapa de herramientas: Dynamo / pyRevit + Claude / NONICA / Bimetryc (Power BI) | COMUNIDAD |
| 3 | 31-ago | Carrusel | s/d | 2.529 | 27 | «Nadie empieza sabiendo…» | Motivacional / identidad | Pregunta en comentarios |
| 4 | 02-sep | Carrusel | s/d | 1.744 | 13 | «Lo que nadie te enseña cuando empiezas a trabajar como modelador BIM freelancer» | Freelance BIM: BEP, plantillas, hitos | Follow |
| 5 | 20-ago | Carrusel | s/d | 1.711 | 24 | «¿Sabías que puedes crear tus propios botones en Revit sin ser programador experto?» | pyRevit + Claude, en 4 pasos | Guardar / YouTube |
| 6 | 24-ago | Carrusel | s/d | 1.251 | **402** | «Pasaba horas cruzando datos del cronograma con el modelo BIM a mano…» | Historia: dashboard Power BI modelo + cronograma (4D) | Comunidad (enlace en el perfil) |
| 7 | 05-oct | Reel 77 s | 22.727 | 790 | **419** | «Conecta ChatGPT con Revit usando MCP» | Tutorial detallado de lo mismo que el #1 | QUIERO (guía) |
| 8 | 28-ago | Carrusel | s/d | 1.058 | 13 | «Esto fue lo que realmente me ayudó a conseguir mis primeros proyectos BIM como freelancer» | Freelance / carrera | Follow |

Fuera del top 8, pero útiles:
- «De CAD a BIM» (04-oct, reel de 44,8 s, 27.173 vistas, 968 likes, 27 comentarios). Es un proceso real narrado: estándares y nomenclaturas con Codex, y cierra con su cara.
- El plan BIM de ANIN Perú (04-sep, reel, 18.036 vistas). Noticia normativa, con 33 cortes en 57 s.
- «ChatGPT modeló los aceros de columnas en Revit usando MCP» (21-oct, 15.410 vistas).
- «pyRevit te permite crear tus propios botones…» (13-sep, 6.054 vistas y **409 comentarios**, 67,6 por cada 1.000, con la palabra GUIA).

### 2.2 Mediana contra top

| | n | Vistas med. | Likes med. | Coment. med. | Top |
|---|---|---|---|---|---|
| Reels | 24 | 5.224 | 165 | 3,5 | 98.570 vistas (18,9 veces la mediana) |
| Carruseles | 26 | s/d | 373 | 11 | 2.928 likes / 808 comentarios |
| Reels **con** «comenta PALABRA» | 6–7 | **11.183** | — | 159 | 14 comentarios por cada 1.000 vistas |
| Reels **sin** palabra | 17 | 4.076 | — | **0** | 0 comentarios por cada 1.000 |
| Carruseles con palabra / sin palabra | 10 / 16 | — | — | **128 / 6,5** | — |

Nota: el filtro de la palabra puede contar 1 falso positivo por «comentarios».

### 2.3 Cadencia

- 50 publicaciones en 65 días: **~5,4 por semana**, mitad reels y mitad carruseles. En los últimos 30 días, 21.
- Publica sobre todo **lunes, miércoles y viernes** (12, 14 y 13 de las 50), casi siempre a las **12:00–13:00 UTC** (7–8 am en Perú/Ecuador).
- Suele sacar 2 reels el mismo día con el mismo tema y dos versiones distintas (5-oct, 4-oct, 19-oct, 21-oct). Es un test A/B orgánico.

### 2.4 Patrones

1. **«Paso a paso» más un recurso por palabra** es lo que lo hace viral: QUIERO, GUIA, DYNAMO, COMUNIDAD. Sin palabra, sus reels se quedan en 0 comentarios.
2. **El tema de la IA como herramienta concreta** (pyRevit, MCP, Claude o ChatGPT dentro de Revit), nunca la IA en abstracto.
3. **Los carruseles de identidad y carrera** («Nadie empieza sabiendo», freelance) dan likes en masa pero no conversación (13–27 comentarios). Construyen marca, no leads.
4. **Historia en primera persona con dolor real** («Pasaba horas cruzando datos del cronograma…», «El primer dashboard que armé fue un desastre»), que trae 200–400 comentarios con palabra o comunidad.
5. **Lo-fi:** celular sobre el monitor, el dedo señalando, subtítulos de 1–2 palabras y algún meme.

---

## 3 · @aecode.ai (AECODE | Ingeniería 4.0 y Construcción Moderna)

**Perfil:** 22.791 seguidores y 701 publicaciones. Bio: «+10K alumnos | 14 países | 85K comunidad».

**Muestra:** sus últimas 50 publicaciones, del 20-ago al 23-oct de 2026: 20 reels, 16 carruseles y 14 imágenes.

### 3.1 Top 8 por engagement

| # | Fecha | Formato | Vistas | Likes | Coment. | Gancho (1.ª línea) | Tema | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 20-ago | Carrusel | s/d | **1.826** | 21 | «5 películas que todo ingeniero civil debería ver» | Entretenimiento / cultura de ingeniería | Pregunta («¿cuál ya viste?») |
| 2 | 08-oct | Carrusel | s/d | **1.294** | **195** | «Si alguna vez tuviste que picar una viga porque el ducto no pasaba, esto es para ti» | Coordinación: Navisworks, Forma, Revizto, Trimble Connect, Dalux | COORDINA(DOR), para su programa |
| 3 | 19-oct | Carrusel | s/d | 195 | **265** | «Si tu día se va en metrar, copiar plantillas y armar informes, esa parte ya la hace una IA» | IA aplicada a la obra | IA (Diplomado) |
| 4 | 15-sep | Carrusel | s/d | 306 | 70 | «Comenta LINKS y te lo mando por DM» | PDF con 28 recursos BIM por rol | LINKS (recurso gratis) |
| 5 | 24-sep | Carrusel | s/d | 187 | 90 | «La IA no sirve para modelar por ti. Sirve para todo lo que haces alrededor de modelar» | 6 escenarios de IA en BIM | «Comenta 1, 2 o 3» (ruta) |
| 6 | 04-sep | Imagen | s/d | 108 | 31 | «90 nodos de Dynamo que todo profesional BIM debería tener mapeados» | Glosario de Dynamo en PDF | INFO |
| 7 | 23-sep | Reel 41 s | **5.466** | 98 | 1 | «Ranking BIM 2026: ¿AutoCAD en último lugar?» | Tier list de software: presentadora y logos que caen en la tabla | Debate en comentarios |
| 8 | 22-ago | Reel 32 s | 4.982 | 81 | 16 | Testimonio: «Mi jefa se enteró del proyecto…» | Alumno (Pablo) de la beca AI Talent | BECA |

### 3.2 Mediana contra top

| | n | Vistas med. | Likes med. | Coment. med. |
|---|---|---|---|---|
| Reels | 20 | **1.588** (máx. 5.466) | 15 | 1 |
| Carruseles | 16 | s/d | 59 | 5 |
| Imágenes | 14 | s/d | 16,5 | 2,5 |
| Reels con palabra (17) / sin palabra (3) | | 1.502 / 2.328 | | 1,02 / 0,35 comentarios por cada 1.000 |

- Con 22,8 mil seguidores, sus reels sacan 0,07 vistas por seguidor: **el orgánico de AECODE en Instagram es débil**.
- Los dos primeros del top (1.826 y 1.294 likes) son 30–100 veces su mediana. Puede haber pauta detrás, pero **no se puede verificar**.
- Ponen palabra en casi todo, pero piden «info del programa» (REVIT, GESTOR, COORDINADOR, IA, PROGRAMAS), y eso saca ~1 comentario por cada 1.000 vistas. **Cuando la palabra da un recurso gratis** (LINKS, INFO del glosario, «1, 2 o 3»), los comentarios suben a 30–90.

### 3.3 Cadencia

- 50 publicaciones en 64 días: ~5,4 por semana, y **30 en los últimos 30 días (~7 por semana)**.
- Publica sobre todo miércoles y jueves, en la noche de Perú (23:00–01:00 UTC).
- Gran parte es promoción de eventos (Peru Tech Week, la beca AI Talent, webinars): 11 de las 50. Ese contenido rinde muy por debajo de la mediana.

### 3.4 Patrones

1. **Lo que funciona en AECODE son carruseles de comparación o mapa de herramientas con un dolor de obra como gancho** («picar una viga»), y recursos en PDF.
2. **El entretenimiento de nicho** (las 5 películas) da muchos likes y pocos comentarios.
3. **El tier list en reel** con presentadora a cámara y logos que caen es su reel más visto, pero casi no tiene comentarios porque no pide palabra.
4. **El testimonio de alumno con resultado laboral** («le liberaron medio tiempo») es su segundo mejor reel.
5. Lo que no funciona: las demos largas sin cortes (0 cortes en 47–56 s), la promoción de eventos y la palabra para pedir información del programa.

---

## 4 · Qué formatos debe copiar DMA

| Copiar | De quién | Por qué (dato) |
|---|---|---|
| **Reel «paso a paso» lo-fi + recurso por palabra** (celular sobre el monitor, 3 pasos, prueba visible, el último dato por DM) | lexmrbim | 98.570 vistas y 3.162 comentarios. Sus reels con palabra: mediana de 11.183 vistas contra 4.076 sin palabra |
| **Dos versiones del mismo tema el mismo día o semana** (una corta y emocional, otra técnica) | lexmrbim | La corta sacó 4,3 veces más vistas que la técnica. Es un test barato sin pauta |
| **Carrusel «mapa de herramientas»** (¿cuál te toca según tu problema?) | lexmrbim (808 comentarios) y AECODE (195 comentarios) | Encaja directo con los bloques del Máster: modelado → coordinación → gestión → BIM + IA |
| **Historia en primera persona con dolor de obra o gestión** | lexmrbim (402 y 130 comentarios) | Le habla al comprador del Máster («hago todo dos veces», «el reporte me toma un día») |
| **Carrusel de comparación de herramientas con un dolor de obra como gancho** | AECODE | Su mejor post reciente: 1.294 likes y 195 comentarios |
| **Tier list en reel** (solo si se le añade palabra) | AECODE | Su reel más visto (5.466), con 1 comentario porque no pedía nada |
| **No copiar:** palabra para «info del programa», promoción de eventos o demos largas sin cortes | AECODE | ~1 comentario por cada 1.000 vistas |

Comparación útil: la mediana de los reels de DMA (5.306 vistas, `OCTUBRE-QUE-FUNCIONA.md`) es **igual** a la de lexmrbim (5.224). El problema de alcance no es el que separa a DMA de Lex. Lo que los separa es que **él convierte cada tutorial en un recurso por palabra y DMA casi no lo hace en reels**.

---

## 5 · Qué llevar a la matriz de noviembre

Ordenadas por viralidad esperada. Es una estimación sobre los patrones de las referencias, no una predicción. Ninguna menciona precios. Cada afirmación técnica sobre software se comprueba en la documentación oficial antes de grabar (regla 0).

**Antes de publicar, revisar las palabras clave** en `fuentes/openreply/campanas.json`:
- **ZAPATA, ACERO, NIVEL y COTIZA** están montadas en GHL.
- **MEMORIA** sale *viva en OpenReply* (30 DM). La regla del 30-sep dice que va en GHL: hay que confirmar que no esté en las dos herramientas.
- **WORKSHOP** no aparece en el cotejo, y el workshop del 22-oct no se dictó. Solo se usa si hay un taller confirmado en noviembre.

| # | Pieza | Formato | Gancho exacto | Estructura | CTA | Referencia |
|---|---|---|---|---|---|---|
| 1 | **«Conectar la IA a Revit, sin humo»** (Máster · BIM + IA) | Reel 50–60 s, celular sobre el monitor, Gabriel 1 s al inicio | «¿Todavía no conectas la IA a Revit? Te lo dejo en 3 pasos… y te digo lo que nadie dice.» | 0–3 gancho · 3–35 tres pasos en pantalla · 35–45 la frase de criterio (oficial = solo lectura; lo que modifica es de terceros, con versión) · 45–55 el bloque BIM + IA · CTA | **WORKSHOP** si hay taller confirmado; si no, **NIVEL** | DeGtyhfoXar (98.570 vistas, 3.162 comentarios) |
| 2 | **«¿Cuál te toca: Dynamo, pyRevit, IA o Power BI?»** (Máster, los 4 bloques) | Carrusel de 7–8 diapositivas | «Si haces lo mismo 20 veces al día en Revit, no te falta IA: te falta saber cuál herramienta te toca.» | Una diapositiva por problema → herramienta → bloque del Máster (Professional / Coordination / Management / BIM + IA). Cierre: «no tienes que aprender todo a la vez» | **NIVEL** («el test te dice por qué bloque empezar») | lexmrbim DchNKVjGOkj (2.928 likes, 808 comentarios) |
| 3 | **«Tres verificaciones de tu nave en 50 s»** (Especialización en Acero) | Reel 45–55 s lo-fi, «PASO 1/2/3» grandes | «¿Todavía revisas tu nave de acero a ojo? Quédate: tres verificaciones en 50 segundos.» | Gancho sobre el pórtico en Robot/Revit · 3 verificaciones con el dedo · la barra que falla en rojo · «las otras dos te las mando» | **ACERO** (guía de 5 verificaciones) | Mecánica de DeGtyhfoXar + tema de lexmrbim DevHuOLsTwv (acero + IA, 15.410 vistas) |
| 4 | **«La viga que hubo que picar»** (Máster · BIM Coordination) | Carrusel comparativo | «Si alguna vez tuviste que picar una viga porque el ducto no pasaba, el choque ya estaba en el modelo.» | Foto de obra o esquema → 4 herramientas y cuándo usar cada una → «antes de coordinar, revisa tu modelo» → bloque Coordination | **NIVEL** | AECODE DeQGKN7ES6W (1.294 likes, 195 comentarios) |
| 5 | **Dos versiones el mismo día del reel 1 o 3** (test A/B orgánico) | 2 reels: uno de 35–45 s emocional y otro de 70 s técnico | Mismo gancho; la versión técnica abre con «Paso a paso completo:» | La corta promete y deja el dato por DM; la larga enseña todo. Se mide cuál saca más vistas y comentarios por cada 1.000 en 7 días | La misma palabra en las dos | DeGtyhfoXar contra DeHDZn4BrL- (4,3 veces más vistas para la corta) |
| 6 | **«Mi reporte de avance me tomaba un día entero»** (Máster · BIM Management) | Carrusel de historia en primera persona (Gabriel o un alumno real) | «Preparar el reporte de avance me tomaba un día entero. No por difícil: por copiar y pegar.» | Dolor → qué se automatizó (modelo + cronograma en un tablero) → resultado verificable → bloque Management | **NIVEL** | lexmrbim DcbpQ8VFhpf (402 comentarios) y Dee1GRdFNhC (130 comentarios) |
| 7 | **«Zapata paso a paso, sin Excel»** (escalera a Acero) | Reel 40–50 s lo-fi con la calculadora en pantalla | «¿Sigues haciendo la zapata en una hoja de Excel heredada? Tres datos y listo.» (no repetir el «a ojo» de septiembre, que está en el histórico) | 3 datos de entrada → resultado → la verificación que el Excel no hace → «te paso la calculadora» | **ZAPATA** | Mecánica de DeGtyhfoXar + el mejor reel propio de DMA («zapatas a ojo», 142 comentarios) |
| 8 | **«Ranking de software para estructuras 2026»** (Acero) | Reel tier list: Gabriel a cámara con logos que caen (Robot, ETABS, SAP2000, Tekla, Advance Steel, Revit) | «Ranking 2026 de software para calcular acero: ¿cuál pondrías último?» | Un logo cada 2–3 s con un veredicto de una frase · cierre con pregunta y palabra | **ACERO** (sin palabra este formato saca 1 comentario) | AECODE Ddpe4jKNJ1z (5.466 vistas, su reel más visto) |

Respaldo si sobra un hueco: un testimonio de alumno con resultado laboral, en el formato de AECODE DcUzptbsqPV (4.982 vistas, el «mi jefa se enteró…»), con un alumno real de Acero o del Máster y **ACERO** o **NIVEL** según el programa. En octubre la matriz ya tenía el testimonio de un alumno de Acero (23-oct): mirar cómo rinde antes de repetir.
