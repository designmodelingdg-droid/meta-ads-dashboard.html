# Qué funciona de verdad — medido, para armar octubre

Cruce completo del 14-sep-2026. Tres fuentes, todas oficiales:

| Fuente | Qué aporta | Fichero |
|---|---|---|
| Graph API orgánica | 168 reels de DMA con vistas, comentarios y guardados | `matriz.json` |
| Meta Ads API | 134 anuncios con su copy literal y sus métricas | `fuentes/ads-copys/anuncios.json` |
| `business_discovery` | 11 cuentas del sector | `competencia.json` |

---

## 1 · El hallazgo: acusar un hábito concreto

Las piezas que funcionan en esta cuenta no enseñan: **acusan**. Dos formas de
lo mismo:

- **«Todavía haces X mal.»** Nombra una práctica que el lector reconoce en sí
  mismo. *«Si todavía dimensionas zapatas a ojo…»*
- **«Ya tienes Y y no lo sabes.»** Le dice que desaprovecha algo que ya pagó.
  *«Tu Revit ya trae IA y poca gente la activó.»*

Las dos son **discutibles**. Por eso la gente comenta en vez de mirar.

### Medido sobre los 168 reels

| | n | Vistas medianas | Comentarios/1k | Guardados med. |
|---|---|---|---|---|
| **Con** el patrón | 13 | 4.198 | **8,61** | **48** |
| Sin el patrón | 154 | 5.306 | 0,54 | 7 |

**16 veces más comentarios — con menos alcance.** Ese detalle es el importante:
no es que llegue a más gente, es que **la gente que llega contesta**.

### Los mejores, por comentarios sobre likes

| c/likes | Comentarios | Pieza |
|---|---|---|
| **2,22** | 142 | «Si **todavía** dimensionas zapatas **a ojo**…» |
| 1,47 | 91 | «Tu Revit **ya trae** IA y **poca gente** la activó» |
| 0,97 | 65 | «Si todavía dimensionas zapatas a ojo» (2.ª versión) |
| 0,95 | 56 | «La IA **ya hace** 5 tareas de tu trabajo BIM. La 6.ª…» |
| 0,85 | 55 | «ChatGPT diseña una losa → la IA **falla en** el criterio» |
| 0,36 | 149 | «Sobredimensionar **no es** ir por el lado seguro» |
| 0,20 | 95 | «El 1 % **no es un capricho**» |

## 2 · Lo mismo vale en pauta

El mejor anuncio de la cuenta —**364 leads a $0,27**— abre así:

> ¿Modelas estructuras de acero en BIM… **pero dependes de otro para el cálculo?**

Es el mismo mecanismo. No promete aprender un software: **nombra una
dependencia que da vergüenza**. Y son 78 caracteres, así que la pregunta entera
cabe antes del corte de «ver más» que Meta hace a los ~125.

**Orgánico y pauta no son dos hallazgos. Son uno solo.**

## 3 · El sector está dormido

Las 11 cuentas del sector, entre ellas una de 119.700 seguidores:

| | Sector | DMA con el patrón |
|---|---|---|
| Mejor pieza por comentarios | **9** | 142 |
| Mejor ratio comentarios/likes | **0,047** | **2,22** |

**47 veces.** Nadie en el sector compite por el comentario: publican obra
terminada y proyecto bonito, que trae likes y silencio.

Esto no es una palmadita. Es una ventana: **el mecanismo que funciona no está
disputado**, y eso puede cambiar en cuanto alguien lo note.

*(Muestra: las ~12 publicaciones más recientes de cada cuenta. `business_discovery`
no da el histórico ni las vistas de cuentas ajenas.)*

## 4 · El eje OBRA, con números

| | n | Vistas medianas | Comentarios/1k |
|---|---|---|---|
| OBRA | 78 | **9.516** — el más alto | **0,17** |
| NÚCLEO-BIM | 24 | 3.882 | 0,00 |
| NÚCLEO-IA | 32 | 2.202 | 0,00 |
| PROMO | 10 | 2.628 | 2,28 |

OBRA es casi la mitad del histórico y **el que más alcance da y menos
conversación**. Para una cuenta que capta por comentario, es tráfico caro de
sostener.

Y ojo con NÚCLEO-BIM y NÚCLEO-IA en 0,00: **no es que el tema no funcione** —
es que se publicaba en modo enseñar, no en modo acusar. Las piezas del patrón
son de esos mismos ejes.

## 5 · Lo que esto propone para octubre

1. **El patrón deja de ser un formato y pasa a ser la regla.** Toda pieza de
   valor abre acusando un hábito o revelando algo desaprovechado. Si un guion
   no puede escribirse así, es señal de que el ángulo todavía no está.

2. **Bajar OBRA.** No a cero —trae alcance y a veces cae gente buena—, pero 78
   de 168 es demasiado para lo que devuelve en conversación.

3. **Reescribir NÚCLEO-BIM y NÚCLEO-IA en modo acusación.** El tema ya está
   validado; lo que falla es el ángulo.

4. **Un banco de hábitos acusables.** Es el cuello de botella real de este
   método: hace falta una lista de cosas concretas que el gremio hace mal y
   reconoce. Salen de las clases de Gabriel, del tutor de IA y de los
   comentarios de las piezas que ya funcionaron.

5. **En pauta: separar los textos duplicados ENTRE CAMPAÑAS.** 65 anuncios
   activos con 15 textos distintos, y Andromeda recorta la entrega a los casi
   idénticos.

   > **Corregido el 15-sep, y la corrección es de Patricio.** Este punto decía
   > que «las nueve copias del anuncio de acero se estorban entre ellas». Es
   > falso: ACERO son 31 anuncios en **una sola campaña**, repartidos en `EC`,
   > `MX` y `Resto`. Eso es geo-split, es deliberado y no compite consigo mismo.
   >
   > El canibalismo real está en el **Máster**: seis textos corriendo en dos
   > campañas a la vez (`[18MAYO] ESCALADO` y `[27AGO] TESTEO`), **$457,24 —
   > el 34 % del gasto de la ventana**. Y el mismo texto sale a $1,01 en una y
   > a $0,38 en la otra. Detalle en `COPYS-CORREGIDOS-ACERO.md`.

   Lo que hay que contar no es cuántos anuncios repiten un texto, sino **en
   cuántas campañas vive ese texto**. Un texto por ángulo, en una campaña.

---

## Cómo se rehace este cruce

```bash
# orgánico + sector + anuncios, todo en una corrida
mcp__github__actions_run_trigger  metricas-semanales.yml
   inputs: { solo_creativos: "true", desde: ..., hasta: ... }
```

El método está en el skill `anuncios-dma`.

**No uses `nicho-viral.yml` para esto.** Cuesta dinero y las páginas de
etiqueta de Instagram devuelven los posts *recientes*, no los top: el 14-sep
gastó $2 para traer 96 piezas sin una sola vista y sin un solo reel. El aviso
ya estaba escrito dentro del propio script desde el 26-ago. Para el sector se
usa `competencia.py`, que es la API oficial y es gratis.
