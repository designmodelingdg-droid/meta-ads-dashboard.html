# IA en los cursos — plan de evaluación y resultados

**Pregunta de Dayana, 27-ago-2026:** más de 30 cursos de ingeniería
estructural en GHL; quiere meterles IA sin regrabar. Esto recoge el plan que
se discutió y lo que las pruebas van contestando. **Todavía no se construye
nada** — ese es el acuerdo.

---

## Las tres cosas distintas que puede significar «meter IA»

| | Qué es | Estado |
|---|---|---|
| **A** | Asistente que responde sobre el contenido que ya existe | candidato al piloto |
| **B** | Módulo transversal «IA aplicada a…», grabado una vez para los 30 | candidato al piloto |
| **C** | Ejercicios corregidos contra rúbrica | **prototipo ya existe**: el verificador de eficiencia + la guía de 5 verificaciones son exactamente eso, solo que viven fuera del curso |
| **D** | Tutor que sabe en qué lección va cada alumno | bloqueado por DATOS, ver prueba |

**La regla que manda sobre todo el diseño:** los alumnos firman planos. El
asistente responde sobre **el material del curso**, no sobre la norma; y
cuando algo no está en el material, **dice que no está**. Un asistente que
rellena huecos es peor que no tener asistente.

**El curso del piloto:** la Especialización en Acero (la más vendida, en
pauta). Pero el piloto corre sobre **los leads del lead magnet**, no sobre los
alumnos que pagaron — mismo perfil, cero riesgo sobre el producto que sostiene
la pauta.

**Precio y nombre (decidido en la discusión):** no se renombra nada hasta que
el agente exista y esté probado — regla 1 del agente de recursos. Y la
propuesta es asistente **gratis para todos** (cuesta centavos, es el argumento
de renovación) + corrección/asesoría priorizada **de pago como nivel nuevo**,
en vez de cobrarle el asistente a quien ya compró. Si aun así se cobra a
todos: corte por fecha, gratis para quien compró en los últimos 60 días.

---

## Prueba 1 · Ask AI de GHL — 27-ago, corrida por Dayana

Preguntó: *«¿Qué alumno va por el módulo 2 de la especialización de acero?
Pásame la lista de todos los cursos y productos».*

### Lo que contestó bien

- **Lee la estructura completa:** 63 cursos, 50 productos, los 9 módulos de un
  diplomado, las 9 fases y 34 lecciones de su módulo 2. Con nombres reales.
- **Y la mejor noticia: supo decir «no lo sé».** Sobre el progreso del alumno
  contestó textual que la API de membresías *«no expone el progreso de lección
  por estudiante»* y que *«el sistema de evaluaciones tampoco registra
  submissions para este diplomado aún»*, y ofreció el camino manual (panel de
  Memberships) en vez de inventar un dato. **Esa era la prueba que decidía
  todo, y la pasó.**

### El peligro que sí apareció — y no estaba en la lista

**Contestó sobre OTRO curso.** Se le preguntó por la *Especialización de
Acero* y respondió: *«La "especialización de acero" corresponde al curso
"Diplomado Universitario Internacional BIM: Edificaciones de Acero Estructural
y Hormigón Armado"»* — un diplomado de **9 módulos** cuyo módulo 2 es
«Proyectos estructurales sismorresistentes» con fases de RSA/Robot.

**El temario verificado de la Especialización tiene 3 módulos** (derivas /
estabilidad y perfiles / uniones — está en
`leadmagnets/GUIA-5-VERIFICACIONES-ACERO.md`). No cuadra. Con 63 cursos de
nombres parecidos, resolvió la ambigüedad **adivinando en vez de preguntando**
— y lo declaró con total confianza.

Para un uso admin es un tropiezo visible y corregible. Para un alumno sería
una respuesta segura y equivocada sobre el curso que pagó. **Este es el modo
de fallo a vigilar: no inventa datos, inventa a qué te refieres.**

### Lo demás que dejó la prueba

- **274 segundos** de reflexión para responder. Sirve para back-office; es
  inusable como tutor de alumno en vivo.
- **D no está bloqueado por acceso sino por datos:** el progreso fino no
  existe porque el curso **no genera submissions** — no tiene evaluaciones.
  La salida no es raspar la pantalla: es **añadir quizzes al curso**, que es
  lo que crea el dato. (Y Ask AI dice poder crear quizzes — sin probar.)
- De rebote: en la lista de cursos aparece **«5 Verificaciones en Acero ·
  Herramienta DMA»** — la membresía del lead magnet **ya está creada**. Falta
  su URL `/purchase-course` para pegarla en la página de gracias, que sigue
  con `URL_MEMBRESIA = ''`.

### Conclusión parcial

**Ask AI es el copiloto de administración** — de Dayana y el equipo, que es
además quien lo ve; los alumnos ni lo tienen en su portal. **No es el tutor
del alumno.** El tutor, si se hace, va embebido en la lección (iframe, como el
verificador), anclado al material del curso correcto y con tiempos de
respuesta normales.

