# Matriz de Contenido Viral — Design Modeling Academy

**Actualizada:** 2026-07-16 (**barrido completo** de `@design_modeling_dg` vía Apify)
**Cuentas analizadas:** 2 en Instagram (`@bimpure`, `@design_modeling_dg`)
**Reels totales:** 143 (DMA: **124** · BIM Pure: 19)
**Fuente cruda:** `fuentes/ig_bimpure.json` + `fuentes/ig_design_modeling_dg_barrido-completo_2026-07-16.json` (124 reels) + archivos previos del 2026-07-08 y del reel DM18.
**Referente descartado:** Dana de Filippi (handle no confirmado).

> ⚠️ **Corrección importante (2026-07-16).** El snapshot original (2026-07-08) analizaba **17 reels de DMA**. El barrido completo encontró que la cuenta tiene **124 reels** — el análisis anterior se basaba en el **~14%** de la cuenta y **omitía TODOS los reels virales reales** (4 reels sobre 1M de views, 13 sobre 100k). Las conclusiones de la versión anterior de `patrones-de-viralidad.md` ("DMA topa en ~20k views") eran un artefacto del muestreo. Este documento y `patrones-de-viralidad.md` están reconstruidos sobre los 124 reels reales.

---

## Convenciones y advertencias sobre los datos

- **ID:** `DM#` = @design_modeling_dg · `BP#` = @bimpure. **DM1–DM18** conservan su ID original (los referencian los guiones); **DM19–DM124** se asignaron en orden cronológico en el barrido del 2026-07-16. El ID **ya no equivale al ranking de views** — la tabla se ordena por views desc para lectura, pero el número de ID es solo una etiqueta estable.
- **Views:** `videoPlayCount` del scraper (reproducciones). Cifras vivas al 2026-07-16.
- **Sh (shares):** todos `s/d`. `includeSharesCount` **no está disponible en el plan free de Apify** (lo confirmó el log: `not supported for free users`) — ya no es decisión de costo.
- **Hook:** para DM1–DM18 es la transcripción de audio (recolección con transcript). Para **DM19–DM124 el hook viene del caption** (marcado `⟨caption⟩`), no del audio: el plan free aborta las corridas con transcripción por límite de datos, así que la transcripción masiva quedó pendiente. En reels educativos el caption suele coincidir con el hook hablado; en los de humor CC el hook real es el texto en pantalla.
- **Estructura:** categorización del formato/gancho. Nueva etiqueta **`REVELACIÓN-TÉCNICA`**: "mira esta técnica/material/dato de obra que no conocías" con visual satisfactorio (`¿sabías que…?`, "ya no es como antes"). Es la categoría que más escala en esta cuenta. Filas marcadas `⟨auto⟩` en la Nota se clasificaron por heurística sobre el caption y son de primera pasada (refinables).
- **Nota:** observación de por qué performa. `⟨auto⟩` = sin nota curada todavía.

**Flags manuales heredados:** BP4 (transcript sospechosa "Hello, how may I help you?"); DM4/DM6/DM9 (humor CC de TikTok, audio importado — hook real = texto en pantalla, no scrapeado).

---

## Tabla completa — 143 reels ordenados por views desc

