# Montar el Tutor IA en GoHighLevel

Para **Ester y Aylin**. Todo lo técnico ya está hecho y probado: el tutor está
en línea, responde citando la sesión y el minuto, y las variables del servidor
están puestas. Lo que falta es que aparezca dentro de los cursos.

**No hay que pegar código.** El editor de cursos de GHL no permite insertar
HTML en la lección — solo bloques con botón y enlace. Por eso el tutor va como
un **botón que abre su página**, no incrustado dentro de la clase.

Esta es la dirección del tutor, la misma en todos los sitios:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-acero/
```

---

## Dónde va, y dónde NO

Va **solo en los 4 cursos de la Especialización en Acero**:

1. Análisis y Diseño Simplificado de Estructuras Complejas de Acero
2. Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales
3. Modelado BIM en Hormigón Armado y Acero Estructural
4. Teoría y Cálculo de Uniones Metálicas en Edificaciones

**No va en la plantilla general ni en ningún curso del Máster.** El tutor solo
conoce esas cuatro clases: a un alumno del Máster le respondería «eso no está
en el material» a todo, y sería peor que no tener botón.

---

## Los pasos, en cada uno de los 4 cursos

1. Abrir el curso → **Editar** → en el selector **Páginas** elegir **Producto**
   (la portada del curso, la que ve el alumno al entrar).
2. Añadir un **Custom Block** en el cuerpo, arriba del todo o justo debajo del
   video de presentación.
3. Rellenar los campos del bloque **exactamente así**:

| Campo del bloque | Qué poner |
|---|---|
| Imagen | `tarjeta-tutor.png` (va adjunta con estas instrucciones) |
| Heading | `Tutor IA · pregúntale a tus clases` |
| Contenido | `Resuelve tus dudas con las clases de tus 4 cursos. Te dice en qué sesión y en qué minuto está la respuesta — y si algo no está en el material, te lo dice en vez de inventarlo.` |
| Button Text | `Abrir el Tutor IA` |
| Tipo de botón | Solid Button |
| Relleno del botón | `#0E2438` |
| Borde del botón | `#E8A04A` |
| Button Text (color) | `#FFFFFF` |
| Ir a la URL | la dirección de arriba, pegada completa |

4. **Guardar cambios.**
5. Repetir en los otros tres cursos.

### Si además se quiere dentro de las lecciones

Con el mismo Custom Block, en **Páginas → Lección**, para que el alumno lo
tenga a mano mientras estudia sin volver a la portada. Es opcional: con la
portada del curso ya se cumple.

---

## Comprobar antes de darlo por hecho

Abrir el curso **como alumno**, no desde el editor. Pulsar el botón y hacer una
pregunta de verdad, por ejemplo:

> ¿Qué es el pandeo?

Tiene que responder y **terminar citando la clase y el minuto**, así:

> *El pandeo es un fenómeno de inestabilidad que ocurre en elementos
> estructurales…*
> **FUENTES:** [221121 Sesión N°1-Acero-DM.mp4 · min 112:09]

Si eso pasa, está bien montado. **Avisar a Dayana cuando los 4 estén hechos**:
hasta que estén, la campaña de publicidad de ACERO no puede salir.

---

## Por qué esto último importa

El precio de la Especialización sube de $200 a **$225 justamente porque incluye
el tutor**. Si la campaña sale antes de que el tutor esté montado, un alumno
paga los $225 y no lo encuentra. Por eso el orden es: primero estos 4 cursos,
después la publicidad.

---

## Lo que hay que saber cuando pregunten

**No hay que activar a nadie.** No se emite ninguna clave por alumno. Quien
entra al área de miembros ya está identificado por GoHighLevel, y con eso
basta: un alumno que se matricula el martes tiene tutor el martes.

**El tutor solo conoce esos 4 cursos.** Si le preguntan por hormigón armado o
por BIM 4D, dirá que no está en el material y mandará a la asesoría. Es a
propósito.

**Nunca da cifras de norma ni precios.** Ante «¿cuántos MPa es la fluencia del
A36?» remite a la norma vigente en vez de dictar el número, porque las
transcripciones automáticas deforman las cifras. Está probado: 17 casos, con
las trampas repetidas 3 veces cada una.

**Hay dos topes al día.** 20 preguntas por navegador y 600 en todo el servicio.
Si un alumno agota las suyas, el mensaje le dice que mañana se reinician y le
ofrece la asesoría.

**El botón abre en otra pestaña.** Es a propósito: el alumno consulta y vuelve
a su clase sin perder dónde iba.

---

## Si algo falla, en este orden

| Qué se ve | Qué significa |
|---|---|
| La página no carga | Abrir la dirección directamente en el navegador. Si tampoco carga, avisar a Dayana. |
| «Token inválido» | Suele ser que el servidor estaba reiniciándose. Esperar dos minutos y recargar con Ctrl+Shift+R. Si sigue, es de Dayana. |
| No responde nada | Problema de permisos del dominio. Es de Dayana. |
| «Alcanzaste tus preguntas de hoy» | No es un fallo: es el tope diario funcionando. |
| «Eso no está en el material» | Tampoco es un fallo. La pregunta es de un tema que el tutor no conoce. |
