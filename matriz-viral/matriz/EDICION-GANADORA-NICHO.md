# Edición ganadora en el nicho BIM + IA (8-oct-2026)

Investigación pedida por Dayana: qué formato y qué edición funcionan en el nicho (no solo en la competencia directa, que vende menos que DMA) para editar mejor **los anuncios** y **los videos de valor**.

Datos crudos: `matriz-viral/fuentes/edicion-ganadora/datos-2026-10-08.json` (script `scripts/edicion_ganadora.py`, Action `edicion-ganadora.yml`). Gasto de Apify ≈ **$1,80** (tope $2,50).

## La muestra, y lo que no dice

| Fuente | Qué se trajo | Señal de «gana» |
|---|---|---|
| TikTok | 83 videos de 6 búsquedas («revit ia», «revit ai», «revit inteligencia artificial», «bim inteligencia artificial», «bim ai», «revit tips»); 37 en español | Vistas, y veces la mediana de su propia cuenta |
| Biblioteca de Anuncios de Meta | 120 anuncios ACTIVOS con video («revit», «curso bim», «bim inteligencia artificial»); 89 son de BIM/Revit; **54 llevan más de 90 días activos y 32 más de 180** | Días activo: nadie paga 300 días un anuncio que no vende |
| Instagram | 11 reels de AECODE, BIM Pure y Zigurat (el actor de reels cuesta ~$0,03 por reel y el tope cortó en 20) | Comentarios por cada 1.000 vistas |
| YouTube Shorts | 0 útiles (el actor no devolvió shorts) | — |

Los 10 mejores de cada fuente se bajaron y se miraron cuadro a cuadro (hojas de contacto) y con ffmpeg (duración, cortes, segundo del primer corte).

Lo que hay que leer con cuidado:
- Las vistas de TikTok son absolutas y no dicen nada de ventas. Los anuncios que llevan meses activos sí son la mejor pista de venta que hay en público.
- La búsqueda de anuncios por palabra en todos los países trajo ruido (tiendas de motos, otros idiomas). Solo se analizaron los de BIM/Revit.
- La detección de cortes mide cambios de plano, no cambios de subtítulo: un video con subtítulos frenéticos y una sola toma da «0 cortes».

## Lo que se repite en lo que gana

### 1 · El tema caliente es «conectar la IA a Revit» (MCP)
De los 12 TikTok más vistos, **6 son Claude/IA conectado a Revit**:
- lexmrbim, 175 mil y 108 mil vistas (10,5 y 6,4 veces su mediana);
- **AECODE, 110 mil (87 veces su mediana)**;
- Geopogo, 90 mil y 58 mil;
- ing.luisvelez, 60 mil.

Es exactamente el tema del workshop del 22.

Varios prometen que la IA **edita o modela** el modelo. Lo logran con plugins de terceros, no con el conector oficial de Revit 2027, que es de solo lectura. **Nuestra diferencia es decir qué sí y qué no**, sin perder el gancho.

### 2 · Ganchos que funcionan en los primeros 2 segundos
- **Miedo o provocación:** «¿Claude acaba de reemplazar a los modeladores BIM?» (AECODE, 110 mil) · «BIM is dead» (191 mil).
- **Número grande:** «AI just designed a $31M hotel» (1 millón).
- **Promesa sin barrera:** «¿Conectar Revit con IA sin saber programar? Sí, es posible» (lexmrbim, 175 mil).
- **Reto visual:** «Claude models the Eiffel Tower in Revit» (Geopogo, 90 mil).

El gancho va **escrito arriba y fijo durante todo el video**, no solo dicho.

### 3 · Tres plantillas de edición dominan

**A · «Tres bandas» (demo de pantalla).** Es la nueva y la que más se repite en IA + Revit:
- arriba, el titular fijo en 2 líneas (la pregunta o el reto);
- al centro, la grabación de pantalla real;
- abajo, la banda fija con el CTA o la oferta («Únete al curso gratuito…», «Últimos 5 cupos»);
- subtítulos de 1 o 2 palabras entre la pantalla y la banda, con la palabra clave en una caja de color.

Se ve en AECODE (TikTok, 24 s) y Geopogo (18 s). Es la más corta: **18 a 35 s**.

**B · «Presentador + B-roll».**
- La cara de un presentador real con el titular encima en 2 líneas (blanco y amarillo).
- Cortes a B-roll o pantalla cada ~2 s (build.with.alan, 1 millón, 4,9 cortes por cada 10 s).
- Subtítulos de 1 palabra en caja amarilla.

**C · «Tutorial con pasos».**
- Grabación de pantalla con logos 3D grandes que entran (Revit, Claude) y «PASO #2 / PASO #3» como títulos.
- Subtítulos amarillos de 2 palabras y algún meme de reacción (lexmrbim, 34 s, 3,6 cortes por cada 10 s).

### 4 · La duración no es lo que separa
La mediana de los 20 TikTok más vistos es 50 s, y la del resto, 46 s. Lo que separa es **el gancho escrito y que algo cambie en pantalla cada 1 a 3 segundos** (subtítulo, captura, corte).

### 5 · Comentarios: solo con palabra
En TikTok los ganadores sacan entre 0,1 y 1,2 comentarios por cada 1.000 vistas. El reel de AECODE en Instagram con «Comenta BIM» saca **18,7**. Es lo mismo que dice nuestra propia matriz: sin palabra no hay comentario.

## Lo que se repite en los anuncios que llevan meses activos

