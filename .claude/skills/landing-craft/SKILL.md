---
name: landing-craft
description: El suelo de calidad que comparten TODAS las landings de Design Modeling Academy (DMA). Define el proceso antes de escribir HTML — entrevista, documento de diseño, recorrido del visitante, curva de sensación con un pico, y verificación con capturas en escritorio y móvil — más las reglas duras de oficio (espaciado, tipografía, color, texto sobre imagen, profundidad, tarjetas, movimiento, estados) y la lista de lo que no se hace. NO genera una landing por sí solo: lo leen `landing-producto`, `landing-evento`, `landing-agenda` y `leadmagnet-app` ANTES de recopilar datos. ACTIVA cuando el usuario diga "landing-craft", "mejora esta landing", "esta landing parece plantilla", "revisa el diseño de la landing", "por qué esta página se ve genérica", "auditar una landing", o cuando vaya a construirse o retocarse cualquier página de DMA.
---

# landing-craft — el oficio que comparten todas las landings de DMA

Nuestras skills de landing funcionan rellenando `{{PLACEHOLDERS}}` sobre una
plantilla fija. Eso hace páginas rápido y hace que **todas se parezcan**: mismo
esqueleto, mismas secciones en el mismo orden, mismo ritmo. Una plantilla
rellenada cinco veces son cinco copias de la misma página, no cinco páginas.

Este archivo es lo que va ANTES del HTML. No sustituye a ninguna skill: las tres
de landing y la de lead magnets lo leen primero y después arman su plantilla.

> **De dónde sale:** adaptado de `scroll-craft`, de Nate Herk, en el fork de
> Luciano Mattica (MIT). Ver `ATRIBUCION.md`. Lo que NO nos aplica y por qué
> está al final, en «Lo que dejamos fuera».

---

## Paso 0 · La entrevista, antes de generar nada

Seis preguntas, en una sola tanda. Si ya están respondidas en el brief del
producto, no se vuelven a preguntar. Si Dayana delega la dirección creativa
(«hazlo tú», «usa tu criterio»), se escriben las decisiones como propias, se
marcan como tales, y se sigue — no se abre otro punto de aprobación.

1. **Qué es y para quién**, en una o dos frases suyas. Sin inferir la marca del
   nombre del producto.
2. **Qué tiene que creer el visitante al final.** UNA frase. Si dan tres, que
   elijan. No es una lista de características.
3. **Qué hace el visitante después.** Una acción, una etiqueta para el botón,
   la misma en toda la página.
4. **El recorrido, sección por sección, en su orden.** Qué ve primero, qué
   sigue, qué es lo último. Su secuencia, no un menú que le ofrecimos.
5. **Cómo debe sentirse en cada tramo, y cuál es el ÚNICO momento que tiene que
   recordar.** Esto es lo que alimenta la curva y el pico. Ver
   [references/sensacion.md](references/sensacion.md).
6. **Qué assets existen ya.** Fotos de obra, capturas de Revit, retratos de
   Gabriel, logo, material del curso. Lo real siempre gana a lo generado, y en
   una academia de ingeniería lo real es la mitad de la credibilidad.

Las referencias visuales se piden **de otros medios** —una revista, una luz, un
catálogo, una película— nunca «webs que te gusten». Nombrar webs es como una
página termina pareciéndose a otra web.

---

## Paso 1 · `DISEÑO.md` antes de una línea de HTML

Se escribe un archivo `DISEÑO.md` junto a la landing, y se muestra **antes** de
construir. Contiene:

- **Las 3 P:** el dolor (en palabras del ingeniero, no de marketing), la persona,
  la promesa.
- **La frase que el visitante tiene que creer al final.**
- **El recorrido**, sección por sección, con lo que siente en cada una.
- **La curva de sensación y el pico** — ver `references/sensacion.md`.
- **El sistema visual:** la paleta DMA con roles, las dos tipografías, el
  espaciado, el tono de las fotos.
- **Las reglas duras** de esta página en concreto (qué no va).
- **Qué cambia en móvil.** No «se adapta»: qué cambia.
- **La lista de imágenes** con nombre de archivo, formato, orientación y en qué
  sección va cada una.

Si falta un dato importante, se pregunta antes de escribir. Si Dayana pide datos
provisionales, se ponen y se marcan como inventados **dentro del documento**.

---

## Paso 2 · El recorrido y la curva

Primero los tramos (4 a 7), cada uno un cambio en lo que el visitante sabe o
siente:

```
1  Reconocimiento   se ve a sí mismo en el problema
2  Tensión          lo que le está costando, dicho sin rodeos
3  Giro             lo que cambia
4  Sustento         por qué esto se sostiene (avales, método, casos)
5  Alcance          qué puede elegir
6  Decisión         la única acción
```

Una sección que no sirve a ningún tramo se corta, por bonita que sea.

**Después la curva de sensación, y solo después los elementos visuales.** Elegir
el recurso visual antes que la emoción es elegir un recurso buscando una excusa.
Dos tramos seguidos con la misma sensación significa que uno sobra.