| ID | Cuenta | Fecha | Dur | Views | Likes | Comm | Sh | Tema | Estructura | Hook | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DM42 | @design_modeling_dg | 2026-02-08 | 10s | 4,720,794 | 44064 | 470 | s/d | Encofrado modular: ya no son tablas y clavos | REVELACIÓN-TÉCNICA | "Hoy en día, encofrar techos ya no significa tablas, clavos y horas de trabajo pesado" | ⭐ TOP ABSOLUTO 4.7M. Reveal técnico "ya no es como antes" + visual satisfactorio de sistema portable. 470 comm = 0.01% (alcance masivo, conversación casi nula) |
| DM32 | @design_modeling_dg | 2026-01-25 | 72s | 1,701,819 | 38534 | 521 | s/d | Columnas de acero enterradas como cimentación | REVELACIÓN-TÉCNICA | "En muchos proyectos se entierran columnas de acero directamente en el suelo" | 2º absoluto 1.7M en 72s — un reveal técnico largo SÍ escala. 521 comm (0.03%) |
| DM45 | @design_modeling_dg | 2026-02-12 | 34s | 1,116,938 | 22148 | 222 | s/d | Aislamiento sísmico: edificios que se mueven con el sismo | PREGUNTA-REVELACIÓN | "¿Sabías que algunos edificios no “luchan” contra los sismos… sino que se mueven con ellos?" | 1.1M. Pregunta-mito universal ("¿sabías que…?") sobre un fenómeno contraintuitivo |
| DM49 | @design_modeling_dg | 2026-02-17 | 19s | 1,113,670 | 10293 | 57 | s/d | Camino temporal de tierra para intervenir un río | REVELACIÓN-TÉCNICA | "Para dar mantenimiento a un río, a veces los ingenieros rodean una parte del cauce" | 1.1M en 19s. Dato curioso de obra civil + visual. Solo 57 comm |
| DM21 | @design_modeling_dg | 2026-01-04 | 60s | 752,713 | 15130 | 314 | s/d | Pasajuntas: los "palitos milagrosos" de las losas | REVELACIÓN-TÉCNICA | "Las losas de concreto viven estresadas: se mueven, se dilatan, se encogen…" | 752k. Reveal técnico con tono cercano ("palitos milagrosos") — humaniza el dato |
| DM29 | @design_modeling_dg | 2026-01-20 | 64s | 708,870 | 14203 | 759 | s/d | Anclaje de tierra con tornillo vs cimentación | REVELACIÓN-TÉCNICA | "En algunos proyectos, un anclaje de tierra con tornillo metálico puede reemplazar una cimentación" | 708k y ⭐ 759 comentarios — el conteo de comm más alto de toda la cuenta (aun así 0.11%) |
| DM60 | @design_modeling_dg | 2026-03-05 | 15s | 676,227 | 65243 | 152 | s/d | Humor: ingenieros a las 11:47pm "reforzando conceptos" | DIÁLOGO-HUMOR | "Ingenieros en capacitación… también los ingenieros a las 11:47pm viendo Bob the Builder" | 676k, ratio likes 9.6% (65k likes) — el más querido. Humor relatable del gremio, CC |
| DM26 | @design_modeling_dg | 2026-01-15 | 33s | 504,603 | 5825 | 6 | s/d | Transporte quirúrgico de una losa de mármol | REVELACIÓN-TÉCNICA | "Transportar una losa de mármol es casi una operación quirúrgica" | 504k pero solo 6 comentarios (0.001%) — reach altísimo, conversación nula |
| DM28 | @design_modeling_dg | 2026-01-18 | 11s | 396,977 | 12303 | 128 | s/d | Humor: primer día como residente de obra | DIÁLOGO-HUMOR | "Primer día como residente de obra: llegas con casco nuevo y libreta lista…" | 397k. Relatable-humor de rol (residente novato). 128 comm |
| DM50 | @design_modeling_dg | 2026-02-19 | 6s | 195,022 | 6579 | 52 | s/d | Humor: la jefa metida en el chisme de obra | DIÁLOGO-HUMOR | "Cuando el chisme está demasiado bueno… y recuerdas que tú eres la jefa" | 195k en 6s. CC humor + giro de liderazgo. Ultra corto |
| DM92 | @design_modeling_dg | 2026-04-19 | 27s | 136,250 | 936 | 19 | s/d | Aquí es donde todo comienza 👷♂️📐 | DIÁLOGO-HUMOR | "Aquí es donde todo comienza 👷♂️📐" ⟨caption⟩ | ⟨auto⟩ |
| DM35 | @design_modeling_dg | 2026-01-29 | 22s | 126,659 | 2670 | 47 | s/d | En sistemas drywall, la distancia entre parr… | REVELACIÓN-TÉCNICA | "En sistemas drywall, la distancia entre parrales (montantes) no es al azar." ⟨caption⟩ | ⟨auto⟩ |
| DM119 | @design_modeling_dg | 2026-06-04 | 46s | 120,784 | 6658 | 52 | s/d | Triángulo isósceles + arcoseno para replanteo | TUTORIAL-TÉCNICO | "Forma un triángulo isósceles, divide la base en 2 y aplica arcoseno para obtener el ángulo" | 120k. Truco de obra + "¿Lo conocías?" (CC @elingef). Tip aplicable = guardable |
| DM20 | @design_modeling_dg | 2025-12-30 | 15s | 68,953 | 536 | 4 | s/d | Has visto cómo los expertos en construcción … | REVELACIÓN-TÉCNICA | "Has visto cómo los expertos en construcción hacen molduras exteriores con una precisión " ⟨caption⟩ | ⟨auto⟩ |
| DM117 | @design_modeling_dg | 2026-05-31 | 6s | 37,422 | 1927 | 0 | s/d | Humor: "un día normal en obra" (contratista) | DIÁLOGO-HUMOR | "Un día normal en obra: Contratista: “Ya qu[edó]…”" | 37k en 6s. Humor de gremio, CC |
| DM57 | @design_modeling_dg | 2026-03-01 | 10s | 25,953 | 308 | 12 | s/d | Cómo va la obra? | DIÁLOGO-HUMOR | "Cómo va la obra?" ⟨caption⟩ | ⟨auto⟩ |
| DM112 | @design_modeling_dg | 2026-05-24 | 20s | 22,969 | 289 | 2 | s/d | Geomembrana como barrera impermeable | REVELACIÓN-TÉCNICA | "La geomembrana actúa como una barrera impermeable" | 23k. Reveal de material |
| DM1 | @design_modeling_dg | 2026-06-25 | 19s | 20,263 | 445 | 4 | s/d | Humor voladizo arqui vs inge | DIÁLOGO-HUMOR | "¿Estás dentro o fuera? ¿De qué hablas, dentro o fuera de qué?" | Top view absoluto. CC de TikTok (@marcos_a_z_) reutilizando meme de película. Corto + tensión narrativa (cliffhanger) |
| DM23 | @design_modeling_dg | 2026-01-11 | 32s | 19,611 | 299 | 2 | s/d | Los caminos de piedra no se colocan al azar. | REVELACIÓN-TÉCNICA | "Los caminos de piedra no se colocan al azar." ⟨caption⟩ | ⟨auto⟩ |
| DM2 | @design_modeling_dg | 2026-06-18 | 19s | 19,563 | 190 | 11 | s/d | Material sorpresa: caucho de poliurea | REVELACIÓN-MITO | "Esto parece concreto, pero mira lo que pasa: se puede doblar como si fuera goma." | Patrón "parece X pero no es" + demostración visual + pregunta cierre "¿lo conocías?". CC de TikTok |
| DM34 | @design_modeling_dg | 2026-01-27 | 21s | 17,976 | 277 | 15 | s/d | Tips para parecer ocupado en la obra: | DIÁLOGO-HUMOR | "Tips para parecer ocupado en la obra:" ⟨caption⟩ | ⟨auto⟩ |
| DM113 | @design_modeling_dg | 2026-05-26 | 15s | 17,201 | 228 | 9 | s/d | Arquitecto con el practicante: 😎📐 “Eso cámbi… | DIÁLOGO-HUMOR | "Arquitecto con el practicante: 😎📐 “Eso cámbialo todo.”" ⟨caption⟩ | ⟨auto⟩ |
| DM3 | @design_modeling_dg | 2026-06-14 | 73s | 17,077 | 279 | 4 | s/d | Por qué el concreto necesita acero (tensión) | PREGUNTA-REVELACIÓN | "Si el concreto es tan fuerte, ¿por qué le ponen varillas de acero?" | Pregunta que todo estudiante se hace + explicación técnica clara. 73s largo pero funciona porque el hook es una duda universal |
| DM85 | @design_modeling_dg | 2026-04-09 | 32s | 16,633 | 334 | 0 | s/d | Un muro de contención no falla por el concre… | DIÁLOGO-HUMOR | "Un muro de contención no falla por el concreto… falla por lo que no ves 💧" ⟨caption⟩ | ⟨auto⟩ |
| DM107 | @design_modeling_dg | 2026-05-14 | 29s | 14,561 | 106 | 2 | s/d | Una zapata no empieza con concreto… empieza … | DIÁLOGO-HUMOR | "Una zapata no empieza con concreto… empieza con una buena excavación 🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM118 | @design_modeling_dg | 2026-06-02 | 7s | 13,892 | 518 | 0 | s/d | Dicen que para que te vaya bien en ingenierí… | DIÁLOGO-HUMOR | "Dicen que para que te vaya bien en ingeniería necesitas estudiar mucho..." ⟨caption⟩ | ⟨auto⟩ |
| DM52 | @design_modeling_dg | 2026-02-22 | 34s | 13,755 | 228 | 13 | s/d | Las máquinas de enlucido han cambiado por co… | DIÁLOGO-HUMOR | "Las máquinas de enlucido han cambiado por completo el acabado de muros 🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM22 | @design_modeling_dg | 2026-01-08 | 6s | 13,753 | 273 | 0 | s/d | Dicen que hacer planos todo el día sentado e… | DIÁLOGO-HUMOR | "Dicen que hacer planos todo el día sentado es estresante… 😩" ⟨caption⟩ | ⟨auto⟩ |
| DM94 | @design_modeling_dg | 2026-04-21 | 9s | 13,337 | 192 | 0 | s/d | Primer día como encargado de obra: modo líde… | DIÁLOGO-HUMOR | "Primer día como encargado de obra: modo líder activado 😎📐" ⟨caption⟩ | ⟨auto⟩ |
| DM25 | @design_modeling_dg | 2026-01-13 | 6s | 12,952 | 186 | 8 | s/d | Llegas a la obra pensando: “Hoy sí avanzamos… | DIÁLOGO-HUMOR | "Llegas a la obra pensando: “Hoy sí avanzamos full”" ⟨caption⟩ | ⟨auto⟩ |
| DM64 | @design_modeling_dg | 2026-03-10 | 14s | 12,462 | 195 | 4 | s/d | Ingeniero, ¿por qué no avanza la obra? 🤨 | DIÁLOGO-HUMOR | "Ingeniero, ¿por qué no avanza la obra? 🤨" ⟨caption⟩ | ⟨auto⟩ |
| DM100 | @design_modeling_dg | 2026-05-03 | 19s | 12,431 | 137 | 2 | s/d | Creen que estoy supervisando la obra… 👷♂️📋 | DIÁLOGO-HUMOR | "Creen que estoy supervisando la obra… 👷♂️📋" ⟨caption⟩ | ⟨auto⟩ |
| DM37 | @design_modeling_dg | 2026-02-01 | 12s | 12,053 | 185 | 3 | s/d | En la obra todos tienen una función… | DIÁLOGO-HUMOR | "En la obra todos tienen una función…" ⟨caption⟩ | ⟨auto⟩ |
| DM39 | @design_modeling_dg | 2026-02-03 | 78s | 11,995 | 309 | 4 | s/d | Te has preguntado por qué algunas vigas sobr… | DIÁLOGO-HUMOR | "Te has preguntado por qué algunas vigas sobresalen por debajo de la losa y el tumbado no" ⟨caption⟩ | ⟨auto⟩ |
| DM77 | @design_modeling_dg | 2026-03-29 | 10s | 11,007 | 205 | 4 | s/d | Los obreros: | DIÁLOGO-HUMOR | "Los obreros:" ⟨caption⟩ | ⟨auto⟩ |
| DM70 | @design_modeling_dg | 2026-03-19 | 10s | 10,591 | 208 | 3 | s/d | Cuando haces el presupuesto de obra gris bie… | DIÁLOGO-HUMOR | "Cuando haces el presupuesto de obra gris bien optimista 😌" ⟨caption⟩ | ⟨auto⟩ |
| DM40 | @design_modeling_dg | 2026-02-05 | 9s | 10,524 | 220 | 5 | s/d | Puedo calcular una losa, diseñar una viga y … | DIÁLOGO-HUMOR | "Puedo calcular una losa, diseñar una viga y levantar una casa completa 🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM87 | @design_modeling_dg | 2026-04-12 | 11s | 9,744 | 74 | 0 | s/d | Cuando ves el problema en obra y piensas: | DIÁLOGO-HUMOR | "Cuando ves el problema en obra y piensas:" ⟨caption⟩ | ⟨auto⟩ |
| DM105 | @design_modeling_dg | 2026-05-12 | 8s | 9,669 | 106 | 0 | s/d | Todo era risas en la obra… 😂🔧 | DIÁLOGO-HUMOR | "Todo era risas en la obra… 😂🔧" ⟨caption⟩ | ⟨auto⟩ |
| DM55 | @design_modeling_dg | 2026-02-26 | 11s | 9,606 | 263 | 4 | s/d | Vienes solo a supervisar, a “dar una vuelta … | DIÁLOGO-HUMOR | "Vienes solo a supervisar, a “dar una vuelta rápida” 👀🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM99 | @design_modeling_dg | 2026-04-30 | 10s | 9,427 | 130 | 4 | s/d | En plena obra: maquinaria, planos, decisione… | DIÁLOGO-HUMOR | "En plena obra: maquinaria, planos, decisiones importantes… 🚧📐" ⟨caption⟩ | ⟨auto⟩ |
| DM54 | @design_modeling_dg | 2026-02-24 | 15s | 9,168 | 109 | 2 | s/d | Tú: “Jefe, ¿le ayudo en algo?” 😃 | DIÁLOGO-HUMOR | "Tú: “Jefe, ¿le ayudo en algo?” 😃" ⟨caption⟩ | ⟨auto⟩ |
| DM4 | @design_modeling_dg | 2026-06-30 | 14s | 8,989 | 248 | 0 | s/d | Humor obra: 3 verdades del trabajo | LISTICLE-HUMOR | s/d (audio-CC, sin narración) | Sin audio hablado, se apoya en texto en pantalla + listicle de 3 puntos + humor Coca-Cola. Ratio likes/views 2.8% (el más alto de la matriz) |
| DM111 | @design_modeling_dg | 2026-05-21 | 13s | 8,895 | 148 | 4 | s/d | Me preguntan por qué escogí ser ingeniero… 👷… | DIÁLOGO-HUMOR | "Me preguntan por qué escogí ser ingeniero… 👷♂️📐" ⟨caption⟩ | ⟨auto⟩ |
| DM47 | @design_modeling_dg | 2026-02-15 | 20s | 8,236 | 87 | 0 | s/d | En la obra siempre hay un equipo… | DIÁLOGO-HUMOR | "En la obra siempre hay un equipo…" ⟨caption⟩ | ⟨auto⟩ |
| DM101 | @design_modeling_dg | 2026-05-05 | 64s | 8,164 | 208 | 1 | s/d | Muchos ven una vía y solo piensan en “asfalt… | DIÁLOGO-HUMOR | "Muchos ven una vía y solo piensan en “asfalto”… 🚧" ⟨caption⟩ | ⟨auto⟩ |
| DM44 | @design_modeling_dg | 2026-02-10 | 7s | 8,090 | 68 | 0 | s/d | Cuando firmas tu contrato pensando que vas a… | DIÁLOGO-HUMOR | "Cuando firmas tu contrato pensando que vas a calcular, supervisar y construir… 🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM59 | @design_modeling_dg | 2026-03-03 | 11s | 7,827 | 67 | 7 | s/d | Cliente: | DIÁLOGO-HUMOR | "Cliente:" ⟨caption⟩ | ⟨auto⟩ |
| DM98 | @design_modeling_dg | 2026-04-28 | 26s | 7,752 | 154 | 1 | s/d | Construir pilares altos no es solo levantar … | DIÁLOGO-HUMOR | "Construir pilares altos no es solo levantar concreto… es precisión, control y seguridad " ⟨caption⟩ | ⟨auto⟩ |
| DM5 | @design_modeling_dg | 2025-05-17 | 63s | 7,709 | 72 | 5 | s/d | Certificaciones internacionales Autodesk | PREGUNTA-DESDE-COMENTARIOS | "Uno de los comentarios que más me preguntan, ¿para qué sirven realmente las certificaciones internacionales de Autodesk?" | Promo camuflada de curso DMA usando pregunta real recurrente como hook |
| DM6 | @design_modeling_dg | 2026-06-11 | 10s | 7,638 | 103 | 3 | s/d | Humor: mientras albañiles trabajan, arquis conversan | DIÁLOGO-HUMOR | s/d (audio-CC: letra de canción de fondo) | Ultra corto (10s) + humor visual + relatable. CC de TikTok (@arqbooksc) |
| DM79 | @design_modeling_dg | 2026-03-31 | 13s | 7,101 | 133 | 6 | s/d | Cuando por fin compras el terreno 🥹✨ | DIÁLOGO-HUMOR | "Cuando por fin compras el terreno 🥹✨" ⟨caption⟩ | ⟨auto⟩ |
| DM7 | @design_modeling_dg | 2024-05-07 | 71s | 6,869 | 61 | 11 | s/d | Promo título universitario US (Sabal University) | PROMO-ANUNCIO | "Tenemos una excelente noticia para ti." | Formato promo directo. Buena performance atípica para promo pura — probable boost por tema "título internacional" |
| DM65 | @design_modeling_dg | 2026-03-12 | 36s | 6,749 | 93 | 3 | s/d | La inge: | DIÁLOGO-HUMOR | "La inge:" ⟨caption⟩ | ⟨auto⟩ |
| DM115 | @design_modeling_dg | 2026-05-28 | 64s | 6,575 | 77 | 0 | s/d | Levantar ladrillos no basta para que una est… | DIÁLOGO-HUMOR | "Levantar ladrillos no basta para que una estructura resista 🧱❌" ⟨caption⟩ | ⟨auto⟩ |
| DM41 | @design_modeling_dg | 2026-02-06 | 33s | 6,366 | 22 | 0 | s/d | 𝗘𝗿𝗿𝗼𝗿𝗲𝘀 𝗰𝗼𝗺𝘂𝗻𝗲𝘀 𝗮𝗹 𝘂𝘀𝗮𝗿 𝗜𝗔 𝗲𝗻 𝗽𝗿𝗼𝘆𝗲𝗰𝘁𝗼𝘀 𝗕𝗜𝗠 | REVELACIÓN-TÉCNICA | "𝗘𝗿𝗿𝗼𝗿𝗲𝘀 𝗰𝗼𝗺𝘂𝗻𝗲𝘀 𝗮𝗹 𝘂𝘀𝗮𝗿 𝗜𝗔 𝗲𝗻 𝗽𝗿𝗼𝘆𝗲𝗰𝘁𝗼𝘀 𝗕𝗜𝗠" ⟨caption⟩ | ⟨auto⟩ |
| DM110 | @design_modeling_dg | 2026-05-19 | 30s | 6,326 | 92 | 2 | s/d | Las losas no solo “cubren espacios” 🏗️ | DIÁLOGO-HUMOR | "Las losas no solo “cubren espacios” 🏗️" ⟨caption⟩ | ⟨auto⟩ |
| DM97 | @design_modeling_dg | 2026-04-26 | 17s | 6,121 | 58 | 1 | s/d | Cliente: “¿Por qué se está demorando tanto l… | DIÁLOGO-HUMOR | "Cliente: “¿Por qué se está demorando tanto la obra?” 🤨" ⟨caption⟩ | ⟨auto⟩ |
| DM89 | @design_modeling_dg | 2026-04-14 | 29s | 6,008 | 86 | 0 | s/d | Una losa reticular bien ejecutada no solo se… | DIÁLOGO-HUMOR | "Una losa reticular bien ejecutada no solo se ve impresionante… trabaja de forma intelige" ⟨caption⟩ | ⟨auto⟩ |
| DM104 | @design_modeling_dg | 2026-05-10 | 56s | 5,984 | 78 | 1 | s/d | Un buen vaciado no es solo “echar concreto” … | DIÁLOGO-HUMOR | "Un buen vaciado no es solo “echar concreto” 🚧🪣" ⟨caption⟩ | ⟨auto⟩ |
| DM62 | @design_modeling_dg | 2026-03-08 | 14s | 5,925 | 51 | 4 | s/d | Ingeniero: | DIÁLOGO-HUMOR | "Ingeniero:" ⟨caption⟩ | ⟨auto⟩ |
| DM82 | @design_modeling_dg | 2026-04-05 | 20s | 5,762 | 152 | 0 | s/d | Detrás de cada obra impresionante hay cálcul… | DIÁLOGO-HUMOR | "Detrás de cada obra impresionante hay cálculos, decisiones y mucho trabajo bien hecho 👷♂" ⟨caption⟩ | ⟨auto⟩ |
| DM8 | @design_modeling_dg | 2026-06-23 | 54s | 5,725 | 99 | 0 | s/d | Cómo se construye una losa deck | TUTORIAL-CONSTRUCCIÓN | "¿Has visto este tipo de losas? Aquí te cuento cómo se construyen." | Hook interrogativo directo + paso a paso técnico corto |
| DM56 | @design_modeling_dg | 2026-02-27 | 16s | 5,444 | 32 | 0 | s/d | Medir con flexómetro ya no es suficiente 📏❌ … | TUTORIAL-TÉCNICO | "Medir con flexómetro ya no es suficiente 📏❌ Con 𝗦𝗰𝗮𝗻 𝘁𝗼 𝗕𝗜𝗠 + 𝗜𝗔 obtienes modelos mucho " ⟨caption⟩ | ⟨auto⟩ |
| DM103 | @design_modeling_dg | 2026-05-07 | 18s | 5,369 | 63 | 0 | s/d | Arquitecto: “Quiero que el edificio parezca … | DIÁLOGO-HUMOR | "Arquitecto: “Quiero que el edificio parezca flotando” ✨🏛️" ⟨caption⟩ | ⟨auto⟩ |
| DM80 | @design_modeling_dg | 2026-04-02 | 9s | 5,349 | 40 | 0 | s/d | Primera parte de la obra: maquinaria activa,… | DIÁLOGO-HUMOR | "Primera parte de la obra: maquinaria activa, todo avanzando fino 🚧🔥" ⟨caption⟩ | ⟨auto⟩ |
| DM74 | @design_modeling_dg | 2026-03-24 | 10s | 5,328 | 55 | 0 | s/d | Nosotros: | DIÁLOGO-HUMOR | "Nosotros:" ⟨caption⟩ | ⟨auto⟩ |
| DM9 | @design_modeling_dg | 2026-06-21 | 14s | 5,323 | 65 | 0 | s/d | Humor: fingir inspección para no responder | DIÁLOGO-HUMOR | s/d (audio-CC: letra de canción de fondo) | Ultra corto + situación relatable de la industria. CC de TikTok (@arquingenio) |
| DM19 | @design_modeling_dg | 2025-12-29 | 16s | 5,283 | 41 | 4 | s/d | 𝗦𝗶 𝘁𝘂𝘀 𝗰𝗼𝗼𝗿𝗱𝗶𝗻𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝘁𝗲 𝘁𝗼𝗺𝗮𝗻 𝗵𝗼𝗿𝗮𝘀 😩⏳, est… | TUTORIAL-TÉCNICO | "𝗦𝗶 𝘁𝘂𝘀 𝗰𝗼𝗼𝗿𝗱𝗶𝗻𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝘁𝗲 𝘁𝗼𝗺𝗮𝗻 𝗵𝗼𝗿𝗮𝘀 😩⏳, este truco te va a encantar. Activa 𝗖𝗹𝗮𝘀𝗵 𝗛𝗶𝗴𝗵𝗹" ⟨caption⟩ | ⟨auto⟩ |
| DM38 | @design_modeling_dg | 2026-02-02 | 60s | 5,246 | 25 | 0 | s/d | 𝗖𝗼́𝗺𝗼 𝘀𝗮𝗯𝗲𝗿 𝘀𝗶 𝗲𝘀𝘁𝗮́𝘀 𝗺𝗼𝗱𝗲𝗹𝗮𝗻𝗱𝗼 𝗯𝗶𝗲𝗻 𝗲𝗻 𝗕𝗜𝗠?… | TUTORIAL-TÉCNICO | "𝗖𝗼́𝗺𝗼 𝘀𝗮𝗯𝗲𝗿 𝘀𝗶 𝗲𝘀𝘁𝗮́𝘀 𝗺𝗼𝗱𝗲𝗹𝗮𝗻𝗱𝗼 𝗯𝗶𝗲𝗻 𝗲𝗻 𝗕𝗜𝗠? La respuesta no está solo en dominar el sof" ⟨caption⟩ | ⟨auto⟩ |
| DM43 | @design_modeling_dg | 2026-02-09 | 42s | 5,144 | 11 | 6 | s/d | Nuestros 𝗰𝘂𝗿𝘀𝗼𝘀 𝘆 𝗲𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝗕𝗜𝗠 está… | PROMO-CURSO | "Nuestros 𝗰𝘂𝗿𝘀𝗼𝘀 𝘆 𝗲𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝗕𝗜𝗠 están diseñados para profesionales que buscan 𝗿𝗲" ⟨caption⟩ | ⟨auto⟩ |
| DM12 | @design_modeling_dg | 2026-07-02 | 37s | 4,993 | 83 | 3 | s/d | Pernos de anclaje acero-concreto | PREGUNTA-REVELACIÓN | "¿Sabes cómo se fija una estructura de acero al concreto?" | Pregunta que ing. civil se hizo alguna vez + explicación técnica corta |
| DM61 | @design_modeling_dg | 2026-03-06 | 28s | 4,866 | 45 | 0 | s/d | 𝗘𝘀𝘁𝗲 𝗲𝗿𝗿𝗼𝗿 𝗲𝗻 𝗰𝗶𝗺𝗲𝗻𝘁𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝘀𝗲 𝗿𝗲𝗽𝗶𝘁𝗲 𝗶𝗻𝗰𝗹𝘂𝘀… | TUTORIAL-TÉCNICO | "𝗘𝘀𝘁𝗲 𝗲𝗿𝗿𝗼𝗿 𝗲𝗻 𝗰𝗶𝗺𝗲𝗻𝘁𝗮𝗰𝗶𝗼𝗻𝗲𝘀 𝘀𝗲 𝗿𝗲𝗽𝗶𝘁𝗲 𝗶𝗻𝗰𝗹𝘂𝘀𝗼 𝗲𝗻 𝗽𝗿𝗼𝘆𝗲𝗰𝘁𝗼𝘀 𝗴𝗿𝗮𝗻𝗱𝗲𝘀… 𝘆 𝗰𝗮𝘀𝗶 𝗻𝗮𝗱𝗶𝗲 𝗹𝗼 𝗻𝗼𝘁𝗮" ⟨caption⟩ | ⟨auto⟩ |
| DM67 | @design_modeling_dg | 2026-03-15 | 11s | 4,860 | 34 | 0 | s/d | La arquitecta: | DIÁLOGO-HUMOR | "La arquitecta:" ⟨caption⟩ | ⟨auto⟩ |
| DM10 | @design_modeling_dg | 2026-06-16 | 6s | 4,816 | 35 | 0 | s/d | Humor: cliente ofrece "monedita" por dibujitos | DIÁLOGO-HUMOR | "Claro, el rico piensa que con una monedita puede comprar al pobre." | El más corto de toda la matriz (6s) + rabia comunitaria del gremio arqui. CC de TikTok |
| DM90 | @design_modeling_dg | 2026-04-16 | 9s | 4,703 | 23 | 4 | s/d | La obra a full: todos trabajando duro 🚧🔥 | DIÁLOGO-HUMOR | "La obra a full: todos trabajando duro 🚧🔥" ⟨caption⟩ | ⟨auto⟩ |
| DM33 | @design_modeling_dg | 2026-01-26 | 30s | 4,652 | 18 | 5 | s/d | 𝗧𝗲𝗻𝗱𝗲𝗻𝗰𝗶𝗮𝘀 𝟮𝟬𝟮𝟲 𝗲𝗻 𝗮𝗿𝗾𝘂𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗮 𝗰𝗼𝗻 𝗜𝗻𝘁𝗲𝗹𝗶𝗴𝗲… | TUTORIAL-TÉCNICO | "𝗧𝗲𝗻𝗱𝗲𝗻𝗰𝗶𝗮𝘀 𝟮𝟬𝟮𝟲 𝗲𝗻 𝗮𝗿𝗾𝘂𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗮 𝗰𝗼𝗻 𝗜𝗻𝘁𝗲𝗹𝗶𝗴𝗲𝗻𝗰𝗶𝗮 𝗔𝗿𝘁𝗶𝗳𝗶𝗰𝗶𝗮𝗹 La IA ya sugiere formas segú" ⟨caption⟩ | ⟨auto⟩ |
| DM46 | @design_modeling_dg | 2026-02-13 | 22s | 4,638 | 41 | 0 | s/d | 𝗟𝗮 𝗜𝗔 𝗽𝘂𝗲𝗱𝗲 𝗱𝗮𝗿𝘁𝗲 𝗼𝗽𝗰𝗶𝗼𝗻𝗲𝘀 🤖 Pero quien deci… [BIM+IA] | TUTORIAL-TÉCNICO | "𝗟𝗮 𝗜𝗔 𝗽𝘂𝗲𝗱𝗲 𝗱𝗮𝗿𝘁𝗲 𝗼𝗽𝗰𝗶𝗼𝗻𝗲𝘀 🤖 Pero quien decide sigue siendo el arquitecto 🧠📐" ⟨caption⟩ | ⟨auto⟩ |
| DM11 | @design_modeling_dg | 2026-06-28 | 83s | 4,523 | 101 | 3 | s/d | Errores en mampostería reforzada | ADVERTENCIA-ERROR | "Pasó lo que no debía pasar. A veces cometemos un grave error..." | Hook de tensión ("lo que no debía pasar"). Largo (83s) pero funciona en contenido técnico de obra |
| DM31 | @design_modeling_dg | 2026-01-24 | 60s | 4,520 | 23 | 0 | s/d | 𝗖𝘂𝗿𝘀𝗼, 𝗲𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝗰𝗶𝗼́𝗻 𝘆 𝗺𝗮́𝘀𝘁𝗲𝗿 𝗻𝗼 𝘀𝗼𝗻 𝗹𝗼 … | PROMO-CURSO | "𝗖𝘂𝗿𝘀𝗼, 𝗲𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝗰𝗶𝗼́𝗻 𝘆 𝗺𝗮́𝘀𝘁𝗲𝗿 𝗻𝗼 𝘀𝗼𝗻 𝗹𝗼 𝗺𝗶𝘀𝗺𝗼. Un curso (30–40 horas) te enseña a us" ⟨caption⟩ | ⟨auto⟩ |
| DM120 | @design_modeling_dg | 2026-06-07 | 32s | 4,440 | 50 | 1 | s/d | Todos trabajando tranquilos... | DIÁLOGO-HUMOR | "Todos trabajando tranquilos..." ⟨caption⟩ | ⟨auto⟩ |
| DM36 | @design_modeling_dg | 2026-01-30 | 33s | 4,438 | 16 | 5 | s/d | 𝗦𝗮𝗯í𝗮𝘀 𝗾𝘂𝗲 𝗹𝗮 𝗜𝗻𝘁𝗲𝗹𝗶𝗴𝗲𝗻𝗰𝗶𝗮 𝗔𝗿𝘁𝗶𝗳𝗶𝗰𝗶𝗮𝗹 𝗽𝘂𝗲𝗱𝗲 … [BIM+IA] | TUTORIAL-TÉCNICO | "𝗦𝗮𝗯í𝗮𝘀 𝗾𝘂𝗲 𝗹𝗮 𝗜𝗻𝘁𝗲𝗹𝗶𝗴𝗲𝗻𝗰𝗶𝗮 𝗔𝗿𝘁𝗶𝗳𝗶𝗰𝗶𝗮𝗹 𝗽𝘂𝗲𝗱𝗲 𝗺𝗲𝗷𝗼𝗿𝗮𝗿 𝘁𝘂 𝗺𝗼𝗱𝗲𝗹𝗼 𝗕𝗜𝗠?" ⟨caption⟩ | ⟨auto⟩ |
| DM30 | @design_modeling_dg | 2026-01-21 | 23s | 4,369 | 19 | 0 | s/d | 𝗗𝗶𝘀𝗲ñ𝗼 𝗿𝗮́𝗽𝗶𝗱𝗼, 𝗯𝗼𝗻𝗶𝘁𝗼 𝘆 𝗲𝗳𝗶𝗰𝗶𝗲𝗻𝘁𝗲? 𝗦í 𝗲𝘀 𝗽𝗼… [BIM+IA] | PREGUNTA-REVELACIÓN | "𝗗𝗶𝘀𝗲ñ𝗼 𝗿𝗮́𝗽𝗶𝗱𝗼, 𝗯𝗼𝗻𝗶𝘁𝗼 𝘆 𝗲𝗳𝗶𝗰𝗶𝗲𝗻𝘁𝗲? 𝗦í 𝗲𝘀 𝗽𝗼𝘀𝗶𝗯𝗹𝗲 𝗰𝗼𝗻 𝗜𝗔 + 𝗕𝗜𝗠🚀 La Inteligencia Artifici" ⟨caption⟩ | ⟨auto⟩ |
| DM48 | @design_modeling_dg | 2026-02-16 | 47s | 4,368 | 19 | 2 | s/d | Es normal tener la duda si un 𝗰𝘂𝗿𝘀𝗼 𝗕𝗜𝗠 𝗰𝗮𝗺𝗯… | TUTORIAL-TÉCNICO | "Es normal tener la duda si un 𝗰𝘂𝗿𝘀𝗼 𝗕𝗜𝗠 𝗰𝗮𝗺𝗯𝗶𝗮 𝘀𝗲𝗴𝘂́𝗻 𝗲𝗹 𝗽𝗮í𝘀 🌎 En Colombia, Perú y Ecua" ⟨caption⟩ | ⟨auto⟩ |
| DM27 | @design_modeling_dg | 2026-01-16 | 56s | 4,168 | 30 | 2 | s/d | 𝗡𝗼 𝗻𝗲𝗰𝗲𝘀𝗶𝘁𝗮𝘀 𝗲𝘅𝗽𝗲𝗿𝗶𝗲𝗻𝗰𝗶𝗮 𝗽𝗿𝗲𝘃𝗶𝗮 𝗽𝗮𝗿𝗮 𝗲𝗺𝗽𝗲𝘇𝗮𝗿… | TUTORIAL-TÉCNICO | "𝗡𝗼 𝗻𝗲𝗰𝗲𝘀𝗶𝘁𝗮𝘀 𝗲𝘅𝗽𝗲𝗿𝗶𝗲𝗻𝗰𝗶𝗮 𝗽𝗿𝗲𝘃𝗶𝗮 𝗽𝗮𝗿𝗮 𝗲𝗺𝗽𝗲𝘇𝗮𝗿 🚀 En nuestra academia, lo primero es que en" ⟨caption⟩ | ⟨auto⟩ |
| DM95 | @design_modeling_dg | 2026-04-23 | 68s | 4,139 | 81 | 0 | s/d | Los muros anclados no solo contienen tierra…… | DIÁLOGO-HUMOR | "Los muros anclados no solo contienen tierra… controlan fuerzas invisibles 👷♂️📐" ⟨caption⟩ | ⟨auto⟩ |
| DM108 | @design_modeling_dg | 2026-05-17 | 12s | 3,905 | 18 | 0 | s/d | Cómo va la obra?” 👷♂️ | DIÁLOGO-HUMOR | "Cómo va la obra?” 👷♂️" ⟨caption⟩ | ⟨auto⟩ |
| DM51 | @design_modeling_dg | 2026-02-20 | 33s | 3,786 | 12 | 0 | s/d | 𝗘𝘀𝘁𝗲 𝗛𝗔𝗖𝗞 𝗕𝗜𝗠 𝗽𝘂𝗲𝗱𝗲 𝗮𝗵𝗼𝗿𝗿𝗮𝗿𝘁𝗲 𝗦𝗘𝗠𝗔𝗡𝗔𝗦 de tra… | TUTORIAL-TÉCNICO | "𝗘𝘀𝘁𝗲 𝗛𝗔𝗖𝗞 𝗕𝗜𝗠 𝗽𝘂𝗲𝗱𝗲 𝗮𝗵𝗼𝗿𝗿𝗮𝗿𝘁𝗲 𝗦𝗘𝗠𝗔𝗡𝗔𝗦 de trabajo en tus proyectos estructurales. Si toda" ⟨caption⟩ | ⟨auto⟩ |
| DM84 | @design_modeling_dg | 2026-04-07 | 9s | 3,691 | 87 | 0 | s/d | Para que la obra quede perfecta: | DIÁLOGO-HUMOR | "Para que la obra quede perfecta:" ⟨caption⟩ | ⟨auto⟩ |
| BP1 | @bimpure | 2026-03-09 | 32s | 3,611 | 97 | 1 | s/d | Historia Slantis (arquitectura tech) | STORY-DOCUMENTAL | "Are we rolling? Hola, what does that mean? I traveled to Uruguay and Argentina to meet Slantis..." | Top view de BIM Pure. Humor bilingual + travel + "detrás de la empresa". Idioma inglés |
| DM53 | @design_modeling_dg | 2026-02-23 | 55s | 3,484 | 14 | 0 | s/d | 𝗣𝗼𝗿 𝗾𝘂𝗲́ 𝗲𝗹𝗲𝗴𝗶𝗿 𝗻𝘂𝗲𝘀𝘁𝗿𝗼𝘀 𝗰𝘂𝗿𝘀𝗼𝘀 𝗕𝗜𝗠? 🤔 Más a… | PROMO-CURSO | "𝗣𝗼𝗿 𝗾𝘂𝗲́ 𝗲𝗹𝗲𝗴𝗶𝗿 𝗻𝘂𝗲𝘀𝘁𝗿𝗼𝘀 𝗰𝘂𝗿𝘀𝗼𝘀 𝗕𝗜𝗠? 🤔 Más allá de certificaciones internacionales y ben" ⟨caption⟩ | ⟨auto⟩ |
| DM24 | @design_modeling_dg | 2026-01-12 | 68s | 3,482 | 13 | 1 | s/d | 𝗟𝗮 𝗺𝗲𝘁𝗼𝗱𝗼𝗹𝗼𝗴í𝗮 𝗕𝗜𝗠 𝘆𝗮 𝗻𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝘀𝗼𝗹𝗮. Hoy … [BIM+IA] | PROMO-CURSO | "𝗟𝗮 𝗺𝗲𝘁𝗼𝗱𝗼𝗹𝗼𝗴í𝗮 𝗕𝗜𝗠 𝘆𝗮 𝗻𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝘀𝗼𝗹𝗮. Hoy opera dentro de un ecosistema inteligente de" ⟨caption⟩ | ⟨auto⟩ |
| DM13 | @design_modeling_dg | 2026-01-06 | 120s | 3,370 | 22 | 4 | s/d | Curso IA aplicada a BIM (BIM Manager) | PROMO-CURSO | "La continuidad de cómo se va a conectar directamente con el módulo 1..." | Máxima duración de la matriz (120s). Promo directa con engagement bajo (likes/views 0.66%) |
| DM78 | @design_modeling_dg | 2026-03-30 | 54s | 3,301 | 18 | 0 | s/d | 𝗡𝗲𝗰𝗲𝘀𝗶𝘁𝗼 𝘁𝗲𝗻𝗲𝗿 𝗲𝗹 𝘁í𝘁𝘂𝗹𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝗴𝗿𝗲𝘀𝗮𝗿? 🎓 No… | PREGUNTA-REVELACIÓN | "𝗡𝗲𝗰𝗲𝘀𝗶𝘁𝗼 𝘁𝗲𝗻𝗲𝗿 𝗲𝗹 𝘁í𝘁𝘂𝗹𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝗴𝗿𝗲𝘀𝗮𝗿? 🎓 No ❌  Si estás estudiando 𝗜𝗻𝗴𝗲𝗻𝗶𝗲𝗿í𝗮 𝗖𝗶𝘃𝗶𝗹 𝗼 𝗔" ⟨caption⟩ | ⟨auto⟩ |
| DM63 | @design_modeling_dg | 2026-03-09 | 61s | 2,600 | 21 | 0 | s/d | 𝗤𝘂𝗶é𝗻 𝗽𝘂𝗲𝗱𝗲 𝗲𝘀𝘁𝘂𝗱𝗶𝗮𝗿 𝗕𝗜𝗠 𝗰𝗼𝗻 𝗻𝗼𝘀𝗼𝘁𝗿𝗼𝘀? Si ti… | TUTORIAL-TÉCNICO | "𝗤𝘂𝗶é𝗻 𝗽𝘂𝗲𝗱𝗲 𝗲𝘀𝘁𝘂𝗱𝗶𝗮𝗿 𝗕𝗜𝗠 𝗰𝗼𝗻 𝗻𝗼𝘀𝗼𝘁𝗿𝗼𝘀? Si tienes formación en Ingeniería Civil o Arquite" ⟨caption⟩ | ⟨auto⟩ |
| DM68 | @design_modeling_dg | 2026-03-17 | 53s | 2,442 | 7 | 0 | s/d | Ustedes ayudan con los 𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗮𝘀 𝘆 𝗹𝗶𝗰𝗲𝗻𝗰𝗶𝗮𝘀… | PREGUNTA-REVELACIÓN | "Ustedes ayudan con los 𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗮𝘀 𝘆 𝗹𝗶𝗰𝗲𝗻𝗰𝗶𝗮𝘀 de Autodesk? 💻 𝗦í ✅  Cuando te matriculas t" ⟨caption⟩ | ⟨auto⟩ |
| DM58 | @design_modeling_dg | 2026-03-02 | 51s | 2,438 | 9 | 0 | s/d | 𝗘𝗹 𝗺𝗲𝗿𝗰𝗮𝗱𝗼 𝘆𝗮 𝗻𝗼 𝗯𝘂𝘀𝗰𝗮 𝘀𝗼𝗹𝗼 𝗽𝗿𝗼𝗳𝗲𝘀𝗶𝗼𝗻𝗮𝗹𝗲𝘀… 𝗯… | TUTORIAL-TÉCNICO | "𝗘𝗹 𝗺𝗲𝗿𝗰𝗮𝗱𝗼 𝘆𝗮 𝗻𝗼 𝗯𝘂𝘀𝗰𝗮 𝘀𝗼𝗹𝗼 𝗽𝗿𝗼𝗳𝗲𝘀𝗶𝗼𝗻𝗮𝗹𝗲𝘀… 𝗯𝘂𝘀𝗰𝗮 𝗲𝘅𝗽𝗲𝗿𝘁𝗼𝘀 𝗲𝗻 𝗕𝗜𝗠. Hoy, las habilidades q" ⟨caption⟩ | ⟨auto⟩ |
| DM71 | @design_modeling_dg | 2026-03-20 | 24s | 2,349 | 17 | 0 | s/d | 𝗡𝗼 𝘀𝗲 𝘁𝗿𝗮𝘁𝗮 𝗱𝗲 𝗺𝗼𝗱𝗲𝗹𝗮𝗿 𝗺á𝘀 𝗿á𝗽𝗶𝗱𝗼… 𝘀𝗲 𝘁𝗿𝗮𝘁𝗮 … | TUTORIAL-TÉCNICO | "𝗡𝗼 𝘀𝗲 𝘁𝗿𝗮𝘁𝗮 𝗱𝗲 𝗺𝗼𝗱𝗲𝗹𝗮𝗿 𝗺á𝘀 𝗿á𝗽𝗶𝗱𝗼… 𝘀𝗲 𝘁𝗿𝗮𝘁𝗮 𝗱𝗲 𝗺𝗼𝗱𝗲𝗹𝗮𝗿 𝗰𝗼𝗻 𝗰𝗿𝗶𝘁𝗲𝗿𝗶𝗼. Muchos creen que tr" ⟨caption⟩ | ⟨auto⟩ |
| DM76 | @design_modeling_dg | 2026-03-28 | 51s | 2,230 | 11 | 0 | s/d | 𝗘𝗻 𝗕𝗜𝗠, 𝗹𝗼𝘀 𝗱𝗲𝘁𝗮𝗹𝗹𝗲𝘀 𝗵𝗮𝗰𝗲𝗻 𝗹𝗮 𝗱𝗶𝗳𝗲𝗿𝗲𝗻𝗰𝗶𝗮 🔥 ¿… | REVELACIÓN-TÉCNICA | "𝗘𝗻 𝗕𝗜𝗠, 𝗹𝗼𝘀 𝗱𝗲𝘁𝗮𝗹𝗹𝗲𝘀 𝗵𝗮𝗰𝗲𝗻 𝗹𝗮 𝗱𝗶𝗳𝗲𝗿𝗲𝗻𝗰𝗶𝗮 🔥 ¿Sabías que no todos los parámetros en Revit " ⟨caption⟩ | ⟨auto⟩ |
| DM75 | @design_modeling_dg | 2026-03-26 | 14s | 2,133 | 24 | 0 | s/d | Cómo saber si tu obra realmente está avanzan… | DIÁLOGO-HUMOR | "Cómo saber si tu obra realmente está avanzando? 👇" ⟨caption⟩ | ⟨auto⟩ |
| DM66 | @design_modeling_dg | 2026-03-13 | 30s | 2,087 | 5 | 0 | s/d | En BIM, un proyecto no se gestiona solo con … | TUTORIAL-TÉCNICO | "En BIM, un proyecto no se gestiona solo con modelos… se gestiona con 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰𝗶ó𝗻 𝗲𝘀𝘁𝗿𝘂𝗰𝘁" ⟨caption⟩ | ⟨auto⟩ |
| DM116 | @design_modeling_dg | 2026-05-29 | 67s | 2,020 | 13 | 0 | s/d | 𝗧𝗼𝗱𝗮𝘃í𝗮 𝘁𝗲 𝗰𝗼𝗻𝗳𝘂𝗻𝗱𝗲𝗻 𝗹𝗼𝘀 𝗽𝗮𝗿á𝗺𝗲𝘁𝗿𝗼𝘀 𝗱𝗲 𝗽𝗿𝗼𝘆𝗲… | PREGUNTA-REVELACIÓN | "𝗧𝗼𝗱𝗮𝘃í𝗮 𝘁𝗲 𝗰𝗼𝗻𝗳𝘂𝗻𝗱𝗲𝗻 𝗹𝗼𝘀 𝗽𝗮𝗿á𝗺𝗲𝘁𝗿𝗼𝘀 𝗱𝗲 𝗽𝗿𝗼𝘆𝗲𝗰𝘁𝗼, 𝘁𝗶𝗽𝗼 𝘆 𝗲𝗷𝗲𝗺𝗽𝗹𝗮𝗿 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? 🤔 En esta cla" ⟨caption⟩ | ⟨auto⟩ |
| DM106 | @design_modeling_dg | 2026-05-12 | 248s | 1,996 | 10 | 0 | s/d | Así se ve un proyecto de racks de almacenami… | PROMO-CURSO | "Así se ve un proyecto de racks de almacenamiento cuando el modelado BIM está bien hecho." ⟨caption⟩ | ⟨auto⟩ |
| DM73 | @design_modeling_dg | 2026-03-23 | 31s | 1,979 | 11 | 0 | s/d | 𝗟𝗮 𝗜𝗔 𝗲𝗻 𝗕𝗜𝗠 𝗻𝗼 𝘃𝗶𝗲𝗻𝗲 𝗮 𝗿𝗲𝗲𝗺𝗽𝗹𝗮𝘇𝗮𝗿𝘁𝗲… 𝘃𝗶𝗲𝗻𝗲 … | TUTORIAL-TÉCNICO | "𝗟𝗮 𝗜𝗔 𝗲𝗻 𝗕𝗜𝗠 𝗻𝗼 𝘃𝗶𝗲𝗻𝗲 𝗮 𝗿𝗲𝗲𝗺𝗽𝗹𝗮𝘇𝗮𝗿𝘁𝗲… 𝘃𝗶𝗲𝗻𝗲 𝗮 𝗽𝗼𝘁𝗲𝗻𝗰𝗶𝗮𝗿𝘁𝗲 🚀  Con una correcta aplicación" ⟨caption⟩ | ⟨auto⟩ |
| DM72 | @design_modeling_dg | 2026-03-22 | 88s | 1,920 | 10 | 2 | s/d | Si quieres controlar los costos de obra, enf… | DIÁLOGO-HUMOR | "Si quieres controlar los costos de obra, enfócate en esto 👇" ⟨caption⟩ | ⟨auto⟩ |
| DM121 | @design_modeling_dg | 2026-06-09 | 41s | 1,878 | 20 | 2 | s/d | La habilidad más importante de un ingeniero … | DIÁLOGO-HUMOR | "La habilidad más importante de un ingeniero no es calcular..." ⟨caption⟩ | ⟨auto⟩ |
| DM109 | @design_modeling_dg | 2026-05-18 | 30s | 1,798 | 6 | 0 | s/d | 𝗡𝗼. ❌ 𝗡𝗼 𝗻𝗲𝗰𝗲𝘀𝗶𝘁𝗮𝘀 𝗱𝗼𝗺𝗶𝗻𝗮𝗿 𝘁𝗼𝗱𝗮𝘀 𝗹𝗮𝘀 𝗲𝘀𝗽𝗲𝗰𝗶𝗮… | TUTORIAL-TÉCNICO | "𝗡𝗼. ❌ 𝗡𝗼 𝗻𝗲𝗰𝗲𝘀𝗶𝘁𝗮𝘀 𝗱𝗼𝗺𝗶𝗻𝗮𝗿 𝘁𝗼𝗱𝗮𝘀 𝗹𝗮𝘀 𝗲𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝗱𝗮𝗱𝗲𝘀. Lo que sí necesitas es un perfil vi" ⟨caption⟩ | ⟨auto⟩ |
| DM96 | @design_modeling_dg | 2026-04-24 | 38s | 1,797 | 14 | 0 | s/d | Si diseñas cimentaciones “a ojo”… estás juga… | REVELACIÓN-TÉCNICA | "Si diseñas cimentaciones “a ojo”… estás jugando con fuego ⚠️ Uno de los errores más comu" ⟨caption⟩ | ⟨auto⟩ |
| DM83 | @design_modeling_dg | 2026-04-06 | 31s | 1,793 | 7 | 0 | s/d | 𝗟𝗮 𝗜𝗔 𝗿𝗲𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗮𝘆𝘂𝗱𝗮 𝗲𝗻 𝗕𝗜𝗠? La respuesta e… [BIM+IA] | PROMO-CURSO | "𝗟𝗮 𝗜𝗔 𝗿𝗲𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗮𝘆𝘂𝗱𝗮 𝗲𝗻 𝗕𝗜𝗠? La respuesta es corta: 𝘀í, 𝗽𝗲𝗿𝗼 𝗻𝗼 𝗰𝗼𝗺𝗼 𝗺𝘂𝗰𝗵𝗼𝘀 𝗰𝗿𝗲𝗲𝗻. En n" ⟨caption⟩ | ⟨auto⟩ |
| DM91 | @design_modeling_dg | 2026-04-17 | 34s | 1,777 | 11 | 0 | s/d | 𝗤𝘂𝗶𝗲𝗿𝗲𝘀 𝘁𝗿𝗮𝗯𝗮𝗷𝗮𝗿 𝟮𝘅 𝗺á𝘀 𝗿á𝗽𝗶𝗱𝗼 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? Mir… | TUTORIAL-TÉCNICO | "𝗤𝘂𝗶𝗲𝗿𝗲𝘀 𝘁𝗿𝗮𝗯𝗮𝗷𝗮𝗿 𝟮𝘅 𝗺á𝘀 𝗿á𝗽𝗶𝗱𝗼 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? Mira esto💡 No todo es modelar manualmente… 𝗛𝗼𝘆 " ⟨caption⟩ | ⟨auto⟩ |
| DM102 | @design_modeling_dg | 2026-05-06 | 57s | 1,774 | 6 | 0 | s/d | 𝗖𝗼𝗻𝘃𝗶𝗲𝗿𝘁𝗲 𝘁𝘂 𝘁í𝘁𝘂𝗹𝗼 𝗲𝗻 𝘂𝗻𝗮 𝘃𝗲𝗻𝘁𝗮𝗷𝗮 𝗿𝗲𝗮𝗹 🚀 Co… | PROMO-CURSO | "𝗖𝗼𝗻𝘃𝗶𝗲𝗿𝘁𝗲 𝘁𝘂 𝘁í𝘁𝘂𝗹𝗼 𝗲𝗻 𝘂𝗻𝗮 𝘃𝗲𝗻𝘁𝗮𝗷𝗮 𝗿𝗲𝗮𝗹 🚀 Con el Máster BIM Internacional + IA no solo o" ⟨caption⟩ | ⟨auto⟩ |
| DM114 | @design_modeling_dg | 2026-05-27 | 20s | 1,766 | 4 | 1 | s/d | 𝗘𝗹 𝗠á𝘀𝘁𝗲𝗿 𝘁𝗶𝗲𝗻𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗼 𝗲𝗻 𝗦𝗘𝗡𝗘𝗦𝗖𝗬𝗧?” Sí ✅ … | TUTORIAL-TÉCNICO | "𝗘𝗹 𝗠á𝘀𝘁𝗲𝗿 𝘁𝗶𝗲𝗻𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗼 𝗲𝗻 𝗦𝗘𝗡𝗘𝗦𝗖𝗬𝗧?” Sí ✅ Gracias a nuestro convenio con la Universida" ⟨caption⟩ | ⟨auto⟩ |
| DM81 | @design_modeling_dg | 2026-04-03 | 49s | 1,750 | 15 | 0 | s/d | 𝗧𝘂 𝗺𝗼𝗱𝗲𝗹𝗼 𝗽𝘂𝗲𝗱𝗲 𝘃𝗲𝗿𝘀𝗲 𝗯𝗶𝗲𝗻… 𝘆 𝗲𝘀𝘁𝗮𝗿 𝗺𝗮𝗹 𝗵𝗲𝗰𝗵… | TUTORIAL-TÉCNICO | "𝗧𝘂 𝗺𝗼𝗱𝗲𝗹𝗼 𝗽𝘂𝗲𝗱𝗲 𝘃𝗲𝗿𝘀𝗲 𝗯𝗶𝗲𝗻… 𝘆 𝗲𝘀𝘁𝗮𝗿 𝗺𝗮𝗹 𝗵𝗲𝗰𝗵𝗼. Si usas familias incorrectas en Revit, tu" ⟨caption⟩ | ⟨auto⟩ |
| DM93 | @design_modeling_dg | 2026-04-20 | 57s | 1,711 | 5 | 1 | s/d | 𝗟𝗮 𝗜𝗔 𝗡𝗢 𝘁𝗲 𝘃𝗮 𝗮 𝗿𝗲𝗲𝗺𝗽𝗹𝗮𝘇𝗮𝗿, pero sí lo hará… | TUTORIAL-TÉCNICO | "𝗟𝗮 𝗜𝗔 𝗡𝗢 𝘁𝗲 𝘃𝗮 𝗮 𝗿𝗲𝗲𝗺𝗽𝗹𝗮𝘇𝗮𝗿, pero sí lo hará alguien que sepa usarla 𝗺𝗲𝗷𝗼𝗿 𝗾𝘂𝗲 𝘁ú." ⟨caption⟩ | ⟨auto⟩ |
| DM69 | @design_modeling_dg | 2026-03-17 | 41s | 1,618 | 12 | 0 | s/d | Cuál es la habilidad más importante de un in… | DIÁLOGO-HUMOR | "Cuál es la habilidad más importante de un ingeniero civil? 🤔" ⟨caption⟩ | ⟨auto⟩ |
| DM14 | @design_modeling_dg | 2026-06-17 | 74s | 1,585 | 17 | 8 | s/d | Análisis estructural: derivas y deformaciones | TUTORIAL-TÉCNICO | "va a indicarnos cuáles son las deformaciones, cuáles son las derivas..." | Muy nicho (ing. estructural). Hook comienza en medio de frase — mala edición del inicio |
| DM88 | @design_modeling_dg | 2026-04-13 | 67s | 1,531 | 9 | 1 | s/d | 𝗦𝗶𝗴𝘂𝗲𝘀 𝘂𝘀𝗮𝗻𝗱𝗼 𝗺𝗮𝗹 𝗹𝗼𝘀 𝗽𝗮𝗿á𝗺𝗲𝘁𝗿𝗼𝘀 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? L… | PROMO-CURSO | "𝗦𝗶𝗴𝘂𝗲𝘀 𝘂𝘀𝗮𝗻𝗱𝗼 𝗺𝗮𝗹 𝗹𝗼𝘀 𝗽𝗮𝗿á𝗺𝗲𝘁𝗿𝗼𝘀 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? La mayoría de ingenieros y arquitectos comete" ⟨caption⟩ | ⟨auto⟩ |
| DM18 | @design_modeling_dg | 2026-07-15 | 40s | 1,471 | 32 | 28 | s/d | ChatGPT diseña una losa → la IA falla en el criterio, no en la fórmula (BIM+IA original) | MITO/EXPECTATIVA-VS-REALIDAD | "Le pedí a ChatGPT que me diseñara una losa de entrepiso y esto fue lo que pasó." | ⭐ **27 comentarios — récord absoluto de la matriz** (top previo: DM2 con 11). Primer reel con CTA real "comenta BIM o IA" → validó el fix de §5 (cuenta genera views, no conversación). Views 1,453 pero medido a <24h de publicado. Likes/views 2.2% (top-3 de la cuenta). Sh `s/d`: `includeSharesCount` no está disponible en plan free de Apify. Datos al 2026-07-16 |
| DM123 | @design_modeling_dg | 2026-06-27 | 185s | 1,395 | 19 | 0 | s/d | Hoy Venezuela nos necesita. | TUTORIAL-TÉCNICO | "Hoy Venezuela nos necesita." ⟨caption⟩ | ⟨auto⟩ |
| DM122 | @design_modeling_dg | 2026-06-12 | 57s | 1,376 | 7 | 0 | s/d | 𝗬 𝘀𝗶 𝘁𝗲 𝗱𝗶𝗷𝗲𝗿𝗮 𝗾𝘂𝗲 𝗹𝗮 𝗜𝗔 𝗽𝘂𝗲𝗱𝗲 𝗮𝘆𝘂𝗱𝗮𝗿𝘁𝗲 𝗮 𝗮𝘂… [BIM+IA] | TUTORIAL-TÉCNICO | "𝗬 𝘀𝗶 𝘁𝗲 𝗱𝗶𝗷𝗲𝗿𝗮 𝗾𝘂𝗲 𝗹𝗮 𝗜𝗔 𝗽𝘂𝗲𝗱𝗲 𝗮𝘆𝘂𝗱𝗮𝗿𝘁𝗲 𝗮 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝘇𝗮𝗿 𝘁𝗮𝗿𝗲𝗮𝘀 𝗲𝗻 𝗥𝗲𝘃𝗶𝘁? Muchos ingenieros" ⟨caption⟩ | ⟨auto⟩ |
| DM16 | @design_modeling_dg | 2026-07-05 | 46s | 1,342 | 11 | 2 | s/d | Revit + Power BI + IA (dashboard) | TUTORIAL-INTEGRACIÓN | "¿Sabía que con Power BI y la inteligencia artificial podemos cambiar cómo identificamos nuestra data y la interpretamos?" | Combo triple (IA + BI + BIM). Muy alineado con línea editorial DMA pero engagement bajo |
| DM86 | @design_modeling_dg | 2026-04-10 | 33s | 1,319 | 11 | 0 | s/d | 𝗘𝗹 𝟵𝟬% 𝗱𝗲 𝗹𝗼𝘀 𝗕𝗜𝗠 𝗠𝗮𝗻𝗮𝗴𝗲𝗿𝘀 𝘀𝗶𝗴𝘂𝗲𝗻 𝘁𝗿𝗮𝗯𝗮𝗷𝗮𝗻𝗱𝗼… [BIM+IA] | TUTORIAL-TÉCNICO | "𝗘𝗹 𝟵𝟬% 𝗱𝗲 𝗹𝗼𝘀 𝗕𝗜𝗠 𝗠𝗮𝗻𝗮𝗴𝗲𝗿𝘀 𝘀𝗶𝗴𝘂𝗲𝗻 𝘁𝗿𝗮𝗯𝗮𝗷𝗮𝗻𝗱𝗼 𝗰𝗼𝗺𝗼 𝗲𝗻 𝟮𝟬𝟮𝟬… y por eso pierden horas cada " ⟨caption⟩ | ⟨auto⟩ |
| DM15 | @design_modeling_dg | 2026-07-01 | 53s | 1,308 | 4 | 0 | s/d | Serie "Noticias BIM que SÍ importan" — ep. 1 | NOTICIA-SERIE | "¿Hasta dónde puede llegar la IA en el mundo BIM? Te lo cuento." | Hook fuerte pero engagement mínimo (2 likes / 1067 views = 0.19%). Recién lanzada + rebrand de serie sin audiencia establecida |
| BP2 | @bimpure | 2025-05-05 | 42s | 1,221 | 24 | 0 | s/d | Recurso gratis: colección de íconos Revit | PROMO-RECURSO | "This is the brand new Revit's icon collection by Beam Pure, which includes different colors for different yearly release." | Regalo gratis + soporte multilenguaje. Palabra clave "free download" |
| BP3 | @bimpure | 2025-05-20 | 65s | 1,204 | 22 | 1 | s/d | Curso D5 render con líder de KPF | PROMO-CURSO | "Hi everybody, my name is Andy Crisoforo. I lead the visualization and AI efforts at KPF" | Autoridad de firma top (KPF) + promesa "amazing renders" |
| DM124 | @design_modeling_dg | 2026-07-03 | 64s | 1,193 | 4 | 1 | s/d | Sabías que una tabla de Revit puede decirte … [BIM+IA] | REVELACIÓN-TÉCNICA | "Sabías que una tabla de Revit puede decirte mucho más que cantidades? 👀" ⟨caption⟩ | ⟨auto⟩ |
| BP4 | @bimpure | 2024-09-19 | 16s | 1,177 | 43 | 1 | s/d | Lanzamiento revista BIM & BEYOND | NOTICIA-LANZAMIENTO | "Hello, how may I help you?" ⚠️ transcript sospechosa | Corto (16s), announcement. Transcript claramente incompleto — bandera manual |
| BP5 | @bimpure | 2025-05-29 | 102s | 1,166 | 32 | 0 | s/d | Vibe-coding con ChatGPT en Revit | TUTORIAL-IA | "Hello everybody and welcome to a new BIMpure video. In this one, we're going to do some vibe coding inside of Revit." | Tema trendy (vibe-coding) + IA + Revit. Formato tutorial largo (102s) — top-3 en duración de BP |
| DM17 | @design_modeling_dg | 2026-07-07 | 53s | 1,071 | 4 | 0 | s/d | FAQ curso SAP2000 Naves Industriales | PROMO-FAQ | "Las tres preguntas más frecuentes que me hacen sobre SAP 2000 las respondo rápido y sin rodeos." | Formato FAQ + promo curso. Recién publicada (7 jul) — muestra pequeña, aún no medible |
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

