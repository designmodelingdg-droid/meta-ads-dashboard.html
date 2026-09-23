# Tutor IA del Diplomado BIM Estructuras — estado y montaje

**Publicado el 23-sep-2026** en
`https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-diplomado-estructuras/`.
Lo único que falta es el botón en el curso de GHL: ver `MONTAJE-GHL.md`.

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

## Estado

| # | Qué | Estado |
|---|---|---|
| 1 | Qué video de Vimeo es cada lección | HECHO: el curso en GHL y en la plataforma anterior (LeadGods #29586), leídos con Claude en Chrome |
| 2 | Bajar el corpus | HECHO: 190 videos, 115 h, módulos 2 a 9 |
| 3 | Probar y medir memoria | HECHO: 189 MB con los dos tutores |
| 4 | Fusionar el servidor (dma-sales-assistant #53) | HECHO |
| 5 | Publicar esta carpeta y hacer la tarjeta | HECHO |
| 6 | Custom Block en el curso del Diplomado en GHL | **Ester y Aylin** → `MONTAJE-GHL.md` |
| 7 | Subtítulos en español del Módulo 2 en Vimeo, y volver a bajar el corpus | En curso |
| — | Módulo 1 | Sin fuente: son videos nativos de GHL, sin Vimeo ni texto |

**La tarjeta (`img/tarjeta-tutor.png`) es propia**: la del Acero dice «de tu
Especialización» y «tus 4 cursos». Esta dice «de tu Diplomado» y las 115 horas
que de verdad tiene indexadas.

## Cómo se resolvió el paso 1

Tres fuentes describían el Diplomado con módulos distintos (el temario oficial,
el bot de ventas y los nombres de carpeta de Vimeo), y la API de GHL no deja
leer los cursos. Se resolvió leyendo el curso mismo: en GHL, lo que ve el
alumno, y en LeadGods, que guarda el número de Vimeo de cada lección. El
emparejamiento está en `dma-sales-assistant/tutor/fuentes/reparto-diplomado-estructuras.json`.
