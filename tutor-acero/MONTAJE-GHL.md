# Montar el Tutor IA en GoHighLevel

Para **Ester y Aylin**. Son dos montajes distintos y uno depende del otro:
primero las variables, después lo que se ve. Si se hace al revés, el chat le
dirá «token inválido» a todos los alumnos y parecerá que está roto.

La página del tutor ya está publicada y lista. No hay que editar código:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-acero/
```

---

## PASO 0 · Variables en Render (lo hace Dayana, va PRIMERO)

Servicio `dma-tutor` → **Environment** → añadir:

| Variable | Valor |
|---|---|
| `TOKEN_PAGINA` | `dma-pagina-b6a195471f0c4e23bae2898a` |
| `LIMITE_GLOBAL_DIA` | `600` |
| `CORS_ORIGENES` | `https://designmodelingdg-droid.github.io,https://designmodelingacademy.app.clientclub.net` |

Render redespliega solo al guardar. Para comprobar que quedó bien, abrir
[/tutor/salud](https://dma-tutor.onrender.com/tutor/salud): tiene que decir
`"ok":true`.

**Hasta que esto no esté hecho, no montar nada de lo de abajo.**

---

## PASO 1 · La lección dentro de los 4 cursos de ACERO

Va **solo** en estos cuatro. En ningún otro curso: el tutor únicamente conoce
estas clases y en un curso del Máster respondería «eso no está en el material»
a todo.

1. Análisis y Diseño Simplificado de Estructuras Complejas de Acero
2. Guía Práctica para el Cálculo Tipo Cerchas en Naves Industriales
3. Modelado BIM en Hormigón Armado y Acero Estructural
4. Teoría y Cálculo de Uniones Metálicas en Edificaciones

En cada uno:

1. Entrar al curso → **Categorías / Módulos**.
2. Crear una lección **al principio**, la primera de todas, llamada
   **`Tutor IA — pregúntale a tus clases`**.
3. En el cuerpo de la lección, insertar un bloque de **código personalizado**
   (Custom Code / HTML) y pegar esto tal cual:

```html
<iframe
  src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-acero/"
  style="width:100%;height:720px;border:0;border-radius:12px;display:block"
  title="Tutor IA · Especialización en Acero"
  loading="lazy"></iframe>
```

4. Guardar y publicar la lección.

**Que el bloque quede a ancho completo y sin relleno lateral.** Si el editor
deja margen a los lados, el chat sale estrecho y se lee mal en el teléfono.

**Comprobar antes de dar por hecho:** abrir la lección **como alumno** (no
desde el editor) y hacer una pregunta de verdad, por ejemplo
*«¿qué es el pandeo?»*. Tiene que responder y terminar citando la clase y el
minuto. Si dice «token inválido», falta el PASO 0.

---

## PASO 2 · El botón en la plantilla (aparece en todos los cursos)

Este sí es global, y por eso **el texto del botón tiene que decir que es solo
de Acero**: así un alumno del Máster entiende que no es para él antes de hacer
clic.

En la plantilla de la membresía, donde van los botones de navegación:

```html
<a href="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-acero/"
   target="_blank" rel="noopener"
   style="display:inline-flex;align-items:center;gap:8px;background:#0E2438;
          color:#fff;font-family:system-ui,sans-serif;font-weight:700;
          font-size:14px;text-decoration:none;padding:11px 18px;
          border-radius:999px;border:1px solid #E8A04A">
  <span style="font-size:16px">✦</span>
  Tutor IA · Especialización en Acero
</a>
```

---

## Lo que hay que saber antes de que pregunten

**No hay que activar a nadie.** No se emite nada por alumno. Quien entra al
área de miembros ya está autenticado por GoHighLevel, y con eso basta: un
alumno que se matricula el martes tiene tutor el martes.

**El tutor solo conoce esos 4 cursos.** Si alguien le pregunta por hormigón
armado o por BIM 4D, responderá que no está en el material y mandará a la
asesoría. Es a propósito, no es un fallo.

**Nunca da cifras de norma ni precios.** Ante «¿cuántos MPa es la fluencia del
A36?» remite a la norma vigente en vez de dictar el número, porque las
transcripciones automáticas deforman las cifras. Está probado: 17 casos, las
trampas repetidas 3 veces cada una.

**Hay dos topes al día.** 20 preguntas por navegador y 600 en todo el
servicio. Si un alumno agota las suyas, el mensaje le dice que mañana se
reinician y le ofrece la asesoría.

**Si algo falla, el orden para mirar:**

1. ¿`/tutor/salud` responde `"ok":true`? Si no, el servicio está caído.
2. ¿Dice «token inválido»? Falta `TOKEN_PAGINA` en Render o no coincide.
3. ¿No responde nada y la consola del navegador habla de CORS? Falta el
   dominio en `CORS_ORIGENES`.
4. ¿Dice «alcanzaste tus preguntas de hoy»? Está funcionando: es el tope.
