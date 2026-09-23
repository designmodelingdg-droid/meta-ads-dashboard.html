# Tutor IA del Diplomado BIM Estructuras — estado y montaje

**Todavía NO está publicado, a propósito.** Esta carpeta no está en
`publish-matriz.yml`, así que no sale a Pages. Se conecta el último, cuando el
servidor ya tenga las clases del Diplomado cargadas.

## Qué es

La misma página que el tutor del Acero, con una diferencia: manda
`programa: 'diplomado-estructuras'` en cada pregunta. El servidor
(`dma-tutor.onrender.com`, repo privado `dma-sales-assistant`) tiene ahora un
corpus y un índice por programa, así que responde solo con las clases del
Diplomado.

## El guardián del orden de despliegue

Un servidor anterior al 23-sep no sabe de programas: ignoraría `programa` y le
contestaría a un alumno del Diplomado **con las clases del Acero, diciéndole
que es su material**. Para que eso no pueda pasar, la página pregunta primero a
`/tutor/salud` si el Diplomado está cargado. Si no lo está —servidor viejo, o
nuevo sin corpus— la caja queda cerrada con «todavía se está preparando» y no
se manda ninguna pregunta. Probado contra el servidor real el 23-sep: solo
consultó `/tutor/salud` y no gastó ninguna pregunta.

## Lo que falta, en orden

| # | Qué | Quién |
|---|---|---|
| 1 | Confirmar qué carpetas de Vimeo son del Diplomado (ver abajo) | quien haya visto el curso en GHL |
| 2 | Bajar el corpus (Action «Tutor — bajar corpus», `programa=diplomado-estructuras`) | Claude |
| 3 | Probar con preguntas reales y medir memoria | Claude |
| 4 | Fusionar el PR del servidor → Render redespliega | Dayana |
| 5 | Añadir esta carpeta a `publish-matriz.yml` y hacer la tarjeta con las horas reales | Claude |
| 6 | Custom Block en el curso del Diplomado en GHL, como el del Acero | Ester y Aylin |

**La tarjeta (`tarjeta-tutor.png`) no se copió del Acero**: dice «de tu
Especialización», «tus 4 cursos» y «135 horas», y las tres cosas son falsas
aquí. Se hace nueva en el paso 5, con las horas del corpus de verdad.

## Por qué el paso 1 no se adivina

Tres fuentes describen el Diplomado con módulos distintos:

- **El temario oficial** (Drive, abril 2026): Fundamentos BIM · Hormigón armado ·
  Acero · Cimentaciones · Documentación · Coordinación (Navisworks) · Análisis
  (Robot/SAP2000) · Automatización (Dynamo) · Proyecto final.
- **El bot de ventas** (`claude_agent.py`): Modelado inicial · Acero
  sismorresistente · Conexiones precalificadas · HA sismorresistente · Refuerzo ·
  Cimentaciones · Documentación · MEP con Navisworks · Presupuestos.
- **Vimeo**: la carpeta «M8 - Diplomado de Estructuras» es de *instalaciones*,
  que no es el módulo 8 del temario.

Y la API de GoHighLevel no deja leer el contenido de los cursos. Si el tutor se
arma con una carpeta que no es del Diplomado, le contesta a un alumno con una
clase que no compró y le dice que está en su material.