---

## Actualización 2026-07-16 — barrido completo (corrida Apify)

Corrida de `apify/instagram-reel-scraper` (plan free). Se pasó de 17 a **124 reels de DMA**. Qué cambió respecto al snapshot del 2026-07-08:

### Lo que el muestreo anterior escondía

| Métrica | Matriz 2026-07-08 (17 reels) | Realidad (124 reels) |
|---|---|---|
| Reel top | DM1 — 19,934 views | **DM42 — 4,720,794 views** (236×) |
| Reels > 100k views | 0 | **13** |
| Reels > 1M views | 0 | **4** |
| Mediana de views | ~5,000 | 5,743 (parecida — el sesgo estaba en la **cola alta**, no en la mediana) |

El muestreo original capturó bien el "piso" de la cuenta pero **perdió toda la cola viral**. Por eso el análisis viejo concluía que DMA es una cuenta de humor-CC con techo ~20k: nunca vio los reveals técnicos de millones.

### El reel DM18 (ChatGPT diseña una losa) en contexto real

- **1,453 views · 32 likes · 27 comentarios**, publicado 2026-07-15 (medido a <24h).
- En alcance es un reel **pequeño** de la cuenta (mediana 5.7k; hay 4 reels sobre 1M). Pero en **tasa de conversación es el #1 histórico por lejos**: 1.90% vs. mediana de la cuenta 0.013% y promedio del top-15 viral 0.026%. El CTA "comenta BIM o IA" multiplicó los comentarios ~100× respecto a la norma de la cuenta.
- Comparación completa vs. su estimación: `guiones/2026-07-08_chatgpt-losa-revit/simulacion.md` → §"Resultado real".