---

## Las tres preguntas que faltan (para pegar en Ask AI)

1. **Desambiguar:** *«Lista todos los cursos que contengan "acero" en el
   nombre. ¿Cuál de ellos es la Especialización en Acero 2026, la del temario
   de 3 módulos?»* — resuelve si el error fue de mapeo o de catálogo.
2. **Profundidad:** *«¿Qué se explica DENTRO de la Fase N°5: Análisis Modal
   Espectral? Cítame el contenido de la lección, no el título.»* — dice si lee
   contenido o solo estructura. De esto depende la opción A.
3. **La trampa:** preguntar por un módulo que **no existe** en el curso
   correcto. Ya dijo «no sé» en progreso; falta verlo en contenido.

---

## Pendientes del plan general

- Sacar la transcripción de UNA clase de acero en Vimeo y ver si el texto
  aguanta solo (las clases de pantalla pueden no transcribir bien).
- Pedir a Patricio las preguntas que más se repiten de alumnos de acero — el
  banco de prueba real.
- El costo por alumno/mes del asistente — sin ese número, la decisión de
  cobrar es una corazonada.


---

## Decisión de Dayana, 04-sep: solo A y B

C (corrección de ejercicios) y D (tutor con progreso) quedan fuera por ahora.
El plan vivo es: **A** el asistente sobre el material existente, **B** un
módulo transversal grabado una vez.

## Prueba 2 · Vimeo — 04-sep, sonda automática

**10 de 12 clases de acero tienen subtítulos automáticos en español**
(`es-x-autogen`). El material para anclar el asistente **ya existe** — no hay
que regrabar ni transcribir.

**Pero la calidad es la que es.** La muestra (sesión introductoria) se
entiende de corrido, y falla justo en los términos técnicos: «sismo» sale como
«si modo», «sismorresistentes» como «mismo resistentes», «de acero» como «de
cero», «losas» como «Laos». Consecuencias de diseño:

1. **Las transcripciones sirven para ENCONTRAR el contenido**, no para citarlo
   textual. El asistente responde con lo que la clase explica, nunca citando
   la transcripción cruda como si fuera exacta.
2. **Las cláusulas de norma jamás salen de la transcripción** — salen de la
   guía verificada y de los PDF del curso. Un ASR que convierte
   «sismorresistente» en «mismo resistentes» no es fuente para un número.
3. Conviene un **glosario de corrección** (los ~30 términos del dominio) al
   indexar, para que la búsqueda encuentre «sismorresistente» aunque el texto
   diga otra cosa.

## La arquitectura acordada (respuesta a «¿dónde corre?»)

```
[Portal GHL: cada curso]                    [GitHub Pages]        [Render]
  botón/lección «Tutor IA»  ──iframe──►  página de chat DMA ──►  servicio propio
  (el acceso lo controla                  (HTML como las apps)    Claude API +
   una OFERTA de membresía)                                       transcripciones
                                                                  del curso
```

- **El botón va en todos los cursos; el ACCESO es una oferta de membresía.**
  Quien la tiene, entra; quien no, cae en la página de venta del upgrade. Así
  se activa «para todo el mundo» y se cobra a la vez — es el mismo mecanismo
  del lead magnet, sin infraestructura nueva de cobro.
- **El chat es una página nuestra** embebida por iframe en una lección, como
  el verificador. No es Ask AI (274 s, y es de administración), no es el bot
  de Patricio (ese vive en los DM y conversa con leads, no con alumnos dentro
  del curso).
- **El cerebro corre en Render** — el mismo patrón que ya usa
  `dma-sales-assistant` — llamando a la API de Claude con las transcripciones
  del curso **concreto**: la página pasa `?curso=acero` y el servicio solo
  carga ese material. Eso arregla por diseño el fallo de Ask AI de contestar
  sobre otro curso.
- **Regla dura en el servicio:** si la respuesta no está en el material,
  responde que no está y sugiere la asesoría. Nunca completa con conocimiento
  general.

## Qué se graba (opción B): UN módulo, no un curso

Nada de los 30 se regraba. Se graba **una vez** un módulo transversal —
p. ej. «IA aplicada a la ingeniería estructural» — y se añade como lección
extra a todos los cursos. Borrador de contenido (4 lecciones):

1. **Conectar Claude/ChatGPT al flujo de Revit** — el ángulo que más
   conversación genera según la matriz.
2. **Lo que la IA sí hace en tu flujo** (memorias de cálculo, comprobaciones,
   documentación) — con demo real.
3. **Donde la IA falla y tú vales: el criterio.** La frontera — es la forma
   que rinde 11-17 comentarios/1k en nuestra cuenta.
4. **Cómo verificar lo que la IA te da** — enlaza con la guía de las 5
   verificaciones y con el descargo profesional.
