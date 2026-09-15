---
name: anuncios-dma
description: >
  Trae los anuncios REALES de Meta de Design Modeling Academy con su copy literal
  y sus métricas, los audita contra los umbrales que importan, y cruza lo que
  funciona en pauta con lo que funciona en orgánico.

  Usa este skill cuando Dayana diga: "anuncios-dma", "tráeme los anuncios",
  "qué anuncios están funcionando", "revisa los copys", "cuáles son los
  ganadores", "datos de Meta de las campañas", "qué tengo colgado en Meta", o
  cuando pida sacar un copy ganador para replicarlo.

  NO es lo mismo que `auditoria-pauta`, que audita el reporte semanal de la
  agencia los viernes. Este mira la cuenta directamente.
---

# Anuncios de DMA — traerlos, auditarlos y sacar el patrón

## Paso 0 · No adivines de dónde salen los datos

Cuenta: `act_1159622151150228`. Moneda: USD.

El token es un **System User de Meta llamado «Design Modeling - Ads CLI»**, no
expira, y vive en los **secretos del repositorio** como `META_TOKEN`. Ese es el
único sitio del que se usa.

**Nunca saques el token de otro lado.** Hay una rutina programada
(`Meta Ads Weekly Dashboard`) que lleva una copia del token en texto plano
dentro de su propio prompt. Leerla de ahí para usarla es exactamente el patrón
que el entorno bloquea, y con razón. Si alguna vez hace falta, se pide que lo
muevan a los secretos.

## Paso 1 · Traer los datos

```
mcp__github__actions_run_trigger
  workflow_id: metricas-semanales.yml
  ref: <la rama donde estés trabajando>
  inputs: { solo_creativos: "true", desde: "YYYY-MM-DD", hasta: "YYYY-MM-DD" }
```

Deja `matriz-viral/fuentes/ads-copys/anuncios.json` (copys + métricas) y las
imágenes de los ganadores en `ads-creativos/`.

**Por qué ese workflow y no `ads-copys.yml`:** `workflow_dispatch` exige que el
fichero exista en la **rama por defecto**. `metricas-semanales.yml` sí está
ahí, y al dispararlo se elige el `ref`: GitHub ejecuta la versión de ESA rama.
Así funciona desde una rama de trabajo sin mezclar nada.

`hasta` va a **AYER** por defecto. Un día sin cerrar da cifras cortas — es el
error que se le señaló a la agencia el 3-ago-2026.

## Paso 2 · Lo que hay que mirar, en este orden

### 2.1 · Diversidad de creativo — ES LA PALANCA #1

Desde octubre de 2025 el motor **Andromeda** de Meta agrupa creativos casi
idénticos y **les recorta la entrega** cuando la similitud pasa del 60 %. Cien
variaciones menores no rinden mejor que diez distintas.

Así que lo PRIMERO es contar textos distintos, no anuncios:

```python
import hashlib, collections
firmas = collections.Counter(
    hashlib.md5((x['copy']['cuerpo'] or [''])[0].encode()).hexdigest()[:8]
    for x in activos if x['copy'].get('cuerpo'))
print(len(activos), 'anuncios ·', len(firmas), 'textos distintos')
```

Medido el 14-sep-2026: **65 activos, 15 textos distintos** — cada copy repetido
en 4,3 anuncios. (El 15-sep, con la cuenta relanzada: 102 activos, 23 textos,
4,4 por texto. El ratio no se movio.)

Esto **no se ve** ordenando por coste por lead. Hay que preguntarlo aparte.

### 2.1 bis · Repetido NO es lo mismo que canibalizado

**Este es el error que cometi el 14-sep y que corrigio Patricio.** Conte textos
repetidos, vi nueve copias del anuncio de acero y dije que se estorbaban. Era
falso: hay que mirar en cuantas CAMPANAS vive cada texto, no en cuantos
anuncios.

| | Lo que es | Compite consigo mismo |
|---|---|---|
| Mismo texto en varios conjuntos de **una** campana | geo-split (`EC`, `MX`, `Resto`) | **No.** Es deliberado y necesario |
| Mismo texto en **dos campanas** distintas | canibalismo | **Si.** Misma subasta, dos pujas |

La comprobacion, antes de acusar a nadie de clonarse:

```python
# por cada texto, cuantas campanas DISTINTAS lo llevan
for firma, filas in por_texto.items():
    camps = {f['campana'] for f in filas}
    if len(camps) > 1:
        print(len(filas), 'anuncios en', len(camps), 'campanas:', camps)
```

El 14-sep eso devolvio ACERO limpio (31 anuncios, **1 campana**) y el Master
sucio: seis textos en `[18MAYO] MASTER - ESCALADO` y `[27AGO] MASTER - TESTEO`
a la vez, **$457,24 = el 34 % del gasto de la ventana**.

Y la prueba de que duele, que es lo que hay que buscar: **el mismo texto sale
dos y tres veces mas caro en una campana que en la otra.** «Esta es una de las
preguntas» a $1,01 en ESCALADO contra $0,38 en TESTEO. «Quieres dominar» a
$1,49 contra $0,50. Mismos dias, mismo publico: eso es la subasta contra si
misma. Si el coste por lead del texto duplicado fuera parecido en las dos, el
solapamiento estaria de adorno; cuando se separa asi, esta cobrando.