| Anunciante (idioma) | Días activo · variantes | Cómo está editado |
|---|---|---|
| **Taller Lap** (español, Revit) | 293–432 días, **3–4 variantes activas** | Presentador de pie frente a una casa u obra real, plano abierto. Subtítulos grandes de 2–3 palabras con la palabra clave en rojo o amarillo. **Las cajas del producto fijas abajo todo el video** («PAQUETE 7x1», «SISTEMA 8x1»). Cortes a Revit. Cierre con el logo. 30–45 s |
| **Arq. Luis Raez** (español) | 340 días | Presentador sentado en primer plano y B-roll en **mosaico** (2 o 3 imágenes apiladas: render, Revit, plano) que cambia rápido. Subtítulo de 1 palabra en caja azul. Vuelve a la cara para el cierre |
| **CAPCI Perú** (español) | activo | Sin presentador: **resultados reales de estudiantes** (modelo, planos, render) y al final la ficha del curso (horarios, horas, certificación). ~60 s |
| **Julia Instalações BIM** (portugués) | activo | **«Proyecto vs obra»**: presentadora con el modelo de Revit al lado de la foto de la obra real. Cifras grandes en pantalla («31 CM»). ~100 s |

Lo común a los anuncios que duran:
1. **Persona real**, nunca avatar.
2. **La oferta siempre visible**: el producto o la banda fija abajo de principio a fin.
3. **Prueba visual**: modelo contra obra, resultados de alumnos o la demo en pantalla.
4. **Son explicativos, no frenéticos**: 30 a 60 s, con un plano largo del presentador y cortes a pantalla.
5. **Varias variantes del mismo video** activas a la vez: cambia el gancho, no el cuerpo.

## Las dos fichas para DMA

### Ficha 1 · Anuncios (30–45 s, 9:16)
| Tramo | Qué va |
|---|---|
| 0–3 s | Gancho escrito arriba y fijo (2 líneas, blanco + naranja #E8893A), dicho por Gabriel en el primer segundo. Número o dolor concreto: «¿Cuántas naves dijiste que no?», «Le pregunté a mi modelo cuántas puertas no tienen resistencia al fuego». |
| 3–25 s | Prueba en pantalla dividida: arriba, Revit/Robot real o la demo de la IA; abajo, Gabriel (en obra o en su escritorio). Algo cambia cada 1–3 s. |
| Todo el video | **Banda fija abajo con la oferta** (workshop, recurso gratis o Acero sin precio del Máster) y subtítulos de 1–2 palabras con la palabra clave en caja naranja, entre la pantalla y la banda. |
| 25–40 s | Una frase de criterio (lo que la IA no hace, o para quién NO es) y el CTA: «Comenta PALABRA» o el botón del anuncio. Logo 1–2 s. |
| Variantes | 3 o 4 versiones del mismo cuerpo con distinto gancho (como Taller Lap). Se apagan las que no rinden; no se produce un video nuevo por cada idea. |

### Ficha 2 · Videos de valor
- **Demos de software (IA + Revit, Robot, el tutor):** plantilla **«Tres bandas»**, 20–35 s:
  - titular-pregunta fijo arriba;
  - pantalla real al centro;
  - banda abajo con «Comenta PALABRA»;
  - subtítulos de 1–2 palabras con palabra clave en caja.
  
  Es la que hoy gana en IA + Revit. Se suma como **Estilo C** a los dos aprobados.
- **Gabriel explicando:** el **Estilo B aprobado** (pizarra + presentador), con el titular de 2 líneas en el gancho y subtítulos de 1 palabra en caja. Ya coincide con lo que gana (build.with.alan).
- **Tutoriales por pasos:** el **Estilo A aprobado**, con «PASO 1 / 2 / 3» grandes, como el tutorial de lexmrbim. Memes de reacción, como mucho uno, y solo si encaja con la marca.
- **Siempre:**
  - gancho escrito en el primer segundo y fijo;
  - nada quieto más de 2–3 s;
  - cierre con palabra clave viva;
  - y nuestra marca de criterio: lo que la IA sí y no hace, con la versión y la licencia cuando dependa de ellas.

## Para la otra conversación (pegar tal cual)

> Edita mis videos con lo que gana hoy en el nicho BIM + IA. El detalle está en `matriz-viral/matriz/EDICION-GANADORA-NICHO.md` del repo meta-ads-dashboard.html, con datos de Apify del 8-oct-2026.
> **Anuncios (30–45 s):**
> - gancho escrito arriba y fijo + dicho en el 1.er segundo;
> - prueba en pantalla dividida (Revit/Robot o demo de IA arriba, Gabriel abajo, persona real);
> - banda fija abajo con la oferta todo el video;
> - subtítulos de 1–2 palabras con palabra clave en caja naranja;
> - una frase de criterio y CTA con palabra;
> - 3–4 variantes con distinto gancho.
>
> **Videos de valor:**
> - demos en plantilla «Tres bandas» (titular-pregunta fijo arriba, pantalla real al centro, banda con «Comenta PALABRA» abajo), 20–35 s;
> - Gabriel explicando, con el Estilo B aprobado (pizarra + presentador);
> - tutoriales, con el Estilo A aprobado y «PASO 1/2/3» grandes;
> - nada quieto más de 2–3 s.
>
> **Tema que más rinde:** conectar la IA a Revit (MCP). Decir siempre que el conector oficial de Revit 2027 es de solo lectura.
> **Marca DMA:** navy, naranja #E8893A, Bebas Neue o Montserrat. Nunca el precio del Máster.