**Un solo pico por página.** Se lleva el mejor asset, el silencio de antes y el
mayor espacio. Tres momentos impresionantes se aplanan entre ellos y el visitante
se va sin poder decir qué vio. Método completo en
[references/sensacion.md](references/sensacion.md).

---

## Paso 3 · Construir

HTML real: `<h1>` de verdad, `<p>` de verdad, orden de lectura de verdad.

Se lee [references/oficio.md](references/oficio.md) **antes** de escribir markup,
no después. Está el espaciado, la tipografía, el color, el texto sobre imagen, la
profundidad, las tarjetas, el movimiento, los estados y la lista de lo que no se
hace.

Recordatorio de nuestro contexto: el HTML se pega en **GHL → Sites → Custom Code
container**, y GHL pone `<html>`, `<head>` y `<body>` por su cuenta.

---

## Paso 4 · Verificar mirándola

No es opcional y no es «debería funcionar». Procedimiento en
[references/verificacion.md](references/verificacion.md).

Mínimo, en cada entrega:

1. Captura a **1200 px** y a **390 px**.
2. **Abrir las capturas y mirarlas.** El script dice que cargó; no dice si la
   jerarquía se entiende, si el titular respira o si la foto está cortada por la
   mitad.
3. La prueba del entrecerrado: difuminar hasta perder el detalle y comprobar que
   todavía se distinguen el elemento principal, el secundario y los grupos.
4. Contraste medido sobre el render, no a ojo: cuerpo ≥ 4.5:1, texto grande ≥ 3:1.
5. Los enlaces responden (no basta con que existan).

Se reporta lo que se verificó **y lo que no**.

---

## Reglas duras

Bloquean la entrega. Cada una es algo que hace que una página se lea como hecha
a máquina.

| Nunca | En su lugar |
|---|---|
| Cifras inventadas en un contador («+4.500 egresados» sin fuente) | Solo números reales. Sin número, sin contador. Es la regla 1 de la casa |
| Una rejilla de tarjetas idénticas icono + título + texto como estructura | Rejilla asimétrica, zigzag de dos, un riel, o tipografía sobre espacio |
| Tres columnas iguales de tarjetas de características | Lo mismo de arriba |
| Un eyebrow encima de cada título de sección | Como mucho uno cada tres secciones |
| Contadores de sección `01 / 06` | Fuera. La secuencia no es información aquí |
| Señales de «scroll», flechas, ratón animado | Nada. Están mirando el hero, ya lo saben |
| Raya larga (—) visible en el copy | Punto, coma, dos puntos o paréntesis |
| Todo el copy centrado | Variar el anclaje: inicio, final, centro, partido |
| Texto quemado dentro de una imagen generada | Markup real, siempre. Se selecciona, se traduce y se ve nítido |
| Texto degradado, glow de neón, sombras de halo sin desplazamiento | Peso y tamaño para enfatizar; sombras con desplazamiento y desenfoque |
| `transition: all`, o animar `width`/`height`/`top`/`left` | `transform` y `opacity`; `clip-path` para barridos |
| Un velo oscuro sobre todo el fotograma para arreglar el contraste | Un velo solo donde está el texto |
| Un hero que desborda la pantalla | Titular máximo dos líneas, subtexto máximo 20 palabras, CTA visible sin bajar |
| Más de cuatro elementos de texto en el hero | Los avales, el precio y las micro-frases bajan a su propia sección |
| Emojis haciendo de sistema de iconos | Una librería de iconos de verdad |
| Verbos de relleno: potencia, revoluciona, lleva al siguiente nivel | Decir qué hace |
| Un final que se desvanece en el footer | El cierre resuelve y se sostiene. La última sensación es la que se llevan |
| Entregar sin capturas miradas | Paso 4 |

---

## Lo que dejamos fuera de scroll-craft, y por qué

Esto no es un recorte por pereza: es que nuestras landings viven **dentro de
GHL**, no en un sitio propio.

- **El motor de scroll (58 KB de JS) y el vídeo que se rebobina con la rueda.**
  Dentro de un Custom Code de GHL es frágil, y nuestro público entra desde el
  móvil con datos en Ecuador. Una página que pesa 30 MB no la ve nadie.
- **La generación de imagen y vídeo con kie.ai.** Es de pago y ya tenemos
  `imagen-marca-dma` (Higgsfield) y el banco de imágenes propio.
- **El «mundo continuo» (worldflight) y los vuelos de cámara.** Caros, frágiles y
  para marcas de producto, no para una academia que vende con argumentos.
- **El registro de huellas (FINGERPRINTS.md).** La idea sí nos sirve —que la
  landing del Máster no sea la del Diplomado con otro color— pero se resuelve con
  el recorrido y la curva, no con un registro aparte.

Si algún día hay que hacer un sitio propio fuera de GHL, el plugin completo está
en `herramientas/scroll-craft/`, con su documento de uso.