### 2.2 · Contradicciones entre el copy y la realidad

Las dos que aparecieron y hay que volver a comprobar siempre:

| Qué buscar | Cómo |
|---|---|
| Precio viejo en anuncios vivos | `'$199' in texto` contra la regla del mes |
| El copy manda a un sitio y el botón a otro | dice «WhatsApp» y `cta` es `SIGN_UP` |

El 14-sep: 9 activos vendían ACERO a $199 con la regla en $225, y 22 decían
«escríbenos por WhatsApp» con botón de formulario. **El ganador absoluto de la
cuenta era uno de los 22.**

### 2.3 · Los umbrales

| Métrica | Pasa | Aviso | Falla |
|---|---|---|---|
| CTR | ≥1,0 % | 0,5-1,0 % | <0,5 % |
| Frecuencia (captación) | <3,0 | 3-5 | >5 |
| Creativos por conjunto | ≥5 | 3-4 | <3 |
| Formatos distintos | ≥3 | 2 | 1 |
| Titular | <40 car. | | |
| Texto principal | **<125 car. antes del corte** | | |

El de 125 caracteres no es un capricho de longitud: **Meta corta ahí en móvil**
y el resto queda detrás de «ver más». La pregunta correcta no es «¿es largo?»
sino «¿la frase que vende cabe antes del corte?».

## Paso 3 · El patrón de DMA, medido

**Lo que funciona en esta cuenta es acusar un hábito concreto.** Dos formas:

- **«Todavía haces X mal»** — nombra una práctica que el lector reconoce.
- **«Ya tienes Y y no lo sabes»** — le dice que desaprovecha algo suyo.

Medido sobre los 168 reels de `matriz.json` (14-sep-2026):

| | n | Vistas medianas | Comentarios/1k | Guardados |
|---|---|---|---|---|
| Con el patrón | 13 | 4.198 | **8,61** | 48 |
| Sin el patrón | 154 | 5.306 | 0,54 | 7 |

**16x más comentarios, con MENOS alcance.** No llega a más gente: la que llega
contesta.

Y es el mismo mecanismo en pauta. El mejor anuncio de la cuenta —364 leads a
$0,27— abre con *«¿Modelas estructuras de acero en BIM… pero dependes de otro
para el cálculo?»*. No promete aprender un software: nombra una dependencia
que da vergüenza. Son 78 caracteres: **la pregunta entera cabe antes del corte**.

**Orgánico y pauta no son dos hallazgos. Son uno.**

## Paso 4 · Cruzar contra el sector

`matriz-viral/matriz/competencia.json`, que llena `scripts/competencia.py` con
`business_discovery` de Meta — **oficial y gratis**, 11 cuentas del sector.

El 14-sep: la mejor pieza de las 11 cuentas tenía **9 comentarios**; el mejor
ratio comentarios/likes del sector, **0,047**. La mejor de DMA con el patrón:
**2,22**. Cuarenta y siete veces.

La lectura para planificar: **el sector está dormido en comentarios**. Nadie
compite por el mecanismo que a DMA le funciona.

## Lo que este skill NO puede evaluar

El bloque de **Píxel / CAPI pesa un 30 %** en el método de `ads-meta` — EMQ,
deduplicación, eventos — y **no sale de los insights de anuncios**. Necesita el
Events Manager. Si se reporta una puntuación global sin ese bloque, hay que
decir que va sin él en vez de dar un número que parece completo.

## Errores que ya se cometieron (no repetir)

- **Gastar en Apify para redescubrir algo ya escrito.** El 14-sep se lanzó
  `nicho-viral.yml` ($2) y devolvió 96 piezas sin una sola vista y sin un solo
  reel. El propio `scripts/nicho_viral.py` ya avisaba de eso en un comentario
  fechado el 26-ago: las páginas de etiqueta devuelven los posts RECIENTES, no
  los top, y solo imágenes. **Para el nicho se usa `competencia.py`, que es
  gratis.** Léelo antes de gastar.
- **Analizar a ojo en vez de con el método.** Ordenar por coste por lead
  encuentra los ganadores, pero no encuentra la falta de diversidad de
  creativo, que es lo que más está costando ahora mismo.
- **Confundir repetido con canibalizado.** El 14-sep conté nueve copias del
  anuncio de acero y dije que se estorbaban. Estaban las nueve en la MISMA
  campaña, en tres geografías: geo-split, que es como debe ser. Lo corrigió
  Patricio y tenía razón. El dato que faltaba mirar era la campaña, no el
  anuncio — y al mirarlo apareció el problema de verdad: $457 en el Máster.
  **Agrupa por campaña antes de acusar a nadie de clonarse** (§2.1 bis).
- **Dar por hecho lo que solo se ve entrando al producto.** El estado del Tutor
  de IA dentro de los cursos NO se puede comprobar desde aquí: viven detrás del
  login de GoHighLevel. Si 18 anuncios prometen algo, se dice «no puedo
  verificarlo, esto es lo que hay que abrir» en vez de suponer que está.