### Datos crudos añadidos a `fuentes/`

- `ig_design_modeling_dg_barrido-completo_2026-07-16.json` (124 reels, master deduplicado)
- `ig_design_modeling_dg_reel_Da1ABdbJ7ji_2026-07-16.json` (reel DM18 con transcript)
- `ig_design_modeling_dg_ultimos10_2026-07-16.json`

### Pendientes de esta pasada

- **Transcripción de audio** de DM19–DM124 (hoy hooks desde caption). Requiere ~30-40 corriditas por el límite de datos del plan free, o subir de plan.
- **Notas curadas** para los reels `⟨auto⟩` (los top ~13 ya están curados).
- Re-medir DM18 maduro (≥7 días) para cerrar su veredicto de alcance.
- Re-verificar la clasificación de estructura de la cola `⟨auto⟩`.

---

## Observaciones al vuelo (reconstruidas sobre 124 reels)

- **El motor viral de DMA es la REVELACIÓN-TÉCNICA, no el humor-CC.** Los 4 reels sobre 1M y la mayoría del top-15 son reveals de técnica/material de obra ("columnas de acero enterradas", "aislamiento sísmico", "encofrado modular", "pasajuntas"). El humor relatable (DIÁLOGO-HUMOR) es el **segundo** motor y el de mejor ratio de likes (el reel "ingenieros a las 11:47pm" tiene 9.6% likes/views), pero los picos absolutos de reach son técnicos.
- **La brevedad sigue subiendo el piso, pero no es requisito de viralidad.** Mediana por duración: <15s = 9,637 · 15-30s = 7,994 · 30-60s = 3,392 · 60-90s = 5,246 · >90s = 1,996. El top absoluto (4.7M) dura 10s, pero el 2º (1.7M) dura 72s: un reveal técnico fuerte escala a cualquier duración.
- **La conversación es el cuello de botella, confirmado a gran escala.** Mediana de comentarios/views = 0.013%; ni el reel de 4.7M pasa de 0.01%. El conteo de comentarios más alto de la cuenta es 759 (reel de 708k = 0.11%). **DM18, con el CTA "comenta BIM o IA", llegó a 1.90%** — el único reel que rompe el patrón. El problema nunca fue el alcance; es que casi ningún guion pide comentar.
- **El contenido BIM+IA sigue siendo un vacío.** Los reels marcados `[BIM+IA]` son pocos y de reach bajo-medio — pero DM18 prueba que el ángulo IA+criterio conecta con conversación. Es el puente natural entre el motor técnico (que ya funciona) y la venta del Máster.
- **Promos directas (PROMO-CURSO) rinden por debajo de la mediana** salvo cuando el ángulo es fuerte por sí mismo (título internacional). Confirma el diagnóstico previo: la venta va montada en contenido de valor, no en piezas de promo separadas.

**Pendiente de destilar en `patrones-de-viralidad.md`** (ya reescrito con estos hallazgos).
